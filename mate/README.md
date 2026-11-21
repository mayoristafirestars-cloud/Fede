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

## Primeros pasos en Windows

No hace falta saber programar ni instalar nada más que Python.

**1. Instalar Python (una sola vez).** Bajalo de `python.org/downloads` y abrí el instalador.
En la primera pantalla, abajo, marcá la casilla **"Add python.exe to PATH"** antes de tocar
"Install Now". Sin esa casilla, Windows después no encuentra a Python.

**2. Abrir PowerShell en la carpeta de trabajo.** En el Explorador de archivos entrá a la
carpeta donde está la carpeta `mate` (tenés que ver `mate` como una carpeta más, no estar
adentro). Hacé clic en la barra de arriba donde figura la dirección, escribí `powershell` y
apretá Enter. Se abre una ventana azul o negra: ahí se escriben las órdenes. Para comprobar
que Python quedó bien instalado:

```
python --version
```

Tiene que contestar algo como `Python 3.12.4`. Si dice que `python` "no se reconoce", cerrá
PowerShell, volvé a correr el instalador marcando la casilla del paso 1 y abrí PowerShell de nuevo.

**3. Escribir el programa en el Bloc de notas.** En esa misma ventana escribí:

```
notepad hola.mate
```

El Bloc de notas pregunta si querés crear el archivo: decile que sí. Escribí este renglón y
guardá con `Ctrl+S`:

```
mostrar("Hola desde Mate")
```

Si en cambio creás el archivo desde el Bloc de notas con "Guardar como", elegí
**Tipo: Todos los archivos** y **Codificación: UTF-8**; si no, queda como `hola.mate.txt`
(Mate igual te avisa cuando pasa).

**4. Correrlo.** De vuelta en PowerShell:

```
python mate\mate.py correr hola.mate
```

Tiene que aparecer `Hola desde Mate`. Con la flecha para arriba vuelve la última orden, así no
hay que tipearla de nuevo cada vez que cambiás el programa.

**5. Para escribir menos: `mate.bat`.** Al lado de `mate.py` hay un `mate.bat` que hace lo mismo
con una orden más corta:

```
.\mate\mate correr hola.mate
```

También podés arrastrar un archivo `.mate` con el mouse y soltarlo encima de `mate.bat`: lo
corre y deja la ventana abierta hasta que apretás una tecla. (El `mate.bat` se escribió con
cuidado pero todavía no se probó en una Windows de verdad: si hace algo raro, la orden larga
del paso 4 anda siempre.)

**6. Si algo sale mal.** Mate te dice el archivo, el número de renglón y qué pasó, en
castellano. En el Bloc de notas, `Ctrl+G` te lleva a ese renglón.

**7. Seguir aprendiendo.** En `mate\ejemplos` hay seis programas cortos, explicados renglón por
renglón, para leer y correr en orden:

| Archivo | Qué enseña |
|---|---|
| `01_hola.mate` | mostrar algo en pantalla |
| `02_variables.mate` | guardar valores con `sea` y `var`, plata y textos |
| `03_decisiones.mate` | `si`, `sino si`, `sino` |
| `04_listas_y_bucles.mate` | listas, mapas, `para`, `mientras`, `romper` y `continuar` |
| `05_funciones_y_pruebas.mate` | funciones, errores atajados y pruebas |
| `06_primer_agente.mate` | el primer agente con sus mensajes |

```
python mate\mate.py correr mate\ejemplos\01_hola.mate
```

**8. Pedirle un programa a una IA.** Esta orden imprime una página con todo Mate:

```
python mate\mate.py guia
```

Copiá lo que muestra y pegalo al empezar un chat con un asistente (Claude, por ejemplo) antes
de pedirle el programa: así escribe Mate de verdad y no inventa palabras. Para guardarla en un
archivo y abrirla con el Bloc de notas: `python mate\mate.py guia > guia.txt`.

## La línea de comandos

| Qué escribís | Qué hace |
|---|---|
| `correr archivo.mate` | corre el programa (también alcanza con poner solo `archivo.mate`) |
| `probar archivo.mate` | corre las pruebas que el programa trae adentro |
| `verificar archivo.mate` | revisa el programa sin correrlo |
| `guia` | imprime una página con todo Mate, para pegarle a una IA (`python mate\mate.py guia`) |
| `ayuda` | muestra las órdenes y un ejemplo listo para copiar |
| `--traza` | muestra la conversación entre agentes, mensaje por mensaje |
| `--traza=conversacion.txt` | guarda esa conversación en un archivo, con un resumen al final |
| `--sin-limite` | no corta los programas que dan muchísimos pasos |
| `--depurar` | si Mate falla por dentro, muestra el detalle técnico |
| `--version` | dice qué versión de Mate es |

Si te equivocás al tipear, Mate te lo dice en vez de seguir de largo: `corer` sugiere `correr`,
`--trasa` sugiere `--traza`, y si el archivo no está te muestra los `.mate` que sí hay en esa
carpeta. Si el Bloc de notas lo guardó como `hola.mate.txt`, también te avisa (y si le pasás
ese nombre completo, lo corre igual con un aviso). La orden va siempre primero: si escribís
`hola.mate probar`, Mate te dice que es `probar hola.mate`.

