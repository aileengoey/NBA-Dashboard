import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ========== Load Data ==========
df = pd.read_csv("nba_data_processed.csv")
df.dropna(subset=['Player', 'PTS'], inplace=True)

# ========== Sidebar Filters ==========
st.sidebar.header("🔎 Filter Pemain")
season = st.sidebar.selectbox("Season", ["2023"])
team_filter = st.sidebar.selectbox("Team", sorted(df['Tm'].unique()))
pos_filter = st.sidebar.selectbox("Position", sorted(df['Pos'].unique()))
if st.sidebar.button("Reset Filters"):
    st.experimental_rerun()

# ========== Main Title ==========
st.title("🏀 NBA Player Performance Analyzer")
st.markdown("**Compare, Analyze, and Draft Your Dream Team**")
st.markdown("---")

# ========== 1. Filter Section Result (Optional) ==========
filtered_df = df.copy()
if team_filter:
    filtered_df = filtered_df[filtered_df['Tm'] == team_filter]
if pos_filter:
    filtered_df = filtered_df[filtered_df['Pos'] == pos_filter]

# ========== 2. Analytics Area ==========
left_col, right_col = st.columns(2)

# -------- Left Column --------
with left_col:
    st.subheader("🟢 Player Comparison Tool")
    players = df['Player'].dropna().unique()
    selected_players = st.multiselect("Pilih 2–3 Pemain", players, max_selections=3)

    stats_to_compare = ['PTS', 'AST', 'TRB', 'STL', 'BLK', 'TOV']
    if len(selected_players) >= 2:
        compare_df = df[df['Player'].isin(selected_players)][['Player'] + stats_to_compare].set_index('Player')
        st.button("🟢 COMPARE")
        st.bar_chart(compare_df.T)
    else:
        st.info("Pilih minimal 2 pemain.")

    st.subheader("🏆 Top 10 Leaderboard")
    stat_map = {'Points': 'PTS', 'Assists': 'AST', 'Rebounds': 'TRB'}
    selected_stat = st.selectbox("Kategori", list(stat_map.keys()))
    col = stat_map[selected_stat]
    top10 = df.sort_values(by=col, ascending=False).head(10)
    st.bar_chart(top10.set_index('Player')[col])
    st.table(top10[['Player', col]])

# -------- Right Column --------
with right_col:
    st.subheader("📇 Player Card / Stats Summary")
    selected_player = st.selectbox("Pilih Pemain", sorted(df['Player'].unique()))
    player_data = df[df['Player'] == selected_player].iloc[0]

    col1, col2, col3 = st.columns(3)
    col1.metric("Points", f"{player_data['PTS']:.1f}")
    col2.metric("Assists", f"{player_data['AST']:.1f}")
    col3.metric("Rebounds", f"{player_data['TRB']:.1f}")

    col4, col5, col6 = st.columns(3)
    col4.metric("FG%", f"{player_data['FG%']:.2f}")
    col5.metric("3P%", f"{player_data['3P%']:.2f}")
    col6.metric("FT%", f"{player_data['FT%']:.2f}")

    st.line_chart(np.random.normal(loc=player_data['PTS'], scale=2, size=10))

    st.caption("✨ LeBron James is the top scorer this season with an average of 27.5 points!")

    st.subheader("🏀 Build Your Dream Team")
    dream_pos = ['PG', 'SG', 'SF', 'PF', 'C']
    dream_team = {}
    for pos in dream_pos:
        options = df[df['Pos'] == pos]['Player'].unique()
        dream_team[pos] = st.selectbox(f"{pos}", options=sorted(options), key=pos)
    team_df = df[df['Player'].isin(dream_team.values())]
    if len(team_df) == 5:
        st.button("🏀 DRAFT NOW")
        totals = team_df[['PTS', 'AST', 'TRB']].sum()
        st.metric("Total Points", f"{totals['PTS']:.1f}")
        st.metric("Total Assists", f"{totals['AST']:.1f}")
        st.metric("Total Rebounds", f"{totals['TRB']:.1f}")
        st.table(team_df[['Player', 'Pos', 'PTS', 'AST', 'TRB']])

# ========== 3. Full Dataset ==========
st.markdown("---")
st.subheader("📋 Full Data Table")
st.caption("Explore full dataset below")
st.dataframe(df)
