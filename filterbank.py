from __future__ import division
import math


def hertz_to_mel(v):
    return 2595 * math.log10(1+(v/700))


def mel_to_hertz(v):
    return 700 * (10 ** (v/2595) - 1)


def get_mel_coeffs(low=80, high=8000, nfilts=26):
    low = hertz_to_mel(low)
    high = hertz_to_mel(high)
    spacing = (high-low) / (nfilts +1)
    coeffs = [ low ]

    while len(coeffs) < nfilts + 2:
        coeffs.append(coeffs[-1] + spacing)

    return coeffs


def mel_coeff_to_hertz(l):
    return map(mel_to_hertz, l)


def get_filter_params(l, nfilts=26):
    filter_params = dict()

    for i in range(nfilts):
        filter_params[i] = { 'low': l[i], 'peak': l[i+1], 'high': l[i+2] }

    return filter_params


mel_coeffs = get_mel_coeffs(80, 8000, 26)
hz_coeffs = mel_coeff_to_hertz(mel_coeffs)
filter_params = get_filter_params(hz_coeffs)

for key, val in filter_params.iteritems():
    print key, val['low'], val['peak'], val['high']
