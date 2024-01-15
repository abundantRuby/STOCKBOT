import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def download_stock_data(symbol, start_date, end_date):
    stock_data = yf.download(symbol, start=start_date, end=end_date)
    return stock_data

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

def generate_buy_signals(stock_data):
    buy_signals = []

    for i in range(len(stock_data)):
        if (
            (
                stock_data['SMA_50'].iloc[i] > stock_data['SMA_200'].iloc[i] and
                stock_data['RSI'].iloc[i] < 32 and
                stock_data['Close'].iloc[i] > stock_data['Support_Level'].iloc[i] and
                stock_data['%K'].iloc[i] > stock_data['%D'].iloc[i] and
                stock_data['%K'].iloc[i] < 32
            ) or (
                stock_data['RSI'].iloc[i] < 28 and
                stock_data['SMA_50'].iloc[i] < stock_data['SMA_200'].iloc[i] and
                stock_data['%K'].iloc[i] < 28
            ) or (
                stock_data['RSI'].iloc[i] < 24
            )
        ):
            buy_signals.append(i)

    return buy_signals

def generate_sell_signals(stock_data):
    sell_signals = []

    sell_condition_1 = (
        (stock_data['SMA_50'] < stock_data['SMA_200']) &
        (stock_data['RSI'] > 73) &
        (stock_data['Close'] < stock_data['Resistance_Level']) &
        (stock_data['%K'] < stock_data['%D']) &
        (stock_data['%K'] > 73)
    )
    sell_condition_2 = (
        (stock_data['RSI'] > 76) &
        (stock_data['SMA_50'] > stock_data['SMA_200']) &
        (stock_data['%K'] > 76)
    )
    sell_condition_3 = (
        (stock_data['RSI'] > 82)
    )

    for i in range(len(stock_data)):
        if sell_condition_1.iloc[i] or sell_condition_2.iloc[i] or sell_condition_3.iloc[i]:
            sell_signals.append(i)

    return sell_signals

def plot_stock_with_signals(stock_data, buy_signals, sell_signals, stock_symbol):
    # Dark theme
    plt.style.use('dark_background')

    # Create a single figure with subplots
    fig, axs = plt.subplots(3, 1, figsize=(12, 12), sharex=True)

    # Plot stock prices with buy and sell signals
    axs[0].plot(stock_data['Close'], label='Stock Price', color='cyan')
    axs[0].plot(stock_data['SMA_50'], label='50-day SMA', color='orange')
    axs[0].plot(stock_data['SMA_200'], label='200-day SMA', color='red')
    for buy_signal in buy_signals:
        axs[0].scatter(stock_data.index[buy_signal], stock_data['Close'].iloc[buy_signal], color='green', marker='^', s=60)
    for sell_signal in sell_signals:
        axs[0].scatter(stock_data.index[sell_signal], stock_data['Close'].iloc[sell_signal], color='red', marker='v', s=60)
    axs[0].set_ylabel("Stock Price")
    axs[0].legend()
    axs[0].set_title(f"{stock_symbol} Stock Analysis")

    # Plot technical indicators
    axs[1].plot(stock_data['RSI'], label='RSI', color='purple')
    axs[1].axhline(70, color='red', linestyle='--', label='Overbought (70)')
    axs[1].axhline(30, color='green', linestyle='--', label='Oversold (30)')
    axs[1].plot(stock_data['Support_Level'], label='Support Level', color='green', linestyle='--')
    axs[1].plot(stock_data['Resistance_Level'], label='Resistance Level', color='red', linestyle='--')
    axs[1].set_ylabel("Value")
    axs[1].legend()
    axs[1].set_title("Technical Indicators")

    # Plot stock volume as a continuous line
    axs[2].plot(stock_data['Volume'], label='Volume', color='cyan')
    axs[2].set_xlabel("Date")
    axs[2].set_ylabel("Volume")
    axs[2].set_title("Stock Volume")

    # Show the plot
    plt.show()

def main():
    # Customize the stock symbol
    stock_symbol = 'gsk'
    stock_symbol = stock_symbol.upper()

    start_date = datetime(2021, 1, 1)
    end_date = datetime.now()

    stock_data = download_stock_data(stock_symbol, start_date, end_date)
    stock_data = calculate_technical_indicators(stock_data)

    buy_signals = generate_buy_signals(stock_data)
    sell_signals = generate_sell_signals(stock_data)

    if buy_signals or sell_signals:
        plot_stock_with_signals(stock_data, buy_signals, sell_signals, stock_symbol)
    else:
        print(f"No buy or sell signals found for {stock_symbol}")

if __name__ == "__main__":
    main()

#STOCKBOT. Made by Dylan Hoag
