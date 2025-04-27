import pandas as pd
import os
from datetime import datetime
import psycopg2

# Step 1: Load player career summary
latest_summary_file = sorted(os.listdir('output'), reverse=True)
summary_file = None

for file in latest_summary_file:
    if file.startswith("batsman_statistics_") and file.endswith(".csv"):
        summary_file = f"output/{file}"
        break

if summary_file is None:
    raise FileNotFoundError("No player career summary file found in output/ folder!")

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

print(f"\n BASRA leaderboard saved to '{filename}'")

# Step 9: Show top 5 players
print("\n Top 5 players by BASRA:")
print(player_stats.head(5))

# Step 10: Show number of records and time
now = datetime.now()
current_time = now.strftime("%I:%M %p")
print(f"\n Saved {len(player_stats)} records at {current_time}")

# -------------------------
# Step 11: Load into PostgreSQL
# -------------------------

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="cricket_data",
    user="postgres",
    password="root1234",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Create table if not exists
create_table_query = """
CREATE TABLE IF NOT EXISTS best_basra_leaderboard (
    batsman TEXT PRIMARY KEY,
    batsman_runs INTEGER,
    average FLOAT,
    strike_rate FLOAT,
    best_score INTEGER,
    basra FLOAT,
    report_date DATE
);
"""
cursor.execute(create_table_query)
conn.commit()

# 🚀 Insert or Update records (UPSERT)
for idx, row in player_stats.iterrows():
    insert_query = """
    INSERT INTO best_basra_leaderboard (batsman, batsman_runs, average, strike_rate, best_score, basra, report_date)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (batsman)
    DO UPDATE SET
        batsman_runs = EXCLUDED.batsman_runs,
        average = EXCLUDED.average,
        strike_rate = EXCLUDED.strike_rate,
        best_score = EXCLUDED.best_score,
        basra = EXCLUDED.basra,
        report_date = EXCLUDED.report_date;
    """
    data = (
        row['batsman'],
        row['batsman_runs'],
        row['average'],
        row['strike_rate'],
        row['best_score'],
        row['basra'],
        row['report_date']
    )
    cursor.execute(insert_query, data)

conn.commit()

# Verify a sample
cursor.execute("SELECT * FROM best_basra_leaderboard LIMIT 5;")
sample_rows = cursor.fetchall()
print("\n Sample data from best_basra_leaderboard table:")
for r in sample_rows:
    print(r)

# Close connection
cursor.close()
conn.close()

print("\n🏆 All Done Successfully!")
