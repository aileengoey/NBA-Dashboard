import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv("nba_data_processed.csv")
df['REB'] = df['ORB'] + df['DRB'] 

# Title
st.title("🏀 NBA Player Performance Analyzer")
st.markdown("### *Compare, Analyze, and Draft Your Dream Team*")

# Sidebar - Filters
st.sidebar.header("🎛️ Filter Pemain")
season = st.sidebar.selectbox("Season", options=["2023-2024"])
teams = st.sidebar.multiselect("Team", options=sorted(df["Tm"].dropna().astype(str).unique()), default=None)
positions = st.sidebar.multiselect("Position", options=sorted(df["Pos"].dropna().astype(str).unique()), default=None)


# Apply filters
filtered_df = df.copy()
if teams:
    filtered_df = filtered_df[filtered_df["Tm"].isin(teams)]
if positions:
    filtered_df = filtered_df[filtered_df["Pos"].isin(positions)]

# Spacing
st.markdown("---")

# 🔍 Player Comparison Tool
st.subheader("🔍 Player Comparison Tool")
st.markdown("Pilih 2–3 pemain untuk dibandingkan:")

selected_players = st.multiselect("Pilih pemain", filtered_df["Player"].unique(), max_selections=3)

if 2 <= len(selected_players) <= 3:
    compare_stats = filtered_df[filtered_df["Player"].isin(selected_players)]
    st.plotly_chart(px.line(compare_stats.set_index("Player")[["PTS", "AST", "REB", "STL", "BLK"]].T,
                            title="Perbandingan Statistik"))
    st.dataframe(compare_stats.set_index("Player")[["PTS", "AST", "REB", "STL", "BLK"]])

st.markdown("---")

# 🏆 Top 10 Leaderboard
st.subheader("🏆 Top 10 Leaderboard by Category")
category = st.selectbox("Pilih Kategori", options=["PTS", "AST", "REB", "STL", "BLK"])
top_10 = filtered_df.sort_values(by=category, ascending=False).head(10)

st.plotly_chart(px.bar(top_10, x="Player", y=category, title=f"Top 10 Pemain berdasarkan {category}"))
st.dataframe(top_10[["Player", "Tm", "Pos", category]])

st.markdown("---")

# 📇 Player Insights Card
st.subheader("📇 Player Insights Card")
selected_card = st.selectbox("Pilih Pemain", options=filtered_df["Player"].unique())
player_info = filtered_df[filtered_df["Player"] == selected_card].iloc[0]

st.markdown(f"**{player_info['Player']}** | {player_info['Pos']} | {player_info['Tm']} | Age: {player_info['Age']}")
st.markdown(f"- PPG: {player_info['PTS']}")
st.markdown(f"- AST: {player_info['AST']}")
st.markdown(f"- REB: {player_info.get('ORB', 0) + player_info.get('DRB', 0)}")

# Trend line dummy (karena tidak ada data per game di file)
st.line_chart(pd.DataFrame({
    "Game 1": [player_info["PTS"] - 2],
    "Game 2": [player_info["PTS"]],
    "Game 3": [player_info["PTS"] + 1],
    "Game 4": [player_info["PTS"] - 1],
    "Game 5": [player_info["PTS"]],
}).T)

st.markdown("---")

# 🧩 Build Your Dream Team
st.subheader("🧩 Build Your Dream Team")
st.markdown("Pilih pemain untuk setiap posisi:")

positions_required = ["PG", "SG", "SF", "PF", "C"]
dream_team = {}

for pos in positions_required:
    players_for_pos = filtered_df[filtered_df["Pos"] == pos]["Player"].unique()
    selected = st.selectbox(f"Pilih {pos}", options=players_for_pos, key=pos)
    dream_team[pos] = selected

# Tampilkan ringkasan performa tim
if all(dream_team.values()):
    team_df = filtered_df[filtered_df["Player"].isin(dream_team.values())]
    avg_stats = team_df[["PTS", "AST", "REB", "STL", "BLK"]].mean()
    
    st.markdown("### 🧠 Total Rata-rata Tim Impian")
    st.write(avg_stats)

st.markdown("---")

# 📊 Full Data Table
st.subheader("📊 Explore Full Dataset Below")
st.caption("Explore full dataset with filters applied.")
st.dataframe(filtered_df)

# 📌 Insight text singkat
top_scorer = df.sort_values(by="PTS", ascending=False).iloc[0]
st.markdown(f"💡 **Insight:** {top_scorer['Player']} is the top scorer this season with an average of {top_scorer['PTS']} points!")

