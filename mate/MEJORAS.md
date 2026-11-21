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
  por defecto quedan anotados para más adelante (mejora 97, que se hizo en la tanda 10).

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
  queda para más adelante (mejora 98, que se hizo en la tanda 10).

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
- **Tanda 9 (mejoras 59, 63, 65 y 93)**: las cuatro que habían quedado salteadas por cambiar
  salidas que las pruebas comparaban letra por letra, o por ser de esfuerzo grande. El dueño
  decidió que esas salidas se podían cambiar.
- **Tanda 10 (mejoras 95 a 99)**: lo que estaba anotado "para más adelante" y el dueño pidió
  terminar: valores por defecto en los parámetros, textos de varios renglones, contratos que
  validan valores, el historial de mensajes en las pruebas y el "sobre" con el número de
  conversación.
- **Tanda 11 (mejora 100)**: conectar los agentes con una IA de verdad (Claude), que había
  quedado afuera por ser paga. El dueño pidió hacerla. Se programó con modo simulado para las
  pruebas, pero sin poder probarla contra el servicio real: está dicho en su nota.
- **Después de las 100 (mejoras 101 a 103, versión 0.4)**: que un agente aprenda con el uso:
  memoria entre corridas, bitácora de errores y lecciones. Están al final, en "Lo que vino
  después de las 100".

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
Nota al hacerla (tanda 9): hecha completa pero conservadora: ante la duda no avisa. El texto es el mismo que al correr (`no existe 'totl'. ¿Quisiste decir 'total'?`). Lo declarado afuera de todo vale aunque esté más abajo o venga de un `usar`; lo de adentro de un bloque, en ese bloque. No se mira adentro de `intentar { }` ni de `asegurar falla { }` (ahí la falla se ataja o es lo que se prueba), y en la consola no se avisa de nombres (lo que falta se puede escribir después). La cantidad de valores se revisa en las funciones incluidas y en las propias cuyo nombre se usa para una sola cosa. Cada nombre que falta se avisa una vez. Para comprobar que no hay errores falsos se hicieron más de 40.000 corridas de programas rotos al azar, comparando cada aviso con lo que pasaba al correr: ningún aviso cayó sobre un nombre que existía. Ojo: un programa viejo con un nombre mal escrito en una parte que nunca se ejecuta ahora no arranca (está en "Qué cambió"). Si un día cambia cómo se declaran los parámetros (mejora 95), hay que tocar `revisar_nombres`.
*Mirada: robustez, principiante · Esfuerzo: grande · Estado: hecha*

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
Nota al hacerla (tanda 9): se decidió que sí se podían cambiar. Cada mensaje lleva su número (el último coincide con el total del resumen); lo que pasa con ese mensaje repite el número: `responde`, `falló: motivo` o `sin respuesta`. Lo que un agente pregunta mientras atiende va con sangría. El aviso de `al fallar` va sin número, porque no es un mensaje. El archivo de `--traza=archivo` (mejora 64) trae los mismos renglones. Se actualizaron las salidas fijadas de `equipo`, `mercado` y `negociacion` con `--traza` y cuatro pruebas más que miraban un renglón de la traza. De paso, "Fallaron N" del resumen ahora cuenta también el mensaje que no se pudo ni empezar a atender (un ciclo de preguntas, por ejemplo).
*Mirada: agentes · Esfuerzo: mediano · Estado: hecha*

**64. Guardar la conversación en un archivo**
`--traza=conversacion.txt` deja la conversación en un archivo que se abre con el Bloc de notas, con un resumen al final.
Nota al hacerla: con `--traza=archivo` la conversación no se muestra en pantalla, va al archivo. El resumen dice cuántos mensajes se entregaron, cuántos con `enviar`, cuántos con `preguntar` y cuántos fallaron. Mate no acepta un nombre terminado en `.mate` o `.py`, para no pisar un programa. Como la 63 quedó pendiente, los renglones del archivo son los mismos que muestra `--traza`.
*Mirada: agentes · Esfuerzo: chico · Estado: hecha*

**65. Aviso cuando una respuesta no tiene quién la reciba**
Si un agente responde a un `enviar` del programa, hoy la respuesta desaparece. Mate va a avisar y sugerir `preguntar`.
Nota (tanda 6): se programó y se deshizo. El ejemplo `mercado.mate` hace exactamente esto a propósito (el mismo `al recibir` sirve para un `enviar` del programa y para un `preguntar` de las pruebas), así que pasaba a mostrar un aviso en cada corrida. Antes de hacerla hay que decidir cómo distinguir ese uso, o cambiar el ejemplo.
Nota al hacerla (tanda 9): el aviso sale solo en la traza (en pantalla o en el archivo), como un renglón más: `la respuesta de Comprador se descartó (para recibirla, usá 'preguntar' en vez de 'enviar'): ...`. Con `correr` a secas no se muestra nada nuevo, así que `mercado.mate` sigue igual; con `--traza` ese ejemplo muestra el renglón dos veces, que es lo que de verdad pasa.
*Mirada: agentes · Esfuerzo: chico · Estado: hecha*

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

### Tanda 7: agentes que se enteran, nombres y condiciones sin trampas, y probar una carpeta

**76. `enviar` a una lista de agentes**
`enviar Aviso { ... } a [norte, sur]` le manda el mismo mensaje a cada uno.
Nota al hacerla: vale una lista escrita ahí mismo o una variable que guarda una lista de agentes. Primero se revisan todos: si alguno no es un agente o no sabe recibir el mensaje, no sale para ninguno. Una lista vacía no manda nada y no es un error. `preguntar` sigue siendo de a uno, y si se le da una lista el error sugiere recorrerla con `para`.
*Mirada: agentes · Esfuerzo: chico · Estado: hecha*

**77. `al fallar`: que el agente se entere si su `enviar` falló**
Un manejador opcional que recibe el aviso cuando un mensaje enviado no pudo atenderse, para no quedarse esperando para siempre.
Nota al hacerla: se escribe `al fallar como f { ... }` dentro del agente, una sola vez. `f` es un mapa con `motivo` (el texto del error), `mensaje` (lo que había mandado) y `destino` (el agente que falló). Con `al fallar`, la falla queda en manos del que envió y ya no se anota como error del programa; si el propio `al fallar` falla, eso sí se anota. Adentro no va `responder`. No suma palabras al lenguaje (`al` y `fallar` ya existían) y no cambia nada para los agentes que no lo declaran. En `--traza` aparece un renglón nuevo, "X se entera de que Y no pudo atender Z", solo en ese caso.
*Mirada: agentes · Esfuerzo: mediano · Estado: hecha*

**78. Más lugar para las funciones que se llaman a sí mismas**
Hoy se cortan cerca de 120 llamadas. Se sube a unas miles, con un error que nombra la función.
Nota al hacerla: hay lugar para 3.000 llamadas una adentro de la otra, y el error dice cuál fue la última función. Se hizo sin hilos: Mate le pide más lugar a Python solo mientras corre el programa y después lo deja como estaba. Vale con Python 3.12 o más nuevo; con uno más viejo queda el tope de antes (unas 120), porque ahí pedir más lugar puede hacer que Python se caiga. La prueba vieja que comparaba el texto entero del error (`demasiada recursión`) ahora mira cómo empieza.
*Mirada: robustez, crítico · Esfuerzo: chico · Estado: hecha*

**79. Los nombres con mayúscula quedan solo para mensajes y agentes**
`sea Listo = verdadero` va a dar un error que lo explica; y `preguntar Ping a A` va a decir "escribí Ping {}".
Nota al hacerla: vale para variables, funciones, parámetros, estados y las variables de `para`, `como` y `si falla`. El error propone el nombre en minúscula (o `mi_estado` si en minúscula es una palabra de Mate). Un mensaje nombrado sin llaves se avisa antes de correr en cualquier lugar, no solo en `preguntar`. Dos pruebas viejas decían que `var Estado` y `funcion Crear` se aceptaban: se actualizaron esos dos renglones.
*Mirada: robustez · Esfuerzo: chico · Estado: hecha*

**80. `mensaje`, `agente` y `crear` aceptan la llave en el renglón de abajo**
Hoy eso declara un mensaje vacío sin avisar.
Nota al hacerla: `agente` ya lo aceptaba; se sumaron `mensaje` y `crear`. No hay confusión posible, porque un renglón nunca empieza con `{` por otro motivo.
*Mirada: robustez, crítico · Esfuerzo: chico · Estado: hecha*

**81. Aviso de condiciones que no son verdadero o falso**
`si 1 { }` o `verdadero y 1` se avisan antes de correr, y no según los datos del momento.
Nota al hacerla: se avisa lo que está escrito a mano y nunca puede dar verdadero o falso: un número, un texto, una lista, un mapa, `nada`, un mensaje o una cuenta (`x + 1`), en `si`, `mientras`, `asegurar` y a los lados de `y`, `o`, `no`. Una variable que resulta no ser lógica se sigue avisando al correr, con el mismo texto. Tres pruebas viejas usaban `si 1` o `asegurar 1` para mirar el control que se hace al correr: ahora guardan el valor en una variable.
*Mirada: lenguaje · Esfuerzo: chico · Estado: hecha*

