# Clase 1: Hola, tu primer programa

## Qué vas a lograr

Vas a correr tu primer programa de Mate y a entender sus tres renglones. Nada más: si
esto anda, tenés todo bien instalado y lo demás es ir sumando de a poco.

Antes de empezar, abrí PowerShell en la carpeta donde está la carpeta `mate` (tenés que
ver `mate` como una carpeta más, no estar adentro). Si no sabés cómo, está explicado en
`mate\README.md`, en "Primeros pasos en Windows".

## El programa

Está en el archivo `mate\curso\clase_01_hola.mate`. Es este:

    # Clase 1: mi primer programa.
    # Los renglones que empiezan con # son comentarios: Mate no los lee, son para vos.

    mostrar("Hola, soy Mate")
    mostrar("Hoy empiezo a programar")
    mostrar("2 + 3 es", 2 + 3)

- `mostrar(...)` escribe en la pantalla lo que le pongas entre los paréntesis.
- Un texto va siempre entre comillas dobles: `"Hola, soy Mate"`.
- Un número o una cuenta van sin comillas: `2 + 3`. Mate hace la cuenta y muestra 5.
- Si a `mostrar` le das varias cosas separadas por comas, las muestra una al lado de la
  otra.

## Cómo se corre

En PowerShell:

    python mate\mate.py correr mate\curso\clase_01_hola.mate

## Lo que tiene que salir

    Hola, soy Mate
    Hoy empiezo a programar
    2 + 3 es 5

## El error más común

Olvidarse las comillas de un texto. Si escribís:

    mostrar(Hola)

Mate cree que `Hola` es el nombre de algo que guardaste, no lo encuentra y te lo dice,
con el número de renglón:

    mate\curso\clase_01_hola.mate:1: error: no existe 'Hola'
        1 | mostrar(Hola)

Se arregla poniendo las comillas: `mostrar("Hola")`. En el Bloc de notas, `Ctrl+G` te
lleva al renglón que dice el error.

## Ejercicio

Hacé un programa tuyo que muestre tu nombre y cuántos minutos tiene un día.

Para escribirlo, creá un archivo de práctica al lado de los del curso (lo vas a usar en
todas las clases):

    notepad mate\curso\practica.mate

El Bloc de notas pregunta si querés crear el archivo: decile que sí. Escribí el programa,
guardá con `Ctrl+S` y corrélo:

    python mate\mate.py correr mate\curso\practica.mate

## Solución

No espíes antes de probar. También está en `mate\curso\clase_01_solucion.mate`.

    # Clase 1, ejercicio resuelto: mi nombre y cuántos minutos tiene un día.

    mostrar("Hola, soy Marta")
    mostrar("Un día tiene", 24 * 60, "minutos")

Tiene que mostrar:

    Hola, soy Marta
    Un día tiene 1440 minutos

Siguiente: clase 2, guardar valores con nombre (`python mate\mate.py curso 2`).
