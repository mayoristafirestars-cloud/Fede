@echo off
rem Instalador de Mate para Windows. No pide permisos de administrador.
rem
rem Que hace: escribe UN solo archivo, el "lanzador" mate.cmd, en una carpeta de tu
rem usuario que Windows ya revisa cuando escribis una orden:
rem     %LOCALAPPDATA%\Microsoft\WindowsApps
rem Con eso la orden  mate  anda desde cualquier carpeta:   mate correr hola.mate
rem El lanzador llama al mate.bat que esta al lado de este instalador.
rem
rem Que NO hace: no toca el PATH, no toca el registro de Windows, no copia Mate a
rem otro lado, no baja nada de internet y no instala Python.
rem
rem Como se usa: doble clic sobre instalar.bat, o en PowerShell:   .\mate\instalar.bat
rem Para deshacerlo:  .\mate\instalar.bat quitar   (o borra ese mate.cmd a mano)
rem
rem Esta escrito sin tildes a proposito: la consola de Windows las mostraria mal.
rem No usa bloques entre parentesis, para que ande con carpetas como "mate (1)".
setlocal EnableExtensions DisableDelayedExpansion
set "AQUI=%~dp0"
set "CARPETA=%LOCALAPPDATA%\Microsoft\WindowsApps"
set "LANZADOR=%CARPETA%\mate.cmd"
set "MARCA=Lanzador de Mate"
set "CODIGO=1"

echo.
if /i "%~1"=="quitar" goto quitar
if not "%~1"=="" goto uso

echo Instalador de Mate
echo ------------------
echo.

rem 1. Tiene que estar Mate entero al lado de este archivo.
if not exist "%AQUI%mate.py" goto falta_mate
if not exist "%AQUI%mate.bat" goto falta_mate

rem 2. Tiene que haber un Python que ande (3.10 o mas nuevo). Se prueba corriendolo:
rem    en Windows puede existir un "python" de mentira que solo abre la tienda.
set "PY="
set "VIEJO="
python -c "import sys; sys.exit(0 if sys.version_info[:2] >= (3, 10) else 3)" >nul 2>nul
set "SALIO=%errorlevel%"
if "%SALIO%"=="0" set "PY=python"
if "%SALIO%"=="3" set "VIEJO=1"
if defined PY goto con_python
py -3 -c "import sys; sys.exit(0 if sys.version_info[:2] >= (3, 10) else 3)" >nul 2>nul
set "SALIO=%errorlevel%"
if "%SALIO%"=="0" set "PY=py -3"
if "%SALIO%"=="3" set "VIEJO=1"
if defined PY goto con_python
if defined VIEJO goto python_viejo
goto falta_python

:con_python
rem 3. La carpeta donde va el lanzador tiene que existir.
if not defined LOCALAPPDATA goto sin_carpeta
if not exist "%CARPETA%\" goto sin_carpeta

rem 4. Si ya hay un mate.cmd ahi y no lo escribio este instalador, no se pisa.
if not exist "%LANZADOR%" goto escribir
findstr /c:"%MARCA%" "%LANZADOR%" >nul 2>nul
if errorlevel 1 goto hay_otro

:escribir
rem 5. El lanzador: cinco renglones. Avisa con MATE_ORDEN que la orden es 'mate'
rem    (asi los comandos que Mate sugiere se escriben con esa orden) y le pasa
rem    todo al mate.bat de esta carpeta.
rem    (ver deja el codigo de error en cero, para saber si fallo la escritura)
ver >nul
>"%LANZADOR%" echo @echo off
if errorlevel 1 goto no_pude_escribir
>>"%LANZADOR%" echo rem %MARCA%: lo escribio instalar.bat. Para sacarlo, borra este archivo.
>>"%LANZADOR%" echo setlocal
>>"%LANZADOR%" echo set "MATE_ORDEN=mate"
>>"%LANZADOR%" echo "%AQUI%mate.bat" %%*
if not exist "%LANZADOR%" goto no_pude_escribir

rem 6. Se prueba de verdad. Primero el lanzador, llamado por su nombre completo.
set "DIJO="
for /f "usebackq delims=" %%V in (`call "%LANZADOR%" --version 2^>nul`) do set "DIJO=%%V"
if not defined DIJO goto lanzador_roto
if /i not "%DIJO:~0,5%"=="Mate " goto lanzador_roto

rem    Despues la orden 'mate' sola, desde otra carpeta, como la vas a escribir vos.
set "DIJO2="
pushd "%SystemRoot%" 2>nul
for /f "usebackq delims=" %%V in (`mate --version 2^>nul`) do set "DIJO2=%%V"
popd
if not defined DIJO2 goto no_se_encuentra

echo Listo: la orden  mate  quedo instalada.   [%DIJO2%]
echo.
echo Que hice:
echo   Escribi un solo archivo, el lanzador:
echo     "%LANZADOR%"
echo   Ese archivo llama al Mate que esta en esta carpeta:
echo     "%AQUI%"
echo   No toque el PATH, ni el registro de Windows, ni ningun otro archivo.
echo.
echo Como se usa: en PowerShell, parado en cualquier carpeta:
echo     mate --version
echo     mate curso
echo     mate correr mi_programa.mate
echo.
echo Importante: Mate sigue viviendo en esta carpeta. Si la moves o le cambias el
echo nombre, la orden deja de andar: corre instalar.bat otra vez desde el lugar nuevo.
echo.
echo Para deshacerlo: borra ese archivo mate.cmd, o corre instalar.bat con la
echo palabra quitar. En PowerShell, parado donde esta la carpeta mate:
echo     .\mate\instalar.bat quitar
set "CODIGO=0"
goto fin

