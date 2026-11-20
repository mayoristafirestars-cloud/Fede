"""Pruebas del intérprete de Mate. Correr con: python3 -m pytest mate/pruebas -q"""

import pathlib
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
