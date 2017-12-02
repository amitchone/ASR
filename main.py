# main.py
# MFCC feature extraction and comparison
# Author: Adam Mitchell
# Email:  adamstuartmitchell@gmail.com

import filterbank as fb
import dft, time

from scipy.io.wavfile import read
from matplotlib import pyplot as plt


if __name__ == '__main__':
    start = time.time()
    p, c = fb.get_filterbank(22050, 512, 80, 8000, 26)
    fs, data = read('1k.wav')

    f = data[0:400]
    m = dft.fft(f)
    print 'Took: {0}s'.format(time.time()-start)
    plt.plot(m)
    plt.show()
