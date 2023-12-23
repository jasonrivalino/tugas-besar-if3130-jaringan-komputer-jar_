import socket
from abc import ABC, abstractmethod
from connection import Connection
from messageinfo import MessageInfo
from segment import Segment

class Node(ABC):
    def __init__(self, ip: str, port: int, socket: socket, handler: callable(MessageInfo)):
        self.connection = Connection(ip, port, socket, handler)
    
    @abstractmethod
    def run():
        pass

    @abstractmethod
    def handle_message(segment: Segment):
        pass