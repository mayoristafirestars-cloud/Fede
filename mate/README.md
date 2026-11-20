# Mate 🧉

Un lenguaje chico, con palabras en español, pensado para dos cosas:

1. **Escribir código más práctico y con menos sorpresas.**
2. **Que los agentes se hablen entre ellos** con mensajes que tienen contrato.

Versión 0.1. El intérprete es un solo archivo (`mate.py`), sin dependencias: alcanza con Python 3.

```bash
python3 mate/mate.py correr mate/ejemplos/negociacion.mate
```

```bash
python3 mate/mate.py correr mate/ejemplos/equipo.mate --traza
```

```bash
python3 mate/mate.py probar mate/ejemplos/negociacion.mate
```

```bash
python3 mate/mate.py verificar mate/ejemplos/negociacion.mate
```

## Un ejemplo

```
mensaje Pedido { producto: texto, cantidad: numero }
mensaje Cotizacion { producto: texto, total: numero }

agente Vendedor {
    estado precios = { yerba: 3500, azucar: 1200 }

    al recibir Pedido como p {
        si no tiene(precios, p.producto) {
            fallar "no vendo {p.producto}"
        }
        responder Cotizacion { producto: p.producto, total: precios[p.producto] * p.cantidad }
    }
}

sea c = preguntar Pedido { producto: "yerba", cantidad: 3 } a Vendedor
mostrar("Total: {c.total}")

prueba "cotiza precio por cantidad" {
    sea c = preguntar Pedido { producto: "azucar", cantidad: 2 } a Vendedor
    asegurar c.total == 2400
}
```

## Qué lo hace más práctico

| Idea | Cómo se ve |
|---|---|
| Los valores son fijos salvo que digas lo contrario | `sea iva = 0.21` no cambia; `var total = 0` sí |
| Nada se convierte a escondidas | `"precio: " + 100` es un error; se escribe `"precio: {100}"` |
| Las condiciones son `verdadero` o `falso`, nunca "algo parecido" | `si 1 { }` es un error |
| Modificar una copia no toca el original | `var b = a` y después `b.n[0] = 99` deja `a` intacto |
| Los errores dicen la línea y se pueden atajar | `intentar { ... } si falla e { ... }` |
| Las pruebas viven al lado del código | `prueba "nombre" { asegurar ... }` y `mate probar` |

## Cómo hablan los agentes

- `mensaje Nombre { campo: tipo }` declara el **contrato** de un mensaje. Tipos: `numero`,
  `texto`, `logico`, `lista`, `mapa`, `agente`, `cualquiera` u otro mensaje. `tipo?` lo hace opcional.
- `agente Nombre { ... }` tiene su `estado` privado y un `al recibir Tipo como x { }` por cada
  mensaje que entiende. Ningún agente puede tocar el estado de otro ni las variables de afuera.
- `enviar Mensaje { ... } a Agente` lo deja en la cola y sigue (asíncrono).
- `preguntar Mensaje { ... } a Agente` espera y devuelve la respuesta. Si el otro agente falla,
  el error le llega al que preguntó.
- `responder valor` contesta al `remitente` y termina de atender ese mensaje.
- `--traza` muestra la conversación entera, mensaje por mensaje.
- `a_json(mensaje)` y `de_json(texto)` pasan los mensajes a JSON y de vuelta, validando el contrato.

**Antes de correr**, Mate revisa los contratos: avisa si a un mensaje le falta o le sobra un
campo, si un valor literal es del tipo equivocado, o si le mandás a un agente algo que no sabe
recibir. Lo que no se puede saber de antemano se valida al construir el mensaje.

## Referencia rápida

```
# comentario
sea x = 1                  var y = [1, 2]             y[0] = 5
funcion doble(n) { devolver n * 2 }
si a > b { } sino si a == b { } sino { }
mientras cond { }          para item en lista { }
y  o  no   ==  !=  <  <=  >  >=   +  -  *  /  %
{ nombre: "yerba", precio: 3500 }       mapa.nombre      mapa["nombre"]
```

Funciones incluidas: `mostrar`, `largo`, `texto`, `numero`, `tipo`, `tiene`, `claves`, `valores`,
`agregar`, `quitar`, `rango`, `sumar`, `ordenar`, `redondear`, `unir`, `partir`, `mayusculas`,
`minusculas`, `a_json`, `de_json`.

Los nombres de mensajes y agentes empiezan con mayúscula; el resto, con minúscula.

## Límites de la versión 0.1

- Los agentes corren todos dentro del mismo programa, de a uno y en orden (por eso el resultado
  es siempre el mismo). Todavía no se conectan con agentes de IA reales ni entre máquinas.
- Cada `agente` es único: no se pueden crear varias copias del mismo.
- Dentro de `"{...}"` no se puede escribir otro texto entre comillas; se guarda antes en un `sea`.
- No hay módulos ni forma de importar otros archivos.

## Pruebas del intérprete

```bash
python3 -m pytest mate/pruebas -q
```
