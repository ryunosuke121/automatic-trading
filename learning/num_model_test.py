from pyexpat import model
from keras.models import load_model
from keras.models import Sequential
from learning.num_ml import PreprocessingService
from utils.plot import FXPlotService


class ModelTestService:
    def __init__(self, path: str):
        self.model: Sequential = self.__load_model(path)

    def test(self, x_test, y_test):
        self.model.summary()
        print(x_test.shape, y_test.shape)
        predictions = self.model.predict(x_test)
        print(predictions.shape)
        correct_num = 0
        for i in range(len(predictions)):
            last_value = x_test[i][-1][0]
            correct_value = y_test[i]
            predicted_value = predictions[i][0]

            if (predicted_value > last_value and correct_value > last_value) or (
                predicted_value < last_value and correct_value < last_value
            ):
                print(
                    f"last_value: {last_value}, correct_value: {correct_value}, predicted_value: {predicted_value}"
                )
                correct_num += 1

        print(f"正解率: {correct_num / len(predictions) * 100}%")

        FXPlotService().plot(predictions, y_test)

    @staticmethod
    def __load_model(path: str) -> Sequential:
        return load_model(path)  # type: ignore


if __name__ == "__main__":
    preprosess_service = PreprocessingService("./data/USD_JPY_1day_2023_12.csv", 60, 3)
    x_test, y_test = preprosess_service.preprocess()

    modelTestService = ModelTestService("./models/model.h5")
    modelTestService.test(x_test, y_test)
