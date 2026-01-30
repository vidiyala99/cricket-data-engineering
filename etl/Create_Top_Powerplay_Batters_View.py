import psycopg2, pandas as pd, os
from datetime import datetime
from etl.db_utils import get_db_connection

conn = get_db_connection()
cursor = conn.cursor()

with open("sql/create_top_powerplay_batters_view.sql", "r") as f:
    cursor.execute(f.read())
conn.commit()
print(" View 'top_powerplay_batters' created.")

df = pd.read_sql_query("SELECT * FROM top_powerplay_batters;", conn)
os.makedirs("output", exist_ok=True)
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
df.to_csv(f"output/Top_Powerplay_Batters_{timestamp}.csv", index=False)

print(df.head(5))
cursor.close(); conn.close()
