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

    return numpy.array(fftd_frames)


def get_mfcc_filterbank(fs, nfilts=26, lf=300, hf=8000, fftres=512):
    '''
    return array of arrays containing mel frequency filterbank coefficients and
    the FFT bin numbers to which they must be applied
    '''
    def hertz_to_mel(f):
        '''
        return mel frequency of given value (f) in hz
        '''
        return round(2595 * math.log10(1+(f/float(700))), 2)


    def mel_to_hertz(q):
        '''
        return frequency of given value (q) in mels
        '''
        return round(700 * (10 ** (q/2595) - 1), 2)


    def hz_to_fft_bin(fftres, f, fs):
        '''
        return FFT bin value closest to given frequency (f)
        note: FFT bin 256 will always be equivalent to fs * 0.5 in 512 point FFT
        '''
        return math.floor((fftres + 1) * f / fs)


    def get_coefficients(lbin, pbin, hbin, lcoeff=0.1, pcoeff=1):
        '''
        return two arrays
        1: triangular filter coefficients to be applied to FFT between lbin and hbin, peak value at pbin
        2: low bin [0] index value of array, peak bin [1] index value of array and high bin [2] etc...
        '''
        fcoeffs = list()
        stepsize = (pcoeff - lcoeff) / (pbin - lbin)

        for i in range(0, pbin - lbin):
            fcoeffs.append(lcoeff + (stepsize * i))

        fcoeffs.append(pcoeff)

        stepsize = (pcoeff - lcoeff) / (hbin - pbin)

        for i in range(hbin - pbin, 0, -1):
            fcoeffs.append(lcoeff + ((stepsize * i) - stepsize))

        return numpy.array(fcoeffs), numpy.array([lbin, pbin, hbin])

    lf = hertz_to_mel(lf)
    hf = hertz_to_mel(hf)
    stepsize = (hf - lf) / (nfilts + 1)
    filters = list()

    melpoints = [ (lf + (i * stepsize)) for i in range(0, nfilts + 2) ]
    hzpoints = [ mel_to_hertz(i) for i in melpoints ]
    bins = [ int(hz_to_fft_bin(fftres, i, fs)) for i in hzpoints ]

    for i in range(len(bins) - 2):
        filters.append(get_coefficients(bins[i], bins[i + 1], bins[i + 2]))

    return numpy.array(filters)


def apply_filters(frames, filterbank):
    '''
    returns array containing len(frames) arrays. each array contains len(filterbank) arrays containing
    each PSDE frames values with corresponding mel-filter applied
    '''
    filtered_frames = list()

    for frame in frames:
        filtered_frame = list()

        for _filter in filterbank:
            filtered = list()

            for idx, i in enumerate(range(_filter[1][0], _filter[1][0] + len(_filter[0]))):
                filtered.append(frame[i -1] * _filter[0][idx])

            filtered_frame.append(numpy.array(filtered))

        filtered_frames.append(numpy.array(filtered_frame))

    return numpy.array(filtered_frames)


def sum_log_filterbank_energies(frames):
    '''
    returns array of arrays. each array represents a frame from (frames) and
     contains 26 values each of which are the base 10 log of the sum of the filter coefficients
    '''
    log_energies = list()

    for frame in frames:
        log_energy = list()

        for _filter in frame:
            log_energy.append(math.log10(sum(_filter)))

        log_energies.append(numpy.array(log_energy))

    return numpy.array(log_energies)





if __name__ == '__main__':
    fs, data = open_file('wavs/one-adam-1.wav')
    framelength, frames = frame_data(data, fs)
    windowed_frames = window_frame(frames, framelength)
    frame_psde = fft_frame(windowed_frames)
    filterbank = get_mfcc_filterbank(fs)
    filtered_signal = apply_filters(frame_psde, filterbank)
    log_energies = sum_log_filterbank_energies(filtered_signal)

    print log_energies.shape
    for energy in log_energies:
        print energy
        break
