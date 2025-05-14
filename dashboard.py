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
        st.write(f"✅ Loaded: {files[0]}")
        return pd.read_csv(files[0])
    else:
        st.warning(f"⚠️ No file found for pattern: {pattern}")
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
basra_df = load_latest_csv("Best_BASRA_Leaderboard")
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
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🏅 BASRA & Top Batters",
    "💀 Death Overs Analysis",
    "⚡ Powerplay Analysis",
    "📊 Team-Level Metrics",
    "🔁 All-Rounders & Raw Stats",
    "🎯 Performance Insights"
])

# === Top Batters Tab ===
with tab1:
    st.subheader("🔥 Top Batters by BASRA")
    render_df(basra_df, "Top_BASRA")

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
