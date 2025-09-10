import streamlit as st
import pandas as pd
import glob
import os

st.set_page_config(page_title="🏏 Cricket Analytics Dashboard", layout="wide")
st.title("🏏 Cricket Analytics Dashboard")

# === Helper Functions ===
@st.cache_data
def load_latest_csv(pattern):
    files = sorted(glob.glob(os.path.join("output", f"{pattern}*.csv")), reverse=True)
    if files:
        return pd.read_csv(files[0])
    else:
        return pd.DataFrame()

def find_column(df, target):
    for col in df.columns:
        if col.strip().lower() == target.strip().lower():
            return col
    return None

def render_df(df, label="data"):
    df_display = df.copy()
    df_display.index = range(1, len(df_display) + 1)
    st.dataframe(df_display, use_container_width=True)
    st.download_button(f"⬇️ Download {label}", df.to_csv(index=False), f"{label}.csv", "text/csv")

# === Load All Data ===
basra_df = load_latest_csv("BASRA_Leaderboard_With_Teams")
batters_df = load_latest_csv("Top_Batters_350runs_130sr")
batters_filtered_df = load_latest_csv("top_batters_filtered")
bowlers_df = load_latest_csv("Top_Bowlers_10wickets_Economy")

# === Load All Additional Data ===
death_batters_df = load_latest_csv("Top_Death_Batters")
death_bowlers_df = load_latest_csv("Top_Death_Bowlers")
pp_batters_df = load_latest_csv("Top_Powerplay_Batters")
pp_bowlers_df = load_latest_csv("Top_Powerplay_Bowlers")
venue_df = load_latest_csv("Team_Win_Percentage_By_Venue")
home_away_df = load_latest_csv("Team_Home_Away_Win_Percentage")
toss_df = load_latest_csv("Impact_of_Toss_Home_Games")
allrounders_df = load_latest_csv("Best_All_Rounders")
raw_batsman_df = load_latest_csv("batsman_statistics")
batter_performance_by_team_df = load_latest_csv("batter_performance_by_team")
batter_performance_against_team_df = load_latest_csv("batter_performance_against_team")

# === Tabs Layout ===
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "🏅 BASRA & Top Batters",
    "💀 Death Overs Analysis",
    "⚡ Powerplay Analysis",
    "📊 Team-Level Metrics",
    "🔁 All-Rounders & Raw Stats",
    "🎯 Performance Insights",
    "🔮 Match Outcome Prediction",
    "📚 Match History & Summary"  # ✅ New tab
])
# === Top Batters Tab ===
with tab1:
    st.subheader("🔥 Top Batters by BASRA (with Team)")

    if not basra_df.empty:
        # Optional team filter
        teams = basra_df['team'].dropna().unique()
        selected_team = st.selectbox("🔍 Filter by Team", options=["All"] + sorted(teams.tolist()))

        if selected_team != "All":
            filtered_basra_df = basra_df[basra_df['team'] == selected_team]
        else:
            filtered_basra_df = basra_df

        render_df(filtered_basra_df, "Top_BASRA_With_Teams")
    else:
        st.warning("No BASRA leaderboard with team data available.")

# === Death Overs Analysis ===
with tab2:
    st.subheader("💀 Top Death Batters")
    render_df(death_batters_df, "Top_Death_Batters")

    st.subheader("🪓 Top Death Bowlers")
    render_df(death_bowlers_df, "Top_Death_Bowlers")

# === Powerplay Analysis ===
with tab3:
    st.subheader("🚀 Top Powerplay Batters")
    render_df(pp_batters_df, "Top_PP_Batters")

    st.subheader("🔫 Top Powerplay Bowlers")
    render_df(pp_bowlers_df, "Top_PP_Bowlers")

# === Team-Level Metrics ===
with tab4:
    st.subheader("🏟️ Team Win % by Venue")
    render_df(venue_df, "Win_By_Venue")

# === All-Rounders & Raw Stats ===
with tab5:
    st.subheader("🏏 Best All-Rounders")
    render_df(allrounders_df, "Best_All_Rounders")

    st.subheader("📋 Raw Batsman Statistics")
    render_df(raw_batsman_df, "Raw_Batsman_Stats")

