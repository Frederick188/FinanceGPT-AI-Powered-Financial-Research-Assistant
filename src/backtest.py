import pandas as pd
import numpy as np

print("Loading predictions...")

# Load final dataset
df = pd.read_csv(
    "../data/final_dataset.csv"
)


# Create Actual Return

df["ACTUAL_RETURN"] = (
    df["Close"].shift(-1) - df["Close"]
) / df["Close"]

df = df.dropna()


# Load Trained Model Again


from xgboost import XGBRegressor

features = [
    "RSI",
    "SMA20",
    "SMA50",
    "EMA20",
    "EMA50",
    "MACD",
    "MACD_SIGNAL",
    "RETURN",
    "VOLATILITY",
    "Volume",
    "sentiment",
    "news_count"
]

# Same split used in train_model.py
split_index = int(
    len(df) * 0.8
)

train_df = df.iloc[:split_index]

test_df = df.iloc[split_index:]

X_train = train_df[features]

y_train = train_df["ACTUAL_RETURN"]

X_test = test_df[features]


# Train Model

model = XGBRegressor(
    n_estimators=300,
    learning_rate=0.05,
    max_depth=5,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42
)

model.fit(
    X_train,
    y_train
)


# Predict


test_df = test_df.copy()

test_df["PREDICTED_RETURN"] = (
    model.predict(X_test)
)

# Trading Strategy


test_df["POSITION"] = np.where(
    test_df["PREDICTED_RETURN"] > 0,
    1,
    0
)

# Strategy return

test_df["STRATEGY_RETURN"] = (
    test_df["POSITION"]
    * test_df["ACTUAL_RETURN"]
)


# Cumulative Returns


test_df["CUM_MARKET"] = (
    1 + test_df["ACTUAL_RETURN"]
).cumprod()

test_df["CUM_STRATEGY"] = (
    1 + test_df["STRATEGY_RETURN"]
).cumprod()


# Metrics


market_return = (
    test_df["CUM_MARKET"].iloc[-1] - 1
)

strategy_return = (
    test_df["CUM_STRATEGY"].iloc[-1] - 1
)

win_rate = (
    (
        np.sign(
            test_df["PREDICTED_RETURN"]
        )
        ==
        np.sign(
            test_df["ACTUAL_RETURN"]
        )
    )
    .mean()
)

sharpe_ratio = (
    test_df["STRATEGY_RETURN"].mean()
    /
    test_df["STRATEGY_RETURN"].std()
) * np.sqrt(252)


# Results


print("\nBACKTEST RESULTS\n")

print(
    f"Market Return: {market_return:.2%}"
)

print(
    f"Strategy Return: {strategy_return:.2%}"
)

print(
    f"Win Rate: {win_rate:.2%}"
)

print(
    f"Sharpe Ratio: {sharpe_ratio:.2f}"
)


# Save

test_df.to_csv(
    "../data/backtest_results.csv",
    index=False
)

print(
    "\nSaved backtest_results.csv"
)