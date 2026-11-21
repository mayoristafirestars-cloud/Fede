# Las 100 mejoras de Mate

Este documento es el plan de trabajo de Mate: cien mejoras concretas, ordenadas de la más
conveniente a la menos conveniente. Está escrito para leerse sin saber programar.

## Cómo se armó esta lista

Trabajaron seis "cabezas", cada una con un papel distinto:

- **Mirada lenguaje**: usó Mate como lo usaría alguien que escribe programas todos los días y
  anotó todo lo que resultaba incómodo o sorprendente.
- **Mirada agentes**: se concentró en el segundo objetivo de Mate, que los agentes se hablen
  con mensajes con contrato, y buscó dónde esa promesa se rompe.
- **Mirada robustez**: trató de romper el intérprete a propósito, con programas mal escritos,
  archivos raros y números enormes.
- **Mirada principiante**: se puso en el lugar de alguien que no programa, usa Windows,
  PowerShell y el Bloc de notas.
- **El crítico**: leyó las más de 150 propuestas, volvió a probar las que pudo, marcó las
  repetidas, las que se contradecían entre sí y las que agrandaban el lenguaje sin necesidad.
  También sumó cosas que nadie había visto.
- **El moderador**: resolvió cada desacuerdo, fusionó las repetidas y dejó exactamente cien.

Casi todos los problemas de la lista fueron comprobados corriendo Mate de verdad, no
supuestos. Donde algo es una suposición, se dice.

**Criterio del orden**: cuánto le sirve al dueño, dividido por cuánto cuesta hacerlo y cuánto
riesgo hay de romper algo que hoy anda. Por eso arriba hay muchas mejoras "aburridas"
(que nunca aparezca un error en inglés, que los decimales se vean bien) y más abajo las
novedades del lenguaje.

**Reglas que ninguna mejora puede romper**: el intérprete sigue siendo un solo archivo, sin
instalar nada extra, con palabras en español, con errores en español claro, y los ejemplos y
las pruebas que ya existen tienen que seguir funcionando.

**Fuera de alcance por ahora**: conectar Mate con modelos de IA reales o con la red, porque
requiere claves pagas. Esas ideas están al final de la lista, anotadas pero sin programar.

## La discusión

Estos fueron los desacuerdos más interesantes y cómo se resolvieron.

### 1. Los decimales: ¿arreglar cómo se ven o cambiar cómo se calculan?

- **Qué se propuso**: tres miradas (lenguaje, robustez y principiante) encontraron que
  `0.1 + 0.2` muestra `0.30000000000000004`. Robustez propuso además que la comparación `==`
  "perdone" diferencias mínimas, y lenguaje sugirió cambiar todos los números a un sistema
  decimal exacto.
- **Qué objetó el crítico**: que una igualdad que "perdona" deja de ser confiable (dos cosas
  iguales a una tercera pueden no ser iguales entre sí) y que el sistema decimal exacto obliga
  a reescribir medio intérprete.
- **Qué se decidió**: se le da la razón al crítico. Los números se muestran limpios (mejora 13),
  `redondear` redondea como espera una persona (mejora 14) y el README va a decir: "para
  comparar plata, redondeá antes".

### 2. Funciones sin nombre y `filtrar` / `transformar`

- **Qué se propuso**: la mirada lenguaje pidió poder escribir funciones "al paso" y funciones
  que reciben otras funciones, para acortar bucles.
- **Qué objetó el crítico**: es la idea que más le cuesta a un principiante, y choca con otra
  mejora que sí importa: prohibir que las funciones viajen dentro de los mensajes.
- **Qué se decidió**: rechazada. Un `para` con un `si` adentro es más largo pero se lee de
  corrido. No está entre las cien.

### 3. ¿Cuántas funciones nuevas?

- **Qué se propuso**: entre lenguaje y robustez sumaban más de 35 funciones nuevas (texto,
  listas, números, mapas).
- **Qué objetó el crítico**: Mate tiene 20 funciones; triplicarlas es lo contrario de un
  lenguaje chico. Propuso un tope de unas 12.
- **Qué se decidió**: tope aceptado. Entran `recortar`, `reemplazar`, `empieza_con`,
  `termina_con`, `minimo`, `maximo`, `promedio`, `absoluto`, `ultimo`, `porcion`, `obtener`,
  más `pesos` y `leer`. Quedan afuera potencia, raíz, piso, techo, repetir, insertar y varias
  más. Para escribir plata había tres nombres propuestos (`formatear`, `pesos`, `moneda`):
  queda uno solo, `pesos`.

### 4. Una variable que se llama igual que una función incluida (`texto`, `tipo`, `numero`)

- **Qué se propuso**: robustez quería permitirlo ("tapar" la función); lenguaje y principiante
  se conformaban con un mensaje claro.
- **Qué objetó el crítico**: si se permite, tres renglones más abajo `texto(5)` deja de andar
  y hay que explicar qué es "tapar".
- **Qué se decidió**: se prohíbe en todos lados con un mensaje que lo explica (mejora 19).
  En cambio sí se permite usar palabras como `estado`, `tipo` o `para` como nombre de campo
  de un mensaje o de un mapa (mejora 18), que lo pidieron las cuatro miradas.

### 5. El `enviar` del programa que llega tarde

- **Qué se propuso**: agentes y robustez comprobaron que un `enviar` seguido de un
  `preguntar` ve el estado viejo. Hubo tres remedios: una palabra nueva `esperar`, entregar
  antes de cada `preguntar`, o entregar después de cada renglón.
- **Qué objetó el crítico**: entregar después de cada renglón cambia el orden de las
  conversaciones de los ejemplos; y una palabra nueva no hace falta.
- **Qué se decidió**: los mensajes pendientes se entregan solos antes de cada `preguntar`
  hecho por el programa y, dentro de una prueba, antes de cada `asegurar` (mejora 27). Sin
  palabra nueva.

### 6. Errores atajados: ¿texto o algo con más datos?

- **Qué se propuso**: lenguaje y agentes ofrecieron siete variantes distintas para que el
  error atajado con `si falla e` traiga más información.
- **Qué objetó el crítico**: hay que elegir una sola, y sin romper el ejemplo `equipo.mate`,
  que busca la palabra "clave" dentro del texto del error. También corrigió un diagnóstico:
  ese ejemplo no "se salva de casualidad", funciona a propósito.