## Cuando algo sale mal

Mate nunca debería mostrarte un error de Python en inglés:

- **Archivos del Bloc de notas**: se leen guardados como UTF-8, "Unicode" o ANSI, con o sin `ñ`.
- **Cosas pegadas desde Word o WhatsApp**: las comillas curvas `“así”` y los espacios raros o
  invisibles se aceptan como los comunes. Si queda algún otro carácter que no se ve, el error
  dice después de qué está, para borrarlo y escribirlo de nuevo.
- **Costumbres de otros lenguajes**: para `;`, `&&`, `||`, `!`, `//`, comillas simples o un texto
  sin cerrar, el error explica cómo se escribe en Mate.
- **Programas que nunca terminan**: después de 10.000.000 de pasos Mate corta y dice en qué
  renglón estaba (un `mientras` cuya condición nunca cambia, casi siempre). Con `--sin-limite`
  se desactiva, para los programas que son largos de verdad.
- **Topes de seguridad**: además de ese freno, Mate corta una función que se llama a sí misma
  demasiadas veces (`demasiada recursión`, hoy cerca de 120 llamadas) y los programas que se
  quedan sin memoria. Ninguno de esos cortes se puede atajar con `intentar`.
- **Cosas demasiado grandes**: un texto o una lista de más de 10.000.000 de elementos
  (`rango(100000000000)`, un texto que se duplica sin parar) o un número entero de más de unas
  4.000 cifras son un error común, con su renglón, en vez de colgar la consola.
- **Ctrl+C** corta el programa y dice en qué renglón iba.
- **Números imposibles**: una cuenta que da un número demasiado grande es un error con su
  renglón, y `numero("inf")` o `numero("nan")` no se aceptan.
- **Consolas viejas de Windows**: si no pueden mostrar `✓`, `✗` o `→`, Mate escribe `OK`,
  `FALLA` y `->`.
- **Llaves, paréntesis y corchetes sin cerrar**: en vez de quejarse del final del archivo, el
  error dice dónde se abrió: `la llave que se abrió en la línea 4 (al recibir Ping) nunca se
  cierra`.
- **Un renglón que no hace nada**: `i + 1` suelto, `mostrar "hola"` sin paréntesis o
  `agregar(lista, 4)` sin guardar el resultado antes pasaban en silencio. Ahora son un error
  que dice qué faltó (`este renglón calcula un valor y no hace nada con él`, `a 'mostrar' le
  faltan los paréntesis`, `agregar() no cambia la lista: devuelve una nueva`).
- **Dónde termina un renglón**: una sentencia termina donde termina su renglón. Sigue en el
  de abajo solo si quedó abierto un `(`, un `[` o una `{`, o si el renglón termina en un
  operador (`+`, `-`, `y`, `==`, `=`...) o en una coma. Un renglón no puede empezar con `+`,
  `*`, `/`, `==`, `y` u `o`; y un `-1` al principio de un renglón ya no se pega a la cuenta
  de arriba. `responder`, `fallar`, `enviar` y `asegurar` llevan lo suyo en el mismo renglón.
- **Un `sea` de más**: dentro de un `si`, `para`, `mientras` o `intentar`, escribir
  `sea cuenta = i` cuando ya hay una `cuenta` afuera no cambiaba nada y no avisaba. Ahora el
  error dice `'cuenta' ya existe afuera de este bloque` y que hay que sacar el `sea`. Lo
  mismo con un `estado` del agente. (Una función o una prueba sí pueden usar adentro un
  nombre que también existe en el programa.)
- **Comparar un texto con un número**: `"18" == 18` daba `falso` sin avisar. Ahora es un
  error que sugiere `numero("18")`. Comparar con `nada` sigue valiendo.
- **El renglón del error**: debajo del mensaje Mate muestra el renglón señalado, por ejemplo
  `    2 | mostrar(totl)`. Para ir a ese renglón en el Bloc de notas: `Ctrl+G` y el número.
- **Nombres mal tipeados**: si escribís `totl` y existe `total`, o `mostar` en vez de
  `mostrar`, el error termina con `¿Quisiste decir 'total'?`. Vale también para campos,
  claves de mapas, mensajes y agentes.
- **Palabras de otros lenguajes, con tilde o con mayúscula**: `print`, `if`, `else`, `true`,
  `función`, `número` o `Si` no se aceptan, pero el error dice cómo se escribe en Mate
  (`mostrar`, `si`, `sino`, `verdadero`, `funcion`, `numero`, `si`). Si vos le pusiste uno de
  esos nombres a algo tuyo (`sea def = 5`, `mensaje Return`), Mate lo respeta.
- **Condiciones mal escritas**: `si x = 5`, `si 1 < x < 10`, `si x > 3 y < 10` y
  `si x > 3 entonces` explican cómo va cada una (`==`, `1 < x y x < 10`, repetir la variable,
  y la llave `{` directamente). También `=>`, `=<`, `===` y `<>` (van `>=`, `<=`, `==` y `!=`).
