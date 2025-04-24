import pandas as pd
import psycopg2

# Load CSV
df = pd.read_csv("output/top_batters_multi_season.csv")

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
create_db_query = """
CREATE TABLE IF NOT EXISTS top_batters_incremental (
    batsman TEXT,
    season INTEGER,
    batsman_runs INTEGER,
    PRIMARY KEY (batsman, season)
);
"""
cursor.execute(create_db_query)
conn.commit()

# Check if data is already loaded
cursor.execute("SELECT COUNT(*) FROM top_batters_incremental;")
existing_row_count = cursor.fetchone()[0]

if existing_row_count == len(df):
    print("✅ Table already loaded. Sample records:")
    cursor.execute("""
        SELECT batsman, season, batsman_runs
        FROM top_batters_incremental
        ORDER BY season ASC, batsman_runs DESC
        LIMIT 5;
    """)
    for row in cursor.fetchall():
        print(row)
else:
    print("⏳ Loading data into the table...")
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO top_batters_incremental (batsman, season, batsman_runs)
            VALUES (%s, %s, %s)
            ON CONFLICT (batsman, season)
            DO UPDATE SET batsman_runs = EXCLUDED.batsman_runs;
        """, (row['batsman'], int(row['season']), int(row['batsman_runs'])))
    conn.commit()
    print("✅ Data loaded successfully!")

cursor.close()
conn.close()
