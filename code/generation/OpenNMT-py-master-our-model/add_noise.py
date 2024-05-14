import librosa
import soundfile
import matplotlib.pyplot as plt
import numpy as np
import math

file_path = '/Users/yima/Downloads/ElevenLabs_2024-05-14T00_11_58_Chia-Wei-Chen_pvc_s100_sb100_se0_b_m2.mp3'
#
#
signal, sr = librosa.load(file_path, sr=16000)
# plt.plot(signal)
#
RMS = math.sqrt(np.mean(signal**2))

STD_n = 0.01
noise = np.random.normal(0, STD_n, signal.shape[0])
#
# # X=np.fft.rfft(noise)
# # radius,angle=to_polar(X)
#
signal_noise = signal+noise

soundfile.write('/Users/yima/Downloads/ElevenLabs_2024-05-14T00_11_58_Chia-Wei-Chen_pvc_s100_sb100_se0_b_m2_NOISE.wav', signal_noise, 16000)