# === Performance Insights ===
with tab6:
    st.subheader("🎯 Batter Performance by Team")
    render_df(batter_performance_by_team_df, "Batter_Performance_By_Team")

    st.subheader("🎯 Batter Performance Against Team")
    render_df(batter_performance_against_team_df, "Batter_Performance_Against_Team")
# === Match Outcome Prediction ===
with tab7:
    st.subheader("🔮 Predict Match Outcome")

    # === Load Match History and Venue Data ===
    from etl.data_cleaning import clean_matches, clean_venue_names
    from etl.venue_mapping import venue_map
    from etl.team_mapping import team_map  # ✅ NEW: Team normalization

    matches_path = "data/raw/matches_extracted.csv"
    try:
        matches_df = pd.read_csv(matches_path)
        matches_df = clean_matches(matches_df)

        venue_df = clean_venue_names(venue_df)
        venue_df["team"] = venue_df["team"].str.strip().map(lambda x: team_map.get(x, x))  # ✅ Normalize team names

        basra_df["team"] = basra_df["team"].str.strip().map(lambda x: team_map.get(x, x))  # ✅ Normalize dropdown teams

        # === Detect Unmapped Venues (Debugging Aid) ===
        unmapped = venue_df[~venue_df["venue"].isin(set(venue_map.values()))]["venue"].unique()
        if len(unmapped) > 0:
            st.warning(f"🕵️ Unmapped venues detected: {unmapped}")
    except Exception as e:
        st.error(f"❌ Failed to load or clean match data: {e}")
        st.stop()

    if matches_df.empty:
        st.error("❌ Match data is empty. Please check the CSV file.")
        st.stop()

    # === Build Dropdowns ===
    teams = sorted(set(basra_df['team'].dropna().unique()))
    venues = sorted(set(venue_df['venue'].dropna().unique())) if 'venue' in venue_df.columns else []

    col1, col2 = st.columns(2)
    with col1:
        team1 = st.selectbox("🏏 Team 1", options=teams)
    with col2:
        team2 = st.selectbox("🏏 Team 2", options=[t for t in teams if t != team1])

    toss_winner = st.selectbox("🎲 Toss Winner", options=[team1, team2])
    toss_decision = st.selectbox("🧭 Toss Decision", options=["bat", "field"])
    venue = st.selectbox("📍 Venue", options=venues)

    # === Feature Functions ===
    def get_recent_form(team_name, df, n=5):
        recent_matches = df[
            (df["team1"] == team_name) | (df["team2"] == team_name)
        ].sort_values("date", ascending=False).head(n)
        return recent_matches[recent_matches["winner"] == team_name].shape[0]

    def get_team_strength(team_name, df, n=10):
        recent_matches = df[
            (df["team1"] == team_name) | (df["team2"] == team_name)
        ].sort_values("date", ascending=False).head(n)
        wins = recent_matches[recent_matches["winner"] == team_name].shape[0]
        return wins / n if n > 0 else 0.5

    def get_venue_win_rate(team_name, venue, venue_df):
        row = venue_df[
            (venue_df["team"] == team_name) & (venue_df["venue"] == venue)
        ]
        if not row.empty and "win_percentage" in row.columns:
            return row["win_percentage"].values[0]
        return 0.5  # fallback if no data

    # === Compute Features ===
    recent_form_team1 = get_recent_form(team1, matches_df)
    recent_form_team2 = get_recent_form(team2, matches_df)
    team1_strength = get_team_strength(team1, matches_df)
    team2_strength = get_team_strength(team2, matches_df)
    venue_win_rate_team1 = get_venue_win_rate(team1, venue, venue_df)
    venue_win_rate_team2 = get_venue_win_rate(team2, venue, venue_df)

    # === Load Model ===
    import joblib
    try:
        model = joblib.load("ML/match_outcome_model.pkl")
    except FileNotFoundError:
        st.error("❌ Model file not found. Please ensure match_outcome_model.pkl is present in the ML folder.")
        st.stop()

    # === Generate Feature Vector ===
    features_df = pd.DataFrame([{
        "team1_strength": team1_strength,
        "team2_strength": team2_strength,
        "venue_win_rate_team1": venue_win_rate_team1,
        "venue_win_rate_team2": venue_win_rate_team2,
        "toss_winner_bin": 1 if toss_winner == team1 else 0,
        "toss_decision_bin": 1 if toss_decision == "field" else 0,
        "recent_form_team1": recent_form_team1,
        "recent_form_team2": recent_form_team2
    }])

    # === Optional: Display Feature Inputs for Debugging
    st.write("🧬 Feature Inputs", features_df)

    # === Predict Outcome ===
    prediction = model.predict(features_df)[0]
    probability = model.predict_proba(features_df)[0][1]
    predicted_team = team1 if prediction == 1 else team2

    # === Display Results ===
    st.metric(label=f"Win Probability for {team1}", value=f"{round(probability * 100, 2)}%")
    st.write(f"🔮 Predicted Winner: **{predicted_team}**")

