import psycopg2
import pandas as pd
import os
from datetime import datetime

# Step 1: Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="cricket_data",
    user="postgres",
    password="root1234",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Step 2: Read and execute SQL file to create the view
with open("sql/create_impact_of_toss_home_games_view.sql", "r") as file:
    sql_script = file.read()

cursor.execute(sql_script)
conn.commit()
print("\n View 'impact_of_toss_home_games' created successfully!")

# Step 3: Query the View into pandas
query = "SELECT * FROM impact_of_toss_home_games;"
df = pd.read_sql_query(query, conn)

# Step 4: Save to timestamped CSV
os.makedirs("output", exist_ok=True)
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
output_filename = f"output/Impact_of_Toss_Home_Games_{timestamp}.csv"
df.to_csv(output_filename, index=False)

print(f"\n CSV saved successfully as '{output_filename}'")

# Step 5: Show sample records
print("\n Sample records:")
print(df.head(5))

# Step 6: Close connections
cursor.close()
conn.close()

print("\n All Done!")
