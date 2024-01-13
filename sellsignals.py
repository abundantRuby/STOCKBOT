import yfinance as yf
import pandas as pd
import numpy as np
import scipy.signal
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime

print('Stock screening started')

def download_stock_data(stock_symbol, start_date, end_date):
    try:
        stock_data = yf.download(stock_symbol, start=start_date, end=end_date, progress=False)
        if stock_data.empty:
            raise ValueError(f"No data found for {stock_symbol} between {start_date} and {end_date}")
        return stock_data
    except Exception as e:
        print(f"Error downloading data for {stock_symbol}: {e}")
        return pd.DataFrame()

def calculate_technical_indicators(stock_data):
    stock_data['SMA_50'] = stock_data['Close'].rolling(window=50).mean()
    stock_data['SMA_200'] = stock_data['Close'].rolling(window=200).mean()

    rsi_period = 14
    stock_data['RSI'] = 100 - (100 / (1 + (stock_data['Close'].diff(1).apply(lambda x: max(0, x)) / stock_data['Close'].diff(1).apply(lambda x: abs(min(0, x)))).rolling(window=rsi_period).mean()))

    stock_data['Support_Level'] = stock_data['Low'].rolling(window=50).min()
    stock_data['Resistance_Level'] = stock_data['High'].rolling(window=50).max()

    # Calculate the Stochastic Oscillator
    stoch_period = 14
    stock_data['%K'] = 100 * ((stock_data['Close'] - stock_data['Low'].rolling(window=stoch_period).min()) /
                               (stock_data['High'].rolling(window=stoch_period).max() - stock_data['Low'].rolling(window=stoch_period).min()))
    stock_data['%D'] = stock_data['%K'].rolling(window=3).mean()

    return stock_data

def calculate_sell_signals(stock_data):
    # Use scipy to find peaks in the data
    peaks, _ = scipy.signal.find_peaks(stock_data['Close'], height=stock_data['Close'].quantile(0.95))

    # Check for conditions for sell signals
    sell_signals = (
        (stock_data['SMA_50'] < stock_data['SMA_200']) &
        (stock_data['RSI'] > 70) &
        (stock_data['Close'] < stock_data['Resistance_Level']) &
        (stock_data['%K'] < stock_data['%D']) &
        (stock_data['%K'] > 70) |
        (stock_data.index.isin(peaks))  # additional condition for peaks
    )

    stock_data['Sell_Signal'] = np.where(sell_signals, stock_data['Close'], None)

    return stock_data

def check_stock_analysis(stock_data, stock_symbol):
    global promising_stocks  # Declare the list as global to accumulate across stock symbols
    if not stock_data.empty and len(stock_data) > 0:
        last_row = stock_data.iloc[-1]
        if last_row['Sell_Signal']:
            messages = [
                f"{stock_symbol} is showing sell signals 📉",
                f"{stock_symbol} is indicating potential downward movement ⬇️",
                f"{stock_symbol} is flashing red flags for selling 🚨",
                f"{stock_symbol} might be a good candidate for selling 🛑",
                f"{stock_symbol} is signaling a possible sell-off 📉",
                f"{stock_symbol} is giving sell indications 📉",
                f"{stock_symbol} is on the radar for potential selling opportunities 📉",
                f"{stock_symbol} is showing signs of a downturn 📉",
            ]
            promising_stocks.append(stock_symbol)
            print(np.random.choice(messages))

def send_email(promising_stocks):
    sender_email = "iamdylanhoag@gmail.com"
    receiver_emails = ["dysco712@gmail.com", "iamdylanhoag@gmail.com"]
    password = "hwys aypg refe luea"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = ", ".join(receiver_emails)
    msg['Subject'] = "Sell Signals"

    body = "We have found some sell signals from multiple portfolios:\n\n"
    body += "\n".join(promising_stocks)
    body += "\n\nBest regards,\nYour Trading Bot"

    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_emails, msg.as_string())

if __name__ == "__main__":
    promising_stocks = []  # Initialize the list to store promising stocks
    stock_symbols = ["APLS", "BROS", "ENPH", "NEE", "ON", "RIVN", "ALLY", "GOLD", "F", "GSK", "PLNT", "PAVE", "HLN", "IRBO", "O", "DAL", "BWA", "YUMC", "AON", "HUM", "SJM", "BMY", "FLO"]

    # ... (rest of your stock symbol list)

    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    current_datetime = datetime.datetime.strptime(current_date, "%Y-%m-%d")
    next_day_datetime = current_datetime + datetime.timedelta(days=1)
    next_day_date = next_day_datetime.strftime("%Y-%m-%d")

    start_date = "2022-01-11"  # YYYY-MM-DD
    end_date = next_day_date

    for stock_symbol in stock_symbols:
        stock_data = download_stock_data(stock_symbol, start_date, end_date)

        if not stock_data.empty and len(stock_data) > 0:
            stock_data = calculate_technical_indicators(stock_data)
            stock_data = calculate_sell_signals(stock_data)
            check_stock_analysis(stock_data, stock_symbol)

    if promising_stocks:
        send_email(promising_stocks)
        print('Stock screening finished; email sent')
    else:
        print('Stock screening finished; no results found and no email sent')










