@echo off
REM ============================================
REM  Instalador de Max - doble click y listo
REM ============================================
cd /d "%~dp0"

echo.
echo === [1/4] Instalando dependencias de Python (puede tardar unos minutos) ===
py -m pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo ERROR: fallo la instalacion de Python. Sacale foto a esta ventana.
    pause
    exit /b 1
)

echo.
echo === [2/4] Instalando dependencias de WhatsApp (puede tardar, baja ~200MB) ===
cd whatsapp-bridge
call npm install
if errorlevel 1 (
    echo.
    echo ERROR: fallo la instalacion de Node. Sacale foto a esta ventana.
    pause
    exit /b 1
)
cd ..

echo.
echo === [3/4] Configurando tu API key de Anthropic ===
if exist .env goto :haskey
set /p KEY="Pega aca tu API key (sk-ant-...) y apreta Enter: "
>.env echo ANTHROPIC_API_KEY=%KEY%
echo API key guardada en .env
:haskey

echo.
echo === [4/4] Configurando tu numero de WhatsApp ===
if exist whatsapp-bridge\allowed.txt goto :hasnum
echo (Es TU numero personal, desde el que le vas a escribir al bot.)
echo (Formato: 549 + codigo de area + numero, sin guiones. Ej: 5492954123456)
set /p NUM="Escribi tu numero y apreta Enter: "
>whatsapp-bridge\allowed.txt echo %NUM%
echo Numero guardado.
:hasnum

echo.
echo ============================================
echo  LISTO! Ahora hace doble click en:
echo  2-arrancar.bat
echo ============================================
pause
