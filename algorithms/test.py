
import librosa
import numpy as np
from glob import glob
import pyloudnorm as pyln

def extract_features(audio_file):
    # Load audio file
    y, sr = librosa.load(audio_file, sr=None)

    # Extract pitch
    pitches, _ = librosa.core.piptrack(y=y, sr=sr)  # Magnitudes are not used
    pitch_mean = pitches.mean()

    # Calculate speech rate (words per minute)
    # Count number of non-silent frames
    non_silent_frames = np.count_nonzero(librosa.effects.split(y, top_db=20))

    # Estimate speech duration (in minutes)
    speech_duration = librosa.get_duration(y=y, sr=sr)

    # Calculate speech rate
    speaking_rate = non_silent_frames / speech_duration * 60

    # Calculate loudness (mean sound intensity level in dB)
    meter = pyln.Meter(sr)
    loudness = meter.integrated_loudness(y)
    
    return pitch_mean, speaking_rate, loudness

# Example usage
audio_files = glob('D:\speechsample\intreduce\*.wav')
src = audio_files[1]  # Choose a specific audio file
print(src)
print("Audio File:", src)
pitch, speech_rate, loudness = extract_features(src)
print("Pitch (Hz):", pitch)
print("Speech Rate (Words Per Minute):", speech_rate)
print("Average Loudness (dB):", loudness)