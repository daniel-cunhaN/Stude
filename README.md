<div align="center">
  <img src="https://github.com/user-attachments/assets/91c18a54-93f1-4d62-b3e1-e4a2633cb4b8" alt="Ícone Stude" height=300px width=300px/>

  <h1 align="center">Stude</h1>
  <h4 align="center">Apicativo open-source de estudos, de estudante para estudantes</h4>
</div>

<!-- IDEIAS PARA ADICIONAR FUTURAMENTE
<div align="center">
  <a href="https://github.com/LizardByte/Sunshine"><img src="https://img.shields.io/github/stars/lizardbyte/sunshine.svg?logo=github&style=for-the-badge" alt="GitHub stars"></a>
  <a href="https://github.com/LizardByte/Sunshine/releases/latest"><img src="https://img.shields.io/github/downloads/lizardbyte/sunshine/total.svg?style=for-the-badge&logo=github" alt="GitHub Releases"></a>
-->

## ℹ️ Sobre

  Stude é um aplicativo web self-hosted para gerenciamento de sessões e metas de estudo. Com um temporizador integrado, você pode registrar suas sessões em tempo real, categorizá-las por matéria e
  acompanhar seu progresso diário, semanal e mensal. Conta com um bloco de notas integrado permitindo anotar ideias e lembretes sem   
  sair do aplicativo. Defina metas semanais e mensais para manter a constância, e visualize seus dados em um dashboard analítico. O Stude roda com
  Streamlit e PostgreSQL, podendo ser hospedado localmente via Docker ou na nuvem gratuitamente pelo Streamlit Community Cloud
  
## 💻 Setup Local (Para Desenvolvimento)

#### Pré-requisitos
**Passo 0:** Certifique-se de ter o **Docker Desktop** aberto e o **WSL** (Windows Subsystem for Linux) instalado no seu computador.

#### Instalação
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

##### No PowerShell:
```bash
.\Start_App.bat
```
##### No CMD:
```bash
Start_App.bat
```

### ☁️ Setup na Nuvem (Deploy)
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
