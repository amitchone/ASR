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

            vectors[frame] = dct([ i for i in log_energies.itervalues() ])

        return vectors


if __name__ == '__main__':
    f1 = FeatureVectorExtract('one-1.wav', 1024, 80, 8000, 0.025, 0.01)
    mfcc1 = f1.mfcc_vectors

    f2 = FeatureVectorExtract('two-1.wav', 1024, 80, 8000, 0.025, 0.01)
    mfcc2 = f2.mfcc_vectors

    f3 = FeatureVectorExtract('three-1.wav', 1024, 80, 8000, 0.025, 0.01)
    mfcc3 = f3.mfcc_vectors

    f4 = FeatureVectorExtract('four-1.wav', 1024, 80, 8000, 0.025, 0.01)
    mfcc4 = f4.mfcc_vectors

    f5 = FeatureVectorExtract('five-1.wav', 1024, 80, 8000, 0.025, 0.01)
    mfcc5 = f5.mfcc_vectors

    f6 = FeatureVectorExtract('six-1.wav', 1024, 80, 8000, 0.025, 0.01)
    mfcc6 = f6.mfcc_vectors

    ftest = FeatureVectorExtract('one-ben1.wav', 1024, 80, 8000, 0.025, 0.01)
    mfcctest = ftest.mfcc_vectors

    lens = [ len(mfcc1), len(mfcc2), len(mfcc3), len(mfcc4), len(mfcc5), len(mfcc6), len(mfcctest) ]

    T1, T2, T3, T4, T5, T6 = 0, 0, 0, 0, 0, 0
    F1, F2, F3, F4, F5, F6 = 0, 0, 0, 0, 0, 0
    tolerance = 0.59

    for i in range(min(lens)):
        comparison1 = numpy.isclose(mfcctest[i], mfcc1[i], atol=tolerance, rtol=tolerance)
        comparison2 = numpy.isclose(mfcctest[i], mfcc2[i], atol=tolerance, rtol=tolerance)
        comparison3 = numpy.isclose(mfcctest[i], mfcc3[i], atol=tolerance, rtol=tolerance)
        comparison4 = numpy.isclose(mfcctest[i], mfcc4[i], atol=tolerance, rtol=tolerance)
        comparison5 = numpy.isclose(mfcctest[i], mfcc5[i], atol=tolerance, rtol=tolerance)
        comparison6 = numpy.isclose(mfcctest[i], mfcc6[i], atol=tolerance, rtol=tolerance)

        T1 += numpy.count_nonzero(comparison1 == True)
        F1 += numpy.count_nonzero(comparison1 == False)
        T2 += numpy.count_nonzero(comparison2 == True)
        F2 += numpy.count_nonzero(comparison2 == False)
        T3 += numpy.count_nonzero(comparison3 == True)
        F3 += numpy.count_nonzero(comparison3 == False)
        T4 += numpy.count_nonzero(comparison4 == True)
        F4 += numpy.count_nonzero(comparison4 == False)
        T5 += numpy.count_nonzero(comparison5 == True)
        F5 += numpy.count_nonzero(comparison5 == False)
        T6 += numpy.count_nonzero(comparison6 == True)
        F6 += numpy.count_nonzero(comparison6 == False)

    print 'C1: True: {0:3} False {1:3}'.format(T1, F1)
    print 'C2: True: {0:3} False {1:3}'.format(T2, F2)
    print 'C3: True: {0:3} False {1:3}'.format(T3, F3)
    print 'C4: True: {0:3} False {1:3}'.format(T4, F4)
    print 'C5: True: {0:3} False {1:3}'.format(T5, F5)
    print 'C6: True: {0:3} False {1:3}'.format(T6, F6)
