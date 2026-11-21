# Clase 12: El mostrador completo

## Qué vas a lograr

Vas a juntar todo el curso en un programa que sirve de verdad: un mostrador que lee tu
lista de precios, charla por teclado, contesta con una IA, tiene frenos para que la IA no
invente precios y recuerda cuántas consultas atendió. Y vas a ver los pasos para pasarlo
del ensayo a la IA de verdad con tu propia lista.

## El programa

Está en `mate\curso\clase_12_mostrador.mate`. Es largo, pero no tiene nada que no hayas
visto: cada parte es de una clase anterior.

    # Clase 12: el mostrador completo.
    # Junta todo el curso: lee tu lista de precios, charla por teclado, contesta con una
    # IA, tiene frenos para que la IA no invente precios, y recuerda cuántas consultas atendió.

    mensaje CargarLista { filas: lista }
    mensaje Consulta { pregunta: texto, sin_ia: texto }
    mensaje Atencion { respuesta: texto, numero: numero, aviso: texto? }

    agente Mostrador {
        estado filas = []
        estado recordado atendidos = 0

        frenos {
            # Los únicos importes que la IA puede nombrar: los de la columna "precio".
            precios: solo_precios(filas)
            prohibido: ["descuento", "fiado"]
            largo: 300
            reserva: "Eso te lo confirma una persona. Ya te paso con alguien."
            consultas_por_dia: 200
        }

        # Un agente no toca archivos: el programa lee la lista y se la manda en un mensaje.
        al recibir CargarLista como c {
            filas = c.filas
        }

        al recibir Consulta como c {
            atendidos += 1
            sea instrucciones = """
                Atendés el mostrador de un almacén. Contestá en castellano rioplatense, corto
                y amable. Usá SOLO los precios de esta lista. Si piden algo que no está,
                decí que no lo trabajamos. Si dice SIN STOCK, avisá que ahora no hay.

                LISTA DE PRECIOS:
                {lista_en_texto(filas)}
            """
            intentar {
                sea dicho = consultar_ia(instrucciones, c.pregunta, c.sin_ia)
                responder Atencion { respuesta: dicho, numero: atendidos }
            } si falla motivo {
                # Sin clave, sin internet o sin crédito: contesta con lo que hay en la lista.
                responder Atencion { respuesta: c.sin_ia, numero: atendidos, aviso: motivo }
            }
        }
    }

    funcion solo_precios(tabla) {
        var importes = []
        para fila en tabla {
            importes = agregar(importes, fila.precio)
        }
        devolver importes
    }

    funcion renglon_de(fila) {
        si fila.stock == 0 {
            devolver "{fila.producto}: {pesos(fila.precio)} - SIN STOCK"
        }
        devolver "{fila.producto}: {pesos(fila.precio)}"
    }

    funcion lista_en_texto(tabla) {
        var renglones = []
        para fila en tabla {
            renglones = agregar(renglones, "- " + renglon_de(fila))
        }
        devolver unir(renglones, "\n")
    }

    # En minúscula y sin tildes, para que "AZUCAR" y "azúcar" sean lo mismo al buscar.
    funcion llano(t) {
        var r = minusculas(t)
        para con, sin en { "á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u" } {
            r = reemplazar(r, con, sin)
        }
        devolver r
    }

    # Lo que se contesta cuando no hay IA: el producto de la lista que nombró el cliente.
    # (Busca la primera palabra del producto: "yerba", "azucar", "fideos"...)
    funcion buscar_en_lista(tabla, pregunta) {
        para fila en tabla {
            sea palabra = llano(partir(fila.producto, " ")[0])
            si tiene(llano(pregunta), palabra) {
                devolver renglon_de(fila)
            }
        }
        devolver "Eso no lo encuentro en la lista. Probá con el nombre del producto."
    }

    # Antes de atender, mira que la planilla tenga lo que el programa necesita. Si algo
    # está mal, lo dice con el nombre del producto y el programa no sigue.
    funcion revisar_lista(tabla) {
        sea arreglo = "Corregilo en Excel, guardá de nuevo como CSV y volvé a correr."
        si largo(tabla) == 0 {
            fallar "precios.csv no tiene productos debajo de los títulos. {arreglo}"
        }
        var cuenta = 0
        para fila en tabla {
            cuenta += 1
            para titulo en ["producto", "precio", "stock"] {
                si no tiene(fila, titulo) {
                    sea hay = unir(claves(fila), ";")
                    sea va = "La primera fila tiene que decir producto;precio;stock, en minúscula"
                    sea falta = "A precios.csv le falta la columna '{titulo}'"
                    fallar "{falta}. {va}, y dice: {hay}. {arreglo}"
                }
            }
            sea cual = "En precios.csv, el producto {cuenta} ({fila.producto})"
            si tipo(fila.precio) != "numero" {
                fallar "{cual} no tiene el precio en números: dice \"{fila.precio}\". {arreglo}"
            }
            si tipo(fila.stock) != "numero" {
                fallar "{cual} no tiene el stock en números (si no hay, va 0). {arreglo}"
            }
        }
    }

    # La charla: una consulta atrás de otra, hasta que escriben chau.
    funcion charlar(tabla) {
        var consultas = 0
        mientras verdadero {
            sea dicho = leer("Cliente:", "chau")
            si dicho == "" {
                continuar
            }
            si minusculas(dicho) == "chau" {
                romper
            }
            sea atencion = preguntar Consulta {
                pregunta: dicho, sin_ia: buscar_en_lista(tabla, dicho),
            } a Mostrador
            mostrar("Mostrador: {atencion.respuesta}")
            si atencion.aviso != nada {
                mostrar("   (la IA no contestó y busqué en la lista. Motivo: {atencion.aviso})")
            }
            consultas += 1
        }
        devolver consultas
    }

    sea precios = leer_tabla("precios.csv")
    revisar_lista(precios)
    enviar CargarLista { filas: precios } a Mostrador
    mostrar("Mostrador: cargué {largo(precios)} productos de precios.csv.")
    mostrar("Escribí tu consulta y apretá Enter. Para terminar, escribí chau.")
    sea atendidas = charlar(precios)
    mostrar("Hasta luego. En esta charla atendí {atendidas} consulta(s).")

    # Cada prueba arranca limpia, con el Mostrador sin lista: por eso primero se la mandan.
    prueba "charla hasta que dicen chau" {
        enviar CargarLista { filas: precios } a Mostrador
        simular_teclado(["¿Cuánto sale la yerba?", "", "y el arroz?", "Chau", "esto no se lee"])
        asegurar charlar(precios) == 2
        asegurar mensajes_enviados("Consulta")[1].mensaje.pregunta == "y el arroz?"
    }

    prueba "la lista de precios le llega a la IA" {
        enviar CargarLista { filas: precios } a Mostrador
        simular_ia("La yerba sale $ 3.500.")
        simular_teclado(["¿Cuánto sale la yerba?"])
        asegurar charlar(precios) == 1
        sea consulta = ultimo(consultas_ia())
        asegurar tiene(consulta.instrucciones, "- Yerba mate 1 kg: $ 3.500,00")
        asegurar tiene(consulta.instrucciones, "- Fideos 500 g: $ 950,00 - SIN STOCK")
    }

    prueba "un precio que no está en la lista no le llega al cliente" {
        enviar CargarLista { filas: precios } a Mostrador
        simular_ia("El café sale $ 9.000 el kilo.")
        sea atencion = preguntar Consulta { pregunta: "¿Y el café?", sin_ia: "" } a Mostrador
        asegurar atencion.respuesta == "Eso te lo confirma una persona. Ya te paso con alguien."
    }

    prueba "sin IA busca el producto en la lista" {
        asegurar buscar_en_lista(precios, "¿Tenés ARROZ?") == "Arroz 1 kg: $ 1.800,00"
        asegurar buscar_en_lista(precios, "y el azucar?") == "Azúcar 1 kg: $ 1.250,50"
        asegurar empieza_con(buscar_en_lista(precios, "¿y clavos?"), "Eso no lo encuentro")
    }

    prueba "una planilla con un precio mal escrito se avisa antes de atender" {
        revisar_lista(precios)
        sea mala = [{ producto: "Pan", precio: "consultar", stock: 3 }]
        intentar {
            revisar_lista(mala)
            fallar "tendría que haber fallado"
        } si falla motivo {
            asegurar tiene(texto(motivo), "(Pan) no tiene el precio en números")
        }
    }

