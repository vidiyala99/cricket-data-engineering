import pandas as pd
import psycopg2

conn = psycopg2.connect(
    dbname="cricket_data",
    user="postgres",
    password="root1234",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()
#query to create table in postgresql
create_db_query="""CREATE TABLE IF NOT EXISTS top_batters_2016 (
    batsman TEXT,
    batsman_runs INTEGER
);
"""
cursor.execute(create_db_query)
conn.commit()

print("Table created successfully!")
#loading the output generated to a dataframe
df = pd.read_csv("output/top_batters_filtered.csv")
#displaying the head of the dataframe
print(df.head())
#inserting into the table row by row
for index, row in df.iterrows():
    cursor.execute(
        "INSERT INTO top_batters_2016 (batsman, batsman_runs) VALUES (%s, %s)",
        (row['batsman'], row['batsman_runs'])
    )
print("Data inserted into the table")
conn.commit() 
# Close
cursor.close()
conn.close()
