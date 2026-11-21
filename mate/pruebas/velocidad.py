"""Medidor de velocidad de Mate: corre varios programas típicos y muestra cuánto tardan.

No es una prueba (pytest no lo levanta): es para comparar el intérprete antes y después de
un cambio. No toca la red ni escribe ningún archivo.

    python mate\\pruebas\\velocidad.py                    (mide el mate.py de esta carpeta)
    python mate\\pruebas\\velocidad.py --mate=otro.py     (mide otra copia del intérprete)
    python mate\\pruebas\\velocidad.py --vueltas=5        (cada programa corre 5 veces)
    python mate\\pruebas\\velocidad.py --contra=otro.py   (mide las dos copias y compara)

De cada programa se muestra la corrida más rápida: es la que menos ruido tiene de lo demás
que esté haciendo la computadora. Los tiempos cambian de una máquina a otra; lo que sirve es
comparar dos copias de mate.py en la misma máquina y en el mismo momento (--contra).
"""

import importlib.util
import pathlib
import sys
import time

AQUI = pathlib.Path(__file__).resolve().parent

# Cada programa termina mostrando un resultado: así se comprueba, además, que las dos copias
# del intérprete calculan lo mismo.
PROGRAMAS = {
    "bucle con cuentas": """
        var total = 0
        var i = 0
        mientras i < 200000 {
            si i % 3 == 0 {
                total = total + i * 2
            } sino {
                total = total - 1
            }
            i += 1
        }
        mostrar(total)
    """,
    "llamadas a funciones": """
        funcion fib(n) {
            si n < 2 {
                devolver n
            }
            devolver fib(n - 1) + fib(n - 2)
        }
        funcion doble(x) { devolver x * 2 }
        var suma = 0
        para i en rango(30000) {
            suma = suma + doble(i)
        }
        mostrar(fib(21), suma)
    """,
    "listas y mapas": """
        var cuadrados = []
        para i en rango(3000) {
            cuadrados = agregar(cuadrados, i * i)
        }
        var cuenta = {}
        para i, c en cuadrados {
            sea clave = texto(c % 10)
            cuenta[clave] = obtener(cuenta, clave, 0) + 1
        }
        var total = 0
        para vuelta en rango(20) {
            para c en cuadrados {
                total = total + c % 7
            }
        }
        sea fichas = [{ nombre: "yerba", precio: 3500 }, { nombre: "azucar", precio: 1200 }]
        var caro = 0
        para vuelta en rango(20000) {
            para f en fichas {
                si f.precio > caro {
                    caro = f.precio
                }
            }
        }
        mostrar(total, cuenta["9"], largo(ordenar(cuadrados)), caro)
    """,
    "textos": """
        var partes = []
        para i en rango(20000) {
            sea renglon = "Cliente {i}: debe {pesos(i * 10, 0)}"
            si termina_con(renglon, "0") y tiene(renglon, "debe") {
                partes = agregar(partes, mayusculas(porcion(renglon, 0, 9)))
            }
        }
        sea todo = unir(partes, ", ")
        mostrar(largo(todo), largo(partir(todo, ", ")), reemplazar(porcion(todo, 0, 20), "C", "c"))
    """,
    "mensajes entre agentes": """
        mensaje Sumar { a: numero, b: numero }
        mensaje Resultado { valor: numero }
        mensaje Anotar { valor: numero }
        mensaje Cuanto {}

        agente Calculadora {
            estado hechas = 0
            al recibir Sumar como s {
                hechas += 1
                responder Resultado { valor: s.a + s.b }
            }
        }

        agente Libreta {
            estado total = 0
            al recibir Anotar como a {
                sea r = preguntar Sumar { a: total, b: a.valor } a Calculadora
                total = r.valor
            }
            al recibir Cuanto {
                responder total
            }
        }

        para i en rango(8000) {
            enviar Anotar { valor: i } a Libreta
        }
        mostrar(preguntar Cuanto {} a Libreta)
    """,
}


def cargar(ruta):
    """Levanta una copia de mate.py desde esa ruta, sin mezclarla con otra ya cargada."""
    ruta = pathlib.Path(ruta).resolve()
    if not ruta.is_file():
        sys.exit(f"no encuentro {ruta}")
    nombre = f"mate_medido_{abs(hash(str(ruta)))}"
    spec = importlib.util.spec_from_file_location(nombre, ruta)
    modulo = importlib.util.module_from_spec(spec)
    sys.modules[nombre] = modulo
    spec.loader.exec_module(modulo)
    return modulo


def medir(mate, fuente, vueltas):
    """(segundos de la corrida más rápida, lo que mostró el programa)."""
    programa = mate.analizar(fuente)
    errores = mate.verificar(programa)
    if errores:
        sys.exit(f"un programa del medidor no pasa la revisión: {errores[0][1]}")
    mejor, mostrado = None, None
    for _ in range(vueltas):
        mostrado = []
        interprete = mate.Interprete(salida=mostrado.append)
        antes = time.perf_counter()
        interprete.correr(programa)
        tardo = time.perf_counter() - antes
        mejor = tardo if mejor is None else min(mejor, tardo)
    return mejor, mostrado


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    ruta, contra, vueltas = AQUI.parent / "mate.py", None, 3
    for a in argv:
        if a.startswith("--mate="):
            ruta = a.split("=", 1)[1]
        elif a.startswith("--contra="):
            contra = a.split("=", 1)[1]
        elif a.startswith("--vueltas=") and a.split("=", 1)[1].isdigit():
            vueltas = max(1, int(a.split("=", 1)[1]))
        else:
            sys.exit(f"no conozco '{a}'. Las opciones son --mate=archivo.py, "
                     "--contra=archivo.py y --vueltas=3")
    mate = cargar(ruta)
    otro = cargar(contra) if contra else None
    print(f"Mate {mate.VERSION} con Python {sys.version.split()[0]} "
          f"(la más rápida de {vueltas} corridas, en segundos)")
    if otro:
        print(f"  comparado con Mate {otro.VERSION} de {contra}")
        print(f"  {'programa':<26}{'el otro':>9}{'este':>9}   cuántas veces más rápido")
    total = total_otro = 0.0
    for nombre, fuente in PROGRAMAS.items():
        if otro:
            # Se alternan las corridas de una copia y de la otra: si la computadora se
            # pone lenta un rato, les toca a las dos.
            tardo = tardo_otro = None
            for _ in range(vueltas):
                t, mostrado = medir(otro, fuente, 1)
                tardo_otro = t if tardo_otro is None else min(tardo_otro, t)
                mostrado_otro = mostrado
                t, mostrado = medir(mate, fuente, 1)
                tardo = t if tardo is None else min(tardo, t)
            if mostrado != mostrado_otro:
                sys.exit(f"'{nombre}' no da lo mismo en las dos copias: {mostrado_otro} "
                         f"y {mostrado}")
            total_otro += tardo_otro
            total += tardo
            print(f"  {nombre:<26}{tardo_otro:>9.3f}{tardo:>9.3f}   {tardo_otro / tardo:.2f}")
        else:
            tardo, _ = medir(mate, fuente, vueltas)
            total += tardo
            print(f"  {nombre:<26}{tardo:>9.3f}")
    if otro:
        print(f"  {'en total':<26}{total_otro:>9.3f}{total:>9.3f}   {total_otro / total:.2f}")
    else:
        print(f"  {'en total':<26}{total:>9.3f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
