import sys
import matplotlib.pyplot as plt
import numpy as np
import librosa
from datetime import datetime
import pyloudnorm as pyln

def plot_audio_features(audio_file):
    try:
        # Load the audio file
        y, sr = librosa.load(audio_file)

        # Extract pitch using librosa's piptrack algorithm
        pitches, magnitudes = librosa.piptrack(y=y, sr=sr)

        # Extract the pitch track (fundamental frequency)
        pitch_track = np.nanmean(pitches, axis=0)

        # Create time axis
        times = librosa.times_like(pitch_track)

        # Plot the graphs
        plt.figure(figsize=(12, 6))  # Reduce the figure height

        # Plot pitch
        plt.subplot(3, 1, 1)
        plt.plot(times, pitch_track, label='Pitch Track (Hz)', color='#8F00FF')
        plt.ylabel('Frequency (Hz)')
        plt.title('Pitch')
        plt.legend()

        # Plot loudness
        plt.subplot(3, 1, 2)
        plt.plot(times, librosa.amplitude_to_db(librosa.feature.rms(y=y), ref=np.max)[0], label='Loudness (dB)', color='#8F00FF')
        plt.ylabel('Loudness (dB)')
        plt.title('Loudness')
        plt.legend()

        # Remove extra space
        plt.tight_layout(pad=1.0)  # Adjust the padding

        # Display the plots
        plt.show()

    except Exception as e:
        print("Error processing audio file:", e)


audio_file_path = './speechsample/extreduce3.wav'

plot_audio_features(audio_file_path)
