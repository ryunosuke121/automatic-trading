from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import websocket
import json
import time
import animate as animate
import threading


class GatherDataWebSocketService:
    __WS_END_POINT = "wss://forex-api.coin.z.com/ws/public/v1"

    def __init__(self, visualizer: animate.RealtimeFXVisualizer):
        self.visualizer = visualizer
        websocket.enableTrace(True)
        self.ws = None
        self.df_rate = pd.DataFrame(
            columns=["ask", "bid", "timestamp", "symbol", "status"]
        )
        self.connect()

    def connect(self):
        self.ws = websocket.WebSocketApp(  # type: ignore
            self.__WS_END_POINT,
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
        )

    def on_open(self, ws):
        message = {"command": "subscribe", "channel": "ticker", "symbol": "USD_JPY"}
        ws.send(json.dumps(message))

    def on_message(self, ws, message):
        if message == "":
            return
        data = json.loads(message)
        df_temp_row = pd.DataFrame([data])
        self.df_rate = pd.concat([self.df_rate, df_temp_row])
        self.visualizer.add_data(df_temp_row)

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws, close_status_code, close_msg):
        print("### closed ###")
        self.df_rate.to_csv("./data/realtime_rate.csv", index=False)

    def reconnect(self):
        print("Attempting to reconnect...")
        time.sleep(5)  # 5秒待機
        self.connect()
        self.ws.run_forever()  # type: ignore

    def run(self):
        try:
            self.ws.run_forever()  # type: ignore
        except KeyboardInterrupt:
            if self.ws:
                self.ws.close()


if __name__ == "__main__":
    try:
        visualizer = animate.RealtimeFXVisualizer()
        gatherDataWebSocketService = GatherDataWebSocketService(visualizer)
        thread = threading.Thread(target=gatherDataWebSocketService.run)
        thread.start()
        plt.show()
    except KeyboardInterrupt:
        if gatherDataWebSocketService.ws:
            gatherDataWebSocketService.ws.close()