- **Qué se decidió**: `e` sigue siendo un texto y se agrega una sola función, `detalle(e)`,
  que devuelve los datos del error (mejora 71). Y toda mejora que cambie la redacción de un
  error tiene que conservar la palabra "clave" en el error de clave inexistente.

### 7. `intentar` se traga los `asegurar`

- **Qué se propuso**: agentes y robustez mostraron que una prueba con un `asegurar` falso
  dentro de un `intentar` pasa en verde. Pidieron además una palabra nueva, `asegurar_falla`.
- **Qué objetó el crítico**: de acuerdo con el arreglo, pero no con la palabra nueva con
  guion bajo; si hace falta, que sea `asegurar falla { ... }`, con dos palabras que ya existen.
- **Qué se decidió**: `intentar` deja de atajar los `asegurar` y los topes de seguridad
  (mejora 30). El atajo `asegurar falla { }` queda más abajo (mejora 72).

### 8. Contratos más ricos

- **Qué se propuso**: agentes pidió rangos (`desde 1`), opciones (`uno de [...]`), valores
  por defecto, `lista de Tipo`, `agente Nombre` y declarar qué se responde a cada mensaje.
- **Qué objetó el crítico**: todo junto convierte la línea más simple de Mate en un
  mini-lenguaje. Propuso quedarse con `lista de Tipo` y con el contrato de respuesta escrito
  en el mensaje (`mensaje Pedido { ... } responde Cotizacion`).
- **Qué se decidió**: se acepta el recorte (mejoras 69 y 70). Los rangos, opciones y valores
  por defecto quedan anotados para más adelante (mejora 97).

### 9. Bucles infinitos y recursión

- **Qué se propuso**: tres miradas pidieron un freno para los `mientras` que nunca terminan,
  con dos mecanismos distintos; robustez pidió además correr Mate en un "hilo" aparte para
  permitir más recursión.
- **Qué objetó el crítico**: alcanza con un solo contador de pasos para todo el programa, y
  el hilo aparte complica Ctrl+C y se comporta distinto en Windows.
- **Qué se decidió**: un solo contador de pasos con un tope alto y la opción `--sin-limite`
  (mejora 12). La recursión se amplía sin hilos (mejora 78). El `preguntar ... con limite N`
  se rechaza.

### 10. Aceptar en silencio o explicar

- **Qué se propuso**: principiante y robustez querían que Mate aceptara `función` con tilde,
  comillas de Word, comillas simples, etc.
- **Qué objetó el crítico**: propuso un criterio: aceptar lo que viene de la herramienta y no
  cambia el significado (comillas curvas, espacios invisibles), y explicar con una pista lo
  que es otra forma de escribir (`función`, `if`, `;`, `&&`).
- **Qué se decidió**: criterio aceptado (mejoras 10 y 20). Así un mismo programa se escribe
  de una sola manera y los ejemplos se parecen entre sí.

### 11. Juntar muchos errores de una vez

- **Qué se propuso**: principiante pidió que Mate informe hasta 10 errores por corrida.
- **Qué objetó el crítico**: después del primer error real suelen aparecer errores falsos en
  cascada, y un principiante no distingue cuál es el verdadero.
- **Qué se decidió**: rechazado. Un error por vez, bien explicado y mostrando el renglón
  (mejora 24). Sí se acepta la otra mitad: que la revisión previa detecte nombres que no
  existen (mejora 59).

### 12. Espiar adentro de los agentes en las pruebas

- **Qué se propuso**: agentes pidió `historial()`, `enviados()`, `estado_de()` y `simular`.
- **Qué objetó el crítico**: `estado_de()` rompe a propósito la garantía de que nadie mira
  adentro de otro agente; `simular` es la única que habilita algo nuevo y deja listo el
  enchufe para un futuro agente de IA.
- **Qué se decidió**: entra `simular` (mejora 73). `estado_de()` se rechaza. El historial
  queda para más adelante (mejora 98).

## Las 100 mejoras

Cada mejora dice de qué mirada salió, cuánto esfuerzo lleva y en qué estado está. Todas
arrancan en "pendiente". Las primeras 36 son las que se programan primero, en tres tandas:

- **Tanda 1 (mejoras 1 a 12)**: que nunca aparezca un error interno en inglés.
- **Tanda 2 (mejoras 13 a 24)**: números que se ven bien y errores que ayudan.
- **Tanda 3 (mejoras 25 a 36)**: cerrar las garantías entre agentes y en las pruebas.
- **Tanda 4 (mejoras 37 a 48)**: renglones sin sorpresas, atajos (`+=`, `romper`, `leer`) y
  primeros pasos en Windows.
- **Tanda 5 (mejoras 49 a 61, salvo la 59)**: comillas dentro de `"{...}"`, avisos para rutas de
  Windows y para `1.500`, la tabla única de funciones, las funciones nuevas y más controles
  antes de correr. La 59 se salteó por ser de esfuerzo grande.
- **Tanda 6 (mejoras 62 a 75, salvo la 63 y la 65)**: `probar` más prolijo, la conversación
  guardada en un archivo, errores que dicen por dónde se llegó, contratos más completos
  (`lista de Tipo`, `responde`), `detalle_de(e)`, `asegurar falla { }`, `simular` y copias con
  nombre único. La 63 y la 65 se saltearon: cada una tiene anotado el motivo.

### Tanda 1: nunca un error interno en inglés

**1. Fijar la salida exacta de los ejemplos antes de tocar nada**
Se guarda lo que hoy imprime cada ejemplo, para que cualquier cambio en esa salida se note enseguida y no pase escondido.
*Mirada: crítico · Esfuerzo: chico · Estado: hecha*

**2. Red de seguridad: nunca mostrar un error interno de Python**
Si algo inesperado falla, o se corta con Ctrl+C, Mate lo dice en español y en un renglón, en vez de mostrar treinta líneas en inglés. Con `--depurar` se ve el detalle técnico.
*Mirada: robustez, principiante, agentes · Esfuerzo: chico · Estado: hecha*

**3. Leer archivos guardados por el Bloc de notas en cualquier codificación**
Un archivo guardado como ANSI o "Unicode" con una `ñ` hoy rompe todo. Mate va a probar las codificaciones comunes y, si no puede, explicar cómo guardarlo.
*Mirada: robustez, principiante · Esfuerzo: chico · Estado: hecha*

**4. Que la consola de Windows no se rompa con ✓, ✗ y →**
En consolas viejas esos símbolos hacen fallar a Mate. Se usa un reemplazo simple (`OK`, `FALLA`, `->`) cuando la consola no los puede mostrar.
*Mirada: robustez, principiante · Esfuerzo: chico · Estado: hecha*

