import struct

SYN_FLAG = 0b00100010
ACK_FLAG = 0b00010000
FIN_FLAG = 0b00000001
DEFAULT_FLAGS = 0b00000000

class SegmentFlag:
    def __init__(self, flag : bytes):
        self.syn = False
        self.ack = False
        self.fin = False
        
        # Cek apakah flag tipe datanya valid
        if SYN_FLAG & flag:
            self.syn = True
        if ACK_FLAG & flag:
            self.ack = True
        if FIN_FLAG & flag:
            self.fin = True

    def get_flag_bytes(self) -> bytes:
        # Inisialisasi flag byte dengan default
        default_flags = DEFAULT_FLAGS
    
        if self.syn:
            default_flags |= SYN_FLAG
        if self.ack:
            default_flags |= ACK_FLAG
        if self.fin:
            default_flags |= FIN_FLAG

        return struct.pack("!B", default_flags)
    
if __name__ == "__main__":
    syn = SegmentFlag(SYN_FLAG)
    ack = SegmentFlag(ACK_FLAG)
    print(syn.get_flag_bytes())