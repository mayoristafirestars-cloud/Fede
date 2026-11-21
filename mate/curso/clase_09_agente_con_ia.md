# Clase 9: Un agente que consulta a una IA

## Qué vas a lograr

Vas a hacer que tu agente le pase la pregunta del cliente a una IA de verdad (Claude, de
la empresa Anthropic) y devuelva lo que contesta. Y vas a aprender a **ensayarlo sin
clave, sin internet y sin gastar**, que es como conviene trabajar casi siempre.

## El programa

Está en `mate\curso\clase_09_agente_con_ia.mate`:

    # Clase 9: un agente que le consulta a una IA.
    # consultar_ia(instrucciones, pregunta, ensayo) le manda la pregunta a una IA de verdad
    # y devuelve lo que contesta, como texto.
    #   - las instrucciones le dicen quién es y cómo tiene que contestar;
    #   - el tercer valor es lo que "contesta" cuando NO se habla con la IA de verdad: en
    #     las pruebas y con la opción --ia-simulada. Así se ensaya sin clave y sin gastar.

    mensaje Consulta { pregunta: texto }
    mensaje Atencion { respuesta: texto }

    agente Mostrador {
        al recibir Consulta como c {
            # Un texto largo va entre tres comillas, y puede ocupar varios renglones.
            sea instrucciones = """
                Atendés el mostrador de un almacén de barrio. Contestá en una sola oración,
                corta y amable.
            """
            sea dicho = consultar_ia(instrucciones, c.pregunta, "Ya te lo averiguo.")
            responder Atencion { respuesta: dicho }
        }
    }

    funcion atender(pregunta) {
        sea atencion = preguntar Consulta { pregunta: pregunta } a Mostrador
        mostrar("Cliente:   {pregunta}")
        mostrar("Mostrador: {atencion.respuesta}")
    }

    atender("¿Tienen yerba sin palo?")
    atender("¿A qué hora cierran?")

    # En una prueba la IA nunca es de verdad. simular_ia() fija lo que "contesta", y
    # consultas_ia() cuenta qué le llegó: las instrucciones, la pregunta y la respuesta.
    prueba "el Mostrador contesta lo que dijo la IA" {
        simular_ia("Sí, tenemos de medio kilo.")
        sea atencion = preguntar Consulta { pregunta: "¿Hay yerba?" } a Mostrador
        asegurar atencion.respuesta == "Sí, tenemos de medio kilo."
    }

    prueba "a la IA le llegan las instrucciones y la pregunta" {
        simular_ia("Hola.")
        sea atencion = preguntar Consulta { pregunta: "¿Hay yerba?" } a Mostrador
        sea consulta = ultimo(consultas_ia())
        asegurar tiene(consulta.instrucciones, "almacén de barrio")
        asegurar consulta.pregunta == "¿Hay yerba?"
        asegurar atencion.respuesta == "Hola."
    }

- `consultar_ia(instrucciones, pregunta, ensayo)` lleva tres cosas: las instrucciones
  (quién es la IA y cómo tiene que contestar), la pregunta, y lo que se contesta cuando
  no se habla con la IA de verdad.
- Un texto entre tres comillas `"""` puede ocupar varios renglones.
- En las pruebas la IA **nunca** es de verdad: `simular_ia("...")` fija qué contesta.
- `consultas_ia()` da la lista de las consultas que se hicieron en esa prueba. `ultimo()`
  saca la última.

## Cómo se corre

Para ensayar, con la opción `--ia-simulada`:

    python mate\mate.py correr mate\curso\clase_09_agente_con_ia.mate --ia-simulada

## Lo que tiene que salir

    Cliente:   ¿Tienen yerba sin palo?
    Mostrador: Ya te lo averiguo.
    Cliente:   ¿A qué hora cierran?
    Mostrador: Ya te lo averiguo.

Las dos veces contesta lo mismo, porque es el tercer valor de `consultar_ia`. Para que el
ensayo conteste distinto según la pregunta, las respuestas se escriben en un archivo de
texto. En la carpeta del curso hay uno, `respuestas.txt` (abrilo con el Bloc de notas):

    python mate\mate.py correr mate\curso\clase_09_agente_con_ia.mate --ia-simulada=mate\curso\respuestas.txt

