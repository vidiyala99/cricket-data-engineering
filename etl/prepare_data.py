from data_cleaning import clean_matches
import pandas as pd

df_raw = pd.read_csv("data/raw/matches_extracted.csv")
df_cleaned = clean_matches(df_raw)
df_cleaned.to_csv("data/processed/matches_cleaned.csv", index=False)