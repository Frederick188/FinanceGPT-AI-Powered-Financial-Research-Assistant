import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Sentiment-Aware Market Predictor",
    layout="wide"
)

st.title("📈 Sentiment-Aware Market Predictor")

st.markdown(
    """
    Predicting stock market movements using:

    - FinBERT Sentiment Analysis
    - Technical Indicators
    - XGBoost Forecasting
    - Backtesting Metrics
    """
)

# Load Data

final_df = pd.read_csv(
    "data/final_dataset.csv"
)

backtest_df = pd.read_csv(
    "data/backtest_results.csv"
)

importance_df = pd.read_csv(
    "data/feature_importance.csv"
)

# Dataset Overview

st.header("Dataset Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Rows",
        len(final_df)
    )

with col2:
    st.metric(
        "Avg Sentiment",
        round(
            final_df["sentiment"].mean(),
            3
        )
    )

with col3:
    st.metric(
        "News Records",
        int(
            final_df["news_count"].sum()
        )
    )

# Price Chart

st.header("Stock Price")

fig_price = px.line(
    final_df,
    x="Date",
    y="Close",
    title="AAPL Closing Price"
)

st.plotly_chart(
    fig_price,
    use_container_width=True
)


# Sentiment Chart


st.header("Daily Sentiment")

fig_sentiment = px.line(
    final_df,
    x="Date",
    y="sentiment",
    title="Daily FinBERT Sentiment"
)

st.plotly_chart(
    fig_sentiment,
    use_container_width=True
)

# Feature Importance

st.header("Feature Importance")

fig_importance = px.bar(
    importance_df,
    x="Importance",
    y="Feature",
    orientation="h",
    title="XGBoost Feature Importance"
)

st.plotly_chart(
    fig_importance,
    use_container_width=True
)


# Backtest Performance


st.header("Backtest Performance")

fig_backtest = px.line(
    backtest_df,
    y=[
        "CUM_MARKET",
        "CUM_STRATEGY"
    ],
    title="Strategy vs Market"
)

st.plotly_chart(
    fig_backtest,
    use_container_width=True
)


# Latest Signals


st.header("Latest Trading Signals")

latest = backtest_df.tail(20)

st.dataframe(
    latest[
        [
            "PREDICTED_RETURN",
            "ACTUAL_RETURN",
            "POSITION"
        ]
    ]
)


# Raw Data


st.header("Raw Dataset")

st.dataframe(
    final_df.head(50)
)