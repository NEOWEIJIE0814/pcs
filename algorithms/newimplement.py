import sys
import librosa
import numpy as np
import pyloudnorm as pyln
from sklearn.preprocessing import StandardScaler
import pickle

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
    
    # Get the audio file path from command-line arguments
    audio_file_path = str(sys.argv[1])

    # Extract features from the audio
    features = extract_features(audio_file_path)

    # Load the SVM model
    loaded_model = pickle.load(open('./algorithms/svm_model.sav', 'rb'))

    # Reshape the input data
    input_data_reshaped = features.reshape(1, -1)

    # Use the model to predict the label for the extracted features
    predicted_label = loaded_model.predict(input_data_reshaped)

    # Map the predicted label to 'introvert' or 'extrovert'
    label = 'extrovert' if predicted_label == 0 else 'introvert'

    # Print the predicted label
    print(label)
