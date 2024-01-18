# STOCKBOT

Hey There 👋

STOCKBOT is a comprehensive tool developed in python that features three primary components: Buy Signals, Sell Signals, and the Individual Stock Screener.

This repository contains in-depth documentation about STOCKBOT, providing insights into each of the main programs. Additionally, you'll find SP500 backtesting results derived from over 44,400 data points since 2019.

Happy reading!

## Guide

- [1: Buy Signals](#buy-signals)
- [2: Sell Signals](#sell-signals)
- [3: Individual Screener](#individual-screener)
- [Testing and Data](#testing-and-data)
- [Other Information](#other-information)
- [Important Note](#important-note)


## Buy Signals

Buysignals.py Overview:

This program is the engine driving the buy signals behind STOCKBOT. This program leverages external libraries such as [TA-lib](https://ta-lib.org/) to perform complex technical analysis on stock data. 

Using a combination of moving averages, RSI, support and resistance levels, and stochastic oscillators, this program precisely identifies optimal entry points for stock investments.

It performs these calculations across a large list of stocks, and then proceeds to send an email containing all the signals to the user.

To send the emails, STOCKBOT securely connects to the Gmail SMTP server by using a remote access code, which allows it to send authorized emails.

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

Furthermore, this program operates on a CRON schedule, which ensures that users receive automated daily emails containing the latest buy signals.

## Sell Signals

SellSignals.py Overview:

This program calculates the sell signals behind STOCKBOT. Using the same technical indicators as buysignals.py, this program identifies optimal points to exit a holding in the stock market.

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

Users can specify a start_date, which prompts the bot to generate a graph with the calculations and data from the designated time period.

The screener includes three different graphs:

- Top Graph: Displays stock price along with moving averages, depicting buy signals (green triangle) and sell signals (red triangle).
- Middle Graph: Illustrates other technical indicators, including RSI, overbought and oversold levels, and support and resistance levels.
- Bottom Graph: Shows stock volume, which currently has no impact on the bot's decision-making. It simply serves as more info on unused space.

In these examples, the bot is displaying all data and calculations since 2020.

Example 1: AAPL (Apple)
![Stock Analysis](https://i.ibb.co/nCLLvPp/AAPL.png)
Example 2: WM (Waste Management)
![Stock Analysis](https://i.ibb.co/56YZTDj/WM.png)
Example 3: AMZN (Amazon)
![Stock Analysis](https://i.ibb.co/TKr81ry/amzn.png)

## Testing and Data

To test the accuracy of STOCKBOT, CalcROI.py was built.

This program calculates ROI by determining the average percent return per transaction, and provides an overall ROI per stock (and for a list of stocks).

It identifies buy signals, and when it encounters the next available sell signal, it computes the ROI for those transaction(s).

Here is an example:

- Buy Signal on July 15
- Buy Signal on July 19
- Buy Signal on July 25
- Sell Signal on July 28 (sell 3x)

In this scenario, all three buy signals were sold on July 28, and the ROI was calculated individually for each of those three transactions.

This program was modified to compute the ROI for a long stock list. In my test, I determined the average ROI per transaction for the entire S&P 500 since 2019 (over 5 years of data).

This test analysed 44,400 data points (each representing one calculated transaction), and resulted in an average ROI per transaction of 4.49%. The program was also adjusted to calculate the average holding time (from buy to sell), which was found to be 64 days.

So in theory, according to this extensive test data, investing in a buy signal will result in a 4.49% gain when sold at the sell signal (about 64 days later). The more buy signals you invest in, the closer your returns will align with these figures.

Predicting the average yearly ROI from this data is challenging, if not impossible, since it depends on many factors such as the number of buy signals invested in, compounding of your funds, and how the market is performing.

But for a very simple estimation based on our data, we can assume investments in 64-day periods:

- Day 1: Invest $100 evenly across x stocks with buy signals.
- Day 65: With $104.49, reinvest across x stocks.
- Day 129: With $109.18, repeat the process.
- Day 193: With $114.08, reinvest.
- Day 257: With $119.20, reinvest.
- Day 321: With $124.55. Assume year ends.

In this very basic scenario, the gain would be 24.55% in 0.88 years. In a more realistic setting, with consistent investments and compounding, and a larger number of buy signals, the actual returns could surpass this figure.

It's important to note that this data and average ROI is generated only by the bot's decisions, and without human intervention. If desired, users can apply their own investment logic, including the use of stop prices.

## Other Information

STOCKBOT was built in python 3.11.7 with the following libraries:

- [yfinance](https://pypi.org/project/yfinance/): Fetches financial data from Yahoo Finance.
- [pandas](https://pandas.pydata.org/): Data manipulation and analysis.
- [TA-lib](https://ta-lib.org/): Technical analysis of financial markets.
- [numpy](https://numpy.org/): Scientific computing with Python.
- [smtplib](https://docs.python.org/3/library/smtplib.html): Sending emails using the SMTP.
- [datetime](https://docs.python.org/3/library/datetime.html): Allows for manipulating dates and times.

Dependencies and versions are specified in requirements.txt

## Important Note

Your comments or suggestions are extremely appreciated, so please reach out!

Text 📱: 208-989-8541  
Email 📧: iamdylanhoag@gmail.com

-Dylan Hoag 😊

