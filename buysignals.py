import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
import random

print('Buy Signal Screening Started')

def download_stock_data(symbol, start_date, end_date):
    stock_data = yf.download(symbol, start=start_date, end=end_date, progress=False)
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


def check_buy_signals(stocks, start_date, end_date):
    buy_list = []

    for stock_symbol in stocks:
        stock_data = download_stock_data(stock_symbol, start_date, end_date)
        stock_data = calculate_technical_indicators(stock_data)
        buy_signals = generate_buy_signals(stock_data)

        if buy_signals:
            # Check if there was a buy signal in the past day
            last_buy_signal_date = stock_data.index[buy_signals[-1]]
            today = datetime.now().date()
            if (today - last_buy_signal_date.date()).days == 1:
                buy_list.append((stock_symbol, get_random_message()))

    return buy_list

def get_random_message():
    messages = [
        "is looking goated 🐐",
        "is on fire 🔥",
        "will make some money 💸",
        "is looking bullish 🐂",
        "is surfing the market waves 🌊",
        "is taking off 🚀",
        "is singing a profitable tune 🎶",
        "is dancing with the bulls 💃",
        "is turning heads on Wall Street 👀",
        "is playing the market game like a pro 🎮",
        "is painting the charts green 🖌️💚",
        "is a rising star ✨",
        "is riding the momentum like a boss 🏄‍♂️",
        "is the hidden gem 💎",
        "is painting profits 🎨",
        "is on the rollercoaster of success 🎢",
        "is taking the market by storm 🌪️"
    ]
    return random.choice(messages)

