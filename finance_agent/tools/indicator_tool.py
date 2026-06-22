from langchain.tools import tool

import yfinance as yf
import ta


@tool
def get_indicators(
    ticker: str
) -> dict:
    """
    Fetch the latest technical indicators
    for a given stock.

    Returns:
    {
        ticker,
        price,
        RSI,
        SMA20,
        SMA50,
        EMA20,
        EMA50,
        MACD,
        MACD_SIGNAL,
        RETURN,
        VOLATILITY,
        VOLUME
    }
    """

    try:

        df = yf.download(
            ticker,
            period="6mo",
            interval="1d",
            auto_adjust=True,
            progress=False
        )

        if df.empty:

            return {

                "ticker": ticker,

                "error": "No stock data found."

            }

        close = df["Close"].squeeze()

        volume = df["Volume"].squeeze()

        rsi = ta.momentum.RSIIndicator(
            close,
            window=14
        ).rsi()

        sma20 = ta.trend.SMAIndicator(
            close,
            window=20
        ).sma_indicator()

        sma50 = ta.trend.SMAIndicator(
            close,
            window=50
        ).sma_indicator()

        ema20 = ta.trend.EMAIndicator(
            close,
            window=20
        ).ema_indicator()

        ema50 = ta.trend.EMAIndicator(
            close,
            window=50
        ).ema_indicator()

        macd = ta.trend.MACD(
            close
        )

        returns = close.pct_change(
            fill_method=None
        )

        volatility = (
            returns
            .rolling(20)
            .std()
        )

        return {

            "ticker": ticker,

            "price": round(
                float(close.iloc[-1]),
                2
            ),

            "RSI": round(
                float(rsi.iloc[-1]),
                2
            ),

            "SMA20": round(
                float(sma20.iloc[-1]),
                2
            ),

            "SMA50": round(
                float(sma50.iloc[-1]),
                2
            ),

            "EMA20": round(
                float(ema20.iloc[-1]),
                2
            ),

            "EMA50": round(
                float(ema50.iloc[-1]),
                2
            ),

            "MACD": round(
                float(macd.macd().iloc[-1]),
                4
            ),

            "MACD_SIGNAL": round(
                float(
                    macd.macd_signal().iloc[-1]
                ),
                4
            ),

            "RETURN": round(
                float(
                    returns.iloc[-1]
                ),
                4
            ),

            "VOLATILITY": round(
                float(
                    volatility.iloc[-1]
                ),
                4
            ),

            "VOLUME": int(
                volume.iloc[-1]
            )

        }

    except Exception as e:

        return {

            "ticker": ticker,

            "error": str(e)

        }