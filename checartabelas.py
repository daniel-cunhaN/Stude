import psycopg2
import os

# Connect to the database using your .env secrets
con = psycopg2.connect(
    host=os.getenv("host"),
    user=os.getenv("user"),
    password=os.getenv("password"),
    dbname=os.getenv("dbname")
)

with con.cursor() as cur:
    # Ask PostgreSQL for a list of tables in the public schema
    cur.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public';
    """)
    
    # Fetch all the results
    tabelas = cur.fetchall()
    
    print("Tables currently in my database:")
    print("--------------------------------")
    for tabela in tabelas:
        print(f"✅ {tabela[0]}")
        
con.close()