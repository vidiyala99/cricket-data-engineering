import pandas as pd
df = pd.read_csv("data/raw/matches_extracted.csv")
print(sorted(df["venue"].dropna().unique()))