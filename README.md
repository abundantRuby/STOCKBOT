# STOCKBOT

Made by Dylan Hoag
- **Text:** (208)-989-8541
- **Email:** dysco712@gmail.com

## Main Programs

- [Buy Signals](#buy-signals)
- [Sell Signals](#sell-signals)
- [BONUS: Individual Screener](#individual-screener)


## Buy Signals

BuySignals.py Overview:

- Technical Analysis of over 600 stocks (including the S&P 500)
- Buy Signal Generation
- Daily Buy Signal Emails

BuySignals.py is the engine driving the buy signals behind STOCKBOT. Using cutting-edge technical analysis and external libraries such as [TA-lib](https://ta-lib.org/), this script analyzes stock data, pinpointing optimal entry points through a combination of moving averages, RSI, and stochastic oscillators. Once a list of stocks has been generated, an email is sent to the user with a randomly-selected message for each stock.

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

## Sell Signals

SellSignals.py Overview:

- Technical Analysis on Stocks of Your Choice
- Sell Signal Generation
- Daily Sell Signal Emails

SellSignals.py complements STOCKBOT by providing sell signals based on advanced technical indicators. Leveraging the power of algorithms and key indicators such as moving averages, RSI, and stochastic oscillators, this script identifies perfect moments to exit a stock position. Seamlessly integrated into your trading strategy, SellSignals.py ensures you stay ahead in the dynamic stock market landscape.


## Individual Screener

Individual-Screener.py Overview:

The Individual Screener is designed for in-depth analysis of individual stocks. It utilizes various technical indicators to provide insights into potential buy and sell signals, and displays all data on a visual graph.

Example: PLNT (Planet Fitness)
![Stock Analysis](https://i.ibb.co/4WwdH2K/plnt.png)
Example: APLS (Apellis Pharma)
![Stock Analysis](https://i.ibb.co/KLPg18K/apls.png)
Example: AMZN (Amazon)
![Stock Analysis](https://i.ibb.co/nrDJKbL/amzn.png)



