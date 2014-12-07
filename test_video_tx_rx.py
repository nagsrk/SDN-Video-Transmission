#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Test Video Tx Rx
#Author: Naga
# Generated: Fri Mar  8 15:32:16 2013
##################################################

from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.gr import firdes
from grc_gnuradio import blks2 as grc_blks2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import wx

class test_video_tx_rx(grc_wxgui.top_block_gui):

	def __init__(self):
		grc_wxgui.top_block_gui.__init__(self, title="Test Video Tx Rx")

		##################################################
		# Variables
		##################################################
		self.samp_rate = samp_rate = 1e6

		##################################################
		# Blocks
		##################################################
		self.gr_file_source_0 = gr.file_source(gr.sizeof_float*1, "/home/Naga/documents/video transmission/GANGNAM STYLE.ts", False)
		self.gr_file_sink_0 = gr.file_sink(gr.sizeof_float*1, "/home/Naga/documents/video transmission/rxfifo.ts")
		self.gr_file_sink_0.set_unbuffered(False)
		self.digital_dxpsk_mod_0 = digital.dbpsk_mod(
			samples_per_symbol=2,
			excess_bw=0.35,
			gray_coded=True,
			verbose=False,
			log=False)
			
		self.digital_dxpsk_demod_0 = digital.dbpsk_demod(
			samples_per_symbol=2,
			excess_bw=0.35,
			freq_bw=6.28/100.0,
			phase_bw=6.28/100.0,
			timing_bw=6.28/100.0,
			gray_coded=True,
			verbose=False,
			log=False
		)
		self.blks2_packet_encoder_0 = grc_blks2.packet_mod_f(grc_blks2.packet_encoder(
				samples_per_symbol=2,
				bits_per_symbol=1,
				access_code="",
				pad_for_usrp=True,
			),
			payload_length=0,
		)
		self.blks2_packet_decoder_0 = grc_blks2.packet_demod_f(grc_blks2.packet_decoder(
				access_code="",
				threshold=-1,
				callback=lambda ok, payload: self.blks2_packet_decoder_0.recv_pkt(ok, payload),
			),
		)

		##################################################
		# Connections
		##################################################
		self.connect((self.gr_file_source_0, 0), (self.blks2_packet_encoder_0, 0))
		self.connect((self.blks2_packet_decoder_0, 0), (self.gr_file_sink_0, 0))
		self.connect((self.blks2_packet_encoder_0, 0), (self.digital_dxpsk_mod_0, 0))
		self.connect((self.digital_dxpsk_mod_0, 0), (self.digital_dxpsk_demod_0, 0))
		self.connect((self.digital_dxpsk_demod_0, 0), (self.blks2_packet_decoder_0, 0))

	def get_samp_rate(self):
		return self.samp_rate

	def set_samp_rate(self, samp_rate):
		self.samp_rate = samp_rate

if __name__ == '__main__':
	parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
	(options, args) = parser.parse_args()
	tb = test_video_tx_rx()
	tb.Run(True)

