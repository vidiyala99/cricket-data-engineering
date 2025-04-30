import psycopg2
import pandas as pd
import os
from datetime import datetime

conn = psycopg2.connect(
    dbname="cricket_data",
    user="postgres",
    password="root1234",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

with open("sql/create_top_powerplay_bowlers_view.sql", "r") as f:
    cursor.execute(f.read())
conn.commit()
print(" View 'top_powerplay_bowlers' created.")

df = pd.read_sql_query("SELECT * FROM top_powerplay_bowlers;", conn)

os.makedirs("output", exist_ok=True)
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
df.to_csv(f"output/Top_Powerplay_Bowlers_{timestamp}.csv", index=False)

print("\n Sample Records:")
print(df.head(5))

cursor.close()
conn.close()
