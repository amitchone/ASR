# mfcc.py
# Compute MFCCs of a given WAV file
# Author: Adam Mitchell
# Email:  adamstuartmitchell@gmail.com

import math, numpy
from scipy.io.wavfile import read


def open_file(f):
    '''
    return sampling frequency (fs) and time series data (data) of .wav file (f)
    '''
    fs, data = read(f)

    return fs, data


def frame_data(data, fs, length=0.025, shift=0.010):
    '''
    return array of arrays where each array is a framed segment of data (data)
    length of frames is given as sampling frequency (fs) * length (in ms)
    shift between frames is given as sampling frequency (fs) * shift (in ms)
    '''
    length = int(round(fs * length))
    shift = int(round(fs * shift))
    frames = list()

    for i in range(0, len(data), shift):
        frame = data[i:i+length]

        if len(frame) != length:
            frame = numpy.append(frame, [0] * (length-len(frame)))

        frames.append(frame)

    return length, numpy.array(frames)


def window_frame(frames, length):
    '''
    return array of arrays where each array is a frame within frames (frames) with
    a hamming window function applied
    length of hamming window is equivalent to the frame lengths (should be uniform)
    '''
    window = numpy.hamming(length)
    windowed_frames = list()

    for frame in frames:
        windowed_frame = list()

        for idx, sample in enumerate(frame):
            windowed_frame.append(sample * window[idx])

        windowed_frames.append(windowed_frame)

    return numpy.array(windowed_frames)


def fft_frame(frames, fftres=512):
    '''
    return array of arrays where each array is a periodogram power spectral density estimate
    of each frame within frames (frames)
    fft resolution is given by fftres
    '''
    fftd_frames = list()

    for frame in frames:
        fftd_frame = list()

        coefficients = numpy.fft.fft(frame, n=fftres)

        for c in coefficients[0:(len(coefficients)/2)]:
            absolute = math.sqrt((c.real ** 2) + (c.imag ** 2))
            periodogram = ((1 / float(len(coefficients))) * absolute) ** 2
            fftd_frame.append(periodogram)

        fftd_frames.append(fftd_frame)

    return fftd_frames


def get_mfcc_filterbank(fs, nfilts=12, lf=300, hf=8000, fftres=512):
    def hertz_to_mel(f):
        return round(2595 * math.log10(1+(f/float(700))), 2)

    def mel_to_hertz(q):
        return round(700 * (10 ** (q/2595) - 1), 2)

    def hz_to_fft_bin(fftres, f, fs):
        return math.floor((fftres + 1) * f / fs)

    lf = hertz_to_mel(lf)
    hf = hertz_to_mel(hf)
    stepsize = (hf - lf) / (nfilts - 1)
    melpoints = list()

    print 'Filterbank parameters:\n\nnfilts: {0:2}   lf: {1:7}   hf: {2:7}   step: {3:7}'.format(nfilts, lf, hf, stepsize)

    for i in range(0, nfilts):
        print i
        melpoints.append(lf + (i * stepsize))

    hzpoints = [ mel_to_hertz(i) for i in melpoints ]
    bins = [ hz_to_fft_bin(fftres, i, fs) for i in hzpoints ]

    print hzpoints, len(hzpoints)
    print bins, len(bins)











if __name__ == '__main__':
    fs, data = open_file('wavs/one-adam-1.wav')
    #framelength, frames = frame_data(data, fs)
    #windowed_frames = window_frame(frames, framelength)
    #fftd_frames = fft_frame(windowed_frames)
    get_mfcc_filterbank(16000)
