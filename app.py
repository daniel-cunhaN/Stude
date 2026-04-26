import streamlit as st
from metodos.database import inicia_conexao

st.set_page_config(page_title="Stude", page_icon="📚", layout="centered")

con = inicia_conexao()

st.title("📚 Stude")

col_b, col_a = st.columns(2)

#if submit_button:
#    with conn.cursor() as cur: