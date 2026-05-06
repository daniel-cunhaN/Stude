import pandas as pd

df = pd.read_csv('limpeza_dados/dados.csv', encoding='utf8', skipinitialspace=True)
df.columns = df.columns.str.strip() # Limpa espaço iniciais e finais das colunas
df = df.drop(columns=['Propriedade', 'Fim', 'Hora', 'StartBT', 'StopBT']) # Seleciona colunas úteis excluindo as inúteis

######################
# Limpeza coluna pausas
######################
df['Pausas (min)'] = pd.to_numeric(df['Pausas (min)'], errors='coerce')  # Converte de string para número
df['Pausas (min)'] = df['Pausas (min)'].astype('Int64') # Converte o número para Int64 para que Pandas reconheça
df['Pausas (min)'] = df['Pausas (min)'].fillna(0) # Preenche nulos com 0

######################
#Limpeza coluna Tags
######################
df['Tags'] = df['Tags'].str.split(',').str[0] # Corta tudo assim que vírgula aparece. ex: Organização, Web -> Organização
dicionario_tags_antigas = {
    'Infra': 'Infraestrutura',
    'Sistemas': 'Sistemas Variados',
}
df['Tags'] = df['Tags'].replace(dicionario_tags_antigas) # Substitui tags antigas por novas aos quais estão dentro do dicionário
df = df[df['Tags'] != 'Organização'] # Drop em todas as colunas com valor "Organização"

######################
# Limpeza coluna "Start"
######################
tradutor_meses = {
    ' de janeiro de ': '/01/',
    ' de fevereiro de ': '/02/',
    ' de março de ': '/03/',
    ' de abril de ': '/04/',
    ' de maio de ': '/05/',
    ' de junho de ': '/06/',
    ' de julho de ': '/07/',
    ' de agosto de ': '/08/',
    ' de setembro de ': '/09/',
    ' de outubro de ': '/10/',
    ' de novembro de ': '/11/',
    ' de dezembro de ': '/12/'
}

df['Start'] = df['Start'].str.replace(' \(BRT\)', '', regex=True) # Procura os "(BRT)" e apaga (substituindo por nada '')

for texto, numero in tradutor_meses.items(): #Pega texto e numero do dicionario
    df['Start'] = df['Start'].str.replace(texto, numero) # Substitui o texto pelo numero do dicionário, ficando DD/MM/AAAA 00:00

df['Start'] = pd.to_datetime(df['Start'], format='%d/%m/%Y %H:%M') #Converte texto da data para número para posterior edição
df['Start'] = df['Start'].dt.date # Retira as horas e minutos e só deixa a data

df = df.rename(columns={'Min': 'minutos', 'Start': 'data', 'Pausas (min)': 'pausas_min', 'Tags': 'tag_id'})

tags = df['tag_id'].unique().tolist() # Extrai tags unicas (ex: Dados, Revisão...)
dicionario_valores = {}
for numero, valor in enumerate(tags, start=1): # Atribui às tags id único
    dicionario_valores[valor] = numero

df['tag_id'] = df['tag_id'].map(dicionario_valores) # Substitui as tags pelos ids

df.to_csv('limpeza_dados/dadosLimpos.csv', index=False, encoding = 'utf-8') # Salva em arquivo novo