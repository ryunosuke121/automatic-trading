from numpy import ndarray
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential, load_model
from keras.layers import Dense, LSTM, Dropout
import numpy as np
from utils import preprocess


class ModelFitService:
    def __init__(self, window_size: int, predict_min_after: int):
        self.window_size = window_size
        self.predict_min_after = predict_min_after
        self.model = self.__init_model(window_size, 1)

    def fit(self, x_train: ndarray, y_train: ndarray):
        self.model.fit(x_train, y_train, batch_size=516, epochs=100)
        self.model.save(f"./models/class_model_{self.window_size}_{self.predict_min_after}.h5")

    def addition_fit(self, model_path: str, x_train: ndarray, y_train: ndarray):
        model = self.__load_model(model_path)
        model.fit(x_train, y_train, batch_size=516, epochs=100)
        model.save(f"./models/class_model_{self.window_size}_{self.predict_min_after}.h5")

    @staticmethod
    def __init_model(time_steps: int, features: int) -> Sequential:
        model = Sequential()
        model.add(LSTM(50, return_sequences=True, input_shape=(time_steps, features)))
        model.add(Dropout(0.2))
        model.add(LSTM(units=50, return_sequences=True))
        model.add(Dropout(0.2))
        model.add(LSTM(units=50, return_sequences=True))
        model.add(Dropout(0.2))
        model.add(LSTM(units=50))
        model.add(Dropout(0.2))
        model.add(Dense(units=2, activation="softmax"))
        model.compile(
            optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"]
        )
        return model

    @staticmethod
    def __load_model(path: str) -> Sequential:
        return load_model(path)  # type: ignore


if __name__ == "__main__":
    preprocess_service = preprocess.PreprocessingService(120, 15)
    data = preprocess_service.load_data("")
    x_train, y_train = preprocess_service.process_xy(data)
    preprocess_service.save_scaler("./scalers")

    modelFitService = ModelFitService(120, 15)
    modelFitService.fit(x_train, y_train)
    # modelFitService.addition_fit("./models/class_model.h5", x_train, y_train)
