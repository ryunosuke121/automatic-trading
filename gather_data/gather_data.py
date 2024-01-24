import requests
import pandas as pd


# データ収集を行うクラス
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


class GatherDataService:
    def __init__(self):
        self.getKlineService = GetKlineService()

    def gather_1month_Kline(
        self, export_path: str, symbol: str, priceType: str, interval: str, date: str
    ):
        df_kline = self.get_1month_Kline(symbol, priceType, interval, date)
        df_kline.to_csv(export_path, index=False)

    def get_1month_Kline(
        self, symbol: str, priceType: str, interval: str, date: str
    ) -> pd.DataFrame:
        df_kline = pd.DataFrame()
        for i in range(0, 31):
            try:
                df_1day_kline = self.getKlineService.get_1day_Kline(
                    symbol, priceType, interval, date
                )
            except Exception as e:
                print(i, e)
                continue
            df_kline = pd.concat([df_kline, df_1day_kline])  # type: ignore
            date = self.__increment_date(date)
        return df_kline

    @staticmethod
    def __increment_date(date: str) -> str:
        year = int(date[0:4])
        month = int(date[4:6])
        day = int(date[6:8])
        if day == 31:
            day = 1
            if month == 12:
                month = 1
                year += 1
            else:
                month += 1
        else:
            day += 1
        return f"{year}{month:02}{day:02}"


if __name__ == "__main__":
    gatherDataService = GatherDataService()
    gatherDataService.gather_1month_Kline(
        "data/USD_JPY_1day_2024_1.csv",
        "USD_JPY",
        "ASK",
        "1min",
        "20240101",
    )
