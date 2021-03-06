#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: LilacSat-2 decoder
# Author: Daniel Estevez
# Description: LilacSat-2 decoder
# Generated: Wed Aug 31 15:25:09 2016
##################################################

from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import lilacsat
import sids


class lilacsat2(gr.top_block):

    def __init__(self, bfo=12000, callsign="", invert=-1, ip="::", latitude=0, longitude=0, port=7355, recstart=""):
        gr.top_block.__init__(self, "LilacSat-2 decoder")

        ##################################################
        # Parameters
        ##################################################
        self.bfo = bfo
        self.callsign = callsign
        self.invert = invert
        self.ip = ip
        self.latitude = latitude
        self.longitude = longitude
        self.port = port
        self.recstart = recstart

        ##################################################
        # Variables
        ##################################################
        self.sub_sps = sub_sps = 32
        self.sub_nfilts = sub_nfilts = 16
        self.sub_alpha = sub_alpha = 0.35
        self.sps = sps = 5
        self.samp_per_sym = samp_per_sym = 5
        self.nfilts = nfilts = 16
        self.alpha = alpha = 0.35
        
        self.variable_constellation_0_0 = variable_constellation_0_0 = digital.constellation_calcdist(([-1, 1]), ([0, 1]), 2, 1).base()
        
        
        self.variable_constellation_0 = variable_constellation_0 = digital.constellation_calcdist(([-1, 1]), ([0, 1]), 2, 1).base()
        
        self.sub_rrc_taps = sub_rrc_taps = firdes.root_raised_cosine(sub_nfilts, sub_nfilts, 1.0/float(sub_sps), sub_alpha, 11*sub_sps*sub_nfilts)
        self.samp_rate = samp_rate = 48000
        self.rrc_taps_0 = rrc_taps_0 = firdes.root_raised_cosine(nfilts, nfilts, 1.0/float(samp_per_sym), 0.35, 11*samp_per_sym*nfilts)
        self.rrc_taps = rrc_taps = firdes.root_raised_cosine(nfilts, nfilts, 1.0/float(sps), alpha, 11*sps*nfilts)
        self.nfilts_0 = nfilts_0 = 16

        ##################################################
        # Blocks
        ##################################################
        self.sids_submit_0 = sids.submit("http://tlm.pe0sat.nl/tlmdb/frame_db.php", 40908, callsign, longitude, latitude, recstart)
        self.low_pass_filter_0 = filter.fir_filter_fff(5, firdes.low_pass(
        	1, samp_rate, 3000, 1000, firdes.WIN_HAMMING, 6.76))
        self.lilacsat_vitfilt27_fb_0_0 = lilacsat.vitfilt27_fb()
        self.lilacsat_vitfilt27_fb_0 = lilacsat.vitfilt27_fb()
        self.lilacsat_kiss_decode_pdu_0_1 = lilacsat.kiss_decode_pdu()
        self.lilacsat_kiss_decode_pdu_0_0 = lilacsat.kiss_decode_pdu()
        self.lilacsat_kiss_decode_pdu_0 = lilacsat.kiss_decode_pdu()
        self.lilacsat_fec_decode_b_0_0_2 = lilacsat.fec_decode_b(114, False, False, False)
        self.lilacsat_fec_decode_b_0_0_0_0 = lilacsat.fec_decode_b(114, True, False, False)
        self.lilacsat_fec_decode_b_0_0_0 = lilacsat.fec_decode_b(114, True, False, False)
        self.lilacsat_fec_decode_b_0_0 = lilacsat.fec_decode_b(114, False, True, False)
        self.lilacsat_fec_decode_b_0 = lilacsat.fec_decode_b(114, False, True, False)
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_fcf(1, (firdes.low_pass(1, samp_rate, 10000, 1000)), bfo, samp_rate)
        self.digital_pfb_clock_sync_xxx_0_0 = digital.pfb_clock_sync_fff(sub_sps, 0.0628, (sub_rrc_taps), sub_nfilts, sub_nfilts/2, 0.01, 1)
        self.digital_pfb_clock_sync_xxx_0 = digital.pfb_clock_sync_ccf(sps, 0.100, (rrc_taps), nfilts, nfilts/2, 1.5, 2)
        self.digital_lms_dd_equalizer_cc_0_0 = digital.lms_dd_equalizer_cc(2, 0.3, 2, variable_constellation_0)
        self.digital_fll_band_edge_cc_0 = digital.fll_band_edge_cc(sps, 0.350, 100, 0.1)
        self.digital_costas_loop_cc_0_0 = digital.costas_loop_cc(0.4, 2, False)
        self.digital_clock_recovery_mm_xx_0 = digital.clock_recovery_mm_ff(10, 0.25*0.175*0.175, 0.5, 0.175, 0.005)
        self.digital_binary_slicer_fb_0 = digital.binary_slicer_fb()
        self.dc_blocker_xx_0 = filter.dc_blocker_ff(1024, True)
        self.blocks_unpack_k_bits_bb_0_0_0_0 = blocks.unpack_k_bits_bb(8)
        self.blocks_unpack_k_bits_bb_0_0_0 = blocks.unpack_k_bits_bb(8)
        self.blocks_udp_source_0 = blocks.udp_source(gr.sizeof_short*1, ip, port, 1472, False)
        self.blocks_threshold_ff_0 = blocks.threshold_ff(0, 0, 0)
        self.blocks_short_to_float_0 = blocks.short_to_float(1, 32767)
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_vff((invert*10, ))
        self.blocks_message_debug_0 = blocks.message_debug()
        self.blocks_float_to_char_0 = blocks.float_to_char(1, 1)
        self.blocks_delay_0_0 = blocks.delay(gr.sizeof_float*1, 1)
        self.blocks_delay_0 = blocks.delay(gr.sizeof_char*1, 1)
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)
        self.analog_feedforward_agc_cc_0 = analog.feedforward_agc_cc(1024, 2)

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.lilacsat_fec_decode_b_0, 'out'), (self.lilacsat_kiss_decode_pdu_0, 'in'))    
        self.msg_connect((self.lilacsat_fec_decode_b_0_0, 'out'), (self.lilacsat_kiss_decode_pdu_0, 'in'))    
        self.msg_connect((self.lilacsat_fec_decode_b_0_0_0, 'out'), (self.lilacsat_kiss_decode_pdu_0_0, 'in'))    
        self.msg_connect((self.lilacsat_fec_decode_b_0_0_0_0, 'out'), (self.lilacsat_kiss_decode_pdu_0_0, 'in'))    
        self.msg_connect((self.lilacsat_fec_decode_b_0_0_2, 'out'), (self.lilacsat_kiss_decode_pdu_0_1, 'in'))    
        self.msg_connect((self.lilacsat_kiss_decode_pdu_0, 'out'), (self.blocks_message_debug_0, 'print_pdu'))    
        self.msg_connect((self.lilacsat_kiss_decode_pdu_0, 'out'), (self.sids_submit_0, 'in'))    
        self.msg_connect((self.lilacsat_kiss_decode_pdu_0_0, 'out'), (self.blocks_message_debug_0, 'print_pdu'))    
        self.msg_connect((self.lilacsat_kiss_decode_pdu_0_0, 'out'), (self.sids_submit_0, 'in'))    
        self.msg_connect((self.lilacsat_kiss_decode_pdu_0_1, 'out'), (self.blocks_message_debug_0, 'print_pdu'))    
        self.msg_connect((self.lilacsat_kiss_decode_pdu_0_1, 'out'), (self.sids_submit_0, 'in'))    
        self.connect((self.analog_feedforward_agc_cc_0, 0), (self.digital_fll_band_edge_cc_0, 0))    
        self.connect((self.blocks_complex_to_real_0, 0), (self.blocks_delay_0_0, 0))    
        self.connect((self.blocks_complex_to_real_0, 0), (self.lilacsat_vitfilt27_fb_0, 0))    
        self.connect((self.blocks_delay_0, 0), (self.lilacsat_fec_decode_b_0_0, 0))    
        self.connect((self.blocks_delay_0_0, 0), (self.lilacsat_vitfilt27_fb_0_0, 0))    
        self.connect((self.blocks_float_to_char_0, 0), (self.lilacsat_fec_decode_b_0_0_2, 0))    
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.digital_clock_recovery_mm_xx_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.low_pass_filter_0, 0))    
        self.connect((self.blocks_short_to_float_0, 0), (self.blocks_multiply_const_vxx_0_0, 0))    
        self.connect((self.blocks_short_to_float_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))    
        self.connect((self.blocks_threshold_ff_0, 0), (self.blocks_float_to_char_0, 0))    
        self.connect((self.blocks_udp_source_0, 0), (self.blocks_short_to_float_0, 0))    
        self.connect((self.blocks_unpack_k_bits_bb_0_0_0, 0), (self.lilacsat_fec_decode_b_0_0_0_0, 0))    
        self.connect((self.blocks_unpack_k_bits_bb_0_0_0_0, 0), (self.lilacsat_fec_decode_b_0_0_0, 0))    
        self.connect((self.dc_blocker_xx_0, 0), (self.digital_pfb_clock_sync_xxx_0_0, 0))    
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.blocks_delay_0, 0))    
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.lilacsat_fec_decode_b_0, 0))    
        self.connect((self.digital_clock_recovery_mm_xx_0, 0), (self.digital_binary_slicer_fb_0, 0))    
        self.connect((self.digital_costas_loop_cc_0_0, 0), (self.digital_lms_dd_equalizer_cc_0_0, 0))    
        self.connect((self.digital_fll_band_edge_cc_0, 0), (self.digital_pfb_clock_sync_xxx_0, 0))    
        self.connect((self.digital_lms_dd_equalizer_cc_0_0, 0), (self.blocks_complex_to_real_0, 0))    
        self.connect((self.digital_pfb_clock_sync_xxx_0, 0), (self.digital_costas_loop_cc_0_0, 0))    
        self.connect((self.digital_pfb_clock_sync_xxx_0_0, 0), (self.blocks_threshold_ff_0, 0))    
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.analog_feedforward_agc_cc_0, 0))    
        self.connect((self.lilacsat_vitfilt27_fb_0, 0), (self.blocks_unpack_k_bits_bb_0_0_0, 0))    
        self.connect((self.lilacsat_vitfilt27_fb_0_0, 0), (self.blocks_unpack_k_bits_bb_0_0_0_0, 0))    
        self.connect((self.low_pass_filter_0, 0), (self.dc_blocker_xx_0, 0))    

    def get_bfo(self):
        return self.bfo

    def set_bfo(self, bfo):
        self.bfo = bfo
        self.freq_xlating_fir_filter_xxx_0.set_center_freq(self.bfo)

    def get_callsign(self):
        return self.callsign

    def set_callsign(self, callsign):
        self.callsign = callsign

    def get_invert(self):
        return self.invert

    def set_invert(self, invert):
        self.invert = invert
        self.blocks_multiply_const_vxx_0_0.set_k((self.invert*10, ))

    def get_ip(self):
        return self.ip

    def set_ip(self, ip):
        self.ip = ip

    def get_latitude(self):
        return self.latitude

    def set_latitude(self, latitude):
        self.latitude = latitude

    def get_longitude(self):
        return self.longitude

    def set_longitude(self, longitude):
        self.longitude = longitude

    def get_port(self):
        return self.port

    def set_port(self, port):
        self.port = port

    def get_recstart(self):
        return self.recstart

    def set_recstart(self, recstart):
        self.recstart = recstart

    def get_sub_sps(self):
        return self.sub_sps

    def set_sub_sps(self, sub_sps):
        self.sub_sps = sub_sps
        self.set_sub_rrc_taps(firdes.root_raised_cosine(self.sub_nfilts, self.sub_nfilts, 1.0/float(self.sub_sps), self.sub_alpha, 11*self.sub_sps*self.sub_nfilts))

    def get_sub_nfilts(self):
        return self.sub_nfilts

    def set_sub_nfilts(self, sub_nfilts):
        self.sub_nfilts = sub_nfilts
        self.set_sub_rrc_taps(firdes.root_raised_cosine(self.sub_nfilts, self.sub_nfilts, 1.0/float(self.sub_sps), self.sub_alpha, 11*self.sub_sps*self.sub_nfilts))

    def get_sub_alpha(self):
        return self.sub_alpha

    def set_sub_alpha(self, sub_alpha):
        self.sub_alpha = sub_alpha
        self.set_sub_rrc_taps(firdes.root_raised_cosine(self.sub_nfilts, self.sub_nfilts, 1.0/float(self.sub_sps), self.sub_alpha, 11*self.sub_sps*self.sub_nfilts))

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.set_rrc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts, 1.0/float(self.sps), self.alpha, 11*self.sps*self.nfilts))

    def get_samp_per_sym(self):
        return self.samp_per_sym

    def set_samp_per_sym(self, samp_per_sym):
        self.samp_per_sym = samp_per_sym
        self.set_rrc_taps_0(firdes.root_raised_cosine(self.nfilts, self.nfilts, 1.0/float(self.samp_per_sym), 0.35, 11*self.samp_per_sym*self.nfilts))

    def get_nfilts(self):
        return self.nfilts

    def set_nfilts(self, nfilts):
        self.nfilts = nfilts
        self.set_rrc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts, 1.0/float(self.sps), self.alpha, 11*self.sps*self.nfilts))
        self.set_rrc_taps_0(firdes.root_raised_cosine(self.nfilts, self.nfilts, 1.0/float(self.samp_per_sym), 0.35, 11*self.samp_per_sym*self.nfilts))

    def get_alpha(self):
        return self.alpha

    def set_alpha(self, alpha):
        self.alpha = alpha
        self.set_rrc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts, 1.0/float(self.sps), self.alpha, 11*self.sps*self.nfilts))

    def get_variable_constellation_0_0(self):
        return self.variable_constellation_0_0

    def set_variable_constellation_0_0(self, variable_constellation_0_0):
        self.variable_constellation_0_0 = variable_constellation_0_0

    def get_variable_constellation_0(self):
        return self.variable_constellation_0

    def set_variable_constellation_0(self, variable_constellation_0):
        self.variable_constellation_0 = variable_constellation_0

    def get_sub_rrc_taps(self):
        return self.sub_rrc_taps

    def set_sub_rrc_taps(self, sub_rrc_taps):
        self.sub_rrc_taps = sub_rrc_taps
        self.digital_pfb_clock_sync_xxx_0_0.update_taps((self.sub_rrc_taps))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, 3000, 1000, firdes.WIN_HAMMING, 6.76))
        self.freq_xlating_fir_filter_xxx_0.set_taps((firdes.low_pass(1, self.samp_rate, 10000, 1000)))

    def get_rrc_taps_0(self):
        return self.rrc_taps_0

    def set_rrc_taps_0(self, rrc_taps_0):
        self.rrc_taps_0 = rrc_taps_0

    def get_rrc_taps(self):
        return self.rrc_taps

    def set_rrc_taps(self, rrc_taps):
        self.rrc_taps = rrc_taps
        self.digital_pfb_clock_sync_xxx_0.update_taps((self.rrc_taps))

    def get_nfilts_0(self):
        return self.nfilts_0

    def set_nfilts_0(self, nfilts_0):
        self.nfilts_0 = nfilts_0


