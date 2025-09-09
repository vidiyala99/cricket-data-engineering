import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, classification_report
from etl.data_cleaning import clean_matches

# === Load and Clean Match Data ===
df = pd.read_csv("data/raw/matches_extracted.csv")
df = clean_matches(df)

# === Label Engineering ===
df["match_winner"] = (df["winner"] == df["team1"]).astype(int)
df["toss_winner_bin"] = (df["toss_winner"] == df["team1"]).astype(int)
df["toss_decision_bin"] = df["toss_decision"].map({"bat": 0, "field": 1})

# === Feature Engineering Functions ===
def get_recent_form(team, match_date, matches_df, n=5):
    recent_matches = matches_df[
        ((matches_df["team1"] == team) | (matches_df["team2"] == team)) &
        (matches_df["date"] < match_date)
    ].sort_values("date", ascending=False).head(n)
    return recent_matches[recent_matches["winner"] == team].shape[0]

def get_venue_win_rate(team, venue, matches_df):
    venue_matches = matches_df[
        ((matches_df["team1"] == team) | (matches_df["team2"] == team)) &
        (matches_df["venue"] == venue)
    ]
    total = venue_matches.shape[0]
    wins = venue_matches[venue_matches["winner"] == team].shape[0]
    return wins / total if total > 0 else 0.5

def get_team_strength(team, match_date, matches_df, n=10):
    recent_matches = matches_df[
        ((matches_df["team1"] == team) | (matches_df["team2"] == team)) &
        (matches_df["date"] < match_date)
    ].sort_values("date", ascending=False).head(n)
    wins = recent_matches[recent_matches["winner"] == team].shape[0]
    return wins / n if n > 0 else 0.5

# === Apply Feature Engineering ===
df["team1_strength"] = df.apply(lambda row: get_team_strength(row["team1"], row["date"], df), axis=1)
df["team2_strength"] = df.apply(lambda row: get_team_strength(row["team2"], row["date"], df), axis=1)
df["venue_win_rate_team1"] = df.apply(lambda row: get_venue_win_rate(row["team1"], row["venue"], df), axis=1)
df["venue_win_rate_team2"] = df.apply(lambda row: get_venue_win_rate(row["team2"], row["venue"], df), axis=1)
df["recent_form_team1"] = df.apply(lambda row: get_recent_form(row["team1"], row["date"], df), axis=1)
df["recent_form_team2"] = df.apply(lambda row: get_recent_form(row["team2"], row["date"], df), axis=1)

# === Feature Set ===
features = [
    "team1_strength",
    "team2_strength",
    "venue_win_rate_team1",
    "venue_win_rate_team2",
    "toss_winner_bin",
    "toss_decision_bin",
    "recent_form_team1",
    "recent_form_team2"
]
X = df[features]
y = df["match_winner"]

# === Train-Test Split ===
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# === Train Model ===
model = XGBClassifier(
    n_estimators=100,
    max_depth=4,
    learning_rate=0.1,
    use_label_encoder=False,
    eval_metric="logloss"
)
model.fit(X_train, y_train)

# === Evaluate Model ===
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"✅ Accuracy: {round(accuracy * 100, 2)}%")
print("📊 Classification Report:\n", classification_report(y_test, y_pred))

# === Save Model ===
joblib.dump(model, "match_outcome_model.pkl")
print("💾 Model saved as match_outcome_model.pkl")

# === Test Prediction Block ===
sample_input = pd.DataFrame([{
    "team1_strength": 0.7,
    "team2_strength": 0.5,
    "venue_win_rate_team1": 0.65,
    "venue_win_rate_team2": 0.45,
    "toss_winner_bin": 1,
    "toss_decision_bin": 1,
    "recent_form_team1": 4,
    "recent_form_team2": 2
}])

sample_pred = model.predict(sample_input)[0]
sample_prob = model.predict_proba(sample_input)[0][1]

print("🔮 Predicted Winner:", "Team 1" if sample_pred == 1 else "Team 2")
print("📈 Win Probability for Team 1:", round(sample_prob * 100, 2), "%")