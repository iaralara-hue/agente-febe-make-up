@echo off
echo ==========================================
echo CRIANDO LINK PUBLICO (QUALQUER LUGAR)...
echo ==========================================

:: 1. Iniciar o Tunel na porta 3000
echo Abrindo o link publico... 
echo Este link permitira acessar o Alpha de QUALQUER celular (4G/5G/Outro Wi-Fi).
echo.
echo COPIE O LINK QUE APARECER ABAIXO:
echo ------------------------------------------
npx localtunnel --port 3000
echo ------------------------------------------

pause
