import yfinance as yf
import pandas as pd
from datetime import datetime


def get_nikkei_data():
    # 日経平均株価のティッカーシンボルは '^N225'
    nikkei_ticker = '^N225'

    # データを取得
    nikkei_data = yf.download(nikkei_ticker, period='1d', interval='1m')

    # 最新の株価情報を取得
    latest_data = nikkei_data.tail(1)

    return latest_data


def record_data_to_csv(data, filename='nikkei_data.csv'):
    # CSVファイルにデータを追記
    data.to_csv(filename, mode='a', header=not pd.io.common.file_exists(filename))


def main():
    # 日経平均株価を取得
    data = get_nikkei_data()
    print("最新の日経平均株価:")
    print(data)

    # データをCSVに記録
    record_data_to_csv(data)
    print("データがCSVファイルに記録されました。")


if __name__ == '__main__':
    main()
