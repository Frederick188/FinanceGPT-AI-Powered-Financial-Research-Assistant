import yfinance as yf
import pandas as pd
import ta

import plotly.express as px
import plotly.graph_objects as go

import streamlit as st


def load_stock_data(ticker):

    df = yf.download(
        ticker,
        period="1y",
        auto_adjust=True,
        progress=False
    )

    # Flatten MultiIndex columns
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df.reset_index(inplace=True)

    return df


# ---------------------------------------
# Candlestick Chart
# ---------------------------------------

def plot_candlestick(df, ticker):

    fig = go.Figure(

        data=[

            go.Candlestick(

                x=df["Date"],

                open=df["Open"],

                high=df["High"],

                low=df["Low"],

                close=df["Close"]

            )

        ]

    )

    fig.update_layout(

        title=f"{ticker} Candlestick Chart",

        xaxis_title="Date",

        yaxis_title="Price",

        height=500
    )

    st.plotly_chart(

        fig,

        use_container_width=True
    )


# ---------------------------------------
# Price Chart
# ---------------------------------------

def plot_price(df, ticker):

    fig = px.line(

        df,

        x="Date",

        y="Close",

        title=f"{ticker} Closing Price"
    )

    st.plotly_chart(

        fig,

        use_container_width=True
    )


# ---------------------------------------
# Volume Chart
# ---------------------------------------

def plot_volume(df):

    fig = px.bar(

        df,

        x="Date",

        y="Volume",

        title="Trading Volume"
    )

    st.plotly_chart(

        fig,

        use_container_width=True
    )


# ---------------------------------------
# RSI Chart
# ---------------------------------------

def plot_rsi(df):

    df["RSI"] = ta.momentum.RSIIndicator(

        df["Close"],

        window=14

    ).rsi()

    fig = go.Figure()

    fig.add_trace(

        go.Scatter(

            x=df["Date"],

            y=df["RSI"],

            name="RSI"
        )

    )

    fig.add_hline(

        y=70,

        line_dash="dash"
    )

    fig.add_hline(

        y=30,

        line_dash="dash"
    )

    fig.update_layout(

        title="Relative Strength Index",

        height=350
    )

    st.plotly_chart(

        fig,

        use_container_width=True
    )


# ---------------------------------------
# MACD Chart
# ---------------------------------------

def plot_macd(df):

    macd = ta.trend.MACD(

        df["Close"]

    )

    df["MACD"] = macd.macd()

    df["SIGNAL"] = macd.macd_signal()

    fig = go.Figure()

    fig.add_trace(

        go.Scatter(

            x=df["Date"],

            y=df["MACD"],

            name="MACD"
        )

    )

    fig.add_trace(

        go.Scatter(

            x=df["Date"],

            y=df["SIGNAL"],

            name="Signal"
        )

    )

    fig.update_layout(

        title="MACD",

        height=350
    )

    st.plotly_chart(

        fig,

        use_container_width=True
    )
    
# ---------------------------------------
# Moving Averages
# ---------------------------------------

def plot_moving_averages(df, ticker):

    df["SMA20"] = df["Close"].rolling(20).mean()

    df["SMA50"] = df["Close"].rolling(50).mean()

    df["EMA20"] = df["Close"].ewm(span=20).mean()

    df["EMA50"] = df["Close"].ewm(span=50).mean()

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["Close"],
            name="Close"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["SMA20"],
            name="SMA20"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["SMA50"],
            name="SMA50"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["EMA20"],
            name="EMA20"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["EMA50"],
            name="EMA50"
        )
    )

    fig.update_layout(

        title=f"{ticker} Moving Averages",

        xaxis_title="Date",

        yaxis_title="Price",

        height=500

    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
    
# ---------------------------------------
# Bollinger Bands
# ---------------------------------------

def plot_bollinger(df, ticker):

    indicator = ta.volatility.BollingerBands(

        close=df["Close"],

        window=20,

        window_dev=2

    )

    df["Upper"] = indicator.bollinger_hband()

    df["Lower"] = indicator.bollinger_lband()

    df["Middle"] = indicator.bollinger_mavg()

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["Close"],
            name="Close"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["Upper"],
            name="Upper Band"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["Middle"],
            name="Middle Band"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["Lower"],
            name="Lower Band"
        )
    )

    fig.update_layout(

        title=f"{ticker} Bollinger Bands",

        xaxis_title="Date",

        yaxis_title="Price",

        height=500

    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )