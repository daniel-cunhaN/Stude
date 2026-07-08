import sqlite3
import streamlit as st
import os

@st.cache_resource #mantém o cache de conexão do streamlit para que o usuário nao precise recarregar a pagina
# a cada botão clicado
def iniciar_conexao():
    # Conecta ao arquivo local de banco de dados SQLite
    con = sqlite3.connect("stude_local.db", check_same_thread=False)
    con.execute("PRAGMA foreign_keys = ON;")
    return con

def criar_tabelas(con): 
    try:
        cur = con.cursor()
        # 1. Tabela tags
        cur.execute("""
        CREATE TABLE IF NOT EXISTS tags(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tag VARCHAR(50) UNIQUE
        );
        """)
        
        # 2. Tabela log_estudo
        cur.execute("""
        CREATE TABLE IF NOT EXISTS log_estudo(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data DATE NOT NULL,
            hora TEXT,
            minutos INT,
            pausas_min INT,
            tag_id INT REFERENCES tags(id)
        );
        """)
        
        # Migração: Adicionar coluna 'hora' para usuários com bancos de dados antigos
        try:
            cur.execute("ALTER TABLE log_estudo ADD COLUMN hora TEXT;")
        except Exception:
            pass
        
        # 3. Tabela metas
        cur.execute("""
        CREATE TABLE IF NOT EXISTS metas(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo_meta VARCHAR(50),
            horas_alvo INT NOT NULL
        );
        """)

            #4. Tabela notas
        cur.execute("""
        CREATE TABLE IF NOT EXISTS notas (
            id INT PRIMARY KEY,
            texto TEXT
        );
        """)
        
        # Garante que existe pelo menos uma linha para ser editada no app.py
        cur.execute("INSERT OR IGNORE INTO notas (id, texto) VALUES (1, '');")

        #5. Tabela Sessão
        cur.execute("""
        CREATE TABLE IF NOT EXISTS sessao(
        id INT PRIMARY KEY,
        hora_inicial TIMESTAMP,
        hora_final TIMESTAMP); """)

        # 6. Tabela Inventário
        cur.execute("""
        CREATE TABLE IF NOT EXISTS inventario (
            id INT PRIMARY KEY,
            trofeus INT DEFAULT 0
        );
        """)
        cur.execute("INSERT OR IGNORE INTO inventario (id, trofeus) VALUES (1, 0);")

        # 7. Tabela Streak Status
        cur.execute("""
        CREATE TABLE IF NOT EXISTS streak_status (
            id INT PRIMARY KEY,
            streak_atual INT DEFAULT 0,
            maior_streak INT DEFAULT 0,
            congelamentos_ativos INT DEFAULT 0,
            ultima_atividade DATE
        );
        """)
        cur.execute("INSERT OR IGNORE INTO streak_status (id, streak_atual, maior_streak, congelamentos_ativos, ultima_atividade) VALUES (1, 0, 0, 0, NULL);")

        # 8. Tabela Historico Conquistas
        cur.execute("""
        CREATE TABLE IF NOT EXISTS historico_conquistas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo_meta VARCHAR(50),
            periodo VARCHAR(50),
            data_conquista DATE
        );
        """)

        con.commit()
    except Exception as e:
        con.rollback()
        st.error(f"Erro ao inicializar banco de dados: {e}")

def obter_tags(con):
    try:
        cur = con.cursor()
        cur.execute("SELECT tag, id FROM tags ORDER BY tag;")
        resultados = cur.fetchall() 
        
        tradutor_dinamico = {}
        for linha in resultados:
            nome_da_tag = linha[0]
            id_da_tag = linha[1]
            tradutor_dinamico[nome_da_tag] = id_da_tag
            
        return tradutor_dinamico
    except Exception as e:
        con.rollback()
        return {}   