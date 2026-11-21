"""Pruebas del intérprete de Mate. Correr con: python3 -m pytest mate/pruebas -q"""

import pathlib
import re
import sys

import pytest

RAIZ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

import mate  # noqa: E402


def correr(fuente, traza=False):
    salida = []
    interprete = mate.Interprete(salida=salida.append, traza=traza)
    programa = mate.analizar(fuente)
    assert mate.verificar(programa) == []
    interprete.correr(programa)
    return salida, interprete


def falla(fuente):
    with pytest.raises(mate.ErrorMate) as info:
        correr(fuente)
    return info.value


def test_aritmetica_y_textos():
    salida, _ = correr('mostrar(1 + 2 * 3, 7 / 2, 6 / 2, 7 % 4, "a" + "b", "x={1 + 1}")')
    assert salida == ["7 3.5 3 3 ab x=2"]


def test_sea_es_fijo_y_var_cambia():
    assert correr("var x = 1\nx = x + 1\nmostrar(x)")[0] == ["2"]
    assert "es fijo" in falla("sea x = 1\nx = 2").mensaje


def test_sin_conversiones_implicitas():
    assert "texto + numero" in falla('mostrar("a" + 1)').mensaje
    assert "condición" in falla("si 1 { mostrar(1) }").mensaje
    assert correr("mostrar(1 == verdadero)")[0] == ["falso"]


def test_los_valores_no_se_comparten_al_modificar():
    salida, _ = correr(
        "sea a = { n: [1, 2] }\nvar b = a\nb.n[0] = 99\nmostrar(a.n[0], b.n[0])")
    assert salida == ["1 99"]


def test_funciones_recursion_y_bucles():
    salida, _ = correr("""
        funcion fact(n) {
            si n <= 1 { devolver 1 }
            devolver n * fact(n - 1)
        }
        var pares = []
        para i en rango(6) {
            si i % 2 == 0 { pares = agregar(pares, i) }
        }
        var n = 0
        mientras n < 3 { n = n + 1 }
        mostrar(fact(5), pares, n)
    """)
    assert salida == ["120 [0, 2, 4] 3"]


def test_errores_llevan_numero_de_linea():
    error = falla("sea a = 1\nsea b = [1]\nmostrar(b[3])")
    assert error.linea == 3 and "fuera de rango" in error.mensaje


def test_intentar_ataja_fallas():
    salida, _ = correr('intentar { fallar "ups" } si falla e { mostrar("atajé " + e) }')
    assert salida == ["atajé ups"]


AGENTES = """
mensaje Sumar { a: numero, b: numero }
mensaje Resultado { valor: numero }
mensaje Contar
mensaje Ping { nota: texto? }

agente Calculadora {
    estado usos = 0
    al recibir Sumar como s {
        usos = usos + 1
        responder Resultado { valor: s.a + s.b }
    }
    al recibir Contar { responder usos }
}
"""


def test_preguntar_devuelve_la_respuesta_y_el_estado_persiste():
    salida, _ = correr(AGENTES + """
        sea r = preguntar Sumar { a: 2, b: 3 } a Calculadora
        mostrar(r.valor, preguntar Contar {} a Calculadora)
    """)
    assert salida == ["5 1"]


def test_enviar_es_asincronico_y_responder_vuelve_al_remitente():
    salida, _ = correr(AGENTES + """
        mensaje Empezar
        agente Cliente {
            al recibir Empezar {
                enviar Sumar { a: 1, b: 1 } a Calculadora
                mostrar("pedido enviado")
            }
            al recibir Resultado como r { mostrar("llegó {r.valor}") }
        }
        enviar Empezar {} a Cliente
    """, traza=True)
    textos = [s for s in salida if not s.startswith("  ·")]
    assert textos == ["pedido enviado", "llegó 2"]
    assert "  · Calculadora → Cliente: Resultado { valor: 2 }" in salida


def test_contrato_de_mensajes_en_ejecucion():
    error = falla(AGENTES + "sea n = \"dos\"\nenviar Sumar { a: n, b: 1 } a Calculadora")
    assert "Sumar.a es de tipo numero y recibió texto" in error.mensaje
    assert correr(AGENTES + "mostrar(Ping {}.nota)")[0] == ["nada"]


def test_verificacion_estatica_de_contratos():
    programa = mate.analizar(AGENTES + """
        enviar Sumar { a: "x", c: 1 } a Calculadora
        enviar Ping {} a Calculadora
        enviar Fantasma {} a Calculadora
    """)
    textos = [t for _, t in mate.verificar(programa)]
    assert "Sumar.a es de tipo numero, no texto" in textos
    assert "Sumar no tiene un campo 'c'" in textos
    assert "a Sumar le falta el campo 'b'" in textos
    assert "Calculadora no sabe recibir 'Ping'" in textos
    assert "no existe el mensaje 'Fantasma'" in textos


def test_un_agente_no_toca_estado_ajeno():
    _, interprete = correr("""
        var global = 0
        mensaje Tocar
        agente Travieso { al recibir Tocar { global = 1 } }
        enviar Tocar {} a Travieso
    """)
    assert "no puede modificar 'global'" in interprete.errores_agentes[0]


def test_ciclo_de_preguntas_se_detecta():
    error = falla("""
        mensaje Ir
        agente A { al recibir Ir { responder preguntar Ir {} a B } }
        agente B { al recibir Ir { responder preguntar Ir {} a A } }
        preguntar Ir {} a A
    """)
    assert "ciclo de preguntas" in error.mensaje


def test_json_ida_y_vuelta():
    salida, _ = correr(AGENTES + """
        sea m = Sumar { a: 1, b: 2 }
        sea t = a_json(m)
        mostrar(t)
        mostrar(de_json(t) == m)
    """)
    assert salida == ['{"tipo": "Sumar", "campos": {"a": 1, "b": 2}}', "verdadero"]


@pytest.mark.parametrize("nombre", ["hola", "negociacion", "equipo", "mercado"])
def test_los_ejemplos_pasan_sus_pruebas(nombre, capsys):
    assert mate.main(["probar", str(RAIZ / "ejemplos" / f"{nombre}.mate")]) == 0
    assert "✗" not in capsys.readouterr().out


def test_crear_copias_con_estado_propio_y_nombre():
    salida, _ = correr(AGENTES + """
        sea otra = crear Calculadora llamado "B" { usos: 10 }
        sea tercera = crear Calculadora
        preguntar Sumar { a: 1, b: 1 } a otra
        mostrar(preguntar Contar {} a otra, preguntar Contar {} a Calculadora)
        mostrar(otra, tercera, otra == otra, otra == tercera)
    """)
    assert salida == ["11 0", "Calculadora B Calculadora#3 verdadero falso"]


def test_yo_es_la_copia_que_atiende():
    salida, _ = correr("""
        mensaje Quien
        agente Eco { al recibir Quien { responder yo } }
        sea copia = crear Eco llamado "dos"
        mostrar(preguntar Quien {} a copia, preguntar Quien {} a Eco)
    """)
    assert salida == ["Eco dos Eco"]


def test_crear_se_verifica_antes_de_correr():
    programa = mate.analizar(AGENTES + "crear Calculadora { uso: 1 }\ncrear Nadie")
    textos = [t for _, t in mate.verificar(programa)]
    assert textos == ["Calculadora no tiene un estado 'uso'", "no existe el agente 'Nadie'"]


def test_el_estado_inicial_puede_usar_valores_declarados_antes():
    salida, _ = correr("""
        mensaje Ver
        sea base = 7
        agente A {
            estado n = base * 2
            al recibir Ver { responder n }
        }
        mostrar(preguntar Ver {} a A)
    """)
    assert salida == ["14"]


def test_usar_trae_declaraciones_pero_no_ejecuta(tmp_path):
    (tmp_path / "lib.mate").write_text(
        'usar "principal.mate"\n'  # los ciclos no rompen
        "mensaje Hola { quien: texto }\n"
        "sea saludo = \"buenas\"\n"
        "funcion doble(n) { devolver n * 2 }\n"
        'mostrar("no debería verse")\n'
        'prueba "no debería correr" { fallar "ups" }\n',
        encoding="utf-8",
    )
    principal = tmp_path / "principal.mate"
    principal.write_text(
        'usar "lib.mate"\nusar "lib.mate"\n'
        'mostrar(saludo, doble(4), Hola { quien: "vos" }.quien)\n',
        encoding="utf-8",
    )
    salida = []
    interprete = mate.Interprete(salida=salida.append)
    programa = mate.analizar(principal.read_text(encoding="utf-8"), str(principal))
    assert interprete.correr(programa, pruebas=True) == []
    assert salida == ["buenas 8 vos"]


def test_errores_en_archivos_usados_dicen_el_archivo(tmp_path, capsys):
    (tmp_path / "lib.mate").write_text("sea x = 1\nsea z = x + \"a\"\n", encoding="utf-8")
    principal = tmp_path / "principal.mate"
    principal.write_text('usar "lib.mate"\nusar "falta.mate"\n', encoding="utf-8")
    assert mate.main(["correr", str(principal)]) == 1
    assert "principal.mate:2: error: no pude abrir 'falta.mate'" in capsys.readouterr().err
    principal.write_text('usar "lib.mate"\n', encoding="utf-8")
    assert mate.main(["correr", str(principal)]) == 1
    assert "lib.mate:2: error: no se puede hacer numero + texto" in capsys.readouterr().err


# ── Mejora 1: la salida exacta de los ejemplos queda fijada ──
# Si una mejora cambia esta salida A PROPÓSITO, se actualiza acá, a la vista, en el mismo cambio.

SALIDAS_ESPERADAS = {
    ("catalogo", False): (0, (
        "Esto solo se ve si corrés catalogo.mate directamente.\n"
    )),
    ("catalogo", True): (0, (
        "Esto solo se ve si corrés catalogo.mate directamente.\n"
    )),
    ("equipo", False): (0, (
        "Listo: VENTAS: subieron 12%; yerba es lo más vendido\n"
        "Listo: STOCK: quedan 40 cajas\n"
    )),
    ("equipo", True): (0, (
        "  · (programa) → Coordinador: Encargo { tema: \"ventas\" }\n"
        "  · (programa) → Coordinador: Encargo { tema: \"stock\" }\n"
        "  · Coordinador → Investigador: Investigar { tema: \"ventas\" }\n"
        "  · Coordinador → Investigador: Investigar { tema: \"stock\" }\n"
        "  · Investigador → Coordinador: Hallazgos { tema: \"ventas\", datos: [\"subieron 12%\", \"yerba es lo más vendido\"] }\n"
        "  · Investigador → Coordinador: Hallazgos { tema: \"stock\", datos: [\"quedan 40 cajas\"] }\n"
        "  · Coordinador → Redactor: Redactar { tema: \"ventas\", datos: [\"subieron 12%\", \"yerba es lo más vendido\"] }\n"
        "  · Coordinador → Redactor: Redactar { tema: \"stock\", datos: [\"quedan 40 cajas\"] }\n"
        "  · Redactor → Coordinador: Borrador { texto: \"VENTAS: subieron 12%; yerba es lo más vendido\" }\n"
        "Listo: VENTAS: subieron 12%; yerba es lo más vendido\n"
        "  · Redactor → Coordinador: Borrador { texto: \"STOCK: quedan 40 cajas\" }\n"
        "Listo: STOCK: quedan 40 cajas\n"
    )),
    ("hola", False): (0, (
        "Hola desde Mate 2.0\n"
        "Subtotal: 8200 | con IVA: 9922\n"
    )),
    ("hola", True): (0, (
        "Hola desde Mate 2.0\n"
        "Subtotal: 8200 | con IVA: 9922\n"
    )),
    ("mercado", False): (0, (
        "Vendedor Norte cotiza 33250\n"
        "Vendedor Sur cotiza 33000\n"
        "Vendedor Centro cotiza 35000\n"
        "Compro 10 de yerba a Vendedor Sur por 33000\n"
        "Vendedor Norte cotiza 4560\n"
        "Vendedor Sur no puede: no vendo azucar\n"
        "Vendedor Centro cotiza 4800\n"
        "Compro 4 de azucar a Vendedor Norte por 4560\n"
    )),
    ("mercado", True): (0, (
        "  · (programa) → Comprador: Comprar { producto: \"yerba\", cantidad: 10, vendedores: [<agente Vendedor Norte>, <agente Vendedor Sur>, <agente Vendedor Centro>] }\n"
        "  · Comprador pregunta a Vendedor Norte: Pedido { producto: \"yerba\", cantidad: 10 }\n"
        "  · Vendedor Norte responde a Comprador: Cotizacion { vendedor: <agente Vendedor Norte>, producto: \"yerba\", total: 33250 }\n"
        "Vendedor Norte cotiza 33250\n"
        "  · Comprador pregunta a Vendedor Sur: Pedido { producto: \"yerba\", cantidad: 10 }\n"
        "  · Vendedor Sur responde a Comprador: Cotizacion { vendedor: <agente Vendedor Sur>, producto: \"yerba\", total: 33000 }\n"
        "Vendedor Sur cotiza 33000\n"
        "  · Comprador pregunta a Vendedor Centro: Pedido { producto: \"yerba\", cantidad: 10 }\n"
        "  · Vendedor Centro responde a Comprador: Cotizacion { vendedor: <agente Vendedor Centro>, producto: \"yerba\", total: 35000 }\n"
        "Vendedor Centro cotiza 35000\n"
        "Compro 10 de yerba a Vendedor Sur por 33000\n"
        "  · (programa) → Comprador: Comprar { producto: \"azucar\", cantidad: 4, vendedores: [<agente Vendedor Norte>, <agente Vendedor Sur>, <agente Vendedor Centro>] }\n"
        "  · Comprador pregunta a Vendedor Norte: Pedido { producto: \"azucar\", cantidad: 4 }\n"
        "  · Vendedor Norte responde a Comprador: Cotizacion { vendedor: <agente Vendedor Norte>, producto: \"azucar\", total: 4560 }\n"
        "Vendedor Norte cotiza 4560\n"
        "  · Comprador pregunta a Vendedor Sur: Pedido { producto: \"azucar\", cantidad: 4 }\n"
        "Vendedor Sur no puede: no vendo azucar\n"
        "  · Comprador pregunta a Vendedor Centro: Pedido { producto: \"azucar\", cantidad: 4 }\n"
        "  · Vendedor Centro responde a Comprador: Cotizacion { vendedor: <agente Vendedor Centro>, producto: \"azucar\", total: 4800 }\n"
        "Vendedor Centro cotiza 4800\n"
        "Compro 4 de azucar a Vendedor Norte por 4560\n"
    )),
    ("negociacion", False): (0, (
        "Me cotizaron 10500 por 3 de yerba\n"
        "Cerramos en 9600.\n"
    )),
    ("negociacion", True): (0, (
        "  · (programa) → Comprador: Iniciar { producto: \"yerba\", cantidad: 3, presupuesto: 9600 }\n"
        "  · Comprador pregunta a Vendedor: Pedido { producto: \"yerba\", cantidad: 3 }\n"
        "  · Vendedor responde a Comprador: Cotizacion { producto: \"yerba\", total: 10500 }\n"
        "Me cotizaron 10500 por 3 de yerba\n"
        "  · Comprador pregunta a Vendedor: Contraoferta { producto: \"yerba\", total: 9600 }\n"
        "  · Vendedor responde a Comprador: Trato { aceptado: verdadero, total: 9600 }\n"
        "Cerramos en 9600.\n"
    )),
}


