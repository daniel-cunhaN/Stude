import psycopg2
import streamlit as st
import os

@st.cache_resource #mantém o cache de conexão do streamlit para que o usuário nao precise recarregar a pagina
# a cada botão clicado
def iniciar_conexao():
    return psycopg2.connect(
        host=os.getenv("host"),
        user=os.getenv("user"),
        password=os.getenv("password"),
        dbname=os.getenv("dbname")
    )

def criar_tabelas(con): 
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

        # 4. Cria tag default para previnir crash no primeiro save
        cur.execute("""
        INSERT INTO tags (id, tag) 
        VALUES (1, 'Geral') 
        ON CONFLICT (id) DO NOTHING;
        """)
        
    con.commit()

def obter_tags(con):
    with con.cursor() as cur:
        # Pede para o banco: "Me dê o texto e o ID de todas as tags, em ordem alfabética"
        cur.execute("SELECT tag, id FROM tags ORDER BY tag;")
        
        # Pega todas as respostas do banco
        resultados = cur.fetchall() 
        
        # Cria um dicionário vazio
        tradutor_dinamico = {}
        
        # Preenche o dicionário com o que veio do banco
        for linha in resultados:
            nome_da_tag = linha[0] # Ex: "Matemática"
            id_da_tag = linha[1]   # Ex: 2
            tradutor_dinamico[nome_da_tag] = id_da_tag
            
        return tradutor_dinamico