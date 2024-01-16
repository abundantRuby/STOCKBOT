import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def download_stock_data(symbol, start_date, end_date):
    stock_data = yf.download(symbol, start=start_date, end=end_date, progress=False)
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
                stock_data['%K'].iloc[i] < 34
            ) or (
                stock_data['RSI'].iloc[i] < 28 and
                stock_data['SMA_50'].iloc[i] < stock_data['SMA_200'].iloc[i] and
                stock_data['%K'].iloc[i] < 32
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
        (stock_data['RSI'] > 68) &
        (stock_data['Close'] < stock_data['Resistance_Level']) &
        (stock_data['%K'] < stock_data['%D']) &
        (stock_data['%K'] > 68)
    )
    sell_condition_2 = (
        (stock_data['RSI'] > 75) &
        (stock_data['SMA_50'] > stock_data['SMA_200']) &
        (stock_data['%K'] > 75)
    )
    sell_condition_3 = (
        (stock_data['RSI'] > 82)
    )

    for i in range(len(stock_data)):
        if sell_condition_1.iloc[i] or sell_condition_2.iloc[i] or sell_condition_3.iloc[i]:
            sell_signals.append(i)

    return sell_signals

def calculate_roi(stock_symbol, buy_signals, sell_signals):
    start_date = datetime(2021, 1, 1)
    end_date = datetime.now()
    
    # Download stock data for the specified symbol
    stock_data = download_stock_data(stock_symbol, start_date, end_date)

    rois = []
    time_diffs = []

    for buy_signal in buy_signals:
        # Find the next sell signal after the buy signal
        sell_signal = next((sell for sell in sell_signals if sell > buy_signal), None)

        if sell_signal is not None:
            buy_price = stock_data['Close'].iloc[buy_signal]
            sell_price = stock_data['Close'].iloc[sell_signal]
            roi = ((sell_price - buy_price) / buy_price) * 100
            rois.append(roi)

            buy_date = stock_data.index[buy_signal]
            sell_date = stock_data.index[sell_signal]
            time_diff = sell_date - buy_date
            time_diffs.append(time_diff)

    return rois, time_diffs

def calculate_average_roi_for_stocks(stock_symbols):
    total_rois = []
    total_time_diffs = []

    for stock_symbol in stock_symbols:
        stock_symbol = stock_symbol.upper()

        start_date = datetime(2021, 1, 1)
        end_date = datetime.now()

        stock_data = download_stock_data(stock_symbol, start_date, end_date)
        stock_data = calculate_technical_indicators(stock_data)

        buy_signals = generate_buy_signals(stock_data)
        sell_signals = generate_sell_signals(stock_data)
        rois, time_diffs = calculate_roi(stock_symbol, buy_signals, sell_signals)

        if rois:
            average_roi = sum(rois) / len(rois)
            total_rois.append(average_roi)

            total_time_diffs.extend(time_diffs)

    if total_rois:
        overall_average_roi = sum(total_rois) / len(total_rois)

        # Calculate overall average time difference in seconds
        overall_average_time_diff_seconds = sum(td.total_seconds() for td in total_time_diffs) / len(total_time_diffs)

        # Convert the overall average time difference back to timedelta
        overall_average_time_diff = timedelta(seconds=overall_average_time_diff_seconds)

        # Format the timedelta to show only days, hours, and minutes
        formatted_time_diff = str(overall_average_time_diff).split('.')[0]

        print(f"Overall Average ROI for {len(stock_symbols)} stocks: {overall_average_roi:.2f}%")
        print(f"Overall Average Time Between Buy and Sell Signals: {formatted_time_diff}")
    else:
        print("No buy or sell signals found for any stock.")

stock_symbols_list = ['NEE', 'SO', 'DUK', 'NGG', 'SRE', 'PCG', 'AEP', 'D', 'BCE', 'EXC', 'XEL', 'ED', 'PEG', 'CHT', 'EIX', 'TU', 'WEC', 'AWK', 'TEF', 'DTE', 'FE', 'ETR', 'EBR', 'FTS', 'PPL', 'ES', 'AEE', 'CNP', 'ATO', 'VIV', 'CMS']
calculate_average_roi_for_stocks(stock_symbols_list)






















 















    



