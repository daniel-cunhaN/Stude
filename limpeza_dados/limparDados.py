import pandas as pd

df = pd.read_csv('limpeza_dados/data.csv', encoding='utf8', skipinitialspace=True)
df.columns = df.columns.str.strip() # Limpa espaço das colunas
df = df.drop(columns=['Propriedade', 'Fim', 'Hora', 'Start', 'StartBT', 'StopBT'])

df['Pausas (min)'] = pd.to_numeric(df['Pausas (min)'], errors='coerce') 
df['Pausas (min)'] = df['Pausas (min)'].astype('Int64')
df['Pausas (min)'] = df['Pausas (min)'].fillna(0)

print(df.head(50))
