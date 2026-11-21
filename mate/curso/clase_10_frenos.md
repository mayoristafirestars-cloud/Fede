# Clase 10: Frenos, para poder confiar en la IA

## Qué vas a lograr

Una IA a veces inventa: un precio que no existe, un descuento que nadie autorizó. Si el
agente atiende clientes, eso no puede llegarle al cliente. Vas a ponerle **frenos** al
Mostrador: reglas que escribís vos y que Mate revisa en cada respuesta de la IA, antes de
que salga. No se le pide a la IA que se controle sola: el control lo hace Mate.

## El programa

Está en `mate\curso\clase_10_frenos.mate`:

    # Clase 10: frenos, para poder confiar en lo que dice la IA.
    # Una IA a veces inventa: un precio que no existe, un descuento que nadie autorizó.
    # Con 'frenos', el agente declara sus reglas y MATE revisa cada respuesta de la IA
    # antes de que salga. Si una respuesta rompe una regla, Mate consulta una vez más
    # avisándole a la IA qué hizo mal; si la vuelve a romper, devuelve el texto de 'reserva'.

    # (sin_ia es lo que "contesta la IA" en los ensayos, con --ia-simulada)
    mensaje Consulta { pregunta: texto, sin_ia: texto }

    agente Mostrador {
        estado permitidos = [3500, 1250.5, 950]

        frenos {
            precios: permitidos
            prohibido: ["descuento", "fiado"]
            largo: 200
            reserva: "Eso te lo confirma una persona. Ya te paso con alguien."
            consultas_por_dia: 50
        }

        al recibir Consulta como c {
            sea instrucciones = """
                Atendés el mostrador de un almacén. Contestá corto y amable.
                Precios: yerba $ 3.500, azúcar $ 1.250,50 y fideos $ 950.
            """
            responder consultar_ia(instrucciones, c.pregunta, c.sin_ia)
        }
    }

    funcion consultar(pregunta, sin_ia) {
        devolver preguntar Consulta { pregunta: pregunta, sin_ia: sin_ia } a Mostrador
    }

    funcion atender(pregunta, sin_ia) {
        mostrar("Cliente:   {pregunta}")
        mostrar("Mostrador: {consultar(pregunta, sin_ia)}")
    }

    # 1. Una respuesta buena: el precio está entre los permitidos, así que pasa tal cual.
    atender("¿Cuánto sale la yerba?", "La yerba sale $ 3.500.")
    # 2. Un precio inventado: $ 9.000 no está permitido. Al cliente le llega la reserva.
    atender("¿Y el café?", "El café sale $ 9.000 el kilo.")
    # 3. Un descuento que nadie autorizó: la palabra está entre las prohibidas.
    atender("¿Me hacés precio?", "¡Dale! Te hago un descuento.")

    sea reserva = "Eso te lo confirma una persona. Ya te paso con alguien."

    prueba "un precio permitido pasa" {
        simular_ia("Los fideos salen $ 950.")
        asegurar consultar("¿fideos?", "") == "Los fideos salen $ 950."
    }

    prueba "un precio inventado no le llega al cliente" {
        simular_ia("El café sale $ 9.000 el kilo.")
        asegurar consultar("¿café?", "") == reserva
        # Fueron dos consultas: la primera y el segundo intento, que tampoco pasó.
        asegurar largo(consultas_ia()) == 2
    }

    prueba "si en el segundo intento la IA se corrige, vale esa respuesta" {
        simular_ia(["El café sale $ 9.000 el kilo.", "Café no trabajamos."])
        asegurar consultar("¿café?", "") == "Café no trabajamos."
    }

`frenos { ... }` va dentro del agente, con una regla por renglón:

- `precios`: los únicos importes en pesos que la IA puede nombrar.
- `prohibido`: palabras que no pueden aparecer (no importan mayúsculas ni tildes).
- `largo`: cuántas letras puede tener la respuesta, como mucho.
- `reserva`: lo que se contesta en lugar de una respuesta mala.
- `consultas_por_dia`: el tope de gasto. Al llegar, ese día no consulta más a la IA y
  contesta con la reserva.

Cuando una respuesta rompe una regla, Mate **no la devuelve**: consulta una vez más,
avisándole a la IA qué regla rompió. Si la segunda respuesta está bien, vale esa. Si
vuelve a estar mal, al cliente le llega el texto de `reserva`.

En este programa, `sin_ia` es lo que "contesta la IA" en el ensayo: dos de las tres
respuestas están mal a propósito, para ver los frenos funcionando.

## Cómo se corre

    python mate\mate.py correr mate\curso\clase_10_frenos.mate --ia-simulada

Para ver cada freno saltando, paso por paso, agregale `--traza`.

## Lo que tiene que salir

    Cliente:   ¿Cuánto sale la yerba?
    Mostrador: La yerba sale $ 3.500.
    Cliente:   ¿Y el café?
    aviso: saltó un freno de Mostrador y quedó una lección propuesta, que no se usa hasta que la
    apruebes. Para verlas:  python mate\mate.py propuestas mate\curso\clase_10_frenos.mate
    Mostrador: Eso te lo confirma una persona. Ya te paso con alguien.
    Cliente:   ¿Me hacés precio?
    Mostrador: Eso te lo confirma una persona. Ya te paso con alguien.

