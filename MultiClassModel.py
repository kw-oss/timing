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

class MultiClassModel:
    def __init__(self, input_dim, output_dim):
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.model = self.build_model()
    
    def build_model(self):
        model = keras.Sequential([
            keras.layers.Dense(64, activation='relu', input_dim=self.input_dim),
            keras.layers.Dense(64, activation='relu'),
            keras.layers.Dense(self.output_dim, activation='softmax')
        ])
        model.compile(optimizer='adam',
                      loss='sparse_categorical_crossentropy',
                      metrics=['accuracy'])
        return model

    def preprocess_data(self, X, y, test_size=0.2, random_state=None):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)

        return X_train, X_test, y_train, y_test

    def train(self, X_train, y_train, epochs=50, batch_size=32, validation_split=0.1):
        self.history = self.model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, validation_split=validation_split)
    
    def evaluate(self, X_test, y_test):
        y_pred = self.model.predict(X_test)
        y_pred_classes = np.argmax(y_pred, axis=1)
        accuracy = accuracy_score(y_test, y_pred_classes)
        return accuracy

    def plot_training_history(self):
        if hasattr(self, 'history'):
            plt.figure(figsize=(12, 4))
            plt.subplot(1, 2, 1)
            plt.plot(self.history.history['loss'], label='Train Loss')
            plt.plot(self.history.history['val_loss'], label='Validation Loss')
            plt.legend()
            plt.xlabel('Epoch')
            plt.title('Train & Validation Loss')

            plt.subplot(1, 2, 2)
            plt.plot(self.history.history['accuracy'], label='Train Accuracy')
            plt.plot(self.history.history['val_accuracy'], label='Validation Accuracy')
            plt.legend()
            plt.xlabel('Epoch')
            plt.title('Train & Validation Accuracy')

            plt.show()
        else:
            print("Train Falied.")

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
    y = placesDF['순위'].values


    '''
    # 예제 데이터 셋
    iris = datasets.load_iris()
    X = iris.data
    y = iris.target

    # 모델 인스턴스 생성
    model = MultiClassModel(input_dim=X.shape[1], output_dim=3)

    # 데이터 분할, 표준화, 모델 훈련, 모델 평가
    X_train, X_test, y_train, y_test = model.preprocess_data(X, y, test_size=0.2, random_state=42)
    model.train(X_train, y_train, epochs=50, batch_size=32, validation_split=0.1)
    accuracy = model.evaluate(X_test, y_test)
    print(f'테스트 세트 정확도: {accuracy}')

    # 훈련 히스토리 시각화
    model.plot_training_history()
    '''