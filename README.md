# 📚 Stude

Bem-vindo ao **Stude**! Um aplicativo web voltado para o gerenciamento de metas e acompanhamento de horas de estudo. 

## 🚀 Tecnologias Utilizadas
* **Python** **Streamlit** (Frontend / Web App)
* **PostgreSQL / Supabase** (Banco de Dados)
* **Docker & WSL** (Ambiente de desenvolvimento local)
* **Psycopg2, Pandas** (Manejo de Dados)

---

# Showcase
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/e4c948ec-7eb4-4d0a-8b85-01c071b803a0" />
---
<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/d00c45f3-61bf-4587-9ef8-4a74243ff35e" />

## 💻 Setup Local (Para Desenvolvimento)

### Pré-requisitos
* **Passo 0:** Certifique-se de ter o **Docker Desktop** aberto e o **WSL** (Windows Subsystem for Linux) instalado no seu computador.

### Instalação
1. Faça o clone do repositório:
```bash
git clone https://github.com/dev-DanielNascimento/Stude.git
```
Escolha um banco de dados PostgreSQL de sua preferência (ex: Supabase), crie credenciais IPv4 e insira no arquivo .env. Atenção: Neste arquivo local, não use espaços ou aspas. Exemplo:

```bash
POSTGRES_USER=postgres.sua_credencial
POSTGRES_PASSWORD=suasenha
POSTGRES_DB=postgres
host=aws-1-regiao.pooler.supabase.com
port=5432
```
Para iniciar o aplicativo e o banco de dados local, basta executar o arquivo Start_App.bat (via duplo clique ou pelo terminal):
# No PowerShell:
.\Start_App.bat

# No CMD:
Start_App.bat

## ☁️ Setup na Nuvem (Deploy)
Para hospedar o aplicativo gratuitamente utilizando o Streamlit Community Cloud:

Acesse a página de deploy do Streamlit (https://share.streamlit.io/deploy) e conecte com este repositório, escolhendo obrigatoriamente a branch webapp.

Escolha o banco de dados de produção. Na tela de deploy do Streamlit, vá em Advanced Settings > Secrets e insira as credenciais utilizando o formato TOML (com aspas e espaços). Exemplo:
```bash
POSTGRES_USER = "postgres.sua_credencial"
POSTGRES_PASSWORD = "suasenha"
POSTGRES_DB = "postgres"
host = "aws-1-regiao.pooler.supabase.com"
port = "5432"
user = "postgres.sua_credencial"
password = "suasenha"
dbname = "postgres"
```
