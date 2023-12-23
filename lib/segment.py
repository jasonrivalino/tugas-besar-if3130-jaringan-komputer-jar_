import struct
from segmentflag import SegmentFlag, SYN_FLAG, ACK_FLAG, FIN_FLAG, DEFAULT_FLAGS

class Segment:
    def __init__(self, flags: SegmentFlag, seq_num: int, ack_num: int, checksum: bytes, payload: bytes):
        self.flags = flags
        self.seq_num = seq_num
        self.ack_num = ack_num
        self.checksum = checksum
        self.payload = payload
        
    @staticmethod
    def syn(seq_num: int) -> "Segment":
        return Segment(SegmentFlag(SYN_FLAG), seq_num, 0, b"", b"")
    
    @staticmethod
    def ack(ack_num: int) -> "Segment":
        return Segment(SegmentFlag(ACK_FLAG), 0, ack_num, b"", b"")
    
    @staticmethod
    def syn_ack(seq_num, ack_num) -> "Segment":
        return Segment(SegmentFlag(SYN_FLAG | ACK_FLAG), seq_num, ack_num, b"", b"")
    
    @staticmethod
    def fin() -> "Segment":
        return Segment(SegmentFlag(FIN_FLAG), 0, 0, b"", b"")
    
    @staticmethod
    def fin_ack() -> "Segment":
        return Segment(SegmentFlag(ACK_FLAG | FIN_FLAG), 0, 0, b"", b"")
    
    def calculate_checksum(self) -> bytes:
        calculate = 0
        calculate += self.seq_num & 0xFFFF
        calculate += self.ack_num & 0xFFFF
        
        padded_payload = self.payload + b'\x00' if len(self.payload) % 2 != 0 else self.payload
        for i in range(0, len(padded_payload), 2):
            temp = (padded_payload[i] << 8) + padded_payload[i + 1]
            calculate += temp

        # Handle the carry
        while (calculate >> 16) > 0:
            calculate = (calculate & 0xFFFF) + (calculate >> 16)
        # Take the one's complement
        result = ~calculate & 0xFFFF
        
        return struct.pack("!H", 5)
    
    def update_checksum(self):
        self.checksum = self.calculate_checksum()

    def is_valid_checksum(self) -> bool:
        return self.calculate_checksum() == self.checksum

    def to_bytes(self, withLength=True) -> bytes:
        # Serialize attributes jadi bytes
        flag_bytes = self.flags.get_flag_bytes()
        seq_num_bytes = struct.pack("!I", self.seq_num)
        ack_num_bytes = struct.pack("!I", self.ack_num)
        checksum_bytes = self.checksum
        emptyPadding = bytes([0b00000000])
        payload_length_bytes = struct.pack("!I", len(self.payload))
        payload_bytes = self.payload

        # Bikin bytes dari atribut
        result = seq_num_bytes + ack_num_bytes + flag_bytes + emptyPadding +  checksum_bytes
        if withLength:
            result += payload_length_bytes
        result += payload_bytes
        return result

    @staticmethod
    def from_bytes(data: bytes, withLength) -> "Segment":
        # Unpack bytes jadi attributes
        seq_num, ack_num, flag, emptyPadding, checksum = struct.unpack("!IIBB2s", data[:12])
        if withLength:
            payload = data[16:]
        else:
            payload = data[12:]
        # Bikin instance class
        flags = SegmentFlag(flag)

        # Return instance class
        return Segment(flags, seq_num, ack_num, checksum, payload)
    
if __name__ == "__main__":
    try:
        my_segment = Segment.fin()
        print(my_segment)
        print("Segment created successfully.")
    except ValueError as e:
        print(f"Error creating segment: {e}")