:quitar
echo Sacar la orden mate
echo -------------------
echo.
if not exist "%LANZADOR%" goto no_estaba
findstr /c:"%MARCA%" "%LANZADOR%" >nul 2>nul
if errorlevel 1 goto hay_otro
del "%LANZADOR%"
if exist "%LANZADOR%" goto no_pude_borrar
echo Listo: borre el lanzador. La orden  mate  ya no esta instalada.
echo     "%LANZADOR%"
echo No toque nada mas. La carpeta de Mate y tus programas siguen donde estaban:
echo     "%AQUI%"
echo Mate se sigue pudiendo usar con la orden larga:   python mate\mate.py ...
set "CODIGO=0"
goto fin

:no_estaba
echo La orden  mate  no estaba instalada: no hay nada que sacar.
echo Busque este archivo y no esta:
echo     "%LANZADOR%"
set "CODIGO=0"
goto fin

:uso
echo No entiendo "%~1". Este instalador se usa de dos maneras:
echo     instalar.bat           deja la orden  mate  lista para usar
echo     instalar.bat quitar    la saca
goto fin

:falta_mate
echo No instale nada: al lado de instalar.bat tienen que estar mate.py y mate.bat,
echo y en esta carpeta no estan:
echo     "%AQUI%"
echo Si abriste instalar.bat desde adentro del archivo .zip, primero hay que sacar
echo todo afuera: clic derecho sobre el .zip, "Extraer todo", y despues doble clic
echo sobre el instalar.bat de la carpeta extraida.
goto fin

:falta_python
echo No instale nada: no encuentro Python en esta computadora, y Mate lo necesita.
echo.
echo   1. Bajalo de https://www.python.org/downloads/
echo   2. Abri el instalador y, en la primera pantalla, abajo, marca la casilla
echo      "Add python.exe to PATH" antes de tocar "Install Now".
echo   3. Cerra esta ventana y volve a correr instalar.bat.
echo.
echo Si ya lo habias instalado, casi seguro falto marcar esa casilla: corre de nuevo
echo el instalador de Python, elegi "Modify" y marcala.
goto fin

:python_viejo
echo No instale nada: el Python de esta computadora es anterior al 3.10, y Mate
echo necesita el 3.10 o uno mas nuevo.
echo Baja el ultimo de https://www.python.org/downloads/ y, en la primera pantalla
echo del instalador, marca la casilla "Add python.exe to PATH". Despues volve a
echo correr instalar.bat.
goto fin

:sin_carpeta
echo No instale nada: no existe la carpeta donde iba a dejar el lanzador:
echo     "%CARPETA%"
echo En Windows 10 y 11 esa carpeta viene de fabrica. Mate se puede usar igual, sin
echo instalar, con la orden larga. Parado en la carpeta que contiene a la carpeta mate:
echo     python mate\mate.py correr mate\ejemplos\01_hola.mate
goto fin

:hay_otro
echo No toque nada: en esa carpeta ya hay un mate.cmd que no escribio este instalador,
echo y no lo quiero pisar ni borrar:
echo     "%LANZADOR%"
echo Si sabes que no lo usas, borralo a mano y corre instalar.bat de nuevo.
goto fin

:no_pude_escribir
echo No instale nada: Windows no me dejo escribir este archivo:
echo     "%LANZADOR%"
echo Mate se puede usar igual, sin instalar, con la orden larga. Parado en la carpeta
echo que contiene a la carpeta mate:
echo     python mate\mate.py correr mate\ejemplos\01_hola.mate
goto fin

:lanzador_roto
del "%LANZADOR%" >nul 2>nul
echo No instale nada: escribi el lanzador, lo probe y no anduvo, asi que lo borre.
echo Lo mas probable es que el nombre de esta carpeta tenga un signo que confunde a
echo Windows, como %% o ^^, o letras que esta consola no sabe escribir:
echo     "%AQUI%"
echo Move la carpeta de Mate a un lugar de nombre simple, por ejemplo C:\mate, y
echo corre instalar.bat desde ahi. Mientras tanto, la orden larga anda igual:
echo     python mate\mate.py correr mate\ejemplos\01_hola.mate
goto fin

:no_se_encuentra
del "%LANZADOR%" >nul 2>nul
echo No instale nada: el lanzador anda, pero Windows no lo encuentra cuando se escribe
echo mate  desde otra carpeta, asi que lo borre para no dejar nada a medias.
echo Pasa cuando esta carpeta no esta entre las que Windows revisa, el PATH:
echo     "%CARPETA%"
echo No cambio el PATH por mi cuenta, para no romper nada. Mate se puede usar igual
echo con la orden larga, parado en la carpeta que contiene a la carpeta mate:
echo     python mate\mate.py correr mate\ejemplos\01_hola.mate
goto fin

:no_pude_borrar
echo No pude borrar el lanzador. Cerra las ventanas de PowerShell que esten usando
echo Mate y proba de nuevo, o borralo a mano:
echo     "%LANZADOR%"
goto fin

:fin
echo.
pause
exit /b %CODIGO%
