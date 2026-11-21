@echo off
rem Mate en Windows. Sirve para escribir menos:
rem   mate correr archivo.mate      (en PowerShell: .\mate correr archivo.mate)
rem   mate probar archivo.mate
rem Tambien se puede arrastrar un archivo .mate y soltarlo encima de este mate.bat.
rem Tiene que estar en la misma carpeta que mate.py.
setlocal
set "MATE=%~dp0mate.py"

rem Con doble clic o arrastrando un archivo, la ventana se cerraria sola al terminar:
rem en esos dos casos se espera una tecla, para poder leer el resultado.
set "ESPERAR="
if "%~1"=="" set "ESPERAR=1"
if "%~2"=="" if exist "%~1" if /i "%~1"=="%~f1" set "ESPERAR=1"

set "PY=python"
where python >nul 2>nul
if not errorlevel 1 goto correr
set "PY=py -3"
where py >nul 2>nul
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