**82. Mensaje correcto de `tiene()` con textos**
`tiene("hola", 1)` va a decir que en un texto se busca otro texto, en vez de "no aplica a texto".
Nota al hacerla: si lo buscado es un número, el error además muestra cómo pasarlo a texto. Con algo que no es lista, mapa ni texto dice qué espera y qué recibió.
*Mirada: lenguaje · Esfuerzo: chico · Estado: hecha*

**83. `quitar` bien explicado y la pista de textos solo cuando corresponde**
Documentar que `quitar` saca por valor, y no sugerir "usá texto()" cuando la cuenta no tiene ningún texto.
Nota al hacerla: el README y la guía dicen que `quitar` saca por valor y no por posición; `quitar` sobre un texto sugiere `reemplazar`, y `quitar(mapa, 1)` avisa que las claves son textos. La pista "usá texto()" ya salía solo cuando hay un texto en la cuenta: se agregó la prueba que lo cuida.
*Mirada: lenguaje · Esfuerzo: chico · Estado: hecha*

**84. `para posicion, item en lista`**
Recorrer una lista sabiendo la posición, o un mapa con clave y valor a la vez.
Nota al hacerla: en una lista da la posición (desde 0) y el elemento; en un mapa, la clave y el valor; en un texto, la posición y la letra. Los dos nombres son fijos adentro del bucle, igual que en el `para` común.
*Mirada: lenguaje · Esfuerzo: chico · Estado: hecha*

**85. Errores de `usar` con más pistas**
Prueba agregando `.mate` al nombre y dice desde qué archivo y renglón se trajo el archivo con el error.
Nota al hacerla: si el archivo no aparece, el error sugiere el nombre parecido, avisa si el Bloc de notas lo guardó como `.txt`, o muestra los `.mate` que hay en esa carpeta. El "se trajo con 'usar' desde..." se agrega a los errores de escritura del archivo traído; los que pasan al correr ya nombraban el archivo.
*Mirada: principiante, robustez · Esfuerzo: chico · Estado: hecha*

**86. `a_mapa(mensaje)`**
Convierte un mensaje en un mapa común cuando hace falta recorrerlo.
Nota al hacerla: devuelve una copia: cambiar el mapa no toca el mensaje. Si ya es un mapa lo devuelve igual. Suma una función incluida más, y el tope de unas 12 funciones nuevas de la discusión 3 ya estaba pasado: conviene tratar la mejora 90 antes de agregar otra.
*Mirada: lenguaje, crítico · Esfuerzo: chico · Estado: hecha*

**87. `probar` con varios archivos o una carpeta**
`mate probar mate\ejemplos` corre todas las pruebas y da un total general.
Nota al hacerla: de una carpeta toma los `.mate` que tiene directamente adentro (no entra en subcarpetas). Cada archivo corre aparte, con su nombre arriba; al final va el total y la lista de los que tuvieron problemas. Un archivo sin pruebas dice `(sin pruebas)` y no cuenta como problema. `correr` y `verificar` siguen llevando un solo archivo.
*Mirada: principiante · Esfuerzo: chico · Estado: hecha*

### Tanda 8: consola, ayuda por palabra, archivos, fechas y el tope escrito

**88. Consola interactiva**
Orden `consola` para probar renglones sueltos sin crear un archivo.
Nota al hacerla: los renglones se numeran de corrido (`  1>`), así un error que dice "línea 4" se entiende. Un valor suelto (`2 + 3`) se muestra solo; si queda una llave abierta sigue en el renglón de abajo, y un renglón vacío corta. Solo en la consola se puede volver a declarar un `sea`, un `var`, una función o un agente para corregirlo. Un error no la cierra. Las pruebas no corren ahí (lo dice). Se sale con `salir`.
*Mirada: principiante · Esfuerzo: mediano · Estado: hecha*

**89. Versión 0.3 y sección "Qué cambió"**
Varias mejoras vuelven error cosas que hoy corren. El README va a listar cada regla nueva y cómo corregir un archivo viejo.
Nota: después de la revisión de las tandas 1 a 3 el README ya tiene la sección "Qué cambió y puede frenar un programa viejo". Queda pendiente el cambio de número de versión y mantenerla al día.
Nota al hacerla (tanda 8): Mate pasó a decir 0.3 (`--version`, la ayuda, la guía y el README). La sección "Qué cambió" aclara que junta todo lo que va de la 0.2 a la 0.3 y sumó los renglones de esta tanda. Cada mejora que frene un programa viejo tiene que seguir agregando su renglón ahí.
*Mirada: crítico · Esfuerzo: chico · Estado: hecha*

**90. Un tope para que Mate siga siendo chico**
Dejar escrito el presupuesto: pocas palabras nuevas, unas 12 funciones nuevas, y cada agregado con su renglón en el README y su prueba.
Nota al hacerla: el tope quedó en 40 palabras propias y 40 funciones incluidas, escrito arriba de todo en `mate.py` y en la sección "El tope" del README. Hoy hay 36 palabras y 39 funciones: queda lugar para una sola función más. Las pruebas frenan a quien se pase, y controlan que cada función y cada palabra tenga su renglón en el README, su `ayuda` y una prueba que la use (ese control encontró que `valores`, `mayusculas` y `minusculas` no tenían prueba; ya la tienen).
*Mirada: crítico · Esfuerzo: chico · Estado: hecha*

**91. Leer y escribir archivos de texto**
`leer_archivo` y `escribir_archivo`, solo desde el programa principal, solo dentro de la carpeta del programa y sin poder pisar archivos `.mate` ni `.py`.
Nota al hacerla: `escribir_archivo` reemplaza el archivo entero (no hay "agregar al final": se lee, se junta y se guarda). Además de `.mate` y `.py` tampoco pisa `.bat`, `.cmd` ni `.ps1`. Vale una subcarpeta que ya exista, pero nada de afuera de la carpeta del programa. Los errores son de una clase nueva para `detalle_de`: `"archivo"`. Ojo: `probar` corre el programa antes de las pruebas, así que lo que el programa escribe se escribe igual. No se pudo probar en una Windows de verdad.
*Mirada: lenguaje, crítico · Esfuerzo: mediano · Estado: hecha*

**92. `hoy()` y `ahora()`**
La fecha y la hora. En las pruebas devuelven una fecha fija, para que el resultado sea siempre el mismo.
Nota al hacerla: devuelven textos como se escriben acá, `"21/11/2026"` y `"21/11/2026 14:30"`. Con `probar` son siempre `"01/01/2025"` y `"01/01/2025 12:00"`. No hay cuentas con fechas (restar días, comparar): sería otra mejora. `hoy` y `ahora` dejan de servir como nombre de variable; está anotado en "Qué cambió".
*Mirada: lenguaje, crítico · Esfuerzo: chico · Estado: hecha*

**93. Un solo formato para todos los errores**
Los errores de agentes y los comunes se ven igual, con el archivo y el renglón adelante.
Nota (tanda 8): salteada. Con `correr` ya se ven igual (`archivo:renglón: error: ...`, también los de agentes). Lo que queda distinto es `probar`, que debajo de cada prueba escribe `línea 5: ...` para los comunes y `Roto al recibir Ping (línea 2): ...` para los de agentes. Unificarlo cambia renglones que varias pruebas existentes comparan letra por letra (es el mismo problema de la mejora 63). Hay que decidir primero si esa salida de `probar` se puede cambiar.
Nota al hacerla (tanda 9): se decidió que sí. `probar` escribe los errores de cada prueba igual que `correr`: `archivo:renglón: error: ...`, el renglón señalado debajo y, si lo hay, "cómo se llegó"; los de agentes dicen `archivo:2: error: Roto al recibir Ping: ...`. Una sola función arma ese texto para las dos órdenes. Por dentro (lo que devuelve el intérprete a las pruebas) también quedó uno solo: `línea 2: Roto al recibir Ping: ...` en vez de `Roto al recibir Ping (línea 2): ...`. Se actualizaron las pruebas que comparaban esos renglones. La consola sigue diciendo `línea N: error: ...`, porque ahí no hay archivo.
*Mirada: principiante · Esfuerzo: chico · Estado: hecha*

**94. `ayuda <palabra>`**
`mate ayuda si` o `mate ayuda largo` muestra una explicación corta con un ejemplo, tomada de la tabla única de funciones.
Nota al hacerla: las funciones salen de la tabla única; las palabras tienen su propia tabla, y cada ejemplo es un programa entero que las pruebas corren. `ayuda print` dice que en Mate es `mostrar`, y `ayuda mostar` sugiere la parecida. También anda adentro de la consola. `ayuda correr` (una orden) sigue mostrando la ayuda general.
*Mirada: principiante · Esfuerzo: mediano · Estado: hecha*

### Revisión final (después de la tanda 8)

Revisores independientes probaron las 94 mejoras hechas y encontraron fallas. Lo que se corrigió:

