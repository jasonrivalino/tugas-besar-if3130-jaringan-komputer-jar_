import socket
from messageinfo import MessageInfo
from segment import Segment

class Connection:
    def __init__(self, ip: str, port: int, socket: socket, handler: callable(MessageInfo)):
        self.ip = ip
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.handler = handler
        self.socket.bind((self.ip, self.port))

    def send(self, ip_remote: str, port_remote: int, message: str):
        print("Sending...")
        self.socket.sendto(message.encode('latin-1'), (ip_remote, port_remote))
    
    def listen(self):
        print("Server listening...")
        while True:
            try:
                self.socket.settimeout(5)
                data, address = self.socket.recvfrom(32768)
                print(f"Received data from {address}")
                return data.decode('latin-1'), address
            except socket.timeout:
                raise
    
    def close(self):
        self.socket.close()

    def register_handler(self, handler: callable(MessageInfo)):
        self.handler = handler

    def notify(self, data: str, withLength=True):
        if self.handler is not None:
            # return data
            segment = Segment.from_bytes(data.encode("latin-1"), withLength)
            return self.handler(segment)

    def connect(self):
        print("Connecting...")
        self.socket.connect((self.ip, self.port))

    def set_timeout(self, timeout):
        self.socket.settimeout(timeout)