**5. `devolver` y `responder` fuera de lugar se avisan antes de correr**
Hoy un `devolver 5` suelto termina en un error interno. Va a decir "'devolver' solo va dentro de una función".
Nota al hacerla: `devolver` directamente dentro de `al recibir` se dejó permitido (termina de atender sin responder), porque `ejemplos/negociacion.mate` ya lo usa.
*Mirada: lenguaje, robustez, agentes · Esfuerzo: chico · Estado: hecha*

**6. Las funciones incluidas nunca fallan con un error de Python**
`partir("abc", "")` o `redondear(2.5, 1.5)` hoy dan error interno. Cada función va a explicar en español qué valor no le sirvió.
*Mirada: lenguaje, robustez · Esfuerzo: chico · Estado: hecha*

**7. Asignar a algo que no es una variable da un error claro**
Cosas como `(a + b)[0] = 1` hoy terminan en error interno. Va a decir que solo se puede asignar a una variable o a una parte de ella.
*Mirada: robustez · Esfuerzo: chico · Estado: hecha*

**8. Usar una lista o un mapa como clave da un error claro**
`tiene({a: 1}, [1])` hoy rompe con un error interno; lo mismo un JSON raro que llega de afuera. Va a responder bien o explicar que las claves son textos.
*Mirada: robustez · Esfuerzo: chico · Estado: hecha*

**9. Números gigantes, "infinito" y "no es un número" no se cuelan**
Las cuentas con números enormes dejan de dar error interno, y `numero("inf")` deja de aceptarse, para que nunca viaje un número inválido entre agentes.
*Mirada: robustez, lenguaje · Esfuerzo: chico · Estado: hecha*

**10. Comillas de Word, espacios invisibles y símbolos de otros lenguajes**
Las comillas curvas y los espacios raros que se pegan desde Word o WhatsApp se aceptan como si fueran los comunes. Para `;`, `&&`, `//`, comillas simples o un texto sin cerrar, Mate explica cómo se escribe.
*Mirada: principiante, robustez, lenguaje, crítico · Esfuerzo: chico · Estado: hecha*

**11. Línea de comandos que ayuda**
Si falta la orden `correr`, si una opción está mal escrita (`--trasa`), si el archivo no existe o quedó como `hola.mate.txt`, Mate lo dice en español y sugiere el arreglo. Se agregan `--version` y `ayuda`.
*Mirada: principiante, robustez · Esfuerzo: chico · Estado: hecha*

**12. Freno para los programas que nunca terminan**
Un `mientras` que no avanza hoy cuelga la consola para siempre. Mate va a cortar después de muchísimos pasos y decir en qué renglón estaba. Con `--sin-limite` se desactiva.
*Mirada: principiante, robustez, agentes · Esfuerzo: chico · Estado: hecha*

### Tanda 2: números que se ven bien y errores que ayudan

**13. Los decimales se muestran limpios**
`0.1 + 0.2` va a mostrar `0.3` y no `0.30000000000000004`; `10 / 3` muestra `3.33333333333`.
Nota de la revisión: el costo es que un decimal de 16 cifras o más se muestra con 12 aunque esté escrito a mano; quedó avisado en el README. `redondear` y `pesos` ahora redondean el número que se muestra.
*Mirada: lenguaje, robustez, principiante · Esfuerzo: chico · Estado: hecha*

**14. `redondear` redondea como en la escuela**
Hoy `redondear(2.5)` da 2 y `redondear(2.675, 2)` da 2.67. Van a dar 3 y 2.68.
*Mirada: robustez · Esfuerzo: chico · Estado: hecha*

**15. `numero()` entiende los números como se escriben en Argentina**
`numero("1.234,50")` va a dar 1234.5. Un texto vacío o raro da un error claro.
*Mirada: lenguaje, principiante, robustez · Esfuerzo: chico · Estado: hecha*

**16. `pesos(n)` para mostrar plata**
Una función nueva: `pesos(1234567.891)` devuelve `$ 1.234.567,89`.
*Mirada: lenguaje, principiante · Esfuerzo: chico · Estado: hecha*

**17. "¿Quisiste decir...?" cuando un nombre no existe**
Si escribís `totl` y existe `total`, o `mostar` en vez de `mostrar`, Mate sugiere el nombre parecido. También para campos, claves, mensajes y agentes.
*Mirada: lenguaje, robustez, principiante · Esfuerzo: chico · Estado: hecha*

**18. Palabras como `estado`, `tipo` o `para` sirven como nombre de campo**
Hoy `mensaje Envio { estado: texto }` falla. Se van a poder usar las palabras propias de Mate como nombre de campo en mensajes y mapas.
*Mirada: las cuatro · Esfuerzo: chico · Estado: hecha*

**19. Error claro al usar una palabra reservada o una función incluida como nombre**
`sea y = 1` va a decir "'y' es una palabra propia de Mate, elegí otro nombre"; `sea texto = "hola"` va a decir que `texto` es una función incluida.
*Mirada: lenguaje, robustez, principiante · Esfuerzo: chico · Estado: hecha*

**20. Pistas para palabras de otros lenguajes, con tilde o con mayúscula**
`print`, `if`, `else`, `true`, `función`, `Si`, `Mostrar`: en cada caso Mate dice cómo se escribe en Mate.
Nota de la revisión: la pista sale solo si el programa no le puso ese nombre a algo suyo (`sea def = 5` y `mensaje Return` vuelven a andar).
*Mirada: principiante, robustez · Esfuerzo: chico · Estado: hecha*

**21. Pistas en las condiciones mal escritas**
`si x = 5`, `si 1 < x < 10`, `si x > 3 y < 10` y `si x > 3 entonces` van a explicar cómo se escribe cada una.
*Mirada: lenguaje, robustez, principiante · Esfuerzo: chico · Estado: hecha*

**22. `asegurar` muestra los valores cuando falla**
En vez de "no se cumplió lo asegurado", va a decir por ejemplo "dio 3 y se esperaba 4".
*Mirada: principiante, robustez · Esfuerzo: chico · Estado: hecha*

**23. El error de "no se puede cambiar" dice de qué se trata**
Hoy, al querer cambiar un parámetro, Mate habla de un `sea` que nadie escribió. Va a decir "'a' es un parámetro...", "es la variable del 'para'...", etc.
*Mirada: lenguaje, robustez · Esfuerzo: chico · Estado: hecha*