- **Mejora 50**: un texto común con dos puntos y salto de renglón (`"Descripción:\n- yerba"`) ya no se confunde con una ruta de Windows.
- **Mejoras 38 y 72**: una cuenta suelta (`i + 1`) se avisa antes de correr. El error de "renglón que no usa el valor" no se ataja con `intentar` ni cuenta en `asegurar falla`; adentro de `asegurar falla { ... }` una cuenta o una función suelta vale (es lo que se prueba), y un nombre mal escrito no cuenta como la falla esperada.
- **Mejora 67**: "cómo se llegó" termina siempre en el origen real, aunque haya muchas llamadas de por medio.
- **Mejoras 64 y 87**: `probar` con varios archivos y `--traza=archivo` guarda todas las conversaciones, una sección por archivo.
- **Mejoras 48 y 88**: una letra que no se puede leer de una entrada redirigida ya no da un error interno; en la consola un renglón que termina en operador sigue abajo, y sus errores no hablan de "el archivo".
- **Mejora 80**: `si x != crear V` con la llave del bloque en el renglón de abajo volvió a andar.
- **Mejoras 45 y 49**: la guía decía al revés lo de los textos adentro de las llaves.
- **Mejora 94**: `ayuda al fallar` existe; el README aclara que el ejemplo de una función es la forma de llamarla.
- **Mejora 85**: `usar "catalgo"` (sin `.mate`) también sugiere el parecido y avisa del `.mate.txt`; repetir un nombre que vino con `usar` dice de qué archivo viene.
- **Mejora 58**: el error de posición ya no dice "dio 2" cuando el 2 salió de una cuenta con decimales. (No se aceptan decimales como posición: esa idea está descartada.)
- **Mejora 74**: `crear ... llamado` exige un texto; `llamado Sur` sin comillas lo explica; una copia creada por un agente que después falla se deshace con su estado.
- **Mejora 91**: si `escribir_archivo` no puede guardar, el archivo queda como estaba.
- **Mejora 40**: un `sea` en un bloque de adentro de una función, prueba o `al recibir` no tapa una variable `var` del programa.
- **Mejora 75**: `de_json(texto, "lista de Pedido")` y los mensajes anidados se arman desde mapas sueltos.
- **Mejora 71**: `numero("")` es de la clase `"numero"`.
- **Mejoras 24 y 37**: el error del final del archivo señala el último renglón escrito.
- **Mejora 10**: un carácter invisible en el medio de una palabra se avisa como tal.
- **Mejora 21**: `21%`, `si no` separado, `al recibir Pedidos` y `precio = 5` sin declarar dan una pista útil.
- **Antes de correr**: un `al recibir` con un `fallar` condicional y sin `responder` cuenta como "nunca responde"; un tipo que no existe ya no arrastra un segundo error falso.
- **Tope de tamaño**: también vale para `unir`, `texto`, `a_json`, `agregar` y `"{...}"`.
- **Fechas**: comparar dos fechas con `<` es un error en vez de un resultado equivocado.

Lo que se dejó como está, y por qué:

- **Decimales de 10.000 millones para arriba**: no se recortan a 12 cifras para no comerse los centavos de un monto grande. El README ahora lo dice.
- **Un mapa con la clave `agente` (o `tipo` y `campos`)** vuelve de `de_json` como agente o mensaje: son las formas reservadas con las que viajan. El README ahora lo avisa.
- **`usar` trae también los `var`**: una función traída puede necesitarlos. Se corrigió la documentación.
- **El freno de 10.000.000 de pasos** tarda unos 20 segundos en saltar. Bajarlo cortaría programas largos de verdad; queda para discutir.
- **Varios errores juntos de la revisión previa**: se siguen mostrando cuando son independientes (tres mensajes sin declarar son tres errores de verdad). Solo se quitó el que salía en cascada.

### Lo que sigue

**95. Valores por defecto en los parámetros (para más adelante)**
`funcion con_iva(precio, tasa = 0.21)`. Postergada para no agrandar el lenguaje todavía.
Nota al hacerla (tanda 10): hecha. Los parámetros con valor van al final (si no, es un error al leer el programa, que muestra cómo quedaría). El valor se calcula en cada llamada, no una sola vez: puede ser una cuenta y usar los parámetros de antes (`funcion f(a, b = a * 2)`), y no hay sorpresas con listas compartidas. El error de cantidad dice el rango (`con_iva() espera entre 1 y 2 argumento(s) y recibió 3`) y para una función sin valores por defecto quedó letra por letra como estaba. La revisión previa (mejora 59) cuenta el mínimo y el máximo y mira los nombres del valor por defecto. Vale también en las funciones de un agente. No se agregó ninguna palabra.
*Mirada: lenguaje · Esfuerzo: chico · Estado: hecha*

**96. Textos de varios renglones (para más adelante)**
Textos con triple comilla. Van a hacer falta cuando los agentes lleven instrucciones largas.
Nota al hacerla (tanda 10): hecha con tres comillas rectas (`"""`), con las mismas llaves `{...}` y las mismas barras que un texto común. Se quita el renglón de las comillas que abren y el de las que cierran (si no tienen nada más) y la sangría que comparten los renglones escritos y el del cierre: así el texto se escribe prolijo dentro de un bloque, y poniendo el cierre más a la izquierda se conserva la sangría que se quiera. El primer renglón, si va pegado a las comillas, no se mide. Lo que va entre llaves se escribe entero en un renglón, y un nombre mal escrito ahí adentro se señala en su renglón, no en el de las comillas. Sin cierre, el error señala dónde se abrió; la consola sigue leyendo renglones hasta el cierre. Las comillas curvas de Word no abren un texto de varios renglones. Antes tres comillas seguidas eran siempre un error, así que ningún programa que corría cambia.
*Mirada: lenguaje · Esfuerzo: mediano · Estado: hecha*

**97. Contratos que validan valores (para más adelante)**
Rangos (`desde 1`), opciones fijas y valores por defecto en los campos de un mensaje.
Nota al hacerla (tanda 10): la sintaxis va después del tipo, en el mismo renglón y en un orden fijo: `cantidad: numero desde 1 hasta 100`, `prioridad: texto en ["baja", "media", "alta"]` y al final `= valor`. No se agregó ninguna palabra propia: `desde` y `hasta` solo significan algo ahí (siguen sirviendo de nombre) y `en` ya existía. Para las opciones se eligió `en [...]` y no `uno de [...]` porque `de` ya se usa en `lista de`. Los valores de las reglas van escritos a mano (no cuentas ni variables): así se revisan al leer el programa, y una regla que no cierra (`desde 5 hasta 1`, un valor por defecto que no cumple su regla, `desde` en un texto, rango y opciones juntos) es un error en la declaración. `desde`/`hasta` solo en `numero`; `en` solo en `numero` o `texto`. Un campo con valor por defecto puede faltar y toma ese valor también si le dan `nada` (por eso no lleva `?`). Se controla siempre que se arma el mensaje (al crearlo, al cambiarle un campo, con `de_json`) y antes de correr cuando el valor está escrito a mano; el texto es el mismo en los dos casos y dice campo, valor y regla. La clase del error para `detalle_de` es `"contrato"`. Quedó afuera a propósito: rangos de largo para textos y listas.
*Mirada: agentes · Esfuerzo: mediano · Estado: hecha*

**98. Historial de mensajes en las pruebas (para más adelante)**
Poder preguntar dentro de una prueba qué mensajes se mandaron.
Nota al hacerla (tanda 10): es una función incluida, `mensajes_enviados()`, y no una palabra nueva. Devuelve una lista de mapas en el orden de entrega: `numero`, `de`, `a`, `tipo`, `mensaje`, `pregunta`, `conversacion` y `respuesta_a`; con un tipo (`mensajes_enviados("Pedido")`) trae solo esos. `de` y `a` son los nombres como texto, igual que en la traza (el programa es `"(programa)"`): así se comparan con `==` y se muestran sin vueltas. Antes de contestar entrega lo que quedó en la cola, como `asegurar`. Cada prueba arranca con el historial vacío y numera desde 1. Solo existe en las pruebas: escrita en el programa o en un agente es un error antes de correr, y al correr también (una función suelta la puede usar si la llama una prueba). Se eligió un nombre largo para no chocar con variables de programas que ya existen (`historial`, `enviados`). Ojo: con esta, las funciones incluidas son 40 de 40; la próxima obliga a sacar una o a discutir el tope. Con `correr` no se guarda nada.
*Mirada: agentes · Esfuerzo: mediano · Estado: hecha*

**99. Un "sobre" para los mensajes y número de conversación (para más adelante)**
Guardar quién, a quién y en respuesta a qué. Es preparación para conectar programas entre sí; no se programa ahora.
Nota al hacerla (tanda 10): sin sintaxis nueva. Cada entrega lleva su sobre: número, quién, a quién, número de conversación y, si es la respuesta a un `enviar`, a qué mensaje contesta. Una conversación empieza cada vez que el programa (o una prueba) manda algo; lo que los agentes mandan mientras atienden, sus respuestas y los avisos de `al fallar` siguen en la misma, y un `enviar` a varios es una sola. Se ve en `--traza`, al final de los renglones sin sangría: `(conversación 2, en respuesta al 4)` (los de más adentro son de la conversación del renglón que los contiene, y no lo repiten), y en `mensajes_enviados()` (mejora 98). Cambia el formato de la traza: está en "Qué cambió", y hubo que actualizar las pruebas que la comparaban letra por letra. Sin `--traza` ningún programa muestra nada distinto. El programa no puede leer el sobre mientras corre (solo las pruebas): eso se decidirá cuando se conecten programas entre sí (mejora 100).
*Mirada: agentes · Esfuerzo: mediano · Estado: hecha*