def send_email(stock_list):
    # Replace 'your_email@gmail.com' and 'your_password' with your Gmail credentials
    from_email = 'iamdylanhoag@gmail.com'
    password = 'hwys aypg refe luea'

    current_date = datetime.now()
    current_day_name = current_date.strftime('%A')

    subject = f'{current_day_name} Buy Signals!'
    body = f"Here are stocks with a buy signal in the past day:\n\n"
    
    for stock_symbol, message in stock_list:
        body += f"{stock_symbol} {message}\n"

    body += "\nBest regards,\nYour Trading Bot"

    to_emails = ['dysco712@gmail.com', '79dmarbles@gmail.com', 'demise226565@gmail.com']

    message = MIMEText(body)
    message['Subject'] = subject
    message['From'] = from_email
    message['To'] = ', '.join(to_emails)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(from_email, password)
            server.sendmail(from_email, to_emails, message.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email. Error: {e}")

def main():
    # Customize the list of stock symbols
    stock_symbols = ["AAPL", "MSFT", "GOOG", "GOOGL", "AMZN", "NVDA", "META", "TSLA", "LLY", "V", "AVGO", "JPM", "UNH", "WMT", "XOM", "MA", "JNJ", "PG", "HD", "COST", "MRK", "ORCL", "ABBV", "CVX", "ADBE", "CRM", "KO", "BAC", "AMD", "PEP", "ACN", "NFLX", 
                     "MCD", "TMO", "CSCO", "INTC", "LIN", "ABT", "TMUS", "CMCSA", "WFC", "INTU", "DHR", "DIS", "AMGN", "VZ", "PFE", "NKE", "QCOM", "IBM", "TXN", "NOW", "PM", "CAT", "MS", "UNP", "BX", "GE", "SPGI", "UPS", "AXP", "COP", "HON", "BA", "UBER", "ISRG", 
                     "PLD", "LOW", "AMAT", "NEE", "RTX", "GS", "BKNG", "BLK", "SYK", "T", "MDT", "SCHW", "LMT", "VRTX", "ELV", "DE", "TJX", "GILD", "SBUX", "PANW", "BMY", "C", "LRCX", "REGN", "MDLZ", "PGR", "CVS", "AMT", "ADP", "ETN", "MMC", "ADI", "CB", "ZTS", 
                     "MU", "CI", "ABNB", "BSX", "FI", "ANET", "SO", "SHW", "EQIX", "ITW", "KLAC", "DUK", "HCA", "SNPS", "MO", "WM", "CDNS", "NOC", "SLB", "ICE", "CME", "GD", "MCO", "CSX", "BDX", "EOG", "CL", "MAR", "PYPL", "USB", "TGT", "MCK", "LULU", "CMG", "FDX", 
                     "MNST", "CTAS", "AON", "MPC", "MMM", "PNC", "PH", "FCX", "APD", "PSX", "APH", "TDG", "ROP", "ECL", "ORLY", "TT", "EMR", "HUM", "CHTR", "NXPI", "MSI", "RSG", "PXD", "NSC", "PSA", "ADSK", "DHI", "OXY", "MET", "WELL", "AJG", "PCAR", "TFC", "CCI", 
                     "COF", "AFL", "DXCM", "GM", "EL", "FTNT", "SPG", "SRE", "AIG", "STZ", "CARR", "HLT", "KHC", "MCHP", "ROST", "CPRT", "F", "EW", "VLO", "TRV", "KDP", "IDXX", "AZO", "COR", "HES", "NEM", "MSCI", "PAYX", "AEP", "LEN", "O", "WMB", "ODFL", "BK", 
                     "CNC", "KMB", "GWW", "NUE", "DLR", "KVUE", "OKE", "TEL", "MRNA", "KMI", "D", "ALL", "LHX", "CTSH", "IQV", "HSY", "AMP", "JCI", "A", "SYY", "URI", "AME", "DOW", "LVS", "PCG", "PRU", "ADM", "EA", "FIS", "FAST", "YUM", "CEG", "GIS", "BIIB", 
                     "EXC", "IT", "OTIS", "ROK", "GEHC", "VRSK", "PPG", "CSGP", "GPN", "XEL", "CMI", "KR", "NDAQ", "CTVA", "DD", "EXR", "VICI", "BKR", "ON", "ED", "IR", "RCL", "HAL", "MLM", "LYB", "FICO", "ANSS", "PEG", "EFX", "VMC", "DLTR", "DG", "HPQ", "PWR", 
                     "CDW", "ACGL", "MPWR", "FANG", "TTWO", "DVN", "DFS", "EIX", "XYL", "BF.B", "KEYS", "WEC", "GLW", "CAH", "CBRE", "WBD", "AVB", "SBAC", "AWK", "ZBH", "WST", "WTW", "MTD", "RMD", "FTV", "DAL", "HIG", "TROW", "WY", "TSCO", "CHD", "BR", "GRMN", 
                     "STT", "EQR", "ULTA", "FITB", "WAB", "NVR", "RJF", "APTV", "HWM", "PHM", "DTE", "MOH", "MTB", "STE", "FE", "ARE", "ILMN", "ETR", "EBAY", "BRO", "ROL", "CCL", "LYV", "VRSN", "ALGN", "TDY", "INVH", "HPE", "BLDR", "VTR", "EXPE", "DOV", "PTC", 
                     "FLT", "IFF", "BAX", "WBA", "PPL", "ES", "JBHT", "IRM", "GPC", "CTRA", "COO", "K", "LH", "AEE", "AXON", "WRB", "PFG", "DRI", "TRGP", "VLTO", "EXPD", "STLD", "WAT", "HBAN", "TYL", "CNP", "NTAP", "MKC", "EPAM", "AKAM", "CLX", "BALL", "FDS", 
                     "OMC", "HUBB", "ATO", "HOLX", "HRL", "NTRS", "STX", "FSLR", "LUV", "RF", "CMS", "J", "CINF", "SWKS", "JBL", "WDC", "EG", "CE", "TER", "ESS", "BBY", "AVY", "L", "TSN", "IEX", "MAA", "TXT", "EQT", "LW", "DGX", "SYF", "LDOS", "MAS", "ENPH", 
                     "SNA", "PKG", "GEN", "ALB", "POOL", "CFG", "CF", "SWK", "FOX", "FOXA", "MGM", "DPZ", "NDSN", "AMCR", "NWS", "BEN", "INCY", "NWSA", "VTRS", "PODD", "HST", "KIM", "CAG", "BG", "SJM", "MRO", "RVTY", "TAP", "CBOE", "KEY", "UAL", "IP", "CPB", 
                     "LNT", "ZBRA", "TRMB", "UDR", "LKQ", "EVRG", "AES", "IPG", "JKHY", "AOS", "NI", "JNPR", "REG", "TFX", "PNR", "NRG", "TECH", "PEAK", "PAYC", "GL", "KMX", "BXP", "CRL", "UHS", "MOS", "WRK", "WYNN", "CPT", "FFIV", "ALLE", "EMN", "CDAY", "CHRW", 
                     "MKTX", "HII", "MTCH", "APA", "DVA", "QRVO", "HSIC", "CZR", "BBWI", "BIO", "RL", "CTLT", "PARA", "AIZ", "AAL", "RHI", "ETSY", "FRT", "TPR", "PNW", "IVZ", "XRAY", "BWA", "GNRC", "FMC", "CMA", "NCLH", "HAS", "MHK", "VFC", "WHR", "ZION", "RIVN",
                     "APLS", "BROS", "HLN", "ALLY", "GSK", "PLNT", "GOLD", "MARA", "RIOT", "ANF", "GPRO", "JYNT", "BVS", "NFGC", "OPK", "RMCF", "U", "LYFT", "EDR", "RBLX", "DDOG", "BN", "PARR", "LANC", "SQ", "AESI", "NET", "RIO", "EXAS", "PINS", "HMC", "KNF",
                     "SE", "DO", "PI", "TSM", "CX", "SRPT", "YUMC"]

    start_date = datetime(2022, 1, 1)
    end_date = datetime.now()

    buy_list = check_buy_signals(stock_symbols, start_date, end_date)

    if buy_list:
        send_email(buy_list)
    else:
        print("No stocks with buy signals in the past day.")

if __name__ == "__main__":
    main()

#STOCKBOT. Made by Dylan Hoag



