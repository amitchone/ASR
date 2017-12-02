# main.py
# MFCC feature extraction and comparison
# Author: Adam Mitchell
# Email:  adamstuartmitchell@gmail.com

import filterbank as fb
import dft

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


if __name__ == '__main__':
    p, c = fb.get_filterbank(22050, 512, 80, 8000, 26)
    fs, data = read('1k.wav')
    f = data[0:400]
    m = dft.fft(f)

    for key, val in c.iteritems():
        fnum = key
        lbin = int(val['lbin'])
        hbin = int(val['hbin'])

        for idx, c in enumerate(val['coeffs']):
            print 'Filter: {0:2}  Bin: {1:2}  Coeff: {2:8}  Mag: {3:8}'.format(fnum, lbin+idx, c, m[lbin+idx])

    #plt.plot(m)
    #plt.show()
