import os

from dotenv import load_dotenv

load_dotenv()

FINNHUB_API_KEY = os.getenv(
    "FINNHUB_API_KEY"
)

MODEL_PATH = (
    "model/xgboost_model.pkl"
)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")