@pytest.mark.parametrize("nombre,traza", sorted(SALIDAS_ESPERADAS))
def test_la_salida_de_los_ejemplos_no_cambia(nombre, traza, capsys):
    codigo_esperado, salida_esperada = SALIDAS_ESPERADAS[(nombre, traza)]
    argumentos = ["correr", str(RAIZ / "ejemplos" / f"{nombre}.mate")] + (["--traza"] if traza else [])
    codigo = mate.main(argumentos)
    assert capsys.readouterr().out == salida_esperada
    assert codigo == codigo_esperado


# ── Tanda 1: nunca un error interno en inglés ──

import os  # noqa: E402
import subprocess  # noqa: E402


def por_main(tmp_path, capsys, fuente, *opciones, orden="correr"):
    """Escribe el programa en un archivo y lo corre como lo haría el dueño."""
    archivo = tmp_path / "programa.mate"
    archivo.write_text(fuente, encoding="utf-8")
    capsys.readouterr()
    codigo = mate.main([orden, str(archivo), *opciones])
    capturado = capsys.readouterr()
    return codigo, capturado.out, capturado.err


# Mejora 2: red de seguridad

def test_demasiados_parentesis_no_muestra_un_error_de_python(tmp_path, capsys):
    codigo, _, err = por_main(tmp_path, capsys, "sea x = " + "(" * 150 + "1" + ")" * 150)
    assert codigo == 1
    assert "demasiados niveles anidados" in err and "Traceback" not in err
    assert len(err.strip().splitlines()) == 1


def test_un_error_interno_se_cuenta_en_espanol(tmp_path, capsys, monkeypatch):
    def roto(self, s, env):
        raise RuntimeError("algo se rompió adentro")
    monkeypatch.setattr(mate.Interprete, "_ejecutar", roto)
    codigo, _, err = por_main(tmp_path, capsys, "sea a = 1\nmostrar(a)")
    assert codigo == 1
    assert "error interno de Mate (no es culpa tuya): RuntimeError: algo se rompió adentro" in err
    assert "programa.mate:1" in err and "--depurar" in err and "Traceback" not in err
    with pytest.raises(RuntimeError):
        por_main(tmp_path, capsys, "mostrar(1)", "--depurar")


def test_ctrl_c_dice_en_que_linea_estaba(tmp_path, capsys, monkeypatch):
    def cortar(self, s, env):
        raise KeyboardInterrupt
    monkeypatch.setattr(mate.Interprete, "_ejecutar", cortar)
    codigo, _, err = por_main(tmp_path, capsys, "sea a = 1\n")
    assert codigo == 130
    assert "programa.mate:1: cortado con Ctrl+C mientras corría esta línea" in err


# Mejora 3: archivos del Bloc de notas

@pytest.mark.parametrize("codificacion", ["cp1252", "utf-16", "utf-8-sig", "utf-8"])
def test_lee_archivos_en_las_codificaciones_del_bloc_de_notas(codificacion, tmp_path, capsys):
    (tmp_path / "lib.mate").write_bytes('sea saludo = "ñandú"\r\n'.encode(codificacion))
    principal = tmp_path / "principal.mate"
    principal.write_bytes('usar "lib.mate"\r\nmostrar("año", saludo)\r\n'.encode(codificacion))
    assert mate.main(["correr", str(principal)]) == 0
    assert capsys.readouterr().out == "año ñandú\n"


def test_archivo_ilegible_explica_como_guardarlo(tmp_path, capsys):
    archivo = tmp_path / "raro.mate"
    archivo.write_bytes(b'mostrar("\x81\x8d")\n')  # ni UTF-8 ni ANSI
    assert mate.main(["correr", str(archivo)]) == 1
    assert "Guardar como > Codificación: UTF-8" in capsys.readouterr().err


# Mejora 4: consolas que no son UTF-8

@pytest.mark.parametrize("codificacion", ["cp1252", "ascii"])
def test_consola_que_no_es_utf8_no_rompe(codificacion):
    entorno = dict(os.environ, PYTHONIOENCODING=codificacion)

    def correr_mate(*args):
        return subprocess.run([sys.executable, str(RAIZ / "mate.py"), *args],
                              env=entorno, capture_output=True)

    r = correr_mate("probar", str(RAIZ / "ejemplos" / "hola.mate"))
    assert r.returncode == 0 and r.stderr == b""
    assert b"  OK el total suma precio por cantidad" in r.stdout
    r = correr_mate("correr", str(RAIZ / "ejemplos" / "equipo.mate"), "--traza")
    assert r.returncode == 0 and r.stderr == b""
    assert b'  - (programa) -> Coordinador: Encargo { tema: "ventas" }' in r.stdout


def test_simbolo_usa_el_reemplazo_solo_si_hace_falta(monkeypatch):
    class Consola:
        encoding = "ascii"
    assert mate.simbolo("✓", "OK") == "✓"
    monkeypatch.setattr(mate.sys, "stdout", Consola())
    assert mate.simbolo("✓", "OK") == "OK"


# Mejora 5: devolver y responder fuera de lugar

def test_devolver_y_responder_sueltos_se_avisan_antes_de_correr(tmp_path, capsys):
    codigo, out, err = por_main(tmp_path, capsys, 'mostrar("no corre")\ndevolver 5')
    assert codigo == 1 and out == ""
    assert "programa.mate:2: error: 'devolver' solo va dentro de una función" in err
    codigo, _, err = por_main(tmp_path, capsys, "responder 5", orden="verificar")
    assert codigo == 1 and "programa.mate:1: error: 'responder' solo va dentro de 'al recibir'" in err
    with pytest.raises(mate.ErrorMate, match="responder"):
        mate.analizar("funcion f() { responder 1 }")
    with pytest.raises(mate.ErrorMate, match="devolver"):
        mate.analizar('prueba "x" { devolver 1 }')


def test_devolver_y_responder_en_su_lugar_siguen_andando():
    salida, _ = correr("""
        mensaje Doble { n: numero }
        mensaje Callar
        agente A {
            funcion contestar(n) { responder n * 2 }
            al recibir Doble como d { contestar(d.n) }
            al recibir Callar { devolver }
        }
        funcion f() { devolver 7 }
        enviar Callar {} a A
        mostrar(f(), preguntar Doble { n: 4 } a A)
    """)
    assert salida == ["7 8"]


def test_red_para_devolver_suelto_si_el_analisis_no_lo_vio():
    programa = [("devolver", mate.Linea(3), None)]
    with pytest.raises(mate.ErrorMate, match="devolver") as info:
        mate.Interprete().correr(programa)
    assert info.value.linea == 3


# Mejora 6: funciones incluidas

def test_las_funciones_incluidas_fallan_en_espanol():
    assert correr('mostrar(partir("abc", ""), partir("a-b", "-"))')[0] == ['["a", "b", "c"] ["a", "b"]']
    error = falla("sea a = 1\nmostrar(redondear(2.5, 1.5))")
    assert error.linea == 2 and "cantidad entera de decimales" in error.mensaje
    assert "cantidad entera de decimales" in falla("redondear(2.5, -1)").mensaje
    assert falla("redondear(1, 2, 3)").mensaje == "redondear() lleva 1 o 2 valores y recibió 3"
    assert falla("largo()").mensaje == "largo() lleva 1 valor y recibió 0"
    assert falla("tiene(1)").mensaje == "tiene() lleva 2 valores y recibió 1"
    assert correr("mostrar(redondear(2.567, 2), redondear(7.4))")[0] == ["2.57 7"]


def test_un_error_de_python_dentro_de_una_funcion_incluida_se_traduce():
    with pytest.raises(mate.ErrorMate, match=r"ordenar\(\)"):
        correr("ordenar([1, \"a\"])")
    with pytest.raises(mate.ErrorMate, match=r"mostrar\(\): no pude hacer eso"):
        mate.Interprete(salida=lambda t: int("x")).correr(mate.analizar("mostrar(1)"))


# Mejora 7: asignar a algo que no es una variable

@pytest.mark.parametrize("fuente", [
    "[[1]][0][0] = 2",
    "sea a = [1]\nsea b = [2]\n(a + b)[0] = 1",
    "mensaje M { a: numero }\nM { a: 1 }.a = 2",
    "funcion f() { devolver { a: 1 } }\nf().a = 2",
    "5 = 3",
])
def test_asignar_a_algo_que_no_es_variable(fuente):
    with pytest.raises(mate.ErrorMate) as info:
        mate.analizar(fuente)
    assert "solo se puede asignar a una variable" in info.value.mensaje
    assert info.value.linea == len(fuente.splitlines())


def test_las_asignaciones_validas_siguen_igual():
    salida, _ = correr("""
        var x = 1
        var m = { a: [{ b: 0 }] }
        var l = [1, 2]
        x = 2
        m.a[0].b = 1
        m.c = 3
        l[0] = 5
        mostrar(x, m, l)
    """)
    assert salida == ['2 {a: [{b: 1}], c: 3} [5, 2]']
    with pytest.raises(mate.ErrorMate, match="solo se puede asignar"):
        mate.Interprete().asignar(("num", 1, 5), 1, mate.Entorno())


# Mejora 8: listas o mapas como clave

def test_claves_que_no_son_texto():
    assert correr("mostrar(tiene({a: 1}, [1]), tiene({a: 1}, {}), tiene({a: 1}, \"a\"))")[0] == [
        "falso falso verdadero"]
    error = falla("sea m = {a: 1}\nmostrar(m[[1]])")
    assert error.linea == 2 and error.mensaje == "las claves de un mapa son textos, no lista"
    assert falla("var m = {a: 1}\nm[1] = 2").mensaje == "las claves de un mapa son textos, no numero"
    assert "clave" in falla('sea m = {a: 1}\nmostrar(m["b"])').mensaje
    salida, _ = correr(AGENTES + r"""
        mostrar(de_json("\{\"tipo\": [1], \"campos\": \{\}\}"))
        mostrar(de_json("\{\"agente\": \{\"x\": 1\}\}"))
        mostrar(de_json("\{\"agente\": \"Calculadora\"\}") == Calculadora)
    """)
    assert salida == ["{tipo: [1], campos: {}}", "{agente: {x: 1}}", "verdadero"]


# Mejora 9: números enormes, inf y nan

def test_numeros_enormes_no_rompen():
    grande = "var n = 1\npara i en rango(400) { n = n * 10 }\n"
    error = falla(grande + "mostrar(n * 1.5)")
    assert error.linea == 3 and error.mensaje == "el resultado es demasiado grande para calcularlo"
    assert "demasiado grande" in falla(grande + "mostrar(n / 3)").mensaje
    assert "demasiado grande" in falla(
        "var f = 1.5\npara i en rango(400) { f = f * 10 }").mensaje
    assert correr(grande + "mostrar(n == n + 0, n > 1)")[0] == ["verdadero verdadero"]  # exactos sí
    assert "demasiado grande" in falla("sea x = " + "9" * 400 + ".5").mensaje


