import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error
)

from xgboost import XGBRegressor

print("Loading dataset...")

df = pd.read_csv(
    "../data/final_dataset.csv"
)


# Create Target
# Next Day Return

df["TARGET"] = (
    df["Close"].shift(-1) - df["Close"]
) / df["Close"]

df = df.dropna()

print(f"Rows available: {len(df)}")


# Features


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

X = df[features]

y = df["TARGET"]


# Train Test Split


split_index = int(
    len(df) * 0.8
)

X_train = X.iloc[:split_index]

X_test = X.iloc[split_index:]

y_train = y.iloc[:split_index]

y_test = y.iloc[split_index:]

print(
    f"Training rows: {len(X_train)}"
)

print(
    f"Testing rows: {len(X_test)}"
)


# Model


print("Training XGBoost...")

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


# Prediction


predictions = model.predict(
    X_test
)


# Metrics


mae = mean_absolute_error(
    y_test,
    predictions
)

rmse = np.sqrt(
    mean_squared_error(
        y_test,
        predictions
    )
)

print("\nResults")

print(
    f"MAE: {mae:.6f}"
)

print(
    f"RMSE: {rmse:.6f}"
)


# Prediction Table


results = pd.DataFrame({
    "Actual": y_test.values,
    "Predicted": predictions
})

print("\nSample Predictions")

print(
    results.head(10)
)


# Feature Importance

importance = pd.DataFrame({
    "Feature": features,
    "Importance": model.feature_importances_
})

importance = (
    importance
    .sort_values(
        by="Importance",
        ascending=False
    )
)

print("\nFeature Importance")

print(importance)

# Save Results

results.to_csv(
    "../data/predictions.csv",
    index=False
)

importance.to_csv(
    "../data/feature_importance.csv",
    index=False
)

print(
    "\nSaved predictions.csv"
)

print(
    "Saved feature_importance.csv"
)


joblib.dump(
    model,
    "../model/xgboost_model.pkl"
)

print("Model saved.")