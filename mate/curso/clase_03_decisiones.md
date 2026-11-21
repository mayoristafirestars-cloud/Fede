# Clase 3: Que el programa decida

## Qué vas a lograr

Vas a hacer que el programa haga una cosa u otra según el caso: un descuento si llevan
muchos, el precio de lista si llevan pocos.

## El programa

Está en `mate\curso\clase_03_decisiones.mate`:

    # Clase 3: que el programa decida.
    # 'si' hace lo que está entre llaves solo cuando la condición es verdadera.

    sea precio = 3500
    sea cantidad = 12
    var total = precio * cantidad

    si cantidad >= 10 {
        mostrar("Lleva 10 o más: tiene 10% de descuento")
        total = total * 0.9
    } sino si cantidad >= 5 {
        mostrar("Lleva 5 o más: tiene 5% de descuento")
        total = total * 0.95
    } sino {
        mostrar("Lleva pocos: paga el precio de lista")
    }

    mostrar("Total: {pesos(total)}")

    # Dos condiciones se juntan con 'y' o con 'o'. 'no' da vuelta una condición.
    sea hay_stock = verdadero
    si hay_stock y cantidad > 0 {
        mostrar("Se puede entregar hoy")
    }

- `si condición { ... }` hace lo que está entre las llaves solo si la condición se cumple.
- `sino si` prueba otra condición cuando la anterior no se cumplió, y `sino` es "en
  cualquier otro caso". `sino` va todo junto.
- Para comparar: `==` (igual), `!=` (distinto), `<`, `<=`, `>`, `>=`.
- `verdadero` y `falso` son valores, como los números. Se juntan con `y`, `o` y `no`.
- La llave `{` va en el mismo renglón que el `si`.

## Cómo se corre

    python mate\mate.py correr mate\curso\clase_03_decisiones.mate

## Lo que tiene que salir

    Lleva 10 o más: tiene 10% de descuento
    Total: $ 37.800,00
    Se puede entregar hoy

Probá cambiar `sea cantidad = 12` por 6 y después por 2, y corrélo de nuevo cada vez.

## El error más común

Comparar con un solo signo igual:

    si cantidad = 10 {

Un solo `=` es para guardar un valor. Para preguntar si dos cosas son iguales van dos:

    mate\curso\clase_03_decisiones.mate:2: error: para comparar se usa '==' (un solo '=' es para
    asignar)
        2 | si cantidad = 10 {

Se arregla con `si cantidad == 10 {`.

## Ejercicio

En tu archivo de práctica: con un precio de 3500 y una cantidad de 4, mostrá el total. Si
el total llega a $ 30.000 el envío es gratis; si no, el envío sale $ 2.500 y hay que
mostrar también el total con envío.

## Solución

También está en `mate\curso\clase_03_solucion.mate`.

    # Clase 3, ejercicio resuelto: el envío es gratis desde $ 30.000.

    sea precio = 3500
    sea cantidad = 4
    sea total = precio * cantidad

    mostrar("Total: {pesos(total)}")
    si total >= 30000 {
        mostrar("El envío es gratis")
    } sino {
        mostrar("El envío sale {pesos(2500)}")
        mostrar("Total con envío: {pesos(total + 2500)}")
    }

Tiene que mostrar:

    Total: $ 14.000,00
    El envío sale $ 2.500,00
    Total con envío: $ 16.500,00

Siguiente: clase 4, listas y bucles (`python mate\mate.py curso 4`).
