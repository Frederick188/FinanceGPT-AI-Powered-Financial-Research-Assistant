import pandas as pd

df = pd.read_csv("../data/apple_news_data.csv")

print(df.columns)
print(df.head())
print(len(df))
