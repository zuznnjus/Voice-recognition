from scipy.io import wavfile
from scipy.signal import decimate
from copy import copy
import numpy as np
import warnings
import os
import re
import matplotlib.pyplot as plt

def getSignalData(w, signal):
    n = signal.shape[0]
    frequencies = np.arange(n) / n * w
    signal_kaiser = signal * np.kaiser(n, 100)
    signal_kaiser_fft = abs(np.fft.fft(signal_kaiser)) / (0.5 * n)

    return frequencies, signal_kaiser_fft

def harmonicProductSpectrum(frequencies, signal_fft):
    fig = plt.figure(figsize=(8, 10), dpi=80)
    ax = fig.add_subplot(5, 1, 1)
    ax.plot(frequencies, signal_fft, '-')
    ax.set_xlim(0, 1000)

    signal_hps = copy(signal_fft)
    for i in np.arange(2, 6):
        dec = decimate(signal_fft, i)
        signal_hps[:len(dec)] *= dec
        ax = fig.add_subplot(5, 1, i)
        ax.plot(frequencies, signal_hps, '-')
        ax.set_xlim(0, 1000)

    # plt.show()
    left_boundary = np.where(frequencies > 20)[0][0]
    return frequencies[np.argmax(signal_hps[left_boundary:])]

def main():
    warnings.filterwarnings('ignore')

    #filename = 'trainall/001_K.wav'
    all = 0
    recognised = 0
    unrecognised = []

    for file in os.listdir("trainall"):
        if file.endswith(".wav"):
            filename = file
            all += 1

        if re.match("\\d{3}_K.wav", filename):
            gender = 'K'
        elif re.match("\\d{3}_M.wav", filename):
            gender = 'M'

        w, signal = wavfile.read("trainall/" + filename)

        if len(signal.shape) > 1:     # only first channel
            signal = signal[:, 0]

        frequencies, signal_fft = getSignalData(w, signal)
        max_freq = harmonicProductSpectrum(frequencies, signal_fft)
        # print(max_freq)

        if max_freq < 170:
            print(filename + ' : M')
            print(max_freq)
            if gender == 'M':
                recognised += 1
            else:
                unrecognised.append(filename)
        else:
            print(filename + ' : K')
            print(max_freq)
            if gender == 'K':
                recognised += 1
            else:
                unrecognised.append(filename)

    print(recognised*100/all)
    # print(unrecognised)

if __name__ == '__main__':
    main()
