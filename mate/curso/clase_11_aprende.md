# Clase 11: Un agente que recuerda y aprende

## Qué vas a lograr

Vas a hacer que el Mostrador recuerde cosas de una vez a la otra, y vas a corregirlo
**sin tocar el programa**: le anotás lecciones desde PowerShell, y Mate se las pasa a la
IA en cada consulta. Además vas a ver las lecciones que Mate propone solo cuando salta un
freno, y que no se usan hasta que las aprobás.

## El programa

Está en `mate\curso\clase_11_aprende.mate`. Es el de la clase 10 con una palabra nueva,
`recordado`:

    # Clase 11: un agente que recuerda y aprende.
    # Tres cosas nuevas, y ninguna se programa: se usan desde PowerShell.
    #   - 'estado recordado': ese dato no se pierde cuando el programa termina.
    #   - lecciones: correcciones que le anotás al agente con la orden 'corregir'. Mate se
    #     las pasa a la IA en cada consulta, sin tocar el programa.
    #   - propuestas: cuando salta un freno, Mate deja una lección PROPUESTA. El agente no
    #     la usa hasta que la aprobás.

    mensaje Consulta { pregunta: texto, sin_ia: texto }
    mensaje Atencion { respuesta: texto, numero: numero }

    agente Mostrador {
        # 'recordado': se guarda al terminar, y la próxima vez arranca con lo que quedó.
        estado recordado atendidos = 0
        estado permitidos = [3500, 1250.5, 950]

        frenos {
            precios: permitidos
            prohibido: ["descuento", "fiado"]
            reserva: "Eso te lo confirma una persona. Ya te paso con alguien."
            consultas_por_dia: 50
        }

        al recibir Consulta como c {
            atendidos += 1
            sea instrucciones = """
                Atendés el mostrador de un almacén. Contestá corto y amable.
                Precios: yerba $ 3.500, azúcar $ 1.250,50 y fideos $ 950.
            """
            sea dicho = consultar_ia(instrucciones, c.pregunta, c.sin_ia)
            responder Atencion { respuesta: dicho, numero: atendidos }
        }
    }

    funcion atender(pregunta, sin_ia) {
        sea atencion = preguntar Consulta { pregunta: pregunta, sin_ia: sin_ia } a Mostrador
        mostrar("Cliente:   {pregunta}")
        mostrar("Mostrador: {atencion.respuesta}")
        mostrar("   (consulta número {atencion.numero} desde que abrió el mostrador)")
    }

    atender("¿Cuánto sale la yerba?", "La yerba sale $ 3.500.")
    atender("¿Y el café?", "El café sale $ 9.000 el kilo.")

    # En las pruebas no hay memoria ni lecciones guardadas: cada prueba arranca limpia.
    # aprender() le fija una lección al agente, para comprobar que le llega a la IA.
    prueba "cada prueba arranca de cero" {
        simular_ia("Hola.")
        sea atencion = preguntar Consulta { pregunta: "hola", sin_ia: "" } a Mostrador
        asegurar atencion.numero == 1
    }

    prueba "la lección le llega a la IA con las instrucciones" {
        aprender("Los domingos el almacén está cerrado.", Mostrador)
        simular_ia("Los domingos cerramos.")
        sea atencion = preguntar Consulta { pregunta: "¿Abren hoy?", sin_ia: "" } a Mostrador
        sea instrucciones = ultimo(consultas_ia()).instrucciones
        asegurar tiene(instrucciones, "Los domingos el almacén está cerrado.")
        asegurar atencion.respuesta == "Los domingos cerramos."
    }

- `estado recordado atendidos = 0`: ese dato se guarda cuando el programa termina y
  vuelve la próxima vez. El 0 es el valor de la primera vez.
- Lo que se recuerda queda en un archivo al lado del programa
  (`clase_11_aprende.memoria.json`). No se manda a ningún lado.
- `aprender("...", Mostrador)` solo se usa así en las pruebas, para fijarle una lección.

## Cómo se corre

    python mate\mate.py correr mate\curso\clase_11_aprende.mate --ia-simulada

## Lo que tiene que salir

La primera vez:

    Cliente:   ¿Cuánto sale la yerba?
    Mostrador: La yerba sale $ 3.500.
       (consulta número 1 desde que abrió el mostrador)
    aviso: saltó un freno de Mostrador y quedó una lección propuesta, que no se usa hasta que la
    apruebes. Para verlas:  python mate\mate.py propuestas mate\curso\clase_11_aprende.mate
    Cliente:   ¿Y el café?
    Mostrador: Eso te lo confirma una persona. Ya te paso con alguien.
       (consulta número 2 desde que abrió el mostrador)

