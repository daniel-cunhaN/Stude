import psycopg2
from metodos.database import iniciar_conexao

con = iniciar_conexao()

def agregar_horas(con):
    with con.cursor() as cur:
        # Horas feitas hoje
        cur.execute("SELECT SUM(minutos) FROM log_estudo WHERE data = CURRENT_DATE")
        resultado_hoje = cur.fetchone()[0]
        minutos_hoje = resultado_hoje if resultado_hoje else 0 #if e else para proteger conta horas_hoje caso retorne nulo
        horas_hoje = int(minutos_hoje / 60)


        # Horas feitas na semana
        cur.execute("SELECT SUM(minutos) FROM log_estudo WHERE data >= CURRENT_DATE - INTERVAL '7 days'")
        resultado_semana = cur.fetchone()[0]
        minutos_semana = resultado_semana if resultado_semana else 0
        horas_semana = int(minutos_semana / 60)


        # Horas feitas no mês
        cur.execute("SELECT SUM(minutos) FROM log_estudo WHERE date_trunc('month', data) = date_trunc('month', CURRENT_DATE)")
        resultado_mes = cur.fetchone()[0]
        minutos_mes = resultado_mes if resultado_mes else 0
        horas_mes = int(minutos_mes / 60)

        return horas_hoje, horas_semana, horas_mes  