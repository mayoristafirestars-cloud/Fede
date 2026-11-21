# Clase 5: Funciones y pruebas

## Qué vas a lograr

Vas a ponerle nombre a una cuenta para usarla muchas veces (una función) y a escribir
pruebas que comprueban solas que la cuenta está bien. Las pruebas son lo que te deja
cambiar un programa sin miedo a romperlo.

## El programa

Está en `mate\curso\clase_05_funciones.mate`:

    # Clase 5: funciones y pruebas.
    # Una función es una cuenta con nombre: se escribe una vez y se usa muchas.

    funcion total_de(precio, cantidad) {
        si cantidad >= 10 {
            devolver precio * cantidad * 0.9
        }
        devolver precio * cantidad
    }

    mostrar("2 paquetes: {pesos(total_de(3500, 2))}")
    mostrar("10 paquetes: {pesos(total_de(3500, 10))}")

    # Una prueba comprueba sola que la función da lo que tiene que dar.
    # No corren con 'correr': corren con 'probar'.
    prueba "con menos de 10 no hay descuento" {
        asegurar total_de(100, 2) == 200
    }

    prueba "desde 10 hay 10% de descuento" {
        asegurar total_de(100, 10) == 900
    }

- `funcion total_de(precio, cantidad) { ... }` declara la función. Lo que va entre
  paréntesis son los datos que recibe.
- `devolver` termina la función y entrega el resultado.
- La función se usa escribiendo su nombre y los datos: `total_de(3500, 2)`.
- `prueba "nombre" { ... }` es una comprobación. Adentro, `asegurar` dice qué tiene que
  cumplirse. Si no se cumple, la prueba falla y Mate muestra qué dio y qué se esperaba.
- `funcion` se escribe sin tilde.

## Cómo se corre

Como siempre:

    python mate\mate.py correr mate\curso\clase_05_funciones.mate

Y para correr las pruebas, con `probar` en lugar de `correr`:

    python mate\mate.py probar mate\curso\clase_05_funciones.mate

## Lo que tiene que salir

Con `correr`:

    2 paquetes: $ 7.000,00
    10 paquetes: $ 31.500,00

Con `probar` (primero corre el programa y después las pruebas):

    2 paquetes: $ 7.000,00
    10 paquetes: $ 31.500,00
      ✓ con menos de 10 no hay descuento
      ✓ desde 10 hay 10% de descuento
    2 de 2 pruebas pasaron

## El error más común

Olvidarse el `devolver`. La función hace la cuenta pero no entrega nada, así que lo que
vuelve es `nada`:

    funcion total_de(precio, cantidad) {
        sea total = precio * cantidad
    }

Mate lo explica cuando querés usar ese resultado:

    mate\curso\clase_05_funciones.mate:4: error: no se puede sumar el valor nada con un número.
    'nada' es la falta de valor: ¿a la función le falta un 'devolver', o es un campo opcional que
    vino vacío?
        4 | mostrar(total_de(3500, 2) + 100)

Se arregla terminando la función con `devolver total`.

Y así se ve una prueba que falla (acá se esperaba 950 a propósito, y da 900):

      ✗ desde 10 hay 10% de descuento
          mate\curso\clase_05_funciones.mate:9: error: no se cumplió lo asegurado: dio 900 y se
          esperaba 950
              9 |     asegurar total_de(100, 10) == 950
    0 de 1 pruebas pasaron

## Ejercicio

En tu archivo de práctica: escribí una función `con_iva(precio)` que devuelva el precio
más el 21%, mostrá cuánto sale con IVA algo de $ 3.500 y escribile dos pruebas.

    python mate\mate.py probar mate\curso\practica.mate

## Solución

También está en `mate\curso\clase_05_solucion.mate`.

    # Clase 5, ejercicio resuelto: una función que suma el IVA, con su prueba.

    funcion con_iva(precio) {
        devolver precio + precio * 21 / 100
    }

    mostrar("Con IVA: {pesos(con_iva(3500))}")

    prueba "le suma el 21%" {
        asegurar con_iva(100) == 121
    }

    prueba "si es gratis sigue siendo gratis" {
        asegurar con_iva(0) == 0
    }

Con `probar` tiene que mostrar:

    Con IVA: $ 4.235,00
      ✓ le suma el 21%
      ✓ si es gratis sigue siendo gratis
    2 de 2 pruebas pasaron

Siguiente: clase 6, que el programa te pregunte (`python mate\mate.py curso 6`).
