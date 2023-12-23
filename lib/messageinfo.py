from segment import Segment

class MessageInfo:
    def __init__(self, ip, port, segment):
        self.ip = ip
        self.port = port
        self.segment = segment
    
    # Setter
    def setIP(self, ip):
        self.ip = ip

    def setPort(self, port):
        self.port = port
    
    def setSegment(self, segment):
        self.segment = segment

    # Getter
    def getIP(self):
        return self.ip
    
    def getPort(self):
        return self.port
    
    def getSegment(self):
        return self.segment

    # String representation
    def __str__(self):
        return f"IP: {self.ip}, Port: {self.port}, Segment: {self.segment}"