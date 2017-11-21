# Import futures
from __future__ import division

# Import from standard lib
from collections import OrderedDict

# Import 3rd party libs
from matplotlib import pyplot as plt
import numpy
from scipy.io.wavfile import read


class FeatureExtract(object):
    def __init__(self, data, mmap=False):
        '''
        args:
            data:   path to .wav file for feature extraction
            mmap:   map wave file to memory?

        vars:
            self.fs:      sampling frequency of .wav file
            self.data:    data contained within .wav file
        '''
        self.fs, self.data = read(data, mmap=mmap)

    def frame(self, length=25, overlap=0.5):
        '''
        args:
            length:     length of frames in ms
            overlap:    fraction of overlap between frames

        vars:
            self.frames:    OrderedDict containing arrays of samples
            self.length:    length of each frame array = sampling frequency / length (ms)
            self.overlap:   interval (in samples) at which a new frame is created
            self.pos:       current position (in samples) in data array
        '''
        self.frames = OrderedDict()

        self.length = self.fs / (1000 / length)
        self.overlap = self.length * overlap
        self.pos = 0

        while self.pos < len(self.data):
            self.frames[int(self.pos)] = self.data[int(self.pos):int(self.pos+self.length)]
            self.pos = self.pos+self.overlap

    def window(self, pos, func='hamming'):
        '''
        args:
            pos:     number of frame to process
            func:    window function to be applied to frame

        vars:
            self.windows:    dict containing available window functions
            idx:             index of window array
            factor:          factor (in window array) by which to multiply sample (in frame)
        '''
        self.windows = { 'blackman': numpy.blackman, 'hanning': numpy.hanning,
                         'bartlett': numpy.bartlett, 'hamming': numpy.hamming
                       }

        for idx, factor in enumerate(self.windows[func](self.length)):
            self.frames[int(pos)][idx] = self.frames[int(pos)][idx] * factor
