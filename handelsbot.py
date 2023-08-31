from datetime import date
import yfinance as yf
import constants

today = date.today()
# Konvertera dagens datum till en sträng i formatet 'YYYY-MM-DD'
today_str = today.strftime('%Y-%m-%d')

# Ladda data för en aktie (till exempel Apple)
ticker = "AAPL"
stock_data = yf.Ticker(ticker)

# Hämta historisk data
historical_data = stock_data.history(period="1d", start="2020-01-01", end=today_str)

# Skriv ut data
print(historical_data)
print(constants.CLOSE)  # Skriver ut 'Close'