**100. Conexión con modelos de IA y con la red**
Al principio quedó afuera: requería claves pagas que el dueño todavía no había decidido usar. El dueño pidió hacerla.
Nota al hacerla (tanda 11): una función incluida, `consultar_ia(instrucciones, pregunta)`, que le pregunta a Claude (de Anthropic) y devuelve el texto. No hay un "agente de IA" especial: un agente común la llama dentro de su `al recibir` y responde con su mensaje con contrato de siempre, así que todo lo demás (contratos, `preguntar`, traza, pruebas) sigue igual. Solo biblioteca estándar (`urllib`), y usa el proxy del sistema. La clave se lee de la variable de entorno `ANTHROPIC_API_KEY` y de ningún otro lado: no va en el programa ni en un archivo, y no aparece en errores ni en la traza. El modelo es `claude-opus-5-5` y se cambia con `MATE_MODELO`. Simulado: con `probar` nunca se sale a la red; la prueba fija la respuesta con `simular_ia("...")` (o una lista, una por consulta), y si no, vale el tercer valor opcional de `consultar_ia`, que es su respuesta preparada (la misma idea que el segundo valor de `leer`). Para correr sin clave está `--ia-simulada` (da las respuestas preparadas) y `--ia-simulada=respuestas.txt` (un renglón por respuesta: `lo que trae la pregunta => lo que contesta`). Llegar a la IA sin respuesta simulada es un error claro. Los errores (sin clave, clave inválida, sin crédito, límite de uso, tope de gasto, modelo que no existe, servicio saturado, sin red, certificado, espera de más de 3 minutos, respuesta cortada, respuesta frenada por un filtro) están en castellano, se atajan con `intentar` y su clase es `"ia"`. Si la IA está saturada o se corta la red se reintenta dos veces. Freno propio: 50 consultas de verdad por corrida (son pagas), que saca `--sin-limite`. Se pide además el respaldo de Anthropic para cuando un filtro frena al modelo (`fallbacks`), y si la cuenta no lo acepta se sigue sin él. **El tope de funciones pasó de 40 a 42**: el cupo estaba completo y estas dos no reemplazan a ninguna; si al equipo no le cierra, lo que hay que discutir es `simular_ia` (se podría reemplazar por el archivo de respuestas). Quedó afuera a propósito: conversaciones con memoria (cada consulta es suelta), que la IA devuelva un mensaje con contrato ya armado (hoy devuelve texto y el agente arma el mensaje; se puede pedir JSON en las instrucciones y usar `de_json`), que la IA use herramientas, y conectar programas de Mate entre máquinas. **Importante: no se probó contra el servicio real**, porque no había clave en el entorno donde se programó. Lo que se probó es el camino completo con respuestas armadas (pedido, encabezados, errores y reintentos, con `urllib` simulado y contra un servidor de mentira en la misma máquina). La forma del pedido y de la respuesta se tomó de la documentación vigente de Anthropic, pero la primera consulta de verdad la tiene que hacer el dueño con su clave.
*Mirada: principiante · Esfuerzo: grande · Estado: hecha*

## Lo que vino después de las 100

Con las 100 hechas, el dueño pidió un tercer objetivo para Mate: **que aprenda de sus
errores**. Que los agentes mejoren con el uso, y que quede anotado lo que sale mal. Estas
son las mejoras de esa etapa (versión 0.4). Siguen las reglas de siempre: un solo archivo,
sin dependencias, palabras y errores en castellano, y Mate chico.

Dos decisiones valen para las tres primeras (101 a 103):

- **Solo `correr` toca el disco.** Con `probar` no se lee ni se escribe memoria, bitácora ni
  lecciones: cada prueba arranca limpia. Y un programa que no usa nada de esto corre igual
  que en la 0.3 y no crea ningún archivo.
- **Los archivos son del dueño.** Quedan al lado del programa, se abren con el Bloc de notas,
  no salen nunca por la red y, si alguien los edita mal, Mate avisa en vez de romperse o de
  pisarlos.

**101. Memoria de agente (`estado recordado`)**
Que un agente no arranque de cero cada vez: marcar parte de su estado para que se guarde al terminar el programa y vuelva en la próxima corrida.
Nota de lo decidido: se escribe `estado recordado atendidos = 0`. `recordado` no es una palabra propia (las palabras siguen siendo 36 de 40): solo significa algo después de `estado` y antes de un nombre, así que `estado recordado = 5` y una variable llamada `recordado` siguen andando. Se guarda en `programa.memoria.json`, al lado del programa: un JSON con sangría, por agente, con una nota adentro que dice qué es. Cada agente declarado tiene lo suyo, y también cada copia con nombre (`crear ... llamado "Centro"`); una copia sin nombre no recuerda (su número depende del orden en que se crean) y Mate lo avisa una vez. Lo recordado le gana al valor que le da `crear`, que pasa a ser solo el de la primera vez. Se recuerdan datos (números, textos, lógicos, listas, mapas y mensajes); un agente o una función no, con aviso. Si el tipo guardado no coincide con el del programa, aviso y valor inicial; lo mismo si un mensaje guardado ya no cumple su contrato. Se guarda también si el programa termina con error o con Ctrl+C, y se escribe en un archivo provisorio que después reemplaza al bueno, así nunca queda a medio escribir. `--olvidar` (solo con `correr`) arranca de cero y deja las lecciones. Un archivo que no se entiende (JSON roto, forma rara) frena la corrida con un error que dice el renglón y cómo salir: se prefirió eso a seguir con valores iniciales y pisar al terminar lo que el dueño había editado. Quedó afuera a propósito: recordar variables del programa principal (para eso ya están `leer_archivo` y `escribir_archivo`), dos corridas a la vez del mismo programa (gana la que termina última) y un historial de valores anteriores.
*Mirada: agentes · Esfuerzo: mediano · Estado: hecha*

**102. Bitácora de errores**
Que las fallas de un agente queden anotadas solas, para poder mirar después qué viene saliendo mal.
Nota de lo decidido: solo la llevan los programas que tienen algún `estado recordado` o que usan lecciones (en el programa o anotadas con `corregir`); los demás no crean nada. Va a `programa.bitacora.txt`: texto común, un renglón por falla con `fecha | agente | qué pasó | qué mensaje atendía | motivo`, y arriba unos renglones con `#` que explican qué es. Se anota cuando un agente falla al atender un mensaje, cuando la IA no le contesta, cuando un mensaje o una respuesta no cumple el contrato y cuando el agente ataja un error con `intentar` (esas fallas antes no las veía nadie). El mismo error no se anota dos veces para el mismo agente; si pasa por dos agentes (uno falla, el otro lo ataja), queda un renglón por cada uno. Guarda las últimas 200. La clave de la IA no queda escrita: los errores ya venían sin ella, y además cada renglón pasa por el mismo filtro antes de guardarse. La orden `bitacora programa.mate` la resume: cuántas, por agente, qué pasó, los motivos más repetidos y las últimas cinco; los renglones que alguien editó a mano y no se entienden se cuentan aparte. Quedó afuera a propósito: anotar lo que falla en el programa principal fuera de los agentes (eso ya se ve en pantalla), niveles o filtros por fecha, y cualquier envío de la bitácora a otro lado.
*Mirada: agentes · Esfuerzo: mediano · Estado: hecha*

**103. Lecciones**
Que el dueño corrija a un agente y el agente no repita el error.
Nota de lo decidido: una lección es un texto corto con fecha, guardado en la memoria del agente. Se anota de dos maneras: desde la línea de comandos, sin tocar el programa (`corregir programa.mate Mostrador "..."`), o desde el propio agente con `aprender("...")`. `lecciones programa.mate` las lista numeradas y `--borrar=2` (o `--borrar=todas`) las saca. Dentro de un agente, `lecciones()` devuelve las suyas como lista de textos. `consultar_ia()` dentro de un agente con lecciones las agrega solas al final de las instrucciones, bajo el título "LECCIONES APRENDIDAS", numeradas; con `--traza` se ve un renglón por lección. Una copia con nombre usa las del agente del que es copia y además las suyas. Lo que consulta el programa principal va sin lecciones. Topes, porque viajan en cada consulta y cada consulta se paga: 20 por agente y 300 letras cada una; al pasarse de cantidad se olvida la más vieja con aviso, y una más larga no se anota (cortarla la dejaría sin sentido). La misma lección no se anota dos veces. Si el agente falla mientras atiende, lo que aprendió en ese mensaje se deshace, igual que su estado. En las pruebas ningún agente tiene lecciones: se fijan con `aprender("...", Mostrador)` y se leen con `lecciones(Mostrador)`, y `consultas_ia()` devuelve lo que se le consultó a la IA (agente, instrucciones completas, pregunta y respuesta). **El tope de funciones pasó de 42 a 45** (`aprender`, `lecciones` y `consultas_ia`): si hay que achicar, la candidata es `consultas_ia`, que solo sirve en las pruebas. `corregir`, `lecciones` y `bitacora` son órdenes de la línea de comandos, no del lenguaje. Quedó afuera a propósito: que la IA se escriba sus propias lecciones (se decidió que las anota el dueño o el programa, que son quienes saben qué estuvo mal), lecciones compartidas entre agentes distintos, y editar una lección (se borra y se anota de nuevo). Ojo: una lección es texto que se le suma a las instrucciones; la IA la tiene en cuenta, pero no es una garantía. Lo que tiene que cumplirse siempre va en el programa. Como la mejora 100, esto se probó con la IA simulada y con respuestas armadas, no contra el servicio real.
*Mirada: principiante · Esfuerzo: grande · Estado: hecha*

