from datetime import datetime, timedelta

import finnhub

from langchain.tools import tool

from finance_agent.config import FINNHUB_API_KEY
from finance_agent.utils.sentiment import analyze_headlines


client = finnhub.Client(
    api_key=FINNHUB_API_KEY
)


@tool
def get_news_sentiment(
    ticker: str
) -> dict:
    """
    Fetch recent news for a stock and
    analyze the headlines using FinBERT.

    Returns:
        {
            ticker,
            sentiment,
            news_count,
            headlines
        }
    """

    try:

        end_date = datetime.today()

        start_date = (
            end_date -
            timedelta(days=7)
        )

        news = client.company_news(
            ticker,
            _from=start_date.strftime("%Y-%m-%d"),
            to=end_date.strftime("%Y-%m-%d")
        )

        if not news:

            return {

                "ticker": ticker,

                "sentiment": 0.0,

                "news_count": 0,

                "headlines": []

            }

        headlines = []

        for article in news:

            headline = article.get(
                "headline",
                ""
            )

            if headline:

                headlines.append(
                    headline
                )

        sentiment = analyze_headlines(
            headlines
        )

        return {

            "ticker": ticker,

            "sentiment": round(
                float(sentiment),
                4
            ),

            "news_count": len(
                headlines
            ),

            "headlines": headlines[:10]

        }

    except Exception as e:

        return {

            "ticker": ticker,

            "sentiment": 0.0,

            "news_count": 0,

            "headlines": [],

            "error": str(e)

        }