- **Nombres que no se pueden usar**: `sea y = 1` avisa que `y` es una palabra propia de Mate, y
  `sea texto = "hola"` que `texto` es una función incluida; en los dos casos hay que elegir otro
  nombre. Como nombre de *campo* sí valen las palabras propias de Mate:
  `mensaje Envio { estado: texto, para: texto }` y después `e.estado`.
- **"No se puede cambiar"**: el error dice por qué: es un `sea`, un parámetro, la variable del
  `para`, el mensaje recibido, una función o un agente.
- **Números escritos a la argentina**: en el código el punto es el de los decimales, así que
  `1.500` vale uno y medio. Como casi siempre se quiso decir mil quinientos, Mate frena y lo
  explica (`1.500 vale 1.5, no 1500`); lo mismo con `1.500.000`. Los miles se escriben todos
  juntos o con guion bajo: `1500` o `1_500`. Y `3,5` suelto dice `los decimales van con punto,
  no con coma: 3.5`. (El aviso salta con tres decimales terminados en cero, como `1.500` o
  `12.250`; `2.125` se toma como el decimal que es.)
- **Errores con `nada`**: "no se puede hacer nada + numero" se leía como otra frase. Ahora dice
  `no se puede sumar el valor nada con un número` y agrega la causa más común: a la función le
  falta un `devolver`, o es un campo opcional que vino vacío.
- **Posiciones de una lista**: `lista[3]` en una lista de tres dice `la lista tiene 3
  elementos, así que las posiciones van de 0 a 2`, y recuerda `ultimo(lista)`. Si la posición
  salió de una cuenta con decimales (`lista[largo(lista) / 2]`), sugiere `redondear()`.
- **Más controles antes de correr**: `yo` o `remitente` fuera de un agente, una clave repetida
  en un mapa (`{ a: 1, a: 2 }`), un parámetro o un estado repetido, y `nada` en un campo
  obligatorio de un mensaje se avisan antes de empezar, no cuando el programa llega ahí.
- **Un `asegurar` que falla muestra los valores**: `asegurar a + 1 == 4` dice
  `no se cumplió lo asegurado: dio 3 y se esperaba 4`. Si los dos lados se ven iguales pero no
  lo son (`0.1 + 0.2 == 0.3`), muestra el número completo y recuerda redondear antes de comparar.
- **Por dónde se llegó al error**: si el error pasó adentro de una función, o en un agente al
  que otro le preguntó, debajo del renglón señalado aparece el recorrido:
  `cómo se llegó: en dividir(), llamada desde precio() (línea 5), llamada desde la línea 9`,
  o `... se lo preguntó Comprador a Vendedor (línea 16)`. El texto del error no cambia.
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
| Un renglón que no sirve para nada se avisa | `agregar(lista, 4)` sin guardar el resultado es un error |
| Atajos solo donde ahorran de verdad | `total += precio` y `total -= 1` (no hay `*=` ni `/=`) |

## Cómo hablan los agentes

- `mensaje Nombre { campo: tipo }` declara el **contrato** de un mensaje. Tipos: `numero`,
  `texto`, `logico`, `lista`, `mapa`, `agente`, `cualquiera` u otro mensaje. `tipo?` lo hace opcional.
- Una lista puede decir de qué es: `items: lista de Pedido`, `vendedores: lista de agente`,
  `precios: lista de numero`. Así no pasa una lista con cosas mezcladas: el error dice en qué
  posición está lo que sobra (`recibió una lista que en la posición 1 tiene un número`).
- El contrato también puede decir **qué se contesta**:
  `mensaje Pedido { producto: texto } responde Cotizacion`. Si un agente le responde otra cosa
  a un `Pedido`, la falla es de ese agente (no del que preguntó) y el error señala su
  `responder`. Sin `responde`, se puede contestar cualquier valor, como siempre.
- `agente Nombre { ... }` tiene su `estado` privado y un `al recibir Tipo como x { }` por cada
  mensaje que entiende. Ningún agente puede tocar el estado de otro ni las variables de afuera
  (tampoco llamando a una función de afuera que las cambie).
- Los mensajes y las respuestas llevan **datos**: números, textos, listas, mapas, otros mensajes
  o agentes. Una función no puede viajar adentro de un mensaje.
- `enviar Mensaje { ... } a Agente` lo deja en la cola y sigue (asíncrono). Si ese agente no
  tiene un `al recibir` para ese mensaje, el error sale ahí mismo, en el renglón del `enviar`.
- `preguntar Mensaje { ... } a Agente` espera y devuelve la respuesta. Si el otro agente falla
  (con `fallar`, con un `asegurar` que no se cumple o con cualquier otro error), el error le
  llega al que preguntó, que lo puede atajar con `intentar`.
- Lo que el programa ya envió se entrega antes de su siguiente `preguntar` (y, en una prueba,
  antes de cada `asegurar`): así la respuesta ya cuenta lo enviado.