### Segunda parte: que el lenguaje aprenda de quien lo usa

Las tres de arriba hacen que aprendan los agentes. Estas cinco son para que mejore Mate: que
quede anotado en qué se traba la persona, para que después un equipo (de gente o de agentes)
pueda arreglar los mensajes que no alcanzan. Las tres últimas salieron del uso real del dueño
en PowerShell y el Bloc de notas. Decisiones que valen para todas:

- **Nada sale de la computadora.** El registro es un archivo local; Mate no lo manda. Para
  compartirlo, el dueño copia el texto que arma `informe --para-mejorar`.
- **Sin datos de la persona.** No se guarda el programa ni el renglón del error, y el mensaje
  pasa por un filtro que tapa textos, nombres, archivos, rutas y claves.
- **No cambia ningún resultado.** No muestra nada nuevo en pantalla, no toca la carpeta del
  programa, y si no puede escribir sigue como si nada.

**104. Registro de errores de uso**
Que cada error que Mate le muestra a la persona deje un renglón anotado, para saber cuáles son los más comunes y cuáles mensajes no ayudaron.
Nota de lo decidido: va a `errores_de_uso.txt`, al lado de `mate.py` (no al lado del programa: es de Mate, no de un programa), en texto común con unos renglones `#` arriba que explican qué es y cómo apagarlo. Cada renglón: `fecha | versión | orden | qué error fue | con o sin sugerencia | cuántas veces seguidas | mensaje tapado`. Se anota **un renglón por corrida que falla**: el primer error que vio la persona, y cuántos más hubo; así "se repitió seguido" es fácil de ver y el archivo no se llena con una sola corrida. La categoría ("qué error fue") es la etapa (al escribir la orden, al leer el programa, antes de correr, al correr, en la consola, por dentro de Mate) más el arranque del mensaje ya tapado y sin números; los errores de la línea de comandos más comunes tienen un nombre fijo (orden que no existe, opción que no existe, falta el archivo, no está el archivo, comando pegado dos veces). Se prefirió eso a ponerle un código a cada uno de los cientos de mensajes: no agrega nada que mantener, y si un mensaje se reescribe, la versión anotada en el renglón dice de cuál se habla. El filtro tapa: la clave de la IA y lo que tenga forma de clave, direcciones y correos, el nombre de usuario, lo que la persona escribió en la orden (`<dato>`), los textos entre comillas (`"<texto>"`), los nombres entre comillas simples que no sean palabras de Mate (`'<nombre>'`), archivos, rutas (hasta el final de la frase, porque una carpeta puede tener espacios), opciones que no existen y números de tres cifras o más. Lo que el programa dice con `fallar` o `asegurar` es texto de la persona: no se guarda, solo queda "el programa cortó con 'fallar'". Si el mismo error (misma categoría, misma orden) vuelve a salir dentro de los 30 minutos, el renglón dice "2 veces seguidas", "3 veces seguidas"...: es la señal de que el mensaje no alcanzó. Guarda los últimos 500. Solo anota cuando Mate se corre desde la línea de comandos: usado como módulo (`mate.main([...])`) no anota, dentro de una corrida de pytest tampoco, y **con la orden `probar` nunca** (es la regla de la 0.4: `probar` no toca nada en el disco). En la consola anota cada error que muestra. Se apaga con la variable `MATE_SIN_REGISTRO=1` o con `--sin-registro`. Un renglón editado a mano que no se entiende no rompe nada: se saltea, se cuenta aparte y no se pisa. Quedó afuera a propósito: mandar el registro a algún lado, anotar las corridas que salen bien (no se sabe entonces si entre dos fallas iguales hubo una buena), anotar todos los errores de una corrida, y avisar en pantalla cada vez que se anota (cambiaría lo que muestra un programa que falla; está dicho en `ayuda` y en el README). Ojo: los nombres que un mensaje trae sin comillas (el de un mensaje, el de un campo) pueden quedar; el README lo dice y pide leer antes de compartir.
*Mirada: equipo que mantiene Mate · Esfuerzo: mediano · Estado: hecha*

**105. La orden `informe`**
Que el registro se pueda leer sin abrir el archivo, y que sirva para pedir mejoras.
Nota de lo decidido: `informe` muestra desde cuándo hay datos y de qué versiones, los diez errores más frecuentes con su último mensaje, los que se repitieron seguido (hasta cuántas veces, y cuántas repeticiones en total), cuántos traían sugerencia y los más frecuentes que no traían ninguna, y con qué orden pasaron. `informe --para-mejorar` arma un texto para copiar y pegarle a un asistente o a un equipo de agentes: qué es Mate, el mismo resumen, y tres preguntas concretas (qué cambiar para que se resuelva al primer intento, con el mensaje nuevo escrito; cuál arreglar primero; cuáles son en realidad problemas de la documentación), más las reglas que no se negocian (chico, un archivo, mismo resultado, cada cambio con su prueba). `informe --borrar` borra el registro. "Sugerencia" quiere decir que el mensaje traía un "¿quisiste decir...?" o el comando bien escrito; no cuenta los consejos que muchos mensajes ya traen en su texto. `--borrar` sola es nueva (antes siempre llevaba `=número`, para las lecciones) y fuera de `informe` sigue siendo un error. Son tres renglones más en la tabla de órdenes y dos opciones (`--para-mejorar`, `--sin-registro`); no se agregó ninguna palabra ni función al lenguaje. Quedó afuera a propósito: filtros por fecha o por orden, exportar a otro formato, y que Mate le mande el pedido a la IA por su cuenta (lo copia el dueño, que así ve lo que comparte).
*Mirada: equipo que mantiene Mate · Esfuerzo: mediano · Estado: hecha*

**106. El comando pegado dos veces**
En PowerShell se pega el comando dos veces en el mismo renglón (`correr mio.matepython mate\mate.py correr mio.mate`, `--trazapython ...`) y Mate contestaba que `correr` lleva un solo archivo, o que no conoce la opción `--trazapython`.
Nota de lo decidido: antes de mirar las opciones, Mate se fija si lo que recibió es el mismo comando repetido (dos o más veces) y pegado sin espacio; si es así dice "parece que el comando se pegó dos veces en el mismo renglón. Escribilo una sola vez:" y abajo el comando entero, con `python mate\mate.py` adelante tal como se escribió y los nombres con espacios entre comillas. Si lo pegado son dos comandos distintos (uno termina en `python` y sigue `mate.py`), muestra el último. En la consola de Mate, un renglón que es el mismo texto dos o tres veces seguidas (`sea x = 1sea x = 1`, `ayuda agenteayuda agente`) da el mismo aviso con el renglón una sola vez, y no corre. Eso último cambia algo: `mostrar(1)mostrar(1)` antes corría dos veces en la consola; se aceptó porque nadie lo escribe así a propósito y está en "Qué cambió". De paso, un comando de PowerShell escrito adentro de la consola de Mate dice que eso va en PowerShell. Solo se mira el caso exacto (el mismo texto repetido): no se intenta adivinar otros pegados.
*Mirada: principiante · Esfuerzo: chico · Estado: hecha*

**107. Tres comillas de más**
Al pegar un bloque dentro de otro queda una cantidad impar de `"""` y el error solo decía que al texto le falta el cierre, señalando el final del archivo.
Nota de lo decidido: cuando un texto de tres comillas queda sin cerrar y en el archivo hay una cantidad impar de juegos de tres comillas (tres o más), el mismo error sigue con: cuántos hay, en qué renglones, que van de a pares y por eso sobra o falta uno, cuál queda sin pareja leyendo de arriba para abajo, y que el culpable puede estar más arriba. Con uno solo (falta el cierre y nada más) el mensaje es el de siempre. La cuenta es simple, sobre el texto del archivo: cuenta también las `"""` que estén en un comentario. Quedó afuera a propósito: adivinar cuál es el juego que sobra (no se puede saber) y el caso de cantidad par mal apareada, que da otro error.
*Mirada: principiante · Esfuerzo: chico · Estado: hecha*

**108. La pantalla de PowerShell adentro del archivo**
Un archivo `.mate` cuyo primer renglón es `python mate\mate.py correr ...` o `PS C:\Users\...>`: se pegó el comando, o la pantalla entera, adentro del programa, y el error era "carácter inesperado".
Nota de lo decidido: antes de leer el programa, Mate mira el primer renglón escrito. Si empieza como la pantalla de PowerShell (`PS C:\...>`) o es un comando (`python ... mate.py`, `py ... mate.py`, `mate correr ...`, `notepad ...`, `cd carpeta`), el error dice que ese renglón no es de Mate, que se pegó adentro del archivo, y qué hacer en el Bloc de notas. Vale también para los archivos traídos con `usar`. Solo se mira el primer renglón escrito: más abajo podría ser un texto de varios renglones que habla de PowerShell a propósito.
*Mirada: principiante · Esfuerzo: chico · Estado: hecha*

### Tercera parte: que deje de ser "lento y chico" (versión 0.5)

