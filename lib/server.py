import socket
from connection import Connection
from segment import Segment
from segmentflag import SegmentFlag, SYN_FLAG, ACK_FLAG, FIN_FLAG, DEFAULT_FLAGS
from node import Node
from messageinfo import MessageInfo
from splashscreen import splashscreen
import struct
import argparse
import os

class Server(Node):
    def __init__(self, ip: str, port: int, socket: socket):
        super().__init__(ip, port, socket, self.handle_message)
        self.clientList = []

    def get_address(self):
        return f"{self.connection.ip}:{self.connection.port}"

    def addClient(self, clientIp, clientPort):
        self.clientList.append([clientIp, clientPort])

    def run(self, path_input):
        splashscreen.splashscreen()
        print("[!] Server started at localhost:", self.connection.port)
        print("[!] Source file |", path_input , "|", os.path.getsize(path_input), "bytes")
        print("[!] Listening to broadcast address for clients...")
        self.three_way_handshake()
        while(len(self.clientList)):
            self.file_transfer(self.clientList[0][0], self.clientList[0][2][0], self.clientList[0][2][1], self.sliceBinaryFile(path_input))

    def handle_message(self, segment: Segment):
        if segment.flags.get_flag_bytes() == bytes([SYN_FLAG]):
            return Segment.syn_ack(segment.seq_num + 1, segment.seq_num)
        elif segment.flags.get_flag_bytes() == bytes([ACK_FLAG]) or segment.flags.get_flag_bytes() == bytes([FIN_FLAG | ACK_FLAG]):
            return segment

    def three_way_handshake(self):
        # Terima SYN
        listening = 'y'
        clientCount = 0
        clientMap = {}
        while listening=='y':
            try:
                data, address = self.connection.listen()
                print(f"[!] Received request from {address[0]}:{address[1]}")
                clientCount += 1
                self.clientList.append([f"CLIENT{clientCount}", data, address])
                clientMap[address[1]] = f"CLIENT{clientCount}"
                listening = input("[?] Listen more? (y/n) ")
                print()
            except socket.timeout:
                print("[!] Receive timeout reached.")

        print("Client list:")
        for clientName, data, address in self.clientList:
            print(f"{clientName} = {address[0]}:{address[1]}")

        print()

        for clientName, data, address in self.clientList:
            response = self.connection.notify(data)
            if response is not None:
                self.connection.send(address[0], address[1], response.to_bytes().decode("latin-1"))
                print(f"[{clientName}] Sending SYN-ACK to {address[0]}:{address[1]} with sequence number = {response.seq_num}")
                print(f"[{clientName}] Waiting for response")
        # Terima ACK
        ackList = []
        while len(ackList)!=len(self.clientList):
            try:
                data, address = self.connection.listen()
                ackList.append([clientMap[address[1]], data, address])
            except socket.timeout:
                print("[!] Receive timeout reached.")
        waitingResponse = True
        while waitingResponse:
            if len(ackList)==len(self.clientList):
                for clientName, data, address in ackList:
                    response = self.connection.notify(data)
                    if (
                        response.flags.get_flag_bytes() == bytes([ACK_FLAG])
                        and response.ack_num == 1
                    ):
                        print(f"[{clientName}] Received ACK from {address[0]}:{address[1]} with sequence number = {response.seq_num}")
                waitingResponse = False

    def send_segment(self, clientName, clientip, clientport, slicedFile, sequence_base, sequence_number, sequence_max, segment_count):
        print()
        while sequence_base <= sequence_number <= sequence_max and sequence_number < segment_count:
            segment = Segment(SegmentFlag(DEFAULT_FLAGS), sequence_number, 0, b"", slicedFile[sequence_number])
            segment.update_checksum()
            self.connection.send(clientip, clientport, segment.to_bytes(False).decode("latin-1"))
            print(f"[{clientName}] Server sent segment to {clientip}:{clientport} with sequence number = {sequence_number}.")
            sequence_number += 1
        return sequence_number

    def file_transfer(self, clientName, clientip, clientport, slicedFile):
        N = 3
        sequence_number = 0
        sequence_base = 0
        sequence_max = N - 1
        segment_count = len(slicedFile)
        
        while True:
            # Kondisi pengiriman segment00
            sequence_number = self.send_segment(clientName, clientip, clientport, slicedFile, sequence_base, sequence_number, sequence_max, segment_count)      
            # Kondisi menerima ACK
            try:
                ack, address = self.connection.listen()
                response = self.connection.notify(ack, False)
                if (response.flags.get_flag_bytes() == bytes([ACK_FLAG])):
                    print(f"[{clientName}] Server recieved acknowledgement from {clientip}:{clientport} with acknowledgement number = {response.ack_num}")
                    if response.ack_num == sequence_base:
                        # update segment base
                        if sequence_base + 1 == segment_count:
                            print(f"[{clientName}] All segment have been sent to {clientip}:{clientport}")
                            break
                        else:
                            sequence_base = response.ack_num+1
                            sequence_max = sequence_base + (N - 1)
                            print(f"Sequence base updated to {sequence_base}, sequence max updated to {sequence_max}, current sequence number = {sequence_number}")
                    else:
                        continue
                else:
                    raise Exception("ACK not received.")
            except socket.timeout:
                print(f"[{clientName}] Received timeout reached. Retransmitting segment with sequence number = {sequence_base}")
                sequence_number = self.send_segment(clientName, clientip, clientport, slicedFile, sequence_base, sequence_base, sequence_max, segment_count)
                continue
            except Exception as e:
                print(f"[{clientName}] Acknowledgement not received. Retransmitting segment with sequence number = {sequence_base}")
                sequence_number = self.send_segment(clientName, clientip, clientport, slicedFile, sequence_base, sequence_base, sequence_max, segment_count)
                continue
            
        # Terima timeout
        print()
        print("Server closing connection.")
        print()
        self.close_connection(clientName, clientip, clientport)

    def close_connection(self, clientName, clientip, clientport):
        # kirim FIN ke client
        while True:
            fin = Segment.fin()
            print(f"[{clientName}] Sending FIN request to {clientip}:{clientport}")
            self.connection.send(clientip, clientport, fin.to_bytes().decode("latin-1"))
            try:
                # terima Fin-Ack
                fin_ack, address = self.connection.listen()
                response = self.connection.notify(fin_ack, False)
                if (response.flags.get_flag_bytes() == bytes([FIN_FLAG | ACK_FLAG]) and address[0] == clientip and address[1] == clientport):
                    print(f"[{clientName}] Server received FIN-ACK. closing connection with {address[0]}:{address[1]}")
                    for client in self.clientList:
                        if (client[0]==clientName):
                            self.clientList.remove(client)
                    if not len(self.clientList):
                        print()
                        print("All client connection have been closed. Closing server connection")
                        self.connection.close()
                    break
                else:
                    raise Exception("ACK not received.")
            except socket.timeout:
                print("FIN-ACK Not Received. Retransmitting FIN request")
                continue
            except Exception as e:
                print(e)
                continue
            
    def sliceBinaryFile(self, filePath):
        with open(filePath, 'rb') as file:
            binaryData = file.read()
        
            
        slicedFile = []
        currentByte = 0
        window = 32756
        while currentByte<len(binaryData):
            if (currentByte + window) >= len(binaryData):
                window = len(binaryData)%window
            slicedFile.append(binaryData[currentByte:currentByte+window])
            currentByte += window
        
        return slicedFile

if __name__ == "__main__":
    # Argument parsing
    parser = argparse.ArgumentParser()
    parser.add_argument("server_port", help="Server port", type=int)
    parser.add_argument("path_input", help="File path", type=str)
    args = parser.parse_args()
    server = Server("127.0.0.1", args.server_port, socket)
    server.run(args.path_input)
