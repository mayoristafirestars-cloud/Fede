# Mate 🧉

Un lenguaje chico, con palabras en español, pensado para dos cosas:

1. **Escribir código más práctico y con menos sorpresas.**
2. **Que los agentes se hablen entre ellos** con mensajes que tienen contrato.

Versión 0.3. El intérprete es un solo archivo (`mate.py`), sin dependencias: alcanza con Python 3.

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
castellano. En el Bloc de notas, `Ctrl+G` te lleva a ese renglón. Y si no te acordás cómo se
usa una palabra, preguntale a Mate: `python mate\mate.py ayuda si` (o `ayuda para`,
`ayuda largo`...) muestra una explicación corta con un ejemplo para copiar.

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
| `probar mate\ejemplos` | corre las pruebas de todos los `.mate` de esa carpeta (o de varios archivos) y da un total |
| `verificar archivo.mate` | revisa el programa sin correrlo (contratos, nombres que no existen...) |
| `guia` | imprime una página con todo Mate, para pegarle a una IA (`python mate\mate.py guia`) |
| `ayuda` | muestra las órdenes y un ejemplo listo para copiar |
| `ayuda si` | explica una palabra de Mate o una función incluida (`ayuda largo`), con un ejemplo |
| `consola` | abre la consola, para probar renglones sueltos sin crear un archivo |
| `--traza` | muestra la conversación entre agentes, mensaje por mensaje, numerada y con lo que falló |
| `--traza=conversacion.txt` | guarda esa conversación en un archivo, con un resumen al final |
| `--sin-limite` | no corta los programas que dan muchísimos pasos |
| `--depurar` | si Mate falla por dentro, muestra el detalle técnico |
| `--version` | dice qué versión de Mate es |

Si te equivocás al tipear, Mate te lo dice en vez de seguir de largo: `corer` sugiere `correr`,
`--trasa` sugiere `--traza`, y si el archivo no está te muestra los `.mate` que sí hay en esa
carpeta. Si el Bloc de notas lo guardó como `hola.mate.txt`, también te avisa (y si le pasás
ese nombre completo, lo corre igual con un aviso). La orden va siempre primero: si escribís
`hola.mate probar`, Mate te dice que es `probar hola.mate`.

### Ayuda de una palabra

```
python mate\mate.py ayuda mientras
```

contesta qué hace `mientras` y muestra un ejemplo corto que se puede copiar tal cual. Vale para
todas las palabras de Mate (`si`, `para`, `agente`, `enviar`, `prueba`, y también
`ayuda al fallar`) y para todas las funciones incluidas (`ayuda largo`, `ayuda pesos`). En las
funciones el ejemplo es la forma de llamarla (`pesos(1234.5)`): así suelto anda en la consola;
en un programa va adentro de otra cosa, `mostrar(pesos(1234.5))` o `sea t = pesos(1234.5)`. Si escribís una palabra de otro lenguaje
(`ayuda print`) te dice cuál es la de Mate, y si le errás por una letra (`ayuda mostar`)
sugiere la parecida.

### La consola

Para probar algo cortito sin crear un archivo:

```
python mate\mate.py consola
```

Aparece `  1>` y Mate espera un renglón. Lo que escribís corre al apretar Enter:

```
  1> sea precio = 3500
  2> precio * 2
7000
  3> funcion con_iva(p) {
  4.     devolver p * 1.21
  5. }
  6> pesos(con_iva(precio))
"$ 4.235,00"
  7> salir
```

- Un valor suelto (`precio * 2`) se muestra solo, sin escribir `mostrar`. Los textos salen
  entre comillas, para distinguir `"5"` de `5`.
- Si queda una llave, un paréntesis o un corchete sin cerrar, o el renglón termina en un
  operador o una coma (`1 +`), la consola sigue en el renglón de abajo (el número termina en
  `.` en vez de `>`). Un renglón vacío corta ahí.
- Si la entrada llega redirigida desde un archivo y trae una letra que no se puede leer, la
  consola pone un signo en su lugar y sigue: nunca se cierra por eso.
- Lo que declarás (variables, funciones, mensajes, agentes) queda para los renglones
  siguientes. Solo acá se puede volver a escribir `sea precio = 4000` o la misma `funcion`
  para corregirla: reemplaza a la anterior. En un archivo eso sigue siendo un error.