def test_inf_y_nan_no_se_cuelan():
    assert falla('numero("nan")').mensaje == "'nan' no es un número"
    assert falla('numero("inf")').mensaje == "'inf' no es un número"
    assert falla('numero("1e999")').mensaje == "'1e999' no es un número"
    assert falla('de_json("[NaN]")').mensaje == "el JSON trae un número que no es válido"
    assert falla('de_json("[1e999]")').mensaje == "el JSON trae un número que no es válido"
    assert falla('de_json("-Infinity")').mensaje == "el JSON trae un número que no es válido"
    interprete = mate.Interprete()
    interprete.glob.definir("raro", float("inf"))
    with pytest.raises(mate.ErrorMate, match="ese número no se puede pasar a JSON"):
        interprete.correr(mate.analizar("a_json([raro])"))


# Mejora 10: lo que se pega desde Word y costumbres de otros lenguajes

def test_comillas_de_word_y_espacios_invisibles():
    assert correr("sea x = “hola”\nmostrar(x)")[0] == ["hola"]
    assert correr("sea x = „hola“\nmostrar(x)")[0] == ["hola"]
    assert correr("sea x = 1​\nmostrar(x)﻿")[0] == ["1"]
    assert correr('mostrar("dijo “che” y se fue")')[0] == ["dijo “che” y se fue"]  # adentro no se tocan


@pytest.mark.parametrize("fuente,pista", [
    ("sea a = 1;", "en Mate no hace falta el punto y coma: borralo"),
    ('mostrar("hola', "a este texto le falta la comilla de cierre (los textos van en un solo renglón)"),
    ("mostrar(“hola)", "a este texto le falta la comilla de cierre (los textos van en un solo renglón)"),
    ("mostrar('hola')", 'los textos van entre comillas dobles: "así"'),
    ("mostrar(‘hola’)", 'los textos van entre comillas dobles: "así"'),
    ("si a && b { }", "en Mate 'y' se escribe con la palabra: a y b"),
    ("si a || b { }", "en Mate 'o' se escribe con la palabra: a o b"),
    ("si !a { }", "en Mate 'no' se escribe con la palabra: no a"),
    ("sea a = 1 // uno", "los comentarios empiezan con #"),
    ("sea a = 1 @ 2", "carácter inesperado: '@'"),
])
def test_simbolos_de_otros_lenguajes_explican_como_se_escribe(fuente, pista):
    with pytest.raises(mate.ErrorMate) as info:
        mate.analizar("sea z = 0\n" + fuente)
    assert info.value.mensaje == pista and info.value.linea == 2


def test_distinto_y_dividir_siguen_andando():
    assert correr("mostrar(1 != 2, 8 / 2 / 2)")[0] == ["verdadero 2"]


# Mejora 11: línea de comandos

def test_ordenes_y_opciones_mal_escritas(tmp_path, capsys):
    ok = tmp_path / "ok.mate"
    ok.write_text('mostrar("corrió")', encoding="utf-8")
    capsys.readouterr()

    def probar_main(*args):
        codigo = mate.main([str(a) for a in args])
        capturado = capsys.readouterr()
        return codigo, capturado.out, capturado.err

    assert probar_main("correr", ok, "--trasa") == (
        2, "", "no conozco la opción --trasa, ¿quisiste decir --traza?\n")
    assert probar_main("corer", ok) == (2, "", "no conozco la orden 'corer', ¿quisiste decir 'correr'?\n")
    codigo, out, err = probar_main("zzz", ok)
    assert codigo == 2 and out == "" and "no conozco la orden 'zzz'" in err
    assert probar_main("CORRER", ok) == (0, "corrió\n", "")
    assert probar_main(ok) == (0, "corrió\n", "")
    assert probar_main("correr", tmp_path / "ok") == (0, "corrió\n", "")
    assert probar_main("correr", ok, "--sin-limite", "--depurar") == (0, "corrió\n", "")
    codigo, out, err = probar_main("correr", ok, ok)
    assert codigo == 2 and out == "" and "'correr' lleva un solo archivo" in err
    codigo, out, err = probar_main("probar")
    assert codigo == 2 and "a 'probar' le falta el archivo" in err


def test_version_y_ayuda(capsys):
    assert mate.main(["--version"]) == 0
    assert capsys.readouterr().out.startswith(f"Mate {mate.VERSION} (Python 3.")
    for argumentos, codigo in ((["ayuda"], 0), (["--ayuda"], 0), ([], 2)):
        assert mate.main(argumentos) == codigo
        out = capsys.readouterr().out
        assert "correr    archivo.mate" in out and "--traza" in out
        assert "hola.mate" in out and "Uso:" not in out


def test_archivo_que_no_esta_o_no_es(tmp_path, capsys):
    (tmp_path / "a.mate").write_text("mostrar(1)", encoding="utf-8")
    (tmp_path / "b.mate").write_text("mostrar(1)", encoding="utf-8")
    (tmp_path / "hola.mate.txt").write_text("mostrar(1)", encoding="utf-8")
    (tmp_path / "carpeta").mkdir()
    capsys.readouterr()

    assert mate.main(["correr", str(tmp_path / "nohay.mate")]) == 2
    err = capsys.readouterr().err
    assert f"no encuentro 'nohay.mate' en {tmp_path}" in err
    assert "archivos .mate que sí hay ahí: a.mate, b.mate" in err

    assert mate.main(["correr", str(tmp_path / "hola.mate")]) == 2
    err = capsys.readouterr().err
    assert "encontré hola.mate.txt: el Bloc de notas le agregó .txt" in err

    assert mate.main(["correr", str(tmp_path / "carpeta")]) == 2
    assert "es una carpeta, no un archivo .mate" in capsys.readouterr().err

    assert mate.main(["correr", str(tmp_path / "no" / "esta.mate")]) == 2
    assert "esa carpeta no existe" in capsys.readouterr().err


def test_no_poder_abrir_no_muestra_texto_en_ingles(tmp_path, capsys, monkeypatch):
    archivo = tmp_path / "a.mate"
    archivo.write_text("mostrar(1)", encoding="utf-8")

    def sin_permiso(ruta):
        raise PermissionError(13, "Permission denied")
    monkeypatch.setattr(mate, "leer_fuente", sin_permiso)
    assert mate.main(["correr", str(archivo)]) == 2
    err = capsys.readouterr().err
    assert "no pude abrir" in err and "Permission" not in err


# Mejora 12: freno para programas que nunca terminan

def test_bucle_que_nunca_termina_se_corta(tmp_path, capsys, monkeypatch):
    monkeypatch.setattr(mate, "MAX_PASOS", 1000)
    codigo, _, err = por_main(tmp_path, capsys, "var i = 0\nmientras i < 3 { }")
    assert codigo == 1
    assert "programa.mate:2: error: el programa lleva más de 1.000 pasos" in err
    assert "¿quedó en un bucle que nunca termina?" in err
    codigo, out, _ = por_main(
        tmp_path, capsys, "para i en rango(5000) { }\nmostrar(\"llegó\")", "--sin-limite")
    assert (codigo, out) == (0, "llegó\n")


def test_el_freno_no_se_ataja_con_intentar_y_nombra_al_agente():
    interprete = mate.Interprete(salida=lambda t: None)
    assert interprete.max_pasos == mate.MAX_PASOS == 10_000_000
    interprete.max_pasos = 1000
    programa = mate.analizar("""
        mensaje Girar
        agente Trompo {
            al recibir Girar {
                intentar {
                    mientras verdadero { sea x = 1 }
                } si falla e {
                    mostrar("atajado")
                }
            }
        }
        enviar Girar {} a Trompo
    """)
    with pytest.raises(mate.ErrorMate) as info:
        interprete.correr(programa)
    assert info.value.clase == "limite" and info.value.linea == 6
    assert info.value.mensaje.startswith("Trompo atendiendo Girar: el programa lleva más de 1.000 pasos")
    assert mate.ErrorMate("x").clase == "falla"


def test_cada_prueba_arranca_con_la_cuenta_de_pasos_en_cero():
    interprete = mate.Interprete()
    interprete.max_pasos = 1000
    programa = mate.analizar("""
        prueba "una" { para i en rango(300) { sea x = i } }
        prueba "dos" { para i en rango(300) { sea x = i } }
        prueba "tres" { mientras verdadero { } }
    """)
    resultados = interprete.correr(programa, pruebas=True)
    assert [error is None for _, error in resultados] == [True, True, False]
    assert "más de 1.000 pasos" in resultados[2][1]


# ── Tanda 2: números que se ven bien y errores que ayudan ──

def mostrado(expresion):
    return correr(f"mostrar({expresion})")[0][0]


# Mejora 13: los decimales se muestran limpios

def test_los_decimales_se_muestran_limpios():
    casos = {
        "0.1 + 0.2": "0.3", "1.1 * 3": "3.3", "10 / 3": "3.33333333333",
        "0.00001": "0.00001", "1234567.891": "1234567.891", "2.5": "2.5", "6 / 2": "3",
        "1234567890123.45": "1234567890123.45", "12345678901.1 + 0.2": "12345678901.3",
        "[0.1 + 0.2]": "[0.3]", '"{0.1 + 0.2}"': "0.3",
    }
    for expresion, esperado in casos.items():
        assert mostrado(expresion) == esperado, expresion
    assert mate.formato(float("inf")) == "infinito"
    assert mate.formato(float("nan")) == "no es un número"


def test_mostrar_limpio_no_cambia_el_valor():
    assert mostrado("0.1 + 0.2 == 0.3") == "falso"
    assert mostrado("redondear(0.1 + 0.2, 2) == redondear(0.3, 2)") == "verdadero"
    assert mostrado("a_json(0.1 + 0.2)") == "0.30000000000000004"


# Mejora 14: redondear con el medio hacia arriba

def test_redondear_lleva_el_medio_hacia_arriba():
    casos = {
        "redondear(2.5)": "3", "redondear(0.5)": "1", "redondear(1.5)": "2",
        "redondear(2.675, 2)": "2.68", "redondear(12.5, 2)": "12.5", "redondear(7)": "7",
        "redondear(-2.5)": "-3", "redondear(3.14159, 2)": "3.14", "redondear(-0.4)": "0",
        "redondear(123456789012345678901234567890, 2)": "123456789012345678901234567890",
        "redondear(1.5, 1000000000)": "1.5",
    }
    for expresion, esperado in casos.items():
        assert mostrado(expresion) == esperado, expresion
    assert "cantidad entera de decimales" in falla("redondear(1.5, -1)").mensaje


# Mejora 15: numero() entiende el formato argentino

def test_numero_entiende_el_formato_argentino():
    casos = {
        'numero("1.234,50")': "1234.5", 'numero("1.234.567")': "1234567",
        'numero("12")': "12", 'numero(" 7,25 ")': "7.25", 'numero("3.500")': "3.5",
        'numero("$ 1.234,5")': "1234.5", 'numero("-$ 1.500,00")': "-1500",
        'numero("-12")': "-12", "numero(5)": "5", 'tipo(numero("3,5"))': "numero",
    }
    for expresion, esperado in casos.items():
        assert mostrado(expresion) == esperado, expresion


def test_numero_rechaza_lo_que_no_es_un_numero():
    assert falla('numero("")').mensaje == "un texto vacío no es un número"
    assert falla('numero("   ")').mensaje == "un texto vacío no es un número"
    for texto in ["1e5", "1_000", "inf", "nan", "hola", "1,2,3", "12.34,5", "$", ".5", "$ 1.234.5"]:
        assert falla(f'numero("{texto}")').mensaje == f"'{texto}' no es un número"
    assert "espera texto" in falla("numero([1])").mensaje


# Mejora 16: pesos()

def test_pesos_muestra_plata():
    casos = {
        "pesos(1234567.891)": "$ 1.234.567,89", "pesos(12.5)": "$ 12,50",
        "pesos(3500)": "$ 3.500,00", "pesos(3500, 0)": "$ 3.500",
        "pesos(-1500)": "-$ 1.500,00", "pesos(2.675)": "$ 2,68", "pesos(-0.001)": "$ 0,00",
        "pesos(999999.999)": "$ 1.000.000,00", "numero(pesos(-1234.5))": "-1234.5",
        "pesos(123456789012345678901234567890, 0)": "$ 123.456.789.012.345.678.901.234.567.890",
    }
    for expresion, esperado in casos.items():
        assert mostrado(expresion) == esperado, expresion
    assert falla('pesos("hola")').mensaje == "pesos() espera numero y recibió texto"
    assert "entre 0 y 6" in falla("pesos(1, 7)").mensaje


# Mejora 17: "¿Quisiste decir...?"

def test_sugiere_el_nombre_parecido():
    assert falla("sea total = 5\nmostrar(totl)").mensaje == \
        "no existe 'totl'. ¿Quisiste decir 'total'?"
    assert falla('mostar("hola")').mensaje.endswith("¿Quisiste decir 'mostrar'?")
    assert falla('Mostrar("x")').mensaje.endswith("¿Quisiste decir 'mostrar'?")
    assert falla("mostrar(zzz)").mensaje == "no existe 'zzz'"
    assert falla("x = 5").mensaje == "no existe 'x'. Para crear la variable escribí: var x = ..."
    assert falla("var total = 1\ntotl = 5").mensaje == "no existe 'totl'. ¿Quisiste decir 'total'?"
    assert mate.sugerir("año", ["ano", "otro"]) == " ¿Quisiste decir 'ano'?"
    assert mate.sugerir("x", ["y", "total"]) == ""


