@echo off
echo ==========================================
echo INICIANDO AGENTE FEBE (BELEZA)...
echo ==========================================

:: Caminho da pasta atual
set BASE_DIR=%~dp0

:: 1. Iniciar Backend (FastAPI)
echo [1/2] Iniciando Backend na porta 8000...
start cmd /k "cd /d "%BASE_DIR%backend" && pip install -r requirements.txt && python main.py"

:: 2. Iniciar Frontend (Vite)
echo [2/2] Iniciando Frontend na porta 3000...
start cmd /k "cd /d "%BASE_DIR%frontend" && npm install && npm run dev"

:: 3. Detectar IP Local
for /f "delims=" %%i in ('python get_ip.py') do set LOCAL_IP=%%i

echo ==========================================
echo AGUARDE UM MOMENTO E ACESSE:
echo [PC]     http://localhost:3000
echo [CELULAR] http://%LOCAL_IP%:3000
echo ==========================================
start http://localhost:3000
pause
