import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

API_KEY = "MQ0SZB1IC0CX5PDI"

if not API_KEY:
    print("API key not found.")
    exit()

TICKER = "AAPL"

# YYYYMMDDTHHMM format
START_DATE = "20240101T0000"
END_DATE = "20260101T0000"

url = (
    "https://www.alphavantage.co/query"
    "?function=NEWS_SENTIMENT"
    f"&tickers={TICKER}"
    f"&time_from={START_DATE}"
    f"&time_to={END_DATE}"
    "&limit=1000"
    f"&apikey={API_KEY}"
)

print(f"Fetching news for {TICKER}...")

response = requests.get(url)
data = response.json()

if "feed" not in data:
    print("No news returned.")
    print(data)
    exit()

news_list = []

for article in data["feed"]:
    news_list.append({
        "date": pd.to_datetime(
            article["time_published"],
            format="%Y%m%dT%H%M%S"
        ).date(),
        "headline": article.get("title", ""),
        "summary": article.get("summary", ""),
        "source": article.get("source", ""),
        "url": article.get("url", "")
    })

news_df = pd.DataFrame(news_list)

print(news_df.head())

print("\nEarliest Date:", news_df["date"].min())
print("Latest Date:", news_df["date"].max())
print("Articles:", len(news_df))

news_df.to_csv(
    "../data/news_data.csv",
    index=False
)

print("\nNews saved to data/news_data.csv")