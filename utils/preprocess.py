from log_config import logger
from numpy import ndarray
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential, load_model
from keras.layers import Dense, LSTM, Dropout
import numpy as np
import pickle

class PreprocessingService:
    def __init__(self, window_size: int, predict_min_after: int, scaler=None):
        if scaler is None:
            self.scaler = MinMaxScaler(feature_range=(0, 1))
        else:
            self.scaler = scaler

        self.window_size = window_size
        self.predict_min_after = predict_min_after
    
    def scale_process(self, data: ndarray) -> ndarray:
        scaled_data = self.MinMaxScale(data)
        scaled_data = np.reshape(scaled_data, (1, scaled_data.shape[0], scaled_data.shape[1]))
        return scaled_data

    # データをxとyに分割する(トレーニング用)
    def process_xy(self, data: ndarray) -> tuple[ndarray, ndarray]:
        # x_train, y_trainの作成
        preprocessed_data = self.MinMaxScale(data)
        x_train, y_train = self.split_xy(
            preprocessed_data, self.window_size, self.predict_min_after
        )
        x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
        return x_train, y_train

    # 0~1に正規化
    def MinMaxScale(self, data: ndarray) -> ndarray:
        return self.scaler.fit_transform(data)


    # 正規化を元に戻す
    def MinMaxInverseScale(self, data: ndarray) -> ndarray:
        return self.scaler.inverse_transform(data)
    
    def save_scaler(self, path: str):
        with open(f'scaler_{self.window_size}{self.predict_min_after}.pkl', 'wb') as file:
            pickle.dump(self.scaler, file)

    # 時系列データとそのpredict_min_after分次の値を分割する
    @staticmethod
    def split_xy(
        data: ndarray, window_size: int, predict_min_after: int
    ) -> tuple[ndarray, ndarray]:
        x, y = [], []
        for i in range(window_size + predict_min_after, len(data) + 1):
            x.append(
                data[i - window_size - predict_min_after : i - predict_min_after, 0]
            )

            # 上昇予測の場合
            if data[i - predict_min_after - 1, 0] < data[i - 1, 0]:
                y.append([1, 0])
            else:
                y.append([0, 1])
        return np.array(x), np.array(y)
    
    # パスからcsv形式のデータを読み込む
    @staticmethod
    def load_data(path: str) -> ndarray:
        df = pd.read_csv(path)
        data = df.filter(["close"])
        data = data.values
        return data