with tab8:
    st.subheader("📚 Match History & Summary")

    # === Team Selection ===
    col1, col2 = st.columns(2)
    with col1:
        team1 = st.selectbox("🏏 Team 1", options=teams, key="summary_team1")
    with col2:
        team2 = st.selectbox("🏏 Team 2", options=[t for t in teams if t != team1], key="summary_team2")

    venue_filter = st.selectbox("📍 Filter by Venue (optional)", options=["All"] + venues)

    # === Filter Matches ===
    filtered_matches = matches_df[
        ((matches_df["team1"] == team1) & (matches_df["team2"] == team2)) |
        ((matches_df["team1"] == team2) & (matches_df["team2"] == team1))
    ]

    if venue_filter != "All":
        filtered_matches = filtered_matches[filtered_matches["venue"] == venue_filter]

    # === Head-to-Head Summary ===
    total_matches = filtered_matches.shape[0]
    team1_wins = filtered_matches[filtered_matches["winner"] == team1].shape[0]
    team2_wins = filtered_matches[filtered_matches["winner"] == team2].shape[0]

    st.markdown(f"**🆚 Head-to-Head Record ({total_matches} matches):**")
    st.write(f"- {team1} wins: {team1_wins}")
    st.write(f"- {team2} wins: {team2_wins}")
    if total_matches > 0:
        win_pct = round((team1_wins / total_matches) * 100, 2)
        st.write(f"- {team1} win %: {win_pct}%")

    # === Recent Form ===
    def recent_form(team, df, n=5):
        recent = df[
            (df["team1"] == team) | (df["team2"] == team)
        ].sort_values("date", ascending=False).head(n)
        wins = recent[recent["winner"] == team].shape[0]
        return wins

    st.markdown("**📈 Recent Form (Last 5 Matches):**")
    st.write(f"- {team1}: {recent_form(team1, matches_df)} wins")
    st.write(f"- {team2}: {recent_form(team2, matches_df)} wins")

    # === Venue Performance ===
    def venue_win_rate(team, venue, venue_df):
        row = venue_df[(venue_df["team"] == team) & (venue_df["venue"] == venue)]
        if not row.empty and "win_percentage" in row.columns:
            return round(row["win_percentage"].values[0], 2)
        return None

    if venue_filter != "All":
        st.markdown(f"**🏟️ Venue Performance at {venue_filter}:**")
        team1_rate = venue_win_rate(team1, venue_filter, venue_df)
        team2_rate = venue_win_rate(team2, venue_filter, venue_df)
        if team1_rate is not None:
            st.write(f"- {team1}: {team1_rate}% win rate")
        if team2_rate is not None:
            st.write(f"- {team2}: {team2_rate}% win rate")

    # === Last 3 Encounters ===
    st.markdown("**🕰️ Last 3 Encounters:**")
    last_3 = filtered_matches.sort_values("date", ascending=False).head(3)
    if last_3.empty:
        st.write("No match history available.")
    else:
        for _, row in last_3.iterrows():
            st.write(f"- {row['date'].date()} at {row['venue']}: Winner - {row['winner']}")