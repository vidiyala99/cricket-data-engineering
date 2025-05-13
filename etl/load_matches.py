import pandas as pd
import psycopg2
from psycopg2.extras import execute_batch
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Database connection parameters from .env file
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

def load_csv_to_postgresql(csv_file, table_name):
    # Connect to PostgreSQL database
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cur = conn.cursor()

    # Load CSV data into a DataFrame
    df = pd.read_csv(csv_file)

    # Generate SQL query for inserting data
    insert_query = f"""
    INSERT INTO {table_name} (id, season, city, date, team1, team2, toss_winner, toss_decision,
                              result, dl_applied, winner, win_by_runs, win_by_wickets,
                              player_of_match, venue, umpire1, umpire2, umpire3)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    # Convert DataFrame rows to list of tuples
    data_tuples = list(df.itertuples(index=False, name=None))

    # Insert data in batches for efficiency
    execute_batch(cur, insert_query, data_tuples)

    # Commit and close connection
    conn.commit()
    cur.close()
    conn.close()

    print(f"✅ Successfully loaded data from '{csv_file}' to PostgreSQL table '{table_name}'.")
csv_file = "data/raw/matches_extracted.csv"
table_name = "matches"
load_csv_to_postgresql(csv_file, table_name)
