import requests


def get_ticker(query: str):

    url = "https://query2.finance.yahoo.com/v1/finance/search"

    params = {
        "q": query,
        "quotesCount": 1,
        "newsCount": 0
    }

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:

        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=5
        )

        data = response.json()

        quotes = data.get("quotes", [])

        if quotes:

            return quotes[0]["symbol"]

    except Exception:

        pass

    return None