**24. El error muestra el renglón del archivo**
Debajo del mensaje se va a ver el renglón señalado, para no tener que contar líneas a mano en el Bloc de notas.
*Mirada: principiante, crítico · Esfuerzo: chico · Estado: hecha*

### Tanda 3: garantías entre agentes y en las pruebas

**25. Las funciones no pueden viajar dentro de un mensaje**
Hoy un agente puede mandarle a otro una función que le cambia el estado por atrás. Los mensajes y respuestas van a llevar solo datos.
*Mirada: agentes, robustez · Esfuerzo: chico · Estado: hecha*

**26. Un agente no puede cambiar variables de afuera a través de una función**
Se cierra un agujero: hoy un agente puede modificar una variable del programa llamando a una función de afuera.
*Mirada: robustez · Esfuerzo: chico · Estado: hecha*

**27. Los `enviar` del programa se entregan antes del siguiente `preguntar`**
Hoy un `enviar` seguido de un `preguntar` ve el estado viejo. Se va a respetar el orden en que está escrito; en las pruebas, también antes de cada `asegurar`.
*Mirada: agentes, robustez · Esfuerzo: chico · Estado: hecha*

**28. El tope de mensajes se reinicia en cada prueba**
Hoy una tanda larga de pruebas puede fallar con "se superaron 100000 mensajes" sin que haya ningún bucle.
*Mirada: agentes, robustez · Esfuerzo: chico · Estado: hecha*

**29. Cada prueba empieza limpia**
Hoy las copias de agentes y las variables del programa arrastran cambios de una prueba a la otra. Cada prueba va a arrancar igual, sin importar el orden.
*Mirada: agentes, robustez · Esfuerzo: mediano · Estado: hecha*

**30. `intentar` ya no esconde los `asegurar` que fallan**
Hoy una prueba con un `asegurar` falso dentro de un `intentar` pasa en verde. Tampoco va a atajar los topes de seguridad.
Nota de la revisión: vale dentro de las pruebas. Al correr el programa, un `asegurar` que no se cumple se ataja como cualquier error, y el de otro agente le llega como error al que le preguntó.
*Mirada: agentes, robustez · Esfuerzo: chico · Estado: hecha*

**31. Si un agente falla, vuelve a como estaba**
Hoy una venta que falló a mitad de camino queda contada. El agente que falla va a recuperar su estado anterior y no manda lo que había encolado.
*Mirada: agentes · Esfuerzo: chico · Estado: hecha*

**32. Aviso de los mensajes que quedaron sin entregar**
Si el programa se corta por un error, Mate va a decir cuántos mensajes quedaron en espera y cuáles.
*Mirada: agentes, robustez · Esfuerzo: chico · Estado: hecha*

**33. Los errores de agentes nombran el archivo correcto, y se muestran todos**
Hoy un error en un agente traído con `usar` nombra otro archivo, y en `probar` algunos errores se pierden.
*Mirada: agentes, robustez · Esfuerzo: chico · Estado: hecha*

**34. La revisión previa sigue a las copias y detecta al agente que nunca responde**
`sea v = crear Vendedor` seguido de un mensaje que `v` no entiende se va a avisar antes de correr; también preguntarle a un agente que nunca usa `responder`.
*Mirada: agentes, robustez · Esfuerzo: chico · Estado: hecha*

**35. `crear` revisa el estado inicial que le dan**
`crear V { precios: 5 }` cuando `precios` es un mapa va a fallar ahí mismo, y no más tarde adentro del agente.
*Mirada: agentes · Esfuerzo: chico · Estado: hecha*

**36. Un `enviar` de algo que el destino no entiende falla en quien lo envía**
El error aparece en el renglón del `enviar`, se puede atajar con `intentar`, y no llega suelto al final.
*Mirada: agentes · Esfuerzo: chico · Estado: hecha*

### Tanda 4: renglones sin sorpresas y primeros pasos

**37. Llaves, paréntesis y corchetes sin cerrar dicen dónde se abrieron**
"La llave que se abrió en la línea 4 (al recibir Ping) nunca se cierra", en vez de señalar el final del archivo.
Nota al hacerla: el número de renglón del error sigue siendo el del final (donde Mate notó la falta) y el mensaje dice dónde se abrió; así no cambia lo que ya mostraba la mejora 24. Cuando falta una llave en el medio, Mate adivina cuál es por la sangría.
*Mirada: robustez, principiante · Esfuerzo: chico · Estado: hecha*

**38. Un renglón que calcula algo y no lo usa es un error**
`i + 1` suelto, `mostrar "hola"` sin paréntesis o `agregar(lista, 4)` sin guardar el resultado hoy no hacen nada y nadie avisa. Va a ser un error con la pista correcta.
Nota al hacerla: se avisa al llegar a ese renglón, no antes de correr, para que un error de la propia cuenta (`numero("x")` suelto) se siga viendo primero. Llamar a una función propia, `mostrar`, `leer`, `preguntar` y `crear` pueden ir sueltos.
*Mirada: las cuatro · Esfuerzo: mediano · Estado: hecha*

**39. Una sola regla para saber dónde termina un renglón**
Hoy un `-1` al principio de un renglón se pega al renglón de arriba, y `responder` solo se come la línea siguiente. Cada sentencia va a ir en su renglón.
Nota al hacerla: la regla es "un renglón termina donde termina, salvo que quede abierto un `(`, `[` o `{`, o que termine en un operador o una coma". Lo que NO se hizo: prohibir dos sentencias en un mismo renglón (`sea a = 1 sea b = 2`), porque las pruebas que ya existían lo usan; queda permitido aunque no se recomienda.
*Mirada: lenguaje, robustez, crítico · Esfuerzo: mediano · Estado: hecha*

**40. Un `sea` de adentro no puede tapar una variable de afuera**
Escribir `sea cuenta = i` dentro de un bucle cuando ya existe `cuenta` afuera hoy no cambia nada y no avisa. Va a ser un error con la pista "sacá el 'sea'".
Nota al hacerla: vale para los bloques de adentro (`si`, `para`, `mientras`, `intentar`) y para los estados del agente. Una función o una prueba sí pueden repetir un nombre del programa: si no, una función traída con `usar` podría romperse por una variable de otro archivo.
*Mirada: lenguaje, crítico · Esfuerzo: chico · Estado: hecha*

