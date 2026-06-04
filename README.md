# 📚 Stude

Bem-vindo ao **Stude**! Um aplicativo web voltado para o gerenciamento de metas e acompanhamento de horas de estudo. 

## 🚀 Tecnologias Utilizadas
* **Python** **Streamlit** (Frontend / Web App)
* **PostgreSQL / Supabase** (Banco de Dados)
* **Docker & WSL** (Ambiente de desenvolvimento local)
* **Psycopg2, Pandas** (Manejo de Dados)
* **Google Datastudio (Looker)** (Business Intelligence)

---

# Showcase
<img width="1899" height="1022" alt="Stude" src="https://github.com/user-attachments/assets/e819ea72-1cbf-433d-afc9-a8c9c1e32592" />


## 💻 Setup Local (Para Desenvolvimento)

### Pré-requisitos
* **Passo 0:** Certifique-se de ter o **Docker Desktop** aberto e o **WSL** (Windows Subsystem for Linux) instalado no seu computador.

### Instalação
1. Faça o clone do repositório:
```bash
git clone https://github.com/dev-DanielNascimento/Stude.git
```
2. Escolha um banco de dados PostgreSQL de sua preferência (ex: Supabase), crie credenciais IPv4 e insira no arquivo .env. Atenção: Neste arquivo local, não use espaços ou aspas. Exemplo:

```bash
host=aws-1-regiao.pooler.supabase.com
user=postgres.sua_credencial
password=suasenha
port=5432
dbname=postgres
url_dashboard=seulinkEmbedGoogleLooker
```
3. Faça a cópia do template do dashboard e adicione seu banco de dados: [Template](https://datastudio.google.com/reporting/3e2c4311-1c4a-412b-b7e4-67104684ddd7)
4. No google data studio, vá em compartilhar e crie seu link embed e mude no .env:
```"url_dashboard=seulinkEmbedGoogleLooker"```
5. Para iniciar o aplicativo e o banco de dados local, basta executar o arquivo Start_App.bat (via duplo clique ou pelo terminal):
# No PowerShell:
.\Start_App.bat

# No CMD:
Start_App.bat

## ☁️ Setup na Nuvem (Deploy)
Para hospedar o aplicativo gratuitamente utilizando o Streamlit Community Cloud:

1. Clone o repositório na branch "webapp"
2. Acesse a página de deploy do Streamlit (https://share.streamlit.io/deploy) e conecte com seu repositório **na nuvem do github** escolhendo sua respectiva branch
3. Escolha o banco de dados de produção. Na tela de deploy do Streamlit, vá em Advanced Settings > Secrets e insira as credenciais utilizando o formato TOML (com aspas e espaços). Exemplo:
```bash
host=aws-1-regiao.pooler.supabase.com
user=postgres.sua_credencial
password=suasenha
port=5432
dbname=postgres
url_dashboard=seulinkEmbedGoogleLooker
```
4. Com a url do seu dashboard (vide instruções na sessão "setup local") Substitua a variável no arquivo ".env":
```
url_dashboard=seulinkEmbedGoogleLooker
```
5. Acesse seu aplicativo por meio do site do streamlit