Qué parte viene de cada clase:

- La lista de precios (`leer_tabla`) y la búsqueda: clase 7.
- La charla (`leer`, `mientras`, `romper`): clase 6.
- Los mensajes y el agente: clase 8.
- `consultar_ia` y el ensayo sin clave: clase 9.
- Los `frenos`: clase 10. Acá los precios permitidos salen de la planilla, así que si
  cambiás un precio en Excel el freno lo sigue solo.
- `estado recordado`, lecciones y propuestas: clase 11.

Lo único nuevo son cuatro detalles:

- `enviar CargarLista { ... } a Mostrador` manda el mensaje **sin esperar respuesta**
  (con `preguntar` se espera). Un agente no lee archivos: el programa lee la lista y se
  la manda.
- `aviso: texto?` en un mensaje: el signo de pregunta dice que ese dato puede faltar.
- `revisar_lista(precios)` mira la planilla **antes de atender**: que estén las columnas
  `producto`, `precio` y `stock`, y que cada precio y cada stock sean números. Si algo
  está mal, lo dice con el nombre del producto y el programa no arranca.
- `llano(texto)` pasa un texto a minúscula y sin tildes, para que al buscar en la lista
  dé lo mismo "AZUCAR", "azucar" o "azúcar".

## Cómo se corre

