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

# Step 2: Read and execute the SQL file to create the View
with open("sql/create_best_all_rounders_view.sql", "r") as file:
    sql_script = file.read()

cursor.execute(sql_script)
conn.commit()
print("\n View 'best_all_rounders_season' created successfully!")

# Step 3: Fetch data from the view
query = "SELECT * FROM best_all_rounders_season;"
df = pd.read_sql_query(query, conn)

# Step 4: Save to CSV in output/ folder
os.makedirs("output", exist_ok=True)
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
output_filename = f"output/Best_All_Rounders_{timestamp}.csv"
df.to_csv(output_filename, index=False)

print(f"\n CSV saved successfully as '{output_filename}'")

# Step 5: Show sample
print("\n Sample records from Best All Rounders View:")
print(df.head(5))

# Step 6: Close connection
cursor.close()
conn.close()

print("\n All Done!")
