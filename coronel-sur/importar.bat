@echo off
call venv\Scripts\activate
echo Importando datos de FactuPyme...
python backend\importador\importar_factupyme.py
echo.
pause