Para ensayar, sin clave y sin gastar:

    python mate\mate.py correr mate\curso\clase_12_mostrador.mate --ia-simulada

Escribí consultas y apretá Enter. Para terminar, `chau` (o `Ctrl+C`; con la orden corta
`mate`, después de `Ctrl+C` Windows puede preguntar "¿Desea terminar el trabajo por
lotes (S/N)?": escribí `S` y Enter).

## Lo que tiene que salir

Depende de lo que escribas. En el ensayo no hay IA: el Mostrador busca en la lista el
producto que nombraste. Si preguntás por la yerba, los fideos y los clavos:

    Mostrador: cargué 5 productos de precios.csv.
    Escribí tu consulta y apretá Enter. Para terminar, escribí chau.
    Cliente: ¿Cuánto sale la yerba?
    Mostrador: Yerba mate 1 kg: $ 3.500,00
    Cliente: ¿Tenés fideos?
    Mostrador: Fideos 500 g: $ 950,00 - SIN STOCK
    Cliente: ¿Y clavos?
    Mostrador: Eso no lo encuentro en la lista. Probá con el nombre del producto.
    Cliente: chau
    Hasta luego. En esta charla atendí 3 consulta(s).

Las pruebas:

    python mate\mate.py probar mate\curso\clase_12_mostrador.mate

      ✓ charla hasta que dicen chau
      ✓ la lista de precios le llega a la IA
      ✓ un precio que no está en la lista no le llega al cliente
      ✓ sin IA busca el producto en la lista
      ✓ una planilla con un precio mal escrito se avisa antes de atender
    5 de 5 pruebas pasaron

## Para usarlo de verdad

1. **Tu lista de precios.** Guardá tu planilla de Excel como CSV, con el nombre
   `precios.csv`, en la carpeta del programa (los pasos están en la clase 7). Los títulos
   tienen que ser `producto`, `precio` y `stock`, en minúscula y en la primera fila (sin
   el nombre de la lista arriba), y cada precio y cada stock, un número (ni vacío ni
   "consultar"). Si algo de eso falla, el programa te lo dice al arrancar.
2. **Tus instrucciones.** En el Bloc de notas, cambiá el texto de `instrucciones` para que
   cuente cómo es tu negocio: horarios, zona de entrega, formas de pago.
3. **Tus frenos.** Revisá `prohibido` y `reserva`, y bajá `consultas_por_dia` a un número
   que te deje tranquilo: es el tope de gasto. Cuando el Mostrador llega al tope, Mate lo
   avisa en pantalla una vez (`aviso: Mostrador llegó a su tope...`) y desde ahí contesta
   la reserva. En un ensayo la cuenta arranca de cero en cada corrida; con la IA de verdad
   vale para todo el día (`--olvidar` no la borra).
4. **Ensayá** con `--ia-simulada` y corré las pruebas con `probar`.
5. **La clave.** Cuando ande, poné la clave en la ventana de PowerShell (clase 9) y
   corrélo sin `--ia-simulada`. Desde ahí cada consulta se paga.
6. **Corregilo con el uso.** Cuando conteste algo que no te gusta, anotale una lección con
   `corregir`; cada tanto mirá `propuestas` y `bitacora` (clase 11).

Lo que este mostrador **no** hace todavía: atiende en la ventana de PowerShell, no por
WhatsApp ni por una página web. Y cada consulta a la IA es suelta: la IA no se acuerda de
la pregunta anterior del mismo cliente.

**Tampoco dice totales.** El freno deja pasar solo los precios de la lista: si un cliente
pregunta cuánto salen 3 yerbas y la IA contesta "$ 10.500", ese importe no está en la
lista y al cliente le llega la reserva. Si en tu negocio eso se pregunta mucho, hay que
calcular esos totales en el programa y sumarlos a los `precios` de los frenos (en
`solo_precios`, agregando también el precio por 2, por 3...). Está explicado en
`mate\README.md`, en "El freno de precios, con detalle".

## El error más común

Correrlo sin `--ia-simulada` cuando todavía no pusiste la clave. Este programa no se
corta: contesta con lo que encuentra en la lista y te cuenta el motivo.

    Mostrador: cargué 5 productos de precios.csv.
    Escribí tu consulta y apretá Enter. Para terminar, escribí chau.
    Cliente: arroz
    Mostrador: Arroz 1 kg: $ 1.800,00
       (la IA no contestó y busqué en la lista. Motivo: consultar_ia(): falta la clave para hablar
       con la IA. En PowerShell, antes de correr, escribí:  $env:ANTHROPIC_API_KEY = "tu-clave"
    La clave se saca en platform.claude.com y el servicio es pago (se cobra cada consulta). Para
    probar sin clave y sin gastar: --ia-simulada)
    Cliente: chau
    Hasta luego. En esta charla atendí 1 consulta(s).

Se arregla igual que en la clase 9: `--ia-simulada` para ensayar, o la clave para usarlo
de verdad.

El otro tropiezo, cuando ponés tu propia planilla: que los títulos no sean `producto`,
`precio` y `stock` (Excel los suele dejar con mayúscula), o que un precio esté vacío. El
programa lo revisa al arrancar y dice qué corregir en la planilla:

    A precios.csv le falta la columna 'producto'. La primera fila tiene que decir
    producto;precio;stock, en minúscula, y dice: Producto;Precio;Stock. Corregilo en
    Excel, guardá de nuevo como CSV y volvé a correr.

Y si al cambiar los `frenos` te equivocás (un nombre de columna mal escrito en
`solo_precios`, un `consultas_por_dia` negativo), el programa no sigue atendiendo sin
frenos: corta y dice `los frenos de Mostrador están mal escritos`, con el renglón.

## Ejercicio

Copiá el programa en tu archivo de práctica y hacé que cada consulta quede anotada en un
archivo `consultas_atendidas.txt`, un renglón por consulta, con la fecha, lo que
preguntaron y lo que se contestó. Hay una función que hace justo eso:
`agregar_a_archivo("consultas_atendidas.txt", texto)`, y `ahora()` da la fecha y la hora.
(Para saber más de cualquiera de las dos: `python mate\mate.py ayuda agregar_a_archivo`.)

## Solución

También está en `mate\curso\clase_12_solucion.mate`. Son dos cambios, marcados con
`LO NUEVO`:

    # Clase 12, ejercicio resuelto: cada consulta queda anotada en un archivo, para
    # mirarlas después con el Bloc de notas. Es el programa de la clase con dos cambios:
    # la función anotar() y el renglón que la llama dentro de charlar().

    mensaje CargarLista { filas: lista }
    mensaje Consulta { pregunta: texto, sin_ia: texto }
    mensaje Atencion { respuesta: texto, numero: numero, aviso: texto? }

    agente Mostrador {
        estado filas = []
        estado recordado atendidos = 0

        frenos {
            precios: solo_precios(filas)
            prohibido: ["descuento", "fiado"]
            largo: 300
            reserva: "Eso te lo confirma una persona. Ya te paso con alguien."
            consultas_por_dia: 200
        }

        al recibir CargarLista como c {
            filas = c.filas
        }

        al recibir Consulta como c {
            atendidos += 1
            sea instrucciones = """
                Atendés el mostrador de un almacén. Contestá en castellano rioplatense, corto
                y amable. Usá SOLO los precios de esta lista. Si piden algo que no está,
                decí que no lo trabajamos. Si dice SIN STOCK, avisá que ahora no hay.

                LISTA DE PRECIOS:
                {lista_en_texto(filas)}
            """
            intentar {
                sea dicho = consultar_ia(instrucciones, c.pregunta, c.sin_ia)
                responder Atencion { respuesta: dicho, numero: atendidos }
            } si falla motivo {
                responder Atencion { respuesta: c.sin_ia, numero: atendidos, aviso: motivo }
            }
        }
    }

    funcion solo_precios(tabla) {
        var importes = []
        para fila en tabla {
            importes = agregar(importes, fila.precio)
        }
        devolver importes
    }

    funcion renglon_de(fila) {
        si fila.stock == 0 {
            devolver "{fila.producto}: {pesos(fila.precio)} - SIN STOCK"
        }
        devolver "{fila.producto}: {pesos(fila.precio)}"
    }

    funcion lista_en_texto(tabla) {
        var renglones = []
        para fila en tabla {
            renglones = agregar(renglones, "- " + renglon_de(fila))
        }
        devolver unir(renglones, "\n")
    }

    # En minúscula y sin tildes, para que "AZUCAR" y "azúcar" sean lo mismo al buscar.
    funcion llano(t) {
        var r = minusculas(t)
        para con, sin en { "á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u" } {
            r = reemplazar(r, con, sin)
        }
        devolver r
    }

    funcion buscar_en_lista(tabla, pregunta) {
        para fila en tabla {
            sea palabra = llano(partir(fila.producto, " ")[0])
            si tiene(llano(pregunta), palabra) {
                devolver renglon_de(fila)
            }
        }
        devolver "Eso no lo encuentro en la lista. Probá con el nombre del producto."
    }

    # Antes de atender, mira que la planilla tenga lo que el programa necesita. Si algo
    # está mal, lo dice con el nombre del producto y el programa no sigue.
    funcion revisar_lista(tabla) {
        sea arreglo = "Corregilo en Excel, guardá de nuevo como CSV y volvé a correr."
        si largo(tabla) == 0 {
            fallar "precios.csv no tiene productos debajo de los títulos. {arreglo}"
        }
        var cuenta = 0
        para fila en tabla {
            cuenta += 1
            para titulo en ["producto", "precio", "stock"] {
                si no tiene(fila, titulo) {
                    sea hay = unir(claves(fila), ";")
                    sea va = "La primera fila tiene que decir producto;precio;stock, en minúscula"
                    sea falta = "A precios.csv le falta la columna '{titulo}'"
                    fallar "{falta}. {va}, y dice: {hay}. {arreglo}"
                }
            }
            sea cual = "En precios.csv, el producto {cuenta} ({fila.producto})"
            si tipo(fila.precio) != "numero" {
                fallar "{cual} no tiene el precio en números: dice \"{fila.precio}\". {arreglo}"
            }
            si tipo(fila.stock) != "numero" {
                fallar "{cual} no tiene el stock en números (si no hay, va 0). {arreglo}"
            }
        }
    }

    # LO NUEVO: un renglón por consulta, con la fecha y la hora, al final del archivo.
    funcion anotar(pregunta, respuesta) {
        agregar_a_archivo("consultas_atendidas.txt", "{ahora()} | {pregunta} | {respuesta}")
    }

    funcion charlar(tabla) {
        var consultas = 0
        mientras verdadero {
            sea dicho = leer("Cliente:", "chau")
            si dicho == "" {
                continuar
            }
            si minusculas(dicho) == "chau" {
                romper
            }
            sea atencion = preguntar Consulta {
                pregunta: dicho, sin_ia: buscar_en_lista(tabla, dicho),
            } a Mostrador
            mostrar("Mostrador: {atencion.respuesta}")
            si atencion.aviso != nada {
                mostrar("   (la IA no contestó y busqué en la lista. Motivo: {atencion.aviso})")
            }
            # LO NUEVO: se anota después de contestar.
            anotar(dicho, atencion.respuesta)
            consultas += 1
        }
        devolver consultas
    }

    sea precios = leer_tabla("precios.csv")
    revisar_lista(precios)
    enviar CargarLista { filas: precios } a Mostrador
    mostrar("Mostrador: cargué {largo(precios)} productos de precios.csv.")
    mostrar("Escribí tu consulta y apretá Enter. Para terminar, escribí chau.")
    sea atendidas = charlar(precios)
    mostrar("Hasta luego. En esta charla atendí {atendidas} consulta(s).")

    # (con 'probar' no se escribe el archivo de verdad: lo anotado se descarta al terminar)
    prueba "cada consulta queda anotada" {
        enviar CargarLista { filas: precios } a Mostrador
        simular_teclado(["arroz"])
        asegurar charlar(precios) == 1
        sea anotado = leer_archivo("consultas_atendidas.txt")
        asegurar tiene(anotado, "01/01/2025 12:00 | arroz | Arroz 1 kg: $ 1.800,00")
    }

Después de charlar un rato, abrí `mate\curso\consultas_atendidas.txt` con el Bloc de
notas: ahí están todas las consultas.

## Y ahora

Terminaste el curso. Para seguir:

- `python mate\mate.py ayuda` muestra todas las órdenes, y `python mate\mate.py ayuda si`
  (o cualquier otra palabra) explica esa palabra con un ejemplo.
- En `mate\ejemplos` hay programas más largos, comentados renglón por renglón.
- `mate\README.md` tiene todo Mate, tema por tema.
- `python mate\mate.py guia` imprime una página con todo el lenguaje para pegarle a un
  asistente de IA (Claude, por ejemplo) antes de pedirle que te escriba un programa.
