class BitStream:
    def __init__(self, bits):
        self._bs = bits[24:]
        
    def u(self,n):
        return self._bs.read(n).uint

    def f(self,n):
        return self.u(n)

    def ue(self):
        return self._bs.read('ue')
    
    def se(self):
        return self._bs.read('se')