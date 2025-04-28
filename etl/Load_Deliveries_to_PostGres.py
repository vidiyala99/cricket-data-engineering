import pandas as pd
import psycopg2
import os

# Step 1: Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="cricket_data",
    user="postgres",
    password="root1234",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Step 2: Load deliveries.csv
deliveries = pd.read_csv("data/raw/deliveries.csv")

# Step 3: Create deliveries table if not exists
create_deliveries_table_query = """
CREATE TABLE IF NOT EXISTS deliveries (
    match_id INTEGER,
    inning INTEGER,
    batting_team TEXT,
    bowling_team TEXT,
    over INTEGER,
    ball INTEGER,
    batsman TEXT,
    non_striker TEXT,
    bowler TEXT,
    is_super_over INTEGER,
    wide_runs INTEGER,
    bye_runs INTEGER,
    legbye_runs INTEGER,
    noball_runs INTEGER,
    penalty_runs INTEGER,
    batsman_runs INTEGER,
    extra_runs INTEGER,
    total_runs INTEGER,
    player_dismissed TEXT,
    dismissal_kind TEXT,
    fielder TEXT
);
"""
cursor.execute(create_deliveries_table_query)
conn.commit()

# Step 4: Insert deliveries data
for idx, row in deliveries.iterrows():
    insert_query = """
    INSERT INTO deliveries (match_id, inning, batting_team, bowling_team, over, ball, batsman, non_striker, bowler, is_super_over, wide_runs, bye_runs, legbye_runs, noball_runs, penalty_runs, batsman_runs, extra_runs, total_runs, player_dismissed, dismissal_kind, fielder)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """
    cursor.execute(insert_query, tuple(row))

conn.commit()

# Step 5: Verify a few rows
cursor.execute("SELECT * FROM deliveries LIMIT 5;")
sample_rows = cursor.fetchall()
print("\n Sample data from deliveries table:")
for r in sample_rows:
    print(r)

# Step 6: Close connection
cursor.close()
conn.close()

print("\n All Done! deliveries.csv successfully loaded into PostgreSQL!")