- Si un agente falla mientras atiende un mensaje, vuelve a como estaba antes de recibirlo: su
  estado no cambia y lo que había dejado para `enviar` no sale. Lo que ya mostró en pantalla y
  lo que otros agentes hicieron al contestarle no se deshace. También cuenta como falla suya no
  responder a un `preguntar`, o responderle a un `enviar` con algo que no es un mensaje o que
  el otro no sabe recibir.
- Si el programa se corta por un error y antes había fallado algún agente, Mate muestra primero
  el error del agente (suele ser la causa) y después el que cortó.
- Si el programa se corta por un error y quedaban mensajes en la cola, Mate dice cuáles no
  llegaron (`quedaron 2 mensaje(s) sin entregar:`).
- `responder valor` contesta al `remitente` y termina de atender ese mensaje. Solo va dentro de
  `al recibir` (o de una función del agente); `devolver` va dentro de una función, o dentro de
  `al recibir` para terminar sin contestar. Fuera de lugar, Mate lo avisa antes de correr.
- `yo` es el agente que está atendiendo; sirve para mandarse a sí mismo dentro de un mensaje.
- Si los agentes se preguntan en ronda, el error muestra la cadena completa:
  `ciclo de preguntas: A → B → C → A. A le preguntó a B (línea 4), B le preguntó a C (línea 5)...`
- `--traza` muestra la conversación entera, mensaje por mensaje. Con
  `--traza=conversacion.txt` no la muestra: la guarda en ese archivo (se abre con el Bloc de
  notas) y al final anota cuántos mensajes hubo y cuántos fallaron. El archivo queda en la
  carpeta donde estás parado; Mate no acepta un nombre terminado en `.mate` o `.py`, para no
  pisar un programa.
- `a_json(mensaje)` y `de_json(texto)` pasan los mensajes a JSON y de vuelta, validando el contrato.
  También viajan los agentes, incluidas las copias hechas con `crear`.
- `de_json(texto, "Pedido")` además exige que lo que llegó sea un `Pedido` (o un `"numero"`,
  una `"lista de Pedido"`...): sirve para los datos que vienen de afuera. Si el texto trae un
  mapa suelto con los campos (`{"producto": "yerba", "cantidad": 2}`), arma el `Pedido` con
  ellos; si no cumple el contrato, el error lo dice.

### Varias copias de un agente

Declarar un `agente` ya crea uno con ese nombre. Con `crear` nacen más, cada uno con su estado:

```
sea norte = crear Vendedor llamado "Norte" { descuento: 0.05 }
sea sur = crear Vendedor llamado "Sur" { precios: { yerba: 3300 } }
sea otro = crear Vendedor
```

Entre llaves va el estado inicial que querés distinto; el resto arranca como en la declaración.
Tiene que ser del mismo tipo que el declarado: si `precios` arranca como mapa y le das un número,
Mate avisa (`Vendedor.precios arranca como mapa y le diste numero`). `nada` vale siempre
("sin tope", "sin cliente todavía"). Lo que le das reemplaza a lo declarado: esa parte de la
declaración ni se calcula.
`llamado` le pone nombre para la traza (`Vendedor Norte`); sin eso se llama `Vendedor#2`.
El nombre puede ser cualquier texto (`llamado "Sucursal " + ciudad`), pero no se repite: crear
dos `Vendedor` llamados `"Norte"` es un error, porque no se los podría distinguir.
Las copias se guardan en variables y se pueden mandar dentro de un mensaje (tipo `agente` o `lista`).

### Varios archivos

```
usar "catalogo.mate"
```

Trae los mensajes, agentes, funciones y valores `sea` del otro archivo (se busca al lado del que
lo usa). Lo que ese archivo ejecuta y sus pruebas no se traen, así que un mismo archivo sirve como
programa y como biblioteca. Usarlo dos veces no molesta. Ver `ejemplos/mercado.mate`.

**Antes de correr**, Mate revisa los contratos: avisa si a un mensaje le falta o le sobra un
campo, si un valor literal es del tipo equivocado, si le mandás a un agente (o a una copia
guardada con `sea`) algo que no sabe recibir, o si le preguntás a un agente que para ese mensaje
nunca llega a un `responder`. Lo que no se puede saber de antemano se valida al construir el mensaje.

### Las pruebas

Cada `prueba` empieza limpia: los agentes declarados arrancan con el mismo estado inicial que
tuvieron al correr el programa, y las variables de afuera (también las que guarda una función
hecha por otra función) y las copias hechas con `crear` vuelven a como las dejó el programa.
Lo que una prueba cambia no le llega a la siguiente. Además:

- Dentro de una prueba, `intentar` no ataja un `asegurar` de la prueba que no se cumple: la
  prueba falla. (Al correr el programa con `correr`, un `asegurar` que no se cumple es un error
  como cualquier otro y sí se puede atajar; y el de otro agente siempre le llega como error al
  que le preguntó.)
- Si varios agentes fallan durante una prueba, se muestran todos los errores, no solo el
  primero, también cuando la prueba además falla por un `asegurar`.
- Debajo de cada error se ve el renglón señalado. Si el renglón es de un archivo traído con
  `usar`, el error lo nombra: `catalogo.mate, línea 7`.
- Si un agente falló al correr el programa, antes de las pruebas, `probar` lo muestra arriba de
  los resultados y termina con error aunque las pruebas pasen.
- Lo que una prueba muestra con `mostrar` aparece debajo de su nombre, con una barra adelante
  (`      | Compro 10 de yerba`), y no mezclado con los resultados.
- Si el archivo no tiene ninguna prueba, `probar` lo dice (y muestra cómo se escribe una). Dos
  pruebas no pueden tener el mismo nombre: se avisa antes de correr.
- `asegurar falla { ... }` es la forma corta de comprobar que algo **tiene que fallar**:

  ```
  prueba "no se puede dividir por cero" {
      asegurar falla { dividir(1, 0) }
  }
  ```

  Se cumple si lo de adentro falla; si no falla, la prueba dice `se esperaba que esto fallara,
  y no falló` (o el texto que le pongas después de una coma). Sirve para lo que falla en el
  momento: una cuenta, una función, un `preguntar`.
- `simular` reemplaza, **solo dentro de esa prueba**, lo que un agente contesta a un mensaje:

  ```
  prueba "el comprador suma lo que le cotizan" {
      simular Vendedor al recibir Pedido como p {
          responder Cotizacion { total: p.cantidad * 10 }
      }
      asegurar preguntar Comprar { cantidad: 2 } a Comprador == 20
  }
  ```

  Así se prueba al `Comprador` sin depender del `Vendedor` de verdad (el día de mañana, un
  agente de IA). Lo simulado ve las variables de la prueba pero no las puede cambiar, no ve el
  estado del agente, tiene que cumplir el contrato (`responde`) y se termina con la prueba: la
  siguiente ya habla con el agente real. También vale para una copia: `simular norte al recibir ...`.

### Los datos de un error atajado: `detalle_de`

En `intentar { ... } si falla e { ... }`, `e` es el texto del error. Para decidir qué hacer sin
depender de cómo está redactado ese texto, `detalle_de(e)` devuelve un mapa con cuatro datos:

| Dato | Qué trae |
|---|---|
| `detalle_de(e).texto` | el mismo texto de `e` |
| `detalle_de(e).linea` | el número de renglón donde pasó |
| `detalle_de(e).clase` | qué clase de error fue (la lista de abajo): no cambia aunque cambie la redacción |
| `detalle_de(e).dato` | el valor que se le dio a `fallar`, tal cual (`fallar { codigo: 404 }`); en los demás errores, `nada` |

Las clases son: `"fallar"` (un `fallar` del programa), `"asegurar"`, `"contrato"` (un mensaje
o una respuesta que no cumple su contrato), `"clave"` (una clave o un campo que no está),
`"posicion"`, `"division"` (por cero), `"nombre"` (un nombre que no existe), `"numero"` (un
texto que no es un número), `"json"`, `"agente"` (no sabe recibir ese mensaje o no respondió),
`"ciclo"` (de preguntas) y `"otro"` para el resto. Hay que pasarle `e` tal cual llegó: si lo
cambiás (`e + "!"`) es un texto común y `detalle_de` avisa que no es un error atajado.

## Referencia rápida

```
# comentario
sea x = 1                  var y = [1, 2]             y[0] = 5
funcion doble(n) { devolver n * 2 }
si a > b { } sino si a == b { } sino { }
mientras cond { }          para item en lista { }
romper                     continuar                  (solo dentro de mientras o para)
y += 1                     y -= 1                     (lo mismo que y = y + 1)
y  o  no   ==  !=  <  <=  >  >=   +  -  *  /  %
{ nombre: "yerba", precio: 3500 }       mapa.nombre      mapa["nombre"]
"Total: {precio * 2}"      "Sale {precios["yerba"]}"  (lo que va entre llaves se calcula)
3.5 (decimal con punto)    1_500 (mil quinientos; los miles nunca llevan punto)
```

### Funciones incluidas

Son estas y no hay otras. Cada renglón es un ejemplo que se puede copiar:

