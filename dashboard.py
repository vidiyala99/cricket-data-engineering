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
    return pd.read_csv(files[0]) if files else pd.DataFrame()

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

death_batters_df = load_latest_csv("Top_Death_Batters")
death_bowlers_df = load_latest_csv("Top_Death_Bowlers")

pp_batters_df = load_latest_csv("Top_Powerplay_Batters")
pp_bowlers_df = load_latest_csv("Top_Powerplay_Bowlers")

venue_df = load_latest_csv("Team_Win_Percentage_By_Venue")
home_away_df = load_latest_csv("Team_Home_Away_Win_Percentage")
toss_df = load_latest_csv("Impact_of_Toss_Home_Games")

allrounders_df = load_latest_csv("Best_All_Rounders")
raw_batsman_df = load_latest_csv("batsman_statistics")

# === Tabs Layout ===
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏅 BASRA & Top Batters",
    "💀 Death Overs Analysis",
    "⚡ Powerplay Analysis",
    "📊 Team-Level Metrics",
    "🔁 All-Rounders & Raw Stats"
])

# === Tab 1: Top Batters ===
with tab1:
    st.subheader("🔥 Top Batters by BASRA")
    if not basra_df.empty:
        df = basra_df.sort_values("basra", ascending=False).head(10)
        render_df(df, "Top_BASRA")
    else:
        st.info("No BASRA leaderboard data found.")

    st.subheader("💥 Batters with 350+ Runs & 130+ SR")
    render_df(batters_df, "Top_Batters_350+130SR") if not batters_df.empty else st.info("No Top Batters data found.")

    st.subheader("🧹 Filtered Top Batters")
    render_df(batters_filtered_df, "Filtered_Top_Batters") if not batters_filtered_df.empty else st.info("No filtered batters data found.")

# === Tab 2: Death Overs Analysis ===
with tab2:
    st.subheader("💀 Top Death Batters")
    render_df(death_batters_df, "Top_Death_Batters") if not death_batters_df.empty else st.info("No death overs batting data found.")

    st.subheader("🪓 Top Death Bowlers")
    render_df(death_bowlers_df, "Top_Death_Bowlers") if not death_bowlers_df.empty else st.info("No death overs bowling data found.")

# === Tab 3: Powerplay Analysis ===
with tab3:
    st.subheader("🚀 Top Powerplay Batters")
    render_df(pp_batters_df, "Top_PP_Batters") if not pp_batters_df.empty else st.info("No powerplay batting data found.")

    st.subheader("🔫 Top Powerplay Bowlers")
    render_df(pp_bowlers_df, "Top_PP_Bowlers") if not pp_bowlers_df.empty else st.info("No powerplay bowling data found.")

# === Tab 4: Team Metrics ===
with tab4:
    st.subheader("🏟️ Team Win % by Venue")
    if not venue_df.empty:
        team_col = find_column(venue_df, "team")
        venue_col = find_column(venue_df, "venue")
        win_col = find_column(venue_df, "win_percentage") or find_column(venue_df, "Win%")

        if team_col and venue_col and win_col:
            team_list = venue_df[team_col].unique().tolist()
            selected_team = st.selectbox("Select team", sorted(team_list))
            team_data = venue_df[venue_df[team_col] == selected_team]
            st.bar_chart(team_data.set_index(venue_col)[win_col])
            render_df(team_data, f"{selected_team}_Win_By_Venue")
        else:
            st.warning("Required columns (team, venue, win_percentage) not found.")
    else:
        st.info("No venue win % data found.")

    st.subheader("🏠 Home vs Away Win %")
    render_df(home_away_df, "Home_Away_Win") if not home_away_df.empty else st.info("No home-away win % data found.")

    st.subheader("🧠 Toss Impact Analysis")
    render_df(toss_df, "Toss_Impact") if not toss_df.empty else st.info("No toss impact data found.")

# === Tab 5: All-Rounders & Raw ===
with tab5:
    st.subheader("🏏 Best All-Rounders")
    render_df(allrounders_df, "Best_All_Rounders") if not allrounders_df.empty else st.info("No all-rounder data found.")

    st.subheader("📋 Raw Batsman Statistics")
    render_df(raw_batsman_df, "Raw_Batsman_Stats") if not raw_batsman_df.empty else st.info("No batsman raw stats found.")
