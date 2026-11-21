# El curso de Mate

Doce clases cortas para aprender Mate desde cero, sin saber programar. Arranca en
"hola" y termina en un mostrador que lee tu lista de precios, charla por teclado,
contesta con una IA, tiene frenos y aprende de tus correcciones.

Cada clase lleva entre 10 y 20 minutos y tiene siempre lo mismo: qué vas a lograr, el
programa completo, el comando para correrlo, lo que tiene que salir, el error más común
(y cómo se arregla) y un ejercicio con su solución.

## Antes de empezar

1. Tené Python instalado y la carpeta `mate` en tu computadora. Si todavía no, los pasos
   están en `mate\README.md`, en "Instalarlo".
2. Abrí PowerShell en la carpeta donde está la carpeta `mate`: en el Explorador de
   archivos entrá a esa carpeta (tenés que ver `mate` como una carpeta más, no estar
   adentro), hacé clic en la barra de arriba donde figura la dirección, escribí
   `powershell` y apretá Enter.
3. Probá que ande:

       python mate\mate.py curso

   Tiene que mostrar la lista de clases.

Si instalaste la orden corta con `instalar.bat`, en todos los comandos del curso podés
escribir `mate` en lugar de `python mate\mate.py`. Por ejemplo: `mate curso 1`.

## Las clases

| Clase | Tema | Texto | Programa |
|---|---|---|---|
| 1 | Hola, tu primer programa | `clase_01_hola.md` | `clase_01_hola.mate` |
| 2 | Guardar valores con nombre | `clase_02_variables.md` | `clase_02_variables.mate` |
| 3 | Que el programa decida | `clase_03_decisiones.md` | `clase_03_decisiones.mate` |
| 4 | Listas y bucles | `clase_04_listas.md` | `clase_04_listas.mate` |
| 5 | Funciones y pruebas | `clase_05_funciones.md` | `clase_05_funciones.mate` |
| 6 | Que el programa te pregunte | `clase_06_teclado.md` | `clase_06_teclado.mate` |
| 7 | Tu lista de precios de Excel | `clase_07_lista_de_precios.md` | `clase_07_lista_de_precios.mate` |
| 8 | El primer agente | `clase_08_agente.md` | `clase_08_agente.mate` |
| 9 | Un agente que consulta a una IA | `clase_09_agente_con_ia.md` | `clase_09_agente_con_ia.mate` |
| 10 | Frenos, para poder confiar en la IA | `clase_10_frenos.md` | `clase_10_frenos.mate` |
| 11 | Un agente que recuerda y aprende | `clase_11_aprende.md` | `clase_11_aprende.mate` |
| 12 | El mostrador completo | `clase_12_mostrador.md` | `clase_12_mostrador.mate` |

Además están `precios.csv` (la lista de precios de muestra, desde la clase 7),
`respuestas.txt` (respuestas de ensayo, para la clase 9) y, de cada clase, el ejercicio
resuelto: `clase_01_solucion.mate`, `clase_02_solucion.mate`...

## Cómo se hace una clase

Para leer la clase 1 en la misma ventana de PowerShell:

    python mate\mate.py curso 1

O para abrirla con el Bloc de notas, que es más cómodo para leer:

    notepad mate\curso\clase_01_hola.md

Para correr el programa de la clase:

    python mate\mate.py correr mate\curso\clase_01_hola.mate

Y para los ejercicios, un archivo tuyo al lado de los del curso (el mismo para todas las
clases):

    notepad mate\curso\practica.mate
    python mate\mate.py correr mate\curso\practica.mate

## Lo que conviene saber

- **No hace falta clave ni internet para ninguna clase.** Desde la clase 9 los programas
  consultan a una IA, pero todo se ensaya con la opción `--ia-simulada`, que no sale a
  internet y no gasta nada. La IA de verdad es paga y es opcional: la clase 9 explica cómo.
- Desde la clase 10, al correr un programa aparecen archivos nuevos al lado
  (`clase_10_frenos.memoria.json`, `clase_10_frenos.bitacora.txt`): es lo que el agente
  recuerda y lo que anotó. Se pueden borrar sin problema.
- Si un comando no anda, leé el error: Mate dice el archivo, el renglón y qué pasó, en
  castellano. En el Bloc de notas, `Ctrl+G` te lleva a ese renglón.
- Si te trabás con una palabra: `python mate\mate.py ayuda si` (o `ayuda para`,
  `ayuda leer`...) la explica con un ejemplo corto.