(Va todo en un solo renglón.) Y sale:

    Cliente:   ¿Tienen yerba sin palo?
    Mostrador: Sí, tenemos yerba con palo y sin palo.
    Cliente:   ¿A qué hora cierran?
    Mostrador: Abrimos de 8 a 20, de lunes a sábado.

**Con la IA de verdad** es el mismo comando sin `--ia-simulada`. Es **pago**: Anthropic
cobra cada consulta. Los pasos:

1. Entrá a `platform.claude.com`, creá una cuenta, cargá crédito y sacá una clave.
2. En la misma ventana de PowerShell donde vas a correr, guardá la clave (con la tuya):

       $env:ANTHROPIC_API_KEY = "tu-clave"

3. Corré el programa sin `--ia-simulada`.

La clave **nunca se escribe en el programa** ni en ningún archivo: vive en esa ventana de
PowerShell y se va al cerrarla. No se la pases a nadie.

## El error más común

Olvidarse el `--ia-simulada` cuando no pusiste la clave. Mate no puede hablar con la IA
y te dice qué hacer:

    mate\curso\clase_09_agente_con_ia.mate:18: error: consultar_ia(): falta la clave para hablar
    con la IA. En PowerShell, antes de correr, escribí:  $env:ANTHROPIC_API_KEY = "tu-clave"
    La clave se saca en platform.claude.com y el servicio es pago (se cobra cada consulta). Para
    probar sin clave y sin gastar: --ia-simulada
        18 |         sea dicho = consultar_ia(instrucciones, c.pregunta, "Ya te lo averiguo.")
        cómo se llegó: se lo preguntó el programa a Mostrador (línea 24), en atender(), llamada
        desde la línea 29

Se arregla agregando `--ia-simulada` (para ensayar) o poniendo la clave (para usarla de
verdad).

## Ejercicio

Copiá el programa en tu archivo de práctica y hacé dos cambios:

1. Agregale el horario a las instrucciones ("de lunes a sábado, de 8 a 20; los domingos
   está cerrado"), para que la IA lo sepa.
2. Que el Mostrador no se caiga si la IA no contesta: usá `intentar { ... } si falla { ... }`
   (el de la clase 6) y, si falla, que responda "Ahora no te puedo atender. Probá en un
   rato."

Escribile una prueba que compruebe que el horario le llega a la IA.

## Solución

También está en `mate\curso\clase_09_solucion.mate`.

    # Clase 9, ejercicio resuelto: el Mostrador sabe el horario, porque está en sus
    # instrucciones, y si la IA no puede contestar no se cae: avisa.

    mensaje Consulta { pregunta: texto }
    mensaje Atencion { respuesta: texto }

    agente Mostrador {
        al recibir Consulta como c {
            sea instrucciones = """
                Atendés el mostrador de un almacén de barrio. Contestá en una sola oración,
                corta y amable.
                Horario: de lunes a sábado, de 8 a 20. Los domingos está cerrado.
            """
            intentar {
                sea dicho = consultar_ia(instrucciones, c.pregunta, "Ya te lo averiguo.")
                responder Atencion { respuesta: dicho }
            } si falla {
                # Sin clave, sin internet o sin crédito: no inventa nada.
                responder Atencion { respuesta: "Ahora no te puedo atender. Probá en un rato." }
            }
        }
    }

    funcion atender(pregunta) {
        sea atencion = preguntar Consulta { pregunta: pregunta } a Mostrador
        mostrar("Cliente:   {pregunta}")
        mostrar("Mostrador: {atencion.respuesta}")
    }

    atender("¿Abren los domingos?")

    prueba "el horario le llega a la IA en las instrucciones" {
        simular_ia("Los domingos cerramos.")
        sea atencion = preguntar Consulta { pregunta: "¿Abren los domingos?" } a Mostrador
        asegurar tiene(ultimo(consultas_ia()).instrucciones, "Los domingos está cerrado")
        asegurar atencion.respuesta == "Los domingos cerramos."
    }

Con `--ia-simulada` muestra:

    Cliente:   ¿Abren los domingos?
    Mostrador: Ya te lo averiguo.

Y sin `--ia-simulada` ni clave ya no corta con un error:

    Cliente:   ¿Abren los domingos?
    Mostrador: Ahora no te puedo atender. Probá en un rato.

Siguiente: clase 10, frenos para la IA (`python mate\mate.py curso 10`).
