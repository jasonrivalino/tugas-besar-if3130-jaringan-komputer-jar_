import socket
from connection import Connection
from  segment import Segment
from  segmentflag import SegmentFlag, SYN_FLAG, ACK_FLAG, FIN_FLAG, DEFAULT_FLAGS
from node import Node
from messageinfo import MessageInfo
import struct
import argparse
from splashscreen import splashscreen

class Client(Node):
    def __init__(self, serverIp: str, serverPort: int, ip: str, port: int, socket: socket):
        super().__init__(ip, port, socket, self.handle_message)
        self.serverIp = serverIp
        self.serverPort = serverPort

    # Fungsi untuk mengembalikan alamat IP dan port
    def getAddress(self):
        return f"{self.connection.ip}:{self.connection.port}"
    
    def getServerAddress(self):
        return f"{self.serverIp}:{self.serverPort}"
    
    def run(self, path_output):
        splashscreen.splashscreen()
        self.three_way_handshake()
        self.listen_file_transfer(path_output)

    def handle_message(self, segment: Segment):
        if (segment.flags.get_flag_bytes()==bytes([SYN_FLAG | ACK_FLAG])):
            return Segment.ack(segment.seq_num)
        elif (segment.flags.get_flag_bytes()==bytes([FIN_FLAG])):
            # self.connection.close()
            return Segment.fin_ack()
        else:
            return segment
          
    def three_way_handshake(self) -> bool:
        # Kirim SYN
        print("Initiating three way handshake ...")
        print()
        syn = Segment.syn(0)
        self.connection.send(self.serverIp, self.serverPort, syn.to_bytes().decode('latin-1'))
        print(f"[HANDSHAKE]  Sending broadcast SYN request with sequence number {syn.seq_num} to port {self.serverPort}")
        print("[HANDSHAKE] Waiting for response ...")
        # Terima SYN-ACK
        while True:
            try:
                try:
                    data, address = self.connection.listen()
                    response = self.connection.notify(data)
                    # Kirim ACK
                    if ((response.flags.get_flag_bytes() == bytes([ACK_FLAG])) and (response.ack_num == 1)):
                        print(f"[HANDSHAKE] Response received. sequence number = {response.ack_num}, acknowledge number = {response.ack_num-1}")
                        self.connection.send(self.serverIp, self.serverPort, response.to_bytes().decode("latin-1"))
                        print(f"[HANDSHAKE] Sending ACK request with sequence number {response.ack_num} to port {self.serverPort}")
                        return True
                except Exception as e:
                    print(e)
                    continue
            except socket.timeout:
                print("Receive timeout reached.")
                continue
            
    def listen_file_transfer(self, filePath):
        # Implementasi file transfer dengan GO-BACK-N
        Rn = 0
        slicedFile = []
        print()
        print("Initiation file transfer...")
        print()

        # Melakukan perulangan sampai semua paket terkirim
        while True:               
             # Menerima paket dari server
            try:
                data, address = self.connection.listen()
                segment = self.connection.notify(data, False)
                if (segment is not None):
                    if (segment.is_valid_checksum()):
                        print(f"Client received data with sequence number = {segment.seq_num}")
                        print(f"Sending acknowledgement with ack_num = {segment.seq_num}")
                        if (segment.seq_num == Rn): 
                            slicedFile.append(segment.payload)
                            Rn += 1
                        self.connection.send(self.serverIp, self.serverPort, Segment.ack(segment.seq_num).to_bytes().decode("latin-1"))
                    elif(segment.flags.get_flag_bytes()==bytes([FIN_FLAG | ACK_FLAG])):
                        print()
                        print(f"FIN Received. Closing connection")
                        self.connection.send(self.serverIp, self.serverPort, Segment.fin_ack().to_bytes().decode("latin-1"))
                        break
            except Exception as e:
                print(e)
                continue     
        
        with open(filePath, 'wb') as file:
            file.write(b"".join(slicedFile))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Client")
    parser.add_argument("client_port", help="Client port", type=int)
    parser.add_argument("server_port", help="Server port", type=int)
    parser.add_argument("path_output", help="File path", type=str)
    args = parser.parse_args()
    client = Client("127.0.0.1", args.server_port, "127.0.0.1", args.client_port, socket)
    client.run(args.path_output)