import pandas as pd
import os
from datetime import datetime

# Step 1: Generate timestamp (date + time for uniqueness)
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")

# Step 2: Load deliveries data
deliveries = pd.read_csv("data/raw/deliveries.csv")

# Step 3: Calculate stats
# 3.1 Total runs
total_runs = deliveries.groupby('batsman')['batsman_runs'].sum().reset_index()

# 3.2 Balls faced (excluding wides)
balls_faced = deliveries[deliveries['wide_runs'] == 0].groupby('batsman').size().reset_index(name='balls_faced')

# 3.3 Dismissals
dismissals = deliveries[deliveries['player_dismissed'].notna()].groupby('player_dismissed').size().reset_index(name='dismissals')
dismissals.rename(columns={'player_dismissed': 'batsman'}, inplace=True)

# 3.4 Best individual score
best_scores = (
    deliveries.groupby(['match_id', 'batsman'])['batsman_runs']
    .sum()
    .reset_index()
    .groupby('batsman')['batsman_runs']
    .max()
    .reset_index(name='best_score')
)

# Step 4: Merge all stats
batsman_stats = total_runs.merge(balls_faced, on='batsman', how='left') \
                          .merge(dismissals, on='batsman', how='left') \
                          .merge(best_scores, on='batsman', how='left')

# Step 5: Fill NaNs for dismissals
batsman_stats['dismissals'] = batsman_stats['dismissals'].fillna(0)

# Step 6: Calculate Average and Strike Rate
batsman_stats['average'] = batsman_stats.apply(
    lambda row: row['batsman_runs'] / row['dismissals'] if row['dismissals'] != 0 else row['batsman_runs'], axis=1
)
batsman_stats['strike_rate'] = (batsman_stats['batsman_runs'] / batsman_stats['balls_faced']) * 100

# Step 7: Prepare final output
final_batsman_stats = batsman_stats[['batsman', 'batsman_runs', 'average', 'strike_rate', 'best_score']]
final_batsman_stats = final_batsman_stats.sort_values(by='batsman_runs', ascending=False)
final_batsman_stats = final_batsman_stats.reset_index(drop=True)
final_batsman_stats.index = range(1, len(final_batsman_stats) + 1)

# Step 8: Save results
# Ensure output folder exists
os.makedirs("output", exist_ok=True)

filename = f"output/batsman_statistics_{timestamp}.csv"
final_batsman_stats.to_csv(filename, index=False)

print(f"\n Batsman statistics saved to '{filename}'")

# Step 9: Read back and show a small sample
saved_df = pd.read_csv(filename)
print("\n Sample data from saved CSV:")
print(saved_df.head(5))

#print("\n All Done Successfully!")