Al comparar Mate con Python o JavaScript, lo primero que se le anotó en contra fue que es
lento y chico: no sirve para programas grandes, y lo que no trae no se le puede sumar. Estas
dos mejoras van contra eso sin agrandar el lenguaje: no se agregó ninguna palabra ni ninguna
función incluida (con estas dos seguían siendo 36 de 40 y 45 de 45; las tres funciones
nuevas de la 0.5 llegaron después, con la cuarta parte).

**109. Un intérprete más rápido**
Que los programas corran bastante más rápido sin que cambie nada de lo que hacen.
Nota de lo decidido: primero se escribió el medidor (`mate/pruebas/velocidad.py`: cinco programas típicos, y de cada uno la corrida más rápida) y se midió la 0.4 antes de tocar nada: bucle con cuentas 1,763 s; llamadas a funciones 0,508 s; listas y mapas 0,499 s; textos 1,003 s; mensajes entre agentes 0,252 s (Python 3.13). Con cProfile se vio que el tiempo no se iba en las cuentas sino en el propio intérprete: por cada valor y cada renglón recorría una cadena de "si es esto, si es aquello" (una cuenta estaba en el lugar 15 de esa cadena) y hacía dos o tres llamadas de Python de más. El cambio: cada sentencia y cada expresión se "arma" una sola vez, la primera vez que se usa, y queda convertida en una función de Python que ya sabe qué hacer (el árbol del programa pasa a funciones encadenadas; el cuerpo de una función de Mate se arma en su primera llamada). Además: las cuentas de todos los días (enteros que no son gigantes, decimales, comparaciones) se resuelven sin pasar por todos los controles, y dan exactamente lo mismo; un `devolver`, un `romper` o un `continuar` ya no cuestan una excepción de Python; un bloque que no declara nada (`sea`, `var` o una función) no crea su propio entorno; los parámetros y la variable de un `para` se anotan sin controles repetidos; y cada función incluida pasa por un envoltorio en vez de dos. Medido al final, las dos versiones en la misma computadora y en el mismo momento (Python 3.13, la más rápida de 7 corridas, 0.4 → 0.5): bucle con cuentas 1,687 → 0,310 s (5,43 veces); llamadas a funciones 0,405 → 0,140 s (2,90 veces); listas y mapas 0,394 → 0,189 s (2,09 veces); textos 1,152 → 0,879 s (1,31 veces); mensajes entre agentes 0,262 → 0,180 s (1,46 veces); en total 3,901 → 1,698 s (2,30 veces). Con Python 3.11, la más rápida de 5: 6,92; 3,24; 2,30; 1,64 y 1,54 veces. **La meta era el doble en bucles y llamadas, y se cumplió; en textos y en mensajes entre agentes no se llegó al doble.** En textos casi todo el tiempo es `lista = agregar(lista, x)` con una lista de 20.000 elementos, que copia la lista entera en cada vuelta: es el precio de que una copia nunca cambie el original, y no se tocó. En los mensajes, el tiempo está en lo que Mate controla por cada mensaje (el contrato, la foto del estado por si el agente falla, que la respuesta no lleve funciones), que tampoco se tocó. Cómo se comprobó que nada cambió: pasan las pruebas que ya había, y además se corrieron 175 comparaciones de la 0.4 contra la 0.5 (todos los ejemplos con `correr`, `correr --traza`, `probar` y `verificar`, y unos cuarenta programas armados para molestar: errores en expresiones de varios renglones, el freno de pasos, recursión sin fin, `romper` y `devolver` fuera de lugar, números gigantes) mirando salida, errores y código de salida: ninguna diferencia. La cuenta de pasos es la misma (hay una prueba que fija 788 pasos para un programa, el número que daba la 0.4). Dos pruebas viejas se cambiaron porque rompían a propósito una función interna que ya no existe (`_ejecutar`); ahora rompen otra. Lo único que se movió: con un Python anterior al 3.12 hay lugar para unas 180 llamadas una adentro de la otra en vez de unas 120, porque cada llamada de Mate gasta menos niveles de Python. Quedó afuera a propósito: resolver de antemano dónde está cada variable (habría que rehacer cómo se revisan los nombres, y un error ahí cambia resultados), que `agregar` no copie (rompería "modificar una copia no toca el original") y traducir el programa a código de Python (dejaría de ser un intérprete que se entiende leyéndolo).
*Mirada: quien corre programas largos · Esfuerzo: grande · Estado: hecha*

**110. Puente a Python (`usar python`)**
Que lo que Mate no trae se pueda sumar desde afuera, con funciones escritas en un archivo de Python que está al lado del programa, sin tocar el intérprete.
Nota de lo decidido: se escribe `usar python "ayudas.py"` y después `ayudas.raiz(144)`: el nombre del archivo, un punto y la función. Se eligió esa forma (y no traer las funciones sueltas, como hace `usar` con un `.mate`) porque así se ve de dónde viene cada una, no chocan con los nombres del programa, y `verificar` no necesita ejecutar el Python para saber que el nombre existe. `python` no es una palabra propia: solo significa algo después de `usar` (las palabras siguen siendo 36). El archivo tiene que estar en la carpeta del programa o en una de adentro (ni `..`, ni rutas completas, ni un acceso directo que lleve afuera), y llamarse como una variable de Mate, porque ese nombre es el que se escribe después. Se ven las funciones escritas ahí con `def` que no empiezan con guion bajo; lo que el archivo importa no se ve. Solo cruzan números, textos, verdadero/falso, nada, listas y mapas, y van y vuelven copiados, para que el Python no pueda cambiarle una lista al programa por atrás; un mensaje hay que pasarlo con `a_mapa`, y si vuelve otra cosa (un conjunto, una fecha de Python, un diccionario con claves que no son textos, infinito) el error dice qué volvió y cómo convertirlo. Un error dentro del Python llega como un error de Mate con el renglón del `.mate`, dice el renglón del `.py`, una explicación en castellano de los doce errores más comunes y lo que dijo Python tal cual (eso viene en inglés y no se puede traducir todo); se ataja con `intentar` y su clase es `"python"`. También si el archivo falla apenas se lo abre, o si quiere cerrar el programa con `exit`. Una función de Python puede ir sola en un renglón (puede estar guardando algo). Antes de correr, Mate avisa si el archivo no está (con el nombre parecido, o el `.py.txt` del Bloc de notas), si Python no lo puede leer, y si el programa pide una función que el archivo no tiene; para eso lee el `.py` sin ejecutarlo. Mate no deja nada al lado del programa: no se arma la carpeta `__pycache__`. En la consola, repetir el `usar python` trae el archivo de nuevo, para probar una corrección. Lo que dice el Python no se guarda en el registro de errores de uso (es texto de la persona, como el de `fallar`). **El riesgo, dicho en todos lados** (README, `ayuda python`, `ayuda`, `guia`, el ejemplo y su `.py`): ese Python corre con todos los permisos de la computadora, también con `probar`, así que solo hay que usar archivos propios o de confianza. Ejemplo: `ejemplos/09_con_python.mate` con `ayudas.py`. Quedó afuera a propósito: pasar agentes, mensajes o funciones de Mate al Python (y que el Python llame a Mate); que el `.py` importe a otro `.py` de la misma carpeta (no se toca por dónde busca Python); instalar paquetes desde Mate; un freno para el Python (no hay forma segura de cortarlo desde adentro: se corta con Ctrl+C); y deshacer entre prueba y prueba lo que el `.py` guarde en sus variables.
*Mirada: quien necesita algo que Mate no trae · Esfuerzo: mediano · Estado: hecha*

### Cuarta parte: datos de verdad y charla por teclado (versión 0.5)

Lo otro que se le anotó en contra a Mate es que lo que hace "se puede hacer en Python con más
trabajo": la ventaja tiene que ser la facilidad. Estas tres mejoras apuntan a eso: que el
dueño de un negocio pueda poner su propia lista de precios al lado del programa y charlar con
su agente, sin aprender nada de archivos ni de codificaciones.

**111. Leer una planilla: `leer_tabla`**
Que un programa pueda usar la lista de precios que el dueño ya tiene en Excel, guardada como CSV, sin que tenga que saber de separadores, codificaciones ni de cómo se escriben los números.
Nota de lo decidido: `leer_tabla("precios.csv")` devuelve una lista con un mapa por fila; las claves son los títulos de la primera fila, tal cual están escritos (no se pasan a minúscula ni se les sacan las tildes: lo que se ve en la planilla es lo que se escribe en el programa, y si no coincide el error de "no tiene un campo" ya sugiere el parecido). El separador se decide mirando la fila de títulos: punto y coma, coma o tabulación, el que más aparezca fuera de las comillas; en el empate gana el punto y coma, que es lo que usa Excel en la Argentina. Se respeta el renglón `sep=;` que a veces pone Excel. La codificación la resuelve lo mismo que ya leía los `.mate` (UTF-8 con o sin marca, ANSI de Windows, "Unicode"). Una celda escrita como número llega como número, también a la argentina (`3.500,50`, `$ 3.500`, `3,5`). Una decisión discutible: **en una planilla `3.500` es tres mil quinientos**, aunque `numero("3.500")` siga dando 3,5 (ahí manda cómo se escribe un número en Mate; en una planilla argentina el punto es de los miles). Los códigos que empiezan con cero (`00123`) quedan como texto, para no perderles los ceros. Una celda vacía es `""` y no `nada`, para que mostrarla no escriba "nada". Los renglones en blanco y los `;;;` que deja Excel se saltean. Errores: archivo que no está (dice en qué carpeta lo buscó y sugiere el parecido), fila con columnas de más o de menos (dice el renglón del archivo, cuántas tiene, cuáles son los títulos y qué dice el renglón), archivo vacío, columna sin título, dos columnas con el mismo título, y un `.xlsx` sin convertir (explica el "Guardar como"). Una planilla con solo los títulos da una lista vacía. Como `leer_archivo`, solo desde el programa principal y en la carpeta del programa. Quedó afuera: leer el `.xlsx` directamente (habría que traer una biblioteca, y Mate es un solo archivo sin instalar nada), elegir la hoja, y escribir tablas.
*Mirada: quien tiene sus datos en Excel · Esfuerzo: mediano · Estado: hecha*

**112. Anotar en un archivo: `agregar_a_archivo`**
Que un programa pueda ir anotando pedidos o consultas, un renglón por vez, sin tener que leer el archivo entero y guardarlo de nuevo.
Nota de lo decidido: `agregar_a_archivo("pedidos.txt", texto)` suma el texto como un renglón al final (le pone el salto si no lo trae) y crea el archivo si no existe, con la marca para que el Bloc de notas muestre bien las tildes. Mismos cuidados que `escribir_archivo` (carpeta del programa, programa principal, no pisa programas). Si el archivo existente está en ANSI o en "Unicode", se guarda entero de nuevo en UTF-8 en vez de mezclar codificaciones. **Con `probar` no toca el disco**: lo agregado queda en la memoria de esa prueba, `leer_archivo()` y `leer_tabla()` lo ven (el archivo como está en el disco más lo agregado), y se descarta al terminar la prueba. `escribir_archivo` se dejó como estaba (con `probar`, lo que escribe el programa principal se escribe), para no cambiarle el comportamiento a los programas que ya existen.
*Mirada: quien quiere que quede anotado · Esfuerzo: chico · Estado: hecha*

**113. Charla por teclado que se puede probar y cortar: `simular_teclado` y Ctrl+C**
Que se pueda charlar con un agente desde el teclado, probar esa charla sin teclear, y cortarla sin que aparezca un error.
Nota de lo decidido: no se inventó nada para preguntar: `leer("Cliente:", "chau")` ya existía, y una charla es un `mientras` con un `leer` adentro que sale con una palabra (la respuesta preparada es esa palabra, así sin teclado termina sola). Lo que faltaba eran tres cosas. Una: `simular_teclado(["hola", "chau"])`, solo dentro de una prueba, fija lo que se "teclea", un texto por cada `leer()` en orden; cuando se acaban, `leer()` da su respuesta preparada, y si no tiene, el error dice cuántos `leer()` hubo y cuántos textos había. Dos: Ctrl+C mientras `leer()` espera ya no es un error con número de línea y código 130: el programa termina ahí con un aviso corto y código 0, y la memoria de los agentes se guarda igual (Ctrl+C en cualquier otro momento sigue como antes). Tres: `leer()` sin teclado disponible (entrada cerrada) usa la respuesta preparada en todos los casos, en vez de poder fallar por dentro. Las tildes y la ñ ya andaban en la ventana de PowerShell (Python lee la consola de Windows en Unicode); lo que no se puede arreglar desde Mate es PowerShell 5.1 cuando se le pasa texto con `|`, y está dicho en el README. **El tope de funciones pasó de 45 a 48** (`leer_tabla`, `agregar_a_archivo`, `simular_teclado`); las tres se pueden tapar con un nombre propio, para que un programa de antes que las usara como nombre siga corriendo. El ejemplo que junta todo es `ejemplos/10_mostrador_mayorista.mate`, con su `precios.csv`. Quedó afuera: una palabra propia para la charla (`charlar con Mostrador`) y que el agente lea el teclado él mismo; se prefirió no agrandar el lenguaje y que siga valiendo que un agente nunca frena a los demás.
*Mirada: quien atiende un mostrador · Esfuerzo: mediano · Estado: hecha*

### Quinta parte: que se le pueda confiar la atención a un agente con IA (versión 0.5)

Lo tercero que se le anotó en contra a Mate: "lo que hace Mate se puede hacer en Python con
más trabajo". Es cierto para casi todo, y por eso estas tres mejoras apuntan a lo que en
Python **no** viene hecho y a un dueño de negocio le importa más que nada: poder confiar en
lo que su agente le dice a un cliente, saber cuánto gasta, y corregirlo sin programar. No se
agregó ninguna palabra ni ninguna función incluida (siguen siendo 36 de 40 y 48 de 48).

**114. Frenos para la IA**
Que el dueño declare, dentro del agente y en castellano, qué no puede decir la IA, y que sea Mate (no la IA) el que lo compruebe sobre cada respuesta antes de devolverla.
Nota de lo decidido: dentro del agente va un bloque `frenos { ... }` con una regla por renglón: `precios` (los importes permitidos), `prohibido` (una lista de textos), `largo` (letras), `reserva` (el texto que se devuelve en lugar de una respuesta mala) y los dos topes de la mejora 115. `frenos` **no es una palabra reservada**: solo significa esto dentro de un agente y seguida de una llave (como `recordado` después de `estado`), así que un programa que la usaba de nombre sigue igual. El valor de cada regla es una expresión que ve el estado y las funciones del agente y se calcula en cada consulta, para que `precios: solo_precios(filas)` siga a la lista si cambia. Cuando una respuesta rompe una regla, Mate consulta **una** vez más con la misma pregunta y un aviso que dice qué regla rompió; si la vuelve a romper (o ese segundo intento falla), `consultar_ia()` devuelve la `reserva`. Por eso `reserva` es obligatoria si hay una regla que mira la respuesta (se avisa antes de correr). Cada freno que salta se ve en `--traza`, queda en la bitácora (qué regla, qué pregunta y qué había contestado la IA) y, en una prueba, en dos campos nuevos de `consultas_ia()`: `freno` y `devuelto` (solo aparecen si el agente tiene frenos, para no cambiarle nada a las pruebas que ya existen). **El freno de precios, que es el delicado:** cuenta como importe un número con `$` adelante o atrás, con la palabra "pesos", con "mil" o "millones" en el medio, o suelto justo después de "sale", "cuesta", "vale", "precio" o "cobramos" si es de 100 o más. `3.500` es siempre tres mil quinientos (el punto es de los miles); `3,500` se acepta si 3,5 o 3500 está permitido. Las cantidades, los teléfonos, las fechas, los porcentajes y los números sueltos en otra frase no se miran: **ante la duda se prefirió frenar de menos**, porque un freno que tapa respuestas buenas se termina apagando. Queda dicho en el README lo que se le escapa: importes escritos con letras, "te lo dejo en 4000", y promesas dichas con otras palabras. `precios` acepta también la tabla entera (valen todos sus números, incluido el stock): es más cómodo y más flojo, y el ejemplo muestra la forma estricta, con la columna de precios sola. `prohibido` no distingue mayúsculas ni tildes y busca desde el comienzo de una palabra ("descuento" frena "descuentos"). Errores cuidados: regla que no existe (con el nombre parecido), regla repetida, bloque vacío o repetido, valor de otro tipo (antes de correr si está escrito, al consultar si se calcula), y `consultar_ia()` adentro de los propios frenos. Ejemplo: `ejemplos/11_mostrador_con_frenos.mate`. Quedó afuera a propósito: frenos para consultas hechas desde el programa principal o al calcular el estado inicial (ahí no hay un agente atendiendo), una regla de "solo hablá de estos temas" (habría que pedirle a otra IA que juzgue, y eso es justo lo que no se quería), y reintentar más de una vez (cada intento se paga).
*Mirada: el dueño que pone un agente a atender · Esfuerzo: grande · Estado: hecha*

**115. Tope de gasto por día y la cuenta de consultas**
Que un agente no pueda consultar a la IA más de lo que el dueño decidió para un día, y que el dueño pueda ver cuánto consultó cada uno.
Nota de lo decidido: son dos reglas más de `frenos`: `consultas_por_dia` y `tokens_por_dia`. Al llegar al tope, `consultar_ia()` no consulta: devuelve la `reserva` o, si no hay, falla con un error que se ataja (clase `"tope"` en `detalle_de`). La cuenta es por día y por agente declarado (sus copias cuentan con él, para que el tope no se esquive creando copias) y se guarda **con la memoria del programa**, en `programa.memoria.json`, los últimos 30 días. Se graba después de cada consulta de verdad, no solo al terminar, por si alguien cierra la ventana con la X. Los tokens son los que informa el servicio en cada respuesta (los de la pregunta más los de la respuesta); como Mate se entera al terminar la consulta, ese tope se puede pasar por lo que gaste la última, y está dicho. **No se calcula plata**: el precio depende del modelo y cambia, y un número inventado sería peor que ninguno. Con `--ia-simulada` también cuenta, pero en una cuenta aparte ("simuladas") y contra el mismo tope: así se puede ver el tope funcionando sin gastar y sin que las pruebas del dueño le coman las consultas de verdad; ahí no hay tokens. Con `probar` nada de esto toca el disco y cada prueba arranca con la cuenta en cero. El segundo intento de un freno es otra consulta y cuenta. La orden `bitacora` ahora muestra al final cuánto consultó cada agente hoy, día por día en la última semana y en total (se prefirió sumarlo ahí antes que inventar otra orden). El tope de siempre (50 consultas de verdad por corrida) no se tocó: es para los bucles. Un programa sin frenos no lleva ninguna cuenta ni crea archivos, así que para llevar la cuenta sin controles alcanza con un `frenos` que solo tenga un tope alto. Quedó afuera: un tope por mes, un tope común a varios programas, y avisar por mail o por pantalla cuando falta poco.
*Mirada: el dueño que paga la cuenta · Esfuerzo: mediano · Estado: hecha*

