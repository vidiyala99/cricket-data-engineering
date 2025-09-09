import pandas as pd
from etl.venue_mapping import venue_map
def clean_venue_names(df):
    from etl.venue_mapping import venue_map
    df["venue"] = df["venue"].str.strip().map(lambda x: venue_map.get(x, x))
    return df
def clean_matches(df):
    df = df.drop_duplicates()
    df["venue"] = df["venue"].str.strip().map(lambda x: venue_map.get(x, x))
    for col in ["team1", "team2", "winner", "toss_winner"]:
        df[col] = df[col].str.strip()

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["team1", "team2", "winner", "venue", "date"])

    if "result" in df.columns:
        df = df[~df["result"].isin(["no result", "abandoned"])]

    return df