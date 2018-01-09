# MFCC Automatic Speech Recognition Algorithm Implementation

A Python implementation of the Mel Frequency Cepstral Coefficient algorithm for the detection of phonemes in continuous speech.

## Feature Extraction Method

1. Extract audio signal and sampling frequency from .wav file
2. Frame signal
3. Apply window function to frame
4. Calculate DFT of frame
5. Calculate power spectral density estimate for each DFT bin
6. Apply Mel Frequency filter bank to signal
7. Calculate logarithm of energy in each filter
8. Take DCT of each filter
9. Voila!

## Vector Comparison Method

1. Compute DTW of comparison vector and training data
2. Specify tolerances
3. Voila!
