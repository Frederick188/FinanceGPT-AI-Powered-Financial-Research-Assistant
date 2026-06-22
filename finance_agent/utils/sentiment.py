from transformers import pipeline

print("Loading FinBERT...")

finbert = pipeline(
    "sentiment-analysis",
    model="ProsusAI/finbert"
)


def analyze_headlines(headlines):

    if len(headlines) == 0:
        return 0.0

    results = finbert(
        headlines,
        truncation=True,
        batch_size=16
    )

    scores = []

    for result in results:

        label = result["label"].lower()
        score = result["score"]

        if label == "positive":
            scores.append(score)

        elif label == "negative":
            scores.append(-score)

        else:
            scores.append(0)

    return sum(scores) / len(scores)