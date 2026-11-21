# Clase 8: El primer agente

## Qué vas a lograr

Vas a crear un agente: una parte del programa que trabaja como un empleado. Tiene sus
propios datos, recibe mensajes y los contesta. Y vas a ver qué es un mensaje "con
contrato": Mate no deja pasar un pedido mal armado.

## El programa

Está en `mate\curso\clase_08_agente.mate`:

    # Clase 8: el primer agente.
    # Un agente es como un empleado: tiene sus datos (su 'estado') y contesta los mensajes
    # que sabe recibir. Nadie más puede tocar sus datos.

    # Un 'mensaje' dice qué datos lleva y de qué tipo es cada uno: ese es su contrato.
    mensaje Pedido { producto: texto, cantidad: numero desde 1 hasta 100 }
    mensaje Cotizacion { producto: texto, total: numero }

    agente Vendedor {
        estado precios = { yerba: 3500, azucar: 1250 }
        estado atendidos = 0

        al recibir Pedido como p {
            si no tiene(precios, p.producto) {
                fallar "no vendo {p.producto}"
            }
            atendidos += 1
            sea total = precios[p.producto] * p.cantidad
            responder Cotizacion { producto: p.producto, total: total }
        }
    }

    # 'preguntar' le manda el mensaje al agente y espera su respuesta.
    sea c = preguntar Pedido { producto: "yerba", cantidad: 3 } a Vendedor
    mostrar("3 de {c.producto} salen {pesos(c.total)}")

    # Si el agente falla, el error le llega al que preguntó, que lo puede atajar.
    intentar {
        sea otra = preguntar Pedido { producto: "clavos", cantidad: 1 } a Vendedor
        mostrar(otra.total)
    } si falla motivo {
        mostrar("El vendedor no pudo: {motivo}")
    }

    prueba "cotiza precio por cantidad" {
        sea r = preguntar Pedido { producto: "azucar", cantidad: 2 } a Vendedor
        asegurar r.total == 2500
    }

    prueba "el contrato no deja pedir 500" {
        asegurar falla { Pedido { producto: "yerba", cantidad: 500 } }
    }

- `mensaje Pedido { ... }` declara qué datos lleva un pedido y de qué tipo es cada uno
  (`texto`, `numero`...). `desde 1 hasta 100` le pone límites a la cantidad. Eso es el
  **contrato**: un pedido que no lo cumple no se puede ni armar.
- `agente Vendedor { ... }` declara al agente. Sus `estado` son sus datos privados: nadie
  de afuera los puede tocar.
- `al recibir Pedido como p { ... }` es lo que hace cuando le llega un pedido. Adentro,
  `p.producto` y `p.cantidad` son los datos de ese pedido.
- `responder` contesta. `fallar "motivo"` corta con un error que le llega al que preguntó.
- `preguntar Pedido { ... } a Vendedor` manda el mensaje y espera la respuesta.
- Los nombres de mensajes y agentes empiezan con mayúscula; los demás, con minúscula.

## Cómo se corre

    python mate\mate.py correr mate\curso\clase_08_agente.mate

Para ver la conversación, mensaje por mensaje, agregale `--traza`:

    python mate\mate.py correr mate\curso\clase_08_agente.mate --traza

## Lo que tiene que salir

    3 de yerba salen $ 10.500,00
    El vendedor no pudo: no vendo clavos

Con `--traza`, además, se ve cada mensaje que va y viene:

      ·  1. (programa) pregunta a Vendedor: Pedido { producto: "yerba", cantidad: 3 }
      (conversación 1)
      ·  1. Vendedor responde a (programa): Cotizacion { producto: "yerba", total: 10500 }
    3 de yerba salen $ 10.500,00
      ·  2. (programa) pregunta a Vendedor: Pedido { producto: "clavos", cantidad: 1 }
      (conversación 2)
      ·  2. Vendedor falló: no vendo clavos
    El vendedor no pudo: no vendo clavos

## El error más común

Armar un mensaje que no cumple su contrato: un dato de otro tipo, un nombre mal escrito
o un dato que falta. Por ejemplo, la cantidad entre comillas (un texto, no un número):

    sea c = preguntar Pedido { producto: "yerba", cantidad: "3" } a Vendedor

Mate lo avisa **antes de correr**, así que el programa ni arranca con ese error adentro:

    mate\curso\clase_08_agente.mate:9: error: Pedido.cantidad es de tipo numero, no texto
        9 | sea c = preguntar Pedido { producto: "yerba", cantidad: "3" } a Vendedor

Se arregla sacando las comillas: `cantidad: 3`.

## Ejercicio

El Vendedor ya cuenta los pedidos que atiende (`atendidos`), pero nadie se lo puede
preguntar. Copiá el programa en tu archivo de práctica, agregá un mensaje `CuantosVan`
(sin datos: `mensaje CuantosVan {}`) y hacé que el Vendedor conteste cuántos pedidos
atendió. Escribile una prueba.

## Solución

También está en `mate\curso\clase_08_solucion.mate`.

    # Clase 8, ejercicio resuelto: el Vendedor también sabe decir cuántos pedidos atendió.

    mensaje Pedido { producto: texto, cantidad: numero desde 1 hasta 100 }
    mensaje Cotizacion { producto: texto, total: numero }
    mensaje CuantosVan {}

    agente Vendedor {
        estado precios = { yerba: 3500, azucar: 1250 }
        estado atendidos = 0

        al recibir Pedido como p {
            si no tiene(precios, p.producto) {
                fallar "no vendo {p.producto}"
            }
            atendidos += 1
            sea total = precios[p.producto] * p.cantidad
            responder Cotizacion { producto: p.producto, total: total }
        }

        al recibir CuantosVan {
            responder atendidos
        }
    }

    sea c = preguntar Pedido { producto: "yerba", cantidad: 3 } a Vendedor
    mostrar("3 de {c.producto} salen {pesos(c.total)}")
    sea van = preguntar CuantosVan {} a Vendedor
    mostrar("El vendedor atendió {van} pedido(s)")

    prueba "cuenta los pedidos que atendió" {
        sea uno = preguntar Pedido { producto: "yerba", cantidad: 1 } a Vendedor
        sea dos = preguntar Pedido { producto: "azucar", cantidad: 1 } a Vendedor
        asegurar uno.total + dos.total == 4750
        asegurar (preguntar CuantosVan {} a Vendedor) == 2
    }

    prueba "un pedido que falla no cuenta" {
        asegurar falla { preguntar Pedido { producto: "clavos", cantidad: 1 } a Vendedor }
        asegurar (preguntar CuantosVan {} a Vendedor) == 0
    }

Con `probar` tiene que mostrar:

    3 de yerba salen $ 10.500,00
    El vendedor atendió 1 pedido(s)
      ✓ cuenta los pedidos que atendió
      ✓ un pedido que falla no cuenta
    2 de 2 pruebas pasaron

Fijate en la segunda prueba: el pedido de clavos falló y no quedó contado. Cuando un
agente falla atendiendo un mensaje, sus datos vuelven a como estaban antes.

Siguiente: clase 9, un agente que consulta a una IA (`python mate\mate.py curso 9`).