def test_sugiere_campos_claves_y_mensajes():
    mapa = 'sea m = { nombre: "a", precio: 2 }\n'
    assert falla(mapa + "mostrar(m.nombr)").mensaje == \
        "mapa no tiene un campo 'nombr'. ¿Quisiste decir 'nombre'?"
    clave = falla(mapa + 'mostrar(m["Precio"])').mensaje
    assert "clave" in clave and clave.endswith("¿Quisiste decir 'precio'?")
    assert falla(mapa + 'mostrar(m["zzz"])').mensaje == 'el mapa no tiene la clave "zzz"'
    pedido = 'mensaje Pedido { producto: texto }\nsea p = Pedido { producto: "x" }\n'
    assert falla(pedido + "mostrar(p.produto)").mensaje.endswith("¿Quisiste decir 'producto'?")
    interprete = mate.Interprete()
    interprete.cargar(mate.analizar("mensaje Pedido { producto: texto }"))
    with pytest.raises(mate.ErrorMate) as info:
        interprete.construir("Pedidoo", {})
    assert info.value.mensaje == "no existe el mensaje 'Pedidoo'. ¿Quisiste decir 'Pedido'?"
    with pytest.raises(mate.ErrorMate) as info:
        interprete.construir("Pedido", {"producto": "x", "produto": "y"})
    assert info.value.mensaje.endswith("¿Quisiste decir 'producto'?")
    errores = mate.verificar(mate.analizar("mensaje Pedido { producto: texo, otro: Pedid }"))
    assert [t for _, t in errores] == [
        "Pedido.otro: no existe el tipo 'Pedid'. ¿Quisiste decir 'Pedido'?",
        "Pedido.producto: no existe el tipo 'texo'. ¿Quisiste decir 'texto'?"]


# Mejora 18: palabras propias de Mate como nombre de campo

def test_palabras_propias_como_nombre_de_campo():
    salida, _ = correr("""
        mensaje Envio { estado: texto, para: texto, tipo: texto, en: numero, y: numero? }
        sea e = Envio { estado: "listo", para: "Ana", tipo: "x", en: 3 }
        mostrar(e.estado, e.para, e.en, e.y)
        sea p = { x: 1, y: 2 }
        mostrar(p.y)
        sea m = { si: 1 }
        mostrar(m.si, m["si"])
        sea ida = a_json(e)
        mostrar(de_json(ida) == e, de_json(ida).para)
        var copia = e
        copia.estado = "otro"
        mostrar(copia.estado, e.estado)
    """)
    assert salida == ["listo Ana 3 nada", "2", "1 1", "verdadero Ana", "otro listo"]
    assert "nombre de campo" in falla("sea m = { si }").mensaje


# Mejora 19: palabras reservadas y funciones incluidas como nombre

def test_no_se_usa_una_palabra_propia_como_nombre():
    error = falla("sea y = 1")
    assert error.mensaje == ("'y' es una palabra propia de Mate y no se puede usar como "
                             "nombre; elegí otro (por ejemplo 'y2')")
    assert error.linea == 1
    assert "palabra propia de Mate" in falla("funcion f(si) { }").mensaje
    assert "palabra propia de Mate" in falla("para en en [1] { }").mensaje


def test_no_se_tapa_una_funcion_incluida():
    incluida = "'texto' es una función incluida de Mate; elegí otro nombre (por ejemplo 'mi_texto')"
    assert falla('sea texto = "hola"').mensaje == incluida
    assert falla("si verdadero { var texto = 1 }").mensaje == incluida
    assert falla("funcion f(texto) { }").mensaje == incluida
    assert falla("\nfuncion mostrar(x) { }").linea == 2
    assert "función incluida" in falla("funcion mostrar(x) { }").mensaje
    assert "función incluida" in falla("para largo en [1] { }").mensaje
    assert "función incluida" in falla("funcion pesos() { }").mensaje
    entorno = mate.Entorno(mate.Interprete().glob)
    with pytest.raises(mate.ErrorMate) as info:
        entorno.definir("tipo", 1)
    assert "función incluida" in info.value.mensaje
    assert falla("sea a = 1\nsea a = 2").mensaje == (
        "'a' ya está definido en este bloque; para cambiarle el valor se escribe a = ... "
        "(y tiene que ser 'var')")


# Mejora 20: pistas para palabras de otros lenguajes

def test_pistas_para_palabras_de_otros_lenguajes():
    assert "en Mate 'print' se escribe 'mostrar'" in falla('print("hola")').mensaje
    assert falla("sea x = true").mensaje == "en Mate 'true' se escribe 'verdadero'"
    assert falla("si verdadero { } else { }").mensaje == "en Mate 'else' se escribe 'sino'"
    assert falla("\nfunción doble(n) { devolver n * 2 }").linea == 2
    assert falla("función doble(n) { devolver n * 2 }").mensaje == \
        "en Mate se escribe 'funcion', sin tilde"
    errores = mate.verificar(mate.analizar("mensaje M { a: número }"))
    assert "en Mate se escribe 'numero', sin tilde" in errores[0][1]
    assert "sin tilde" in falla('mostrar(mayúsculas("a"))').mensaje
    assert "'romper'" in falla("mientras verdadero { break }").mensaje


def test_las_pistas_no_rompen_campos_ni_nombres_con_tilde():
    assert correr("sea m = { for: 1, if: 2 }\nmostrar(m.for, m.if)")[0] == ["1 2"]
    assert correr("sea número = 5\nmostrar(número)")[0] == ["5"]


def test_palabras_propias_con_mayuscula():
    assert falla("Si verdadero { }").mensaje == "'Si' va en minúscula: 'si'"
    assert falla("si verdadero { } Sino { }").mensaje == "'Sino' va en minúscula: 'sino'"
    assert "va en minúscula" in falla("sea x = Verdadero").mensaje
    assert correr("var Estado = 1\nEstado = 2\nmostrar(Estado)")[0] == ["2"]


# Mejora 21: pistas en condiciones mal escritas

def test_pistas_en_condiciones_mal_escritas():
    assert falla("sea x = 5\nsi x = 5 { }").mensaje == \
        "para comparar se usa '==' (un solo '=' es para asignar)"
    assert falla("sea x = 5\nmientras x = 5 { }").linea == 2
    assert falla("sea x = 5\nsi x > 3 y < 10 { }").mensaje == \
        "después de 'y' hay que repetir la variable: x > 3 y x < 10"
    assert "después de 'o'" in falla("sea x = 5\nsi x == 1 o == 2 { }").mensaje
    encadenadas = "las comparaciones no se encadenan: escribí 1 < x y x < 10"
    assert falla("mostrar(1 < 2 < 3)").mensaje == encadenadas
    assert falla("sea x = 5\nsi 1 < x < 10 { }").mensaje == encadenadas
    assert "no va 'entonces'" in falla("sea x = 5\nsi x > 3 entonces { }").mensaje
    salida, _ = correr('sea x = 5\nsi x > 3 y x < 10 { mostrar("ok") }\nmostrar((1 < 2) == verdadero)')
    assert salida == ["ok", "verdadero"]


# Mejora 22: asegurar muestra los valores

def test_asegurar_muestra_los_valores():
    programa = mate.analizar("""sea a = 2
        prueba "igual" { asegurar a + 1 == 4 }
        prueba "menor" { asegurar a > 5 }
        prueba "propio" { asegurar a < 1, "a tiene que ser chico" }
        prueba "textos" { asegurar "hola" == "chau" }
        prueba "suelto" { asegurar falso }
        prueba "bien" { asegurar a == 2 }
    """)
    resultados = dict(mate.Interprete().correr(programa, pruebas=True))
    assert resultados == {
        "igual": "línea 2: no se cumplió lo asegurado: dio 3 y se esperaba 4",
        "menor": "línea 3: no se cumplió lo asegurado: 2 > 5 es falso",
        "propio": "línea 4: a tiene que ser chico (2 < 1 es falso)",
        "textos": 'línea 5: no se cumplió lo asegurado: dio "hola" y se esperaba "chau"',
        "suelto": "línea 6: no se cumplió lo asegurado",
        "bien": None,
    }


def test_asegurar_evalua_cada_lado_una_sola_vez():
    error = falla("""
        var n = 0
        funcion siguiente() {
            n = n + 1
            devolver n
        }
        asegurar siguiente() == 5
    """)
    assert error.mensaje == "no se cumplió lo asegurado: dio 1 y se esperaba 5"
    assert error.clase == "asegurar"
    assert "condición" in falla("asegurar 1").mensaje


# Mejora 23: por qué no se puede cambiar

def test_no_se_puede_cambiar_dice_de_que_se_trata():
    error = falla("funcion f(a) { a = a + 1 }\nf(1)")
    assert error.mensaje == ("'a' es un parámetro y no se cambia; guardalo en otra variable: "
                             "var a2 = a")
    assert error.linea == 1
    assert "variable del 'para'" in falla("para i en [1] { i = 2 }").mensaje
    assert "error atajado" in falla('intentar { fallar "x" } si falla e { e = 1 }').mensaje
    assert falla("funcion f() { }\nf = 1").mensaje == \
        "'f' es una función y no se le puede asignar un valor"
    agente = "mensaje M\nagente Vendedor { al recibir M como p { p = 1 } }\n"
    assert falla(agente + "Vendedor = 2").mensaje == \
        "'Vendedor' es un agente y no se le puede asignar un valor"
    _, interprete = correr(agente + "enviar M {} a Vendedor")
    assert "'p' es el mensaje recibido y no se cambia" in interprete.errores_agentes[0]
    assert "función incluida" in falla("mostrar = 1").mensaje
    assert falla("sea x = 1\nx = 2").mensaje == \
        "'x' es fijo (sea); declaralo con 'var' para cambiarlo"


# Mejora 24: el error muestra el renglón

def test_el_error_muestra_el_renglon(tmp_path, capsys):
    codigo, _, err = por_main(tmp_path, capsys, "sea total = 5\n    mostrar(totl)   \n")
    renglones = err.splitlines()
    assert codigo == 1 and len(renglones) == 2
    assert renglones[0].endswith("programa.mate:2: error: no existe 'totl'. ¿Quisiste decir 'total'?")
    assert renglones[1] == "    2 |     mostrar(totl)"


def test_el_renglon_de_un_error_al_final_del_archivo(tmp_path, capsys):
    _, _, err = por_main(tmp_path, capsys, "sea x = 1\nsi x == 1 {\n  mostrar(x)\n\n\n")
    assert err.splitlines()[1] == "    3 |   mostrar(x)"
    _, _, err = por_main(tmp_path, capsys, "mensaje M { a: texo, b: nro }\n", orden="verificar")
    assert len(err.splitlines()) == 3  # dos errores del mismo renglón: se muestra una vez
    assert mate.renglon_de(str(tmp_path / "no_esta.mate"), 1) is None


def test_sugiere_el_agente_parecido():
    programa = mate.analizar("mensaje M\nagente Vendedor { al recibir M { } }\ncrear Vendedr")
    assert [t for _, t in mate.verificar(programa)] == [
        "no existe el agente 'Vendedr'. ¿Quisiste decir 'Vendedor'?"]


# ── Tanda 3: garantías entre agentes y en las pruebas ──

def probar(fuente):
    """Corre las pruebas de un programa y devuelve {nombre: error o None}."""
    interprete = mate.Interprete(salida=lambda _: None)
    programa = mate.analizar(fuente)
    assert mate.verificar(programa) == []
    return dict(interprete.correr(programa, pruebas=True))


def revisar(fuente):
    return [(int(linea), texto) for linea, texto in mate.verificar(mate.analizar(fuente))]


# Mejora 25: las funciones no viajan en los mensajes

def test_las_funciones_no_viajan_en_un_mensaje():
    error = falla("mensaje P { datos: mapa }\nsea p = P { datos: {x: mostrar} }")
    assert error.linea == 2
    assert error.mensaje == "los mensajes llevan datos, no funciones (campo 'datos' de P)"
    error = falla("mensaje P { datos: cualquiera }\nfuncion f() { }\nsea g = f\n"
                  "sea p = P { datos: [1, [g]] }")
    assert error.linea == 4 and "no funciones" in error.mensaje
    assert revisar("mensaje P { datos: cualquiera }\nfuncion f() { }\nsea p = P { datos: f }") == [
        (3, "los mensajes llevan datos, no funciones (campo 'datos' de P)")]
    # Un parámetro que se llama igual que una función no confunde a la revisión previa.
    assert revisar("mensaje P { datos: cualquiera }\nfuncion f() { }\n"
                   "funcion g(f) { devolver P { datos: f } }") == []


def test_no_se_responde_con_una_funcion():
    error = falla("""mensaje Dame
        agente A {
            estado secreto = 1
            funcion cambiar(n) { secreto = n }
            al recibir Dame {
                responder cambiar
            }
        }
        sea f = preguntar Dame {} a A""")
    assert error.linea == 6
    assert error.mensaje == "no se puede responder con una función: las respuestas llevan datos"


# Mejora 26: un agente no cambia lo de afuera a través de una función

CONTADOR = """
    var cont = 0
    funcion inc() { cont = cont + 1 }
    mensaje Ping
    agente A { al recibir Ping { inc()  responder 1 } }
"""


def test_un_agente_no_cambia_lo_de_afuera_con_una_funcion():
    salida, _ = correr(CONTADOR + """
        intentar { preguntar Ping {} a A } si falla e { mostrar(e) }
        mostrar(cont)
        inc()
        mostrar(cont)
    """)
    assert salida[0].startswith(
        "A no puede modificar 'cont' (ni siquiera a través de la función inc())")
    assert salida[1:] == ["0", "1"]
    assert probar(CONTADOR + 'prueba "afuera sí" { inc()\n asegurar cont == 1 }') == {
        "afuera sí": None}


def test_una_funcion_llamada_por_un_agente_usa_sus_propias_variables():
    salida, _ = correr("""
        funcion doble(n) { var r = n  r = r * 2  devolver r }
        mensaje Ping
        agente A { estado veces = 0
            al recibir Ping { veces = veces + 1  responder doble(veces) } }
        mostrar(preguntar Ping {} a A)
    """)
    assert salida == ["2"]


# Mejora 27: lo enviado llega antes de la próxima pregunta

SUMADOR = """
    mensaje Sumar { n: numero }
    mensaje Ver
    agente C {
        estado total = 0
        al recibir Sumar como s { total = total + s.n }
        al recibir Ver { responder total }
    }
"""


def test_lo_enviado_llega_antes_de_preguntar():
    salida, _ = correr(SUMADOR + "enviar Sumar { n: 5 } a C\nmostrar(preguntar Ver {} a C)")
    assert salida == ["5"]
    assert probar(SUMADOR + """
        prueba "con preguntar" { enviar Sumar { n: 5 } a C
            asegurar (preguntar Ver {} a C) == 5 }
        prueba "con asegurar solo" { enviar Sumar { n: 5 } a C
            sea antes = 1
            asegurar antes == 1
            asegurar (preguntar Ver {} a C) == 5 }
    """) == {"con preguntar": None, "con asegurar solo": None}


# Mejora 28: el tope de mensajes es por prueba

def test_el_tope_de_mensajes_se_reinicia_en_cada_prueba(monkeypatch):
    monkeypatch.setattr(mate, "MAX_MENSAJES", 100)
    cuerpo = "para i en rango(60) { asegurar (preguntar Ver {} a C) == 0 }"
    assert probar(SUMADOR + f'prueba "uno" {{ {cuerpo} }}\nprueba "dos" {{ {cuerpo} }}') == {
        "uno": None, "dos": None}


# Mejora 29: cada prueba empieza limpia

def test_cada_prueba_empieza_limpia():
    resultados = probar("""
        mensaje Sumar { n: numero }
        agente C { estado total = 0
            al recibir Sumar como s { total = total + s.n  responder total } }
        sea copia = crear C { total: 100 }
        var g = 0
        g = 7
        prueba "uno" { g = g + 1
            asegurar (preguntar Sumar { n: 5 } a copia) == 105 }
        prueba "dos" { asegurar g == 7
            asegurar (preguntar Sumar { n: 1 } a copia) == 101
            asegurar (preguntar Sumar { n: 1 } a C) == 1 }
        prueba "tres" { asegurar (preguntar Sumar { n: 1 } a C) == 1 }
    """)
    assert resultados == {"uno": None, "dos": None, "tres": None}


# Mejora 30: 'intentar' no ataja los 'asegurar' ni los topes

def test_intentar_no_ataja_un_asegurar():
    resultados = probar('prueba "x" { intentar { asegurar 1 == 2 } si falla e { } }\n'
                        'prueba "y" { intentar { fallar "ups" } si falla e { asegurar e == "ups" } }')
    assert resultados["x"].endswith("no se cumplió lo asegurado: dio 1 y se esperaba 2")
    assert resultados["y"] is None


def test_intentar_no_ataja_los_topes(monkeypatch):
    error = falla("funcion f(n) { devolver f(n + 1) }\n"
                  "intentar { f(0) } si falla e { mostrar(e) }")
    assert error.mensaje == "demasiada recursión" and error.clase == "limite"
    monkeypatch.setattr(mate, "MAX_MENSAJES", 10)
    error = falla(SUMADOR + "intentar { para i en rango(20) { preguntar Ver {} a C } } "
                            "si falla e { mostrar(e) }")
    assert "se superaron 10 mensajes" in error.mensaje


# Mejora 31: si un agente falla, vuelve a como estaba

def test_si_un_agente_falla_vuelve_a_como_estaba():
    salida, interprete = correr("""
        mensaje Pedido { producto: texto }
        mensaje Cuantas
        mensaje Aviso
        agente Otro { al recibir Aviso { mostrar("aviso") } }
        agente V {
            estado ventas = 0
            al recibir Pedido como p {
                ventas = ventas + 1
                enviar Aviso {} a Otro
                si p.producto == "cafe" { fallar "no vendo cafe" }
                responder ventas
            }
            al recibir Cuantas { responder ventas }
        }
        intentar { preguntar Pedido { producto: "cafe" } a V } si falla e { mostrar(e) }
        mostrar(preguntar Cuantas {} a V)
        mostrar(preguntar Pedido { producto: "yerba" } a V)
    """)
    # El aviso del pedido que falló no sale; el del pedido que anduvo, sí.
    assert salida == ["no vendo cafe", "0", "1", "aviso"]
    assert interprete.errores_agentes == []


# Mejora 32: aviso de lo que quedó sin entregar

def test_avisa_los_mensajes_que_quedaron_sin_entregar(tmp_path, capsys):
    programa = ('mensaje Pedido { producto: texto }\nagente V { al recibir Pedido { } }\n'
                + 'enviar Pedido { producto: "cafe" } a V\n' * 7
                + 'fallar "algo se rompió arriba"\n')
    codigo, _, err = por_main(tmp_path, capsys, programa)
    renglones = err.splitlines()
    assert codigo == 1
    assert renglones[0].endswith("programa.mate:10: error: algo se rompió arriba")
    assert renglones[2] == "quedaron 7 mensaje(s) sin entregar:"
    assert renglones[3] == '  (programa) -> V: Pedido { producto: "cafe" }'
    assert len(renglones) == 9 and renglones[8] == "  ... y 2 más"
    _, _, err = por_main(tmp_path, capsys, 'fallar "nada en la cola"\n')
    assert "sin entregar" not in err


# Mejora 33: errores de agentes con el archivo correcto, y todos a la vista

def test_el_error_de_un_agente_dice_su_archivo(tmp_path, capsys):
    (tmp_path / "lib.mate").write_text(
        'mensaje Ping\nagente Roto { al recibir Ping { fallar "me rompí" } }\n', encoding="utf-8")
    codigo, _, err = por_main(tmp_path, capsys, 'usar "lib.mate"\nenviar Ping {} a Roto\n')
    renglones = err.splitlines()
    assert codigo == 1
    assert renglones[0].endswith("lib.mate:2: error: Roto al recibir Ping: me rompí")
    assert renglones[1].startswith("    2 | agente Roto")


def test_probar_muestra_los_errores_del_programa_principal(tmp_path, capsys):
    codigo, out, err = por_main(tmp_path, capsys, """mensaje Ping
agente Roto { al recibir Ping { fallar "me rompí" } }
enviar Ping {} a Roto
prueba "anda" { asegurar 1 == 1 }
""", orden="probar")
    assert codigo == 1
    assert "1 de 1 pruebas pasaron" in out
    assert err.splitlines()[0] == "errores al correr el programa (antes de las pruebas):"
    assert "programa.mate:2: error: Roto al recibir Ping: me rompí" in err


def test_una_prueba_muestra_todos_los_errores_de_agentes():
    resultados = probar("""mensaje Ping { n: numero }
        agente Roto { al recibir Ping como p { fallar "me rompí {p.n}" } }
        prueba "dos errores" { enviar Ping { n: 1 } a Roto
            enviar Ping { n: 2 } a Roto }""")
    assert resultados["dos errores"] == ("Roto al recibir Ping (línea 2): me rompí 1\n"
                                         "Roto al recibir Ping (línea 2): me rompí 2")


# Mejora 34: la revisión previa sigue a las copias y detecta al que nunca responde

def test_la_revision_sigue_a_las_copias():
    assert revisar("agente V { al recibir Ping { responder 1 } }\nmensaje Ping {}\n"
                   "mensaje Pong {}\nsea v = crear V\nenviar Pong {} a v") == [
        (5, "V no sabe recibir 'Pong'")]
    assert revisar("mensaje Ping\nmensaje Pong\n"
                   "agente V { al recibir Ping {\n enviar Pong {} a yo } }") == [
        (4, "V no sabe recibir 'Pong'")]
    # Si el nombre se usa para más de una cosa, la revisión no opina.
    assert revisar("agente V { al recibir Ping { responder 1 } }\nmensaje Ping {}\n"
                   "mensaje Pong {}\nsea v = crear V\nfuncion f(v) { enviar Pong {} a v }") == []


def test_la_revision_detecta_al_agente_que_nunca_responde():
    assert revisar('mensaje Ping\nagente Mudo { al recibir Ping { mostrar("hola") } }\n'
                   "sea r = preguntar Ping {} a Mudo") == [
        (3, "Mudo recibe 'Ping' pero nunca responde: no se le puede preguntar "
            "(le falta un 'responder')")]
    # Si responde una función suya, o siempre falla a propósito, no opina.
    assert revisar("mensaje Ping\nagente A { funcion r() { responder 1 }\n"
                   "al recibir Ping { r() } }\nsea x = preguntar Ping {} a A") == []
    assert revisar('mensaje Ping\nagente A { al recibir Ping { fallar "no" } }\n'
                   "sea x = preguntar Ping {} a A") == []
    error = falla("mensaje Ping\nagente A { al recibir Ping como p { si p == 1 { responder 1 } } }\n"
                  "sea x = preguntar Ping {} a A")
    assert error.mensaje == ("A no respondió a 'Ping': el 'al recibir' terminó sin llegar "
                             "a un 'responder'")


@pytest.mark.parametrize("nombre", ["catalogo", "equipo", "hola", "mercado", "negociacion"])
def test_verificar_los_ejemplos_no_da_errores(nombre, capsys):
    assert mate.main(["verificar", str(RAIZ / "ejemplos" / f"{nombre}.mate")]) == 0
    assert capsys.readouterr().out.strip().endswith("sin errores")


# Mejora 35: 'crear' revisa el estado inicial

AGENTE_V = ("agente V { estado precios = {}  estado ventas = 0  estado nota = nada\n"
            " al recibir Ping { responder ventas } }\nmensaje Ping\n")


def test_crear_revisa_el_estado_inicial():
    assert revisar(AGENTE_V + 'sea v = crear V { precios: 5, ventas: "muchas" }') == [
        (4, "V.precios arranca como mapa y le diste numero"),
        (4, "V.ventas arranca como numero y le diste texto")]
    error = falla(AGENTE_V + "sea p = 5\nsea v = crear V { precios: p }")
    assert error.linea == 5
    assert error.mensaje == "V.precios arranca como mapa y le diste numero"
    salida, _ = correr(AGENTE_V + 'sea v = crear V { ventas: 10, nota: "lo que sea" }\n'
                                  "mostrar(preguntar Ping {} a v)")
    assert salida == ["10"]


# Mejora 36: un 'enviar' que el destino no entiende falla en quien lo envía

def test_enviar_algo_que_no_entiende_falla_en_el_que_envia(tmp_path, capsys):
    programa = ("mensaje Ping {}\nmensaje Pong {}\nagente V { al recibir Ping { } }\n"
                "var v = crear V\n")
    salida, interprete = correr(
        programa + "intentar { enviar Pong {} a v } si falla e { mostrar(e) }")
    assert salida == ["V#2 no sabe recibir 'Pong'"]
    assert interprete.errores_agentes == []
    error = falla(programa + "var x = 1\nenviar Pong {} a v")
    assert error.linea == 6 and error.mensaje == "V#2 no sabe recibir 'Pong'"
    codigo, out, err = por_main(
        tmp_path, capsys, programa + "intentar { enviar Pong {} a v } si falla e { mostrar(e) }")
    assert (codigo, out, err) == (0, "V#2 no sabe recibir 'Pong'\n", "")


def test_la_respuesta_a_un_enviar_tiene_que_poder_recibirse():
    _, interprete = correr("""
        mensaje Ping
        mensaje Pong
        mensaje Arrancar
        agente Eco { al recibir Ping { responder Pong {} } }
        agente Sordo { al recibir Arrancar { enviar Ping {} a Eco } }
        enviar Arrancar {} a Sordo
    """)
    assert interprete.errores_agentes == [
        "Eco al recibir Ping: Eco respondió Pong a Sordo, pero Sordo no tiene 'al recibir Pong'"]


# ───────────── Correcciones de la revisión de las tandas 1 a 3 ─────────────

DEPOSITO = """
mensaje Pedido { cantidad: numero }
agente Deposito {
    estado stock = 10
    al recibir Pedido como p {
        asegurar p.cantidad > 0, "cantidad invalida"
        stock = stock - p.cantidad
        responder stock
    }
}
"""


def test_un_asegurar_se_ataja_al_correr_y_entre_agentes():
    salida, _ = correr(DEPOSITO + """
        intentar { mostrar(preguntar Pedido { cantidad: -1 } a Deposito) }
        si falla e { mostrar("rechazado: " + e) }
        funcion validar(x) {
            asegurar x > 0, "tiene que ser positivo"
            devolver x
        }
        para i en [1, -1] { intentar { mostrar(validar(i)) } si falla e { mostrar(e) } }
        mostrar("sigo")
    """)
    assert salida == ["rechazado: cantidad invalida (-1 > 0 es falso)", "1",
                      "tiene que ser positivo (-1 > 0 es falso)", "sigo"]
    # En una prueba: el 'asegurar' de otro agente se ataja; el de la prueba, no.
    resultados = probar(DEPOSITO + """
        prueba "el del agente llega como error" {
            var visto = ""
            intentar { preguntar Pedido { cantidad: -1 } a Deposito } si falla e { visto = e }
            asegurar tiene(visto, "cantidad invalida")
        }
        prueba "el propio no se esconde" { intentar { asegurar 1 == 2 } si falla { } }
    """)
    assert resultados["el del agente llega como error"] is None
    assert "dio 1 y se esperaba 2" in resultados["el propio no se esconde"]


