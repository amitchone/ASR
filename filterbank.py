# filterbank.py
# Generate triangular filterbank with specified number of filters and cutoff frequencies
# Author: Adam Mitchell
# Email:  adamstuartmitchell@gmail.com

from __future__ import division
from math import log10
from scipy.signal import triang


def hertz_to_mel(v):
    return 2595 * log10(1+(v/700))


def mel_to_hertz(v):
    return 700 * (10 ** (v/2595) - 1)


def get_mel_coeffs(low, high, nfilts):
    low = hertz_to_mel(low)
    high = hertz_to_mel(high)
    spacing = (high-low) / (nfilts +1)
    coeffs = [ low ]

    while len(coeffs) < nfilts + 2:
        coeffs.append(coeffs[-1] + spacing)

    return coeffs


def get_fft_resolution(fs, nfftpoints):
    return (fs) / (nfftpoints)


def hertz_to_bin(h, fs, nfftpoints):
    return round(h / get_fft_resolution(fs, nfftpoints))


def calc_filterbank_params(fs, nfftpoints, low, high, nfilts):
    mc = get_mel_coeffs(low, high, nfilts)
    hc = map(mel_to_hertz, mc)

    filter_params = dict()

    for i in range(nfilts):
        filter_params[i] = { 'low': hc[i], 'peak': hc[i+1], 'high': hc[i+2],
                             'lbin': hertz_to_bin(hc[i], fs, nfftpoints),
                             'pbin': hertz_to_bin(hc[i+1], fs, nfftpoints),
                             'hbin': hertz_to_bin(hc[i+2], fs, nfftpoints)
                           }

    return filter_params


def get_filterbank(fs, nfftpoints, low, high, nfilts=26):
    filter_params = calc_filterbank_params(fs, nfftpoints, low, high, nfilts)
    filter_coeffs = dict()

    for key, val in filter_params.iteritems():
        ncoeffs = (val['hbin'] - val['lbin']) + 1
        coeffs = triang(ncoeffs)

        filter_coeffs[key] = { 'lbin': val['lbin'], 'hbin': val['hbin'], 'coeffs': coeffs }

    return filter_params, filter_coeffs
