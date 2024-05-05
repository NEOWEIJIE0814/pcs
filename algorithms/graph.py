import sys
import matplotlib
matplotlib.use('TkAgg')  # Specify the backend explicitly

import numpy as np
import librosa
import matplotlib.pyplot as plt
from datetime import datetime

def calculate_speaking_rate(y, sr):
    # Count non-silent frames and calculate speaking rate
    non_silent_frames = np.count_nonzero(librosa.effects.split(y, top_db=20))
    speech_duration = librosa.get_duration(y=y, sr=sr)
    speaking_rate = non_silent_frames / speech_duration * 60
    return speaking_rate

def plot_audio_features(audio_file):
    # Load the audio file
    y, sr = librosa.load(audio_file)

    # Extract pitch using librosa's yin algorithm
    f0, voiced_flag, voiced_probs = librosa.pyin(y, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'))

    # Compute loudness
    loudness = librosa.amplitude_to_db(librosa.feature.rms(y=y), ref=np.max)

    # Create time axis
    times = librosa.times_like(loudness)

    # Calculate speaking rate for each minute
    num_segments = int(np.ceil(y.shape[0] / sr / 60))  # Number of one-minute segments
    speaking_rates = []
    for i in range(num_segments):
        start_sample = i * sr * 60
        end_sample = min((i + 1) * sr * 60, len(y))
        speaking_rate = calculate_speaking_rate(y[start_sample:end_sample], sr)
        speaking_rates.append(speaking_rate)

    # Plot the graphs
    plt.figure(figsize=(12, 6))  # Reduce the figure height

    # Plot pitch
    plt.subplot(3, 1, 1)
    plt.plot(librosa.times_like(f0), f0, label='Pitch (Hz)')
    plt.ylabel('Frequency (Hz)')
    plt.title('Pitch')

    # Plot loudness
    plt.subplot(3, 1, 2)
    plt.plot(times, loudness[0], label='Loudness (dB)')
    plt.ylabel('Loudness (dB)')
    plt.title('Loudness')

    # Plot speaking rate
    plt.subplot(3, 1, 3)
    plt.plot(np.arange(num_segments) + 1, speaking_rates, marker='o', linestyle='-')
    plt.xlabel('Minute')
    plt.ylabel('Speaking Rate (words per minute)')
    plt.title('Speaking Rate')

    # Remove extra space
    plt.tight_layout(pad=1.0)  # Adjust the padding

    # Save the plot
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    save_path = f"C:/Users/Windows10/Desktop/xampp/htdocs/pcs/audiographs/graph_{now}.png"
    relative_path = f"../audiographs/graph_{now}.png"
    try:
        plt.savefig(save_path)
        print(relative_path)
    except Exception as e:
        print("Error saving plot:", e)
    
    
if __name__ == "__main__":
    # Check if audio file path is provided YES
    if len(sys.argv) != 2:
        print("Usage: python script.py <audio_file_path>")
        sys.exit(1)

    # Get the audio file path from command-line arguments
    audio_file_path = sys.argv[1]
    
    #audio_file = ('./speechsample/intreduce30.wav')  # Replace with your audio file path
    plot_audio_features(audio_file_path)
    
