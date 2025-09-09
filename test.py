import pandas as pd
df = pd.read_csv(r"C:\Users\aakas\Documents\cricket-data-engineering\data\raw\matches_extracted.csv")
print(df.columns.tolist())
print(df.head())