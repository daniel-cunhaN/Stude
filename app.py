import streamlit as st
from metodos.database import iniciar_conexao, criar_tabelas

st.set_page_config(page_title="Stude", page_icon="📚", layout="centered")

con = iniciar_conexao()
criar_tabelas()

st.title("📚 Stude")

col_b, col_a = st.columns(2)

#if submit_button:
#    with conn.cursor() as cur: