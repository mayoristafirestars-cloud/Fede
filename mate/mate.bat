@echo off
rem Mate en Windows. Sirve para escribir menos:
rem   mate correr archivo.mate      (en PowerShell: .\mate correr archivo.mate)
rem   mate probar archivo.mate
rem Tambien se puede arrastrar un archivo .mate y soltarlo encima de este mate.bat.
rem Tiene que estar en la misma carpeta que mate.py.
rem Para tener la orden  mate  desde cualquier carpeta, sin el .\ adelante: instalar.bat
setlocal
set "MATE=%~dp0mate.py"

rem Con doble clic o arrastrando un archivo, la ventana se cerraria sola al terminar:
rem en esos dos casos se espera una tecla, para poder leer el resultado.
set "ESPERAR="
if "%~1"=="" set "ESPERAR=1"
if "%~2"=="" if exist "%~1" if /i "%~1"=="%~f1" set "ESPERAR=1"
rem (la orden  mate  que deja instalar.bat se escribe en una ventana que ya esta
rem abierta: ahi no se espera nunca)
if defined MATE_ORDEN set "ESPERAR="

rem Se prueba que Python ande de verdad: en Windows puede haber un "python" de
rem mentira, que no es Python sino un atajo a la tienda de Microsoft.
set "PY=python"
python -c "import sys" >nul 2>nul
if not errorlevel 1 goto correr
set "PY=py -3"
py -3 -c "import sys" >nul 2>nul
if not errorlevel 1 goto correr
echo No encuentro Python en esta computadora.
echo Instalalo desde https://www.python.org/downloads/ y, en la primera pantalla
echo del instalador, marca la casilla "Add python.exe to PATH".
set "CODIGO=1"
goto fin

:correr
%PY% "%MATE%" %*
set "CODIGO=%errorlevel%"

:fin
if defined ESPERAR pause
exit /b %CODIGO%
