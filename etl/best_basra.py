import psycopg2
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from urllib.parse import quote
import argparse

# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

# -----------------------------
# CLI arguments for flexibility
# -----------------------------
parser = argparse.ArgumentParser()
parser.add_argument("--mode", choices=["replace", "append"], default="replace",
                    help="Mode to write to DB: replace (default) or append")
args = parser.parse_args()

# -----------------------------
# Function: Load DataFrame to PostgreSQL
# -----------------------------
def load_to_postgres(df, table_name="basra_leaderboard_with_teams", if_exists="replace"):
    """Loads a DataFrame into a PostgreSQL table."""
    print(f"🔄 Loading data to PostgreSQL table: {table_name} with mode = {if_exists}")
    
    password_encoded = quote(DB_PASSWORD)
    engine = create_engine(
        f'postgresql+psycopg2://{DB_USER}:{password_encoded}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    )

    df.to_sql(
        name=table_name,
        con=engine,
        if_exists=if_exists,
        index=False
    )

    print(f"✅ Successfully loaded {len(df)} rows into table: {table_name}")

# -----------------------------
# Step 1: Read SQL from file
# -----------------------------
with open("sql/generate_basra_leaderboard.sql", "r") as file:
    sql_query = file.read()

# -----------------------------
# Step 2: Execute SQL and Fetch
# -----------------------------
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)
cursor = conn.cursor()

cursor.execute(sql_query)
rows = cursor.fetchall()
columns = [desc[0] for desc in cursor.description]

cursor.close()
conn.close()

# -----------------------------
# Step 3: Save to DataFrame and CSV
# -----------------------------
df = pd.DataFrame(rows, columns=columns)
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
output_path = f"output/BASRA_Leaderboard_With_Teams_{timestamp}.csv"
df.to_csv(output_path, index=False)

print(f"\n🏏 BASRA leaderboard saved to: {output_path}")
print("\nTop 5 rows:\n", df.head())

# -----------------------------
# Step 4: Load into PostgreSQL
# -----------------------------
load_to_postgres(df, if_exists=args.mode)