| Ejemplo | Qué da |
|---|---|
| `mostrar("Total:", total)` | escribe en pantalla |
| `leer("¿Cuántos?", "3")` | le pide un texto a la persona (en las pruebas da el 2.º valor) |
| `texto(3.5)` | lo pasa a texto: "3.5" |
| `numero("1.234,50")` | lee un número escrito como texto: 1234.5 |
| `tipo(x)` | dice qué es: "numero", "texto", "lista", "mapa"... |
| `largo(lista)` | cuántos elementos tiene (o letras, o claves) |
| `redondear(3.14159, 2)` | 3.14 (sin el 2.º valor, sin decimales) |
| `pesos(1234.5)` | el texto "$ 1.234,50" |
| `absoluto(-5)` | 5: el número sin el signo |
| `sumar([1, 2, 3])` | 6 |
| `promedio([4, 6])` | 5 |
| `minimo([3, 1, 2])` | 1: el más chico de la lista |
| `maximo([3, 1, 2])` | 3: el más grande de la lista |
| `rango(1, 10, 3)` | [1, 4, 7]; rango(3) es [0, 1, 2] y rango(2, 5) es [2, 3, 4] |
| `tiene(lista, x)` | verdadero si x está en la lista, es clave del mapa o parte del texto |
| `claves(mapa)` | la lista de sus claves |
| `valores(mapa)` | la lista de sus valores |
| `obtener(mapa, "clave", 0)` | el valor de esa clave o, si el mapa no la tiene, el 3.er valor |
| `agregar(lista, x)` | una lista NUEVA con x al final |
| `quitar(lista, x)` | una lista NUEVA sin los que valen x (en un mapa, sin esa clave) |
| `ordenar(lista, "precio")` | una lista NUEVA ordenada; el campo es opcional: ordenar(lista) |
| `ultimo(lista)` | el último elemento (o la última letra de un texto) |
| `porcion(lista, 1, 3)` | los de las posiciones 1 y 2; sin el 3.er valor, hasta el final |
| `unir(lista, ", ")` | un texto con los elementos separados por coma |
| `partir("a,b", ",")` | la lista ["a", "b"] |
| `mayusculas("hola")` | "HOLA" |
| `minusculas("HOLA")` | "hola" |
| `recortar("  hola ")` | "hola": sin los espacios de las puntas |
| `reemplazar(t, "a", "b")` | el texto con cada a cambiada por b |
| `empieza_con(t, "Sr.")` | verdadero si el texto empieza así |
| `termina_con(t, ".txt")` | verdadero si el texto termina así |
| `a_json(valor)` | el valor escrito como texto JSON |
| `de_json(texto, "Pedido")` | el valor que describe ese JSON; el 2.º valor (opcional) exige ese tipo |
| `detalle_de(e)` | los datos de un error atajado: un mapa con texto, linea, clase y dato |

- Si a una función le das valores de más o de menos, el error trae el ejemplo:
  `obtener() lleva 3 valores y recibió 2. Por ejemplo: obtener(mapa, "clave", 0)`.
- `agregar`, `quitar`, `ordenar` y `porcion` no cambian la lista original: devuelven una nueva.
  `quitar(lista, x)` saca **por valor** (todos los que valen `x`), no por posición.
- `ordenar` ordena los textos como el diccionario: sin importar mayúsculas ni tildes, y con la
  `ñ` después de la `n`. Con un segundo valor ordena una lista de mapas o de mensajes por ese
  campo: `ordenar(productos, "precio")`.
- `minimo`, `maximo`, `promedio` y `ultimo` no pueden con una lista vacía: es un error que lo
  dice. `porcion(lista, 1, 3)` cuenta las posiciones desde 0 y no incluye la del final; si el
  final se pasa del largo, llega hasta donde haya.
- `obtener(mapa, "clave", 0)` sirve para no preguntar antes con `tiene`. Si en cambio escribís
  `mapa["clave"]` y la clave no está, el error dice cuáles sí tiene:
  `el mapa no tiene la clave "cafe" (tiene: yerba, azucar)`.
- Esta tabla, la de `python mate\mate.py guia` y los ejemplos de los errores salen de un mismo
  lugar dentro de `mate.py`, así que no se desacomodan entre sí.

### Textos

- Dentro de un texto, lo que va entre llaves se calcula: `"Total: {precio * 2}"`. Adentro de
  las llaves puede haber otros textos con sus comillas: `"Sale {precios["yerba"]}"` o
  `"Compras: {unir(lista, ", ")}"`.
- La barra `\` es especial: `\n` es un salto de renglón, `\t` un espacio largo, `\"` una
  comilla, `\{` una llave de verdad y `\\` una barra. Cualquier otra combinación es un error
  que lo explica, y también un texto que parece una ruta de Windows con barras simples:
  `"C:\temp\nuevo"` antes salía con un salto de renglón en el medio sin avisar. Las rutas se
  escriben `"C:/temp/nuevo"` (Windows las entiende igual) o `"C:\\temp\\nuevo"`.

### Pedirle un dato a la persona: `leer`

```
sea nombre = leer("¿Cómo te llamás?")
sea cantidad = numero(leer("¿Cuántos paquetes?", "3"))
```

- `leer` muestra la pregunta, espera que la persona escriba y apriete Enter, y devuelve lo
  escrito como **texto** (sin los espacios de las puntas). Para hacer cuentas, pasalo por
  `numero(...)`.
- El segundo valor es la **respuesta preparada**: es lo que devuelve `leer` cuando corren las
  pruebas (`probar` nunca espera el teclado) o cuando no hay teclado. Si en una prueba se
  llega a un `leer` sin respuesta preparada, es un error que lo explica.
- Solo se usa desde el programa principal (o desde una función llamada por él). Un agente no
  puede frenar a todos esperando el teclado: se lee el dato afuera y se le manda en un mensaje.