def argument_parser():
    description = 'LilacSat-2 decoder'
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option, description=description)
    parser.add_option(
        "", "--bfo", dest="bfo", type="eng_float", default=eng_notation.num_to_str(12000),
        help="Set carrier frequency of the BPSK signal [default=%default]")
    parser.add_option(
        "", "--callsign", dest="callsign", type="string", default="",
        help="Set your callsign [default=%default]")
    parser.add_option(
        "-i", "--invert", dest="invert", type="intx", default=-1,
        help="Set invert the waveform (-1 to invert) [default=%default]")
    parser.add_option(
        "", "--ip", dest="ip", type="string", default="::",
        help="Set UDP listen IP [default=%default]")
    parser.add_option(
        "", "--latitude", dest="latitude", type="eng_float", default=eng_notation.num_to_str(0),
        help="Set latitude (format 00.000 or -00.000) [default=%default]")
    parser.add_option(
        "", "--longitude", dest="longitude", type="eng_float", default=eng_notation.num_to_str(0),
        help="Set longitude (format 00.000 or -00.000) [default=%default]")
    parser.add_option(
        "", "--port", dest="port", type="intx", default=7355,
        help="Set UDP port [default=%default]")
    parser.add_option(
        "", "--recstart", dest="recstart", type="string", default="",
        help="Set start of recording, if processing a recording (format YYYY-MM-DD HH:MM:SS) [default=%default]")
    return parser


def main(top_block_cls=lilacsat2, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    tb = top_block_cls(bfo=options.bfo, callsign=options.callsign, invert=options.invert, ip=options.ip, latitude=options.latitude, longitude=options.longitude, port=options.port, recstart=options.recstart)
    tb.start()
    tb.wait()


if __name__ == '__main__':
    main()
