import pandas as pd
import os
from datetime import datetime

# Step 1: Load player career summary
latest_summary_file = sorted(os.listdir('output'), reverse=True)
summary_file = None

for file in latest_summary_file:
    if file.startswith("batsman_statistics_") and file.endswith(".csv"):
        summary_file = f"output/{file}"
        break

if summary_file is None:
    raise FileNotFoundError("❌ No player career summary file found in output/ folder!")

player_stats = pd.read_csv(summary_file)

# Step 2: Filter players with at least 250 career runs
player_stats = player_stats[player_stats['batsman_runs'] >= 250]

# Step 3: Create new column BASRA = batting average + strike rate
player_stats['basra'] = player_stats['average'] + player_stats['strike_rate']

# Step 4: Sort players by BASRA in descending order
player_stats = player_stats.sort_values(by='basra', ascending=False)

# Step 5: Select important columns
player_stats = player_stats[['batsman', 'batsman_runs', 'average', 'strike_rate', 'best_score', 'basra']]

# Step 6: Reset index cleanly
player_stats = player_stats.reset_index(drop=True)
player_stats.index = range(1, len(player_stats) + 1)

# Step 7: Add report date
today_date = datetime.now().strftime("%Y-%m-%d")
player_stats['report_date'] = today_date

# Step 8: Save with timestamp
os.makedirs("output", exist_ok=True)

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
filename = f"output/Best_BASRA_Leaderboard_{timestamp}.csv"

player_stats.to_csv(filename, index=False)

print(f"\n✅ BASRA leaderboard saved to '{filename}'")

# Step 9: Show top 5 players
print("\n✅ Top 5 players by BASRA:")
print(player_stats.head(5))

# Step 10: Show number of records and time
now = datetime.now()
current_time = now.strftime("%I:%M %p")
print(f"\n✅ Saved {len(player_stats)} records at {current_time} ✅")
