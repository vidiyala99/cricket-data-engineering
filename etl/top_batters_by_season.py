import pandas as pd

# Load CSVs
deliveries = pd.read_csv("data/raw/deliveries.csv")
matches = pd.read_csv("data/raw/matches.csv")

# Ensure correct types
deliveries['match_id'] = deliveries['match_id'].astype(int)
matches['id'] = matches['id'].astype(int)

# Merge on match_id
merged_df = pd.merge(deliveries, matches, left_on='match_id', right_on='id')

# Group by season & batsman and sum runs
season_batter_runs = (
    merged_df.groupby(['season', 'batsman'])['batsman_runs']
    .sum()
    .reset_index()
)

# Sort seasons ascending, batters descending by runs
season_batter_runs = season_batter_runs.sort_values(['season', 'batsman_runs'], ascending=[True, False])

# Get top 5 batters per season
top_5_batters = (
    season_batter_runs.groupby('season')
    .head(5)
    .reset_index(drop=True)
)

# 1-based indexing
top_5_batters.index = range(1, len(top_5_batters) + 1)

# Save to CSV
top_5_batters.to_csv("output/top_batters_multi_season.csv", index=False)

# Optional: Preview
print(top_5_batters)
