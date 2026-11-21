# Clase 2: Guardar valores con nombre

## Qué vas a lograr

Vas a guardar un precio y una cantidad con su nombre, hacer cuentas con ellos y mostrar el
resultado escrito como plata (`$ 7.000,00`).

## El programa

Está en `mate\curso\clase_02_variables.mate`:

    # Clase 2: guardar valores con nombre.
    # 'sea' guarda un valor que no cambia más. 'var' guarda uno que después puede cambiar.

    sea producto = "yerba"
    sea precio = 3500
    var cantidad = 2

    # Dentro de un texto, lo que va entre llaves se calcula. pesos() lo escribe como plata.
    mostrar("{cantidad} paquetes de {producto} salen {pesos(precio * cantidad)}")

    cantidad = 5
    mostrar("y {cantidad} paquetes salen {pesos(precio * cantidad)}")

    # Un porcentaje se escribe como una cuenta: 21 / 100 (o 0.21).
    sea iva = 21 / 100
    mostrar("El IVA de un paquete es {pesos(precio * iva)}")

- `sea precio = 3500` guarda el 3500 con el nombre `precio`. Un `sea` **no cambia más**:
  así nadie lo pisa sin querer.
- `var cantidad = 2` guarda un valor que **sí puede cambiar**. Para cambiarlo se escribe
  `cantidad = 5`, ya sin el `var`.
- Dentro de un texto, lo que va entre llaves `{ }` se calcula y se pone ahí.
- `pesos(7000)` devuelve el texto `$ 7.000,00`.
- Los números se escriben sin punto de miles: `3500`. El punto es el de los decimales.

## Cómo se corre

    python mate\mate.py correr mate\curso\clase_02_variables.mate

## Lo que tiene que salir

    2 paquetes de yerba salen $ 7.000,00
    y 5 paquetes salen $ 17.500,00
    El IVA de un paquete es $ 735,00

## El error más común

Escribir el precio como en la Argentina, con punto de miles:

    sea precio = 3.500

Para Mate eso sería tres y medio. Como casi siempre se quiso decir tres mil quinientos,
frena y lo explica:

    mate\curso\clase_02_variables.mate:1: error: en Mate el punto es el de los decimales: 3.500
    vale 3.5, no 3500. Si querías decir 3500, escribilo sin punto (3500) o con guion bajo (3_500);
    si era el decimal, escribí 3.5
        1 | sea precio = 3.500

Se arregla escribiendo `3500` (o `3_500`, si te resulta más fácil de leer).

El otro error de esta clase es querer cambiar un `sea`. Si el valor tiene que cambiar,
se declara con `var`.

## Ejercicio

En tu archivo de práctica (`notepad mate\curso\practica.mate`), guardá otro producto con
su precio, calculá cuánto salen 3 y mostrá el total y el total con IVA (21%).

    python mate\mate.py correr mate\curso\practica.mate

## Solución

También está en `mate\curso\clase_02_solucion.mate`.

    # Clase 2, ejercicio resuelto: otro producto, tres unidades y el total con IVA.

    sea producto = "azúcar"
    sea precio = 1200
    sea cantidad = 3
    sea iva = 21 / 100

    sea subtotal = precio * cantidad
    mostrar("{cantidad} paquetes de {producto} salen {pesos(subtotal)}")
    mostrar("Con IVA: {pesos(subtotal + subtotal * iva)}")

Tiene que mostrar:

    3 paquetes de azúcar salen $ 3.600,00
    Con IVA: $ 4.356,00

Siguiente: clase 3, que el programa decida (`python mate\mate.py curso 3`).
