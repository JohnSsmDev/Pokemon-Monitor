import streamlit as st
import pandas as pd
import sqlite3

st.set_page_config(layout="wide")

st.title("📈 Pokémon Market Radar")

conn = sqlite3.connect("market.db")

df = pd.read_sql_query(
    "SELECT * FROM prices",
    conn
)

# =========================
# HISTÓRICO
# =========================
st.subheader("Histórico de preços")

st.dataframe(df)

# =========================
# RANKING
# =========================
st.subheader("🏆 Ranking de preço médio")

avg = (
    df.groupby("name")["price"]
    .mean()
    .sort_values(ascending=False)
)

st.bar_chart(avg)

# =========================
# GRÁFICO
# =========================
st.subheader("📊 Evolução histórica")

selected = st.selectbox(
    "Carta",
    df["name"].unique()
)

chart_data = df[df["name"] == selected]

st.line_chart(chart_data["price"])

# =========================
# ÚLTIMOS PREÇOS
# =========================
st.subheader("🔥 Últimos preços")

latest = (
    df.groupby("name")
    .last()
)

st.dataframe(latest)