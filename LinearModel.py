# Machine Learning을 위한 Library
import numpy as np
import tensorflow as tf
from tensorflow import keras
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
from sklearn import datasets

# File I/O 를 위한 Library
import pandas as pd
from os.path import join

class RecommendationModel:
    def __init__(self):
        self.model = self.build_model()

    def build_model(self):
        model = keras.Sequential([
            keras.layers.Dense(32, activation='relu', input_shape=(3,)),  # Adjust input shape and layer configuration
            keras.layers.Dense(16, activation='relu'),
            keras.layers.Dense(1, activation='linear')
        ])
        model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])
        return model

    def train(self, X, y, epochs=100, batch_size=32, test_size=0.2, random_state=42):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        self.model.fit(X_train_scaled, y_train, epochs=epochs, batch_size=batch_size, validation_data=(X_test_scaled, y_test))

    def evaluate(self, X, y):
        X_scaled = StandardScaler().transform(X)
        loss, mae = self.model.evaluate(X_scaled, y)
        return loss, mae

    def predict(self, X):
        X_scaled = StandardScaler().transform(X)
        predictions = self.model.predict(X_scaled)
        return predictions

if __name__ == "__main__":
    # 합칠 때, UI에서 선호도 가져오면 됩니다.
    Meat_pre = 1
    Noodle_pre = 2
    Rice_pre = 3
    FastFood_pre = 4

    # map에서 따온 정보들 저장한 csv
    placesDF = pd.read_csv('preference.csv', encoding = 'cp949')

    Meat = ['닭발', '곱창,막창,양', '돼지고기구이', '스테이크,립', '정육식당', '육류,고기요리', '돈가스', '고기뷔페', '양식', '족발,보쌈', '소고기구이', '닭갈비', '치킨,닭강정', '만두']
    Noodle = ['중식당', '국수', '아시아음식', '우동,소바']
    Rice = ['죽', '한식', '보리밥', '국밥', '김밥', '감자탕', '한정식', '백반,가정식']
    FastFood = ['햄버거', '베이커리', '피자']

    preference_dict = {
        'Meat': Meat,
        'Noodle': Noodle,
        'Rice': Rice,
        'FastFood': FastFood
    }

    # '선호도' 열을 추가하고 초기값을 0으로 설정
    placesDF['선호도'] = 0

    # '종류' 열을 기반으로 '선호도' 값을 업데이트
    for category, preferences in preference_dict.items():
        placesDF.loc[placesDF['종류'].isin(preferences), '선호도'] = placesDF['선호도'] + {
        'Meat': Meat_pre,
        'Noodle': Noodle_pre,
        'Rice': Rice_pre,
        'FastFood': FastFood_pre
    }[category]

    X = placesDF[['별점', '리뷰', '선호도']].values   # 거리 추가해야 함 
    y = placesDF['추천율'].values

    # 모델 생성
    model = RecommendationModel()
    model.train(X, y)