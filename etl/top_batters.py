import pandas as pd
import os

# Load the dataset
df = pd.read_csv("C:\\Users\\aakas\\Documents\\cricket_data_pipeline\\data\\raw\\deliveries.csv")

# Group by batsman and calculate total runs
batting_stats = df.groupby('batsman')['batsman_runs'].sum().reset_index()
batting_stats = batting_stats.sort_values(by='batsman_runs', ascending=False)

# Define output directory and file path
output_dir = "C:\\Users\\aakas\\Documents\\cricket_data_pipeline\\output"
output_file = os.path.join(output_dir, "top_batters.csv")

# Create directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Save to CSV
batting_stats.to_csv(output_file, index=False)

print(f"File saved to: {output_file}")
