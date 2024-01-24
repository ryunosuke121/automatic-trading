from learning.num_ml import ModelFitService, PreprocessingService
from plot import FXPlotService


def main():
    preprosess_service = PreprocessingService("./data/USD_JPY_1day_2023_11.csv", 60, 3)
    x, y = preprosess_service.preprocess()
    print(x[0], y[0])
    print(x.shape)
    print(y.shape)
    model_fit_service = ModelFitService(60, 3)
    model_fit_service.fit(x, y)


if __name__ == "__main__":
    main()