def test_crear_no_calcula_el_estado_que_le_dan():
    salida, _ = correr("""
        mensaje Ver { }
        agente Caja { estado n = 0
            al recibir Ver { responder n } }
        funcion avisar() {
            mostrar("calculando")
            devolver 10
        }
        agente Local {
            estado caja = crear Caja
            estado tope = avisar()
            al recibir Ver { responder tope }
        }
        sea mia = crear Caja { n: 7 }
        sea l = crear Local { caja: mia, tope: 5 }
        mostrar(preguntar Ver {} a l)
        mostrar(crear Caja)
        intentar { crear Local { tope: "alto" } } si falla e { mostrar(e) }
        intentar { crear Local { caja: 3 } } si falla e { mostrar(e) }
    """)
    assert salida == ["calculando", "5", "Caja#4", "Local.tope arranca como numero y le diste texto",
                      "Local.caja arranca como agente y le diste numero"]


def test_crear_acepta_nada_como_estado_inicial():
    salida, _ = correr(AGENTE_V + "sea v = crear V { ventas: nada }\nmostrar(preguntar Ping {} a v)")
    assert salida == ["nada"]


def test_un_crear_rechazado_no_gasta_numero_de_copia():
    salida, _ = correr(AGENTE_V + "sea cinco = 5\n"
                       "intentar { crear V { precios: cinco } } si falla e { }\nmostrar(crear V)")
    assert salida == ["V#2"]


def test_los_nombres_propios_que_parecen_de_otro_lenguaje_se_respetan():
    assert correr("sea def = 5\nsea or = 2\nmostrar(def + or)")[0] == ["7"]
    assert correr("mensaje Return { x: numero }\nsea r = Return { x: 1 }\nmostrar(r)")[0] == [
        "Return { x: 1 }"]
    assert correr("funcion Crear(x) { devolver x }\nCrear(3)\nmostrar(Crear(4))")[0] == ["4"]
    assert correr("funcion f(let) { devolver let + 1 }\nmostrar(f(1))")[0] == ["2"]
    # ...pero usados como palabras de otro lenguaje se siguen explicando antes de correr
    for fuente, pista in [("sea x = 1\nif x == 1 {\n}", "en Mate 'if' se escribe 'si'"),
                          ("sea x = true", "en Mate 'true' se escribe 'verdadero'"),
                          ("si verdadero { } else { }", "en Mate 'else' se escribe 'sino'"),
                          ("si verdadero and verdadero { }", "en Mate 'and' se escribe 'y'"),
                          ('print("hola")', "en Mate 'print' se escribe 'mostrar'"),
                          ("función f() { }", "en Mate se escribe 'funcion', sin tilde")]:
        with pytest.raises(mate.ErrorMate) as info:
            mate.analizar(fuente)
        assert info.value.mensaje == pista, fuente


def test_palabras_con_mayuscula_en_el_medio_del_renglon():
    assert falla("sea x = 5\nsi x > 3 Y x < 10 { }").mensaje == "'Y' va en minúscula: 'y'"
    assert falla("para i En [1] { }").mensaje == "'En' va en minúscula: 'en'"
    assert falla("sea x = 4\nSi (x > 3) { }").mensaje == "'Si' va en minúscula: 'si'"


def test_pistas_para_los_comparadores_mal_escritos():
    casos = {"si x => 5 { }": "'mayor o igual' se escribe '>='",
             "si x =< 5 { }": "'menor o igual' se escribe '<='",
             "si x === 5 { }": "para comparar se usa '=='",
             "si x <> 5 { }": "'distinto' se escribe '!='",
             "si (x = 5) { }": "para comparar se usa '=='",
             "asegurar x = 5": "para comparar se usa '=='"}
    for fuente, pista in casos.items():
        error = falla("sea x = 5\n" + fuente)
        assert error.linea == 2 and pista in error.mensaje, fuente


def test_llaves_vacias_o_a_medias_dentro_de_un_texto():
    for fuente in ['mostrar("{}")', 'mostrar("{1 +}")']:
        error = falla(fuente)
        assert "entre { y }" in error.mensaje and "final del archivo" not in error.mensaje


def test_la_pista_de_sumar_depende_de_lo_que_se_suma():
    assert "agregar(lista, valor)" in falla("mostrar([1] + 2)").mensaje
    assert "texto()" not in falla("mostrar([1] + 2)").mensaje
    assert "texto()" in falla('mostrar("a" + 2)').mensaje
    assert falla("mostrar(1 + verdadero)").mensaje == "no se puede hacer numero + logico"


def test_redondear_y_pesos_redondean_lo_que_se_muestra():
    casos = {
        "0.57 * 50": "28.5", "redondear(0.57 * 50)": "29", "pesos(0.57 * 50, 0)": "$ 29",
        "redondear(1.15 * 0.1, 2)": "0.12", "pesos(1.15 * 0.1)": "$ 0,12",
        "redondear(1.005 * 100)": "101", "redondear(2 / 3, 14)": "0.66666666666667",
        "redondear(2.4999)": "2", "redondear(-0.57 * 50)": "-29",
    }
    for expresion, esperado in casos.items():
        assert mostrado(expresion) == esperado, expresion
    assert "no puede ser negativa" in falla("redondear(1234, -2)").mensaje


def test_asegurar_con_decimales_que_se_ven_iguales():
    error = falla("asegurar 0.1 + 0.2 == 0.3")
    assert "dio 0.30000000000000004 y se esperaba 0.3" in error.mensaje
    assert "redondear(a, 2) == redondear(b, 2)" in error.mensaje
    assert "Redondeá antes de comparar" in falla("asegurar [0.1 + 0.2] == [0.3]").mensaje
    assert falla("asegurar 1 == 2").mensaje == "no se cumplió lo asegurado: dio 1 y se esperaba 2"


def test_numero_lee_lo_que_escribe_pesos():
    casos = {
        'numero(pesos(3500, 0))': "3500", 'numero(pesos(1234567, 0))': "1234567",
        'numero("-$ 3.500")': "-3500", 'numero(pesos(999.5))': "999.5",
        'numero(pesos(3.5, 3))': "3.5", 'numero("3.500")': "3.5", 'numero("$ 3.50")': "3.5",
    }
    for expresion, esperado in casos.items():
        assert mostrado(expresion) == esperado, expresion


def test_de_json_explica_en_espanol():
    casos = {'""': "JSON inválido: el texto está vacío",
             '"[1,2"': "JSON inválido: falta una coma o el cierre (']' o '}') (al final del texto)",
             '"[1] 2"': "JSON inválido: sobra texto después del final (en la letra 5 del texto)",
             '"hola"': "JSON inválido: falta un valor (en la letra 1 del texto)"}
    for texto, esperado in casos.items():
        assert falla(f"de_json({texto})").mensaje == esperado
    for texto in ['"\\{a: 1}"', '"[1,]"', '"\\{\\"a\\" 1}"', '"[\\"a"']:
        mensaje = falla(f"de_json({texto})").mensaje
        assert mensaje.startswith("JSON inválido: ")
        assert not any(palabra in mensaje for palabra in ("Expecting", "Invalid", "Extra", "Illegal"))


def test_cosas_demasiado_grandes_son_un_error_comun():
    error = falla("sea a = 1\nmostrar(rango(100000000000))")
    assert error.linea == 2 and error.mensaje.startswith("rango(): son demasiados números")
    error = falla('var t = "aaaaaaaaaa"\nmientras verdadero { t = t + t }')
    assert error.linea == 2 and "el texto quedaría demasiado largo" in error.mensaje
    assert "la lista quedaría demasiado larga" in falla(
        "var l = [1, 2]\nmientras verdadero { l = l + l }").mensaje
    error = falla("var x = 2\nmientras verdadero { x = x * x }")
    assert error.linea == 2 and error.mensaje == mate.DEMASIADO_GRANDE
    assert falla("var x = 1\nmientras verdadero { x = x + x }").mensaje == mate.DEMASIADO_GRANDE


def test_quedarse_sin_memoria_no_es_un_error_interno(monkeypatch):
    def sin_lugar(*_):
        raise MemoryError()
    monkeypatch.setattr(mate, "formato", sin_lugar)
    error = falla("sea a = 1\nmostrar(texto(a))")
    assert error.clase == "limite" and "se quedó sin memoria" in error.mensaje


def test_la_division_exacta_entre_enteros_no_pierde_cifras():
    casos = {"12345678901234567890 / 2": "6172839450617283945",
             "90071992547409931 / 1": "90071992547409931",
             "7 / 2": "3.5", "6 / 3": "2", "-7 / 7": "-1", "0 / 5": "0"}
    for expresion, esperado in casos.items():
        assert mostrado(expresion) == esperado, expresion


def test_el_freno_nombra_sin_limite():
    interprete = mate.Interprete(salida=lambda _: None)
    interprete.max_pasos = 100
    with pytest.raises(mate.ErrorMate) as info:
        interprete.correr(mate.analizar("para i en rango(1000) { }"))
    assert "--sin-limite" in info.value.mensaje and "Si es un 'mientras'" in info.value.mensaje


def test_ayuda_con_algo_al_lado_muestra_la_ayuda(capsys):
    assert mate.main(["ayuda", "correr"]) == 0
    capturado = capsys.readouterr()
    assert "Órdenes:" in capturado.out and capturado.err == ""


def test_el_archivo_antes_de_la_orden_o_sin_orden(tmp_path, capsys, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "hola.mate").write_text('mostrar("hola")', encoding="utf-8")
    (tmp_path / "nota.mate.txt").write_text('mostrar("nota")', encoding="utf-8")
    assert mate.main(["hola.mate", "probar"]) == 2
    assert capsys.readouterr().err == "la orden va primero y el archivo después: probar hola.mate\n"
    assert mate.main(["hola"]) == 0
    assert capsys.readouterr().out == "hola\n"
    assert mate.main(["nota.mate.txt"]) == 0
    capturado = capsys.readouterr()
    assert capturado.out == "nota\n" and "termina en .txt" in capturado.err
    assert mate.main(["corer", "hola.mate"]) == 2
    assert "¿quisiste decir 'correr'?" in capsys.readouterr().err


def test_mas_espacios_invisibles_y_el_que_no_se_acepta_se_nombra(tmp_path, capsys):
    raros = "".join(chr(c) for c in (0x200E, 0x2003, 0x3000, 0x200D, 0x2060, 0x2028, 0x0C))
    assert correr("mostrar(1)" + raros + "\nmostrar(2)")[0] == ["1", "2"]
    error = falla("sea a = 1\nmostrar(a)" + chr(7))
    assert error.linea == 2
    assert error.mensaje.startswith("hay un carácter invisible después de 'mostrar(a)'")
    # un archivo "Unicode" guardado sin la marca del principio
    archivo = tmp_path / "programa.mate"
    archivo.write_bytes('mostrar("ñandú")\n'.encode("utf-16-le"))
    assert mate.main(["correr", str(archivo)]) == 0
    assert capsys.readouterr().out == "ñandú\n"


def test_probar_muestra_el_renglon_y_todos_los_errores(tmp_path, capsys):
    codigo, out, _ = por_main(tmp_path, capsys, """mensaje Sumar { n: numero }
mensaje Total
agente C {
    estado t = 0
    al recibir Sumar como s {
        si s.n > 3 { fallar "no acepto más de 3" }
        t = t + s.n
    }
    al recibir Total { responder t }
}
prueba "con causa" {
    enviar Sumar { n: 5 } a C
    sea r = preguntar Total {} a C
    asegurar r == 5
}
""", orden="probar")
    assert codigo == 1
    renglones = [r.strip() for r in out.split("\n")]
    assert renglones[1:5] == [
        "línea 14: no se cumplió lo asegurado: dio 0 y se esperaba 5",
        "14 |     asegurar r == 5",
        "C al recibir Sumar (línea 6): no acepto más de 3",
        '6 |         si s.n > 3 { fallar "no acepto más de 3" }']


def test_probar_nombra_el_archivo_traido_con_usar(tmp_path, capsys):
    (tmp_path / "lib.mate").write_text(
        "mensaje Pedir { que: texto }\n\nagente Deposito {\n    estado stock = { yerba: 1 }\n"
        "    al recibir Pedir como p {\n        responder stock[p.que]\n    }\n}\n",
        encoding="utf-8")
    codigo, out, _ = por_main(tmp_path, capsys, """usar "lib.mate"
prueba "pide" { sea r = preguntar Pedir { que: "cafe" } a Deposito }
prueba "envia" { enviar Pedir { que: "cafe" } a Deposito }
""", orden="probar")
    assert codigo == 1
    assert 'lib.mate, línea 6: el mapa no tiene la clave "cafe"' in out
    assert 'Deposito al recibir Pedir (lib.mate, línea 6): el mapa no tiene la clave "cafe"' in out
    assert "6 |         responder stock[p.que]" in out


