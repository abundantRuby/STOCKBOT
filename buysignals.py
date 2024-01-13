import yfinance as yf
import pandas as pd
import numpy as np
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime

print('Stock Screening Has Started')

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
    stock_data['RSI'] = 100 - (100 / (1 + (stock_data['Close'].diff(1).apply(lambda x: max(0, x)) / stock_data['Close'].diff(1).apply(lambda x: abs(min(0, x)))).rolling(window=rsi_period).mean()))

    stock_data['Support_Level'] = stock_data['Low'].rolling(window=50).min()
    stock_data['Resistance_Level'] = stock_data['High'].rolling(window=50).max()

    # Calculate the Stochastic Oscillator
    stoch_period = 14
    stock_data['%K'] = 100 * ((stock_data['Close'] - stock_data['Low'].rolling(window=stoch_period).min()) /
                               (stock_data['High'].rolling(window=stoch_period).max() - stock_data['Low'].rolling(window=stoch_period).min()))
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

def calculate_buy_signals(stock_data, start_date, end_date):
    conditions = (stock_data['SMA_50'].shift(1) > stock_data['SMA_200'].shift(1)) & \
                  (stock_data['Close'].shift(1) > stock_data['Support_Level'].shift(1)) & \
                  (stock_data['%K'].shift(1) > stock_data['%D'].shift(1)) & \
                  (stock_data['%K'].shift(1) < 30)
    conditions_past_7_days = conditions.fillna(0).rolling(window=7).sum() > 0
    stock_data['Buy_Signal'] = np.where(conditions_past_7_days, stock_data['Close'], None)

    return stock_data

def check_stock_analysis(stock_data, stock_symbol, buy_signals_within_range, stock_messages):
    promising_stocks = []  # Initialize the list to store promising stocks for each stock symbol
    if not stock_data.empty and len(stock_data) > 0:
        last_row = stock_data.iloc[-1]
        other_conditions = (
            last_row['SMA_50'] > last_row['SMA_200'] and
            last_row['Close'] > last_row['Support_Level'] and
            last_row['%K'] > last_row['%D'] and
            last_row['%K'] < 36 and
            last_row['RSI'] < 36
        )
        second_condition = (
            last_row['RSI'] < 30 and
            last_row['SMA_50'] < last_row['SMA_200'] and
            last_row['%K'] < 30  # other conditions
        )
        if second_condition or other_conditions:

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

current_date = datetime.datetime.now()
day_of_week = current_date.weekday()
day_name = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'][day_of_week]

def send_email(stock_messages):
    sender_email = "iamdylanhoag@gmail.com"
    receiver_emails = ["dysco712@gmail.com", "iamdylanhoag@gmail.com"]
    password = "hwys aypg refe luea"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg["To"] = ", ".join(receiver_emails)
    msg['Subject'] = (f"{day_name} Promising Stocks")

    # Combine stock symbols and random messages in the email body
    body = "Here are the stocks for today!\n\n"
    body += "\n".join(stock_messages)
    body += "\nBest regards,\nYour Trading Bot"

    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_emails, msg.as_string())

