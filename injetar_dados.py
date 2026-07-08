import sqlite3
import random
from datetime import datetime, timedelta

def injetar_dados():
    con = sqlite3.connect("stude_local.db")
    cur = con.cursor()

    print("Injetando dados de teste no banco de dados...")

    # 1. Limpar dados antigos (opcional, para garantir que as tags IDs batem e não acumula lixo infinito)
    # cur.execute("DELETE FROM log_estudo;")
    # cur.execute("DELETE FROM tags;")
    # cur.execute("DELETE FROM metas;")

    # 2. Inserir algumas tags (Matérias)
    materias = ['Matemática', 'Física', 'História', 'Inglês', 'Programação']
    tag_ids = []
    
    for mat in materias:
        try:
            cur.execute("INSERT INTO tags (tag) VALUES (?);", (mat,))
            tag_ids.append(cur.lastrowid)
        except sqlite3.IntegrityError:
            # Se já existir, a gente busca o ID dela
            cur.execute("SELECT id FROM tags WHERE tag = ?;", (mat,))
            tag_ids.append(cur.fetchone()[0])
            
    # 3. Inserir Metas Fictícias
    cur.execute("INSERT OR REPLACE INTO metas (id, tipo_meta, horas_alvo) VALUES (1, 'semanal', 10);")
    cur.execute("INSERT OR REPLACE INTO metas (id, tipo_meta, horas_alvo) VALUES (2, 'mensal', 40);")

    # 4. Inserir histórico de estudos (últimos 30 dias)
    hoje = datetime.now()
    dias_para_injetar = 30

    print(f"Gerando histórico de estudos para os últimos {dias_para_injetar} dias...")
    
    for i in range(dias_para_injetar):
        # 80% de chance de ter estudado nesse dia (para criar buracos na ofensiva)
        if random.random() < 0.8:
            data_estudo = hoje - timedelta(days=i)
            str_data = data_estudo.strftime('%Y-%m-%d')
            
            # Gera 1 a 3 ciclos de estudo no dia
            ciclos_no_dia = random.randint(1, 3)
            for _ in range(ciclos_no_dia):
                minutos_estudados = random.randint(20, 120)
                pausa = random.randint(0, 15)
                tag_escolhida = random.choice(tag_ids)
                
                cur.execute(
                    "INSERT INTO log_estudo (data, minutos, pausas_min, tag_id) VALUES (?, ?, ?, ?)",
                    (str_data, minutos_estudados, pausa, tag_escolhida)
                )

    # 5. Modificar Troféus e Streak para teste
    cur.execute("UPDATE inventario SET trofeus = ? WHERE id = 1", (random.randint(5, 15),))
    
    # Colocando um streak falso de 7 dias, ativo hoje
    cur.execute("""
        UPDATE streak_status 
        SET streak_atual = 7, maior_streak = 15, congelamentos_ativos = 1, ultima_atividade = ?
        WHERE id = 1
    """, (hoje.strftime('%Y-%m-%d'),))
    
    con.commit()
    con.close()
    
    print("✅ Dados de teste injetados com sucesso! Atualize o seu navegador (F5).")

if __name__ == "__main__":
    injetar_dados()
