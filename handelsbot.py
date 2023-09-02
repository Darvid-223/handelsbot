from datetime import date, timedelta
import yfinance as yf
import pandas as pd
import mplfinance as mpf

# Beräkna dagens datum och datumet för 1 år sedan
today = date.today()
one_year_ago = today - timedelta(days=365)
today_str = today.strftime("%Y-%m-%d")
one_year_ago_str = one_year_ago.strftime("%Y-%m-%d")

# Variabler för tidsram och tidsintervall
time_period = "1h"
start_date = one_year_ago_str
end_date = today_str

# Definiera valutaparet vi är intresserade av (i det här fallet USD/EUR)
ticker = "EURUSD=X"

# Hämta data från Yahoo Finance
forex_data = yf.Ticker(ticker)
historical_data = forex_data.history(period=time_period, start=start_date, end=end_date)

# Beräkna RSI
delta = historical_data['Close'].diff(1)
gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
rs = gain / loss
historical_data['RSI'] = 100 - (100 / (1 + rs))

# Beräkna 50-dagars och 200-dagars SMA
historical_data['SMA_50'] = historical_data['Close'].rolling(window=50).mean()
historical_data['SMA_200'] = historical_data['Close'].rolling(window=200).mean()

# Identifiera köp- och säljsignaler
buy_signals = historical_data[(historical_data['SMA_50'] > historical_data['SMA_200']) & (historical_data['SMA_50'].shift(1) <= historical_data['SMA_200'].shift(1))].index
sell_signals = historical_data[(historical_data['SMA_50'] < historical_data['SMA_200']) & (historical_data['SMA_50'].shift(1) >= historical_data['SMA_200'].shift(1))].index

# Köp- och säljsignalerna som datapunkter
buy_dict = dict()
sell_dict = dict()
for buy in buy_signals:
    buy_dict[buy] = historical_data['Close'].loc[buy]
for sell in sell_signals:
    sell_dict[sell] = historical_data['Close'].loc[sell]

# Konvertera dictionaries till Pandas Series
buy_series = pd.Series(buy_dict)
sell_series = pd.Series(sell_dict)

# Förbereder köp- och säljsignaler för plotting
aplots = [
    mpf.make_addplot(buy_series, type='scatter', markersize=100, marker='^', panel=0, color='g'),
    mpf.make_addplot(sell_series, type='scatter', markersize=100, marker='v', panel=0, color='r'),
    mpf.make_addplot(historical_data['SMA_50'], panel=0, color='c', secondary_y=False),
    mpf.make_addplot(historical_data['SMA_200'], panel=0, color='m', secondary_y=False),
    mpf.make_addplot(historical_data['RSI'], panel=1, color='b', secondary_y=True)
]
print(historical_data.head())
print(buy_series.head())
print(sell_series.head())

# Plotta candlestick-grafen
mpf.plot(historical_data, 
         type='candle', 
         style='charles', 
         title='EURUSD=X Candlestick', 
         ylabel='Price', 
         ylabel_lower='Volume', 
         volume=True, 
         figscale=1.5, # Justerar storleken på figuren
         mav=(50, 200),
         addplot=aplots,
         panel_ratios=(1,0.25))  # Använder två paneler, huvudpanelen är 4 gånger större än RSI-panelen

