import pandas as pd
import psycopg2
from metodos.database import iniciar_conexao
import sys

con = iniciar_conexao()
try:
    df = pd.read_csv('limpeza_dados/dadosLimpos.csv', encoding='utf-8')
except Exception as e:
    print(f"ERRO ao ler CSV: {e}")
    sys.exit(1)

# Preparando os dados para inserção múltipla (lista de tuplas)
dados_para_inserir = list(zip(
    df['minutos'], 
    df['pausas_min'], 
    df['tag_id'], 
    df['data']
))

try:
    with con.cursor() as cur:
        # Usamos IDs explícitos que batem com a ordem gerada no limparDados.py
        # 1: Revisão, 2: Web, 3: Sistemas Variados, 4: Infraestrutura, 5: Dados
        tags_fixas = [
            (1, 'Revisão'), 
            (2, 'Web'), 
            (3, 'Sistemas Variados'), 
            (4, 'Infraestrutura'), 
            (5, 'Dados')
        ]

        # Inserção com IDs explícitos para garantir compatibilidade com o CSV
        cur.executemany(
            "INSERT INTO tags (id, tag) VALUES (%s, %s) ON CONFLICT (id) DO UPDATE SET tag = EXCLUDED.tag", 
            tags_fixas
        )

        # Ajusta a sequência para que novos inserts (automáticos) não falhem
        cur.execute("SELECT setval('tags_id_seq', (SELECT MAX(id) FROM tags))")

        print("Tags injetadas com sucesso")

        # 2. Insere dados na tabela principal
        query = """
            INSERT INTO log_estudo (minutos, pausas_min, tag_id, data) 
            VALUES (%s, %s, %s, %s)
        """
        cur.executemany(query, dados_para_inserir)

        con.commit()
        print("Dados injetados com sucesso!")

except Exception as erro:
    con.rollback()
    print(f"ERRO: {erro}")
finally:
    con.close()