import pandas as pd

# Load the data
df = pd.read_csv("data/raw/deliveries_with_season.csv")

# === Filter: First innings only ===
df_innings1 = df[df["inning"] == "1st innings"]

# === Filter: Specific team (e.g., Sunrisers Hyderabad) ===
df_srh = df_innings1[df_innings1["batting_team"] == "Sunrisers Hyderabad"]

# === Filter: Powerplay overs (1 to 6) ===
df_powerplay = df_srh[df_srh["over"] <= 6]

# === View sample rows ===
print(df_powerplay.head(10))