from .globals import GET_SYMBOL_COUNT, INC_SYMBOL_COUNT

class BitStream:
    def __init__(self, bits):
        self._bits = bits[24:]

        self.convert_payload_rbsp()

    def __repr__(self):
        return f'BitStream(data:<{self._bits}>)'
        
    def u(self,n):
        return self._bits.read(n).uint

    def f(self,n):
        return self.u(n)

    def ue(self):
        return self._bits.read('ue')
    
    def se(self):
        return self._bits.read('se')
    
    # perform anti-emulation prevention
    def convert_payload_rbsp(self):
        self._bits.replace('0x000003', '0x0000', bytealigned=True)

    def ReadCode(self, symbolName, uiLength):
        rValue = self.u(uiLength)

        descriptor = f"u({uiLength})"
        print(f"{GET_SYMBOL_COUNT():>8}  {symbolName:50} {descriptor:5} : {rValue}")
        INC_SYMBOL_COUNT()
        
        return rValue
    
    def ReadFlag(self, symbolName):
        return self.ReadCode(symbolName, 1)

    
