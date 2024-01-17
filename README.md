# STOCKBOT

Hey There 👋

STOCKBOT is a comprehensive tool developed in python featuring three primary components: Buy Signals, Sell Signals, and the Individual Stock Screener.

This repository contains in-depth documentation about STOCKBOT, providing insights into each of the main programs. Additionally, you'll find SP500 backtesting results derived from over 44,400 data points since 2019.

Happy reading!

## Guide

- [1: Buy Signals](#buy-signals)
- [2: Sell Signals](#sell-signals)
- [3: Individual Screener](#individual-screener)
- [Testing and Data](#testing-and-data)
- [Other](#other)


## Buy Signals

Buysignals.py Overview:

This program is the engine driving the buy signals behind STOCKBOT. This program leverages external libraries such as [TA-lib](https://ta-lib.org/) to perform complex technical analysis on stock data. 

Using a combination of moving averages, RSI, support and resistance levels, and stochastic oscillators, this program precisely identifies optimal entry points for stock investments.

It performs these calculations across a large list of stocks, and then proceeds to send an email containing all the signals to the user.

To send the emails, STOCKBOT securely connects to the Gmail SMTP server by utilizing a remote access code, which allows it to send authorized emails.

```python
def send_email(stock_messages):
    sender_email = "sender@gmail.com"  # Replace with your email
    receiver_email = "recipent@gmail.com"  # Replace with recipient's email
    password = "xxxx xxxx xxxx xxxx"  # Replace with your remote access code

    current_datetime = datetime.datetime.now()
    day_of_week = current_datetime.strftime("%A")

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = f"{day_of_week} Sell Signals"

    # Generates the email body
    body = "Here are the stocks with sell signals today!\n\n"
    body += "\n".join(stock_messages)
    body += "\n\nBest regards,\nYour Trading Bot"

    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
```

To make the emails more interesting, a unique message is randomly generated for each stock:

```python
messages = [
    f"{stock_symbol} is looking goated 🐐",
    f"{stock_symbol} is on fire 🔥",
    f"{stock_symbol} will make some money 💸",
    f"{stock_symbol} is looking bullish 🐂",
    f"{stock_symbol} is surfing the market waves 🌊",
    f"{stock_symbol} is taking off 🚀",
    f"{stock_symbol} is singing a profitable tune 🎶",
    f"{stock_symbol} is dancing with the bulls 💃",
    f"{stock_symbol} is turning heads on Wall Street 👀",
    f"{stock_symbol} is playing the market game like a pro 🎮",
    f"{stock_symbol} is painting the charts green 🖌️💚",
    f"{stock_symbol} is a rising star ✨",
    f"{stock_symbol} is riding the momentum like a boss 🏄‍♂️",
    f"{stock_symbol} is the hidden gem 💎",
    f"{stock_symbol} is painting profits 🎨",
    f"{stock_symbol} is on the rollercoaster of success 🎢",
    f"{stock_symbol} is taking the market by storm 🌪️"
]
```

Furthermore, this program operates on a CRON schedule, ensuring that users receive automated daily emails containing the latest buy signals.

## Sell Signals

SellSignals.py Overview:

This program calculates the sell signals behind STOCKBOT. Leveraging the same technical indicators as buysignals.py, this program identifies optimal points to exit a position in the stock market.

This program also uses the same logic for sending emails, and also integrates custom messages:

```python
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
```

The email structure also is identical for both programs:

![Stock Analysis](https://i.ibb.co/qxHZWRr/Screenshot-2024-01-17-151932.png)


## Individual Screener

Individual-Screener.py Overview:

The Individual Screener is designed for in-depth analysis of individual stocks, and provides a visual representation of the buy and sell signals.

Users can specify a start_date, prompting the bot to generate a graph encompassing the calculations and data from the designated time period.

The screener includes three different graphs:

- Top Graph: Displays stock price alongside moving averages, depicting buy signals (green triangle) and sell signals (red triangle).
- Middle Graph: Illustrates additional technical indicators, including RSI, overbought and oversold levels, as well as support and resistance levels.
- Bottom Graph: Shows stock volume, which currently has no impact on the bot's decision-making. It simply serves as additional information on unused space.

Example 1: AAPL (Apple)
![Stock Analysis](https://i.ibb.co/nCLLvPp/AAPL.png)
Example 2: WM (Waste Management)
![Stock Analysis](https://i.ibb.co/56YZTDj/WM.png)
Example 2: AMZN (Amazon)
![Stock Analysis](https://i.ibb.co/TKr81ry/amzn.png)

## Testing and Data
STOCKBOT is built with the following libraries:

- [yfinance](https://pypi.org/project/yfinance/): Fetches financial data from Yahoo Finance.
- [pandas](https://pandas.pydata.org/): Data manipulation and analysis.
- [TA-lib](https://ta-lib.org/): Technical analysis of financial markets.
- [numpy](https://numpy.org/): Scientific computing with Python.
- [smtplib](https://docs.python.org/3/library/smtplib.html): Sending emails using the Simple Mail Transfer Protocol.
- [datetime](https://docs.python.org/3/library/datetime.html): Allows for manipulating dates and times.

## Other
Made by Dylan Hoag
- **Text:** (208)-989-8541
- **Email:** dysco712@gmail.com

Contact me with your comments ☺

