class NALUnit:
    def __init__(self, bits):
        self._bits = bits

        self.read_nalunit_header()

    def __repr__(self):
        attrs = ', '.join(f'{k}={v}' for k, v in self.__dict__.items() if not k.startswith('_'))
        return f'NALU({attrs})'


    def read_nalunit_header(self):
        self.forbidden_zero_bit = self._bits.f(1)
        self.nal_unit_type = self._bits.u(6)
        self.nuh_layer_id = self._bits.u(6)
        self.nuh_temporal_id_plus1 = self._bits.u(3) - 1

        self.trace_nalunit_header()
    
    def trace_nalunit_header(self):
        print(f'*********** NAL UNIT ({self.nalunit_type_to_string(self.nal_unit_type)}) ***********')
        print(f'forbidden_zero_bit: {self.forbidden_zero_bit}')
        print(f'nal_unit_type: {self.nal_unit_type}')
        print(f'nuh_layer_id: {self.nuh_layer_id}')
        print(f'nuh_temporal_id_plus1: {self.nuh_temporal_id_plus1}')

    def nalunit_type_to_string(self, type):
        NalUnitType = {
            1: "TRAIL_R",
            0: "TRAIL_N",
            3: "TSA_R",
            2: "TSA_N",
            5: "STSA_R",
            4: "STSA_N",
            16: "BLA_W_LP",
            17: "BLA_W_RADL",
            18: "BLA_N_LP",
            19: "IDR_W_RADL",
            20: "IDR_N_LP",
            21: "CRA",
            7: "RADL_R",
            6: "RADL_N",
            9: "RASL_R",
            8: "RASL_N",
            32: "VPS",
            33: "SPS",
            34: "PPS",
            35: "AUD",
            36: "EOS",
            37: "EOB",
            38: "FILLER",
            39: "Prefix SEI",
            40: "Suffix SEI",
        }
        return NalUnitType.get(type, "UNK")



