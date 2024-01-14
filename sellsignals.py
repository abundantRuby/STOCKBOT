import yfinance as yf
import pandas as pd
import talib
import numpy as np
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime

print('Stock Screening for Sell Signals Started')

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
    stock_data['RSI'] = talib.RSI(stock_data['Close'], timeperiod=rsi_period)

    stock_data['Support_Level'] = stock_data['Low'].rolling(window=50).min()
    stock_data['Resistance_Level'] = stock_data['High'].rolling(window=50).max()

    # Calculate the Stochastic Oscillator
    stoch_period = 14
    stock_data['%K'] = 100 * ((stock_data['Close'] - stock_data['Low'].rolling(window=stoch_period).min()) /
                              (stock_data['High'].rolling(window=stoch_period).max() -
                               stock_data['Low'].rolling(window=stoch_period).min()))

    stock_data['%D'] = stock_data['%K'].rolling(window=3).mean()

    return stock_data

def check_sell_signals(stock_data):
    sell_signals = (
        (stock_data['SMA_50'] < stock_data['SMA_200']) &
        (stock_data['RSI'] > 68) &
        (stock_data['Close'] < stock_data['Resistance_Level']) &
        (stock_data['%K'] < stock_data['%D']) &
        (stock_data['%K'] > 68)
    ) | (
        (stock_data['RSI'] > 75) &
        (stock_data['SMA_50'] > stock_data['SMA_200']) &
        (stock_data['%K'] > 75)  # other conditions
    ) | (
        (stock_data['RSI'] > 82)
    )

    stock_data['Sell_Signal'] = np.where(sell_signals, stock_data['Close'], None)

    return stock_data

def check_stock_analysis(stock_data, stock_symbol, sell_signals, stock_messages):
    if not stock_data.empty and len(stock_data) > 0:
        last_row = stock_data.iloc[-1]
        if sell_signals.iloc[-1]:
            messages = [
                f"{stock_symbol} is showing sell signals 📉",
                f"{stock_symbol} might be showing an exit opportunity 🚪",
                f"{stock_symbol} is signaling a potential downturn ⬇️",
                f"{stock_symbol} is waving a red flag 🚩",
                f"{stock_symbol} is displaying sell indicators ⚠️",
                f"{stock_symbol} is on a sell trajectory 🔻",
                f"{stock_symbol} is on the sellers' radar 🚨",
                f"{stock_symbol} is in a bearish route 🐻",
                f"{stock_symbol} is suggesting a sell opportunity 📉",
                f"{stock_symbol} is signaling a bearish trend 🐾",
                f"{stock_symbol} is in the sell zone 📊",
                f"{stock_symbol} is on the sellers' watchlist 🚨",
            ]
            random_message = np.random.choice(messages)
            stock_messages.append(f"{random_message}")

def send_email(stock_messages):
    sender_email = "iamdylanhoag@gmail.com"  # Replace with your email
    receiver_email = "dysco712@gmail.com"  # Replace with recipient's email
    password = "hwys aypg refe luea"  # Replace with your email password

    current_datetime = datetime.datetime.now()
    day_of_week = current_datetime.strftime("%A")

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = f"{day_of_week} Sell Signals"

    # Combine stock symbols and random messages in the email body
    body = "Here are the stocks with sell signals today!\n\n"
    body += "\n".join(stock_messages)
    body += "\n\nBest regards,\nYour Trading Bot"

    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())

def is_weekend():
    today = datetime.date.today()
    return today.weekday() in [5, 6]  # 5 is Saturday, 6 is Sunday

if __name__ == "__main__":
    stock_symbols = ["DAL", "RIVN", "BWA", "ENPH", "F", "ALLY", "ON", "BROS", "O", "IRBO", "HLN", "PAVE", "PLNT", "NEE", "GSK", "GOLD", "HUM", "AON", "YUMC", "RIO", "BMY", "FLO", "SJM"]  # Replace with your stock symbols

    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    current_datetime = datetime.datetime.strptime(current_date, "%Y-%m-%d")
    next_day_datetime = current_datetime + datetime.timedelta(days=1)
    next_day_date = next_day_datetime.strftime("%Y-%m-%d")

    start_date = "2022-01-11"  # Replace with your desired start date
    end_date = next_day_date

    stock_messages = []  # Create a list to store formatted stock messages

    for stock_symbol in stock_symbols:
        stock_data = download_stock_data(stock_symbol, start_date, end_date)

        if not stock_data.empty and len(stock_data) > 0:
            stock_data = calculate_technical_indicators(stock_data)
            stock_data = check_sell_signals(stock_data)
            check_stock_analysis(stock_data, stock_symbol, stock_data['Sell_Signal'].notnull(), stock_messages)

    if stock_messages:
        send_email(stock_messages)
        print('Sell Signals Detected. Email Sent')
    else:
        print('No Sell Signals Found; No Email Sent')
        if is_weekend():
            print("It's the weekend. Market might be closed.")