(El renglón de `aviso:` sale solo esa primera vez, mientras la propuesta siga sin aprobar
ni descartar.)

Corrélo de nuevo, con el mismo comando. Ahora la cuenta sigue desde donde quedó:

       (consulta número 3 desde que abrió el mostrador)
       (consulta número 4 desde que abrió el mostrador)

### Corregir al agente: una lección

Supongamos que el Mostrador le dijo a un cliente que el domingo estaba abierto. Se lo
corregís así (todo en un renglón: la orden, el programa, el agente y la lección entre
comillas):

    python mate\mate.py corregir mate\curso\clase_11_aprende.mate Mostrador "Los domingos el almacén está cerrado."

    Anotado. Mostrador tiene 1 lección(es):
      1. Los domingos el almacén está cerrado.   (del 21/11/2026 16:39)
    La va a tener en cuenta cada vez que consulte a la IA con consultar_ia(), desde la próxima
    corrida de clase_11_aprende.mate (la memoria y las lecciones son del programa que se corre).
    Para borrar una:  python mate\mate.py lecciones mate\curso\clase_11_aprende.mate Mostrador
    --borrar=1

Desde la próxima corrida, esa lección viaja con las instrucciones cada vez que el
Mostrador consulta a la IA.

### Las lecciones que propone Mate

Cuando saltó el freno del café, Mate dejó una lección **propuesta**. Para verla:

    python mate\mate.py propuestas mate\curso\clase_11_aprende.mate

    Lecciones propuestas, sin aprobar (1). Ningún agente las usa todavía:
      1. Para Mostrador: No nombres ningún importe que no esté en los precios que te dieron. Si no
      sabés un precio, decí que lo confirma una persona.   (del 21/11/2026 16:39)
           Por qué: saltó un freno: nombró el importe $ 9.000, que no está entre los precios
           permitidos. La IA había contestado: "El café sale $ 9.000 el kilo."
    Para aprobar una:    python mate\mate.py propuestas mate\curso\clase_11_aprende.mate aprobar 1
    Para descartar una:  python mate\mate.py propuestas mate\curso\clase_11_aprende.mate descartar
    1     (o varias: descartar 1 2, o todas)

El Mostrador no la usa hasta que la aprobás:

    python mate\mate.py propuestas mate\curso\clase_11_aprende.mate aprobar 1

    Listo: aprobé 1 propuesta. Desde la próxima corrida la va a tener en cuenta en cada consulta a
    la IA.
    Mostrador tiene 2 lección(es):
      1. Los domingos el almacén está cerrado.   (del 21/11/2026 16:39)
      2. No nombres ningún importe que no esté en los precios que te dieron. Si no sabés un
      precio, decí que lo confirma una persona.   (del 21/11/2026 16:39)

Si no te convence, `descartar 1` en vez de `aprobar 1`.

### Ver qué le llega a la IA

Con `--traza` se ve cada consulta, y debajo las lecciones que viajaron con ella:

    python mate\mate.py correr mate\curso\clase_11_aprende.mate --ia-simulada --traza

Muestra mucho. Lo primero es esto, con las dos lecciones debajo de la consulta:

      ·  1. (programa) pregunta a Mostrador: Consulta { pregunta: "¿Cuánto sale la yerba?",
      sin_ia: "La yerba sale $ 3.500." }   (conversación 1)
      ·        Mostrador consulta a la IA (simulada): "¿Cuánto sale la yerba?"
      ·           con la lección 1: "Los domingos el almacén está cerrado."
      ·           con la lección 2: "No nombres ningún importe que no esté en los precios que te
      dieron. Si..."
      ·        la IA contesta: "La yerba sale $ 3.500."
      ·  1. Mostrador responde a (programa): Atencion { respuesta: "La yerba sale $ 3.500.",
      numero: 5 }

### Otras órdenes que conviene conocer

    python mate\mate.py lecciones mate\curso\clase_11_aprende.mate
    python mate\mate.py lecciones mate\curso\clase_11_aprende.mate Mostrador --borrar=1
    python mate\mate.py bitacora mate\curso\clase_11_aprende.mate
    python mate\mate.py correr mate\curso\clase_11_aprende.mate --ia-simulada --olvidar

