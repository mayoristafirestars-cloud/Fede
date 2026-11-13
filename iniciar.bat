@echo off
call venv\Scripts\activate
echo Iniciando Coronel Sur...
echo Abriendo navegador en http://localhost:8000
start http://localhost:8000
python backend\main.py
