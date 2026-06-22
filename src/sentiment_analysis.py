import pandas as pd
from transformers import pipeline

print("Loading dataset...")

news_df = pd.read_csv("../data/apple_news_data.csv")

print(f"Total articles: {len(news_df)}")

# ==========================
# Date Processing
# ==========================

news_df["date"] = pd.to_datetime(
    news_df["date"]
).dt.date

# ==========================
# Filter AAPL News
# ==========================

if "symbols" in news_df.columns:

    news_df = news_df[
        news_df["symbols"]
        .astype(str)
        .str.contains("AAPL", na=False)
    ]

print(f"AAPL articles: {len(news_df)}")

# ==========================
# Load FinBERT
# ==========================

print("Loading FinBERT...")

sentiment_model = pipeline(
    "sentiment-analysis",
    model="ProsusAI/finbert"
)

# ==========================
# Batch Inference
# ==========================

BATCH_SIZE = 64

headlines = (
    news_df["title"]
    .fillna("")
    .astype(str)
    .tolist()
)

scores = []

print("Running FinBERT...")

for i in range(
    0,
    len(headlines),
    BATCH_SIZE
):

    batch = headlines[
        i:i + BATCH_SIZE
    ]

    results = sentiment_model(
        batch,
        truncation=True
    )

    for result in results:

        label = result["label"]
        score = result["score"]

        if label == "positive":
            scores.append(score)

        elif label == "negative":
            scores.append(-score)

        else:
            scores.append(0)

    if i % 1000 == 0:
        print(
            f"Processed {i}/{len(headlines)}"
        )

news_df["sentiment"] = scores

print("\nSample Results:")

print(
    news_df[
        [
            "date",
            "title",
            "sentiment"
        ]
    ].head()
)

# ==========================
# Daily Aggregation
# ==========================

daily_sentiment = (
    news_df
    .groupby("date")
    .agg(
        sentiment=(
            "sentiment",
            "mean"
        ),
        news_count=(
            "sentiment",
            "count"
        )
    )
    .reset_index()
)

print("\nDaily Sentiment Sample:")

print(
    daily_sentiment.head()
)

daily_sentiment.to_csv(
    "../data/sentiment_data.csv",
    index=False
)

print(
    f"\nSaved {len(daily_sentiment)} sentiment days."
)