**41. Comparar un texto con un número es un error**
Hoy `"18" == 18` da falso en silencio. Va a avisar y sugerir `numero(...)`. Comparar con `nada` sigue permitido. De paso se corrige que `[1] == [verdadero]` dé verdadero.
*Mirada: principiante, robustez · Esfuerzo: chico · Estado: hecha*

**42. README con "Primeros pasos en Windows"**
Instalar Python, abrir PowerShell, guardar un `.mate` desde el Bloc de notas y correrlo, con los comandos tal como se escriben en Windows.
*Mirada: principiante · Esfuerzo: mediano · Estado: hecha*

**43. Ejemplos graduales, de tres renglones en adelante**
`01_hola.mate`, `02_variables.mate`, hasta `06_primer_agente.mate`, comentados renglón por renglón e incluidos en las pruebas para que no queden viejos.
*Mirada: principiante · Esfuerzo: mediano · Estado: hecha*

**44. Un `mate.bat` para escribir menos**
Permite escribir `mate correr archivo.mate` o arrastrar un archivo encima, y deja la ventana abierta para leer el resultado. (Que la ventana se cierre sola con doble clic es una suposición, no se pudo comprobar.)
Nota al hacerla: `mate.bat` quedó escrito pero NO se pudo probar en una Windows de verdad (se programó en Linux). Falta que el dueño lo pruebe: doble clic, arrastrar un archivo y `.\mate\mate correr archivo.mate` desde PowerShell. El README lo avisa.
*Mirada: principiante, crítico · Esfuerzo: chico · Estado: hecha*

**45. Orden `guia`: una página de Mate para pegarle a una IA**
Imprime la referencia completa y compacta del lenguaje, para copiarla al empezar un chat con un asistente y que escriba Mate sin inventar.
Nota al hacerla: la guía trae un programa completo de ejemplo y una prueba automática lo corre, para que no quede vieja. Cuando salga la tabla única de funciones (mejora 53) conviene armar la lista de funciones desde ahí.
*Mirada: crítico · Esfuerzo: chico · Estado: hecha*

**46. Atajos `+=` y `-=`**
`suma += precio` en vez de `suma = suma + precio`.
*Mirada: lenguaje · Esfuerzo: chico · Estado: hecha*

**47. `romper` y `continuar` en los bucles**
Para salir de un `para` o `mientras` antes de tiempo, o saltar a la vuelta siguiente.
Nota al hacerla: `romper` y `continuar` pasan a ser palabras propias de Mate (ya no sirven como nombre de variable).
*Mirada: lenguaje · Esfuerzo: chico · Estado: hecha*

**48. `leer("pregunta")` para pedirle un dato a la persona**
Solo desde el programa principal (un agente no puede frenar todo esperando el teclado). En las pruebas usa respuestas preparadas.
Nota al hacerla: la "respuesta preparada" es el segundo valor: `leer("¿Cuántos?", "3")`. En `probar` nunca se espera el teclado.
*Mirada: lenguaje, principiante, crítico · Esfuerzo: chico · Estado: hecha*

### Tanda 5: textos y números sin trampas, más funciones y más controles

**49. Comillas dentro de `"{...}"`**
Se va a poder escribir `"valor {m["a"]}"`, que hoy figura como límite en el README.
Nota al hacerla: adentro de las llaves va cualquier cuenta, también con textos que a su vez tengan llaves. Lo que antes era un error (una llave sin cerrar, una comilla de más) lo sigue siendo, con el mismo mensaje.
*Mirada: lenguaje, robustez, principiante · Esfuerzo: mediano · Estado: hecha*

