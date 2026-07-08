import sqlite3
import streamlit as st
from datetime import datetime, timedelta

def obter_inventario(con):
    cur = con.cursor()
    cur.execute("SELECT trofeus FROM inventario WHERE id = 1")
    resultado = cur.fetchone()
    return resultado[0] if resultado else 0

def obter_streak_status(con):
    cur = con.cursor()
    cur.execute("SELECT streak_atual, maior_streak, congelamentos_ativos, ultima_atividade FROM streak_status WHERE id = 1")
    resultado = cur.fetchone()
    if resultado:
        return {
            "streak_atual": resultado[0],
            "maior_streak": resultado[1],
            "congelamentos_ativos": resultado[2],
            "ultima_atividade": resultado[3]
        }
    return None

def atualizar_streak(con):
    """
    Atualiza o streak baseado na data da última atividade e no dia de hoje.
    """
    status = obter_streak_status(con)
    if not status:
        return

    hoje = datetime.now().date()
    ultima_atividade = status["ultima_atividade"]

    if ultima_atividade:
        ultima_data = datetime.strptime(ultima_atividade, '%Y-%m-%d').date()
        diferenca_dias = (hoje - ultima_data).days

        if diferenca_dias > 1:
            # Passou mais de 1 dia desde o último estudo
            congelamentos = status["congelamentos_ativos"]
            dias_a_cobrir = diferenca_dias - 1
            
            if congelamentos >= dias_a_cobrir:
                # Usa congelamentos e mantém a ofensiva
                novo_congelamento = congelamentos - dias_a_cobrir
                cur = con.cursor()
                cur.execute("""
                    UPDATE streak_status 
                    SET congelamentos_ativos = ?, ultima_atividade = ?
                    WHERE id = 1
                """, (novo_congelamento, (hoje - timedelta(days=1)).strftime('%Y-%m-%d')))
                con.commit()
            else:
                # Perdeu a ofensiva
                cur = con.cursor()
                cur.execute("""
                    UPDATE streak_status 
                    SET streak_atual = 0, congelamentos_ativos = 0 
                    WHERE id = 1
                """)
                con.commit()

def registrar_estudo_streak(con):
    """
    Chamar quando o usuário salvar um ciclo de estudo. Aumenta a ofensiva.
    """
    status = obter_streak_status(con)
    if not status:
        return

    hoje = datetime.now().strftime('%Y-%m-%d')
    ultima_atividade = status["ultima_atividade"]
    streak_atual = status["streak_atual"]
    maior_streak = status["maior_streak"]

    if ultima_atividade != hoje:
        # Se for o primeiro estudo do dia
        novo_streak = streak_atual + 1
        novo_maior = max(novo_streak, maior_streak)

        cur = con.cursor()
        cur.execute("""
            UPDATE streak_status 
            SET streak_atual = ?, maior_streak = ?, ultima_atividade = ?
            WHERE id = 1
        """, (novo_streak, novo_maior, hoje))
        con.commit()

def verificar_e_premiar_metas(con, horas_semana, horas_mes, meta_semana, meta_mes):
    """
    Verifica se a meta semanal/mensal foi atingida e premia se ainda não foi no período atual.
    """
    hoje = datetime.now()
    periodo_semana = f"{hoje.year}-W{hoje.isocalendar()[1]}"
    periodo_mes = f"{hoje.year}-{hoje.month:02d}"

    cur = con.cursor()
    trofeus_ganhos = 0

    # Meta Semanal
    if meta_semana > 0 and horas_semana >= meta_semana:
        cur.execute("SELECT id FROM historico_conquistas WHERE tipo_meta = 'semanal' AND periodo = ?", (periodo_semana,))
        if not cur.fetchone():
            # Premia
            cur.execute("INSERT INTO historico_conquistas (tipo_meta, periodo, data_conquista) VALUES ('semanal', ?, ?)", (periodo_semana, hoje.strftime('%Y-%m-%d')))
            cur.execute("UPDATE inventario SET trofeus = trofeus + 1 WHERE id = 1")
            trofeus_ganhos += 1

    # Meta Mensal
    if meta_mes > 0 and horas_mes >= meta_mes:
        cur.execute("SELECT id FROM historico_conquistas WHERE tipo_meta = 'mensal' AND periodo = ?", (periodo_mes,))
        if not cur.fetchone():
            # Premia
            cur.execute("INSERT INTO historico_conquistas (tipo_meta, periodo, data_conquista) VALUES ('mensal', ?, ?)", (periodo_mes, hoje.strftime('%Y-%m-%d')))
            cur.execute("UPDATE inventario SET trofeus = trofeus + 2 WHERE id = 1")
            trofeus_ganhos += 2

    if trofeus_ganhos > 0:
        con.commit()
        st.toast(f"Parabéns! Você bateu sua meta e ganhou {trofeus_ganhos} 🏆!", icon="🎉")

def comprar_congelamento(con):
    trofeus = obter_inventario(con)
    status = obter_streak_status(con)
    custo = 2

    if status and status["congelamentos_ativos"] >= 1:
        return False, "⚠️ Você já tem um congelamento ativo! Guarde seus troféus."

    if trofeus >= custo:
        cur = con.cursor()
        cur.execute("UPDATE inventario SET trofeus = trofeus - ? WHERE id = 1", (custo,))
        cur.execute("UPDATE streak_status SET congelamentos_ativos = congelamentos_ativos + 1 WHERE id = 1")
        con.commit()
        return True, "Congelamento de Streak comprado com sucesso! Seu próximo dia sem estudos será perdoado."
    else:
        return False, "Você não tem troféus suficientes."
