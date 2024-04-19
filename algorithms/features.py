import csv
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
audio_files = glob('../speechsample/intreduce/*.wav')

# Create or open the CSV file for writing
with open('extracted_features.csv', 'w', newline='') as csvfile:
    # Define CSV writer
    writer = csv.writer(csvfile)
    # Write header row
    writer.writerow(['Audio File', 'Pitch (Hz)', 'Speech Rate (Words Per Minute)', 'Average Loudness (dB)', 'Label'])
    # Extract features for each audio file and write to CSV
    for audio_file in audio_files:
        pitch, speech_rate, loudness = extract_features(audio_file)
        # Determine label based on filename
        label = 'extrovert' if 'extreduce' in audio_file else 'introvert'
        writer.writerow([audio_file, pitch, speech_rate, loudness, label])

print("Feature extraction completed and saved to 'extracted_features.csv'.")