**50. Las barras de las rutas de Windows no se rompen en silencio**
`"C:\temp\nuevo"` hoy sale con un salto de línea en el medio. Mate va a avisar y sugerir `/` o doble barra.
Nota al hacerla: son dos avisos. Un texto que empieza como ruta (`C:\` con una sola barra) es un error aunque sus barras formen `\t` o `\n`; y una barra seguida de una letra que no significa nada (`\a`, `\d`) también, cuando antes la barra desaparecía sin avisar. Valen `\n`, `\t`, `\\`, `\"`, `\{` y `\}`. Una ruta sin letra de disco cuyas barras den justo `\n` o `\t` (`"datos\nuevo.txt"`) no se puede distinguir de un texto con salto de renglón, así que no se avisa.
*Mirada: lenguaje, robustez · Esfuerzo: chico · Estado: hecha*

**51. Aviso para `1.500` y `3,5` escritos en el código**
`1.500` vale uno y medio, no mil quinientos: Mate va a avisar. Para miles se va a poder escribir `1_500`. Y `3,5` va a decir "los decimales van con punto".
Nota al hacerla: se resolvió como error antes de correr, no como aviso (Mate no tiene avisos que dejen seguir). Para no prohibir decimales de verdad, salta solo con una a tres cifras, punto y tres decimales terminados en cero (`1.500`, `12.250`): esos siempre tienen una forma más corta (`1.5`, `12.25`). `2.125` o `1.999` pasan como decimales. `3,5` se avisa cuando la coma no está dentro de paréntesis o corchetes; `mostrar(3,5)` sigue mostrando dos valores.
*Mirada: lenguaje, robustez, principiante · Esfuerzo: chico · Estado: hecha*

**52. Mensajes de error que no se leen como otra frase**
"No se puede hacer nada + numero" pasa a ser "no se puede sumar el valor nada con un número", con la causa probable ("¿a la función le falta un devolver?").
Nota al hacerla: se cambió la redacción solo cuando hay un `nada` de por medio (sumar, comparar, campos, posiciones, condiciones, recorrer, llamar y las funciones incluidas). Los demás mensajes (`no se puede hacer numero + logico`) quedaron como estaban para no mover lo que ya se conoce.
*Mirada: robustez, principiante · Esfuerzo: chico · Estado: hecha*

**53. Una tabla única de funciones incluidas**
Un solo lugar con el nombre, cuántos valores lleva y un ejemplo de cada función. De ahí salen los errores con ejemplo, las sugerencias, la guía y la tabla del README.
Nota al hacerla: la tabla `FUNCIONES` de `mate.py` tiene, por función, cuántos valores lleva, un ejemplo y qué hace. De ahí salen el control de cantidad de valores, el `Por ejemplo: ...` del error, la lista de la guía y la tabla del README (una prueba controla que el README coincida renglón por renglón). Se ajustaron cuatro pruebas viejas que comparaban el texto entero de esos errores.
*Mirada: crítico · Esfuerzo: mediano · Estado: hecha*

**54. Funciones de texto que faltan**
`recortar`, `reemplazar`, `empieza_con` y `termina_con`, para limpiar lo que escribe una persona o devuelve un agente.
Nota al hacerla: con las de la mejora 55 y `obtener` quedan usadas las funciones nuevas del tope acordado en la discusión (punto 3).
*Mirada: lenguaje · Esfuerzo: chico · Estado: hecha*

**55. Funciones de listas y números que faltan**
`minimo`, `maximo`, `promedio`, `absoluto`, `ultimo`, `porcion`, y un tercer valor en `rango` para ir de a saltos.
Nota al hacerla: `minimo` y `maximo` aceptan una lista de números o una toda de textos; con la lista vacía es un error, igual que `promedio` y `ultimo`. `porcion(lista, desde, hasta)` no incluye la posición `hasta` y, si se pasa del final, llega hasta donde haya; `ultimo` y `porcion` también sirven con textos. Ojo: `minimo`, `maximo`, `promedio`, `ultimo`, `absoluto`, `porcion` y `obtener` dejan de servir como nombre de variable (está en "Qué cambió" del README).
*Mirada: lenguaje · Esfuerzo: chico · Estado: hecha*

**56. `obtener(mapa, clave, por_defecto)` y un error que lista lo que sí hay**
Cuando falta una clave, Mate va a decir cuáles tiene el mapa y sugerir la parecida.
Nota al hacerla: `obtener` lleva siempre los tres valores, para que nunca devuelva `nada` sin que se lo pidan. El error de clave muestra la sugerencia si hay una parecida y, si no, hasta ocho claves del mapa; conserva la palabra "clave". Lo mismo para un campo que no está (`mapa.campo`).
*Mirada: lenguaje, robustez · Esfuerzo: chico · Estado: hecha*

**57. `ordenar` por campo y con el abecedario español**
`ordenar(productos, "precio")`, y los textos ordenados sin que las mayúsculas vayan primero ni la ñ al final.
Nota al hacerla: el abecedario español se usa en `ordenar`, `minimo` y `maximo`. Las comparaciones `<` y `>` entre textos no se tocaron: siguen el orden de siempre (mayúsculas primero). Con el campo, todos los valores tienen que ser números o todos textos.
*Mirada: lenguaje, robustez · Esfuerzo: mediano · Estado: hecha*

**58. Errores de posición más claros en las listas**
"La lista tiene 3 elementos: las posiciones van de 0 a 2", y pistas para el último elemento y para posiciones que salieron de una cuenta con decimales.
Nota al hacerla: el mensaje conserva las palabras "fuera de rango". Al asignar (`lista[3] = x`) la pista es `agregar(lista, valor)`.
*Mirada: lenguaje, robustez · Esfuerzo: chico · Estado: hecha*

**59. La revisión previa detecta nombres que no existen**
Hoy un nombre mal escrito dentro de una parte poco usada del programa recién falla el día que se ejecuta. Se va a avisar antes de correr, junto con la cantidad de valores equivocada en una llamada.
Nota (tanda 5): salteada por ser de esfuerzo grande. Necesita seguir, sin correr el programa, qué nombres se ven desde cada bloque, función, agente y archivo traído con `usar`; hecha a medias daría errores falsos, que es peor que no avisar.
*Mirada: robustez, principiante · Esfuerzo: grande · Estado: pendiente*

**60. Más controles antes de correr**
`responder`, `remitente` y `yo` fuera de un agente; claves repetidas en un mapa; parámetros o estados repetidos; `nada` en un campo obligatorio.
Nota al hacerla: `responder` fuera de un agente ya se avisaba (mejora 5). `yo` y `remitente` son un error también dentro de una función de afuera de un agente, aunque la llame un agente: hay que pasarle el agente como valor. Se sumó el estado repetido dentro de `crear`.
*Mirada: agentes, robustez · Esfuerzo: mediano · Estado: hecha*

**61. Prueba de bombardeo: "nunca un error interno"**
Una prueba automática que rompe los ejemplos de cientos de maneras y comprueba que Mate siempre contesta en español.
Nota al hacerla: la prueba rompe cada uno de los 11 ejemplos de 60 maneras con un sorteo fijo (siempre las mismas) y los pasa por `correr` y `probar`: 1.320 corridas en un par de segundos. Antes de dejarla así se la corrió una vez con 33.000 variantes y no apareció ningún error interno.
*Mirada: crítico · Esfuerzo: chico · Estado: hecha*

### Tanda 6: pruebas más cómodas, contratos más completos y errores que cuentan el camino

**62. `probar` más prolijo**
No mezcla la salida del programa con los resultados, avisa si el archivo no tiene pruebas y si hay dos pruebas con el mismo nombre.
Nota al hacerla: lo que cada prueba muestra con `mostrar` aparece debajo de su nombre, con una barra `|` adelante. Si no hay pruebas, `probar` lo dice y muestra cómo se escribe una (ya no dice `0 de 0 pruebas pasaron`). Dos pruebas con el mismo nombre son un error antes de correr.
*Mirada: principiante, agentes · Esfuerzo: chico · Estado: hecha*

**63. Una traza que muestra las fallas**
Mensajes numerados, sangría para las preguntas anidadas, y renglones "falló" y "sin respuesta", para seguir la conversación completa.
Nota (tanda 6): salteada. Cualquiera de los tres cambios (números, sangría, renglones "falló") modifica la salida de `--traza` de los ejemplos `mercado.mate` y `negociacion.mate`, que las pruebas existentes comparan letra por letra. Hay que decidir primero si esas salidas se pueden cambiar.
*Mirada: agentes · Esfuerzo: mediano · Estado: pendiente*

**64. Guardar la conversación en un archivo**
`--traza=conversacion.txt` deja la conversación en un archivo que se abre con el Bloc de notas, con un resumen al final.
Nota al hacerla: con `--traza=archivo` la conversación no se muestra en pantalla, va al archivo. El resumen dice cuántos mensajes se entregaron, cuántos con `enviar`, cuántos con `preguntar` y cuántos fallaron. Mate no acepta un nombre terminado en `.mate` o `.py`, para no pisar un programa. Como la 63 quedó pendiente, los renglones del archivo son los mismos que muestra `--traza`.
*Mirada: agentes · Esfuerzo: chico · Estado: hecha*

**65. Aviso cuando una respuesta no tiene quién la reciba**
Si un agente responde a un `enviar` del programa, hoy la respuesta desaparece. Mate va a avisar y sugerir `preguntar`.
Nota (tanda 6): se programó y se deshizo. El ejemplo `mercado.mate` hace exactamente esto a propósito (el mismo `al recibir` sirve para un `enviar` del programa y para un `preguntar` de las pruebas), así que pasaba a mostrar un aviso en cada corrida. Antes de hacerla hay que decidir cómo distinguir ese uso, o cambiar el ejemplo.
*Mirada: agentes · Esfuerzo: chico · Estado: pendiente*

**66. El error de "ciclo de preguntas" muestra la cadena**
"A → B → C → A", diciendo quién le preguntó a quién y en qué renglón.
Nota al hacerla: el error sigue empezando con "ciclo de preguntas" y sigue diciendo quién "todavía está atendiendo otro mensaje"; en el medio trae la cadena y los renglones.
*Mirada: agentes · Esfuerzo: chico · Estado: hecha*

**67. Los errores dicen por dónde se llegó**
"En precio (línea 2), llamada desde a (línea 4)" y, entre agentes, "se lo preguntó A (línea 16)".
Nota al hacerla: el recorrido aparece en un renglón aparte, "cómo se llegó: ...", debajo del renglón señalado (en `correr` y en `probar`). El texto del error no cambia, así que lo que ataja `si falla e` es lo mismo de antes. Si una función se llama a sí misma muchas veces, el recorrido se acorta con puntos suspensivos.
*Mirada: agentes, robustez · Esfuerzo: mediano · Estado: hecha*

**68. Responder algo que no es un mensaje a un `enviar` da un error con renglón**
Hoy ese error llega tarde y sin número de línea.
Nota al hacerla: el error ahora señala el renglón del `responder`. También lo trae el de "respondió X a Y, pero Y no tiene 'al recibir X'". Dos pruebas viejas comprobaban justamente que el error señalaba solo el `al recibir`: se actualizaron esos dos renglones.
*Mirada: agentes · Esfuerzo: chico · Estado: hecha*

**69. `lista de Tipo` en los contratos**
`vendedores: lista de agente` o `items: lista de Pedido`, para que no pase una lista con cosas mezcladas.
Nota al hacerla: vale `lista de` cualquier tipo, también `lista de lista de numero`, y se puede marcar opcional (`lista de texto?`). Lo escrito a mano se revisa antes de correr; lo demás, al armar el mensaje, y el error dice en qué posición está lo que no corresponde.
*Mirada: lenguaje, agentes · Esfuerzo: mediano · Estado: hecha*

**70. Contrato de respuesta: `responde`**
`mensaje Pedido { ... } responde Cotizacion` declara qué se contesta, y Mate lo controla del lado de quien responde.
Nota al hacerla: se puede declarar `responde` con un mensaje, un tipo común o una `lista de ...`. Responder otra cosa es una falla del que responde (su estado vuelve atrás) y el error señala su `responder`. Si lo que responde está escrito a mano, se avisa antes de correr. Un mensaje sin `responde` sigue aceptando cualquier respuesta.
*Mirada: agentes, robustez · Esfuerzo: mediano · Estado: hecha*

**71. `detalle(e)`: los datos de un error atajado**
Devuelve el texto, el renglón, una clase de error que no cambia con la redacción, y el dato original de `fallar`.
Nota al hacerla: la función se llama `detalle_de(e)` y no `detalle(e)`, porque el ejemplo `equipo.mate` ya usa `detalle` como nombre de variable y una función incluida ocupa su nombre. Devuelve un mapa con `texto`, `linea`, `clase` y `dato`. Las clases son: fallar, asegurar, contrato, clave, posicion, division, nombre, numero, json, agente, ciclo y otro. `e` sigue siendo un texto.
*Mirada: lenguaje, agentes, crítico · Esfuerzo: mediano · Estado: hecha*

**72. `asegurar falla { ... }`**
Una forma corta de escribir la prueba "esto tiene que fallar".
Nota al hacerla: después de la llave se puede poner una coma y un texto propio. Igual que `intentar`, no cuenta como falla un `asegurar` de la prueba que no se cumple ni el freno de pasos. También funciona fuera de las pruebas.
*Mirada: agentes, robustez, crítico · Esfuerzo: chico · Estado: hecha*

**73. `simular`: reemplazar un agente en una prueba**
Dentro de una prueba se puede decir "en esta prueba, Vendedor contesta esto". Deja listo el enchufe para probar sin un agente de IA real.
Nota al hacerla: se escribe `simular Vendedor al recibir Pedido como p { ... }` y solo va dentro de una prueba. Vale hasta que termina esa prueba. Lo simulado ve las variables de la prueba (no las puede cambiar), no ve el estado del agente y tiene que cumplir el contrato `responde`. Solo se simula un mensaje que el agente ya recibe. Suma una palabra al lenguaje: `simular`.
*Mirada: agentes · Esfuerzo: mediano · Estado: hecha*

**74. Copias de agentes con nombre único**
No se pueden crear dos copias con el mismo nombre, las copias sobreviven al ida y vuelta por JSON, y el apodo acepta cualquier valor de texto.
Nota al hacerla: dos copias con el mismo nombre son un error en el renglón del segundo `crear`; también en una prueba, si el programa ya había creado esa copia. El nombre después de `llamado` puede ser una cuenta de textos (`"Sucursal " + ciudad`) y no puede estar vacío.
*Mirada: agentes, robustez · Esfuerzo: chico · Estado: hecha*

**75. `de_json(texto, "Pedido")` exige el tipo**
El que recibe datos de afuera puede pedir "esto tiene que ser un Pedido" y recibir un error claro si no lo es.
Nota al hacerla: el segundo valor puede ser un mensaje, un tipo común o una `lista de ...`. Si se pide un mensaje y el texto trae un mapa suelto con esos campos, Mate arma el mensaje con ellos (así llegan los datos de programas que no conocen Mate).
*Mirada: agentes · Esfuerzo: chico · Estado: hecha*

### Lo que sigue

**76. `enviar` a una lista de agentes**
`enviar Aviso { ... } a [norte, sur]` le manda el mismo mensaje a cada uno.
*Mirada: agentes · Esfuerzo: chico · Estado: pendiente*

**77. `al fallar`: que el agente se entere si su `enviar` falló**
Un manejador opcional que recibe el aviso cuando un mensaje enviado no pudo atenderse, para no quedarse esperando para siempre.
*Mirada: agentes · Esfuerzo: mediano · Estado: pendiente*

**78. Más lugar para las funciones que se llaman a sí mismas**
Hoy se cortan cerca de 120 llamadas. Se sube a unas miles, con un error que nombra la función.
*Mirada: robustez, crítico · Esfuerzo: chico · Estado: pendiente*

**79. Los nombres con mayúscula quedan solo para mensajes y agentes**
`sea Listo = verdadero` va a dar un error que lo explica; y `preguntar Ping a A` va a decir "escribí Ping {}".
*Mirada: robustez · Esfuerzo: chico · Estado: pendiente*

**80. `mensaje`, `agente` y `crear` aceptan la llave en el renglón de abajo**
Hoy eso declara un mensaje vacío sin avisar.
*Mirada: robustez, crítico · Esfuerzo: chico · Estado: pendiente*

**81. Aviso de condiciones que no son verdadero o falso**
`si 1 { }` o `verdadero y 1` se avisan antes de correr, y no según los datos del momento.
*Mirada: lenguaje · Esfuerzo: chico · Estado: pendiente*

**82. Mensaje correcto de `tiene()` con textos**
`tiene("hola", 1)` va a decir que en un texto se busca otro texto, en vez de "no aplica a texto".
*Mirada: lenguaje · Esfuerzo: chico · Estado: pendiente*

**83. `quitar` bien explicado y la pista de textos solo cuando corresponde**
Documentar que `quitar` saca por valor, y no sugerir "usá texto()" cuando la cuenta no tiene ningún texto.
*Mirada: lenguaje · Esfuerzo: chico · Estado: pendiente*

**84. `para posicion, item en lista`**
Recorrer una lista sabiendo la posición, o un mapa con clave y valor a la vez.
*Mirada: lenguaje · Esfuerzo: chico · Estado: pendiente*

**85. Errores de `usar` con más pistas**
Prueba agregando `.mate` al nombre y dice desde qué archivo y renglón se trajo el archivo con el error.
*Mirada: principiante, robustez · Esfuerzo: chico · Estado: pendiente*

**86. `a_mapa(mensaje)`**
Convierte un mensaje en un mapa común cuando hace falta recorrerlo.
*Mirada: lenguaje, crítico · Esfuerzo: chico · Estado: pendiente*

**87. `probar` con varios archivos o una carpeta**
`mate probar mate\ejemplos` corre todas las pruebas y da un total general.
*Mirada: principiante · Esfuerzo: chico · Estado: pendiente*

**88. Consola interactiva**
Orden `consola` para probar renglones sueltos sin crear un archivo.
*Mirada: principiante · Esfuerzo: mediano · Estado: pendiente*

**89. Versión 0.3 y sección "Qué cambió"**
Varias mejoras vuelven error cosas que hoy corren. El README va a listar cada regla nueva y cómo corregir un archivo viejo.
Nota: después de la revisión de las tandas 1 a 3 el README ya tiene la sección "Qué cambió y puede frenar un programa viejo". Queda pendiente el cambio de número de versión y mantenerla al día.
*Mirada: crítico · Esfuerzo: chico · Estado: pendiente*

**90. Un tope para que Mate siga siendo chico**
Dejar escrito el presupuesto: pocas palabras nuevas, unas 12 funciones nuevas, y cada agregado con su renglón en el README y su prueba.
*Mirada: crítico · Esfuerzo: chico · Estado: pendiente*

**91. Leer y escribir archivos de texto**
`leer_archivo` y `escribir_archivo`, solo desde el programa principal, solo dentro de la carpeta del programa y sin poder pisar archivos `.mate` ni `.py`.
*Mirada: lenguaje, crítico · Esfuerzo: mediano · Estado: pendiente*

**92. `hoy()` y `ahora()`**
La fecha y la hora. En las pruebas devuelven una fecha fija, para que el resultado sea siempre el mismo.
*Mirada: lenguaje, crítico · Esfuerzo: chico · Estado: pendiente*

**93. Un solo formato para todos los errores**
Los errores de agentes y los comunes se ven igual, con el archivo y el renglón adelante.
*Mirada: principiante · Esfuerzo: chico · Estado: pendiente*

**94. `ayuda <palabra>`**
`mate ayuda si` o `mate ayuda largo` muestra una explicación corta con un ejemplo, tomada de la tabla única de funciones.
*Mirada: principiante · Esfuerzo: mediano · Estado: pendiente*

**95. Valores por defecto en los parámetros (para más adelante)**
`funcion con_iva(precio, tasa = 0.21)`. Postergada para no agrandar el lenguaje todavía.
*Mirada: lenguaje · Esfuerzo: chico · Estado: pendiente*

**96. Textos de varios renglones (para más adelante)**
Textos con triple comilla. Van a hacer falta cuando los agentes lleven instrucciones largas.
*Mirada: lenguaje · Esfuerzo: mediano · Estado: pendiente*

**97. Contratos que validan valores (para más adelante)**
Rangos (`desde 1`), opciones fijas y valores por defecto en los campos de un mensaje.
*Mirada: agentes · Esfuerzo: mediano · Estado: pendiente*

**98. Historial de mensajes en las pruebas (para más adelante)**
Poder preguntar dentro de una prueba qué mensajes se mandaron.
*Mirada: agentes · Esfuerzo: mediano · Estado: pendiente*

**99. Un "sobre" para los mensajes y número de conversación (para más adelante)**
Guardar quién, a quién y en respuesta a qué. Es preparación para conectar programas entre sí; no se programa ahora.
*Mirada: agentes · Esfuerzo: mediano · Estado: pendiente*

**100. Conexión con modelos de IA y con la red (fuera de alcance por ahora)**
No se programa: requiere claves pagas que el dueño todavía no decidió usar. Sí se va a documentar el plan y la idea de un agente "simulado" que lee sus respuestas de un archivo.
*Mirada: principiante · Esfuerzo: chico · Estado: pendiente*

## Lo que se descartó

Para que quede constancia, estas ideas se discutieron y no entraron: funciones sin nombre con
`filtrar` y `transformar`; igualdad "aproximada" entre decimales; cambiar todos los números a
decimales exactos; permitir que una variable tape una función incluida; aceptar `función` con
tilde como sinónimo; comillas simples como segunda forma de texto; informar diez errores
juntos; aceptar decimales como posición de una lista; `preguntar ... a todos`; `preguntar ...
con limite`; `estado_de()` para espiar agentes; un segundo formato de errores para
herramientas; la traza en formato JSON; `*=` y `/=`; y la condición corta en un renglón.
