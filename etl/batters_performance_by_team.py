import psycopg2
import pandas as pd
from dotenv import load_dotenv
import os
from datetime import datetime

# Load environment variables
load_dotenv()

# Database connection details
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

# Connect to PostgreSQL
conn = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)

# Function to fetch batter performance against team
def get_batter_performance_against_team():
    query = open('sql/batters_performance_by_team.sql', 'r').read()
    df = pd.read_sql(query, conn)

    # Adjust column indexing (1-based)
    df.index += 1

    # Save to CSV with timestamp
    output_filename = f'output/batter_performance_by_team_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    df.to_csv(output_filename, index=True)

    print("Batter Performance For Team (First 5 Records):\n", df.head())
    return df

# Main
if __name__ == '__main__':
    df_against_team = get_batter_performance_against_team()

    conn.close()
