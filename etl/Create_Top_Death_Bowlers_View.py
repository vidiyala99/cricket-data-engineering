import psycopg2
import pandas as pd
import os
from datetime import datetime

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="cricket_data",
    user="postgres",
    password="root1234",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Step 1: Create or replace the view
with open("sql/create_top_death_bowlers_view.sql", "r") as f:
    cursor.execute(f.read())
conn.commit()
print(" View 'top_death_bowlers' created.")

# Step 2: Query the view into pandas
df = pd.read_sql_query("SELECT * FROM top_death_bowlers;", conn)

# Step 3: Save to timestamped CSV
os.makedirs("output", exist_ok=True)
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
filename = f"output/Top_Death_Bowlers_{timestamp}.csv"
df.to_csv(filename, index=False)

# Step 4: Show sample records
print("\n Sample Records:")
print(df.head(5))

# Cleanup
cursor.close()
conn.close()
