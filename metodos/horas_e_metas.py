import psycopg2
from metodos.database import iniciar_conexao

def agregar_horas(con):
    with con.cursor() as cur:
        # Horas feitas hoje
        cur.execute("""
            SELECT 
                COALESCE(SUM(minutos), 0), 
                COALESCE(SUM(pausas_min), 0) 
            FROM log_estudo 
            WHERE data = (NOW() AT TIME ZONE 'America/Sao_Paulo')::date
        """)
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
            WHERE data >= (date_trunc('week', (NOW() AT TIME ZONE 'America/Sao_Paulo')::date + INTERVAL '1 day') - INTERVAL '1 day')::date
        """)
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
            WHERE date_trunc('month', data) = date_trunc('month', (NOW() AT TIME ZONE 'America/Sao_Paulo')::date)
        """)
        minutos, pausas = cur.fetchone()
        total_mes = minutos - pausas
        horas_mes = int(total_mes / 60)
        min_restantes_mes = int(total_mes % 60)

        # Retorna todos os 6 valores
    return horas_hoje, min_restantes_hoje, horas_semana, min_restantes_semana, horas_mes, min_restantes_mes

def extrair_metas(con):
    with con.cursor() as cur:
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
