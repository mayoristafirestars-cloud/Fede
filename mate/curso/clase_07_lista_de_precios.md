# Clase 7: Tu lista de precios de Excel

## Qué vas a lograr

Vas a hacer que el programa lea una lista de precios de un archivo, en vez de tenerla
escrita adentro. Así, cuando cambia un precio, cambiás la planilla y no el programa.

## El programa

Está en `mate\curso\clase_07_lista_de_precios.mate`, y usa el archivo `precios.csv` que
está en la misma carpeta. Ese archivo es una planilla de muestra, y dice esto:

    producto;precio;stock
    Yerba mate 1 kg;3.500;40
    Azúcar 1 kg;1.250,50;25
    Fideos 500 g;950;0
    Arroz 1 kg;1.800;15
    Aceite 900 ml;$ 2.900;8

El programa:

    # Clase 7: usar tu lista de precios de Excel.
    # leer_tabla() lee una planilla guardada como CSV. Cada fila queda como un mapa, y los
    # nombres de los datos son los títulos de la primera fila: fila.producto, fila.precio...

    sea precios = leer_tabla("precios.csv")
    mostrar("Cargué {largo(precios)} productos de precios.csv")

    para fila en precios {
        si fila.stock == 0 {
            mostrar("- {fila.producto}: {pesos(fila.precio)} (ahora no hay)")
        } sino {
            mostrar("- {fila.producto}: {pesos(fila.precio)}")
        }
    }

    # Busca en la lista el primer producto que tenga esa palabra en el nombre.
    # Si no hay ninguno devuelve 'nada', que es la forma de decir "no hay valor".
    funcion buscar(tabla, palabra) {
        para fila en tabla {
            si tiene(minusculas(fila.producto), minusculas(palabra)) {
                devolver fila
            }
        }
        devolver nada
    }

    sea encontrado = buscar(precios, "arroz")
    mostrar("Busqué arroz y encontré: {encontrado.producto}, a {pesos(encontrado.precio)}")

    prueba "los precios llegan como números" {
        asegurar precios[0].precio == 3500
        asegurar precios[1].precio == 1250.5
    }

    prueba "busca sin importar las mayúsculas" {
        asegurar buscar(precios, "YERBA").precio == 3500
        asegurar buscar(precios, "clavos") == nada
    }

- `leer_tabla("precios.csv")` devuelve una lista con un mapa por cada fila. Los nombres
  de los datos son los títulos de la primera fila, tal cual están escritos:
  `fila.producto`, `fila.precio`, `fila.stock`.
- Los números llegan como números aunque estén escritos a la argentina: `3.500`,
  `1.250,50` y `$ 2.900`. (En la planilla el punto es de los miles; en el programa, no.)
- `tiene(texto, otro)` dice si un texto tiene adentro al otro.
- `nada` es "no hay valor". Sirve para avisar que no se encontró lo que se buscaba.
- El archivo tiene que estar **en la misma carpeta que el programa**.

**Para usar tu propia lista**, desde Excel:

1. La primera fila tiene que tener los títulos, en minúscula y sin espacios: `producto`,
   `precio`, `stock`. Debajo, un producto por fila.
2. Archivo > Guardar como > en "Tipo" elegí **CSV (delimitado por comas) (*.csv)**. Si
   Excel pregunta si querés mantener ese formato, decile que sí.
3. Guardala con el nombre `precios.csv` en la carpeta del programa.

## Cómo se corre

    python mate\mate.py correr mate\curso\clase_07_lista_de_precios.mate

## Lo que tiene que salir

    Cargué 5 productos de precios.csv
    - Yerba mate 1 kg: $ 3.500,00
    - Azúcar 1 kg: $ 1.250,50
    - Fideos 500 g: $ 950,00 (ahora no hay)
    - Arroz 1 kg: $ 1.800,00
    - Aceite 900 ml: $ 2.900,00
    Busqué arroz y encontré: Arroz 1 kg, a $ 1.800,00

Y con `probar`, al final:

      ✓ los precios llegan como números
      ✓ busca sin importar las mayúsculas
    2 de 2 pruebas pasaron

## El error más común

Escribir el título de una columna distinto de como está en la planilla. Si la planilla
dice `precio` y el programa pide `Precio`, con mayúscula:

    mostrar(precios[0].Precio)

Mate dice que ese dato no está y sugiere el parecido:

    mate\curso\clase_07_lista_de_precios.mate:2: error: mapa no tiene un campo 'Precio'. ¿Quisiste
    decir 'precio'?
        2 | mostrar(precios[0].Precio)

El otro tropiezo es darle a `leer_tabla` la planilla de Excel sin convertir
(`precios.xlsx`), o un archivo que no está en la carpeta: en los dos casos el error dice
qué pasó, en qué carpeta buscó y cómo se arregla.

## Ejercicio

En tu archivo de práctica (que está en la misma carpeta que `precios.csv`): calculá
cuánta plata hay en mercadería, o sea, la suma de precio por stock de todos los
productos. Hacelo con una función y escribile una prueba.

## Solución

También está en `mate\curso\clase_07_solucion.mate`.

    # Clase 7, ejercicio resuelto: cuánta plata hay en mercadería (precio por stock).

    sea precios = leer_tabla("precios.csv")

    funcion valor_del_stock(tabla) {
        var total = 0
        para fila en tabla {
            total += fila.precio * fila.stock
        }
        devolver total
    }

    mostrar("En mercadería hay {pesos(valor_del_stock(precios))}")

    prueba "multiplica cada precio por su stock" {
        sea tabla = [{ precio: 100, stock: 2 }, { precio: 50, stock: 0 }]
        asegurar valor_del_stock(tabla) == 200
    }

Tiene que mostrar:

    En mercadería hay $ 221.462,50

Siguiente: clase 8, el primer agente (`python mate\mate.py curso 8`).
