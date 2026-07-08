@echo off
REM ============================================
REM  Arranca el VENDEDOR virtual - doble click
REM ============================================
cd /d "%~dp0"

if not exist .env (
    echo Falta el archivo .env con tu API key.
    pause
    exit /b 1
)

if not exist vendedor-bridge\node_modules (
    echo Primera vez: instalando dependencias del vendedor...
    cd vendedor-bridge
    call npm install
    cd ..
)

echo Abriendo el cerebro del vendedor...
start "Vendedor - cerebro (NO CERRAR)" cmd /k py -m uvicorn vendedor_server:app --port 8003

timeout /t 6 /nobreak >nul

echo Abriendo la conexion de WhatsApp del negocio...
cd vendedor-bridge
start "Vendedor - WhatsApp (NO CERRAR)" cmd /k npm start
cd ..

echo.
echo ============================================
echo  Se abrieron 2 ventanas nuevas. NO las cierres.
echo.
echo  La PRIMERA VEZ: aparece un QR en la ventana de
echo  WhatsApp. Escanealo desde el telefono del NEGOCIO
echo  (el numero donde van a escribir los clientes).
echo.
echo  IMPORTANTE: ese numero NO debe ser el mismo que
echo  usa Max. Cada bot necesita su propio numero.
echo ============================================
pause
