# Machine Learning을 위한 Library
import numpy as np
import tensorflow as tf
from tensorflow import keras
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from sklearn import datasets

# File I/O 를 위한 Library
import pandas as pd
from os.path import join

# String Library
import re

class RecommendationModel:
    def __init__(self):
        self.scaler = StandardScaler()
        self.model = self.build_model()

    def build_model(self):
        model = keras.Sequential([
            keras.layers.Dense(32, activation='relu', input_shape=(4,)),  # Adjust input shape and layer configuration
            keras.layers.Dense(16, activation='relu'),
            keras.layers.Dense(1, activation='linear')
        ])
        model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])
        return model

    def train(self, X, y, epochs=150, batch_size=32, test_size=0.2, random_state=42):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
        self.scaler.fit(X_train)
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        self.model.fit(X_train_scaled, y_train, epochs=epochs, batch_size=batch_size, validation_data=(X_test_scaled, y_test))

    def evaluate(self, X, y):
        X_scaled = StandardScaler().transform(X)
        loss, mae = self.model.evaluate(X_scaled, y)
        return loss, mae

    def predict(self, X):
        X_scaled = self.scaler.transform(X)
        predictions = self.model.predict(X_scaled)
        return predictions

def Extract_Numbers(text):
    numbers = re.findall(r'\d+', str(text))
    return int(numbers[0]) if numbers else 0
