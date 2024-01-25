from datetime import datetime
import queue
import time
import pandas as pd
import requests

class RatePublisher:
    def __init__(self, config):
        self.q = queue.Queue()
        self.get_kline_service = GetKlineService()
        self.config = config
        self.run()
    
    def run(self):
        while True:
            rate = self.get_rate()
            self.publish(rate)
            time.sleep(60)

    def publish(self, rate):
        self.q.put(rate)
    
    def get_rate(self):
        current_date = datetime.now().strftime("%Y%m%d")
        rate_df = self.get_kline_service.get_1day_Kline(
            self.config["symbol"], "ASK", "1min", current_date
        )
        
        return rate_df["close"].tail(self.config["window_size"])



class GetKlineService:
    __API_END_POINT = "https://forex-api.coin.z.com/public"

    def get_1day_Kline(
        self, symbol: str, priceType: str, interval: str, date: str
    ) -> pd.DataFrame:
        url = self.__API_END_POINT + "/v1/klines"
        params = {
            "symbol": symbol,
            "priceType": priceType,
            "interval": interval,
            "date": date,
        }
        response = requests.get(url, params=params)

        if response.status_code != 200:
            raise Exception("APIのレスポンスが200以外です")
        kline_data = response.json()["data"]
        df_kline = self.__convert_Kline_to_dataframe(kline_data)
        return df_kline

    # [{'openTime': '1698616800000', 'open': '149.641', 'high': '149.685', 'low': '149.641', 'close': '149.673'}]
    # という形式の引数データをpandasのDataFrameに変換する
    # 文字列は数値に変換する
    @staticmethod
    def __convert_Kline_to_dataframe(data: list):
        # 文字列を数値に変換
        for row in data:
            row["openTime"] = int(row["openTime"])
            row["open"] = float(row["open"])
            row["high"] = float(row["high"])
            row["low"] = float(row["low"])
            row["close"] = float(row["close"])

        df = pd.DataFrame(data)
        return df
    