CAJA = """
mensaje Venta { n: numero }
mensaje Cuantas
mensaje Arrancar
agente Caja {
    estado ventas = 0
    al recibir Venta como v {
        ventas = ventas + 1
        enviar Cuantas {} a yo
        si v.n > 1 { responder 5 }
    }
    al recibir Cuantas { responder ventas }
}
agente Cliente { al recibir Arrancar { enviar Venta { n: 2 } a Caja } }
"""


def test_responder_mal_o_no_responder_tambien_deja_al_agente_como_estaba():
    salida, interprete = correr(CAJA + """
        enviar Arrancar {} a Cliente
        mostrar(preguntar Cuantas {} a Caja)
        intentar { preguntar Venta { n: 1 } a Caja } si falla e { mostrar("atajado") }
        mostrar(preguntar Cuantas {} a Caja)
    """)
    assert salida == ["0", "atajado", "0"]
    assert interprete.errores_agentes == [
        "Caja al recibir Venta: a un 'enviar' solo se le responde con un mensaje"]
    # el error señala al menos el 'al recibir' que estaba atendiendo
    assert [int(linea) for linea, _ in interprete.errores_agentes_det] == [7]
    assert len(interprete.cola) == 0


def test_el_error_de_un_agente_se_muestra_aunque_despues_corte_otro(tmp_path, capsys):
    codigo, _, err = por_main(tmp_path, capsys, """mensaje Cargar { producto: texto, precio: numero }
mensaje Precio { producto: texto }
agente Lista {
    estado precios = {}
    al recibir Cargar como c {
        si c.precio <= 0 { fallar "el precio tiene que ser mayor que cero" }
        precios[c.producto] = c.precio
    }
    al recibir Precio como p { responder precios[p.producto] }
}
enviar Cargar { producto: "yerba", precio: 0 } a Lista
mostrar(preguntar Precio { producto: "yerba" } a Lista)
""")
    assert codigo == 1
    causa = err.index("programa.mate:6: error: Lista al recibir Cargar: el precio tiene que ser")
    assert causa < err.index('programa.mate:9: error: el mapa no tiene la clave "yerba"')


def test_un_agente_no_cambia_lo_que_guarda_una_funcion_de_afuera():
    programa = """
        mensaje Tocar
        agente V { estado cb = nada
            al recibir Tocar { cb()
                responder 1 } }
        funcion hacer() {
            var n = 0
            funcion inc() { n = n + 1
                devolver n }
            devolver inc
        }
    """
    resultados = probar(programa + """
        prueba "variable de la prueba" {
            var cuenta = 0
            var visto = ""
            funcion sube() { cuenta = cuenta + 1 }
            sea w = crear V { cb: sube }
            intentar { preguntar Tocar {} a w } si falla e { visto = e }
            asegurar cuenta == 0
            asegurar tiene(visto, "no puede modificar 'cuenta'")
        }
    """)
    assert resultados == {"variable de la prueba": None}
    error = falla(programa + "sea contador = hacer()\n"
                  "agente W { al recibir Tocar { responder contador() } }\n"
                  "preguntar Tocar {} a W")
    assert error.mensaje.startswith("W no puede modificar 'n' (ni siquiera a través de la función inc())")
    # Las variables que nacen mientras el agente atiende sí son suyas.
    salida, _ = correr("""
        mensaje Tocar
        funcion contar_hasta(tope) {
            var k = 0
            funcion mas() { k = k + 1 }
            mientras k < tope { mas() }
            devolver k
        }
        agente X { estado z = 0
            al recibir Tocar { z = contar_hasta(3)
                responder z } }
        mostrar(preguntar Tocar {} a X)
    """)
    assert salida == ["3"]


def test_las_pruebas_empiezan_limpias_tambien_con_funciones_que_guardan_algo():
    resultados = probar("""
        funcion hacer() {
            var n = 0
            funcion inc() { n = n + 1
                devolver n }
            devolver inc
        }
        sea contador = hacer()
        contador()
        prueba "uno" { asegurar contador() == 2 }
        prueba "dos" { asegurar contador() == 2 }
    """)
    assert resultados == {"uno": None, "dos": None}


def test_en_las_pruebas_el_agente_arranca_como_arranco_en_el_programa():
    salida = []
    interprete = mate.Interprete(salida=salida.append)
    resultados = interprete.correr(mate.analizar("""
        var x = 1
        mensaje Ver
        mensaje Subir
        mensaje Hola
        agente Otro { al recibir Hola { fallar "soy yo" } }
        agente A {
            estado n = x
            estado ayudante = crear Otro
            al recibir Ver { responder n }
            al recibir Subir { n = n + 10
                enviar Hola {} a ayudante }
        }
        enviar Subir {} a A
        mostrar(preguntar Ver {} a A)
        x = 5
        prueba "estado inicial" { asegurar (preguntar Ver {} a A) == 1 }
        prueba "mismo nombre de copia" { enviar Subir {} a A }
    """), pruebas=True)
    assert salida == ["11"]
    assert interprete.errores_principal[0][1] == "Otro#2 al recibir Hola: soy yo"
    assert dict(resultados) == {"estado inicial": None,
                                "mismo nombre de copia": "Otro#2 al recibir Hola (línea 6): soy yo"}


def test_no_se_entregan_mensajes_a_un_agente_que_esta_naciendo():
    salida, interprete = correr("""
        mensaje Hola { n: numero }
        mensaje Dame
        enviar Hola { n: 1 } a A
        enviar Hola { n: 2 } a B
        enviar Hola { n: 3 } a A
        agente B {
            al recibir Hola como h { mostrar("B recibe {h.n}") }
            al recibir Dame { responder 7 }
        }
        agente A {
            estado base = preguntar Dame {} a B
            al recibir Hola como h { mostrar("A recibe {h.n} base {base}") }
        }
    """)
    assert salida == ["A recibe 1 base 7", "B recibe 2", "A recibe 3 base 7"]
    assert interprete.errores_agentes == []


def test_el_readme_avisa_los_cambios_que_frenan_programas_viejos():
    leeme = (RAIZ / "README.md").read_text(encoding="utf-8")
    assert "## Qué cambió y puede frenar un programa viejo" in leeme
    for frase in ["función incluida", "nunca responde", "Demasiada recursión", '`numero(".5")`',
                  "`redondear(x, -2)`", "12 cifras", "redacción de varios errores"]:
        assert frase in leeme, frase
    # y lo que el README promete sobre esos casos sigue siendo cierto
    assert "función incluida" in falla('funcion saludar(texto) { devolver texto }').mensaje
    assert falla('numero(".5")').mensaje == "'.5' no es un número"
    assert mostrado("3.141592653589793") == "3.14159265359"
    assert mostrado("a_json(3.141592653589793)") == "3.141592653589793"
    assert mostrado("redondear(1234 / 100) * 100") == "1200"
    assert mostrado("12345678.12345678 == numero(a_json(12345678.12345678))") == "verdadero"


def test_hablarle_a_un_agente_que_esta_naciendo_es_un_error_claro():
    error = falla("""
        mensaje Dame
        agente B { al recibir Dame { responder preguntar Dame {} a A } }
        agente A {
            estado base = preguntar Dame {} a B
            al recibir Dame { responder base }
        }
    """)
    assert "A todavía está armando su estado inicial" in error.mensaje


# ── Tanda 4: renglones, atajos y primeros pasos ──

# Mejora 37: lo que queda sin cerrar dice dónde se abrió

def test_la_llave_sin_cerrar_dice_donde_se_abrio():
    error = falla("mensaje Ping\n\nagente A {\n    al recibir Ping {\n        mostrar(1)\n\n"
                  "    al recibir Ping {\n        mostrar(2)\n    }\n}\n")
    assert error.mensaje == ("la llave que se abrió en la línea 4 (al recibir Ping) "
                             "nunca se cierra")
    error = falla("sea x = 1\nsi x == 1 {\n  mostrar(x)\n")
    assert error.mensaje == "la llave que se abrió en la línea 2 (si x == 1) nunca se cierra"


def test_parentesis_y_corchetes_sin_cerrar_dicen_donde_se_abrieron():
    assert falla("sea x = [1, 2\nmostrar(x)\n").mensaje == \
        "el corchete que se abrió en la línea 1 nunca se cierra"
    error = falla("si verdadero {\n  mostrar((1 + 2)\n}\n")
    assert error.mensaje == "el paréntesis que se abrió en la línea 2 nunca se cierra"
    # las llaves dentro de un texto no cuentan, y un cierre de más lo explica el análisis
    assert correr('mostrar("{1 + 1} \\{")')[0] == ["2 {"]
    assert "no esperaba '}'" in falla("mostrar(1)\n}\n").mensaje


# Mejora 38: un renglón que calcula algo y no lo usa

def test_un_renglon_que_calcula_y_no_usa_es_un_error():
    error = falla("sea i = 1\ni + 1\n")
    assert error.linea == 2 and "calcula un valor y no hace nada con él" in error.mensaje
    assert "calcula un valor" in falla('"hola"').mensaje
    assert falla("largo").mensaje == "a 'largo' le faltan los paréntesis: largo(...)"
    assert falla("funcion f() { devolver 1 }\nf\n").mensaje == \
        "a 'f' le faltan los paréntesis: f(...)"
    assert falla('mostrar "hola"').mensaje == "a 'mostrar' le faltan los paréntesis: mostrar(...)"


def test_una_funcion_incluida_suelta_avisa_que_hay_que_guardar_el_resultado():
    error = falla("sea lista = [1]\nagregar(lista, 4)\n")
    assert error.linea == 2 and error.mensaje.startswith("agregar() no cambia la lista")
    assert "lista = agregar(lista, ...)" in error.mensaje
    assert "largo() devuelve un valor y este renglón no lo usa" in falla('largo("abc")').mensaje
    # si la función falla, se ve ese error y no el de "no lo usa"
    assert falla('numero("x")').mensaje == "'x' no es un número"


def test_lo_que_hace_algo_puede_ir_suelto():
    salida, _ = correr("""
        mensaje Ping
        agente A { al recibir Ping { responder 1 } }
        funcion avisar(t) { mostrar(t) devolver 5 }
        avisar("hola")
        preguntar Ping {} a A
        crear A
        mostrar("chau")
    """)
    assert salida == ["hola", "chau"]


# Mejora 39: dónde termina un renglón

def test_un_menos_al_principio_del_renglon_no_se_pega_al_de_arriba():
    error = falla("sea x = 5\n-1\nmostrar(x)\n")
    assert error.linea == 2 and "dejá el '-' al final de ese renglón" in error.mensaje
    assert correr("funcion f() {\n  sea x = 5\n  devolver x\n}\nmostrar(f())")[0] == ["5"]


def test_un_renglon_no_empieza_con_un_operador():
    for operador in ["+", "*", "==", "y", "o"]:
        error = falla(f"sea a = verdadero\nsea x = a\n{operador} a\n")
        assert error.linea == 3, operador
        assert error.mensaje.startswith(f"un renglón no puede empezar con '{operador}'")


def test_la_cuenta_sigue_abajo_si_queda_algo_abierto_o_termina_en_operador():
    salida, _ = correr("""
        sea a = 5 +
            1
        sea b = (5
            - 1
            + 3)
        sea c = [1,
            -2]
        sea d = { uno: 1
            - 1 }
        sea e = a > 1 y
            b > 1
        mostrar(a, b, c, d, e)
    """)
    assert salida == ["6 7 [1, -2] {uno: 0} verdadero"]


def test_responder_fallar_y_asegurar_no_se_comen_el_renglon_de_abajo():
    error = falla("mensaje P\nagente A { al recibir P {\n responder\n mostrar(1)\n} }\n")
    assert error.linea == 3 and error.mensaje.startswith("a 'responder' le falta lo que sigue")
    assert falla('fallar\n"ups"\n').mensaje.startswith("a 'fallar' le falta lo que sigue")
    assert falla("asegurar\n1 == 1\n").mensaje.startswith("a 'asegurar' le falta lo que sigue")
    assert falla("mensaje P\nagente A { al recibir P { } }\nenviar\nP {} a A\n").linea == 3


# Mejora 40: un 'sea' de adentro no tapa una variable de afuera

def test_un_sea_de_adentro_no_tapa_una_variable_de_afuera():
    error = falla("var cuenta = 0\npara i en rango(3) {\n    sea cuenta = i\n}\n")
    assert error.linea == 3
    assert error.mensaje.startswith("'cuenta' ya existe afuera de este bloque")
    assert "sacá el 'sea'" in error.mensaje
    error = falla("funcion f(n) {\n  si n > 0 {\n    var n = 1\n  }\n}\nf(1)\n")
    assert error.linea == 3 and "'n' ya existe afuera" in error.mensaje
    _, interprete = correr("""
        mensaje P
        agente A {
            estado ventas = 0
            al recibir P { sea ventas = 1 }
        }
        enviar P {} a A
    """)
    assert "'ventas' es un estado de este agente" in interprete.errores_agentes[0]


def test_una_funcion_o_una_prueba_si_pueden_repetir_un_nombre_de_afuera():
    salida, _ = correr("""
        sea total = 10
        funcion doble(n) {
            sea total = n * 2
            devolver total
        }
        para i en rango(2) { sea propio = i }
        para i en rango(2) { sea propio = i }
        mostrar(doble(4), total)
    """)
    assert salida == ["8 10"]
    interprete = mate.Interprete(salida=lambda _: None)
    resultados = interprete.correr(mate.analizar(
        'sea c = 1\nprueba "p" { sea c = 2\n asegurar c == 2 }'), pruebas=True)
    assert resultados == [("p", None)]


