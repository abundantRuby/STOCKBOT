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

This program is the engine driving the buy signals behind STOCKBOT. Essentially it uses external libraries such as [TA-lib](https://ta-lib.org/) to perform complex technical analysis on stock data. 

Through a combination of moving averages, RSI, support and resistance levels, and stochastic oscillators, it pinpoints optimal entry points to invest in a stock.

It performs these calculations for a large list of stocks, and then sends an email to the user with all of the buy signals.

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

Additionally, this program is set up on a CRON schedule, so the user gets automated daily emails about buy signals.

If you keep reading, you will learn about individual-screener.py, which was built to visualize the buy and sell signals on a graph, to visually see how buysignals.py works.

## Sell Signals

SellSignals.py Overview:

This program calculates the sell signals behind STOCKBOT. Leveraging the same technical indicators as buysignals.py, this program identifies optimal points to exit a position in the stock market.

This program also uses the same logic for sending emails, and also includes custom messages:

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

The Individual Screener is designed for in-depth analysis of individual stocks, and it helps to visualize the buy and sell signals calculated by the two previous programs.

The user can input a start_date, and the bot will pull up a graph of all the calculations and data from your specified time period, and show all the calculated buy and sell signals.

As you will see below, there are three different graphs.

- Top Graph: Shows the stock price, the moving averages, and the buy signals (green triangle) and sell signals (red triangle)
- Middle Graph: Shows the other technical indicators, such as RSI, the calculated overbought and oversold levels, and the calculated support and resistance levels
- Bottom Graph: Shows the stock volume. This doesn't currently have any impact on the program, but it takes up unused space and can explain sudden price changes

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

