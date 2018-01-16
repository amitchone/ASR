# MFCC Automatic Speech Recognition Algorithm Implementation

A Python implementation of the Mel Frequency Cepstral Coefficient algorithm for the detection of phonemes in continuous speech.

## Method

1.  Read audio data and sampling frequency from .wav file
2.  Frame signal
3.  Apply window function to frame (default=hamming)
4.  Calculate DFT of frame
5.  Calculate periodogram power spectral density estimate for each DFT bin
6.  Apply Mel-Frequency filterbank to signal
7.  Sum energies within each filter and take the base 10 logarithm
8.  Take DCT of each filter
9.  Keep coefficients [1:13]
10. Compute DTW best path of reference vector and input vector (euclidean distance)

### To-do

1. Noise gate
2. Pre-emphasis / Lifter
3. Feature vector database
4. Audio record/playback script
