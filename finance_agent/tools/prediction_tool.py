import joblib
import pandas as pd

from langchain.tools import tool

from finance_agent.config import MODEL_PATH

print("Loading XGBoost model...")

model = joblib.load(MODEL_PATH)


@tool
def predict_return(
    RSI: float,
    SMA20: float,
    SMA50: float,
    EMA20: float,
    EMA50: float,
    MACD: float,
    MACD_SIGNAL: float,
    RETURN: float,
    VOLATILITY: float,
    VOLUME: float,
    sentiment: float,
    news_count: int
) -> dict:
    """
    Predict the next-day stock return using the trained XGBoost model.

    Returns:
        predicted_return : Expected next-day return (in %)
        signal           : STRONG BUY / BUY / HOLD / SELL / STRONG SELL
        confidence       : Confidence score (0-100)
    """

    try:

        X = pd.DataFrame([{
            "RSI": RSI,
            "SMA20": SMA20,
            "SMA50": SMA50,
            "EMA20": EMA20,
            "EMA50": EMA50,
            "MACD": MACD,
            "MACD_SIGNAL": MACD_SIGNAL,
            "RETURN": RETURN,
            "VOLATILITY": VOLATILITY,
            "Volume": VOLUME,
            "sentiment": sentiment,
            "news_count": news_count
        }])

        prediction = float(model.predict(X)[0])

        # ----------------------------------
        # Recommendation
        # ----------------------------------

        if prediction >= 0.01:
            signal = "BUY"

        elif prediction <= -0.01:   
            signal = "SELL"

        else:
            signal = "HOLD"

        # ----------------------------------
        # Confidence Score
        # ----------------------------------

        confidence = 0.0

        # Prediction Strength (35%)

        prediction_score = min(
            abs(prediction) / 0.02,
            1.0
        ) * 35

        confidence += prediction_score

        # News Sentiment (25%)

        sentiment_score = min(
            abs(sentiment),
            1.0
        ) * 25

        confidence += sentiment_score

        # Indicator Agreement (25%)

        agreement = 0

        if RSI > 60 or RSI < 40:
            agreement += 1

        if MACD > MACD_SIGNAL:
            agreement += 1

        if EMA20 > EMA50:
            agreement += 1

        if SMA20 > SMA50:
            agreement += 1

        indicator_score = (
            agreement / 4
        ) * 25

        confidence += indicator_score

        # Volatility Adjustment (15%)

        volatility_score = max(
            0,
            15 - (VOLATILITY * 300)
        )

        confidence += volatility_score

        confidence = round(
            min(confidence, 100),
            1
        )

        return {

            "predicted_return": round(
                prediction * 100,
                2
            ),

            "signal": signal,

            "confidence": confidence

        }

    except Exception as e:

        return {

            "error": str(e)

        }