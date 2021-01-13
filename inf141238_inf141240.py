from scipy.io import wavfile
from scipy.signal import decimate
import numpy as np
import matplotlib.pyplot as plt
import warnings

<<<<<<< HEAD
=======

>>>>>>> 5beabd1ebc7a9e70e35b89d390a7f7632c3e8391
def getSignalData(w, signal):
    n = signal.shape[0]
    frequencies = np.arange(n) / n * w
    signal_kaiser = signal * np.kaiser(n, 100)
    signal_kaiser_fft = abs(np.fft.fft(signal_kaiser)) / (0.5 * n)

    return frequencies, signal_kaiser_fft

<<<<<<< HEAD
=======

>>>>>>> 5beabd1ebc7a9e70e35b89d390a7f7632c3e8391
def harmonicProductSpectrum(frequencies, signal_fft):
    fig = plt.figure(figsize=(8, 10), dpi=80)
    ax = fig.add_subplot(5, 1, 1)
    ax.plot(frequencies, signal_fft, '-')
    ax.set_xlim(0, 1000)

    signal_hps = signal_fft
    for i in np.arange(2, 6):
        dec = decimate(signal_fft, i)
        signal_hps[:len(dec)] *= dec
        ax = fig.add_subplot(5, 1, i)
        ax.plot(frequencies, signal_hps, '-')
        ax.set_xlim(0, 1000)

    plt.show()

    return frequencies[np.argmax(signal_hps)]

<<<<<<< HEAD
def main():
    warnings.filterwarnings('ignore')
=======

def main():
    warnings.filterwarnings('ignore')

>>>>>>> 5beabd1ebc7a9e70e35b89d390a7f7632c3e8391
    filename = 'trainall/001_K.wav'
    w, signal = wavfile.read(filename)

    if signal.shape[1] > 1:     # only first channel
        signal = signal[:, 0]

    frequencies, signal_fft = getSignalData(w, signal)
    max_freq = harmonicProductSpectrum(frequencies, signal_fft)
<<<<<<< HEAD
=======

>>>>>>> 5beabd1ebc7a9e70e35b89d390a7f7632c3e8391
    print(max_freq)

    if max_freq < 170:
        print('M')
    else:
        print('K')

<<<<<<< HEAD
=======

>>>>>>> 5beabd1ebc7a9e70e35b89d390a7f7632c3e8391
if __name__ == '__main__':
    main()
