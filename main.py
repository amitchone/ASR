# main.py
# MFCC feature extraction and comparison
# Author: Adam Mitchell
# Email:  adamstuartmitchell@gmail.com

import filterbank as fb
import dft

import math, time

import numpy
from matplotlib import pyplot as plt
from scipy.io.wavfile import read
from scipy.fftpack import dct

# TODO:
# lexicon
# language model
# feature vector database

class FeatureVectorExtract(object):
    def __init__(self, wavfile, nfftpoints, fblf, fbhf, frlen, frovrlp, fbnfilts=26, winfunc='hamming', mfcc=True):
        fs, data = read(wavfile)

        if mfcc:
            framed_signal = self.get_frames(frlen, frovrlp, fs, data)
            self.mfcc_vectors = self.get_mfcc(fs, framed_signal, nfftpoints, fblf, fbhf, fbnfilts, winfunc)


    def get_frames(self, frlen, frovrlp, fs, data):
        length = int(round(frlen * fs))
        ovrlap = int(round(frovrlp * fs))
        pointr = 0
        countr = 0
        frames = dict()

        while pointr < len(data):
            frames[countr] = data[pointr:pointr+length]

            if len(frames[countr]) != length:
                frames[countr] = numpy.append(frames[countr], [0] * (length-len(frames[countr])))

            countr += 1
            pointr += ovrlap

        return frames


    def get_mfcc(self, fs, data, nfftpoints, fblf, fbhf, fbnfilts, winfunc):
        fp, c = fb.get_filterbank(fs, nfftpoints, fblf, fbhf, fbnfilts)
        vectors = dict()

        for frame, signal in data.iteritems():
            p = dft.fft(signal, npoints=nfftpoints)

            log_energies = dict()

            for key, val in c.iteritems():
                fvals = list()
                fnum = key
                lbin = int(val['lbin'])

                for idx, coeff in enumerate(val['coeffs']):
                    fvals.append(coeff * p[lbin+idx])

                log_energies[key] = math.log10(sum(fvals))

            vectors[frame] = dct([ i for i in log_energies.itervalues() ])[0:13]

        return vectors


if __name__ == '__main__':
    start = time.time()
    f = FeatureVectorExtract('06s.wav', 1024, 80, 8000, 0.025, 0.01)
    mfccs = f.mfcc_vectors
    for key, val in mfccs.iteritems():
        print key, val
    print time.time() - start
