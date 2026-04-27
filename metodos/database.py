import psycopg2
import streamlit as st
import os

@st.cache_resource #mantém o cache de conexão do streamlit
def iniciar_conexao():
    psycopg2.connect(
        host=os.getenv("host"),
        user=os.getenv("user"),
        password=os.getenv("password"),
        dbname=os.getenv("dbname")
    )

con = inicia_conexao()

def criar_tabelas():
    with con.cursor() as cur:
        
        # 1. Tabela tags
        cur.execute("""
        CREATE TABLE IF NOT EXISTS tags(
            id SERIAL PRIMARY KEY,
            tag VARCHAR(50)
        );
        """)
        
        # 2. Tabela log_estudo
        cur.execute("""
        CREATE TABLE IF NOT EXISTS log_estudo(
            id SERIAL PRIMARY KEY,
            data DATE NOT NULL,
            minutos INT,
            pausas_min INT,
            tag_id INT REFERENCES tags(id)
        );
        """)
        
        # 3. Tabela metas
        cur.execute("""
        CREATE TABLE IF NOT EXISTS metas(
            id SERIAL PRIMARY KEY,
            tipo_meta VARCHAR(50),
            horas_alvo INT NOT NULL
        );
        """)
    con.commit()