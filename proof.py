# proof.py
# Compute MFCCs and DTW comparison using 3rd-party libraries
# Author: Adam Mitchell
# Email:  adamstuartmitchell@gmail.com

import librosa, numpy
from scipy.io.wavfile import read


def get_frames(length, ovrlap, fs, data):
    length = int(round(length * fs))
    ovrlap = int(round(ovrlap * fs))
    pointr, countr = 0, 0
    frames = dict()

    while pointr < len(data):
        frames[countr] = data[pointr:pointr+length]

        if len(frames[countr]) != length:
            frames[countr] = numpy.append(frames[countr], [0] * (length-len(frames[countr])))

        countr += 1
        pointr += ovrlap

    return frames


def get_mfcc_vector(sample, framelength=0.025, frameoverlap=0.0125, n_mfccs=13):
    fs, data = read(sample)
    samplevector = list()

    for frame, samples in get_frames(framelength, frameoverlap, fs, data).iteritems():
        samplevector.append(librosa.feature.mfcc(samples, sr=fs, n_mfcc=13))

    return numpy.array(samplevector)


def get_dtw(template, test):
    template = template[10]
    test = test[10]

    D, wp = librosa.dtw(template, test)
    best_cost = D[wp[-1, 0], wp[-1, 1]]

    print best_cost


if __name__ == '__main__':
    one_1 = get_mfcc_vector('wavs/one-adam-1.wav')
    print one_1.shape

    one_2 = get_mfcc_vector('wavs/one-adam-2.wav')
    print one_2.shape
    '''
    one_3 = get_mfcc_vector('wavs/one-adam-3.wav')

    one_b = get_mfcc_vector('wavs/one-ben-1.wav')

    two_1 = get_mfcc_vector('wavs/two-adam-1.wav')

    get_dtw(one_1, one_b)
    '''
