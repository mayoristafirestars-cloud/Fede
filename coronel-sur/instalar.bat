@echo off
echo ============================================
echo   CORONEL SUR — Instalacion inicial
echo ============================================
echo.

:: Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no esta instalado.
    echo Descargalo de https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Crear entorno virtual si no existe
if not exist "venv" (
    echo Creando entorno virtual...
    python -m venv venv
)

:: Activar entorno virtual e instalar dependencias
echo Instalando dependencias...
call venv\Scripts\activate
pip install fastapi uvicorn python-multipart --quiet

echo.
echo ============================================
echo   Instalacion completa
echo ============================================
echo.
echo Para IMPORTAR los CSVs de FactuPyme:
echo   1. Copiar los CSVs a la carpeta:  data\csv_originales\
echo   2. Nombrarlos: inventario.csv / ventas.csv / presupuestos.csv
echo   3. Ejecutar: importar.bat
echo.
echo Para INICIAR el sistema:
echo   Ejecutar: iniciar.bat
echo.
pause
