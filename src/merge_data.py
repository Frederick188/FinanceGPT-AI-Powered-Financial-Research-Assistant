import pandas as pd

print("Reading technical indicators...")

tech_df = pd.read_csv(
    "../data/technical_indicators.csv"
)

print("Reading sentiment data...")

sentiment_df = pd.read_csv(
    "../data/sentiment_data.csv"
)

# ==========================
# Date Conversion
# ==========================

tech_df["Date"] = pd.to_datetime(
    tech_df["Date"]
)

sentiment_df["date"] = pd.to_datetime(
    sentiment_df["date"]
)

# ==========================
# Merge
# ==========================

print("Merging datasets...")

merged_df = pd.merge(
    tech_df,
    sentiment_df,
    left_on="Date",
    right_on="date",
    how="left"
)

# ==========================
# Fill Missing Sentiment
# ==========================

merged_df["sentiment"] = (
    merged_df["sentiment"]
    .fillna(0)
)

merged_df["news_count"] = (
    merged_df["news_count"]
    .fillna(0)
)

# ==========================
# Remove Rows Where Indicators
# Are Not Yet Available
# ==========================

merged_df = merged_df.dropna(
    subset=[
        "RSI",
        "SMA20",
        "SMA50",
        "MACD",
        "MACD_SIGNAL"
    ]
)

# ==========================
# Keep Useful Columns
# ==========================

final_df = merged_df[
    [
        "Date",
        "Close",
        "Volume",
        "RSI",
        "SMA20",
        "SMA50",
        "EMA20",
        "EMA50",
        "MACD",
        "MACD_SIGNAL",
        "RETURN",
        "VOLATILITY",
        "sentiment",
        "news_count"
    ]
]

print("\nFinal Dataset Sample:\n")

print(final_df.head())

print("\nRows:", len(final_df))

# ==========================
# Save
# ==========================

final_df.to_csv(
    "../data/final_dataset.csv",
    index=False
)

print(
    "\nFinal dataset saved to data/final_dataset.csv"
)