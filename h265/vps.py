from enum import Enum

class ProfileIdc(Enum):
    NONE = 0
    MAIN = 1
    MAIN10 = 2
    MAINSTILLPICTURE = 3
    MAINREXT = 4
    HIGHTHROUGHPUTREXT = 5

class VPS:
    def __init__(self, bitstream):
        self._bits = bitstream
        self.general_profile_compatibility_flag = [0]*32

        self.parseVPS()
        self.rbsp_trailing_bits()
    
    def profile_tier_level(self):
        self.profile_space = self._bits.ReadCode("profile_space", 2)
        self.tier_flag = self._bits.ReadFlag("tier_flag")
        self.profile_idc = self._bits.ReadCode("profile_idc", 5)
        for j in range(32):
            self.general_profile_compatibility_flag[j] = self._bits.ReadFlag(f"general_profile_compatibility_flag[][{j}]")
        self.general_progressive_source_flag = self._bits.ReadFlag("general_progressive_source_flag")
        self.general_interlaced_source_flag = self._bits.ReadFlag("general_interlaced_source_flag")
        self.general_non_packed_constraint_flag = self._bits.ReadFlag("general_non_packed_constraint_flag")
        self.general_frame_only_constraint_flag = self._bits.ReadFlag("general_frame_only_constraint_flag")

        if self.profile_idc == ProfileIdc.MAINREXT.value or self.general_profile_compatibility_flag[ProfileIdc.MAINREXT.value] \
            or self.profile_idc == ProfileIdc.HIGHTHROUGHPUTREXT.value or self.general_profile_compatibility_flag[ProfileIdc.HIGHTHROUGHPUTREXT.value]:
            self.general_reserved_zero_44bits = self._bits.ReadCode("general_reserved_zero_44bits", 44)
        else:
            if self.profile_idc == ProfileIdc.MAIN.value or self.general_profile_compatibility_flag[ProfileIdc.MAIN.value]:
                self.general_reserved_zero_7bits = self._bits.ReadCode("general_reserved_zero_7bits", 7)
                self.one_picture_only_constraint_flag = self._bits.ReadFlag("general_one_picture_only_constraint_flag")
                self._bits.ReadCode("general_reserved_zero_35bits[0..15]", 16)
                self._bits.ReadCode("general_reserved_zero_35bits[16..31]", 16)
                self._bits.ReadCode("general_reserved_zero_35bits[32..34]", 3)
            else:
                self._bits.ReadCode("general_reserved_zero_35bits[0..15]", 16)
                self._bits.ReadCode("general_reserved_zero_35bits[16..31]", 16)
                self._bits.ReadCode("general_reserved_zero_35bits[32..42]", 11)

        if self.profile_idc >= ProfileIdc.MAIN.value and self.profile_idc <= ProfileIdc.HIGHTHROUGHPUTREXT.value \
            or self.general_profile_compatibility_flag[ProfileIdc.MAIN.value] \
            or self.general_profile_compatibility_flag[ProfileIdc.MAIN10.value] \
            or self.general_profile_compatibility_flag[ProfileIdc.MAINSTILLPICTURE.value] \
            or self.general_profile_compatibility_flag[ProfileIdc.MAINREXT.value]:
                self.general_inbld_flag = self._bits.ReadFlag("general_inbld_flag")
        else:
            self.general_reserved_zero_bit = self._bits.ReadFlag("general_reserved_zero_bit")
        
        self._bits.ReadCode("general_level_idc", 8)

            
    def parseVPS(self):
        print("=========== Video Parameter Set     ===========")
        self.video_parameter_set_id = self._bits.ReadCode("video_parameter_set_id", 4)
        self.vps_base_layer_internal_flag = self._bits.ReadFlag("vps_base_layer_internal_flag")
        self.vps_base_layer_available_flag = self._bits.ReadFlag("vps_base_layer_available_flag")
        self.vps_max_layers_minus1 = self._bits.ReadCode("vps_max_layers_minus1", 6)
        self.vps_max_sub_layers_minus1 = self._bits.ReadCode("vps_max_sub_layers_minus1", 3)
        self.vps_temporal_id_nesting_flag = self._bits.ReadFlag("vps_temporal_id_nesting_flag")
        self.vps_reserved_0xffff_16bits = self._bits.ReadCode("vps_reserved_0xffff_16bits", 16)
        self.profile_tier_level()
        self.vps_sub_layer_ordering_info_present_flag = self._bits.ReadFlag("vps_sub_layer_ordering_info_present_flag")

        startIndex = 0 if self.vps_sub_layer_ordering_info_present_flag else self.vps_max_sub_layers_minus1
        endIndex = self.vps_max_sub_layers_minus1 + 1

        self.vps_max_dec_pic_buffering_minus1 = {}
        self.vps_max_num_reorder_pics = {}
        self.vps_max_latency_increase_plus1 = {}
        for i in range(startIndex, endIndex):
            self.vps_max_dec_pic_buffering_minus1[i] = self._bits.ReadUVLC("vps_max_dec_pic_buffering_minus1")
            self.vps_max_num_reorder_pics[i] = self._bits.ReadUVLC("vps_max_num_reorder_pics")
            self.vps_max_latency_increase_plus1[i] = self._bits.ReadUVLC("vps_max_latency_increase_plus1")

        self.vps_max_layer_id = self._bits.ReadCode("vps_max_layer_id", 6)
        self.vps_num_layer_sets_minus1 = self._bits.ReadUVLC("vps_num_layer_sets_minus1")
        self.vps_timing_info_present_flag = self._bits.ReadFlag("vps_timing_info_present_flag")
        self.vps_extension_flag = self._bits.ReadFlag("vps_extension_flag")

    def rbsp_trailing_bits(self):
        self._bits.ReadFlag("rbsp_stop_one_bit")
        while not self._bits.byte_aligned():
            self._bits.ReadFlag("rbsp_alignment_zero_bit")