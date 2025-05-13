import psycopg2
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# PostgreSQL connection details (from .env)
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# SQL file path
SQL_FILE_PATH = "sql/top_batters_by_season.sql"

def load_top_batters():
    connection = None
    cursor = None
    try:
        # Establish PostgreSQL connection
        connection = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = connection.cursor()

        # Check if the SQL file exists
        if not os.path.exists(SQL_FILE_PATH):
            print(f"❌ SQL file '{SQL_FILE_PATH}' not found. Please create it first.")
            return

        # Read the SQL query from the file
        with open(SQL_FILE_PATH, 'r') as file:
            sql_query = file.read().strip()

        # Execute the query
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        # Convert results to DataFrame
        top_batters_df = pd.DataFrame(rows, columns=columns)

        # Display results
        print("\n✅ Top Batters by Season:")
        print(top_batters_df)

        # Save results to CSV
        output_path = "output/top_batters_multi_season.csv"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        top_batters_df.to_csv(output_path, index=False)
        print(f"\n✅ Results saved to {output_path}")

    except Exception as error:
        print(f"❌ Error: {error}")

    finally:
        # Safely close cursor and connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()
            print("🔌 PostgreSQL connection closed.")

if __name__ == "__main__":
    load_top_batters()