El renglón que empieza con `aviso:` lo escribe Mate: cuenta que saltó un freno y que dejó
una lección propuesta. Eso es la clase 11. **Ese aviso sale solo la primera vez**: si
corrés de nuevo (por ejemplo con `--traza`), ya no aparece, porque la propuesta sigue
ahí, esperando que la apruebes o la descartes.

**Si de golpe contesta siempre la reserva**, mirá si arriba salió un renglón como este:

    aviso: Mostrador llegó a su tope (ya hizo 50 consulta(s) a la IA hoy y su tope es 50
    por día). Desde ahora contesta con el texto de reserva, sin consultar. ...

Es el tope de gasto haciendo su trabajo. En un ensayo (`--ia-simulada`) la cuenta arranca
de cero en cada corrida. Con la IA de verdad vale para todo el día: mañana vuelve a
consultar sola, o subí `consultas_por_dia`. Ojo: `--olvidar` no borra esa cuenta.

Al correrlo aparecen dos archivos nuevos al lado del programa:
`clase_10_frenos.memoria.json` (la cuenta de consultas del día) y
`clase_10_frenos.bitacora.txt` (los frenos que saltaron). Para verlos resumidos:

    python mate\mate.py bitacora mate\curso\clase_10_frenos.mate

Y las pruebas, que no escriben ningún archivo:

    python mate\mate.py probar mate\curso\clase_10_frenos.mate

      ✓ un precio permitido pasa
      ✓ un precio inventado no le llega al cliente
      ✓ si en el segundo intento la IA se corrige, vale esa respuesta
    3 de 3 pruebas pasaron

## El error más común

Poner reglas y olvidarse la `reserva`. Si Mate frena una respuesta, necesita saber qué
contestar en su lugar, así que lo avisa antes de correr:

    mate\curso\clase_10_frenos.mate:5: error: a los frenos de Mostrador les falta 'reserva': lo
    que contesta el agente cuando la IA rompe una regla dos veces seguidas. Por ejemplo:  reserva:
    "Eso te lo confirma una persona, ya te paso."
        5 |         prohibido: ["descuento", "fiado"]

Se arregla agregando el renglón `reserva: "..."` dentro de `frenos`.

Y un límite que conviene saber: los frenos buscan importes, palabras y cuentan letras. No
entienden el sentido de la respuesta. Una promesa dicha con otras palabras ("te lo dejo
más barato") pasa, salvo que la pongas en `prohibido`.

## Ejercicio

Copiá el programa en tu archivo de práctica y cambiá los frenos para que el Mostrador
tampoco pueda prometer envíos, y para que conteste en 120 letras como mucho. Escribí una
prueba para cada cosa. (Pista: `unir(rango(200), " ")` arma un texto bien largo.)

## Solución

También está en `mate\curso\clase_10_solucion.mate`.

    # Clase 10, ejercicio resuelto: tampoco puede prometer envíos, y contesta más corto.

    mensaje Consulta { pregunta: texto, sin_ia: texto }

    agente Mostrador {
        estado permitidos = [3500, 1250.5, 950]

        frenos {
            precios: permitidos
            prohibido: ["descuento", "fiado", "envío"]
            largo: 120
            reserva: "Eso te lo confirma una persona. Ya te paso con alguien."
            consultas_por_dia: 50
        }

        al recibir Consulta como c {
            sea instrucciones = """
                Atendés el mostrador de un almacén. Contestá corto y amable.
                Precios: yerba $ 3.500, azúcar $ 1.250,50 y fideos $ 950.
            """
            responder consultar_ia(instrucciones, c.pregunta, c.sin_ia)
        }
    }

    funcion consultar(pregunta, sin_ia) {
        devolver preguntar Consulta { pregunta: pregunta, sin_ia: sin_ia } a Mostrador
    }

    funcion atender(pregunta, sin_ia) {
        mostrar("Cliente:   {pregunta}")
        mostrar("Mostrador: {consultar(pregunta, sin_ia)}")
    }

    atender("¿Me lo mandan a casa?", "Sí, hacemos envíos a todo el barrio.")
    atender("¿Cuánto sale el azúcar?", "El azúcar sale $ 1.250,50.")

    sea reserva = "Eso te lo confirma una persona. Ya te paso con alguien."

    prueba "no promete envíos, con o sin tilde" {
        simular_ia("Te hacemos el ENVIO gratis.")
        asegurar consultar("¿mandan?", "") == reserva
    }

    prueba "una respuesta larguísima tampoco pasa" {
        simular_ia(unir(rango(200), " "))
        asegurar consultar("contame", "") == reserva
    }

Con `--ia-simulada` muestra (más el aviso de Mate):

    Cliente:   ¿Me lo mandan a casa?
    aviso: saltó un freno de Mostrador y quedó una lección propuesta, que no se usa hasta que la
    apruebes. Para verlas:  python mate\mate.py propuestas mate\curso\clase_10_solucion.mate
    Mostrador: Eso te lo confirma una persona. Ya te paso con alguien.
    Cliente:   ¿Cuánto sale el azúcar?
    Mostrador: El azúcar sale $ 1.250,50.

Siguiente: clase 11, un agente que recuerda y aprende (`python mate\mate.py curso 11`).
