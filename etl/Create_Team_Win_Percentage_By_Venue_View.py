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

# Execute the SQL file
with open("sql/create_team_win_percentage_by_venue.sql", "r") as file:
    sql_script = file.read()

cursor.execute(sql_script)
conn.commit()
print("\n View 'team_win_percentage_by_venue' created successfully!")

# Query the view
query = "SELECT * FROM team_win_percentage_by_venue;"
df = pd.read_sql_query(query, conn)

# Save to CSV
os.makedirs("output", exist_ok=True)
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
output_filename = f"output/Team_Win_Percentage_By_Venue_{timestamp}.csv"
df.to_csv(output_filename, index=False)

print(f"\n CSV saved as '{output_filename}'")
print("\n Sample records:")
print(df.head(5))

# Clean up
cursor.close()
conn.close()
print("\n Done.")
