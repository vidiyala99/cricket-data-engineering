import psycopg2
import pandas as pd
import os
from datetime import datetime
from etl.db_utils import get_db_connection

conn = get_db_connection()
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
