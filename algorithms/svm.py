import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


class SVM_classifier():
    
    #initiating the hyperparameters
    def __init__(self, learning_rate, no_of_iteration, lambda_parameter ):
        self.learning_rate = learning_rate
        self.no_of_iteration = no_of_iteration
        self.lambda_parameter = lambda_parameter
        
    #fitting the dataset to svm classifier    
    def fit(self, X, Y):
        
        # m ->num of data points -> num of rows
        # n -> num of input features -> num of columns
        self.m, self.n = X.shape
        
        #initiating weight value and bias value
        self.w = np.zeros(self.n)
        
        self.b = 0
        
        self.X = X
        
        self.Y = Y
        
        #implementing Gradient Descent Algori for Optimization
        
        for i in range(self.no_of_iteration):
            self.update_weights()
            
        
        
    #function for updating the weight and bias valye    
    def update_weights(self, ):
        
        y_label = np.where(self.Y <=0, -1, 1)
        
        #gradients (dw, db)
        for index, x_i in  enumerate(self.X): 
            
            condition = y_label[index] * (np.dot(x_i, self.w) - self.b) >= 1
            
            if(condition == True):
                dw = 2 * self.lambda_parameter * self.w
                db = 0
                
            else:
                dw = 2 * self.lambda_parameter * self.w - np.dot(x_i,y_label[index])
                db = y_label[index]
                
            self.w = self.w - self.learning_rate * dw
            
            self.b = self.b - self.learning_rate * db
        
    #predict the label for a given input value   
    def predict(self, X):
        
        output = np.dot(X, self.w) - self.b
        
        predicted_labels = np.sign(output)
        
        y_hat = np.where(predicted_labels <= -1, 0, 1)
        
        return y_hat
        
        
    
# model = SVM_classifier(learning_rate=0.001, no_of_iteration=1000, lambda_parameter=0.01)
        
#loading the data from the csv file to pandas dataframe

audio_data = pd.read_csv('./extracted_features.csv')
   
#print the first 5 row of the dataframe
audio_data.head()

# num of rows and columns in the dataset

audio_data.shape

# getting the statistical measures of the dataset
audio_data.describe


audio_data['Label'].value_counts()
# 0 - extrovert
# 1 - introvert

#separating features and target

features = audio_data.drop(columns='Label', axis=1)

target = audio_data['Label']

#print(features)
#print(target)

#data standardization

scaler = StandardScaler()

scaler.fit(features)

standardized_data = scaler.transform(features)

#print(standardized_data)

features = standardized_data
target = audio_data['Label']

#Train test split function
#test_size=0.2 mean 20% data become test data
X_train, X_test, Y_train, Y_test = train_test_split(features, target, test_size=0.2, random_state=2)

#print(features.shape, X_train.shape, X_train.shape)

#Training the model
#SVM Classifier

classifier = SVM_classifier(learning_rate=0.001, no_of_iteration=1000, lambda_parameter=0.01)

#--Training SVM with data

classifier.fit(X_train, Y_train)

# --Model Evaluation
# --Accuracy score
# --Accuracy on training data

X_train_prediction = classifier.predict(X_train)
training_data_accuracy = accuracy_score(Y_train, X_train_prediction)

#print("accuracy score on train data: ", training_data_accuracy)

# --Accuracy on test data

X_test_prediction = classifier.predict(X_test)
training_data_accuracy = accuracy_score(Y_test, X_test_prediction)

#print("accuracy score on test data: ", training_data_accuracy)

#---------------------------------------------------------------
#--Building a predictive system

input_data = (21.90977,210.6122796672837,-26.711063007447496)

# --change the input data to numpy array

input_data_as_np = np.array(input_data)

#-- reshape the array

input_data_reshaped = input_data_as_np.reshape(1, -1)

#standardizing the input data
std_data = scaler.transform(input_data_reshaped)
print(std_data)

prediction = classifier.predict(std_data)
print(prediction)

if(prediction[0] == 0):
    print("The person is extrovert")
    
else:
    print("The person is introvert")