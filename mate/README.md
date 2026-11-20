# Mate 🧉

Un lenguaje chico, con palabras en español, pensado para dos cosas:

1. **Escribir código más práctico y con menos sorpresas.**
2. **Que los agentes se hablen entre ellos** con mensajes que tienen contrato.

Versión 0.2. El intérprete es un solo archivo (`mate.py`), sin dependencias: alcanza con Python 3.

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

En Windows (PowerShell) es lo mismo con `python` y barras al revés:

```
python mate\mate.py correr mate\ejemplos\hola.mate
```

## La línea de comandos

| Qué escribís | Qué hace |
|---|---|
| `correr archivo.mate` | corre el programa (también alcanza con poner solo `archivo.mate`) |
| `probar archivo.mate` | corre las pruebas que el programa trae adentro |
| `verificar archivo.mate` | revisa el programa sin correrlo |
| `ayuda` | muestra las órdenes y un ejemplo listo para copiar |
| `--traza` | muestra la conversación entre agentes, mensaje por mensaje |
| `--sin-limite` | no corta los programas que dan muchísimos pasos |
| `--depurar` | si Mate falla por dentro, muestra el detalle técnico |
| `--version` | dice qué versión de Mate es |

Si te equivocás al tipear, Mate te lo dice en vez de seguir de largo: `corer` sugiere `correr`,
`--trasa` sugiere `--traza`, y si el archivo no está te muestra los `.mate` que sí hay en esa
carpeta. Si el Bloc de notas lo guardó como `hola.mate.txt`, también te avisa.

## Cuando algo sale mal

Mate nunca debería mostrarte un error de Python en inglés:

- **Archivos del Bloc de notas**: se leen guardados como UTF-8, "Unicode" o ANSI, con o sin `ñ`.
- **Cosas pegadas desde Word o WhatsApp**: las comillas curvas `“así”` y los espacios raros se
  aceptan como los comunes.
- **Costumbres de otros lenguajes**: para `;`, `&&`, `||`, `!`, `//`, comillas simples o un texto
  sin cerrar, el error explica cómo se escribe en Mate.
- **Programas que nunca terminan**: después de 10.000.000 de pasos Mate corta y dice en qué
  renglón estaba (un `mientras` cuya condición nunca cambia, casi siempre). Ese corte no se
  puede atajar con `intentar`. Con `--sin-limite` se desactiva.
- **Ctrl+C** corta el programa y dice en qué renglón iba.
- **Números imposibles**: una cuenta que da un número demasiado grande es un error con su
  renglón, y `numero("inf")` o `numero("nan")` no se aceptan.
- **Consolas viejas de Windows**: si no pueden mostrar `✓`, `✗` o `→`, Mate escribe `OK`,
  `FALLA` y `->`.
- **El renglón del error**: debajo del mensaje Mate muestra el renglón señalado, por ejemplo
  `    2 | mostrar(totl)`. Para ir a ese renglón en el Bloc de notas: `Ctrl+G` y el número.
- **Nombres mal tipeados**: si escribís `totl` y existe `total`, o `mostar` en vez de
  `mostrar`, el error termina con `¿Quisiste decir 'total'?`. Vale también para campos,
  claves de mapas, mensajes y agentes.
- **Palabras de otros lenguajes, con tilde o con mayúscula**: `print`, `if`, `else`, `true`,
  `función`, `número` o `Si` no se aceptan, pero el error dice cómo se escribe en Mate
  (`mostrar`, `si`, `sino`, `verdadero`, `funcion`, `numero`, `si`).
- **Condiciones mal escritas**: `si x = 5`, `si 1 < x < 10`, `si x > 3 y < 10` y
  `si x > 3 entonces` explican cómo va cada una (`==`, `1 < x y x < 10`, repetir la variable,
  y la llave `{` directamente).
- **Nombres que no se pueden usar**: `sea y = 1` avisa que `y` es una palabra propia de Mate, y
  `sea texto = "hola"` que `texto` es una función incluida; en los dos casos hay que elegir otro
  nombre. Como nombre de *campo* sí valen las palabras propias de Mate:
  `mensaje Envio { estado: texto, para: texto }` y después `e.estado`.
- **"No se puede cambiar"**: el error dice por qué: es un `sea`, un parámetro, la variable del
  `para`, el mensaje recibido, una función o un agente.
