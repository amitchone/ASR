# dft.py
# Compute the discrete fourier transform of a given data set
# Author: Adam Mitchell
# Email:  adamstuartmitchell@gmail.com

import math, numpy


def window(frame, func='hamming'):
    funcs = { 'bartlett': numpy.bartlett, 'hamming': numpy.hamming,
              'blackman': numpy.blackman, 'hanning': numpy.hanning
            }

    window = funcs[func](len(frame))

    windowed = list()

    for idx, coeff in enumerate(window):
        windowed.append(frame[idx] * coeff)

    return windowed


def fft(frame, npoints=512, winfunc='hamming'):
    f = window(frame, func=winfunc)
    c = numpy.fft.fft(f, n=npoints)

    magnitudes = list()

    for coeff in c[0:(len(c)/2)]:
        magnitudes.append(math.sqrt((coeff.real ** 2) + (coeff.imag ** 2))/len(frame) * 2)

    return magnitudes