# Mejora 41: comparar un texto con un número

def test_comparar_un_texto_con_un_numero_es_un_error():
    error = falla('sea edad = "18"\nsi edad == 18 { mostrar("sí") }')
    assert error.linea == 2
    assert error.mensaje.startswith('no se puede comparar un texto con un número ("18" == 18)')
    assert 'numero("18")' in error.mensaje
    assert "comparar un texto con un número" in falla('mostrar(1.5 != "a")').mensaje


def test_comparar_con_nada_y_entre_otros_tipos_sigue_permitido():
    assert mostrado('nada == "a"') == "falso"
    assert mostrado("1 != nada") == "verdadero"
    assert mostrado("1 == verdadero") == "falso"
    assert mostrado('"18" == texto(18)') == "verdadero"
    assert mostrado('tiene(["18"], 18)') == "falso"  # buscar en una lista no es un error


def test_la_igualdad_no_convierte_adentro_de_listas_mapas_ni_mensajes():
    assert mostrado("[1] == [verdadero]") == "falso"
    assert mostrado("{ a: 1 } == { a: verdadero }") == "falso"
    assert mostrado("[1, [2.0]] == [1.0, [2]]") == "verdadero"
    assert mostrado("tiene([[verdadero]], [1])") == "falso"
    salida, _ = correr("mensaje M { v: cualquiera }\nmostrar(M { v: 1 } == M { v: verdadero }, "
                       "M { v: [1] } == M { v: [1] })")
    assert salida == ["falso verdadero"]


# Mejoras 42 y 44: primeros pasos en Windows y mate.bat

def test_el_readme_trae_los_primeros_pasos_en_windows():
    leeme = (RAIZ / "README.md").read_text(encoding="utf-8")
    assert "## Primeros pasos en Windows" in leeme
    for frase in ["python.org", "Add python.exe to PATH", "PowerShell", "Bloc de notas",
                  "Todos los archivos", "python --version",
                  "python mate\\mate.py correr hola.mate", ".\\mate\\mate correr hola.mate"]:
        assert frase in leeme, frase


def test_mate_bat_esta_listo_para_windows():
    crudo = (RAIZ / "mate.bat").read_bytes()
    assert crudo.isascii()  # sin tildes: la consola de Windows las mostraría mal
    assert b"\r\n" in crudo and b"\n" not in crudo.replace(b"\r\n", b"")
    texto = crudo.decode("ascii")
    assert "%~dp0mate.py" in texto and "%*" in texto and "pause" in texto


# Mejora 43: ejemplos graduales

GRADUALES = sorted(p.name for p in (RAIZ / "ejemplos").glob("0*.mate"))


def test_estan_los_seis_ejemplos_graduales():
    assert [n[:2] for n in GRADUALES] == ["01", "02", "03", "04", "05", "06"]
    assert GRADUALES[0] == "01_hola.mate" and GRADUALES[-1] == "06_primer_agente.mate"
    for nombre in GRADUALES:  # están comentados: al menos un comentario cada cuatro renglones
        renglones = [r.strip() for r in (RAIZ / "ejemplos" / nombre).read_text(
            encoding="utf-8").splitlines() if r.strip()]
        assert 4 * sum(r.startswith("#") for r in renglones) >= len(renglones), nombre


@pytest.mark.parametrize("nombre", GRADUALES)
def test_los_ejemplos_graduales_corren_y_pasan_sus_pruebas(nombre, capsys):
    ruta = str(RAIZ / "ejemplos" / nombre)
    assert mate.main(["verificar", ruta]) == 0
    assert mate.main(["correr", ruta]) == 0
    capturado = capsys.readouterr()
    assert capturado.err == "" and len(capturado.out.splitlines()) >= 3
    assert mate.main(["probar", ruta]) == 0
    assert "✗" not in capsys.readouterr().out


def test_los_ejemplos_graduales_muestran_lo_que_dicen_sus_comentarios(capsys):
    assert mate.main(["correr", str(RAIZ / "ejemplos" / "01_hola.mate")]) == 0
    assert capsys.readouterr().out == "Hola, mundo\n1 + 1 es 2\nMate amargo 3\n"
    assert mate.main(["correr", str(RAIZ / "ejemplos" / "02_variables.mate")]) == 0
    assert capsys.readouterr().out.splitlines()[0] == "Total: $ 8.000,00"
    assert mate.main(["correr", str(RAIZ / "ejemplos" / "06_primer_agente.mate")]) == 0
    assert capsys.readouterr().out == ("Dos de yerba salen $ 7.000\n"
                                       "Después del aumento salen $ 8.000\n")


# Mejora 45: la orden 'guia'

def test_la_guia_nombra_todas_las_palabras_y_funciones(capsys):
    assert mate.main(["guia"]) == 0
    guia = capsys.readouterr().out
    assert guia.startswith(f"GUÍA DE MATE {mate.VERSION}")
    palabras = set(re.findall(r"\w+", guia))
    assert sorted(mate.PALABRAS - palabras) == []
    assert sorted(mate.incluidas() - palabras) == []
    assert sorted(mate.TIPOS_BASE - palabras) == []
    assert max(len(r) for r in guia.splitlines()) <= 100


def test_el_ejemplo_de_la_guia_anda(tmp_path, capsys):
    ejemplo = mate.texto_de_guia().split("--- ejemplo ---")[1].split("--- fin del ejemplo ---")[0]
    codigo, salida, err = por_main(tmp_path, capsys, ejemplo, orden="probar")
    assert (codigo, err) == (0, "")
    assert salida.splitlines() == ["Se saltea: no vendo café", "Total: $ 7.000,00",
                                   "  ✓ suma solo lo que el vendedor vende",
                                   "1 de 1 pruebas pasaron"]


def test_la_ayuda_y_los_errores_de_tipeo_conocen_la_guia(capsys):
    assert mate.main(["ayuda"]) == 0
    assert "guia " in capsys.readouterr().out
    assert mate.main(["gia"]) == 2
    assert "¿quisiste decir 'guia'?" in capsys.readouterr().err


# Mejora 46: += y -=

def test_los_atajos_mas_igual_y_menos_igual():
    salida, _ = correr("""
        var suma = 10
        suma += 5
        suma -= 2
        var m = { a: [1], t: "ho" }
        m.a[0] += 4
        m.t += "la"
        var l = [1]
        l += [2]
        mostrar(suma, m, l)
    """)
    assert salida == ['13 {a: [5], t: "hola"} [1, 2]']


def test_los_atajos_dan_los_errores_de_siempre():
    assert falla("sea s = 1\ns += 2").mensaje == \
        "'s' es fijo (sea); declaralo con 'var' para cambiarlo"
    assert falla("3 += 2").mensaje.startswith("solo se puede asignar a una variable")
    assert "numero + texto" in falla('var s = 1\ns += "a"').mensaje
    assert "no existe 'totl'" in falla("var total = 1\ntotl += 1").mensaje
    error = falla("var s = 1\ns *= 2")
    assert error.linea == 2 and error.mensaje.startswith("los únicos atajos son '+=' y '-='")


# Mejora 47: romper y continuar

def test_romper_y_continuar_en_para_y_mientras():
    salida, _ = correr("""
        var vistos = []
        para i en rango(10) {
            si i == 1 { continuar }
            si i == 4 { romper }
            vistos += [i]
        }
        var n = 0
        mientras verdadero {
            n += 1
            si n % 2 == 1 { continuar }
            intentar {
                si n >= 6 { romper }
            } si falla { mostrar("romper no es un error") }
        }
        var pares = 0
        para i en rango(3) {
            para j en rango(3) {
                si j == 1 { romper }
                pares += 1
            }
        }
        mostrar(vistos, n, pares)
    """)
    assert salida == ["[0, 2, 3] 6 3"]


def test_romper_y_continuar_fuera_de_un_bucle_se_avisan_antes_de_correr():
    for palabra in ["romper", "continuar"]:
        esperado = f"'{palabra}' solo va dentro de un 'mientras' o de un 'para'"
        assert falla(f'mostrar("antes")\n{palabra}\n').mensaje == esperado
        assert falla(f"si verdadero {{ {palabra} }}").mensaje == esperado
        # una función declarada dentro de un bucle no está "dentro" del bucle
        assert falla(f"mientras verdadero {{\n funcion f() {{ {palabra} }}\n}}").mensaje == esperado
    assert "palabra propia de Mate" in falla("sea romper = 1").mensaje
    assert falla("para i en rango(3) { break }").mensaje == "en Mate 'break' se escribe 'romper'"
    assert falla("para i en rango(3) { continue }").mensaje == \
        "en Mate 'continue' se escribe 'continuar'"


def test_el_freno_sigue_cortando_un_bucle_que_solo_continua():
    interprete = mate.Interprete(salida=lambda _: None)
    interprete.max_pasos = 500
    with pytest.raises(mate.ErrorMate) as info:
        interprete.correr(mate.analizar("mientras verdadero { continuar }"))
    assert info.value.clase == "limite"


# Mejora 48: leer()

def correr_con_teclado(fuente, respuestas, pruebas=False):
    salida, preguntas, respuestas = [], [], list(respuestas)

    def teclado(pregunta):
        preguntas.append(pregunta)
        if not respuestas:
            raise EOFError
        return respuestas.pop(0)

    interprete = mate.Interprete(salida=salida.append)
    interprete.entrada = teclado
    resultados = interprete.correr(mate.analizar(fuente), pruebas=pruebas)
    return salida, preguntas, resultados


def test_leer_le_pide_un_dato_a_la_persona():
    salida, preguntas, _ = correr_con_teclado(
        'sea nombre = leer("¿Cómo te llamás?")\nsea edad = numero(leer("¿Edad?"))\n'
        'leer("Enter para seguir")\nmostrar("Hola {nombre}, el año que viene tenés {edad + 1}")',
        ["  Ana \n", "30", ""])
    assert preguntas == ["¿Cómo te llamás?", "¿Edad?", "Enter para seguir"]
    assert salida == ["Hola Ana, el año que viene tenés 31"]


def test_leer_en_las_pruebas_usa_la_respuesta_preparada():
    fuente = ('funcion saludo() { devolver "Hola " + leer("¿Nombre?", "Pepe") }\n'
              'mostrar(saludo())\nprueba "saluda" { asegurar saludo() == "Hola Pepe" }')
    salida, preguntas, resultados = correr_con_teclado(fuente, ["Ana"], pruebas=True)
    assert (salida, preguntas, resultados) == (["Hola Pepe"], [], [("saluda", None)])
    # al correr de verdad se usa lo que escribe la persona
    assert correr_con_teclado(fuente, ["Ana"])[0] == ["Hola Ana"]
    # y si no hay teclado (la entrada está cerrada), la preparada
    assert correr_con_teclado(fuente, [])[0] == ["Hola Pepe"]
    with pytest.raises(mate.ErrorMate) as info:
        correr_con_teclado('leer("¿Nombre?")', [], pruebas=True)
    assert "dale una respuesta preparada" in info.value.mensaje
    with pytest.raises(mate.ErrorMate) as info:
        correr_con_teclado('leer("¿Nombre?")', [])
    assert "no hay nadie para contestar" in info.value.mensaje


def test_un_agente_no_puede_leer_del_teclado():
    with pytest.raises(mate.ErrorMate) as info:
        correr_con_teclado("""
            mensaje P
            agente A { al recibir P { responder leer("¿Qué contesto?") } }
            mostrar(preguntar P {} a A)
        """, ["algo"])
    assert info.value.mensaje.startswith("leer() solo se usa desde el programa principal")
    assert falla("leer(5)").mensaje == "leer() espera texto y recibió numero"
    assert "función incluida" in falla('sea leer = "x"').mensaje


def test_leer_por_la_linea_de_comandos(tmp_path):
    archivo = tmp_path / "saludo.mate"
    archivo.write_text('sea n = leer("¿Nombre?")\nmostrar("Hola {n}")\n', encoding="utf-8")
    r = subprocess.run([sys.executable, str(RAIZ / "mate.py"), "correr", str(archivo)],
                       input="Ana\n", capture_output=True, encoding="utf-8",
                       env=dict(os.environ, PYTHONIOENCODING="utf-8"))
    assert (r.returncode, r.stdout, r.stderr) == (0, "¿Nombre? Hola Ana\n", "")
    r = subprocess.run([sys.executable, str(RAIZ / "mate.py"), "correr", str(archivo)],
                       input="", capture_output=True, encoding="utf-8",
                       env=dict(os.environ, PYTHONIOENCODING="utf-8"))
    assert r.returncode == 1 and "no hay nadie para contestar" in r.stderr
    assert "Traceback" not in r.stderr


def test_el_readme_avisa_lo_que_cambio_en_la_tanda_4():
    leeme = (RAIZ / "README.md").read_text(encoding="utf-8")
    for frase in ["calcula un valor y no hace nada", "no puede empezar con", "ya existe afuera",
                  "comparar un texto con un número", "`romper`", "`continuar`", "`leer`",
                  "total += precio", "mate.py guia", "01_hola.mate"]:
        assert frase in leeme, frase
