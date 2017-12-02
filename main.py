# main.py
# MFCC feature extraction and comparison
# Author: Adam Mitchell
# Email:  adamstuartmitchell@gmail.com

import filterbank as fb
import dft

import numpy

from scipy.io.wavfile import read
from matplotlib import pyplot as plt

'''
Current arguments required for class:

wav file (will provide audio data and sampling frequency)
npoints for fft
filterbank lf and hf end points
filterbank nfilters
window function

Must add:

padding function for frames - pad end with 0s to reach frame length
feature extract class
lexicon
language model
feature vector database
'''

class FeatureVectorExtract(object):
    def __init__(self, wavfile, nfftpoints, fblf, fbhf, frlen, frovrlp, fbnfilts=26, winfunc='hamming', mfcc=True):
        fs, data = read(wavfile)

        if mfcc:
            framed_signal = self.get_frames(frlen, frovrlp, fs, data)
            for key, val in framed_signal.iteritems():
                print key, val
                
            #self.get_mfcc(fs, framed_signal, nfftpoints, fblf, fbhf, fbnfilts, winfunc)


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
        p, c = fb.get_filterbank(fs, nfftpoints, fblf, fbhf, fbnfilts)



if __name__ == '__main__':
    f = FeatureVectorExtract('1k.wav', 1024, 80, 8000, 0.025, 0.010)



    '''
    f = data[0:400]
    m = dft.fft(f, npoints=1024)

    filtered = dict()

    for key, val in c.iteritems():
        fvals = list()
        fnum = key
        lbin = int(val['lbin'])

        for idx, c in enumerate(val['coeffs']):
            fvals.append(c * m[lbin+idx])

        filtered[key] = fvals

    for key, val in filtered.iteritems():
        print key, val
    #plt.plot(m)
    #plt.show()
    '''
