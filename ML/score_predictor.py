import pandas as pd
import joblib
import sys, os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# === Add project root to sys.path ===
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# === Load Data ===
deliveries = pd.read_csv("../deliveries_with_season.csv")
matches = pd.read_csv("../matches_extracted.csv")

# === Normalize Team & Venue Names ===
from etl.team_mapping import team_map
from etl.venue_mapping import venue_map

deliveries["batting_team"] = deliveries["batting_team"].map(lambda x: team_map.get(x, x))
matches["team1"] = matches["team1"].map(lambda x: team_map.get(x, x))
matches["team2"] = matches["team2"].map(lambda x: team_map.get(x, x))
matches["toss_winner"] = matches["toss_winner"].map(lambda x: team_map.get(x, x))
matches["venue"] = matches["venue"].map(lambda x: venue_map.get(x, x))

# === Rename match ID column ===
matches.rename(columns={"id": "match_id"}, inplace=True)

# === Aggregate to Innings-Level ===
innings_df = deliveries.groupby(["match_id", "inning", "batting_team"]).agg({
    "total_runs": "sum",
    "player_dismissed": lambda x: x.notna().sum(),
    "over": "max"
}).reset_index().rename(columns={
    "total_runs": "total_runs",
    "player_dismissed": "wickets_lost",
    "over": "overs_completed"
})

# === Calculate Run Rate ===
innings_df["run_rate_so_far"] = innings_df["total_runs"] / (innings_df["overs_completed"] + 1)

# === Powerplay & Death Overs Flags ===
innings_df["powerplay_flag"] = (innings_df["overs_completed"] <= 6).astype(int)
innings_df["death_overs_flag"] = (innings_df["overs_completed"] >= 16).astype(int)

# === Merge Metadata ===
df = innings_df.merge(matches, on="match_id", how="left")

# === Identify Bowling Team ===
df["bowling_team"] = df.apply(
    lambda row: row["team2"] if row["batting_team"] == row["team1"] else row["team1"], axis=1
)

# === Toss Features ===
df["toss_winner_bin"] = (df["toss_winner"] == df["batting_team"]).astype(int)
df["toss_decision_bin"] = (df["toss_decision"] == "bat").astype(int)

# === Drop unused string columns ===
df.drop(columns=["city", "date", "result", "winner", "player_of_match", "umpire1", "umpire2", "umpire3"], inplace=True, errors="ignore")

# === One-Hot Encode Categorical Features ===
df = pd.get_dummies(df, columns=["batting_team", "bowling_team", "venue"], drop_first=True)

# === Define Features & Target ===
X = df.drop(columns=[
    "match_id", "inning", "total_runs", "team1", "team2", "toss_winner", "toss_decision"
])
y = df["total_runs"]

# === Final Sanity Check ===
assert X.select_dtypes(include="object").empty, "Non-numeric columns still present!"

# === Train/Test Split ===
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# === Train Model ===
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# === Evaluate ===
y_pred = model.predict(X_test)
print("📊 MAE:", round(mean_absolute_error(y_test, y_pred), 2))
print("📊 RMSE:", round(mean_squared_error(y_test, y_pred, squared=False), 2))
print("📊 R² Score:", round(r2_score(y_test, y_pred), 3))

# === Save Model ===
joblib.dump(model, "../ML/score_predictor.pkl")