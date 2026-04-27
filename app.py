import streamlit as st
from metodos.database import iniciar_conexao, criar_tabelas # <-- Updated here!

st.set_page_config(page_title="Stude", page_icon="📚", layout="centered")

# Connect using the new name
con = iniciar_conexao()
criar_tabelas()

st.title("📚 Stude")

with st.form("form_novo_estudo"):
    st.subheader("Registrar Sessão de Estudo")
    
    col_a, col_b = st.columns(2)
    with col_a:
        minutos_estudo = st.number_input("Minutos Estudados", min_value=1, step=1)
    with col_b:
        minutos_pausa = st.number_input("Minutos de Pausa", min_value=0, step=1)
        
    data_estudo = st.date_input("Data do Estudo")
    tag_escolhida = st.number_input("ID da Tag (ex: 1)", min_value=1, step=1)
    
    submit_button = st.form_submit_button("Salvar Sessão")

if submit_button:
    with con.cursor() as cur:
        cur.execute("""
            INSERT INTO log_estudo (data, minutos, pausas_min, tag_id)
            VALUES (%s, %s, %s, %s)
        """, (data_estudo, minutos_estudo, minutos_pausa, tag_escolhida))
        
    con.commit() 
    st.success("Sessão salva com sucesso! 🚀")