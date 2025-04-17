import streamlit as st
import pandas as pd
import plotly.express as px
import base64

# === Background Gambar ===
def add_bg_from_local(image_file):
    with open(image_file, "rb") as file:
        encoded = base64.b64encode(file.read()).decode()
        css = f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)

add_bg_from_local("lebron.jpg")

# === Overlay aman agar teks tetap jelas ===
st.markdown("""
    <style>
    .stApp::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        height: 100%;
        width: 100%;
        background-color: rgba(0, 0, 0, 0.5);
        z-index: 0;
    }
    .block-container {
        position: relative;
        z-index: 1;
    }
    </style>
""", unsafe_allow_html=True)

# === Load CSS Tambahan ===
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# === Load data ===
df = pd.read_csv("nba_data_processed.csv")
df['REB'] = df['ORB'] + df['DRB']

# === Warna tim (sampel) ===
team_colors = {
    "LAL": {"primary": "#552583"},
    "GSW": {"primary": "#FDB927"},
    "BOS": {"primary": "#007A33"},
    "MIA": {"primary": "#98002E"},
    "MIL": {"primary": "#00471B"},
}

# === Judul Aplikasi ===
col1, col2 = st.columns([1, 8])
with col1:
    st.image("logo NBA.jpg", width=50)
with col2:
    st.markdown("<h1 style='color: #fdd835; text-shadow: 2px 2px 4px #000;'>NBA Player Performance Analyzer</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: white; text-shadow: 1px 1px 3px #000;'>Explore Stats. Uncover Talent. Build the Ultimate Team.</p>", unsafe_allow_html=True)

# === Sidebar Filter ===
with st.sidebar:
    st.header("🎛️ Filter Pemain")
    season = st.selectbox("Season", options=["2023-2024"])
    all_teams = sorted(df["Tm"].dropna().astype(str).unique())
    all_positions = sorted(df["Pos"].dropna().astype(str).unique())
    selected_teams = st.multiselect("Team", options=all_teams)
    selected_positions = st.multiselect("Position", options=all_positions)
    apply_filters = st.button("✅ Apply Filter")

if "filtered_df" not in st.session_state:
    st.session_state.filtered_df = df.copy()

if apply_filters:
    filtered_df = df.copy()
    if selected_teams:
        filtered_df = filtered_df[filtered_df["Tm"].isin(selected_teams)]
    if selected_positions:
        filtered_df = filtered_df[filtered_df["Pos"].isin(selected_positions)]
    st.session_state.filtered_df = filtered_df

filtered_df = st.session_state.filtered_df if "filtered_df" in st.session_state else df.copy()

# === Layout Tab ===
tabs = st.tabs(["🆚 Comparison Tool", "🏆 Leaderboard", "📌 Filter by Team & Position", "📈 Player Insights", "⭐ Build Your Dream Team"])

# === Tab 1: Player Comparison ===
with tabs[0]:
    st.header("🔍 Player Comparison Tool")
    selected_players = st.multiselect("Pilih pemain untuk dibandingkan:", options=filtered_df["Player"].unique())

    if 2 <= len(selected_players) <= 3:
        compare_stats = filtered_df[filtered_df["Player"].isin(selected_players)]
        st.markdown("### ⚔️ Battle Card View")
        card_cols = st.columns(len(selected_players))
        for i, player in enumerate(selected_players):
            p = compare_stats[compare_stats["Player"] == player].iloc[0]
            team = p["Tm"]
            team_color = team_colors.get(team, {"primary": "#444"})["primary"]
            with card_cols[i]:
                html_card = f"""
                <div style='background-color:{team_color}; padding: 20px; border-radius: 12px;
                            box-shadow: 0 0 20px {team_color}; text-align: center; color: white;'>
                    <h3>{player}</h3>
                    <p>🏀 {p['PTS']} PTS</p>
                    <p>🎯 {p['AST']} AST</p>
                    <p>🛡️ {p['REB']} REB</p>
                    <div style='background:#f44336; height:10px; width:{p["PTS"]*3}px; border-radius:5px; margin-bottom:4px;'></div>
                    <div style='background:#2196f3; height:10px; width:{p["AST"]*5}px; border-radius:5px; margin-bottom:4px;'></div>
                    <div style='background:#4caf50; height:10px; width:{p["REB"]*4}px; border-radius:5px;'></div>
                </div>
                """
                st.markdown(html_card, unsafe_allow_html=True)
    elif len(selected_players) > 3:
        st.warning("Maksimal hanya bisa membandingkan 3 pemain.")
    else:
        st.info("Pilih minimal 2 pemain untuk membandingkan.")

# === Tab 2: Leaderboard ===
with tabs[1]:
    st.header("🏆 Top 10 Players by Category")
    category = st.selectbox("Pilih kategori statistik:", ["PTS", "AST", "REB", "STL", "BLK"])
    top_players = df.sort_values(by=category, ascending=False).head(10)
    fig = px.bar(top_players, x="Player", y=category, color="Player", title=f"Top 10 Players - {category}")
    st.plotly_chart(fig)
    st.dataframe(top_players[["Player", "Tm", category]])

# === Tab 3: Filter by Team & Position ===
with tabs[2]:
    st.header("📌 Pemain berdasarkan Tim & Posisi")
    team_choice = st.selectbox("Pilih Tim:", options=all_teams)
    pos_choice = st.selectbox("Pilih Posisi:", options=all_positions)
    filtered_team_pos = df[(df["Tm"] == team_choice) & (df["Pos"] == pos_choice)]
    st.dataframe(filtered_team_pos[["Player", "Pos", "Tm", "PTS", "AST", "REB"]])

# === Tab 4: Player Insights ===
with tabs[3]:
    st.header("📈 Player Insights")
    selected_player = st.selectbox("Pilih pemain:", options=df["Player"].unique())
    p = df[df["Player"] == selected_player].iloc[0]
    st.markdown(f"### {selected_player}")
    st.markdown(f"""
    **Team:** {p['Tm']}  
    **Position:** {p['Pos']}  
    **PTS:** {p['PTS']} | **AST:** {p['AST']} | **REB:** {p['REB']}
    """)
    fig = px.line(x=["PTS", "AST", "REB"], y=[p["PTS"], p["AST"], p["REB"]], markers=True, title="Stat Overview")
    st.plotly_chart(fig)

# === Tab 5: Build Your Dream Team ===
with tabs[4]:
    st.header("⭐ Build Your Dream Team")
    dream_team = st.multiselect("Pilih 5 pemain dari posisi berbeda:", options=df["Player"].unique(), max_selections=5)
    if len(dream_team) == 5:
        team_df = df[df["Player"].isin(dream_team)]
        avg_pts = team_df["PTS"].mean()
        avg_ast = team_df["AST"].mean()
        avg_reb = team_df["REB"].mean()
        st.success("### Rata-rata Performa Tim Impian")
        st.markdown(f"- 🏀 **Points:** {avg_pts:.1f}")
        st.markdown(f"- 🎯 **Assists:** {avg_ast:.1f}")
        st.markdown(f"- 🛡️ **Rebounds:** {avg_reb:.1f}")
        st.dataframe(team_df[["Player", "Pos", "PTS", "AST", "REB"]])
    elif len(dream_team) > 5:
        st.error("Maksimal 5 pemain saja!")
    else:
        st.info("Pilih 5 pemain untuk membentuk tim impianmu.")
