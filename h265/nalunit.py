from .vps import VPS

class NALUnit:
    def __init__(self, bitstream):
        self._bs = bitstream

        self.readNalUnitHeader()

        if self.nal_unit_type == 32:
           self._bs.vps = VPS(self._bs)

    def __repr__(self):
        attrs = ', '.join(f'{k}={v}' for k, v in self.__dict__.items() if not k.startswith('_'))
        return f'NALU({attrs})'

    def readNalUnitHeader(self):
        self.forbidden_zero_bit = self._bs.f(1)
        self.nal_unit_type = self._bs.u(6)
        self.nuh_layer_id = self._bs.u(6)
        self.nuh_temporal_id_plus1 = self._bs.u(3) - 1

