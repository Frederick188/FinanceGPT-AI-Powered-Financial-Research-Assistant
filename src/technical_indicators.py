import pandas as pd
import ta

print("Reading stock data...")

df = pd.read_csv("../data/stock_data.csv")

df["Date"] = pd.to_datetime(df["Date"])

df["Close"] = pd.to_numeric(
    df["Close"],
    errors="coerce"
)

# RSI
df["RSI"] = ta.momentum.RSIIndicator(
    close=df["Close"],
    window=14
).rsi()

# SMA
df["SMA20"] = df["Close"].rolling(20).mean()
df["SMA50"] = df["Close"].rolling(50).mean()

# EMA
df["EMA20"] = df["Close"].ewm(
    span=20,
    adjust=False
).mean()

df["EMA50"] = df["Close"].ewm(
    span=50,
    adjust=False
).mean()

# MACD
macd = ta.trend.MACD(
    close=df["Close"]
)

df["MACD"] = macd.macd()

df["MACD_SIGNAL"] = (
    macd.macd_signal()
)

# Daily Return
df["RETURN"] = (
    df["Close"]
    .pct_change()
)

# 20-day Volatility
df["VOLATILITY"] = (
    df["RETURN"]
    .rolling(20)
    .std()
)

print(
    df[
        [
            "Date",
            "Close",
            "RSI",
            "SMA20",
            "SMA50",
            "EMA20",
            "EMA50",
            "MACD",
            "MACD_SIGNAL",
            "RETURN",
            "VOLATILITY"
        ]
    ].tail()
)

df.to_csv(
    "../data/technical_indicators.csv",
    index=False
)

print("Technical indicators saved.")