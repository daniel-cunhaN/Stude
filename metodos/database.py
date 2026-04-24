import psycopg2
import streamlit as st
import os

db_url = os.getenv("")

@st.cache_resource #mantém o cache de conexão do streamlit
def inicia_conexao():
    psycopg2.connect(
        host="aws-1-sa-east-1.pooler.supabase.com",
        user="postgres.qlmtpejkoqlepgvvemgu",
        password="J9Cynx99J4SZbtD2",
        dbname="postgres"
    )