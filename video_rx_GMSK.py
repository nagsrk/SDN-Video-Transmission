#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Video reception
# Author: Naga
# Description: Using GMSK Modulation
# Generated: Mon Apr 22 12:16:50 2013
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

class video_rx_GMSK(grc_wxgui.top_block_gui):

	def __init__(self, address="addr=192.168.10.2"):
		grc_wxgui.top_block_gui.__init__(self, title="Video reception")

		##################################################
		# Parameters
		##################################################
		self.address = address

		##################################################
		# Variables
		##################################################
		self.samp_rate = samp_rate = 1e6
		self.freq = freq = 1.2805e9

		##################################################
		# Blocks
		##################################################
		self.notebook_0 = self.notebook_0 = wx.Notebook(self.GetWin(), style=wx.NB_TOP)
		self.notebook_0.AddPage(grc_wxgui.Panel(self.notebook_0), "RF Spectrum")
		self.notebook_0.AddPage(grc_wxgui.Panel(self.notebook_0), "Filtered spectrum")
		self.Add(self.notebook_0)
		self.wxgui_fftsink2_0_0_1 = fftsink2.fft_sink_c(
			self.notebook_0.GetPage(0).GetWin(),
			baseband_freq=freq,
			y_per_div=5,
			y_divs=10,
			ref_level=-40,
			ref_scale=2.0,
			sample_rate=samp_rate,
			fft_size=1024,
			fft_rate=15,
			average=False,
			avg_alpha=None,
			title="FFT Plot",
			peak_hold=False,
		)
		self.notebook_0.GetPage(0).Add(self.wxgui_fftsink2_0_0_1.win)
		self.wxgui_fftsink2_0_0_0 = fftsink2.fft_sink_c(
			self.notebook_0.GetPage(1).GetWin(),
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
		)
		self.notebook_0.GetPage(1).Add(self.wxgui_fftsink2_0_0_0.win)
		self.uhd_usrp_source_0 = uhd.usrp_source(
			device_addr=address,
			stream_args=uhd.stream_args(
				cpu_format="fc32",
				channels=range(1),
			),
		)
		self.uhd_usrp_source_0.set_samp_rate(samp_rate)
		self.uhd_usrp_source_0.set_center_freq(freq, 0)
		self.uhd_usrp_source_0.set_gain(65, 0)
		self.uhd_usrp_source_0.set_antenna("TX/RX", 0)
		self.low_pass_filter_1 = gr.fir_filter_ccf(1, firdes.low_pass(
			1, samp_rate, 350e3, 50e3, firdes.WIN_HAMMING, 6.76))
		self.gr_file_sink_1 = gr.file_sink(gr.sizeof_char*1, "/home/Naga/documents/video transmission/test")
		self.gr_file_sink_1.set_unbuffered(False)
		self.gr_file_sink_0 = gr.file_sink(gr.sizeof_char*1, "/home/Naga/documents/video transmission/rxfifo.ts")
		self.gr_file_sink_0.set_unbuffered(False)
		self.digital_gmsk_demod_0 = digital.gmsk_demod(
			samples_per_symbol=2,
			gain_mu=0.175,
			mu=0.5,
			omega_relative_limit=0.005,
			freq_error=0.0,
			verbose=False,
			log=False,
		)
		self.blks2_packet_decoder_0 = grc_blks2.packet_demod_b(grc_blks2.packet_decoder(
				access_code="",
				threshold=-1,
				callback=lambda ok, payload: self.blks2_packet_decoder_0.recv_pkt(ok, payload),
			),
		)

		##################################################
		# Connections
		##################################################
		self.connect((self.low_pass_filter_1, 0), (self.digital_gmsk_demod_0, 0))
		self.connect((self.low_pass_filter_1, 0), (self.wxgui_fftsink2_0_0_0, 0))
		self.connect((self.digital_gmsk_demod_0, 0), (self.blks2_packet_decoder_0, 0))
		self.connect((self.blks2_packet_decoder_0, 0), (self.gr_file_sink_0, 0))
		self.connect((self.blks2_packet_decoder_0, 0), (self.gr_file_sink_1, 0))
		self.connect((self.uhd_usrp_source_0, 0), (self.low_pass_filter_1, 0))
		self.connect((self.uhd_usrp_source_0, 0), (self.wxgui_fftsink2_0_0_1, 0))

	def get_address(self):
		return self.address

	def set_address(self, address):
		self.address = address

	def get_samp_rate(self):
		return self.samp_rate

	def set_samp_rate(self, samp_rate):
		self.samp_rate = samp_rate
		self.low_pass_filter_1.set_taps(firdes.low_pass(1, self.samp_rate, 350e3, 50e3, firdes.WIN_HAMMING, 6.76))
		self.wxgui_fftsink2_0_0_0.set_sample_rate(self.samp_rate)
		self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)
		self.wxgui_fftsink2_0_0_1.set_sample_rate(self.samp_rate)

	def get_freq(self):
		return self.freq

	def set_freq(self, freq):
		self.freq = freq
		self.wxgui_fftsink2_0_0_0.set_baseband_freq(self.freq)
		self.uhd_usrp_source_0.set_center_freq(self.freq, 0)
		self.wxgui_fftsink2_0_0_1.set_baseband_freq(self.freq)

if __name__ == '__main__':
	parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
	parser.add_option("-a", "--address", dest="address", type="string", default="addr=192.168.10.2",
		help="Set IP Address [default=%default]")
	(options, args) = parser.parse_args()
	tb = video_rx_GMSK(address=options.address)
	tb.Run(True)

