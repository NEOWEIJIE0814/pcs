import argparse
import sys
import librosa
import numpy as np
import pyloudnorm as pyln
from sklearn.preprocessing import StandardScaler
import pickle
import io
import base64

class SVM_classifier():
    # Initialize SVM classifier with hyperparameters
    def __init__(self, learning_rate, no_of_iteration, lambda_parameter):
        self.learning_rate = learning_rate
        self.no_of_iteration = no_of_iteration
        self.lambda_parameter = lambda_parameter
        self.w = None
        self.b = None

    # Fit the dataset to the SVM classifier
    def fit(self, X, Y):
        self.m, self.n = X.shape
        self.w = np.zeros(self.n)
        self.b = 0
        for i in range(self.no_of_iteration):
            self.update_weights(X, Y)

    # Update weights and bias values
    def update_weights(self, X, Y):
        y_label = np.where(Y <= 0, -1, 1)
        for index, x_i in enumerate(X):
            condition = y_label[index] * (np.dot(x_i, self.w) - self.b) >= 1
            if condition:
                dw = 2 * self.lambda_parameter * self.w
                db = 0
            else:
                dw = 2 * self.lambda_parameter * self.w - np.dot(x_i, y_label[index])
                db = y_label[index]
            self.w -= self.learning_rate * dw
            self.b -= self.learning_rate * db

    # Predict the label for a given input value
    def predict(self, X):
        output = np.dot(X, self.w) - self.b
        predicted_labels = np.sign(output)
        return np.where(predicted_labels <= -1, 0, 1)

def extract_features(audio_file):
    y, sr = librosa.load(audio_file, sr=None)
    pitches, _ = librosa.core.piptrack(y=y, sr=sr)
    pitch_mean = pitches.mean()
    non_silent_frames = np.count_nonzero(librosa.effects.split(y, top_db=20))
    speech_duration = librosa.get_duration(y=y, sr=sr)
    speaking_rate = non_silent_frames / speech_duration * 60
    meter = pyln.Meter(sr)
    loudness = meter.integrated_loudness(y)
    return np.array([pitch_mean, speaking_rate, loudness])

if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("audio_file", help="Path to the audio file")
    args = parser.parse_args()

    try:
        # Decode the audio blob data received from PHP
        with open(args.audio_file, 'rb') as f:
            audio_blob_data = f.read()

        # Write the decoded audio blob data to a .wav file
        output_filename = 'output.wav'
        with open(output_filename, 'wb') as f:
            f.write(audio_blob_data)

        # Extract features from the audio
        features = extract_features(output_filename)

        # Load the SVM model
        loaded_model = pickle.load(open('./svm_model.sav', 'rb'))

        # Reshape the input data
        input_data_reshaped = features.reshape(1, -1)

        # Use the model to predict the label for the extracted features
        predicted_label = loaded_model.predict(input_data_reshaped)

        # Map the predicted label to 'introvert' or 'extrovert'
        label = 'extrovert' if predicted_label == 0 else 'introvert'

        #  Print the predicted label
        sys.stdout.write(label)
        sys.stdout.flush()

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)