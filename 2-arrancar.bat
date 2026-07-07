@echo off
REM ============================================
REM  Arranca Max + WhatsApp - doble click
REM ============================================
cd /d "%~dp0"

if not exist .env (
    echo Falta el archivo .env con tu API key.
    echo Ejecuta primero 1-instalar.bat
    pause
    exit /b 1
)

echo Abriendo el cerebro de Max...
start "Max - cerebro (NO CERRAR)" cmd /k py -m uvicorn max_server:app --port 8002

timeout /t 6 /nobreak >nul

echo Abriendo la conexion de WhatsApp...
cd whatsapp-bridge
start "Max - WhatsApp (NO CERRAR)" cmd /k npm start
cd ..

echo.
echo ============================================
echo  Se abrieron 2 ventanas nuevas. NO las cierres.
echo.
echo  La PRIMERA VEZ: en la ventana de WhatsApp va a
echo  aparecer un QR. Escanealo desde el telefono del
echo  bot: WhatsApp ^> Ajustes ^> Dispositivos vinculados
echo  ^> Vincular un dispositivo.
echo.
echo  Cuando diga "Bridge conectado", escribile al bot
echo  desde tu WhatsApp y Max te responde.
echo ============================================
pause
