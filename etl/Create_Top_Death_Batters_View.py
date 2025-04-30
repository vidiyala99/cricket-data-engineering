import psycopg2
import pandas as pd
import os
from datetime import datetime

# PostgreSQL connection
conn = psycopg2.connect(
    dbname="cricket_data",
    user="postgres",
    password="root1234",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Step 1: Create view from SQL
with open("sql/create_top_death_batters_view.sql", "r") as f:
    cursor.execute(f.read())
conn.commit()
print(" View 'top_death_batters' created.")

# Step 2: Query the view
df = pd.read_sql_query("SELECT * FROM top_death_batters;", conn)

# Step 3: Save as timestamped CSV
os.makedirs("output", exist_ok=True)
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
filename = f"output/Top_Death_Batters_{timestamp}.csv"
df.to_csv(filename, index=False)

# Step 4: Preview
print("\n Sample Records:")
print(df.head(5))

# Cleanup
cursor.close()
conn.close()
