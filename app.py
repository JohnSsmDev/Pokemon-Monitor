import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

conn = sqlite3.connect("precos.db", check_same_thread=False)
cursor = conn.cursor()

st.title("📊 Radar Pokémon Pro")

df = pd.read_sql("SELECT * FROM historico ORDER BY id DESC", conn)

if not df.empty:

    st.subheader("🔥 Top oportunidades")

    top = df.sort_values("score", ascending=False).head(20)

    st.dataframe(top)

    st.subheader("📈 Evolução de preço")

    nome = st.selectbox("Escolha carta", df["nome"].unique())

    hist = df[df["nome"] == nome].tail(30)

    plt.plot(hist["preco"])
    st.pyplot(plt)

else:
    st.warning("Sem dados ainda.")