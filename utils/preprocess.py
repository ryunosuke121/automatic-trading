from numpy import ndarray
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential, load_model
from keras.layers import Dense, LSTM, Dropout
import numpy as np

class PreprocessingService:
    def __init__(self, path: str, window_size: int, predict_min_after: int):
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.window_size = window_size
        self.predict_min_after = predict_min_after
        self.data: ndarray = self.load_data(path)

    def preprocess(self) -> tuple[ndarray, ndarray]:
        # x_train, y_trainの作成
        preprocessed_data = self.MinMaxScale(self.data)
        x_train, y_train = self.process_xy_data(
            preprocessed_data, self.window_size, self.predict_min_after
        )
        x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
        return x_train, y_train

    # 0~1に正規化
    def MinMaxScale(self, data: ndarray) -> ndarray:
        scaled_data = self.scaler.fit_transform(data)
        return scaled_data

    # 正規化を元に戻す
    def MinMaxInverseScale(self, data: ndarray) -> ndarray:
        return self.scaler.inverse_transform(data)

    # パスからcsv形式のデータを読み込む
    @staticmethod
    def load_data(path: str) -> ndarray:
        df = pd.read_csv(path)
        data = df.filter(["close"])
        data = data.values
        return data
    
    # 時系列データとそのpredict_min_after分次の値を分割する
    @staticmethod
    def process_xy_data(
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