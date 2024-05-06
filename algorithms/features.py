import csv
import librosa
import numpy as np
from glob import glob
import pyloudnorm as pyln
import assemblyai as aai

#Set up the API endpoint and headers.
aai.settings.api_key = "66387440eacc419aaedd76a574988d96" 

def extract_features(audio_file):
    # Load audio file
    y, sr = librosa.load(audio_file, sr=None)

    # Extract pitch
    pitches, _ = librosa.core.piptrack(y=y, sr=sr)  # Magnitudes are not used
    pitch_mean = pitches.mean()

    # Calculate speech rate (words per minute)
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_file)

    if transcript.status == aai.TranscriptStatus.error:
        print(transcript.error)
    else:
        transcribed_text = transcript.text
        words = transcribed_text.split()  # Split text into words
        num_words = len(words)
    
        # Calculate the duration of the audio file (in minutes)
        audio_duration_minutes = transcript.audio_duration / 60
    
        # Calculate the speaking rate (words per minute)
        speaking_rate = num_words / audio_duration_minutes

    # Calculate loudness (mean sound intensity level in dB)
    meter = pyln.Meter(sr)
    loudness = meter.integrated_loudness(y)
    
    return pitch_mean, speaking_rate, loudness

# Example usage
audio_files = glob('./speechsample/*.wav')

# Create or open the CSV file for writing
with open('extracted_features.csv', 'w', newline='') as csvfile:
    # Define CSV writer
    writer = csv.writer(csvfile)
    # Write header row
    writer.writerow(['Pitch (Hz)', 'Speech Rate (Words Per Minute)', 'Average Loudness (dB)', 'Label'])
    # Extract features for each audio file and write to CSV
    for audio_file in audio_files:
        pitch, speech_rate, loudness = extract_features(audio_file)
        # Determine label based on filename
        # 0 - extrovert
        # 1 - introvert
        label = 0 if 'extreduce' in audio_file else 1
        writer.writerow([pitch, speech_rate, loudness, label])

print("Feature extraction completed and saved to 'extracted_features.csv'.")
