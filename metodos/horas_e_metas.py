import sqlite3
from metodos.database import iniciar_conexao
from datetime import datetime, timedelta

def agregar_horas(con):
    hoje = datetime.now()
    data_hoje = hoje.strftime('%Y-%m-%d')
    
    dias_desde_domingo = (hoje.weekday() + 1) % 7
    domingo_atual = (hoje - timedelta(days=dias_desde_domingo)).strftime('%Y-%m-%d')
    
    domingo_anterior = (hoje - timedelta(days=dias_desde_domingo + 7)).strftime('%Y-%m-%d')
    sabado_anterior = (hoje - timedelta(days=dias_desde_domingo + 1)).strftime('%Y-%m-%d')
    
    primeiro_dia_mes = hoje.replace(day=1).strftime('%Y-%m-%d')

    cur = con.cursor()
    
    # Horas feitas hoje
    cur.execute("""
        SELECT 
            COALESCE(SUM(minutos), 0), 
            COALESCE(SUM(pausas_min), 0) 
        FROM log_estudo 
        WHERE data = ?
    """, (data_hoje,))
    minutos, pausas = cur.fetchone()
    total_hoje = minutos - pausas
    horas_hoje = int(total_hoje / 60)
    min_restantes_hoje = int(total_hoje % 60)

    # Horas feitas na semana
    cur.execute("""
        SELECT 
            COALESCE(SUM(minutos), 0), 
            COALESCE(SUM(pausas_min), 0) 
        FROM log_estudo 
        WHERE data >= ?
    """, (domingo_atual,))
    minutos, pausas = cur.fetchone()
    total_semana = minutos - pausas
    horas_semana = int(total_semana / 60)
    min_restantes_semana = int(total_semana % 60)

    # Horas feitas no mês
    cur.execute("""
        SELECT 
            COALESCE(SUM(minutos), 0), 
            COALESCE(SUM(pausas_min), 0) 
        FROM log_estudo 
        WHERE data >= ?
    """, (primeiro_dia_mes,))
    minutos, pausas = cur.fetchone()
    total_mes = minutos - pausas
    horas_mes = int(total_mes / 60)
    min_restantes_mes = int(total_mes % 60)

    # Horas feitas na semana anterior
    cur.execute("""
        SELECT 
            COALESCE(SUM(minutos), 0), 
            COALESCE(SUM(pausas_min), 0) 
        FROM log_estudo 
        WHERE data >= ? AND data <= ?
    """, (domingo_anterior, sabado_anterior))
    minutos, pausas = cur.fetchone()
    total_semana_anterior = minutos - pausas
    horas_semana_anterior = int(total_semana_anterior / 60)
    min_restantes_semana_anterior = int(total_semana_anterior % 60)

    return horas_hoje, min_restantes_hoje, horas_semana, min_restantes_semana, horas_mes, min_restantes_mes, horas_semana_anterior, min_restantes_semana_anterior

def extrair_metas(con):
    cur = con.cursor()
    cur.execute("SELECT tipo_meta, horas_alvo FROM metas")
    resultados = cur.fetchall()

    meta_semana = 0
    meta_mes = 0
    for item in resultados:
        tipo = item[0]
        horas = item[1]

        if tipo == 'semanal':
            meta_semana = horas
        elif tipo == 'mensal':
            meta_mes = horas
    return meta_semana, meta_mes
