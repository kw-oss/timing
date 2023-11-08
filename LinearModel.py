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

class RecommendationModel:
    def __init__(self):
        self.scaler = StandardScaler()
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

if __name__ == "__main__":
    # 합칠 때, UI에서 선호도 가져오면 됩니다.
    Meat_pre = 1
    Noodle_pre = 2
    Rice_pre = 3
    FastFood_pre = 4

    # train_data 읽어오기
    TrainDF = pd.read_csv('train_data.csv', encoding = 'cp949')

    Meat = ['닭발', '곱창,막창,양', '돼지고기구이', '스테이크,립', '정육식당', '육류,고기요리', '돈가스', '고기뷔페', '양식', '족발,보쌈', '소고기구이', '닭갈비', '치킨,닭강정', '만두', '닭요리']
    Noodle = ['중식당', '국수', '아시아음식', '우동,소바', '샤브샤브']
    Rice = ['죽', '한식', '보리밥', '국밥', '김밥', '감자탕', '한정식', '백반,가정식', '곰탕,설렁탕']
    FastFood = ['햄버거', '베이커리', '피자', '카페', '카페,디저트']

    preference_dict = {
        'Meat': Meat,
        'Noodle': Noodle,
        'Rice': Rice,
        'FastFood': FastFood
    }

    # '선호도' 열을 추가하고 초기값을 3(중간)으로 설정
    TrainDF['선호도'] = 3

    # '종류' 열을 기반으로 '선호도' 값을 업데이트
    for category, preferences in preference_dict.items():
        TrainDF.loc[TrainDF['종류'].isin(preferences), '선호도'] = {
        'Meat': Meat_pre,
        'Noodle': Noodle_pre,
        'Rice': Rice_pre,
        'FastFood': FastFood_pre
    }[category]
        
    # 사용자의 음식 선호도에 맞게 TrianData를 학습시키기 위해서 추가하는 공식
    TrainDF['추천율'] = 0
    TrainDF['추천율'] = TrainDF['별점'].values * TrainDF['선호도'] + (TrainDF['리뷰'].values * 0.01)

    X = TrainDF[['별점', '리뷰', '선호도']].values   # 거리 추가해야 함 
    y = TrainDF['추천율'].values

    # 모델 생성
    model = RecommendationModel()
    model.train(X, y)

    # 실제 음식점 목록 읽어오기
    placesDF = pd.read_csv('naver_map_places.csv', encoding = 'cp949')
    placesDF['선호도'] = 3
    for category, preferences in preference_dict.items():
        placesDF.loc[placesDF['종류'].isin(preferences), '선호도'] = {
            'Meat': Meat_pre,
            'Noodle': Noodle_pre,
            'Rice': Rice_pre,
            'FastFood': FastFood_pre
        }[category]
    realX = placesDF[['별점', '리뷰', '선호도']].values

    # 여기 X에는 실제 데이터가 들어가야합니다! (지금은 잘 나오나 원래 데이터로 돌려봤어요.)
    Predict_data = model.predict(realX)

    # 실제 데이터프레임(placesDF 말고)에서 '추천율' column을 생성한 후에 예측한 추천율을 넣어놓습니다.
    placesDF['추천율'] = 0
    placesDF['추천율'] = Predict_data

    # 추천율을 기준으로 정렬합니다. (추천율이 높은 순서대로 하기위해서 ascending = False를 사용했습니다.)
    placesDF.sort_values('추천율', ascending = False)

    print(TrainDF)