from .nalunit import NALUnit

class BitStream:
    def __init__(self, bits):
        self._bs = bits[24:]

        self.convert_payload_rbsp()

    def __repr__(self):
        return f'BitStream(data:<{self._bs}>)'
        
    def u(self,n):
        return self._bs.read(n).uint

    def f(self,n):
        return self.u(n)

    def ue(self):
        return self._bs.read('ue')
    
    def se(self):
        return self._bs.read('se')
    
    # perform anti-emulation prevention
    def convert_payload_rbsp(self):
        self._bs.replace('0x000003', '0x0000', bytealigned=True)

    