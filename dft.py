# dft.py
# Compute the discrete fourier transform of a given data set
# Author: Adam Mitchell
# Email:  adamstuartmitchell@gmail.com

import math, numpy, time

from matplotlib import pyplot as plt
from scipy.io.wavfile import read


N = [ 0, 0.707, 1, 0.707, 0, -0.707, -1, -0.707]


def dft(N):
    magnitudes = list()

    for fidx in range(len(N)/2):

        e = list()

        for sidx, sample in enumerate(N):
            c = complex(sample * math.cos((-(2 * math.pi * fidx * sidx)/len(N))),
                        sample * math.sin((-(2 * math.pi * fidx * sidx)/len(N)))
                       )
            e.append(c)

        coeff = sum(e) * 2
        magnitudes.append(math.sqrt((coeff.real ** 2) + (coeff.imag ** 2))/len(N))

    return magnitudes


def npfft(N):
    magnitudes = list()

    c = numpy.fft.fft(N, n=512)

    for coeff in c[0:(len(c)/2)+1]:
        magnitudes.append(math.sqrt((coeff.real ** 2) + (coeff.imag ** 2))/len(N) * 2)

    return magnitudes


def normalise(N):
    f = max(N)

    return [ i/f for i in N ]


class FeatureExtract(object):
    def __init__(self, _file, flen=25, fovl=50):
        self.fs, self.data = read(_file)
        self.flen = int(round(self.fs / (1000/flen)))
        self.fovl = int(round(self.flen * (fovl/100)))
        self.pntr = 0

    def setPntr(self, pntr):
        if isinstance(pntr, [int, float, long]):
            self.pntr = int(pntr)
        else:
            raise TypeError('Argument "pntr" must be of type: int, float, long. Got {0}'.format(type(pntr)))

    def frame(self, N):
        F = N[self.pntr:self.pntr+self.flen]
        self.pntr = self.pntr + self.flen
        return F

    def hamming(self, N):
        window = numpy.hamming(len(N))

        for idx, sample in enumerate(N):
            yield sample * window[idx]

    def fft(self, N, window=True):
        magnitudes = list()

        if window:
            N = [ i for i in self.hamming(N)]

        c = numpy.fft.fft(N)

        for coeff in c[0:int(len(c)/2)]:
            ab = math.sqrt((coeff.real ** 2) + (coeff.imag ** 2))/len(N) * 2
            magnitudes.append(1/len(N) * (ab ** 2))

        return magnitudes



if __name__ == '__main__':
    '''
    f = FeatureExtract('1k.wav')
    F = f.frame(f.data)
    M = f.fft(F)
    print len(M)
    plt.plot(M)
    plt.show
    #print f.__dict__

    '''
    fs, data = read('1k.wav')

    window = numpy.hamming(400)
    windowed = list()
    for idx, c in enumerate(data[0:400]):
        windowed.append(c * window[idx])

    start = time.time()
    mags = npfft(windowed) # array of power spectral density estimates i.e. periodograms
    print len(mags)
    plt.plot(mags)
    plt.show()
