@echo off
REM ============================================
REM  Vigilante: avisa por WhatsApp si algo se cae
REM  (opcional en la PC; en el VPS arranca solo)
REM ============================================
cd /d "%~dp0"
start "Vigilante (NO CERRAR)" cmd /k py watchdog.py
echo Vigilante iniciado en una ventana nueva.
pause
