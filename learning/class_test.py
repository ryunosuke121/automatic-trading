from keras.models import load_model
from keras.models import Sequential
from learning.class_ml import PreprocessingService
from plot import FXPlotService


class ModelTestService:
    def __init__(self, path: str):
        self.model: Sequential = self.__load_model(path)

    def test(self, x_test, y_test):
        self.model.summary()
        print(x_test.shape, y_test.shape)
        predictions = self.model.predict(x_test)
        print(predictions.shape)

        correct_count = 0
        for i in range(len(predictions)):
            last_value = x_test[i][-1][0]
            correct_value = y_test[i]
            predicted_value = predictions[i]
            print(
                f"last_value: {last_value}, correct_value: {correct_value}, predicted_value: {predicted_value}"
            )
            if (predicted_value[0] > 0.5 and correct_value[0] == 1) or (
                predicted_value[1] > 0.5 and correct_value[1] == 1
            ):
                correct_count += 1

        print(f"正解率: {correct_count / len(predictions) * 100}%")

        # FXPlotService().plot(predictions, y_test)

    @staticmethod
    def __load_model(path: str) -> Sequential:
        return load_model(path)  # type: ignore


if __name__ == "__main__":
    preprosess_service = PreprocessingService("./data/USD_JPY_1day_2023_11.csv", 60, 3)
    x_test, y_test = preprosess_service.preprocess()

    modelTestService = ModelTestService("./models/class_model.h5")
    modelTestService.test(x_test, y_test)
