import yfinance as yf
import pandas as pd
import talib
import numpy as np
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime

print('Stock Screening Started')

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

def check_buy_signals_within_range(stock_data, start_date, end_date):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    buy_signals_within_range = (
        (stock_data['Buy_Signal'].notnull()) &
        (stock_data.index >= start_date) &
        (stock_data.index <= end_date)
    )
    return buy_signals_within_range.sum() > 0

def calculate_buy_signals(stock_data):
    condition_1 = (stock_data['SMA_50'] > stock_data['SMA_200']) & \
                  (stock_data['RSI'] < 33) & \
                  (stock_data['Close'] > stock_data['Support_Level']) & \
                  (stock_data['%K'] > stock_data['%D']) & \
                  (stock_data['%K'] < 33)

    condition_2 = (stock_data['RSI'] < 28) & \
                  (stock_data['SMA_50'] < stock_data['SMA_200']) & \
                  (stock_data['%K'] < 28)
    
    condition_3 = (
        (stock_data['RSI'] < 24)
    )

    buy_signals = condition_1 | condition_2 | condition_3
    stock_data['Buy_Signal'] = np.where(buy_signals, stock_data['Close'], None)

    return stock_data

def check_stock_analysis(stock_data, stock_symbol, buy_signals_within_range, stock_messages):
    promising_stocks = []  # Initialize the list to store promising stocks for each stock symbol
    if not stock_data.empty and len(stock_data) > 0:
        last_row = stock_data.iloc[-1]
        other_conditions = (
            last_row['SMA_50'] > last_row['SMA_200'] and
            last_row['Close'] > last_row['Support_Level'] and
            last_row['%K'] > last_row['%D'] and
            last_row['%K'] < 32 and
            last_row['RSI'] < 32
        )
        second_condition = (
            last_row['RSI'] < 28 and
            last_row['SMA_50'] < last_row['SMA_200'] and
            last_row['%K'] < 28  # other conditions
        )
        third_condition = (
            last_row['RSI'] < 23
        )
        if second_condition or other_conditions or third_condition:

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
            if buy_signals_within_range:
                promising_stocks.append(stock_symbol)
                random_message = np.random.choice(messages)
                stock_messages.append(f"{random_message}")

    return promising_stocks

