@echo off
echo Iniciando o Stude e preparando o navegador... 
echo ==========================================
echo !!! Deixe esta janela aberta enquanto estiver trabalhando !!!
echo.
echo Quando quiser fechar o aplicativo,
echo clique nesta janela e aperte 'Ctrl + C'.
echo ==========================================

:: Esse comando conta 4 segundos e depois abre o seu site
start /min cmd /c "timeout /t 4 /nobreak >nul & start http://localhost:8501"

:: Esse comando liga o aplicativo
wsl bash -c "cd /mnt/c/Dev/Stude/docker && docker compose up"