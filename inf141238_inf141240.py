from scipy.io import wavfile
from scipy.signal import decimate
from copy import copy
import numpy as np
import warnings
import sys


def getSignalData(w, signal):
    n = signal.shape[0]
    frequencies = np.arange(n) / n * w
    signal_kaiser = signal * np.kaiser(n, 20)
    signal_kaiser_fft = abs(np.fft.fft(signal_kaiser)) / (0.5 * n)

    return frequencies, signal_kaiser_fft


def harmonicProductSpectrum(frequencies, signal_fft):
    signal_hps = copy(signal_fft)

    for i in np.arange(2, 6):
        dec = decimate(signal_fft, i)
        signal_hps[:len(dec)] *= dec

    left_boundary = np.where(frequencies > 20)[0][0]
    right_boundary = np.where(frequencies > 1000)[0][0]

    return (frequencies[left_boundary:right_boundary])[np.argmax(signal_hps[left_boundary:right_boundary])]


def main():
    try:
        warnings.filterwarnings('ignore')

        filename = sys.argv[1]
        w, signal = wavfile.read(filename)

        if len(signal.shape) > 1:     # only first channel
            signal = signal[:, 0]

        frequencies, signal_fft = getSignalData(w, signal)
        max_freq = harmonicProductSpectrum(frequencies, signal_fft)

        if max_freq < 170:
            print('M')
        else:
            print('K')
    except:
        print('K')


if __name__ == '__main__':
    main()
