import pandas as pd
import psycopg2
from psycopg2 import sql
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# PostgreSQL connection setup
def connect_postgresql():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        print("✅ Connected to PostgreSQL database successfully.")
        return conn
    except Exception as e:
        print(f"❌ Error connecting to PostgreSQL: {e}")
        exit(1)

# Path to extracted CSV
deliveries_csv = "data/raw/deliveries_with_season.csv"
if not os.path.exists(deliveries_csv):
    print(f"❌ CSV file not found: {deliveries_csv}")
    exit(1)

# Load CSV with Pandas (ensuring text type for problematic columns)
df = pd.read_csv(deliveries_csv, dtype={"inning": str, "season": str})

# Connect to PostgreSQL
conn = connect_postgresql()
cur = conn.cursor()

# Create deliveries_updated table (if not exists) with complete schema
create_table_query = '''
CREATE TABLE IF NOT EXISTS deliveries_updated (
    match_id VARCHAR(100),
    season VARCHAR(10),
    inning VARCHAR(100),
    batting_team VARCHAR(200),
    bowling_team VARCHAR(200),
    over INTEGER,
    ball INTEGER,
    batsman VARCHAR(200),
    non_striker VARCHAR(200),
    bowler VARCHAR(200),
    is_super_over INTEGER,
    wide_runs INTEGER,
    bye_runs INTEGER,
    legbye_runs INTEGER,
    noball_runs INTEGER,
    penalty_runs INTEGER,
    batsman_runs INTEGER,
    extra_runs INTEGER,
    total_runs INTEGER,
    player_dismissed VARCHAR(200),
    dismissal_kind VARCHAR(200),
    fielder VARCHAR(500)
);
'''
cur.execute(create_table_query)
conn.commit()
print("✅ 'deliveries_updated' table with complete schema ensured in database.")

# Load data using batch insertion (optimized)
insert_query = '''
INSERT INTO deliveries_updated (match_id, season, inning, batting_team, bowling_team, 
                                over, ball, batsman, non_striker, bowler, is_super_over, 
                                wide_runs, bye_runs, legbye_runs, noball_runs, penalty_runs, 
                                batsman_runs, extra_runs, total_runs, 
                                player_dismissed, dismissal_kind, fielder)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
'''
data_tuples = list(df.itertuples(index=False, name=None))
cur.executemany(insert_query, data_tuples)

conn.commit()
print("✅ Data loaded successfully into 'deliveries_updated' table.")

# Close connection
cur.close()
conn.close()
print("🔌 PostgreSQL connection closed.")

