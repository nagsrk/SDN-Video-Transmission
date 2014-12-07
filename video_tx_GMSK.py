#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Video transmission
# Author: Naga
# Description: Using GMSK modulation
# Generated: Wed Mar 13 16:33:22 2013
##################################################

from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import uhd
from gnuradio import window
from gnuradio.eng_option import eng_option
from gnuradio.gr import firdes
from gnuradio.wxgui import fftsink2
from grc_gnuradio import blks2 as grc_blks2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import wx

class video_tx_GMSK(grc_wxgui.top_block_gui):

	def __init__(self, address="addr=192.168.10.2"):
		grc_wxgui.top_block_gui.__init__(self, title="Video transmission")

		##################################################
		# Parameters
		##################################################
		self.address = address

		##################################################
		# Variables
		##################################################
		self.samples = samples = 2
		self.samp_rate = samp_rate = 1e6
		self.freq = freq = 1.2805e9

		##################################################
		# Blocks
		##################################################
		self.notebook_0 = self.notebook_0 = wx.Notebook(self.GetWin(), style=wx.NB_TOP)
		self.notebook_0.AddPage(grc_wxgui.Panel(self.notebook_0), "RF Spectrum")
		self.Add(self.notebook_0)
		self.wxgui_fftsink2_1 = fftsink2.fft_sink_c(
			self.notebook_0.GetPage(0).GetWin(),
			baseband_freq=freq,
			y_per_div=10,
			y_divs=15,
			ref_level=0,
			ref_scale=2.0,
			sample_rate=samp_rate,
			fft_size=1024,
			fft_rate=15,
			average=False,
			avg_alpha=None,
			title="FFT Plot",
			peak_hold=False,
			win=window.hamming,
		)
		self.notebook_0.GetPage(0).Add(self.wxgui_fftsink2_1.win)
		self.uhd_usrp_sink_0 = uhd.usrp_sink(
			device_addr=address,
			stream_args=uhd.stream_args(
				cpu_format="fc32",
				channels=range(1),
			),
		)
		self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
		self.uhd_usrp_sink_0.set_center_freq(freq, 0)
		self.uhd_usrp_sink_0.set_gain(0, 0)
		self.uhd_usrp_sink_0.set_antenna("TX/RX", 0)
		self.gr_multiply_const_vxx_0 = gr.multiply_const_vcc((0.1, ))
		self.gr_file_source_0 = gr.file_source(gr.sizeof_char*1, "/home/Naga/documents/video transmission/txfifo.ts", False)
		self.digital_gmsk_mod_0 = digital.gmsk_mod(
			samples_per_symbol=samples,
			bt=0.35,
			verbose=False,
			log=False,
		)
		self.blks2_packet_encoder_0 = grc_blks2.packet_mod_b(grc_blks2.packet_encoder(
				samples_per_symbol=samples,
				bits_per_symbol=1,
				access_code="",
				pad_for_usrp=True,
			),
			payload_length=0,
		)

		##################################################
		# Connections
		##################################################
		self.connect((self.gr_file_source_0, 0), (self.blks2_packet_encoder_0, 0))
		self.connect((self.blks2_packet_encoder_0, 0), (self.digital_gmsk_mod_0, 0))
		self.connect((self.digital_gmsk_mod_0, 0), (self.gr_multiply_const_vxx_0, 0))
		self.connect((self.gr_multiply_const_vxx_0, 0), (self.uhd_usrp_sink_0, 0))
		self.connect((self.gr_multiply_const_vxx_0, 0), (self.wxgui_fftsink2_1, 0))

	def get_address(self):
		return self.address

	def set_address(self, address):
		self.address = address

	def get_samples(self):
		return self.samples

	def set_samples(self, samples):
		self.samples = samples

	def get_samp_rate(self):
		return self.samp_rate

	def set_samp_rate(self, samp_rate):
		self.samp_rate = samp_rate
		self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)
		self.wxgui_fftsink2_1.set_sample_rate(self.samp_rate)

	def get_freq(self):
		return self.freq

	def set_freq(self, freq):
		self.freq = freq
		self.uhd_usrp_sink_0.set_center_freq(self.freq, 0)
		self.wxgui_fftsink2_1.set_baseband_freq(self.freq)

if __name__ == '__main__':
	parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
	parser.add_option("", "--address", dest="address", type="string", default="addr=192.168.10.2",
		help="Set IP Address [default=%default]")
	(options, args) = parser.parse_args()
	tb = video_tx_GMSK(address=options.address)
	tb.Run(True)

