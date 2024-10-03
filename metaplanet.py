import yfinance as yf
import ccxt
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# APIの指定
def get_stock_data(ticker, start_date, end_date):
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    stock_data['Return'] = stock_data['Adj Close'].pct_change()
    return stock_data

def get_crypto_data(symbol, timeframe, since):
    exchange = ccxt.binance()  # Binanceを例に使用
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since=since)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    df['Return'] = df['close'].pct_change()
    return df

# 日付指定
end_date = datetime.now()
start_date = end_date - timedelta(days=180)  # 半年分

# 株価データをYfinanceから取得
stock_ticker = '3350.T'  # レオン自動機のティッカーシンボル
stock_data = get_stock_data(stock_ticker, start_date, end_date)

# ビットコインデーターの取得
crypto_symbol = 'BTC/USDT'  # ビットコイン対米ドル
since = int(start_date.timestamp() * 1000)
crypto_data = get_crypto_data(crypto_symbol, '1d', since)

# グラフ化
combined_df = stock_data[['Return']].join(crypto_data[['Return']], how='inner', lsuffix='_stock', rsuffix='_crypto')
combined_df.dropna(inplace=True)

# 増加率の比率計算
combined_df['Ratio'] = combined_df['Return_stock'] / combined_df['Return_crypto']

# グラフ作成
plt.figure(figsize=(14, 7))
plt.plot(combined_df.index, combined_df['Ratio'], label='Stock/Bitcoin Return Ratio', color='b')
plt.xlabel('Date')
plt.ylabel('Ratio')
plt.title('Meta planet Inc Stock Return / Bitcoin Return Ratio')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