def send_email(stock_messages):
    sender_email = "iamdylanhoag@gmail.com"
    receiver_email = "dysco712@gmail.com"
    password = "hwys aypg refe luea"

    current_datetime = datetime.datetime.now()
    day_of_week = current_datetime.strftime("%A")

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = f"{day_of_week} Buy Signals"

    # Combine stock symbols and random messages in the email body
    body = "Here are the stocks for today!\n\n"
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
    stock_symbols = ["GOOGL", "TSLA", "APLS", "PLNT", "CX", "WM", "VMC", "VZ", "VTI", "VB", "U", "TTWO", "TSM", "SE", "CRM", "RMCF", "RBLX", "RIVN", "RIOT", "RIO", "RSG", "PFE", "PARR", "OPK", "NEE", "NFGC", "MARA", "DOCU", "BURL", "SGML", "FIVE", "LYFT", "LANC", 
                     "JYNT", "JNJ", "XT", "ICE", "PI", "HMC", "GPRO", "GE", "EXAS", "EDR", "DO", "DDOG", "KO", "NET", "CVX", "BN", "SQ", "BLK", "BVS", "AESI", "ANET", "AAL", "ANF", "META", "KNF", "PXD", "BHP", "MTD", "CRSR", "LLY", "V", "JPM", "PG", "HD", "BABA", 
                     "BAC", "PEP", "NVS", "MCD", "SAP", "TMUS", "TTE", "ABT", "PM", "COP", "TXN", "MS", "SPGI", "HON", "UPS", "RTX", "UL", "CAT", "T", "LMT", "ASR", "FVRR", "PACB", "CSX", "UBER", "AZN", "CVS", "PANW", "UNH", "XOM", "AVGO", "MA", "MRK", "ABBV", 
                     "WMT", "ACN", "LIN", "AMD", "TMO", "DIS", "IBM", "NKE", "NOW", "BMY", "ELV", "VRTX", "MMC", "RCL", "STEM", "ZTO", "RHP", "SYK", "CI", "CB", "AMT", "SLB", "MU", "BSX", "FI", "MO", "DUK", "CDNS", "NOC", "ITW", "SHW", "GD", "USB", "MMM", "TT", 
                     "LULU", "F", "LCID", "NIO", "PSA", "YUM", "EA", "CRSP", "SPB", "HOG", "CMI", "KR", "HPE", "MRO", "CLX", "BG", "BALL", "ARE", "PFG", "WBA", "EQT", "TXT", "CF", "OMC", "WAT", "DGX", "HUBB", "RF", "IEX", "AVY", "SWKS", "SNA", "JBHT", "EMR", 
                     "PYPL", "GLOB", "OC", "YUMC", "PKG", "ALGN", "MAA", "LDOS", "EPAM", "ALB", "LUV", "WRB", "STX", "WDC", "ESS", "K", "LW", "AMCR", "TSN", "SWK", "CAG", "BBY", "DPZ", "POOL", "LNT", "SYF", "CCL", "MAS", "CFG", "APA", "L", "LYV", "HST", "LKQ", 
                     "CE", "CNQ", "DLB", "AAP", "NDSN", "EVRG", "SJM", "TER", "AES", "MOS", "MGM", "ENPH", "ROL", "ZBRA", "JKHY", "KEY", "NRG", "KMX", "TRMB", "NI", "INCY", "GL", "REG", "TFX", "PNR", "CDAY", "UDR", "GEN", "WRK", "CPT", "CZR", "TDG", "KTOS", 
                     "HAE", "RLJ", "HII", "TECH", "CRL", "PEAK", "EMN", "ALLE", "AOS", "QRVO", "AIZ", "MKTX", "RHI", "HSIC", "PNW", "UHS", "BXP", "CPB", "MTCH", "FOXA", "PAYC", "BWA", "ETSY", "BBWI", "FMC", "FRT", "BEN", "GNRC", "TPR", "RNR", "CTLT", "IVZ", 
                     "PARA", "WHR", "BIO", "HAS", "CMA", "NCLH", "VFC", "SEE", "RL", "DVA", "MHK", "ALK", "SEDG", "FOX", "NWS", "RHHBY", "CL", "KMB", "HSY", "GIS", "XEL", "ORAN", "ED", "WEC", "VFS", "SRPT", "AEE", "HRL", "CMS", "KKPNY", "FLO", "PNM", "NEA", 
                     "NAD", "BTT", "SAFT", "RY", "SONY", "ADP", "ETN", "REGN", "C", "UBS", "ABNB", "FSR", "RACE", "MELI", "FDX", "CMG", "MAR", "SCCO", "INN", "MPC", "SNOW", "MSI", "TGT", "PSX", "APO", "TEAM", "KDP", "HLT", "AEP", "SGEN", "BUD", "SHOP", "PINS", 
                     "BX", "ECL", "HES", "VLO", "DHI", "ET", "LNG", "STZ", "JD", "GWW", "DLR", "CEG", "EW", "TRV", "STM", "WDS", "D", "NUE", "LVS", "O", "DASH", "AME", "DOW", "ALL", "CVE", "SYY", "ARES", "SPOT", "CSGP", "A", "DD", "DVN", "ON", "FANG", "IR", 
                     "GOLD", "NTR", "ZS", "WST", "SPLK", "WBD", "MPWR", "CHPT", "EC", "AWK", "GIB", "IX", "GRMN", "TEF", "TSCO", "HUBS", "DFS", "STT", "BR", "FE", "FTS", "MTB", "INVH", "OWL", "GPC", "TRGP", "ES", "SNAP", "IFF", "MKL", "IRM", "WMG", "ATO", 
                     "JBL", "DECK", "ADT", "DNMR", "TEVA", "TM", "PII", "GOEV", "STLA", "GM", "NVO", "SNY", "HLN", "GSK", "RPRX", "ALNY", "CRH", "JHX", "USLM", "EXP", "MLM", "SMID", "SUM", "SND", "NWPX", "COIN", "BYND", "EWBC", "PLTR", "QQQ", "TTD", "NU", 
                     "SOFI", "AFRM", "APPN", "SWN", "BBD", "CNM", "ACIW", "NEM", "VALE", "GRAB", "HWM", "AXON", "LHX", "HEI", "WWD", "CW", "CAE", "DRS", "ERJ", "MRCY", "ACHR", "CDRE", "SPCE", "PL", "SKYH", "ATRO", "PKE", "KITT", "TATT", "ASTR", "MNTS", "GPS", 
                     "AAPL", "MSFT", "AMZN", "NVDA", "GOOG", "COST", "ADBE", "NFLX", "CSCO", "INTC", "WFC", "CMCSA", "INTU", "ORCL", "QCOM", "DHR", "BA", "AMGN", "UNP", "AMAT", "LOW", "GS", "BKNG", "PLD", "ISRG", "SBUX", "MDT", "AXP", "DE", "TJX", "SCHW", 
                     "LRCX", "GILD", "ADI", "MDLZ", "PGR", "ZTS", "SNPS", "KLAC", "SO", "CME", "EQIX", "EOG", "BDX", "MCO", "PNC", "APD", "MCK", "FCX", "AON", "APH", "PH", "NXPI", "ROP", "ORLY", "HUM", "HCA", "NSC", "ADSK", "PCAR", "CCI", "WELL", "COF", "MCHP", 
                     "CTAS", "TFC", "AJG", "SPG", "CARR", "AIG", "SRE", "AZO", "ROST", "DXCM", "IDXX", "TEL", "AFL", "MSCI", "WMB", "CPRT", "IQV", "PAYX", "MET", "MNST", "OKE", "OXY", "BK", "CNC", "CHTR", "URI", "AMP", "ADM", "JCI", "CTSH", "PRU", "FAST", "LEN", 
                     "FTNT", "PCG", "KVUE", "OTIS", "ODFL", "BIIB", "FIS", "ROK", "EXC", "IT", "PPG", "VRSK", "KMI", "EL", "COR", "CTVA", "HAL", "GPN", "VICI", "EXR", "PWR", "PEG", "CDW", "GEHC", "EFX", "FICO", "MRNA", "KHC", "DG", "DLTR", "KEYS", "CBRE", "ACGL", 
                     "SBAC", "EIX", "XYL", "AVB", "DAL", "HPQ", "ANSS", "RMD", "FTV", "ZBH", "WY", "APTV", "CAH", "LYB", "WTW", "HIG", "TROW", "ULTA", "FITB", "GLW", "DTE", "WAB", "CHD", "EBAY", "PHM", "NVR", "ILMN", "STE", "DOV", "RJF", "ETR", "EQR", "MOH", 
                     "PTC", "BLDR", "FLT", "TDY", "EXPE", "DRI", "BAX", "VTR", "PPL", "CTRA", "NDAQ", "LH", "NTAP", "CBOE", "STLD", "EXPD", "VRSN", "AKAM", "HBAN", "CNP", "COO", "VLTO", "FSLR", "FDS", "HOLX", "NTRS", "TYL", "MKC", "BRO", "J", "CINF", "EG", "PODD", 
                     "UAL", "KIM", "RVTY", "IP", "VTRS", "IPG", "TAP", "FFIV", "CHRW", "JNPR", "NWSA", "WYNN", "XRAY", "ZION", "NWS" 
                    ]
    

    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    current_datetime = datetime.datetime.strptime(current_date, "%Y-%m-%d")
    next_day_datetime = current_datetime + datetime.timedelta(days=1)
    next_day_date = next_day_datetime.strftime("%Y-%m-%d")

    start_date = "2022-01-11"  # YYYY-MM-DD
    end_date = next_day_date

    stock_messages = []  # Create a list to store formatted stock messages

    for stock_symbol in stock_symbols:
        stock_data = download_stock_data(stock_symbol, start_date, end_date)

        if not stock_data.empty and len(stock_data) > 0:
            stock_data = calculate_technical_indicators(stock_data)
            stock_data = calculate_buy_signals(stock_data)
            buy_signals_within_range = check_buy_signals_within_range(stock_data, start_date, end_date)
            promising_stocks = check_stock_analysis(stock_data, stock_symbol, buy_signals_within_range, stock_messages)

    if stock_messages:
        send_email(stock_messages)
        print('Buy Signals Detected. Email Sent')
    else:
        print('No Buy Signals Found; No Email Sent')
        if is_weekend():
            print("It's the weekend. Market might be closed.")

#STOCKBOT. Made by Dylan Hoag