### Salir de un bucle: `romper` y `continuar`

```
para cosa en compras {
    si cosa == "" { continuar }      # salta a la vuelta siguiente
    si cosa == "fin" { romper }      # corta el bucle acá
    mostrar(cosa)
}
```

Valen dentro de `para` y de `mientras`, y afectan al bucle más cercano. Fuera de un bucle,
Mate lo avisa antes de correr.

### Números y plata

- Los decimales se muestran limpios: `mostrar(0.1 + 0.2)` muestra `0.3` y `mostrar(10 / 3)`
  muestra `3.33333333333`. Es solo cómo se ven: por dentro la cuenta sigue teniendo su resto
  minúsculo, así que `0.1 + 0.2 == 0.3` da `falso`. Para comparar plata, redondeá antes:
  `redondear(a, 2) == redondear(b, 2)`.
- Ojo con los números de muchas cifras: un decimal de 16 cifras o más se muestra con 12 como
  mucho, aunque lo hayas escrito vos (`mostrar(3.141592653589793)` muestra `3.14159265359`).
  Lo mismo hacen `texto()`, `unir()` y `"{...}"`, así que `numero(texto(x))` puede no dar
  exactamente `x`. El valor guardado no cambia; para pasarlo entero a texto usá `a_json(x)`.
- Entre enteros la suma, la resta, la multiplicación y la división que da justo son exactas,
  por grandes que sean.
- `redondear(2.5)` da `3` y `redondear(2.675, 2)` da `2.68`: el medio va siempre hacia arriba,
  como en la escuela. En los negativos se aleja del cero: `redondear(-2.5)` da `-3`.
  `redondear` y `pesos` redondean el número que se ve: `0.57 * 50` se muestra `28.5` y
  `redondear(0.57 * 50)` da `29`. La cantidad de decimales va de 0 en adelante:
  `redondear(1234, -2)` es un error.
- `pesos(1234567.891)` devuelve el texto `$ 1.234.567,89`; `pesos(3500, 0)` devuelve `$ 3.500`
  (el segundo valor es la cantidad de decimales, de 0 a 6). Los negativos salen `-$ 1.500,00`.
- `numero("1.234,50")` da `1234.5` y `numero("$ 7,25")` da `7.25`: entiende la coma decimal, el
  punto de miles y el signo `$`. Ojo: con un solo punto y sin coma, el punto es decimal
  (`numero("3.500")` da `3.5`); con dos o más puntos son miles (`numero("1.234.567")`). Con el
  signo `$` adelante, el punto seguido de tres cifras son miles: `numero("$ 3.500")` da `3500`,
  así lo que escribe `pesos()` se puede volver a leer. Un texto vacío o que no es un número
  (`"1e5"`, `"hola"`, `".5"`, `"5."`, `"1_000"`) es un error: medio se escribe `"0.5"` o `"0,5"`.

- La igualdad no convierte nada, tampoco adentro de una lista o un mapa: `1 == verdadero` da
  `falso` y `[1] == [verdadero]` también.

Los nombres de mensajes y agentes empiezan con mayúscula; el resto, con minúscula.

Detalles: `partir("abc", "")` separa letra por letra; `redondear(3.14159, 2)` lleva una cantidad
entera de decimales; `rango(10, 0, -1)` cuenta para atrás; las claves de un mapa son siempre textos (`tiene(mapa, [1])` da `falso`);
solo se puede asignar a una variable o a una parte de ella (`x`, `x.campo`, `x[0]`).

## Qué cambió y puede frenar un programa viejo

Varias mejoras vuelven error cosas que antes corrían. Si un archivo viejo deja de andar, casi
seguro es por una de estas:

