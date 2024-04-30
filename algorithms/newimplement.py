import sys
import os
import librosa
import numpy as np
import pandas as pd
import pyloudnorm as pyln
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pickle

class SVM_classifier():
    def __init__(self, learning_rate, no_of_iteration, lambda_parameter):
        self.learning_rate = learning_rate
        self.no_of_iteration = no_of_iteration
        self.lambda_parameter = lambda_parameter
        self.w = None
        self.b = None

    def fit(self, X, Y):
        self.m, self.n = X.shape
        self.w = np.zeros(self.n)
        self.b = 0
        for i in range(self.no_of_iteration):
            self.update_weights(X, Y)

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

    def predict(self, X):
        output = np.dot(X, self.w) - self.b
        predicted_labels = np.sign(output)
        return np.where(predicted_labels <= -1, 0, 1)

def extract_features(audio_file):
    try:
        y, sr = librosa.load(audio_file, sr=None)
        pitches, _ = librosa.core.piptrack(y=y, sr=sr)
        pitch_mean = pitches.mean()
        non_silent_frames = np.count_nonzero(librosa.effects.split(y, top_db=20))
        speech_duration = librosa.get_duration(y=y, sr=sr)
        speaking_rate = non_silent_frames / speech_duration * 60
        meter = pyln.Meter(sr)
        loudness = meter.integrated_loudness(y)
        return np.array([pitch_mean, speaking_rate, loudness])
    except Exception as e:
        print("Error extracting features:", e)
        return None

if __name__ == "__main__":
    # Check if audio file path is provided YES
    if len(sys.argv) != 2:
        print("Usage: python script.py <audio_file_path>")
        sys.exit(1)

    # Get the audio file path from command-line arguments
    audio_file_path = sys.argv[1]
    
    audio_data = pd.read_csv('../algorithms/extracted_features.csv') #New add
    features = audio_data.drop(columns='Label', axis=1) #New add
    target = audio_data['Label'] #New add
    #data standardization
    scaler = StandardScaler() #New add
    scaler.fit(features) #New add
    standardized_data = scaler.transform(features) #New add
    features = standardized_data
    target = audio_data['Label']#New add
    X_train, X_test, Y_train, Y_test = train_test_split(features, target, test_size=0.2, random_state=2) #New add
    classifier = SVM_classifier(learning_rate=0.001, no_of_iteration=1000, lambda_parameter=0.01) #New add
    classifier.fit(X_train, Y_train) #New add

    try:
        file_stats = os.stat(audio_file_path)
        
    except FileNotFoundError:
        print("File not found")

    # Check if the audio file exists
    if not os.path.exists(audio_file_path):
        print("Error: Audio file not found.")
        sys.exit(1)

    # Extract features from the audio
    features = extract_features(audio_file_path)
    #print(features)

    if features is None:    
        print("Error: Failed to extract features.")
        sys.exit(1)

    # Load the SVM model
    #model_file_path = '../algorithms/svm_model.sav'
    #if not os.path.exists(model_file_path):
       # print("Error: Model file not found.")
       # sys.exit(1)

    #try:
    #    loaded_model = pickle.load(open(model_file_path, 'rb'))
    #except Exception as e:
    #    print("Error loading model:", e)
    #    sys.exit(1)

    # Use the model to predict the label for the extracted features
    #predicted_label = loaded_model.predict(features.reshape(1, -1))

    input_data_reshaped = features.reshape(1, -1)
    std_data = scaler.transform(input_data_reshaped)
    prediction = classifier.predict(std_data)
    
    # Map the predicted label to 'introvert' or 'extrovert'
    label = 'extrovert' if prediction == 0 else 'introvert'

    
    # Print the pitch_mean
    print(features[0])
    # Print the speaking_rate
    print(features[1])
    # Print the loudness
    print(features[2])
    # Print the predicted label
    print(label)
