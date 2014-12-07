SDN-Video-Transmission
======================

Author: Naga Sreekanth

This Project requires GNU Radio library to work properly. The test_video_tx_rx.py file is the core python file which uses video_tx_GMSK.py and video_rx_GMSK.py files for the Modulation of Video Signals.

This code uses the txfifo.ts file video as Input and and the output is observed at the Receiver end. The output is queued as fifo packets which are added to the pipe and rxfifo.ts file is reconstructed.

The Encoding and decoding can be further upgraded and the buffer queue reconstruction at the receiver can be implemented better.
