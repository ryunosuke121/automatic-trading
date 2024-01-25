from matplotlib import pyplot as plt
from numpy import ndarray
import pandas as pd
import matplotlib.animation as animation


class FXPlotService:
    def plot(self, pred: ndarray, correct: ndarray):
        plt.plot(pred)
        plt.plot(correct)
        plt.legend(["ask", "bid"])
        plt.show()


if __name__ == "__main__":
    df = pd.read_csv("./data/USD_JPY_1day_2023_12.csv")
    data = df.filter(["close"])
    data = data.values
    plt.plot(data)
    plt.show()
