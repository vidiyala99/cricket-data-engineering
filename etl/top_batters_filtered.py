import pandas as pd
import os
deliveries = pd.read_csv("data/raw/deliveries.csv")
matches = pd.read_csv('data/raw/matches.csv')
# Join deliveries with matches on match_id (common key)
merged_df = pd.merge(deliveries, matches, how='inner', left_on='match_id', right_on='id')
# Filter from 2016 onwards
filtered_df = merged_df[merged_df['season'] >= 2016]

# Group and sort by total runs
batting_stats = filtered_df.groupby('batsman')['batsman_runs'].sum().reset_index()
batting_stats = batting_stats.sort_values(by='batsman_runs', ascending=False)

print(batting_stats.head())
# Define output directory and file path
output_dir = "C:\\Users\\aakas\\Documents\\cricket_data_pipeline\\output"
output_file = os.path.join(output_dir, "top_batters_filtered.csv")

# Create directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Save to CSV
batting_stats.to_csv(output_file, index=False)
