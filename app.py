import streamlit as st
from metodos.database import inicia_conexao

st.set_page_config(page_title="Stude", page_icon="📚", layout="centered")

con = inicia_conexao()

st.title("📚 Stude")