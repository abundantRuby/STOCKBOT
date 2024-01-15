import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
import random

print('Sell Signal Screening Started')

def download_stock_data(symbol, start_date, end_date):
    stock_data = yf.download(symbol, start=start_date, end=end_date, progress=False)
    return stock_data

def generate_sell_signals(stock_data):
    sell_signals = []

    for i in range(len(stock_data)):
        if (
            (
                stock_data['SMA_50'].iloc[i] < stock_data['SMA_200'].iloc[i] and
                stock_data['RSI'].iloc[i] > 73 and
                stock_data['Close'].iloc[i] < stock_data['Resistance_Level'].iloc[i] and
                stock_data['%K'].iloc[i] < stock_data['%D'].iloc[i] and
                stock_data['%K'].iloc[i] > 73
            ) or (
                stock_data['RSI'].iloc[i] > 76 and
                stock_data['SMA_50'].iloc[i] > stock_data['SMA_200'].iloc[i] and
                stock_data['%K'].iloc[i] > 76
            ) or (
                stock_data['RSI'].iloc[i] > 82
            )
        ):
            sell_signals.append(i)

    return sell_signals

def calculate_technical_indicators(stock_data):
    # Calculate Simple Moving Averages (SMA_50, SMA_200)
    stock_data['SMA_50'] = stock_data['Close'].rolling(window=50).mean()
    stock_data['SMA_200'] = stock_data['Close'].rolling(window=200).mean()

    # Calculate Relative Strength Index (RSI)
    delta = stock_data['Close'].diff(1)
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()

    rs = avg_gain / avg_loss
    stock_data['RSI'] = 100 - (100 / (1 + rs))

    # Calculate Support and Resistance Levels (for illustration purposes)
    stock_data['Support_Level'] = stock_data['Low'].rolling(window=30).min()
    stock_data['Resistance_Level'] = stock_data['High'].rolling(window=30).max()

    # Calculate Stochastic Oscillator (%K, %D)
    stock_data['%K'] = ((stock_data['Close'] - stock_data['Low'].rolling(window=14).min()) /
                        (stock_data['High'].rolling(window=14).max() - stock_data['Low'].rolling(window=14).min())) * 100
    stock_data['%D'] = stock_data['%K'].rolling(window=3).mean()

    return stock_data

def check_sell_signals(stocks, start_date, end_date):
    sell_list = []

    for stock_symbol in stocks:
        stock_data = download_stock_data(stock_symbol, start_date, end_date)
        stock_data = calculate_technical_indicators(stock_data)
        sell_signals = generate_sell_signals(stock_data)

        if sell_signals:
            # Check if there was a sell signal in the past day
            last_sell_signal_date = stock_data.index[sell_signals[-1]]
            today = datetime.now().date()
            if (today - last_sell_signal_date.date()).days <= 2:
                sell_list.append((stock_symbol, get_random_message()))

    return sell_list

def get_random_message():
    messages = [
        "is showing sell signals 📉",
        "might be showing an exit opportunity 🚪",
        "is signaling a potential downturn ⬇️",
        "is waving a red flag 🚩",
        "is displaying sell indicators ⚠️",
        "is on a sell trajectory 🔻",
        "is on the sellers' radar 🚨",
        "is in a bearish route 🐻",
        "is suggesting a sell opportunity 📉",
        "is signaling a bearish trend 🐾",
        "is in the sell zone 📊",
        "is on the sellers' watchlist 🚨"
    ]
    return random.choice(messages)

def send_email(sell_list):
    # Replace 'your_email@gmail.com' and 'your_password' with your Gmail credentials
    from_email = 'iamdylanhoag@gmail.com'
    password = 'hwys aypg refe luea'

    current_date = datetime.now()
    current_day_name = current_date.strftime('%A')

    subject = f'{current_day_name} Sell Signals!'
    body = f"Here are stocks with a sell signal in the past day:\n\n"
    
    for stock_symbol, message in sell_list:
        body += f"{stock_symbol} {message}\n"

    body += "\nBest regards,\nYour Trading Bot"

    to_email = 'dysco712@gmail.com'  # Replace with the recipient's email address

    message = MIMEText(body)
    message['Subject'] = subject
    message['From'] = from_email
    message['To'] = to_email

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(from_email, password)
            server.sendmail(from_email, to_email, message.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email. Error: {e}")

def main():
    # Customize the list of stock symbols
    stock_symbols = ["DAL", "RIVN", "BWA", "ENPH", "F", "ALLY", "ON", "BROS", "O", "IRBO", "HLN", "PAVE", "PLNT", "NEE", "GSK", "GOLD", "HUM", "AON", "YUMC", "RIO", "BMY", "FLO", "SJM"]

    start_date = datetime(2022, 1, 1)
    end_date = datetime.now()

    sell_list = check_sell_signals(stock_symbols, start_date, end_date)

    if sell_list:
        send_email(sell_list)
    else:
        print("No stocks with sell signals in the past day.")

if __name__ == "__main__":
    main()

#STOCKBOT. Made by Dylan Hoag










