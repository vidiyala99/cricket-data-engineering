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

# Step 2: Load matches_cricsheet.csv
matches = pd.read_csv("data/raw/matches_cricsheet.csv")

# Step 3: Parse date column correctly
matches['date'] = pd.to_datetime(matches['date'], dayfirst=True, errors='coerce')

# Step 4: Create matches table if not exists
create_matches_table_query = """
DROP TABLE IF EXISTS matches CASCADE;

CREATE TABLE matches (
    id INTEGER PRIMARY KEY,
    season INTEGER,
    city TEXT,
    date DATE,
    team1 TEXT,
    team2 TEXT,
    toss_winner TEXT,
    toss_decision TEXT,
    result TEXT,
    dl_applied INTEGER,
    winner TEXT,
    win_by_runs INTEGER,
    win_by_wickets INTEGER,
    player_of_match TEXT,
    venue TEXT,
    umpire1 TEXT,
    umpire2 TEXT,
    umpire3 TEXT  -- ← Must be included
);
"""
cursor.execute(create_matches_table_query)
conn.commit()

# Step 5: Insert or Update records (Upsert logic)
for idx, row in matches.iterrows():
    # Fix NaT dates by replacing with None
    row['date'] = None if pd.isna(row['date']) else row['date']

    insert_query = """
    INSERT INTO matches (id, season, city, date, team1, team2, toss_winner, toss_decision, result, dl_applied, winner, win_by_runs, win_by_wickets, player_of_match, venue, umpire1, umpire2, umpire3)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (id) DO NOTHING;
    """
    data = tuple(row)
    cursor.execute(insert_query, data)

conn.commit()

# Step 6: Verify a few rows
cursor.execute("SELECT * FROM matches LIMIT 5;")
sample_rows = cursor.fetchall()
print("\n Sample data from matches table:")
for r in sample_rows:
    print(r)

# Step 7: Close connection
cursor.close()
conn.close()

print("\n All Done! matches.csv successfully loaded into PostgreSQL!")