**116. Lecciones propuestas: Mate las redacta y el dueño las aprueba**
Que el dueño no tenga que escribir cada lección a mano, sin que por eso un agente empiece a usar lecciones que nadie miró.
Nota de lo decidido: una lección propuesta queda guardada con la memoria del agente, aparte de sus lecciones, y **no se usa en ninguna consulta hasta que el dueño la aprueba**. Aparecen de dos maneras. Una: cuando salta un freno, queda sola una propuesta con una redacción fija por regla ("No nombres ningún importe que no esté en los precios que te dieron...") y el motivo (la regla y lo que había contestado la IA); se avisa una vez por corrida. Dos: la orden `proponer programa.mate Agente "qué estuvo mal"` (y, si se quiere, lo que había contestado el agente): si la clave está puesta, la redacta la IA, se dice que fue una consulta paga y entra en la cuenta del día; sin clave, con `--ia-simulada` sola, o si la IA falla o se pasa de las 300 letras, va una redacción fija, y siempre se dice cuál fue. La orden `propuestas programa.mate` las muestra numeradas, con su motivo; `propuestas programa.mate aprobar 2` la pasa a las lecciones (con los topes de siempre: 20 por agente, 300 letras, sin repetir) y `descartar 2` la saca; valen varios números y `todas`. Las propuestas tienen su propio tope (20 por agente, se va la más vieja) y la misma no se propone dos veces, ni si ya es una lección aprobada. Con `probar` no se propone nada. Dos órdenes nuevas, `propuestas` y `proponer`, y ninguna palabra ni función. Quedó afuera: que Mate apruebe solo (es justo lo que no tiene que pasar), editar la propuesta antes de aprobarla (se descarta y se escribe con `corregir`), y proponer lecciones a partir de las fallas comunes de la bitácora.
*Mirada: el dueño que corrige a su agente · Esfuerzo: mediano · Estado: hecha*

### Sexta parte: que otra persona pueda instalarlo y aprenderlo sola (versión 0.5)

Lo último que se le anotó en contra a Mate: "lo usa una sola persona; no hay comunidad,
cursos ni gente que lo conozca". Una comunidad no se programa, pero sí lo que hace falta para
que alguien más pueda empezar sin el dueño al lado: un curso, un instalador y una página para
pasarle. No se agregó ninguna palabra ni ninguna función incluida (siguen siendo 36 de 40 y
48 de 48); hay una orden nueva de la línea de comandos, `curso`.

**117. El curso: doce clases y la orden `curso`**
Que alguien que nunca programó pueda ir de "hola" a un mostrador con IA, lista de precios, frenos y lecciones, solo, con el Bloc de notas y PowerShell.
Nota de lo decidido: la carpeta `mate/curso` tiene doce clases. Cada clase son tres archivos: el texto (`clase_01_hola.md`, escrito para leerse bien en el Bloc de notas: renglones cortos y el código con sangría, sin cercos), el programa (`clase_01_hola.mate`) y el ejercicio resuelto (`clase_01_solucion.mate`). Todas tienen las mismas partes: qué vas a lograr, el programa, cómo se corre, lo que tiene que salir, el error más común y cómo se arregla, ejercicio y solución. Lo que cada texto dice que "tiene que salir" y los errores que muestra no se escribieron a mano: se sacaron corriendo Mate, y las pruebas del intérprete comprueban que el programa y la solución que figuran en el texto son los del archivo, que todos pasan `verificar` y `probar`, y que lo que muestran al correr es lo que dice el texto. Desde la clase 9 la IA se ensaya con `--ia-simulada`: ninguna clase necesita clave ni internet. La orden `curso` lista las clases y dice cómo leer, abrir y correr la primera; `curso 3` muestra la clase 3 en la pantalla. Solo lee los archivos del curso: no corre ni escribe nada. Para los ejercicios se propone un archivo `practica.mate` al lado de los del curso (así encuentra `precios.csv`), que no se sube al proyecto. Quedó afuera: clases sobre `usar python`, `crear` y `al fallar` (están en el README y en los ejemplos), y un modo que corrija los ejercicios solo.
*Mirada: quien llega sin el dueño al lado · Esfuerzo: grande · Estado: hecha*

**118. Instalador para Windows: `instalar.bat`**
Que la orden `mate` ande desde cualquier carpeta, sin permisos de administrador, y que quede claro qué se hizo y cómo se deshace.
Nota de lo decidido: es un `.bat` y no un script de PowerShell, porque en muchas computadoras la ejecución de scripts de PowerShell está bloqueada. **No toca el PATH ni el registro**: cambiar el PATH desde un script es la manera más común de romperle algo a alguien, y este instalador no se pudo probar en una Windows de verdad. En cambio escribe un solo archivo, un lanzador `mate.cmd` de cinco renglones, en `%LOCALAPPDATA%\Microsoft\WindowsApps`, que en Windows 10 y 11 ya está en el PATH de cada usuario y se puede escribir sin permisos. El lanzador llama al `mate.bat` de siempre (Mate no se copia: sigue en su carpeta) y avisa con la variable `MATE_ORDEN` que la orden es `mate`, para que los comandos que Mate sugiere salgan escritos así. Antes de escribir comprueba que estén `mate.py` y `mate.bat` (si no, casi seguro se abrió desde adentro del `.zip`, y lo dice), que haya un Python 3.10 o más nuevo **corriéndolo** (el `python` que trae Windows puede ser un atajo a la tienda), y que no haya un `mate.cmd` ajeno. Después de escribir lo prueba dos veces, por su nombre completo y como `mate` desde otra carpeta, y si alguna falla borra el lanzador y explica por qué. `instalar.bat quitar` lo saca. Está escrito sin tildes, sin bloques entre paréntesis (para carpetas como `mate (1)`) y con todas las rutas entre comillas. De paso, `mate.bat` ahora también prueba a Python corriéndolo, y no espera una tecla cuando lo llama el lanzador. **Sin probar en Windows real**: se revisó renglón por renglón y las pruebas del intérprete controlan su forma (solo ASCII, fin de renglón de Windows, cada salto a una etiqueta que existe, que no use `setx` ni `reg` y que solo escriba el lanzador). Quedó afuera: agregar la carpeta al PATH cuando `WindowsApps` no está (se avisa y se deja la orden larga), un instalador para Linux o Mac, y asociar los `.mate` al doble clic.
*Mirada: quien instala sin ayuda · Esfuerzo: mediano · Estado: hecha*

**119. Una página para compartir y un README que se entiende de entrada**
Que haya algo para pasarle a otra persona por el celular, y que quien abre el README sepa en el primer pantallazo qué es Mate, cómo se instala y por dónde empezar.
Nota de lo decidido: `docs/index.html` es un solo archivo, sin nada de afuera (ni letras, ni imágenes, ni programas ajenos), que se acomoda al celular y al modo oscuro. Cuenta qué es Mate en tres renglones, para quién es, un mostrador con IA entero (las pruebas del intérprete lo sacan de la página y lo corren), las cuatro diferencias, cómo bajarlo e instalarlo, el curso, y para qué **no** sirve todavía: no atiende por WhatsApp, es de una sola persona, es lento, los frenos no entienden lo que leen y la IA es paga. No lleva escrito ningún nombre ni dirección: los enlaces para bajar Mate y para leer el curso se arman solos cuando la página se publica con GitHub Pages, y si se abre como archivo suelto lo dice. El README se reordenó: arriba van qué es, "Instalarlo", "Por dónde empezar" y "El curso"; lo nuevo de la versión pasó a "Qué cambió en la 0.5", todo junto. Quedó afuera: publicar la página (lo decide el dueño) y traducirla.
*Mirada: quien le cuenta Mate a otro · Esfuerzo: mediano · Estado: hecha*

## Lo que se descartó

Para que quede constancia, estas ideas se discutieron y no entraron: funciones sin nombre con
`filtrar` y `transformar`; igualdad "aproximada" entre decimales; cambiar todos los números a
decimales exactos; permitir que una variable tape una función incluida; aceptar `función` con
tilde como sinónimo; comillas simples como segunda forma de texto; informar diez errores
juntos; aceptar decimales como posición de una lista; `preguntar ... a todos`; `preguntar ...
con limite`; `estado_de()` para espiar agentes; un segundo formato de errores para
herramientas; la traza en formato JSON; `*=` y `/=`; y la condición corta en un renglón.

(Una sola excepción a "una variable no tapa una función incluida", decidida en la revisión de
la 0.4: `aprender`, `lecciones` y `consultas_ia` llegaron con la 0.4 y son nombres muy
comunes, así que un programa que ya los usaba para algo suyo sigue corriendo igual. Lo mismo
vale para las tres de la 0.5: `leer_tabla`, `agregar_a_archivo` y `simular_teclado`. Las demás
funciones incluidas siguen sin poder taparse.)
