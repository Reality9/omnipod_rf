from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes

class FskDemod(gr.top_block):

    def __init__(self, input_file, output_file):
        gr.top_block.__init__(self)

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 2048000

        ##################################################
        # Blocks
        ##################################################
        self.low_pass_filter_1 = filter.fir_filter_fff(1, firdes.low_pass(
        	1, samp_rate, 85000, 2000, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0 = filter.fir_filter_ccf(1, firdes.low_pass(
        	1, samp_rate, 200000, 1000, firdes.WIN_HAMMING, 6.76))
        self.blocks_wavfile_source_0 = blocks.wavfile_source(input_file, False)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_float*1, output_file, False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.blocks_add_const_vxx_0 = blocks.add_const_vff((0.00, ))
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, 450000, 1, 0)
        self.analog_quadrature_demod_cf_0 = analog.quadrature_demod_cf(1)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.low_pass_filter_1, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.blocks_wavfile_source_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.blocks_wavfile_source_0, 1), (self.blocks_float_to_complex_0, 1))
        self.connect((self.low_pass_filter_0, 0), (self.analog_quadrature_demod_cf_0, 0))
        self.connect((self.low_pass_filter_1, 0), (self.blocks_add_const_vxx_0, 0))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, 10e3, 10e3, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_1.set_taps(firdes.low_pass(1, self.samp_rate, 40400, 20200, firdes.WIN_HAMMING, 6.76))