| Qué pasa ahora | Cómo se arregla |
|---|---|
| Un parámetro, un estado o una variable no puede llamarse como una función incluida (`texto`, `tipo`, `numero`, `largo`, `valores`, `pesos`...), tampoco dentro de una función | Elegir otro nombre: `funcion saludar(nombre)`. Ojo: cada función incluida nueva ocupa un nombre |
| `responder` dentro de una función de afuera de un agente es un error antes de correr | Pasar la función adentro del agente, o que devuelva el valor y el `responder` quede en el `al recibir` |
| `preguntar` a un agente que para ese mensaje nunca responde es un error antes de correr | Usar `enviar`: ahora se entrega solo antes del siguiente `preguntar` |
| Dentro de una prueba, `intentar` no ataja un `asegurar` de la prueba | Para comprobar que algo falla, usar `fallar` en el código y `asegurar` afuera del `intentar` |
| "Demasiada recursión" y el freno de pasos no se atajan con `intentar` | Achicar la recursión, o `--sin-limite` para el freno de pasos |
| Un agente no puede cambiar ninguna variable que no sea suya, ni llamando a una función que la tenga guardada | Que la función devuelva el valor y el agente lo guarde en su `estado` |
| `numero(".5")`, `numero("5.")` y `numero("1_000")` son error; `numero("1.234.567")` y `numero("1,5")` ahora sí son números | Escribir `"0.5"`; si usabas `intentar` para detectar texto inválido, revisalo |
| `redondear(x, -2)` es un error, y el medio redondea hacia arriba | Para centenas: `redondear(x / 100) * 100` |
| Los decimales se muestran con 12 cifras como mucho, y `fallar 0.1 + 0.2` dice `0.3` | Ver "Números y plata" |
| Cambió la redacción de varios errores (`largo() lleva 1 valor y recibió 2`, sugerencias `¿Quisiste decir...?`, `las claves de un mapa son textos, no numero`) | No comparar el texto entero del error con `==`; buscar una palabra con `tiene(e, "clave")` |
| `if`, `else`, `true`, `función`... usados como si fueran de Mate son un error antes de correr | Escribir la palabra de Mate que dice el error |
| Un renglón que solo calcula (`i + 1`, `largo(x)`, `agregar(lista, 4)` sin guardar) es un error: "calcula un valor y no hace nada con él" | Guardar el resultado (`lista = agregar(lista, 4)`), mostrarlo o borrar el renglón |
| Un renglón no puede empezar con `+`, `*`, `/`, `==`, `y`, `o`; y un `-` al principio de un renglón empieza una sentencia nueva | Dejar el operador al final del renglón de arriba, o encerrar la cuenta entre paréntesis |
| `responder`, `fallar`, `enviar` y `asegurar` con lo suyo en el renglón de abajo son un error | Escribirlo en el mismo renglón |
| `sea x = ...` dentro de un `si`, `para`, `mientras` o `intentar` cuando `x` "ya existe afuera" (o es un `estado` del agente) es un error | Sacar el `sea` si querías cambiar la de afuera (tiene que ser `var`), o elegir otro nombre |
| "No se puede comparar un texto con un número" con `==` o `!=` | Convertir uno de los dos: `numero(t) == 18` |
| `[1] == [verdadero]` y `{ a: 1 } == { a: verdadero }` ahora dan `falso` | Nada: antes daban `verdadero` por error |
| `romper`, `continuar` son palabras de Mate y `leer` es una función incluida: no sirven como nombre de variable | Elegir otro nombre |
| El error de una llave sin cerrar cambió de redacción ("la llave que se abrió en la línea...") | No comparar el texto entero del error |
| `recortar`, `reemplazar`, `empieza_con`, `termina_con`, `minimo`, `maximo`, `promedio`, `absoluto`, `ultimo`, `porcion` y `obtener` son funciones incluidas: no sirven como nombre de variable | Elegir otro nombre: `sea precio_minimo = ...`, `sea el_ultimo = ...` |
| Dentro de un texto, una barra `\` seguida de algo que no es `n`, `t`, `\`, comilla o llave es un error; también `"C:\temp"` con una sola barra | Escribir `/` o doble barra: `"C:/temp"` o `"C:\\temp"` |
| `1.500`, `12.000` (tres decimales terminados en cero) y `3,5` suelto son un error | `1500` o `1_500` si eran miles; `1.5` y `3.5` si eran decimales |
| `ordenar` ya no pone las mayúsculas primero ni la `ñ` y las tildes al final | Nada: ahora ordena como el diccionario |
| `yo` y `remitente` fuera de un agente (también en una función de afuera), una clave repetida en un mapa, un parámetro o estado repetido y `nada` en un campo obligatorio son un error antes de correr | Pasarle el agente a la función como valor; borrar el repetido; declarar el campo opcional con `?` |
| `simular` es una palabra de Mate y `detalle_de` es una función incluida: no sirven como nombre de variable | Elegir otro nombre |
| Dos copias de un agente no pueden tener el mismo nombre (`crear Vendedor llamado "Norte"` dos veces, o en una prueba cuando el programa ya creó esa copia) | Darles nombres distintos, o crear sin `llamado` |
| Dos pruebas con el mismo nombre son un error antes de correr | Cambiarle el nombre a una |
| `probar` muestra lo que cada prueba escribe debajo de su nombre (con `|` adelante), y si no hay pruebas ya no dice `0 de 0 pruebas pasaron` | Nada |
| El error de un ciclo de preguntas ahora trae la cadena (`A → B → A`), y el de responderle mal a un `enviar` trae el renglón del `responder` | No comparar el texto entero del error |
| Cambió la redacción de más errores: `la posición 3 está fuera de rango...` (antes "índice"), `el valor nada` en vez de `nada`, la lista `(tiene: ...)` en el error de clave, y `Por ejemplo: ...` al final del error de cantidad de valores | No comparar el texto entero del error; el de clave sigue trayendo la palabra "clave" |

## Límites de la versión 0.2

- Los agentes corren todos dentro del mismo programa, de a uno y en orden (por eso el resultado
  es siempre el mismo). Todavía no se conectan con agentes de IA reales ni entre máquinas.
- Todo lo que trae `usar` queda en un único espacio de nombres: dos archivos no pueden declarar
  algo con el mismo nombre.

## Pruebas del intérprete

```bash
python3 -m pytest mate/pruebas -q -p no:cacheprovider
```
