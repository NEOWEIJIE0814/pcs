import sys
import matplotlib.pyplot as plt
import numpy as np
import librosa
from datetime import datetime
import pyloudnorm as pyln
import assemblyai as aai

#Set up the API endpoint and headers.
aai.settings.api_key = "66387440eacc419aaedd76a574988d96" 

def extract_features(audio_file):
    try:
        # Transcribe audio to text
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(audio_file)

        if transcript.status == aai.TranscriptStatus.error:
            print(transcript.error)
            return None
        else:
            transcribed_text = transcript.text
            words = transcribed_text.split()  # Split text into words
            num_words = len(words)
    
            # Calculate the duration of the audio file (in minutes)
            audio_duration_minutes = transcript.audio_duration / 60
    
            # Calculate the speaking rate (words per minute)
            speaking_rate = num_words / audio_duration_minutes
            return speaking_rate
    except Exception as e:
        print("Error extracting features:", e)
        return None

def plot_audio_features(audio_file):
    try:
        # Load the audio file
        y, sr = librosa.load(audio_file)

        # Extract features
        features = extract_features(audio_file)
        if features is None:
            print("Error: Unable to extract features from audio file.")
            return

        speaking_rate = features

        # Extract pitch using librosa's yin algorithm
        f0, voiced_flag, voiced_probs = librosa.pyin(y, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'))

        # Compute loudness using extracted features
        # Compute loudness
        loudness = librosa.amplitude_to_db(librosa.feature.rms(y=y), ref=np.max)

        # Create time axis
        times = librosa.times_like(loudness)

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
        plt.axhline(y=speaking_rate, color='r', linestyle='--', label='Speaking Rate (words per minute)')
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

    except Exception as e:
        print("Error processing audio file:", e)

if __name__ == "__main__":
    # Check if audio file path is provided
    if len(sys.argv) != 2:
        print("Usage: python script.py <audio_file_path>")
        sys.exit(1)

    # Get the audio file path from command-line arguments
    audio_file_path = sys.argv[1]

    plot_audio_features(audio_file_path)