if __name__ == "__main__":
    stock_symbols = ["GOOGL", "TSLA", "APLS", "PLNT", "CX", "WM", "VMC", "VZ", "VTI", "VB", "U", "TTWO", "TSM", "SE", "CRM", "RMCF", "RBLX", "RIVN", "RIOT", "RIO", "RSG", "PFE", "PARR", "OPK", "NEE", "NFGC", "MARA", "DOCU", "BURL", "SGML", "FIVE",
                     "LYFT", "LANC", "JYNT", "JNJ", "XT", "ICE", "PI", "HMC", "GPRO", "GE", "EXAS", "EDR", "DO", "DDOG", "KO", "NET", "CVX", "BN", "SQ", "BLK", "BVS", "AESI", "ANET", "AAL", "ANF", "META", "KNF", "PXD", "BHP", "MTD", "CRSR",
                     "LLY", "V", "JPM", "PG", "HD", "BABA", "BAC", "PEP", "CRM", "NVS", "MCD", "SAP", "TMUS", "TTE", "ABT", "VZ", "PM", "COP", "TXN", "MS", "GE", "SPGI", "HON", "UPS", "RTX", "UL", "CAT", "T", "LMT", "ASR", "FVRR", "PACB", "CSX",
                      "UBER", "AZN", "CVS", "PANW", "UNH", "XOM", "AVGO", "MA", "MRK", "ABBV", "WMT", "ACN", "LIN", "AMD", "TMO", "DIS", "PM",  "IBM", "NKE", "NOW", "BMY", "ELV", "VRTX", "MMC", "RCL", "STEM", "ZTO", "RHP",
                     "SYK", "CI", "CB", "AMT", "SLB", "MU", "BSX", "FI", "MO", "DUK", "CDNS", "NOC", "ITW", "SHW", "GD", "USB", "MMM", "TT", "LULU", "F", "LCID", "NIO", "PSA", "YUM", "EA", "CRSP", "SPB", "HOG",
                     "CMI", "KR", "VMC", "HPE", "MRO", "CLX", "BG", "BALL", "ARE", "PFG", "WBA", "EQT", "TXT", "CF", "OMC", "WAT", "DGX", "HUBB", "RF", "IEX", "AVY", "SWKS", "SNA", "JBHT", "EMR", "PYPL", "GLOB", "OC", "YUMC",
                     "PKG", "ALGN", "MAA", "LDOS", "EPAM", "ALB", "LUV", "WRB", "STX", "WDC", "ESS", "K", "LW", "AMCR", "TSN", "SWK", "CAG", "BBY", "DPZ", "POOL", "LNT", "SYF", "CCL", "MAS", "CFG", "APA", "L", "LYV", "HST", "LKQ", "CE", "CNQ", "UL", "DLB", "AAP",
                     "NDSN", "EVRG", "SJM", "TER", "LW", "AES", "MOS", "MGM", "ENPH", "ROL", "ZBRA", "JKHY", "KEY", "NRG", "KMX", "TRMB", "NI", "INCY", "GL", "REG", "TFX", "PNR", "CDAY", "UDR", "GEN", "WRK", "CPT", "CZR", "TDG", "KTOS", "NOC", "HAE", "RLJ",
                     "HII", "TECH", "CRL", "PEAK", "EMN", "ALLE", "AOS", "QRVO", "AIZ", "MKTX", "RHI", "HSIC", "PNW", "UHS", "BXP", "CPB", "MTCH", "FOXA", "PAYC", "BWA", "ETSY", "AAL", "BBWI", "FMC", "FRT", "BEN", "GNRC", "TPR", "RNR", 
                     "CTLT", "IVZ", "PARA", "WHR", "BIO", "HAS", "CMA", "NCLH", "VFC", "SEE", "RL", "DVA", "MHK", "ALK", "SEDG", "FOX", "NWS", "PG", "MRK", "RHHBY", "VZ", "DUK", "CL", "KMB", "HSY", "GIS", "XEL", "ORAN", "ED", "WEC", "VFS", "SRPT",
                     "AEE", "K", "HRL", "CMS", "KKPNY", "CPB", "FLO", "PNM", "NEA", "NAD", "BTT", "SAFT", "WM", "CL", "PG", "DIS", "HON", "CAT", "RY", "SONY", "ADP", "ETN", "CVS", "REGN", "C", "UBS", "ABNB", "FSR", "RACE", "MELI", "FDX", "CMG", "MAR", "SCCO", "INN",
                     "MPC", "SNOW", "MSI", "TT", "TGT", "PSX", "RSG", "APO", "TEAM", "KDP", "HLT", "AEP", "SGEN", "BUD", "BLK", "AZN", "SHOP", "PINS", "BX", "ECL", "HES", "VLO", "DHI", "ET", "LNG", "STZ", "JD", "GWW", "DLR",
                     "CEG", "EW", "TRV", "STM", "WDS", "D", "NUE", "LVS", "O", "DASH", "AME", "DOW", "ALL", "CVE", "SYY", "ARES", "SPOT", "CSGP", "A", "ED", "DD", "DVN", "ON", "FANG", "IR", "GOLD", "NTR", "ZS", "WST", "SPLK", "WBD", "MPWR", "CHPT",
                     "EC", "AWK", "GIB", "IX", "GRMN", "TEF", "TSCO", "HUBS", "DFS", "STT", "BR", "FE", "FTS", "MTB", "INVH", "OWL", "GPC", "TRGP", "ES", "SNAP", "IFF", "K", "MKL", "IRM", "WMG", "TSN", "CLX", "ATO", "JBL", "DECK", "ADT", "DNMR", "TEVA",
                     "TM", "HMC", "PII", "GOEV", "STLA", "GM", "NVO", "SNY", "HLN", "GSK", "RPRX", "ALNY", "CRH", "JHX", "USLM", "EXP", "MLM", "VMC", "SMID", "SUM", "SND", "NWPX", "COIN", "BYND", "EWBC", "PLTR", "QQQ", "TTD", "NU", "SOFI", "AFRM", "APPN",
                     "SWN", "BBD", "CNM", "CCL", "ACIW", "NEM", "VALE", "GRAB", "KEY", "HWM", "TXT", "AXON", "LHX", "HEI", "NOC", "WWD", "CW", "CAE", "DRS", "ERJ", "MRCY", "ACHR", "CDRE", "SPCE", "PL", "SKYH", "ATRO", "PKE", "KITT", "TATT", "ASTR", "MNTS", "GPS",
                     "AAPL", "MSFT", "AMZN", "NVDA", "GOOGL", "META", "GOOG", "TSLA", "AVGO", "JPM", "UNH", "LLY", "V", "XOM", "JNJ", "HD", "MA", "PG", "COST", "ADBE", "ABBV", "MRK", "CVX", "CRM", "PEP", "BAC", "KO", "WMT", "AMD", "NFLX", "ACN", "MCD", 
                     "CSCO", "TMO", "LIN", "INTC", "ABT", "WFC", "CMCSA", "INTU", "DIS", "ORCL", "VZ", "QCOM", "PFE", "TXN", "DHR", "NKE", "CAT", "BA", "AMGN", "IBM", "UNP", "PM", "NOW", "SPGI", "COP", "GE", "HON", "AMAT", "LOW", "UBER", "GS", "NEE", "BKNG", "PLD", 
                     "T", "RTX", "MS", "ISRG", "UPS", "BLK", "SBUX", "ELV", "MDT", "AXP", "DE", "BMY", "VRTX", "TJX", "SCHW", "LRCX", "CVS", "AMT", "GILD", "LMT", "SYK", "C", "ADI", "ADP", "MDLZ", "PANW", "ETN", "MMC", "PGR", "REGN", "BX", "ZTS", "CB", "CI", "MU", 
                     "SNPS", "BSX", "FI", "TMUS", "KLAC", "SO", "CME", "SLB", "EQIX", "DUK", "CDNS", "SHW", "MO", "EOG", "ITW", "ICE", "BDX", "CSX", "PYPL", "USB", "NOC", "WM", "CL", "CMG", "TGT", "ABNB", "MCO", "PNC", "APD", "MCK", "FCX", "PSX", "AON", "ANET", 
                     "MPC", "LULU", "APH", "PH", "NXPI", "MMM", "FDX", "ROP", "GD", "ORLY", "HUM", "TT", "TDG", "EMR", "MAR", "PXD", "HCA", "NSC", "MSI", "ADSK", "PCAR", "CCI", "ECL", "WELL", "COF", "GM", "MCHP", "CTAS", "TFC", "NEM", "AJG", "SPG", "CARR", "AIG", 
                     "F", "PSA", "SRE", "AZO", "ROST", "HLT", "DXCM", "VLO", "DHI", "EW", "IDXX", "NUE", "TEL", "AFL", "MSCI", "AEP", "WMB", "TRV", "CPRT", "IQV", "PAYX", "O", "MET", "A", "HES", "DLR", "KMB", "MNST", "OKE", "OXY", "D", "BK", "LHX", "CNC", "DOW", 
                     "CHTR", "STZ", "URI", "AMP", "ADM", "GIS", "CEG", "AME", "JCI", "CTSH", "SYY", "PRU", "FAST", "LEN", "FTNT", "PCG", "YUM", "KVUE", "OTIS", "ODFL", "GWW", "BIIB", "ALL", "CSGP", "ON", "FIS", "ROK", "EXC", "IT", "PPG", "CMI", "VRSK", "KMI", 
                     "XEL", "EA", "EL", "COR", "RSG", "CTVA", "HAL", "KDP", "GPN", "VICI", "EXR", "DD", "PWR", "ED", "PEG", "IR", "MLM", "CDW", "GEHC", "VMC", "KR", "MPWR", "EFX", "DVN", "FICO", "MRNA", "RCL", "KHC", "DG", "DLTR", "FANG", "KEYS", "CBRE", "ACGL", 
                     "HSY", "DFS", "SBAC", "EIX", "XYL", "AVB", "DAL", "WBD", "WST", "WEC", "HPQ", "ANSS", "MTD", "RMD", "AWK", "FTV", "ZBH", "TTWO", "WY", "APTV", "CAH", "LYB", "WTW", "HIG", "TROW", "ULTA", "STT", "FITB", "BR", "GLW", "TSCO", "DTE", "WAB", "CHD", 
                     "EBAY", "MTB", "PHM", "NVR", "ILMN", "HPE", "STE", "ES", "DOV", "RJF", "ETR", "EQR", "HWM", "MOH", "IFF", "PTC", "BLDR", "FLT", "TDY", "IRM", "EXPE", "ARE", "DRI", "INVH", "BAX", "VTR", "PPL", "GRMN", "GPC", "TRGP", "WAT", "CTRA", "ALGN", 
                     "FE", "AEE", "NDAQ", "LH", "NTAP", "CBOE", "STLD", "WBA", "EXPD", "CCL", "VRSN", "AKAM", "HBAN", "CNP", "AXON", "COO", "VLTO", "RF", "FSLR", "LVS", "SWKS", "BALL", "ENPH", "CLX", "LUV", "FDS", "HOLX", "NTRS", "HUBB", "PFG", "TYL", "ATO", 
                     "OMC", "MKC", "ALB", "CMS", "EPAM", "JBL", "BRO", "AVY", "JBHT", "IEX", "J", "CINF", "WDC", "TER", "STX", "EQT", "TXT", "ESS", "SYF", "EG", "MAA", "POOL", "MAS", "CFG", "CE", "DGX", "SNA", "LW", "CF", "SWK", "BG", "BBY", "PKG", "TSN", "PODD", 
                     "LDOS", "MRO", "DPZ", "WRB", "K", "AMCR", "NDSN", "HST", "UAL", "CAG", "ZBRA", "KIM", "KEY", "RVTY", "LYV", "GEN", "TRMB", "LKQ", "LNT", "IP", "SJM", "VTRS", "IPG", "L", "AES", "TECH", "ROL", "JKHY", "MGM", "KMX", "CRL", "EVRG", "MOS", "TFX", 
                     "PNR", "TAP", "INCY", "UDR", "NRG", "APA", "WRK", "REG", "PEAK", "QRVO", "ALLE", "NI", "FFIV", "MKTX", "EMN", "GL", "CPT", "CDAY", "HII", "ETSY", "BXP", "PAYC", "CHRW", "CZR", "AOS", "HSIC", "BBWI", "JNPR", "MTCH", "RHI", "AAL", "HRL", 
                     "UHS", "NWSA", "AIZ", "WYNN", "TPR", "CPB", "BEN", "NCLH", "BWA", "PNW", "GNRC", "IVZ", "CTLT", "FRT", "FMC", "PARA", "FOXA", "XRAY", "CMA", "BIO", "HAS", "WHR", "ZION", "VFC", "RL", "DVA", "MHK", "FOX", "NWS"
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
        stock_data = calculate_buy_signals(stock_data, start_date, end_date)
        buy_signals_within_range = check_buy_signals_within_range(stock_data, start_date, end_date)
        promising_stocks = check_stock_analysis(stock_data, stock_symbol, buy_signals_within_range, stock_messages)

if stock_messages:
    send_email(stock_messages)

print('Stock Screening Complete; Email Sent')