- **Un `asegurar` que falla muestra los valores**: `asegurar a + 1 == 4` dice
  `no se cumplió lo asegurado: dio 3 y se esperaba 4`.
- Si igual aparece "error interno de Mate", no es culpa tuya: corré de nuevo con `--depurar`
  y guardá lo que muestra.

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
- `responder valor` contesta al `remitente` y termina de atender ese mensaje. Solo va dentro de
  `al recibir` (o de una función del agente); `devolver` va dentro de una función, o dentro de
  `al recibir` para terminar sin contestar. Fuera de lugar, Mate lo avisa antes de correr.
- `yo` es el agente que está atendiendo; sirve para mandarse a sí mismo dentro de un mensaje.
- `--traza` muestra la conversación entera, mensaje por mensaje.
- `a_json(mensaje)` y `de_json(texto)` pasan los mensajes a JSON y de vuelta, validando el contrato.

### Varias copias de un agente

Declarar un `agente` ya crea uno con ese nombre. Con `crear` nacen más, cada uno con su estado:

```
sea norte = crear Vendedor llamado "Norte" { descuento: 0.05 }
sea sur = crear Vendedor llamado "Sur" { precios: { yerba: 3300 } }
sea otro = crear Vendedor
```

Entre llaves va el estado inicial que querés distinto; el resto arranca como en la declaración.
`llamado` le pone nombre para la traza (`Vendedor Norte`); sin eso se llama `Vendedor#2`.
Las copias se guardan en variables y se pueden mandar dentro de un mensaje (tipo `agente` o `lista`).

### Varios archivos

```
usar "catalogo.mate"
```

Trae los mensajes, agentes, funciones y valores `sea` del otro archivo (se busca al lado del que
lo usa). Lo que ese archivo ejecuta y sus pruebas no se traen, así que un mismo archivo sirve como
programa y como biblioteca. Usarlo dos veces no molesta. Ver `ejemplos/mercado.mate`.

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
`minusculas`, `a_json`, `de_json`, `pesos`.

### Números y plata

- Los decimales se muestran limpios: `mostrar(0.1 + 0.2)` muestra `0.3` y `mostrar(10 / 3)`
  muestra `3.33333333333`. Es solo cómo se ven: por dentro la cuenta sigue teniendo su resto
  minúsculo, así que `0.1 + 0.2 == 0.3` da `falso`. Para comparar plata, redondeá antes:
  `redondear(a, 2) == redondear(b, 2)`.
- `redondear(2.5)` da `3` y `redondear(2.675, 2)` da `2.68`: el medio va siempre hacia arriba,
  como en la escuela. En los negativos se aleja del cero: `redondear(-2.5)` da `-3`.
- `pesos(1234567.891)` devuelve el texto `$ 1.234.567,89`; `pesos(3500, 0)` devuelve `$ 3.500`
  (el segundo valor es la cantidad de decimales, de 0 a 6). Los negativos salen `-$ 1.500,00`.
- `numero("1.234,50")` da `1234.5` y `numero("$ 7,25")` da `7.25`: entiende la coma decimal, el
  punto de miles y el signo `$`. Ojo: con un solo punto y sin coma, el punto es decimal
  (`numero("3.500")` da `3.5`); con dos o más puntos son miles (`numero("1.234.567")`). Un texto
  vacío o que no es un número (`"1e5"`, `"hola"`) es un error.

Los nombres de mensajes y agentes empiezan con mayúscula; el resto, con minúscula.

Detalles: `partir("abc", "")` separa letra por letra; `redondear(3.14159, 2)` lleva una cantidad
entera de decimales; las claves de un mapa son siempre textos (`tiene(mapa, [1])` da `falso`);
solo se puede asignar a una variable o a una parte de ella (`x`, `x.campo`, `x[0]`).

## Límites de la versión 0.2

- Los agentes corren todos dentro del mismo programa, de a uno y en orden (por eso el resultado
  es siempre el mismo). Todavía no se conectan con agentes de IA reales ni entre máquinas.
- Dentro de `"{...}"` no se puede escribir otro texto entre comillas; se guarda antes en un `sea`.
- Todo lo que trae `usar` queda en un único espacio de nombres: dos archivos no pueden declarar
  algo con el mismo nombre.

## Pruebas del intérprete

```bash
python3 -m pytest mate/pruebas -q -p no:cacheprovider
```