La primera muestra las lecciones; la segunda le borra la número 1; `bitacora` resume los
frenos que saltaron y cuánto consultó a la IA cada día; y `--olvidar` hace que el agente
arranque de cero (las lecciones no se borran con eso).

Una aclaración honesta: una lección es un texto que se le suma a las instrucciones. La
IA la tiene en cuenta, pero no es una garantía. Lo que tiene que cumplirse sí o sí va en
los frenos o en el programa.

## El error más común

Escribir mal el nombre del agente en `corregir` (va igual que en el programa, con su
mayúscula):

    python mate\mate.py corregir mate\curso\clase_11_aprende.mate Mostrado "Cerramos a las 20."

    clase_11_aprende.mate no tiene un agente 'Mostrado'. ¿Quisiste decir 'Mostrador'? Sus agentes
    son: Mostrador

El otro tropiezo es olvidarse las comillas de la lección: sin comillas, PowerShell la
parte en palabras sueltas.

## Ejercicio

Copiá el programa en tu archivo de práctica y hacé que el Mostrador también recuerde
cuántas veces tuvo que contestar con el texto de reserva, y que lo diga cuando le llega
un mensaje `CuantasReservas`. (Pista: guardá el texto de reserva con un `sea` arriba de
todo y comparalo con lo que devolvió `consultar_ia`.)

## Solución

También está en `mate\curso\clase_11_solucion.mate`.

    # Clase 11, ejercicio resuelto: el Mostrador también recuerda cuántas veces tuvo que
    # contestar con el texto de reserva, y lo dice cuando se lo preguntan.

    mensaje Consulta { pregunta: texto, sin_ia: texto }
    mensaje Atencion { respuesta: texto, numero: numero }
    mensaje CuantasReservas {}

    sea reserva = "Eso te lo confirma una persona. Ya te paso con alguien."

    agente Mostrador {
        estado recordado atendidos = 0
        estado recordado con_reserva = 0
        estado permitidos = [3500, 1250.5, 950]

        frenos {
            precios: permitidos
            prohibido: ["descuento", "fiado"]
            reserva: reserva
            consultas_por_dia: 50
        }

        al recibir Consulta como c {
            atendidos += 1
            sea instrucciones = """
                Atendés el mostrador de un almacén. Contestá corto y amable.
                Precios: yerba $ 3.500, azúcar $ 1.250,50 y fideos $ 950.
            """
            sea dicho = consultar_ia(instrucciones, c.pregunta, c.sin_ia)
            si dicho == reserva {
                con_reserva += 1
            }
            responder Atencion { respuesta: dicho, numero: atendidos }
        }

        al recibir CuantasReservas {
            responder con_reserva
        }
    }

    funcion atender(pregunta, sin_ia) {
        sea atencion = preguntar Consulta { pregunta: pregunta, sin_ia: sin_ia } a Mostrador
        mostrar("Cliente:   {pregunta}")
        mostrar("Mostrador: {atencion.respuesta}")
    }

    atender("¿Cuánto sale la yerba?", "La yerba sale $ 3.500.")
    atender("¿Y el café?", "El café sale $ 9.000 el kilo.")
    sea reservas = preguntar CuantasReservas {} a Mostrador
    mostrar("Hasta ahora contestó con la reserva {reservas} vez/veces")

    prueba "cuenta las veces que contestó con la reserva" {
        simular_ia(["Hola.", "El café sale $ 9.000.", "El café sale $ 9.000."])
        sea una = preguntar Consulta { pregunta: "hola", sin_ia: "" } a Mostrador
        sea otra = preguntar Consulta { pregunta: "¿café?", sin_ia: "" } a Mostrador
        asegurar una.respuesta == "Hola." y otra.respuesta == reserva
        asegurar (preguntar CuantasReservas {} a Mostrador) == 1
    }

La primera vez, con `--ia-simulada`, muestra (más el aviso de Mate):

    Cliente:   ¿Cuánto sale la yerba?
    Mostrador: La yerba sale $ 3.500.
    aviso: saltó un freno de Mostrador y quedó una lección propuesta, que no se usa hasta que la
    apruebes. Para verlas:  python mate\mate.py propuestas mate\curso\clase_11_solucion.mate
    Cliente:   ¿Y el café?
    Mostrador: Eso te lo confirma una persona. Ya te paso con alguien.
    Hasta ahora contestó con la reserva 1 vez/veces

Siguiente: clase 12, el mostrador completo (`python mate\mate.py curso 12`).
