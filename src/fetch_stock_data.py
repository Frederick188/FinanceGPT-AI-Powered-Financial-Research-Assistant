import yfinance as yf

ticker = "AAPL"

df = yf.download(
    ticker,
    start="2022-01-01",
    end="2025-12-31",
    auto_adjust=True
)

# Remove second level (AAPL)
if hasattr(df.columns, "droplevel"):
    try:
        df.columns = df.columns.droplevel(1)
    except:
        pass

df.reset_index(inplace=True)

print(df.head())

df.to_csv(
    "../data/stock_data.csv",
    index=False
)