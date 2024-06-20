class NALUnit:
    def __init__(self, bitstream):
        self._bs = bitstream
        self.__dict__['forbidden_zero_bit'] = self._bs.f(1)
        self.__dict__['nal_ref_idc'] = self._bs.u(2)
        self.__dict__['nal_unit_type'] = self._bs.u(5)

    def __repr__(self):
        attrs = ', '.join(f'{k}={v}' for k, v in self.__dict__.items() if not k.startswith('_'))
        return f'NALU({attrs})'
    
