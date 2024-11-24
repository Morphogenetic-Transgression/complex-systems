import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt
from copy import copy


def softmax(x: np.ndarray):
    return np.exp(x)/sum(np.exp(x))


class AudioSignalEntropy:
    def __init__(self, figures_storage_path: str, audio_file_path: str = None, option: int = None): # in wav format
        self.signal_fig_path = f'{figures_storage_path}/signal.png'
        self.fft_fig_path = f'{figures_storage_path}/fft.png'
        self.distribution_fig_path = f'{figures_storage_path}/distribution.png'
        self.histogram_fig_path = f'{figures_storage_path}/histogram.png'
        self.histogram_bins = 100
        self.update_signal(audio_file_path, option)

    def pure_sine_array(self, frequency=440):
        fs = 1100  # Sampling frequency (Hz)
        duration = 2  # seconds
        frequency = frequency  # A4 note frequency (Hz)
        self.time = np.linspace(0, duration, int(fs * duration), endpoint=False)
        self.signal = np.sin(2 * np.pi * frequency * self.time)

    def noisy_sine_array(self, frequency=440):
        fs = 1100  # Sampling frequency (Hz)
        duration = 2  # seconds
        frequency = frequency  # A4 note frequency (Hz)
        self.time = np.linspace(0, duration, int(fs * duration), endpoint=False)
        self.signal = np.sin(2 * np.pi * frequency * self.time) + np.random.normal(loc=0, scale=1, size=len(self.time))

    def gauss_noise_array(self):
        fs = 1100  # Sampling frequency (Hz)
        duration = 2  # seconds
        self.time = np.linspace(0, duration, int(fs * duration), endpoint=False)
        self.signal = np.random.normal(loc=0, scale=1, size=len(self.time))
        
    def uniform_noise_array(self):
        fs = 1100  # Sampling frequency (Hz)
        duration = 2  # seconds
        self.time = np.linspace(0, duration, int(fs * duration), endpoint=False)
        self.signal = np.random.uniform(low=0, high=1, size=len(self.time))
        
    def audio_signal_array(self, audio_file_path: str):
        rate, self.signal = wavfile.read(audio_file_path)
        length = self.signal.shape[0] / rate
        self.time = np.linspace(0., length, self.signal.shape[0])

    def update_signal(self, audio_file_path: str = None, option: int = None):
        assert (audio_file_path is not None) or (option is not None), "specify audio_file_path or option [1, 2, 3, 4]"
        if (audio_file_path is not None) and (audio_file_path):
            self.audio_signal_array(audio_file_path)
        elif option == 1:
            self.pure_sine_array()
        elif option == 2:
            self.noisy_sine_array()
        elif option == 3:
            self.gauss_noise_array()
        elif option == 4:
            self.uniform_noise_array()
        else:
            assert False, "Specified option does not exist."
        self.figure_time()
        self.spectral_decomposition()
        self.figure_frequency()
        self.amplitude_frequency_as_distribution()
        self.figure_hist()
        self.figure_distribution()
        self.calculate_entropy()           

    def figure_time(self):
        fig, ax = plt.subplots()
        ax.plot(self.time, self.signal)
        ax.set_title('Audio Signal (in time domain)')
        ax.set_xlabel("Time [s]")
        ax.set_ylabel("Amplitude")
        fig.savefig(self.signal_fig_path)
        plt.close(fig)  

    def figure_frequency(self):
        fig, ax = plt.subplots()
        ax.plot(self.fft_frequency, self.fft)
        ax.set_title('FFT of the Signal (in frequency domain)')
        ax.set_xlabel('Frequency (Hz)')
        ax.set_ylabel('Amplitude')
        fig.savefig(self.fft_fig_path)
        plt.close(fig)

    def figure_hist(self):
        fig, ax = plt.subplots()
        ax.hist(self.signal, self.histogram_bins)
        ax.set_title(f'Histogram ({self.histogram_bins} bins)')
        ax.set_xlabel('Value')
        ax.set_ylabel('Number of values in bin')
        fig.savefig(self.histogram_fig_path)
        plt.close(fig)

    def figure_distribution(self):
        fig, ax = plt.subplots()
        ax.plot(self.fft_frequency, self.distribution)
        ax.set_title('Scaled distribution')
        ax.set_xlabel('Frequency (Hz)')
        ax.set_ylabel('pseudo probability')
        fig.savefig(self.distribution_fig_path)
        plt.close(fig)

    def spectral_decomposition(self):
        steps_number = len(self.time)
        duration = self.time.max()
        # Applying FFT
        fft_result = np.fft.fft(self.signal)
        freq = np.fft.fftfreq(self.time.shape[-1], d=duration/steps_number)
        real_positive_amplitude = np.abs(fft_result[0 : steps_number//2])
        real_positive_frequency = freq[0 : steps_number//2]
        self.fft = real_positive_amplitude
        self.fft_frequency = real_positive_frequency
        self.fft_scaled = copy(self.fft)
        if self.fft_scaled.max() != 0:
            self.fft_scaled /= self.fft_scaled.max()

    def amplitude_frequency_as_distribution(self):
        self.distribution = softmax(self.fft_scaled)

    def calculate_entropy(self):
        tmp_scaler = 100
        self.entropy = np.dot(tmp_scaler*self.distribution, np.log(tmp_scaler)-np.log(tmp_scaler*self.distribution)) / tmp_scaler
        # self.entropy = np.dot(self.distribution, np.log(sum(np.exp(self.fft_scaled))) - self.fft_scaled)



# plt.plot(self.time, self.signal)
# plt.title('Audio Signal (in time domain)')
# plt.xlabel("Time [s]")
# plt.ylabel("Amplitude")
# plt.savefig(self.signal_fig_path)
# # plt.show()


