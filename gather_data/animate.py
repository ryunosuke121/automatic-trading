from matplotlib import pyplot as plt
from numpy import ndarray
import pandas as pd
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation


class RealtimeFXVisualizer:
    def __init__(self):
        self.data = pd.DataFrame(
            columns=["ask", "bid", "timestamp", "symbol", "status"]
        )
        self.fig, self.ax = plt.subplots()
        (self.ask_line,) = self.ax.plot([], [], lw=2)
        (self.bid_line,) = self.ax.plot([], [], lw=1)

        # アニメーションの初期化
        self.ani = FuncAnimation(
            self.fig,
            self.update_graph,
            init_func=self.init_graph,
            interval=100,
        )

    def add_data(self, data: pd.DataFrame):
        self.data = pd.concat([self.data, data], ignore_index=True)

    def init_graph(self):
        return [self.ask_line, self.bid_line]

    def update_graph(self, frame):
        self.ask_line.set_data(self.data.index, pd.to_numeric(self.data["ask"]))
        self.bid_line.set_data(self.data.index, pd.to_numeric(self.data["bid"]))
        self.ax.relim()
        self.ax.autoscale_view()

        return [self.ask_line, self.bid_line]
