# Clase 6: Que el programa te pregunte

## Qué vas a lograr

Vas a charlar con tu programa: te pregunta, escribís, te contesta, y así hasta que
escribas `chau`. Es la base del mostrador de las últimas clases.

## El programa

Está en `mate\curso\clase_06_teclado.mate`:

    # Clase 6: que el programa te pregunte.
    # leer() muestra una pregunta y espera que escribas algo y aprietes Enter.

    sea precio = 3500

    funcion atender() {
        var pedidos = 0
        # 'mientras verdadero' repite sin parar: se sale con 'romper'.
        mientras verdadero {
            # El segundo valor ("chau") es lo que se "escribe" cuando no hay teclado, por
            # ejemplo al correr las pruebas: así el programa nunca se queda esperando.
            sea dicho = leer("¿Cuántos paquetes de yerba?", "chau")
            si minusculas(dicho) == "chau" {
                romper
            }
            # leer() siempre devuelve un texto. numero() lo pasa a número, y si no puede,
            # falla: con 'intentar' esa falla se ataja en vez de cortar el programa.
            intentar {
                sea cantidad = numero(dicho)
                mostrar("{cantidad} paquetes salen {pesos(precio * cantidad)}")
                pedidos += 1
            } si falla {
                mostrar("No entendí \"{dicho}\". Escribí un número, por ejemplo 3.")
            }
        }
        devolver pedidos
    }

    mostrar("Mostrador de yerba. Para terminar, escribí chau.")
    sea atendidos = atender()
    mostrar("Atendí {atendidos} pedido(s). ¡Hasta luego!")

    # En una prueba nadie teclea: simular_teclado() dice qué se "escribe" en cada leer().
    prueba "cuenta solo los pedidos que entendió" {
        simular_teclado(["2", "muchos", "5", "chau"])
        asegurar atender() == 2
    }

- `leer("pregunta", "chau")` muestra la pregunta y espera que escribas y aprietes Enter.
  Devuelve lo escrito, **siempre como texto**.
- `numero(dicho)` pasa ese texto a número, para poder hacer cuentas. Entiende `3`, `3,5`
  y `1.500`.
- `mientras condición { ... }` repite mientras la condición se cumpla. Con
  `mientras verdadero` repite siempre, y se sale con `romper`.
- `intentar { ... } si falla { ... }` prueba hacer algo y, si falla, hace lo otro en vez
  de cortar el programa.
- `minusculas(dicho)` hace que valgan igual `chau`, `Chau` y `CHAU`.
- `\"` dentro de un texto es una comilla de verdad.

## Cómo se corre

    python mate\mate.py correr mate\curso\clase_06_teclado.mate

## Lo que tiene que salir

Depende de lo que escribas. Si contestás `2`, después `muchos` y después `chau`:

    Mostrador de yerba. Para terminar, escribí chau.
    ¿Cuántos paquetes de yerba? 2
    2 paquetes salen $ 7.000,00
    ¿Cuántos paquetes de yerba? muchos
    No entendí "muchos". Escribí un número, por ejemplo 3.
    ¿Cuántos paquetes de yerba? chau
    Atendí 1 pedido(s). ¡Hasta luego!

También podés terminar con `Ctrl+C` mientras el programa espera: Mate avisa que cortaste
y no muestra ningún error.

Con `probar` nadie tiene que escribir nada: lo "tecleado" sale de `simular_teclado`.

    python mate\mate.py probar mate\curso\clase_06_teclado.mate

    Mostrador de yerba. Para terminar, escribí chau.
    Atendí 0 pedido(s). ¡Hasta luego!
      ✓ cuenta solo los pedidos que entendió
          | 2 paquetes salen $ 7.000,00
          | No entendí "muchos". Escribí un número, por ejemplo 3.
          | 5 paquetes salen $ 17.500,00
    1 de 1 pruebas pasaron

(Lo que una prueba muestra en pantalla aparece debajo de su nombre, con una barra adelante.)

## El error más común

Hacer una cuenta con lo que devolvió `leer` sin pasarlo por `numero`:

    sea dicho = leer("¿Cuántos paquetes de yerba?", "2")
    mostrar(dicho * 3500)

Lo que escribe la persona es un texto, aunque sean números, y un texto no se multiplica:

    ¿Cuántos paquetes de yerba? 2
    mate\curso\clase_06_teclado.mate:2: error: no se puede hacer texto * numero
        2 | mostrar(dicho * 3500)

Se arregla con `numero(dicho) * 3500`.

## Ejercicio

Copiá el programa de la clase en tu archivo de práctica y cambialo para que, en vez de
contar los pedidos, sume los paquetes: al terminar tiene que decir cuántos paquetes se
pidieron en total y cuánta plata es. Cambiá también la prueba.

## Solución

También está en `mate\curso\clase_06_solucion.mate`.

    # Clase 6, ejercicio resuelto: al terminar dice cuántos paquetes se pidieron en total.

    sea precio = 3500

    funcion atender() {
        var paquetes = 0
        mientras verdadero {
            sea dicho = leer("¿Cuántos paquetes de yerba?", "chau")
            si minusculas(dicho) == "chau" {
                romper
            }
            intentar {
                sea cantidad = numero(dicho)
                mostrar("{cantidad} paquetes salen {pesos(precio * cantidad)}")
                paquetes += cantidad
            } si falla {
                mostrar("No entendí \"{dicho}\". Escribí un número, por ejemplo 3.")
            }
        }
        devolver paquetes
    }

    mostrar("Mostrador de yerba. Para terminar, escribí chau.")
    sea vendidos = atender()
    mostrar("En total pidieron {vendidos} paquetes: {pesos(precio * vendidos)}")

    prueba "suma los paquetes de todos los pedidos" {
        simular_teclado(["2", "muchos", "5", "chau"])
        asegurar atender() == 7
    }

Si contestás `2`, `5` y `chau`:

    Mostrador de yerba. Para terminar, escribí chau.
    ¿Cuántos paquetes de yerba? 2
    2 paquetes salen $ 7.000,00
    ¿Cuántos paquetes de yerba? 5
    5 paquetes salen $ 17.500,00
    ¿Cuántos paquetes de yerba? chau
    En total pidieron 7 paquetes: $ 24.500,00

Siguiente: clase 7, tu lista de precios de Excel (`python mate\mate.py curso 7`).