- Los renglones se numeran de corrido, así que si un error dice `línea 4` es el renglón 4 de
  lo que escribiste. Un error no cierra la consola.
- `ayuda si` explica una palabra ahí mismo. Las pruebas no corren en la consola: van en un
  archivo, con `probar`.
- Para terminar: `salir` (o `Ctrl+Z` y Enter en Windows).

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
  sin parar (`demasiada recursión`: hay lugar para 3.000 llamadas una adentro de la otra, y el
  error nombra la función) y los programas que se quedan sin memoria. Ninguno de esos cortes
  se puede atajar con `intentar`. (Con un Python anterior al 3.12 el lugar es menor: unas 120
  llamadas.)
- **Cosas demasiado grandes**: un texto o una lista de más de 10.000.000 de elementos
  (`rango(100000000000)`, un texto que se duplica sin parar, `unir`, `texto`, `a_json` o
  `"{...}"` con una lista enorme) o un número entero de más de unas 4.000 cifras son un error
  común, con su renglón, en vez de colgar la consola.
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
  faltan los paréntesis`, `agregar() no cambia la lista: devuelve una nueva`). Una cuenta
  suelta se avisa antes de correr, esté donde esté. Y estos errores no se atajan con
  `intentar`: para validar un dato se guarda el resultado,
  `intentar { sea n = numero(dato) ... } si falla e { ... }`.
- **Porcentajes**: `sea iva = 21%` no existe en Mate (`%` es el resto de una división). El
  error lo dice en ese renglón: se escribe `21 / 100` o `0.21`.
- **`si no` separado**: se escribe `sino`, todo junto, y el error lo explica.
- **Dónde termina un renglón**: una sentencia termina donde termina su renglón. Sigue en el
  de abajo solo si quedó abierto un `(`, un `[` o una `{`, o si el renglón termina en un
  operador (`+`, `-`, `y`, `==`, `=`...) o en una coma. Un renglón no puede empezar con `+`,
  `*`, `/`, `==`, `y` u `o`; y un `-1` al principio de un renglón ya no se pega a la cuenta
  de arriba. `responder`, `fallar`, `enviar` y `asegurar` llevan lo suyo en el mismo renglón.
- **Un `sea` de más**: dentro de un `si`, `para`, `mientras` o `intentar`, escribir
  `sea cuenta = i` cuando ya hay una `cuenta` afuera no cambiaba nada y no avisaba. Ahora el
  error dice `'cuenta' ya existe afuera de este bloque` y que hay que sacar el `sea`. Lo
  mismo con un `estado` del agente. Una función o una prueba sí pueden usar adentro un
  nombre que también existe en el programa, con una excepción: desde un `si`, `para`,
  `mientras` o `intentar` de adentro de la función (o de la prueba, o de un `al recibir`) no
  se puede repetir el nombre de una variable `var` del programa, que es el caso en el que
  casi seguro se la quiso cambiar.
- **Comparar un texto con un número**: `"18" == 18` daba `falso` sin avisar. Ahora es un
  error que sugiere `numero("18")`. Comparar con `nada` sigue valiendo.
- **El renglón del error**: debajo del mensaje Mate muestra el renglón señalado, por ejemplo
  `    2 | mostrar(totl)`. Para ir a ese renglón en el Bloc de notas: `Ctrl+G` y el número.
- **Nombres mal tipeados**: si escribís `totl` y existe `total`, o `mostar` en vez de
  `mostrar`, el error termina con `¿Quisiste decir 'total'?`. Vale también para campos,
  claves de mapas, mensajes y agentes.
- **Nombres que no existen, antes de correr**: un nombre mal escrito en una parte del
  programa que casi nunca se usa (adentro de un `si`, de una función, de un agente, de una
  prueba) antes saltaba recién el día que el programa pasaba por ahí. Ahora Mate lo avisa
  antes de empezar, con el mismo texto (`no existe 'totl'. ¿Quisiste decir 'total'?`), y
  también una llamada con valores de más o de menos (`largo(lista, 2)`, o `doble(1, 2)` si
  `doble` lleva uno solo). Mate avisa solo cuando está seguro; ante la duda deja correr:
  - lo declarado afuera de todo (`sea`, `var`, `funcion`, `agente`) vale aunque esté más
    abajo en el archivo, o en un archivo traído con `usar`;
  - adentro de `intentar { ... }` y de `asegurar falla { ... }` no revisa, porque ahí la
    falla se ataja o es justo lo que se está probando;
  - si el mismo nombre falta en varios renglones, lo dice una sola vez (el primero);
  - en la consola no avisa de nombres, porque lo que falta se puede escribir en el renglón
    siguiente.
- **Todos los errores se escriben igual**: `archivo:renglón: error: lo que pasó`, y debajo
  el renglón señalado. Vale para los errores comunes y para los de un agente
  (`mercado.mate:12: error: Vendedor al recibir Pedido: no vendo café`), con `correr` y
  también debajo de cada prueba con `probar`.
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
- **Condiciones que nunca pueden ser verdadero o falso**: `si 1 { }`, `mientras "a" { }`,
  `verdadero y 1` o `si x + 1 { }` se avisan antes de correr, estén donde estén en el
  programa (antes saltaban recién cuando el programa pasaba por ahí).
- **Nombres con mayúscula**: quedan para los mensajes y los agentes. `sea Listo = verdadero`
  dice que va `listo`. Y si te olvidás las llaves de un mensaje sin campos
  (`preguntar Ping a Agente`), el error dice `Escribí Ping {}`.
- **La llave en el renglón de abajo**: `mensaje Pedido`, `agente Vendedor` y `crear Vendedor`
  aceptan que la `{` venga en el renglón siguiente. (Antes, en un mensaje, eso declaraba un
  mensaje vacío sin avisar.)
- **`tiene` y `quitar`**: `tiene("hola", 1)` dice que dentro de un texto se busca otro texto, y
  `quitar("hola", "h")` que `quitar` es para listas y mapas (para un texto va `reemplazar`).
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
- `enviar Aviso { ... } a [norte, sur]` le manda el mismo mensaje a cada agente de la lista
  (también vale una variable que guarda una lista de agentes). Si alguno de la lista no sabe
  recibirlo, el error sale ahí mismo y no se le manda a ninguno. `preguntar` sigue siendo de a
  uno: para preguntarle a varios se recorre la lista con `para`.
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
- **`al fallar`**: un `enviar` no espera, así que el que envía no se entera si el otro falló.
  Si quiere enterarse, el agente declara (una sola vez) un `al fallar`:

  ```
  agente Comprador {
      estado sin_atender = 0
      al recibir Encargar como e { enviar Pedido { producto: e.producto } a Vendedor }
      al fallar como f {
          sin_atender += 1
          mostrar("{f.destino} no pudo con {f.mensaje.producto}: {f.motivo}")
      }
  }
  ```

  `f.motivo` es el texto del error, `f.mensaje` el mensaje que había mandado y `f.destino` el
  agente que falló. Con `al fallar`, esa falla queda en manos del agente y ya no se anota como
  error del programa; sin `al fallar`, todo sigue como antes. Adentro no va `responder` (es un
  aviso, no una pregunta), pero sí `enviar`. Vale para lo que el agente mandó con `enviar`: lo
  que manda con `preguntar` ya le llega como error y se ataja con `intentar`.
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
- `--traza` muestra la conversación entera, mensaje por mensaje:

  ```
    ·  1. (programa) → Comprador: Comprar { producto: "azucar", cantidad: 4 }
    ·  2.    Comprador pregunta a Vendedor Norte: Pedido { producto: "azucar", cantidad: 4 }
    ·  2.    Vendedor Norte responde a Comprador: Cotizacion { total: 4560 }
    ·  3.    Comprador pregunta a Vendedor Sur: Pedido { producto: "azucar", cantidad: 4 }
    ·  3.    Vendedor Sur falló: no vendo azucar
    ·  1. la respuesta de Comprador se descartó (para recibirla, usá 'preguntar' en vez de 'enviar'): Cotizacion { total: 4560 }
  ```

  Cada mensaje lleva su número, en el orden en que se entregó, y lo que pasa con ese
  mensaje repite el número: `responde` (lo que contestó), `falló` (con el motivo) o
  `sin respuesta` (le preguntaron y terminó sin llegar a un `responder`). Lo que un agente
  pregunta mientras atiende va con sangría, debajo del mensaje que está atendiendo. Si un
  agente le responde a un `enviar` del programa, esa respuesta no le llega a nadie: la
  traza lo dice (`la respuesta ... se descartó`) y sugiere `preguntar`. Sin `--traza` no se
  muestra nada de esto.
- Con `--traza=conversacion.txt` la conversación no se muestra: se guarda en ese archivo (se
  abre con el Bloc de notas), con los mismos renglones, y al final anota cuántos mensajes
  hubo y cuántos fallaron. El archivo queda en la
  carpeta donde estás parado; Mate no acepta un nombre terminado en `.mate` o `.py`, para no
  pisar un programa. Con `probar` sobre varios archivos o una carpeta, el archivo junta la
  conversación de todos, una sección por archivo.
- `a_json(mensaje)` y `de_json(texto)` pasan los mensajes a JSON y de vuelta, validando el contrato.
  También viajan los agentes, incluidas las copias hechas con `crear`. Para eso Mate usa dos
  formas reservadas: `{"tipo": "Pedido", "campos": {...}}` es un mensaje y
  `{"agente": "Vendedor"}` es un agente. Ojo: un mapa tuyo que tenga justo esas claves (y
  nombre un mensaje o un agente que existe) vuelve de `de_json` convertido en eso; si no
  querés eso, usá otras claves.
- `de_json(texto, "Pedido")` además exige que lo que llegó sea un `Pedido` (o un `"numero"`,
  una `"lista de Pedido"`...): sirve para los datos que vienen de afuera. Si el texto trae un
  mapa suelto con los campos (`{"producto": "yerba", "cantidad": 2}`), arma el `Pedido` con
  ellos, también cuando está adentro de una lista (`"lista de Pedido"`) o de otro mensaje
  (un `Pedido` con `items: lista de Item`); si no cumple el contrato, el error lo dice.

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
El nombre puede ser cualquier texto (`llamado "Sucursal " + ciudad`), pero tiene que ser un
texto (con un número o con `nada` es un error, y `llamado Sur` sin comillas también) y
no se repite: crear dos `Vendedor` llamados `"Norte"` es un error, porque no se los podría
distinguir.
Si un agente crea una copia mientras atiende un mensaje y después falla, esa copia se deshace
junto con su estado, y el nombre queda libre.
Las copias se guardan en variables y se pueden mandar dentro de un mensaje (tipo `agente` o `lista`).

### Varios archivos

```
usar "catalogo.mate"
```

Trae los mensajes, agentes, funciones y variables (`sea` y `var`) del otro archivo (se busca al
lado del que lo usa). Un nombre que ya vino de ahí no se puede declarar de nuevo: el error dice
de qué archivo viene. Lo que ese archivo ejecuta y sus pruebas no se traen, así que un mismo archivo sirve como
programa y como biblioteca. Usarlo dos veces no molesta. Ver `ejemplos/mercado.mate`.
Si el nombre va sin `.mate` (`usar "catalogo"`), Mate lo prueba también con `.mate`. Si el
archivo no aparece, el error sugiere el nombre parecido, avisa si el Bloc de notas lo guardó
como `.mate.txt` o muestra los `.mate` que hay en esa carpeta (con o sin `.mate` en el nombre); y si el error está adentro del archivo traído, dice quién lo trajo:
`(este archivo, catalogo.mate, se trajo con 'usar' desde mercado.mate, línea 5)`.

**Antes de correr**, Mate revisa los nombres (que todo lo que se nombra exista, y que las
funciones reciban la cantidad de valores que llevan: ver "Cuando algo sale mal") y los
contratos: avisa si a un mensaje le falta o le sobra un
campo, si un valor literal es del tipo equivocado, si le mandás a un agente (o a una copia
guardada con `sea`) algo que no sabe recibir, o si le preguntás a un agente que para ese mensaje
nunca llega a un `responder` (un `fallar` adentro de un `si` no cuenta como respuesta; un
`al recibir` que termina en `fallar` sí vale: falla siempre, a propósito). Lo que no se puede
saber de antemano se valida al construir el mensaje.

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
- Los errores de una prueba se escriben igual que con `correr`, sean de la prueba o de un
  agente: `archivo:renglón: error: lo que pasó`, y debajo el renglón señalado. Si el renglón
  es de un archivo traído con `usar`, el que se nombra es ese archivo: `catalogo.mate:7: error: ...`.
- Si un agente falló al correr el programa, antes de las pruebas, `probar` lo muestra arriba de
  los resultados y termina con error aunque las pruebas pasen.
- Lo que una prueba muestra con `mostrar` aparece debajo de su nombre, con una barra adelante
  (`      | Compro 10 de yerba`), y no mezclado con los resultados.
- Si el archivo no tiene ninguna prueba, `probar` lo dice (y muestra cómo se escribe una). Dos
  pruebas no pueden tener el mismo nombre: se avisa antes de correr.
- `probar` también acepta una carpeta o varios archivos: `python mate\mate.py probar mate\ejemplos`
  corre las pruebas de cada `.mate` de esa carpeta, uno por uno, y termina con el total
  (`En total: 14 de 14 pruebas pasaron, en 11 archivos`) y la lista de los que tuvieron problemas.
- `asegurar falla { ... }` es la forma corta de comprobar que algo **tiene que fallar**:

  ```
  prueba "no se puede dividir por cero" {
      asegurar falla { dividir(1, 0) }
  }
  ```

  Se cumple si lo de adentro falla; si no falla, la prueba dice `se esperaba que esto fallara,
  y no falló` (o el texto que le pongas después de una coma). Sirve para lo que falla en el
  momento: una cuenta (`asegurar falla { 10 / 0 }`), una función, un `preguntar`. Un nombre
  mal escrito ahí adentro (`dividr(1, 0)`) no cuenta como la falla esperada: la prueba falla y
  dice cuál es el nombre que no existe.
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
`"ciclo"` (de preguntas), `"archivo"` (un archivo que no está o que no se puede tocar) y
`"otro"` para el resto. Hay que pasarle `e` tal cual llegó: si lo
cambiás (`e + "!"`) es un texto común y `detalle_de` avisa que no es un error atajado.

## Referencia rápida

```
# comentario
sea x = 1                  var y = [1, 2]             y[0] = 5
funcion doble(n) { devolver n * 2 }
si a > b { } sino si a == b { } sino { }
mientras cond { }          para item en lista { }
para i, item en lista { }  para clave, valor en mapa { }   (i es la posición, desde 0)
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
| `a_mapa(pedido)` | un mapa común con los campos de ese mensaje, para recorrerlos |
| `detalle_de(e)` | los datos de un error atajado: un mapa con texto, linea, clase y dato |
| `hoy()` | la fecha, "21/11/2026" (en las pruebas, siempre "01/01/2025") |
| `ahora()` | fecha y hora, "21/11/2026 14:30" (en las pruebas, "01/01/2025 12:00") |
| `leer_archivo("notas.txt")` | el texto de ese archivo (de la carpeta del programa) |
| `escribir_archivo("notas.txt", t)` | guarda el texto t en ese archivo (si ya existía, lo pisa) |

- Si a una función le das valores de más o de menos, el error trae el ejemplo:
  `obtener() lleva 3 valores y recibió 2. Por ejemplo: obtener(mapa, "clave", 0)`.
- `agregar`, `quitar`, `ordenar` y `porcion` no cambian la lista original: devuelven una nueva.
  `quitar(lista, x)` saca **por valor** (todos los que valen `x`), no por posición.
- `a_mapa(pedido)` sirve para recorrer los campos de un mensaje:
  `para campo, valor en a_mapa(pedido) { mostrar("{campo}: {valor}") }`. El mapa es una copia:
  cambiarlo no toca el mensaje.
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

### Archivos de texto: `leer_archivo` y `escribir_archivo`

```
escribir_archivo("compras.txt", unir(["yerba", "pan"], "\n"))
sea renglones = partir(leer_archivo("compras.txt"), "\n")
```

- `leer_archivo("compras.txt")` devuelve todo el archivo como un texto; con
  `partir(texto, "\n")` queda una lista con un renglón por elemento. Lee lo que guarda el Bloc
  de notas en cualquiera de sus codificaciones.
- `escribir_archivo("compras.txt", texto)` guarda ese texto. Si el archivo ya existía, **lo
  reemplaza entero** (para agregar, leelo antes y guardá lo viejo más lo nuevo). Lo que se
  guarda tiene que ser un texto: un número va con `texto(n)`, una lista con `unir(lista, "\n")`
  y un mensaje con `a_json(mensaje)`.
- Los archivos son **los de la carpeta del programa** (o de una subcarpeta que ya exista:
  `"datos/compras.txt"`). Con `"C:/Windows/algo.txt"` o `"../afuera.txt"` Mate frena y lo
  explica. En la consola, la carpeta es en la que estás parado.
- `escribir_archivo` nunca pisa un programa: no escribe en archivos `.mate`, `.py`, `.bat`,
  `.cmd` ni `.ps1`.
- Solo andan desde el programa principal (o desde una función llamada por él). Un agente no
  toca archivos: se lee afuera y se le manda el dato en un mensaje.
- Si el archivo no está, el error lo dice y sugiere el nombre parecido (o el `notas.txt.txt`
  que deja el Bloc de notas). Para seguir igual:
  `intentar { sea t = leer_archivo("notas.txt") } si falla e { ... }`, y
  `detalle_de(e).clase` vale `"archivo"`.
- Ojo: `probar` también corre el programa antes de las pruebas, así que lo que el programa
  escribe se escribe igual.

### La fecha y la hora: `hoy` y `ahora`

- `hoy()` devuelve la fecha como texto, `"21/11/2026"` (día/mes/año), y `ahora()` le agrega
  la hora, `"21/11/2026 14:30"`. Sirven para mostrar o guardar: `"Presupuesto del {hoy()}"`.
- Con `probar` devuelven siempre `"01/01/2025"` y `"01/01/2025 12:00"`: así una prueba da lo
  mismo cualquier día que se corra.
- Son textos: no se pueden restar, y compararlos con `<` o `>` es un error (como textos,
  `"21/11/2026" < "01/12/2026"` daría cualquier cosa). Con `==` y `!=` sí se puede ver si son
  la misma fecha. El día, el mes y el año salen con `partir(hoy(), "/")`.

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
  Esto vale para los números de menos de 10.000 millones. En los más grandes Mate solo quita
  el ruido del final cuando puede hacerlo sin perder cifras de verdad (los centavos de un
  monto enorme), así que `mostrar(100000000000 / 3)` muestra `33333333333.333332`.
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

Los nombres de mensajes y agentes empiezan con mayúscula; el resto (variables, funciones,
parámetros), con minúscula: Mate no acepta `sea Total = 0`.

Detalles: `partir("abc", "")` separa letra por letra; `redondear(3.14159, 2)` lleva una cantidad
entera de decimales; `rango(10, 0, -1)` cuenta para atrás; las claves de un mapa son siempre textos (`tiene(mapa, [1])` da `falso`);
solo se puede asignar a una variable o a una parte de ella (`x`, `x.campo`, `x[0]`).

## Qué cambió y puede frenar un programa viejo

Varias mejoras vuelven error cosas que antes corrían. Esta tabla junta todo lo que cambió
desde la versión 0.2 hasta la 0.3 (`python mate\mate.py --version` dice cuál tenés). Si un
archivo viejo deja de andar, casi seguro es por una de estas:

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
| Un nombre de variable, función o parámetro no puede empezar con mayúscula (`sea Total = 0`, `funcion Doble(n)`) | Pasarlo a minúscula: `sea total = 0` |
| Una condición escrita a mano que nunca es verdadero o falso (`si 1 { }`, `verdadero y 1`, `si x + 1 { }`) es un error antes de correr, aunque esté en una parte que no se ejecuta | Escribir la comparación: `si x + 1 > 0 { }` |
| `mensaje Pedido` con la `{` en el renglón de abajo ahora declara el mensaje con esos campos (antes quedaba vacío); lo mismo `crear Vendedor` | Nada: es lo que se quería escribir |
| `a_mapa` es una función incluida: no sirve como nombre de variable | Elegir otro nombre |
| Un renglón que solo calcula (`i + 1`) se avisa antes de correr, aunque esté en una parte que no se ejecuta; y ese error (también el de `numero(x)` suelto) ya no se ataja con `intentar` ni cuenta en `asegurar falla` | Guardar el resultado: `intentar { sea n = numero(dato) ... } si falla e { ... }` |
| `asegurar falla { ... }` ya no se cumple por un nombre que no existe ahí adentro | Corregir el nombre |
| `preguntar` a un agente cuyo `al recibir` solo tiene un `fallar` adentro de un `si` (y ningún `responder`) es un error antes de correr | Agregar el `responder`, o usar `enviar` |
| `sea iva = 21%` y `} si no {` son un error que explica cómo se escribe | `21 / 100` o `0.21`; `sino` todo junto |
| Comparar con `<`, `<=`, `>` o `>=` dos textos con forma de fecha (`"21/11/2026"`) es un error | Antes daba un resultado equivocado sin avisar; separar con `partir(fecha, "/")` y comparar los números |
| `crear ... llamado` con algo que no es un texto (un número, `nada`, `llamado Sur` sin comillas) es un error | Pasarlo a texto: `llamado "Sucursal {n}"` |
| Dentro de un `si`, `para`, `mientras` o `intentar` de una función, una prueba o un `al recibir`, `sea x = ...` es un error si `x` es una variable `var` del programa | Sacar el `sea` si querías cambiarla, o elegir otro nombre |
| `unir`, `texto`, `a_json`, `agregar` y `"{...}"` tampoco pueden armar un texto o una lista de más de 10.000.000 de elementos | Trabajar con menos datos por vez |
| Volver a declarar un nombre que vino con `usar` dice de qué archivo viene (cambió la redacción); el final de un archivo a medio escribir se señala en el último renglón escrito | Elegir otro nombre; no comparar el texto entero del error |
| El error de "demasiada recursión" es más largo y nombra la función; y hay lugar para 3.000 llamadas en vez de 120 | No comparar el texto entero del error |
| Cambió la redacción de los errores de `tiene()` y `quitar()` con un valor que no corresponde, y `quitar(mapa, 1)` es un error (las claves son textos) | No comparar el texto entero del error |
| Un agente con `al fallar` se hace cargo de las fallas de lo que envió: ya no aparecen como error del programa | Nada si no usás `al fallar` |
| `hoy`, `ahora`, `leer_archivo` y `escribir_archivo` son funciones incluidas: no sirven como nombre de variable (`sea hoy = ...`) | Elegir otro nombre: `sea fecha = hoy()` |
| `ayuda` seguida de una palabra (`ayuda si`) ya no muestra la ayuda general sino la de esa palabra; y `consola` es una orden | Nada: `ayuda` sola sigue igual |
| Un nombre que no existe (`totl`), o una llamada con valores de más o de menos (`largo(x, 2)`), es un error antes de correr aunque esté en una parte que no se ejecuta (un `si`, una función, un agente o una prueba que no se usan): el programa ya no arranca. Si faltan varios nombres, se avisan todos juntos | Corregir el nombre o la llamada. Adentro de `intentar` y de `asegurar falla` sigue como antes |
| `--traza` cambió de formato: cada mensaje lleva su número, lo que un agente pregunta mientras atiende va con sangría, y hay renglones nuevos (`falló`, `sin respuesta`, `la respuesta ... se descartó`). El archivo de `--traza=archivo` trae lo mismo | Nada, salvo que compares la traza letra por letra con una guardada |
| `probar` escribe los errores de cada prueba como `correr`: `archivo:5: error: ...` (antes `línea 5: ...` y `Agente al recibir X (línea 5): ...`) | Nada |

## El tope: Mate tiene que seguir siendo chico

Mate sirve porque entra en la cabeza. Para que siga así hay un presupuesto escrito, y las
pruebas del intérprete no dejan pasarse:

- **Palabras propias: 40 como mucho.** Hoy son 36 (`sea`, `si`, `agente`...).
- **Funciones incluidas: 40 como mucho.** Hoy son 39. Empezó con 20 y el plan era sumar unas
  12; con las de archivos y fechas queda lugar para una sola más. Para agregar otra hay que
  sacar una, o discutir el tope.
- **Cada agregado trae lo suyo**: su renglón en este README (en la tabla de funciones o en la
  referencia), su explicación en `ayuda <palabra>` y al menos una prueba que lo use.
- **Una sola forma de escribir cada cosa.** Nada de sinónimos (`función` con tilde, comillas
  simples, `*=`): Mate explica cómo va, pero no acepta dos maneras.
- **Un solo archivo, sin instalar nada**, y todo en castellano: palabras y errores.

Los números están en `mate.py` (`TOPE_DE_PALABRAS` y `TOPE_DE_FUNCIONES`), bien arriba.

## Límites de la versión 0.3

- Los agentes corren todos dentro del mismo programa, de a uno y en orden (por eso el resultado
  es siempre el mismo). Todavía no se conectan con agentes de IA reales ni entre máquinas.
- Todo lo que trae `usar` queda en un único espacio de nombres: dos archivos no pueden declarar
  algo con el mismo nombre.

## Pruebas del intérprete

```bash
python3 -m pytest mate/pruebas -q -p no:cacheprovider
```
