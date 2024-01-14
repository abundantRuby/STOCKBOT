import yfinance as yf
import pandas as pd
import talib
import matplotlib.pyplot as plt
import numpy as np

def download_stock_data(stock_symbol, start_date, end_date):
    stock_data = yf.download(stock_symbol, start=start_date, end=end_date)
    return stock_data

def calculate_technical_indicators(stock_data):
    stock_data['SMA_50'] = stock_data['Close'].rolling(window=50).mean()
    stock_data['SMA_200'] = stock_data['Close'].rolling(window=200).mean()
    
    rsi_period = 14
    stock_data['RSI'] = talib.RSI(stock_data['Close'], timeperiod=rsi_period)
    
    stock_data['Support_Level'] = stock_data['Low'].rolling(window=50).min()
    stock_data['Resistance_Level'] = stock_data['High'].rolling(window=50).max()

    stoch_period = 14
    stock_data['%K'] = 100 * ((stock_data['Close'] - stock_data['Low'].rolling(window=stoch_period).min()) / 
                            (stock_data['High'].rolling(window=stoch_period).max() - stock_data['Low'].rolling(window=stoch_period).min()))
    
    stock_data['%D'] = stock_data['%K'].rolling(window=3).mean()
    
    return stock_data

def calculate_beta(end_date, start_date, stock_symbol):
    benchmark = '^GSPC'  # S&P 500 benchmark
    stock_data = yf.download([stock_symbol, benchmark], start=start_date, end=end_date)['Adj Close']
    returns = stock_data.pct_change().dropna()

    cov_matrix = returns.cov()
    beta = cov_matrix[stock_symbol][benchmark] / cov_matrix[benchmark][benchmark]
    return beta

def calculate_buy_signals(stock_data):
    buy_signal = []

    for i in range(1, len(stock_data)):
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
            buy_signal.append(stock_data['Close'].iloc[i])
        else:
            buy_signal.append(None)
    
    buy_signal = [None] + buy_signal

    stock_data['Buy_Signal'] = buy_signal
    return stock_data

def calculate_sell_signals(stock_data):
    sell_signal = []

    for i in range(1, len(stock_data)):
        if (
            (
                stock_data['SMA_50'].iloc[i] < stock_data['SMA_200'].iloc[i] and
                stock_data['RSI'].iloc[i] > 68 and
                stock_data['Close'].iloc[i] < stock_data['Resistance_Level'].iloc[i] and
                stock_data['%K'].iloc[i] < stock_data['%D'].iloc[i] and
                stock_data['%K'].iloc[i] > 68
            ) or (
                stock_data['RSI'].iloc[i] > 75 and
                stock_data['SMA_50'].iloc[i] > stock_data['SMA_200'].iloc[i] and
                stock_data['%K'].iloc[i] > 75
            ) or (
                stock_data['RSI'].iloc[i] > 82
            )
        ):
            sell_signal.append(stock_data['Close'].iloc[i])
        else:
            sell_signal.append(None)

    sell_signal = [None] + sell_signal

    stock_data['Sell_Signal'] = sell_signal
    return stock_data

def calculate_volatility(stock_data):
    stock_data['Daily_Return'] = stock_data['Close'].pct_change()
    volatility = stock_data['Daily_Return'].std() * (252 ** 0.5)  # 252 trading days in a year
    return volatility

def plot_stock_analysis(stock_data, stock_symbol):
    plt.style.use('dark_background')

    fig = plt.figure(figsize=(12, 10))

    ax1 = plt.subplot(3, 1, 1)
    ax1.plot(stock_data.index, stock_data['Close'], label='Close Price', color='cyan')
    ax1.plot(stock_data.index, stock_data['SMA_50'], label='50-Day SMA', color='orange')
    ax1.plot(stock_data.index, stock_data['SMA_200'], label='200-Day SMA', color='red')
    ax1.scatter(stock_data[stock_data['Buy_Signal'].notnull()].index,
                stock_data[stock_data['Buy_Signal'].notnull()]['Buy_Signal'],
                marker='^', color='yellow', label='Buy Signal', alpha=1)
    ax1.scatter(stock_data[stock_data['Sell_Signal'].notnull()].index,
                stock_data[stock_data['Sell_Signal'].notnull()]['Sell_Signal'],
                marker='v', color='red', label='Sell Signal', alpha=1)
    ax1.set_title(f"{stock_symbol} Stock Analysis")
    ax1.set_ylabel("Price")
    ax1.legend()

    ax2 = plt.subplot(3, 1, 2, sharex=ax1)
    ax2.plot(stock_data.index, stock_data['RSI'], label='RSI', color='purple')
    ax2.axhline(y=70, color='red', linestyle='--', label='Overbought (70)')
    ax2.axhline(y=28, color='green', linestyle='--', label='Oversold (28)')
    ax2.plot(stock_data.index, stock_data['Support_Level'], label='Support Level', color='green')
    ax2.plot(stock_data.index, stock_data['Resistance_Level'], label='Resistance Level', color='red')
    ax2.set_title("Technical Indicator Stuff")
    ax2.set_xlabel("Date")
    ax2.set_ylabel("Values")
    ax2.legend()

    beta = calculate_beta(stock_data.index[-1].strftime('%Y-%m-%d'), stock_data.index[0].strftime('%Y-%m-%d'), stock_symbol)
    plt.figtext(0.1, 0.97, f"Beta: {beta:.2f}", fontsize=12, color='white')
    if beta > 1.4:
        plt.figtext(0.1, 0.95, "Warning: High Beta", fontsize=12, color='red')

    volatility = calculate_volatility(stock_data)
    if volatility > 0.4:
        plt.figtext(0.1, 0.93, f"Warning: High Volatility ({volatility:.2%})", fontsize=12, color='red')
    
    warning_message = ""
    if volatility > 0.4 and beta > 1.4:
        warning_message = "Warning: Bot is HIGHLY inaccurate (especially sell signals)"
    elif volatility > 0.4 or beta > 1.4:
        warning_message = "Warning: Bot may be inaccurate"
    if warning_message:
        plt.figtext(0.1, 0.91, warning_message, fontsize=12, color='red')

    ax3 = plt.subplot(3, 1, 3, sharex=ax1)
    ax3.plot(stock_data.index, stock_data['Volume'], label='Volume', color='cyan')
    ax3.set_title("Trading Volume")
    ax3.set_xlabel("Date")
    ax3.set_ylabel("Volume")
    ax3.legend()

    plt.show()

if __name__ == "__main__":
    stock_symbol = "plnt"
    stock_symbol = stock_symbol.upper()
    start_date = "2020-1-19"
    end_date = "2024-1-13"
    stock_data = download_stock_data(stock_symbol, start_date, end_date)
    stock_data = calculate_technical_indicators(stock_data)
    stock_data = calculate_buy_signals(stock_data)
    stock_data = calculate_sell_signals(stock_data)
    plot_stock_analysis(stock_data, stock_symbol)

#STOCKBOT. Made by Dylan Hoag
