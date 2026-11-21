# Clase 4: Listas y bucles

## Qué vas a lograr

Vas a guardar varios productos juntos y a recorrerlos uno por uno, para mostrarlos y para
sumar sus precios.

## El programa

Está en `mate\curso\clase_04_listas.mate`:

    # Clase 4: muchas cosas juntas.
    # Una lista va entre corchetes. Un mapa va entre llaves y le pone nombre a cada dato.

    sea productos = [
        { nombre: "Yerba", precio: 3500 },
        { nombre: "Azúcar", precio: 1200 },
        { nombre: "Fideos", precio: 950 },
    ]

    # 'para' repite lo que está entre llaves una vez por cada elemento de la lista.
    var total = 0
    para p en productos {
        mostrar("- {p.nombre}: {pesos(p.precio)}")
        total += p.precio
    }
    mostrar("Son {largo(productos)} productos y suman {pesos(total)}")

    # El primero de la lista está en la posición 0.
    mostrar("El primero es {productos[0].nombre}")

    # agregar() no cambia la lista: devuelve una lista nueva, con uno más.
    sea con_arroz = agregar(productos, { nombre: "Arroz", precio: 1800 })
    mostrar("Con el arroz son {largo(con_arroz)}")

- Una **lista** va entre corchetes, con sus elementos separados por comas: `[1, 2, 3]`.
- Un **mapa** va entre llaves y le pone nombre a cada dato:
  `{ nombre: "Yerba", precio: 3500 }`. Cada dato se saca con un punto: `p.nombre`.
- `para p en productos { ... }` repite lo de las llaves una vez por cada elemento, y en
  cada vuelta `p` es el elemento que toca.
- `total += p.precio` es la forma corta de `total = total + p.precio`.
- `largo(lista)` dice cuántos elementos tiene.
- Las posiciones se cuentan desde 0: `productos[0]` es el primero.

## Cómo se corre

    python mate\mate.py correr mate\curso\clase_04_listas.mate

## Lo que tiene que salir

    - Yerba: $ 3.500,00
    - Azúcar: $ 1.200,00
    - Fideos: $ 950,00
    Son 3 productos y suman $ 5.650,00
    El primero es Yerba
    Con el arroz son 4

## El error más común

Creer que `agregar` cambia la lista. No la cambia: devuelve una lista nueva. Si escribís
el renglón suelto, sin guardar lo que devuelve:

    agregar(productos, "Arroz")

Mate te avisa que ese renglón no sirve para nada:

    mate\curso\clase_04_listas.mate:2: error: agregar() no cambia la lista: devuelve una nueva.
    Guardá el resultado: lista = agregar(lista, ...)
        2 | agregar(productos, "Arroz")

Se arregla guardando el resultado. Si la lista es un `var`, se puede guardar en ella
misma: `productos = agregar(productos, "Arroz")`.

## Ejercicio

En tu archivo de práctica: con la misma lista de productos, mostrá solo los que salen más
de $ 1.000 y al final decí cuántos son. (Pista: un `si` adentro del `para`.)

## Solución

También está en `mate\curso\clase_04_solucion.mate`.

    # Clase 4, ejercicio resuelto: mostrar solo los que salen más de $ 1.000 y contarlos.

    sea productos = [
        { nombre: "Yerba", precio: 3500 },
        { nombre: "Azúcar", precio: 1200 },
        { nombre: "Fideos", precio: 950 },
    ]

    var caros = 0
    para p en productos {
        si p.precio > 1000 {
            mostrar("- {p.nombre}: {pesos(p.precio)}")
            caros += 1
        }
    }
    mostrar("Hay {caros} productos de más de {pesos(1000)}")

Tiene que mostrar:

    - Yerba: $ 3.500,00
    - Azúcar: $ 1.200,00
    Hay 2 productos de más de $ 1.000,00

Siguiente: clase 5, funciones y pruebas (`python mate\mate.py curso 5`).
