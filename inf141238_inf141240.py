from scipy.io import wavfile
from scipy.signal import decimate
import numpy as np
import copy
import warnings
import os
import re

def getSignalData(w, signal):
    n = signal.shape[0]
    frequencies = np.arange(n) / n * w
    signal_kaiser = signal * np.kaiser(n, 100)
    signal_kaiser_fft = abs(np.fft.fft(signal_kaiser)) / (0.5 * n)

    return frequencies, signal_kaiser_fft

def harmonicProductSpectrum(frequencies, signal_fft):
    signal_hps = copy.copy(signal_fft)
    for i in np.arange(2, 6):
        dec = decimate(signal_fft, i)
        signal_hps[:len(dec)] *= dec

    return frequencies[np.argmax(signal_hps)]

def main():
    warnings.filterwarnings('ignore')

    #filename = 'trainall/001_K.wav'
    all = 0
    recognised = 0

    for file in os.listdir("trainall"):
        if file.endswith(".wav"):
            filename = file
            all += 1

        if re.match("\\d{3}_K.wav", filename):
            gender = 'K'
        else:
            gender = 'M'

        w, signal = wavfile.read("trainall/" + filename)

        if len(signal.shape) > 1:     # only first channel
            signal = signal[:, 0]

        frequencies, signal_fft = getSignalData(w, signal)
        max_freq = harmonicProductSpectrum(frequencies, signal_fft)
        #print(max_freq)

        if max_freq < 170:
            print('M')
            if gender == 'M':
                recognised += 1
        else:
            print('K')
            if gender == 'K':
                recognised += 1

    print(recognised*100/all)

if __name__ == '__main__':
    main()
