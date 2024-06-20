import bitstring

class BitStream:
    def __init__(self, filename):
        self._bits = bitstring.BitStream(filename=filename)
        self._nalus = list(self._bits.split('0x000001', bytealigned=True))[1:]

    def __getitem__(self, i):
        return self._nalus[i]
    
    def u(self,n):
        return self._bits.read(n).uint

    def f(self,n):
        return self.u(n)

    def ue(self):
        return self._bits.read('ue')
    
    def se(self):
        return self._bits.read('se')