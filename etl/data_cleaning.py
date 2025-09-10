import pandas as pd
from etl.venue_mapping import venue_map
from etl.team_mapping import team_map
def clean_venue_names(df):
    df["venue"] = df["venue"].str.strip()
    df["venue"] = df["venue"].map(lambda x: venue_map.get(x, x))
    return df

def clean_matches(df):
    df = df.drop_duplicates()

    # Normalize venue names
    df = clean_venue_names(df)

    # Strip whitespace from team-related columns
    for col in ["team1", "team2", "winner", "toss_winner"]:
        df[col] = df[col].str.strip().map(lambda x: team_map.get(x, x))

    # Convert date column to datetime
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # Drop rows with missing critical fields
    df = df.dropna(subset=["team1", "team2", "winner", "venue", "date"])

    # Remove abandoned or no-result matches
    if "result" in df.columns:
        df = df[~df["result"].isin(["no result", "abandoned"])]

    return df