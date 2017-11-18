# Import futures
from __future__ import division

# Import from standard lib
from collections import OrderedDict

# Import 3rd party libs
import numpy
from scipy.io.wavfile import read


class FeatureExtract(object):
    def __init__(self, data, mmap=False):
        self.fs, self.data = read(data, mmap=mmap)

    def frame(self, length=25, overlap=0.5):
        self.frames = OrderedDict()

        self.length = self.fs / (1000 / length)
        self.overlap = self.length * overlap
        self.pos = 0

        while self.pos < len(self.data):
            self.frames[int(self.pos)] = self.data[int(self.pos):int(self.pos+self.length)]
            self.pos = self.pos+self.overlap

    def window(self, pos, func='hamming'):
        self.windows = {'blackman': numpy.blackman, 'hanning': numpy.hanning,
                        'hamming':  numpy.hamming,  'bartlett': numpy.bartlett
                       }
        self.window = self.windows[func](self.length)

        for idx, coeff in enumerate(self.window):
            self.frames[int(pos)][idx] = self.frames[int(pos)][idx] * coeff




f = FeatureExtract('today.wav')
f.frame()
f.window(0)
