"""Pruebas del intérprete de Mate. Correr con: python3 -m pytest mate/pruebas -q"""

import pathlib
import re
import sys

import pytest

RAIZ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

import mate  # noqa: E402


@pytest.fixture(autouse=True)
def sin_red_ni_clave(monkeypatch):
    """Ninguna prueba sale a la red ni usa una clave de verdad (mejora 100)."""
    import urllib.request

    def nadie_sale(*_a, **_k):
        raise AssertionError("una prueba quiso salir a la red")

    monkeypatch.setattr(urllib.request, "urlopen", nadie_sale)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("MATE_MODELO", raising=False)
    monkeypatch.setattr(mate, "_IA_SIN_RESPALDO", set())


def correr(fuente, traza=False):
    salida = []
    interprete = mate.Interprete(salida=salida.append, traza=traza)
    programa = mate.analizar(fuente)
    assert mate.verificar(programa) == []
    interprete.correr(programa)
    return salida, interprete


def falla(fuente):
    """El error que da ese programa: el que avisa la revisión previa (un nombre que no
    existe, una llamada con valores de más: mejora 59) o, si esa pasa, el de correrlo."""
    try:
        antes = mate.verificar(mate.analizar(fuente))
    except mate.ErrorMate as mal_escrito:
        return mal_escrito
    if antes:
        error = mate.ErrorMate(antes[0][1], antes[0][0])
        error.antes_de_correr = True
        return error
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
    assert "condición" in falla("sea uno = 1\nsi uno { mostrar(1) }").mensaje
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
    assert ("  ·  3. Calculadora → Cliente: Resultado { valor: 2 }   (conversación 1, en "
            "respuesta al 2)") in salida


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
        "  ·  1. (programa) → Coordinador: Encargo { tema: \"ventas\" }   (conversación 1)\n"
        "  ·  2. (programa) → Coordinador: Encargo { tema: \"stock\" }   (conversación 2)\n"
        "  ·  3. Coordinador → Investigador: Investigar { tema: \"ventas\" }   (conversación 1)\n"
        "  ·  4. Coordinador → Investigador: Investigar { tema: \"stock\" }   (conversación 2)\n"
        "  ·  5. Investigador → Coordinador: Hallazgos { tema: \"ventas\", datos: [\"subieron 12%\", \"yerba es lo más vendido\"] }   (conversación 1, en respuesta al 3)\n"
        "  ·  6. Investigador → Coordinador: Hallazgos { tema: \"stock\", datos: [\"quedan 40 cajas\"] }   (conversación 2, en respuesta al 4)\n"
        "  ·  7. Coordinador → Redactor: Redactar { tema: \"ventas\", datos: [\"subieron 12%\", \"yerba es lo más vendido\"] }   (conversación 1)\n"
        "  ·  8. Coordinador → Redactor: Redactar { tema: \"stock\", datos: [\"quedan 40 cajas\"] }   (conversación 2)\n"
        "  ·  9. Redactor → Coordinador: Borrador { texto: \"VENTAS: subieron 12%; yerba es lo más vendido\" }   (conversación 1, en respuesta al 7)\n"
        "Listo: VENTAS: subieron 12%; yerba es lo más vendido\n"
        "  · 10. Redactor → Coordinador: Borrador { texto: \"STOCK: quedan 40 cajas\" }   (conversación 2, en respuesta al 8)\n"
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
        "  ·  1. (programa) → Comprador: Comprar { producto: \"yerba\", cantidad: 10, vendedores: [<agente Vendedor Norte>, <agente Vendedor Sur>, <agente Vendedor Centro>] }   (conversación 1)\n"
        "  ·  2.    Comprador pregunta a Vendedor Norte: Pedido { producto: \"yerba\", cantidad: 10 }\n"
        "  ·  2.    Vendedor Norte responde a Comprador: Cotizacion { vendedor: <agente Vendedor Norte>, producto: \"yerba\", total: 33250 }\n"
        "Vendedor Norte cotiza 33250\n"
        "  ·  3.    Comprador pregunta a Vendedor Sur: Pedido { producto: \"yerba\", cantidad: 10 }\n"
        "  ·  3.    Vendedor Sur responde a Comprador: Cotizacion { vendedor: <agente Vendedor Sur>, producto: \"yerba\", total: 33000 }\n"
        "Vendedor Sur cotiza 33000\n"
        "  ·  4.    Comprador pregunta a Vendedor Centro: Pedido { producto: \"yerba\", cantidad: 10 }\n"
        "  ·  4.    Vendedor Centro responde a Comprador: Cotizacion { vendedor: <agente Vendedor Centro>, producto: \"yerba\", total: 35000 }\n"
        "Vendedor Centro cotiza 35000\n"
        "Compro 10 de yerba a Vendedor Sur por 33000\n"
        "  ·  1. la respuesta de Comprador se descartó (para recibirla, usá 'preguntar' en vez de 'enviar'): Cotizacion { vendedor: <agente Vendedor Sur>, producto: \"yerba\", total: 33000 }\n"
        "  ·  5. (programa) → Comprador: Comprar { producto: \"azucar\", cantidad: 4, vendedores: [<agente Vendedor Norte>, <agente Vendedor Sur>, <agente Vendedor Centro>] }   (conversación 2)\n"
        "  ·  6.    Comprador pregunta a Vendedor Norte: Pedido { producto: \"azucar\", cantidad: 4 }\n"
        "  ·  6.    Vendedor Norte responde a Comprador: Cotizacion { vendedor: <agente Vendedor Norte>, producto: \"azucar\", total: 4560 }\n"
        "Vendedor Norte cotiza 4560\n"
        "  ·  7.    Comprador pregunta a Vendedor Sur: Pedido { producto: \"azucar\", cantidad: 4 }\n"
        "  ·  7.    Vendedor Sur falló: no vendo azucar\n"
        "Vendedor Sur no puede: no vendo azucar\n"
        "  ·  8.    Comprador pregunta a Vendedor Centro: Pedido { producto: \"azucar\", cantidad: 4 }\n"
        "  ·  8.    Vendedor Centro responde a Comprador: Cotizacion { vendedor: <agente Vendedor Centro>, producto: \"azucar\", total: 4800 }\n"
        "Vendedor Centro cotiza 4800\n"
        "Compro 4 de azucar a Vendedor Norte por 4560\n"
        "  ·  5. la respuesta de Comprador se descartó (para recibirla, usá 'preguntar' en vez de 'enviar'): Cotizacion { vendedor: <agente Vendedor Norte>, producto: \"azucar\", total: 4560 }\n"
    )),
    ("negociacion", False): (0, (
        "Me cotizaron 10500 por 3 de yerba\n"
        "Cerramos en 9600.\n"
    )),
    ("negociacion", True): (0, (
        "  ·  1. (programa) → Comprador: Iniciar { producto: \"yerba\", cantidad: 3, presupuesto: 9600 }   (conversación 1)\n"
        "  ·  2.    Comprador pregunta a Vendedor: Pedido { producto: \"yerba\", cantidad: 3 }\n"
        "  ·  2.    Vendedor responde a Comprador: Cotizacion { producto: \"yerba\", total: 10500 }\n"
        "Me cotizaron 10500 por 3 de yerba\n"
        "  ·  3.    Comprador pregunta a Vendedor: Contraoferta { producto: \"yerba\", total: 9600 }\n"
        "  ·  3.    Vendedor responde a Comprador: Trato { aceptado: verdadero, total: 9600 }\n"
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
    assert b'  -  1. (programa) -> Coordinador: Encargo { tema: "ventas" }' in r.stdout


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
    assert falla("redondear(1, 2, 3)").mensaje == \
        "redondear() lleva 1 o 2 valores y recibió 3. Por ejemplo: redondear(3.14159, 2)"
    assert falla("largo()").mensaje == \
        "largo() lleva 1 valor y recibió 0. Por ejemplo: largo(lista)"
    assert falla("tiene(1)").mensaje == \
        "tiene() lleva 2 valores y recibió 1. Por ejemplo: tiene(lista, x)"
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
    assert falla(mapa + 'mostrar(m["zzz"])').mensaje == \
        'el mapa no tiene la clave "zzz" (tiene: nombre, precio)'
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
    assert "'mi_estado'" in falla("var Estado = 1\nEstado = 2\nmostrar(Estado)").mensaje


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
    assert "condición" in falla("sea uno = 1\nasegurar uno").mensaje


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
    assert error.mensaje.startswith("demasiada recursión") and error.clase == "limite"
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
    assert resultados["dos errores"] == ("línea 2: Roto al recibir Ping: me rompí 1\n"
                                         "línea 2: Roto al recibir Ping: me rompí 2")


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
        "línea 5: Eco al recibir Ping: Eco respondió Pong a Sordo, pero Sordo no tiene "
        "'al recibir Pong'"]  # (mejora 68: ahora trae el renglón del 'responder')


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
    assert correr("funcion crea(x) { devolver x }\ncrea(3)\nmostrar(crea(4))")[0] == ["4"]
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
    archivo = tmp_path / "programa.mate"
    assert renglones[1:5] == [  # el error de la prueba y el del agente se escriben igual
        f"{archivo}:14: error: no se cumplió lo asegurado: dio 0 y se esperaba 5",
        "14 |     asegurar r == 5",
        f"{archivo}:6: error: C al recibir Sumar: no acepto más de 3",
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
    assert 'lib.mate:6: error: el mapa no tiene la clave "cafe"' in out
    assert 'lib.mate:6: error: Deposito al recibir Pedir: el mapa no tiene la clave "cafe"' in out
    assert "programa.mate:" not in out  # los dos errores están en el archivo traído
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
        "línea 10: Caja al recibir Venta: a un 'enviar' solo se le responde con un mensaje"]
    # el error señala el renglón del 'responder' (mejora 68; antes, solo el 'al recibir')
    assert [int(linea) for linea, _ in interprete.errores_agentes_det] == [10]
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
                                "mismo nombre de copia": "línea 6: Otro#2 al recibir Hola: soy yo"}


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


def test_estan_los_seis_ejemplos_graduales():  # (y el séptimo, el de la IA: mejora 100)
    assert [n[:2] for n in GRADUALES] == ["01", "02", "03", "04", "05", "06", "07"]
    assert GRADUALES[0] == "01_hola.mate" and GRADUALES[-1] == "07_agente_con_ia.mate"
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


# ── Tanda 5: textos y números sin trampas, más funciones y más controles ──

def mostrados(fuente):
    return correr(fuente)[0]


# Mejora 49: comillas dentro de "{...}"

def test_comillas_dentro_de_las_llaves_de_un_texto():
    assert mostrados('sea m = { a: 1, "b c": 2 }\n'
                     'mostrar("valor {m["a"]} y {m["b c"]} y {unir(["x", "y"], "-")}.")') == [
        "valor 1 y 2 y x-y."]
    assert mostrados('mostrar("afuera {"adentro {1 + 1} }"} fin")') == ["afuera adentro 2 } fin"]
    assert mostrados('mostrar("{largo("}")}", "{"\\{"}")') == ["1 {"]
    assert mostrados('mostrar(“con comillas de Word {unir(["a"], "")}”)') == [
        "con comillas de Word a"]
    # lo que ya era un error lo sigue siendo, con la misma explicación
    assert "falta '}'" in falla('mostrar("falta { algo")').mensaje
    assert "comilla de cierre" in falla('mostrar("a {m["a} b")').mensaje
    assert "otras comillas" not in mate.texto_de_guia()


# Mejora 50: las barras de las rutas de Windows

def test_las_barras_de_windows_no_se_rompen_en_silencio():
    error = falla('sea a = 1\nmostrar("C:\\temp\\nuevo")')
    assert error.linea == 2 and "ruta de Windows" in error.mensaje
    assert '"C:/datos/lista.txt"' in error.mensaje and "doble barra" in error.mensaje
    error = falla('mostrar("datos\\archivo.txt")')
    assert "\\a no significa nada" in error.mensaje and "doble barra" in error.mensaje
    assert mostrados('mostrar("C:\\\\temp\\\\nuevo", "C:/temp/nuevo")') == [
        "C:\\temp\\nuevo C:/temp/nuevo"]
    assert mostrados('mostrar("a\\tb\\nc \\"x\\" \\{ \\}")') == ['a\tb\nc "x" { }']


# Mejora 51: 1.500 y 3,5 escritos en el código

def test_aviso_para_miles_con_punto_y_decimales_con_coma():
    error = falla("sea a = 1\nsea precio = 1.500")
    assert error.linea == 2
    assert "1.500 vale 1.5, no 1500" in error.mensaje and "1_500" in error.mensaje
    assert "12.000 vale 12, no 12000" in falla("mostrar(12.000 * 2)").mensaje
    assert "un solo punto" in falla("sea x = 1.500.000").mensaje
    assert falla("sea x = 3,5").mensaje == "los decimales van con punto, no con coma: 3.5"
    assert "decimales van con punto" in falla("si 4 > 3,5 { mostrar(1) }").mensaje
    assert mostrados("mostrar(1_500, 1_500_000 + 1, 1.5, 2.125, 0.250, 1500.5)") == [
        "1500 1500001 1.5 2.125 0.25 1500.5"]
    # adentro de paréntesis o corchetes la coma separa valores, como siempre
    assert mostrados("mostrar(3,5)\nmostrar([3,5], sumar([1,2]))") == ["3 5", "[3, 5] 3"]


# Mejora 52: errores que no se leen como otra frase

def test_los_errores_con_nada_no_se_leen_como_otra_frase():
    error = falla("funcion precio(p) { sea x = p }\nmostrar(precio(1) + 10)")
    assert error.linea == 2
    assert error.mensaje.startswith("no se puede sumar el valor nada con un número.")
    assert "¿a la función le falta un 'devolver'" in error.mensaje
    assert falla('mostrar("a" * nada)').mensaje.startswith(
        "no se puede multiplicar un texto con el valor nada.")
    for fuente, frase in [
            ("mostrar(nada.campo)", "el valor nada no tiene campos"),
            ("mostrar(nada[0])", "el valor nada no tiene posiciones ni claves"),
            ("mostrar(1 < nada)", "no se puede comparar un número con el valor nada"),
            ("sea v = nada\nsi v { mostrar(1) }", "verdadero o falso, no el valor nada"),
            ("mostrar(largo(nada))", "largo() no aplica al valor nada"),
            ("mostrar(numero(nada))", "numero() espera texto y recibió el valor nada"),
            ("para x en nada { mostrar(x) }", "no se puede recorrer el valor nada"),
            ("sea f = nada\nf()", "el valor nada no es una función")]:
        mensaje = falla(fuente).mensaje
        assert frase in mensaje, mensaje
        assert not re.search(r"(hacer|recibió|recorrer|comparar|a|con|no) nada\b", mensaje), mensaje
    # sin 'nada' de por medio, los mensajes de siempre
    assert falla("mostrar(1 + verdadero)").mensaje == "no se puede hacer numero + logico"
    assert falla('mostrar("a" < 1)').mensaje == "no se puede comparar texto con numero"


# Mejora 53: una tabla única de funciones incluidas

def test_la_tabla_de_funciones_es_la_unica_fuente():
    interprete = mate.Interprete(salida=lambda _: None)
    assert sorted(interprete.glob.vars) == sorted(mate.FUNCIONES)
    assert mate.incluidas() == frozenset(mate.FUNCIONES)
    leeme = (RAIZ / "README.md").read_text(encoding="utf-8")
    guia = mate.texto_de_guia()
    for nombre, (minimo, maximo, ejemplo, que) in mate.FUNCIONES.items():
        assert ejemplo.startswith(nombre + "("), nombre
        assert f"- {ejemplo}" in guia and que in guia, nombre
        assert f"| `{ejemplo}` | {que} |" in leeme, nombre
        # el ejemplo de la tabla respeta la cantidad de valores que dice la tabla
        llamada = mate.analizar(f"sea x = {ejemplo}")[0][3]
        assert llamada[0] == "llamar" and minimo <= len(llamada[3]), nombre
        assert maximo is None or len(llamada[3]) <= maximo, nombre


def test_el_error_de_cantidad_de_valores_trae_un_ejemplo():
    assert falla("mostrar(obtener({}, 1))").mensaje == \
        'obtener() lleva 3 valores y recibió 2. Por ejemplo: obtener(mapa, "clave", 0)'
    assert falla("mostrar(rango())").mensaje == \
        "rango() lleva entre 1 y 3 valores y recibió 0. Por ejemplo: rango(1, 10, 3)"
    assert mostrados("mostrar()") == [""]


# Mejora 54: funciones de texto

def test_funciones_de_texto_nuevas():
    assert mostrados('mostrar(recortar("  hola  \\n") + "|", reemplazar("a-b-c", "-", " y "))') == [
        "hola| a y b y c"]
    assert mostrados('mostrar(empieza_con("Sr. Paz", "Sr."), empieza_con("Paz", "Sr."), '
                     'termina_con("a.txt", ".txt"), termina_con("a.txt", ".mate"))') == [
        "verdadero falso verdadero falso"]
    assert falla("mostrar(recortar(5))").mensaje == "recortar() espera texto y recibió numero"
    assert "no puede estar vacío" in falla('mostrar(reemplazar("a", "", "b"))').mensaje
    assert "espera texto" in falla('mostrar(empieza_con("a", 1))').mensaje
    assert "función incluida" in falla('sea recortar = 1').mensaje


# Mejora 55: funciones de listas y números

def test_funciones_de_listas_y_numeros_nuevas():
    assert mostrados("mostrar(minimo([3, 1, 2]), maximo([3, 1.5, 2]), promedio([4, 6]), "
                     "promedio([1, 2]), absoluto(-5), absoluto(2.5))") == ["1 3 5 1.5 5 2.5"]
    assert mostrados('mostrar(ultimo([1, 2, 3]), ultimo("abc"), minimo(["pera", "Ananá"]))') == [
        "3 c Ananá"]
    assert mostrados('mostrar(porcion([0, 1, 2, 3, 4], 1, 3), porcion("hola mundo", 5), '
                     "porcion([1, 2], 0, 99), porcion([1, 2], 2))") == ["[1, 2] mundo [1, 2] []"]
    assert mostrados("mostrar(rango(1, 10, 3), rango(5, 0, -2), rango(3), rango(2, 5))") == [
        "[1, 4, 7] [5, 3, 1] [0, 1, 2] [2, 3, 4]"]
    for fuente, frase in [
            ("minimo([])", "no puede con una lista vacía"),
            ("promedio([])", "no puede con una lista vacía"),
            ('maximo([1, "a"])', "sin mezclar"),
            ('promedio(["a"])', "promedio() espera una lista de números"),
            ("ultimo([])", "una lista vacía"),
            ('absoluto("a")', "absoluto() espera numero y recibió texto"),
            ("porcion([1], 2, 1)", "no puede ser mayor"),
            ("porcion([1], -1)", "de 0 en adelante"),
            ("porcion([1], 0.5)", "de 0 en adelante"),
            ("rango(1, 5, 0)", "no puede ser 0"),
            ("rango(0, 100000000000, 1)", "demasiados números"),
            ("minimo(3, 5)", "Por ejemplo: minimo([3, 1, 2])")]:
        assert frase in falla(f"mostrar({fuente})").mensaje, fuente


# Mejora 56: obtener() y el error que lista las claves que sí hay

def test_obtener_y_el_error_de_clave_que_lista_las_que_hay():
    mapa = 'sea m = { yerba: 3500, azucar: 1200 }\n'
    assert mostrados(mapa + 'mostrar(obtener(m, "yerba", 0), obtener(m, "café", 0), '
                            'obtener(m, "café", nada))') == ["3500 0 nada"]
    assert falla(mapa + 'mostrar(m["cafe"])').mensaje == \
        'el mapa no tiene la clave "cafe" (tiene: yerba, azucar)'
    assert falla(mapa + 'mostrar(m["Yerba"])').mensaje == \
        'el mapa no tiene la clave "Yerba". ¿Quisiste decir \'yerba\'?'
    assert falla(mapa + "mostrar(m.cafe)").mensaje == \
        "mapa no tiene un campo 'cafe' (tiene: yerba, azucar)"
    assert falla('sea v = {}\nmostrar(v["a"])').mensaje == \
        'el mapa no tiene la clave "a" (está vacío)'
    muchas = "{ " + ", ".join(f"k{i}: {i}" for i in range(12)) + " }"
    assert falla(f'mostrar({muchas}["zzz"])').mensaje.endswith("k6, k7, ...)")
    assert "espera mapa" in falla('mostrar(obtener([1], "a", 0))').mensaje
    assert "claves de un mapa son textos" in falla("mostrar(obtener({}, 1, 0))").mensaje


# Mejora 57: ordenar por campo y con el abecedario español

def test_ordenar_usa_el_abecedario_y_ordena_por_campo():
    assert mostrados('mostrar(ordenar(["zapallo", "Ñandú", "ananá", "Banana", "nuez", '
                     '"ñoqui", "oso", "árbol"]))') == [
        '["ananá", "árbol", "Banana", "nuez", "Ñandú", "ñoqui", "oso", "zapallo"]']
    assert mostrados("mostrar(ordenar([3, 1.5, 2, 10]))") == ["[1.5, 2, 3, 10]"]
    productos = ('sea productos = [{ nombre: "yerba", precio: 3500 }, '
                 '{ nombre: "Azúcar", precio: 1200 }, { nombre: "café", precio: 9000 }]\n')
    assert mostrados(productos + 'para p en ordenar(productos, "precio") { mostrar(p.nombre) }\n'
                     'mostrar(productos[0].nombre)') == ["Azúcar", "yerba", "café", "yerba"]
    assert mostrados(productos + 'para p en ordenar(productos, "nombre") { mostrar(p.nombre) }') \
        == ["Azúcar", "café", "yerba"]
    assert mostrados('mensaje P { n: numero }\n'
                     'mostrar(ordenar([P { n: 2 }, P { n: 1 }], "n"))') == [
        "[P { n: 1 }, P { n: 2 }]"]
    assert falla(productos + 'mostrar(ordenar(productos, "precoi"))').mensaje == \
        "ordenar(): un elemento de la lista no tiene 'precoi'. ¿Quisiste decir 'precio'?"
    assert "sin mezclar" in falla('mostrar(ordenar([{ a: 1 }, { a: "x" }], "a"))').mensaje
    assert "lista de mapas o de mensajes" in falla('mostrar(ordenar([1, 2], "a"))').mensaje
    assert "comparables" in falla('mostrar(ordenar([1, "a"]))').mensaje


# Mejora 58: errores de posición más claros

def test_los_errores_de_posicion_dicen_cuantos_hay():
    assert falla("sea l = [1, 2, 3]\nmostrar(l[3])").mensaje == (
        "la posición 3 está fuera de rango: la lista tiene 3 elementos, así que las posiciones "
        "van de 0 a 2. Como se cuenta desde 0, el último está en la posición 2 (o usá ultimo(...))")
    assert falla("mostrar([][0])").mensaje == \
        "la posición 0 está fuera de rango: la lista no tiene ningún elemento"
    assert "la única posición es la 0" in falla("mostrar([7][5])").mensaje
    assert "para el último usá ultimo(...)" in falla("mostrar([1, 2][-1])").mensaje
    assert "el texto tiene 3 letras" in falla('mostrar("abc"[7])').mensaje
    error = falla("sea l = [1, 2, 3]\nmostrar(l[largo(l) / 2])").mensaje
    assert "dio 1.5" in error and "redondear()" in error
    assert falla('mostrar([1]["a"])').mensaje == \
        "la posición tiene que ser un número entero, no texto"
    assert "agregar(lista, valor)" in falla("var l = [1]\nl[1] = 2").mensaje


# Mejora 60: más controles antes de correr

def test_mas_controles_antes_de_correr():
    assert revisar("mostrar(1)\nmostrar(yo)") == [
        (2, "'yo' solo existe dentro de un agente (es el agente que está atendiendo); "
            "acá afuera no hay ninguno")]
    assert "'remitente' solo existe dentro de un agente" in revisar(
        "funcion f() {\n devolver remitente }")[0][1]
    assert revisar("sea m = { a: 1,\n b: 2, a: 3 }") == [
        (1, "la clave 'a' está repetida en el mapa: la segunda taparía a la primera")]
    assert revisar("funcion f(a, b, a) { devolver a }") == [
        (1, "f(): el parámetro 'a' está repetido")]
    agente = ("mensaje P { n: numero, t: texto?, c: cualquiera }\n"
              "agente A {\n estado x = 1\n estado x = 2\n"
              ' al recibir P { mostrar("{yo} {remitente}") }\n}\n')
    assert revisar(agente) == [(4, "A: el estado 'x' está repetido")]
    assert revisar(agente.replace("estado x = 2", "") + "sea c = crear A { x: 1, x: 2 }") == [
        (7, "A: el estado 'x' está repetido")]
    assert revisar("mensaje P { n: numero, t: texto?, c: cualquiera }\n"
                   "sea p = P { n: nada, t: nada, c: nada }") == [
        (2, "P.n es obligatorio y le diste nada. Si puede faltar, declaralo opcional en el "
            "mensaje: n: numero?")]


# Mejora 61: prueba de bombardeo

def romper_programa(fuente, azar):
    """Una versión rota del programa: le saca, repite, cambia o agrega un pedazo."""
    piezas = re.findall(r"\w+|\s+|.", fuente, re.S)
    lugar = azar.randrange(len(piezas))
    forma = azar.randrange(7)
    if forma == 0:
        del piezas[lugar]
    elif forma == 1:
        piezas.insert(lugar, piezas[lugar])
    elif forma == 2:
        otro = azar.randrange(len(piezas))
        piezas[lugar], piezas[otro] = piezas[otro], piezas[lugar]
    elif forma == 3:
        piezas[lugar] = azar.choice([
            "nada", "0", "-1", "1.5", '""', "[]", "{}", "verdadero", "yo", "remitente", "x",
            "mostrar", "largo", "Pedido", "(", ")", "{", "}", "[", "]", '"', ",", ".", ":",
            "=", "+", "-", "/", "\\", "\n", "si", "para", "en", "a", "responder", "devolver",
            "romper", "enviar", "preguntar", "crear", "fallar", "asegurar", "ñ", "“", "\t",
            "1.500", "3,5", "99999999999999999999", "%", "?", "#", "'", ";", "\u200b", "\x00"])
    elif forma == 4:
        del piezas[lugar:lugar + azar.randrange(1, 12)]
    elif forma == 5:
        del piezas[lugar:]
    else:
        piezas.insert(lugar, azar.choice([" ", "\n", "(", "nada", "sea x = ", '"{', "}"]))
    return "".join(piezas)


@pytest.mark.parametrize("nombre", sorted(p.name for p in (RAIZ / "ejemplos").glob("*.mate")))
def test_bombardeo_nunca_un_error_interno(nombre, tmp_path, capsys, monkeypatch):
    """Rompe cada ejemplo de muchas maneras: Mate siempre tiene que contestar en español,
    con su código de salida, y nunca con un error interno ni de Python."""
    import random
    import shutil

    def sin_teclado(_pregunta):
        raise EOFError

    monkeypatch.setattr(mate, "por_teclado", sin_teclado)
    monkeypatch.setattr(mate, "MAX_PASOS", 20_000)
    monkeypatch.setattr(mate, "MAX_MENSAJES", 2_000)
    monkeypatch.setattr(mate, "MAX_LARGO", 100_000)
    for ejemplo in (RAIZ / "ejemplos").glob("*.mate"):
        shutil.copy(ejemplo, tmp_path / ejemplo.name)
    original = (RAIZ / "ejemplos" / nombre).read_text(encoding="utf-8")
    azar = random.Random(nombre)
    archivo = tmp_path / "roto.mate"
    for vuelta in range(60):
        fuente = romper_programa(original, azar)
        archivo.write_text(fuente, encoding="utf-8")
        for orden in ("correr", "probar"):
            capsys.readouterr()
            codigo = mate.main([orden, str(archivo), "--traza"])
            capturado = capsys.readouterr()
            todo = capturado.out + capturado.err
            assert codigo in (0, 1, 2), (vuelta, orden, fuente)
            assert "error interno" not in todo and "Traceback" not in todo, (
                vuelta, orden, capturado.err, fuente)
            if codigo:
                assert capturado.err.strip() or "pruebas pasaron" in capturado.out, (
                    vuelta, orden, fuente)


def test_el_readme_avisa_lo_que_cambio_en_la_tanda_5():
    leeme = (RAIZ / "README.md").read_text(encoding="utf-8")
    for frase in ["### Funciones incluidas", '"Sale {precios["yerba"]}"', '"C:/temp/nuevo"',
                  "`1_500`", "el valor nada", "las posiciones van de 0 a 2",
                  "(tiene: yerba, azucar)", "`ñ` después de la `n`", "no sirven como nombre",
                  "`yo` y `remitente` fuera de un agente"]:
        assert frase in leeme, frase
    assert "no se puede escribir otro texto entre comillas" not in leeme


# ── Tanda 6 ──

# Mejora 62: 'probar' más prolijo

def test_probar_no_mezcla_lo_que_muestra_cada_prueba(tmp_path, capsys):
    codigo, out, err = por_main(tmp_path, capsys, """mostrar("arranca")
prueba "una" { mostrar("adentro de una") }
prueba "dos" {
    mostrar("adentro de dos")
    asegurar 1 == 2
}
""", orden="probar")
    assert (codigo, err) == (1, "")
    assert out.splitlines() == [
        "arranca",
        "  ✓ una",
        "      | adentro de una",
        "  ✗ dos",
        "      | adentro de dos",
        f"      {tmp_path / 'programa.mate'}:5: error: no se cumplió lo asegurado: dio 1 y "
        "se esperaba 2",
        "          5 |     asegurar 1 == 2",
        "1 de 2 pruebas pasaron"]


def test_probar_avisa_si_no_hay_pruebas(tmp_path, capsys):
    codigo, out, err = por_main(tmp_path, capsys, 'mostrar("hola")\n', orden="probar")
    assert (codigo, err) == (0, "")
    assert out.splitlines()[0] == "hola"
    assert "este archivo no tiene pruebas" in out and 'prueba "suma bien"' in out
    assert "0 de 0" not in out


def test_dos_pruebas_con_el_mismo_nombre_se_avisan_antes_de_correr(tmp_path, capsys):
    codigo, out, err = por_main(
        tmp_path, capsys, 'prueba "suma" { asegurar 1 == 1 }\nprueba "suma" { asegurar 2 == 2 }\n',
        orden="probar")
    assert codigo == 1 and out == ""
    assert 'programa.mate:2: error: ya hay una prueba llamada "suma" (línea 1)' in err


# Mejora 64: guardar la conversación en un archivo

def test_traza_a_un_archivo_con_resumen(tmp_path, capsys):
    destino = tmp_path / "conversacion.txt"
    codigo = mate.main(["correr", str(RAIZ / "ejemplos" / "negociacion.mate"),
                        f"--traza={destino}"])
    out = capsys.readouterr().out
    assert codigo == 0
    # en pantalla queda solo lo que el programa muestra, y el aviso de dónde se guardó
    assert out.splitlines() == ["Me cotizaron 10500 por 3 de yerba", "Cerramos en 9600.",
                                f"La conversación quedó guardada en {destino}"]
    guardado = destino.read_text(encoding="utf-8-sig").splitlines()
    assert guardado[0].startswith("Conversación de ")
    assert ('  ·  2.    Comprador pregunta a Vendedor: Pedido { producto: "yerba", cantidad: 3 }'
            in guardado)
    assert guardado[-1] == ("Resumen: 3 mensaje(s) entregado(s): 1 con 'enviar' y 2 con "
                            "'preguntar'. Ninguno falló.")


def test_traza_a_un_archivo_cuenta_las_fallas_y_no_pisa_programas(tmp_path, capsys):
    destino = tmp_path / "c.txt"
    codigo, out, err = por_main(tmp_path, capsys, """mensaje Ping
agente Roto { al recibir Ping { fallar "me rompí" } }
enviar Ping {} a Roto
""", f"--traza={destino}")
    assert codigo == 1 and "me rompí" in err
    assert destino.read_text(encoding="utf-8-sig").splitlines()[-1].endswith("Fallaron 1.")
    for malo in ("--traza=programa.mate", "--traza=mate.py", "--traza="):
        codigo, out, err = por_main(tmp_path, capsys, "mostrar(1)\n", malo)
        assert (codigo, out) == (2, "") and "--traza=conversacion.txt" in err


# Mejora 65 (aviso cuando una respuesta no tiene quién la reciba): el aviso sale solo en la
# traza (ver la tanda 9). El ejemplo mercado.mate responde a un 'enviar' del programa a
# propósito, y con 'correr' a secas no debe mostrar nada nuevo.

def test_responder_a_un_enviar_del_programa_sigue_sin_molestar(capsys):
    assert mate.main(["correr", str(RAIZ / "ejemplos" / "mercado.mate")]) == 0
    assert capsys.readouterr().err == ""


# Mejora 66: el ciclo de preguntas muestra la cadena

def test_el_ciclo_de_preguntas_muestra_la_cadena():
    error = falla("""mensaje Ir
agente A { al recibir Ir { responder preguntar Ir {} a B } }
agente B { al recibir Ir { responder preguntar Ir {} a C } }
agente C { al recibir Ir { responder preguntar Ir {} a A } }
preguntar Ir {} a A""")
    assert error.mensaje == (
        "ciclo de preguntas: A → B → C → A. A le preguntó a B (línea 2), B le preguntó a C "
        "(línea 3), C le preguntó a A (línea 4), y A todavía está atendiendo otro mensaje")
    solo = falla("mensaje Ir\nagente A { al recibir Ir { responder preguntar Ir {} a yo } }\n"
                 "preguntar Ir {} a A")
    assert "ciclo de preguntas: A → A. A le preguntó a A (línea 2)" in solo.mensaje


# Mejora 67: los errores dicen por dónde se llegó

CAMINO = """funcion dividir(a, b) {
    devolver a / b
}
funcion precio(x) {
    devolver dividir(10, x)
}
mensaje Pedir
agente Caja { al recibir Pedir { responder precio(0) } }
"""


def test_el_error_dice_por_donde_se_llego(tmp_path, capsys):
    codigo, _, err = por_main(tmp_path, capsys, CAMINO + "mostrar(precio(0))\n")
    assert codigo == 1
    assert err.splitlines() == [
        f"{tmp_path / 'programa.mate'}:2: error: división por cero",
        "    2 |     devolver a / b",
        "    cómo se llegó: en dividir(), llamada desde precio() (línea 5), llamada desde "
        "la línea 9"]


def test_el_camino_tambien_nombra_al_que_pregunto(tmp_path, capsys):
    codigo, _, err = por_main(tmp_path, capsys, CAMINO + """mensaje Ir
agente Jefe { al recibir Ir { responder preguntar Pedir {} a Caja } }
mostrar(preguntar Ir {} a Jefe)
""")
    assert codigo == 1
    assert err.splitlines()[2] == (
        "    cómo se llegó: en dividir(), llamada desde precio() (línea 5), llamada desde la "
        "línea 8, se lo preguntó Jefe a Caja (línea 10), se lo preguntó el programa a Jefe "
        "(línea 11)")


def test_el_camino_en_las_pruebas_y_sin_camino_no_se_agrega_nada(tmp_path, capsys):
    codigo, out, _ = por_main(tmp_path, capsys, CAMINO + 'prueba "precio" { asegurar '
                              'precio(0) == 1 }\n', orden="probar")
    assert codigo == 1
    assert "          cómo se llegó: en dividir(), llamada desde precio() (línea 5), " \
        "llamada desde la línea 9" in out
    codigo, _, err = por_main(tmp_path, capsys, "mostrar(1 / 0)\n")
    assert "cómo se llegó" not in err
    # el texto del error atajado no cambia: el camino va aparte
    assert correr(CAMINO + "intentar { precio(0) } si falla e { mostrar(e) }")[0] == [
        "división por cero"]


def test_el_camino_de_una_funcion_que_se_llama_mil_veces_es_corto(tmp_path, capsys):
    codigo, _, err = por_main(tmp_path, capsys, """funcion bajar(n) {
    si n == 0 { fallar "llegué" }
    bajar(n - 1)
}
bajar(30)
""")
    assert codigo == 1
    camino = err.splitlines()[2]
    assert camino.count("bajar()") <= 6 and "..., " in camino and camino.endswith("línea 5")


# Mejora 68: responder mal a un 'enviar' señala el renglón del 'responder'

def test_responder_algo_que_no_es_mensaje_a_un_enviar_dice_el_renglon(tmp_path, capsys):
    codigo, _, err = por_main(tmp_path, capsys, """mensaje Venta
mensaje Arrancar
agente Caja {
    al recibir Venta {
        responder 5
    }
}
agente Cliente { al recibir Arrancar { enviar Venta {} a Caja } }
enviar Arrancar {} a Cliente
""")
    assert codigo == 1
    assert err.splitlines() == [
        f"{tmp_path / 'programa.mate'}:5: error: Caja al recibir Venta: a un 'enviar' solo se "
        "le responde con un mensaje",
        "    5 |         responder 5"]


# Mejora 69: 'lista de Tipo' en los contratos

LISTAS = """
mensaje Item { nombre: texto, cantidad: numero }
mensaje Pedido { items: lista de Item, notas: lista de texto? }
mensaje Reparto { vendedores: lista de agente, tablas: lista de lista de numero }
agente Deposito {
    al recibir Pedido como p { responder largo(p.items) }
    al recibir Reparto como r { responder largo(r.vendedores) }
}
sea yerba = Item { nombre: "yerba", cantidad: 2 }
"""


def test_lista_de_tipo_acepta_lo_que_cumple():
    salida, _ = correr(LISTAS + """
        mostrar(preguntar Pedido { items: [yerba, yerba], notas: ["urgente"] } a Deposito)
        mostrar(preguntar Pedido { items: [] } a Deposito)
        mostrar(preguntar Reparto { vendedores: [Deposito], tablas: [[1, 2], []] } a Deposito)
        mostrar(de_json(a_json(Pedido { items: [yerba] })).items[0].nombre)
    """)
    assert salida == ["2", "0", "1", "yerba"]


def test_lista_de_tipo_rechaza_una_lista_con_cosas_mezcladas():
    assert falla(LISTAS + "sea mezcla = [yerba, 3]\nmostrar(Pedido { items: mezcla })").mensaje == (
        "Pedido.items es de tipo lista de Item y recibió una lista que en la posición 1 "
        "tiene un número")
    assert falla(LISTAS + 'sea n = 4\nmostrar(Pedido { items: n })').mensaje == (
        "Pedido.items es de tipo lista de Item y recibió numero")
    assert "en la posición 0 tiene una lista" in falla(
        LISTAS + 'sea t = [[1, "a"]]\nmostrar(Reparto { vendedores: [], tablas: t })').mensaje
    assert "JSON" not in falla(
        LISTAS + 'mostrar(de_json("{\\"tipo\\": \\"Pedido\\", \\"campos\\": '
                 '{\\"items\\": [1]}}"))').mensaje


def test_lista_de_tipo_se_revisa_antes_de_correr():
    programa = mate.analizar(LISTAS + """
        mensaje Raro { xs: lista de Fantasma }
        enviar Pedido { items: [yerba, "suelto"] } a Deposito
        enviar Pedido { items: 5 } a Deposito
        enviar Pedido { items: [yerba, Item { nombre: "a", cantidad: 1 }] } a Deposito
    """)
    assert [t for _, t in mate.verificar(programa)] == [
        "Raro.xs: no existe el tipo 'Fantasma'",
        "Pedido.items es de tipo lista de Item, y adentro de la lista hay un valor de tipo texto",
        "Pedido.items es de tipo lista de Item, no numero"]


# Mejora 70: contrato de respuesta con 'responde'

RESPONDE = """
mensaje Cotizacion { total: numero }
mensaje Pedido { cantidad: numero } responde Cotizacion
mensaje Precios responde lista de numero
agente Vendedor {
    estado ventas = 0
    al recibir Pedido como p {
        ventas += 1
        sea total = p.cantidad * 100
        si p.cantidad > 10 { responder total }
        responder Cotizacion { total: total }
    }
    al recibir Precios { responder [100, 200] }
}
"""


def test_responde_controla_lo_que_contesta_el_agente():
    salida, _ = correr(RESPONDE + """
        mostrar(preguntar Pedido { cantidad: 2 } a Vendedor)
        mostrar(preguntar Precios {} a Vendedor)
        intentar { preguntar Pedido { cantidad: 20 } a Vendedor } si falla e { mostrar(e) }
    """)
    assert salida == [
        "Cotizacion { total: 200 }", "[100, 200]",
        "Vendedor respondió numero a 'Pedido', y el contrato dice que a Pedido se le "
        "responde Cotizacion"]


def test_responder_fuera_de_contrato_es_falla_del_que_responde(tmp_path, capsys):
    # la falla es del vendedor: su estado vuelve atrás y el error señala su 'responder'
    codigo, out, err = por_main(tmp_path, capsys, RESPONDE + """mensaje Cuantas
agente Espia { al recibir Cuantas { responder 0 } }
mostrar(preguntar Pedido { cantidad: 20 } a Vendedor)
""")
    assert codigo == 1 and out == ""
    assert err.splitlines()[:2] == [
        f"{tmp_path / 'programa.mate'}:10: error: Vendedor respondió numero a 'Pedido', y el "
        "contrato dice que a Pedido se le responde Cotizacion",
        "    10 |         si p.cantidad > 10 { responder total }"]


def test_responde_se_revisa_antes_de_correr():
    programa = mate.analizar("""mensaje Cotizacion { total: numero }
mensaje Pedido responde Cotizacion
mensaje Otro responde Fantasma
mensaje Nombres responde lista de texto
agente Vendedor {
    al recibir Pedido { responder "cien" }
    al recibir Nombres { responder ["a", 1] }
}""")
    assert mate.verificar(programa) == [
        (3, "Otro responde 'Fantasma', que no es un tipo ni un mensaje declarado"),
        (6, "Vendedor responde texto a 'Pedido', y el contrato dice que a Pedido se le "
            "responde Cotizacion"),
        (7, "Vendedor responde una lista con un valor de tipo numero a 'Nombres', y el "
            "contrato dice que a Nombres se le responde lista de texto")]
    # sin 'responde' todo sigue como antes: se puede contestar cualquier cosa
    assert correr("mensaje Ping\nagente A { al recibir Ping { responder 1 } }\n"
                  "mostrar(preguntar Ping {} a A)")[0] == ["1"]


# Mejora 71: detalle_de(e), los datos de un error atajado

def test_detalle_de_un_error_atajado():
    salida, _ = correr("""funcion vender(producto) {
    fallar { codigo: 404, producto: producto }
}
intentar {
    vender("café")
} si falla e {
    sea d = detalle_de(e)
    mostrar(d.clase, d.linea, d.dato.codigo, d.dato.producto)
    mostrar(d.texto == e, tipo(e), e + "!")
}""")
    assert salida == ['fallar 2 404 café', "verdadero texto {codigo: 404, producto: \"café\"}!"]


@pytest.mark.parametrize("codigo,clase", [
    ("fallar nada", "fallar"),
    ("asegurar 1 == 2", "asegurar"),
    ('sea m = { a: 1 }\nmostrar(m["b"])', "clave"),
    ("sea m = { a: 1 }\nmostrar(m.b)", "clave"),
    ("mostrar([1, 2][5])", "posicion"),
    ("mostrar(1 / 0)", "division"),
    ("mostrar(no_existe)", "nombre"),
    ('mostrar(numero("abc"))', "numero"),
    ('mostrar(de_json("[1,"))', "json"),
    ("sea n = \"x\"\nmostrar(Sumar { a: n, b: 1 })", "contrato"),
    ("sea quien = [Calculadora]\npreguntar Ping {} a quien[0]", "agente"),
    ("preguntar Sumar { a: 1, b: 2 } a Tercero", "ciclo"),
    ('mostrar("a" + 1)', "otro"),
])
def test_la_clase_del_error_no_depende_de_la_redaccion(codigo, clase):
    salida, _ = correr(AGENTES + """
        mensaje Vuelta
        agente Tercero { al recibir Sumar como s { responder preguntar Sumar { a: 1, b: 1 } a yo } }
        intentar {
        """ + codigo + """
        } si falla e { mostrar(detalle_de(e).clase, detalle_de(e).dato) }""")
    assert salida == [f"{clase} nada"]


def test_el_detalle_viaja_con_el_error_y_e_sigue_siendo_un_texto():
    salida, _ = correr("""mensaje Pedir
agente Caja { al recibir Pedir { fallar ["sin stock", 3] } }
var guardado = ""
intentar { preguntar Pedir {} a Caja } si falla e { guardado = e }
mostrar(detalle_de(guardado).dato[1], guardado == "[\\"sin stock\\", 3]")
mostrar(tiene(guardado, "stock"), largo(guardado), a_json(guardado) == a_json(texto(guardado)))""")
    assert salida == ["3 verdadero", "verdadero 16 verdadero"]
    error = falla('mostrar(detalle_de("un texto cualquiera"))')
    assert "espera el error que ataja 'si falla e'" in error.mensaje and "un texto" in error.mensaje
    assert "función incluida" in falla("sea detalle_de = 1").mensaje


# Mejora 72: asegurar falla { ... }

def test_asegurar_falla_pasa_si_lo_de_adentro_falla(tmp_path, capsys):
    codigo, out, err = por_main(tmp_path, capsys, """funcion dividir(a, b) { devolver a / b }
prueba "dividir por cero falla" {
    asegurar falla { dividir(1, 0) }
}
prueba "esto no falla" {
    asegurar falla { dividir(4, 2) }
}
prueba "con mensaje propio" {
    asegurar falla { dividir(4, 2) }, "tenía que frenar la división"
}
prueba "un asegurar de adentro no cuenta como falla" {
    asegurar falla { asegurar 1 == 2 }
}
""", orden="probar")
    assert (codigo, err) == (1, "")
    renglones = out.splitlines()
    assert renglones[0] == "  ✓ dividir por cero falla"
    archivo = tmp_path / "programa.mate"
    assert renglones[1:3] == [
        "  ✗ esto no falla",
        f"      {archivo}:6: error: se esperaba que esto fallara, y no falló"]
    assert f"      {archivo}:9: error: tenía que frenar la división" in renglones
    assert (f"      {archivo}:12: error: no se cumplió lo asegurado: dio 1 y se esperaba 2"
            in renglones)
    assert renglones[-1] == "1 de 4 pruebas pasaron"


def test_asegurar_falla_tambien_vale_fuera_de_las_pruebas():
    assert correr('asegurar falla { fallar "x" }\nmostrar("sigue")')[0] == ["sigue"]
    assert "no falló" in falla("asegurar falla { mostrar(1) }").mensaje
    # lo que se define adentro no queda afuera, y el freno no se ataja
    assert "no existe 'x'" in falla("asegurar falla {\nsea x = 1\nfallar 2\n}\nmostrar(x)").mensaje
    assert "asegurar total == 10" in falla("asegurar\nfalla { }").mensaje


# Mejora 73: 'simular', reemplazar un agente en una prueba

SIMULAR = """mensaje Cotizacion { total: numero }
mensaje Pedido { cantidad: numero } responde Cotizacion
mensaje Comprar { cantidad: numero }
agente Vendedor {
    estado atendidos = 0
    al recibir Pedido como p {
        atendidos += 1
        responder Cotizacion { total: p.cantidad * 3500 }
    }
}
agente Comprador {
    al recibir Comprar como c {
        sea cot = preguntar Pedido { cantidad: c.cantidad } a Vendedor
        responder cot.total
    }
}
"""


def test_simular_reemplaza_la_respuesta_solo_en_esa_prueba():
    resultados = probar(SIMULAR + """
prueba "con el vendedor simulado" {
    sea precio = 10
    simular Vendedor al recibir Pedido como p {
        responder Cotizacion { total: p.cantidad * precio }
    }
    asegurar preguntar Comprar { cantidad: 2 } a Comprador == 20
}
prueba "la prueba siguiente ve al vendedor de verdad" {
    asegurar preguntar Comprar { cantidad: 2 } a Comprador == 7000
}
prueba "el simulado puede fallar, y vale para una copia" {
    sea otro = crear Vendedor llamado "Otro"
    simular otro al recibir Pedido { fallar "cerrado" }
    asegurar falla { preguntar Pedido { cantidad: 1 } a otro }
    asegurar (preguntar Pedido { cantidad: 1 } a Vendedor).total == 3500
}
""")
    assert resultados == {"con el vendedor simulado": None,
                          "la prueba siguiente ve al vendedor de verdad": None,
                          "el simulado puede fallar, y vale para una copia": None}


def test_simular_respeta_el_contrato_y_no_toca_lo_de_la_prueba():
    resultados = probar(SIMULAR + """
prueba "fuera de contrato" {
    sea mal = "caro"
    simular Vendedor al recibir Pedido { responder mal }
    mostrar(preguntar Comprar { cantidad: 2 } a Comprador)
}
prueba "no cambia variables de la prueba" {
    var veces = 0
    simular Vendedor al recibir Pedido {
        veces += 1
        responder Cotizacion { total: 1 }
    }
    mostrar(preguntar Comprar { cantidad: 2 } a Comprador)
}
""")
    assert "Vendedor respondió texto a 'Pedido'" in resultados["fuera de contrato"]
    assert "Vendedor no puede modificar 'veces'" in resultados["no cambia variables de la prueba"]


def test_simular_solo_va_en_una_prueba_y_se_revisa_antes():
    assert "'simular' solo va dentro de una prueba" in falla(
        SIMULAR + "simular Vendedor al recibir Pedido { responder 1 }").mensaje
    assert "'simular' solo va dentro de una prueba" in falla(
        SIMULAR + 'prueba "x" {\nfuncion f() { simular Vendedor al recibir Pedido { fallar 1 } }\n}'
    ).mensaje
    assert "'al recibir'" in falla(SIMULAR + 'prueba "x" { simular Vendedor Pedido { } }').mensaje
    programa = mate.analizar(SIMULAR + """prueba "x" {
    simular Vendedor al recibir Comprar { responder 1 }
    simular Vendedor al recibir Fantasma { responder 1 }
    simular Vendedor al recibir Pedido { responder "barato" }
}""")
    assert [t for _, t in mate.verificar(programa)] == [
        "Vendedor no sabe recibir 'Comprar': solo se simula un mensaje que el agente ya recibe",
        "no existe el mensaje 'Fantasma'",
        "Vendedor responde texto a 'Pedido', y el contrato dice que a Pedido se le responde "
        "Cotizacion"]
    assert "palabra propia de Mate" in falla("sea simular = 1").mensaje


# Mejora 74: copias de agentes con nombre único

def test_dos_copias_no_pueden_llamarse_igual():
    error = falla(AGENTES + 'sea a = crear Calculadora llamado "Norte"\n'
                            'sea b = crear Calculadora llamado "Norte"')
    assert error.mensaje.startswith('ya hay un Calculadora llamado "Norte"') and error.linea == 16
    assert "no puede estar vacío" in falla(AGENTES + 'sea a = crear Calculadora llamado " "').mensaje
    # sin nombre, o con nombres distintos, no hay problema; y cada prueba empieza limpia
    salida, _ = correr(AGENTES + """
        sea sucursales = ["Norte", "Sur"]
        para s en sucursales { mostrar(crear Calculadora llamado "Sucursal " + s { usos: 3 }) }
        mostrar(crear Calculadora, crear Calculadora llamado sucursales[0])
    """)
    assert salida == ["Calculadora Sucursal Norte", "Calculadora Sucursal Sur",
                      "Calculadora#4 Calculadora Norte"]
    assert probar(AGENTES + 'prueba "una" { mostrar(crear Calculadora llamado "X") }\n'
                            'prueba "otra" { mostrar(crear Calculadora llamado "X") }') == {
        "una": None, "otra": None}


def test_las_copias_sobreviven_al_ida_y_vuelta_por_json():
    salida, _ = correr(AGENTES + """
        mensaje Reparto { quienes: lista de agente }
        sea norte = crear Calculadora llamado "Norte" { usos: 7 }
        sea sin_nombre = crear Calculadora
        sea t = a_json(Reparto { quienes: [norte, sin_nombre, Calculadora] })
        sea vuelta = de_json(t)
        mostrar(vuelta.quienes == [norte, sin_nombre, Calculadora])
        mostrar(preguntar Contar {} a vuelta.quienes[0])
        mostrar(tipo(de_json("\\{\\"agente\\": \\"Calculadora Fantasma\\"\\}")))
    """)
    assert salida == ["verdadero", "7", "mapa"]


# Mejora 75: de_json(texto, "Pedido") exige el tipo

def test_de_json_con_tipo_exige_ese_tipo():
    salida, _ = correr(AGENTES + """
        sea t = a_json(Sumar { a: 1, b: 2 })
        mostrar(de_json(t, "Sumar"), de_json("[1, 2]", "lista de numero"), de_json("3", "numero"))
        mostrar(de_json("\\{\\"a\\": 5, \\"b\\": 6\\}", "Sumar"))
        para caso in [["[1, 2]", "Sumar"], [t, "Resultado"], [t, "mapa"],
                      ["[1, \\"x\\"]", "lista de numero"], ["\\{\\"a\\": 5\\}", "Sumar"],
                      ["1", "Sumarr"], ["\\{\\"a\\": \\"x\\", \\"b\\": 1\\}", "Sumar"]] {
            intentar { mostrar(de_json(caso[0], caso[1])) } si falla e {
                mostrar("{detalle_de(e).clase}: {e}")
            }
        }
    """.replace("para caso in", "para caso en"))
    assert salida == [
        "Sumar { a: 1, b: 2 } [1, 2] 3",
        "Sumar { a: 5, b: 6 }",
        "contrato: de_json(): se esperaba Sumar y el texto trae lista",
        "contrato: de_json(): se esperaba Resultado y el texto trae Sumar",
        "contrato: de_json(): se esperaba mapa y el texto trae Sumar",
        "contrato: de_json(): se esperaba lista de numero y el texto trae una lista que en "
        "la posición 1 tiene un texto",
        "contrato: a Sumar le falta el campo 'b'",
        "otro: de_json(): no existe el tipo 'Sumarr'. ¿Quisiste decir 'Sumar'?",
        "contrato: Sumar.a es de tipo numero y recibió texto"]
    assert correr('mostrar(de_json("[1]"))')[0] == ["[1]"]  # sin tipo, como siempre


def test_el_readme_cuenta_lo_de_la_tanda_6(tmp_path, capsys):
    leeme = (RAIZ / "README.md").read_text(encoding="utf-8")
    for frase in ["`--traza=conversacion.txt`", "cómo se llegó: en dividir()", "lista de Pedido",
                  "responde Cotizacion", "detalle_de(e).clase", "asegurar falla { dividir(1, 0) }",
                  "simular Vendedor al recibir Pedido como p", 'de_json(texto, "Pedido")',
                  "ciclo de preguntas: A → B → C → A", "no se repite"]:
        assert frase in leeme, frase
    # los dos ejemplos de pruebas del README andan tal cual están escritos
    bloques = re.findall(r"(?m)^  ```\n(  prueba .*?)^  ```", leeme, re.S)
    assert len(bloques) == 3  # (el tercero es el de mensajes_enviados: tiene su prueba)
    bloques = bloques[:2]
    programa = """funcion dividir(a, b) { devolver a / b }
mensaje Cotizacion { total: numero }
mensaje Pedido { cantidad: numero } responde Cotizacion
mensaje Comprar { cantidad: numero }
agente Vendedor { al recibir Pedido como p { responder Cotizacion { total: 0 } } }
agente Comprador {
    al recibir Comprar como c {
        responder (preguntar Pedido { cantidad: c.cantidad } a Vendedor).total
    }
}
""" + "\n".join(re.sub(r"(?m)^  ", "", b) for b in bloques)
    codigo, out, err = por_main(tmp_path, capsys, programa, orden="probar")
    assert (codigo, err) == (0, "") and out.endswith("2 de 2 pruebas pasaron\n")


# ───────── Tanda 7 ─────────

DIFUSION = """
mensaje Aviso { texto: texto }
mensaje Otro
agente Sucursal {
    estado vistos = []
    al recibir Aviso como a {
        vistos = agregar(vistos, a.texto)
        mostrar("{yo} vio {a.texto}")
    }
}
agente Sordo { al recibir Otro { } }
sea norte = crear Sucursal llamado "Norte"
sea sur = crear Sucursal llamado "Sur"
"""


# Mejora 76: enviar a una lista de agentes

def test_enviar_a_una_lista_de_agentes():
    salida, _ = correr(DIFUSION + 'enviar Aviso { texto: "cierra" } a [norte, sur, Sucursal]\n'
                       'sea nadie = []\nenviar Aviso { texto: "x" } a nadie')
    assert salida == ["Sucursal Norte vio cierra", "Sucursal Sur vio cierra",
                      "Sucursal vio cierra"]
    # si uno de la lista no sirve, no sale para ninguno
    salida, _ = correr(DIFUSION + """
        sea mezcla = [norte, Sordo]
        sea con_numero = [norte, 3]
        intentar { enviar Aviso { texto: "a" } a mezcla } si falla e { mostrar(e) }
        intentar { enviar Aviso { texto: "b" } a con_numero } si falla e { mostrar(e) }
        intentar { enviar Aviso { texto: "c" } a 5 } si falla e { mostrar(e) }
        intentar { preguntar Aviso { texto: "d" } a mezcla } si falla e { mostrar(e) }
    """)
    assert salida == [
        "Sordo no sabe recibir 'Aviso'",
        "en una lista de destinos tienen que ser todos agentes, y en la posición 1 hay un número",
        "el destino tiene que ser un agente o una lista de agentes, no numero",
        "el destino tiene que ser un agente, no lista. Se le pregunta a un agente por vez: "
        "recorré la lista con 'para agente en lista { ... }'"]
    # escrito a mano, se avisa antes de correr
    assert revisar(DIFUSION + 'enviar Aviso { texto: "a" } a [norte, Sordo]') == [
        (14, "Sordo no sabe recibir 'Aviso'")]


# Mejora 77: 'al fallar'

CON_AL_FALLAR = """
mensaje Pedido { producto: texto }
mensaje Encargar { producto: texto }
mensaje Cuantas
agente Vendedor {
    al recibir Pedido como p {
        si p.producto != "yerba" { fallar "no vendo {p.producto}" }
    }
}
agente Comprador {
    estado fallas = []
    al recibir Encargar como e { enviar Pedido { producto: e.producto } a Vendedor }
    al recibir Cuantas { responder fallas }
    al fallar como f {
        fallas = agregar(fallas, "{f.destino}: {f.motivo} ({f.mensaje.producto})")
        si f.mensaje.producto == "bomba" { fallar "el aviso también falló" }
    }
}
"""


def test_al_fallar_le_avisa_al_que_envio():
    salida, interprete = correr(CON_AL_FALLAR + """
        enviar Encargar { producto: "café" } a Comprador
        enviar Encargar { producto: "yerba" } a Comprador
        mostrar(preguntar Cuantas {} a Comprador)
    """, traza=True)
    assert ("  ·     Comprador se entera de que Vendedor no pudo atender Pedido: no vendo café"
            in salida)
    assert salida[-1] == '["Vendedor: no vendo café (café)"]'
    assert interprete.errores_agentes == []  # la falla quedó en manos del Comprador
    assert interprete.cuenta == {"enviar": 4, "preguntar": 1, "fallaron": 1}
    # sin 'al fallar', la falla se anota como siempre
    sin = CON_AL_FALLAR.replace("al fallar como f {", "funcion nunca(f) {")
    _, interprete = correr(sin + 'enviar Encargar { producto: "café" } a Comprador')
    assert interprete.errores_agentes == ["línea 7: Vendedor al recibir Pedido: no vendo café"]
    # si el propio 'al fallar' falla, eso sí es un error (y su estado vuelve atrás)
    salida, interprete = correr(CON_AL_FALLAR + """
        enviar Encargar { producto: "bomba" } a Comprador
        mostrar(preguntar Cuantas {} a Comprador)
    """)
    assert interprete.errores_agentes == [
        "línea 16: Comprador en 'al fallar': el aviso también falló"]
    assert salida == ["[]"]


def test_al_fallar_tiene_sus_reglas():
    base = "mensaje P\nagente A { al recibir P { }\n"
    assert "no hay a quién responder" in falla(base + "al fallar { responder 1 } }").mensaje
    assert revisar(base + "al fallar { }\nal fallar como f { } }") == [
        (4, "A ya tiene un 'al fallar': va uno solo")]
    assert "'recibir' o 'fallar'" in falla("agente A { al romper { } }").mensaje
    # dentro de una prueba, una falla avisada no hace fallar la prueba
    resultados = probar(CON_AL_FALLAR + """
        prueba "se entera" {
            enviar Encargar { producto: "café" } a Comprador
            asegurar largo(preguntar Cuantas {} a Comprador) == 1
        }
        prueba "empieza limpia" { asegurar preguntar Cuantas {} a Comprador == [] }
    """)
    assert resultados == {"se entera": None, "empieza limpia": None}


# Mejora 78: más lugar para la recursión

@pytest.mark.skipif(sys.version_info < (3, 12), reason="en un Python viejo queda el tope de antes")
def test_la_recursion_llega_a_miles_de_llamadas():
    salida, _ = correr("""
        funcion suma(n) {
            si n == 0 { devolver 0 }
            devolver n + suma(n - 1)
        }
        funcion texto_hondo(n) {
            si n == 0 { devolver "" }
            devolver "{texto_hondo(n - 1)}"
        }
        mostrar(suma(2500), largo(texto_hondo(2500)))
    """)
    assert salida == ["3126250 0"]


def test_el_error_de_recursion_nombra_la_funcion():
    tope = sys.getrecursionlimit()
    error = falla("funcion cuenta(n) { devolver cuenta(n + 1) }\nmostrar(cuenta(0))")
    assert error.clase == "limite" and error.linea == 1
    assert "la última, a cuenta()" in error.mensaje and "un 'si' que la frene" in error.mensaje
    assert sys.getrecursionlimit() == tope  # Mate deja a Python como lo encontró


# Mejora 79: los nombres con mayúscula quedan para mensajes y agentes

def test_los_nombres_con_mayuscula_son_de_mensajes_y_agentes():
    for fuente, sugerido in [("sea Listo = verdadero", "'listo'"), ("var Total = 0", "'total'"),
                             ("funcion Doble(n) { devolver n * 2 }", "'doble'"),
                             ("funcion f(Precio) { devolver 1 }", "'precio'"),
                             ("para Item en [1] { }", "'item'"),
                             ("sea Texto = 1", "'mi_texto'"), ("sea Para = 1", "'mi_para'")]:
        mensaje = falla(fuente).mensaje
        assert "empieza con mayúscula" in mensaje and mensaje.endswith(sugerido), mensaje
    ping = "mensaje Ping\nagente A { al recibir Ping { responder 1 } }\n"
    assert revisar(ping + "mostrar(preguntar Ping a A)") == [
        (3, "'Ping' es un mensaje: para armar uno van las llaves, aunque no tenga campos. "
            "Escribí Ping {}")]
    assert correr(ping + "mostrar(preguntar Ping {} a A)")[0] == ["1"]


# Mejora 80: la llave en el renglón de abajo

def test_la_llave_puede_ir_en_el_renglon_de_abajo():
    salida, _ = correr("""
        mensaje Pedido
        {
            producto: texto
        } responde numero
        agente Vendedor
        {
            estado precio = 10
            al recibir Pedido como p { responder precio }
        }
        sea caro = crear Vendedor llamado "Caro"
        {
            precio: 99
        }
        mostrar(preguntar Pedido { producto: "yerba" } a caro, caro)
    """)
    assert salida == ["99 Vendedor Caro"]
    assert "le falta el campo 'producto'" in revisar(
        "mensaje Pedido\n{ producto: texto }\nsea p = Pedido {}")[0][1]


# Mejora 81: condiciones que no son verdadero o falso, antes de correr

def test_las_condiciones_imposibles_se_avisan_antes_de_correr():
    no_es = "la condición tiene que ser verdadero o falso, "
    for fuente, que in [("si 1 { }", "no numero"), ('mientras "a" { }', "no texto"),
                        ("mostrar(verdadero y 1)", "no numero"),
                        ("mostrar([] o falso)", "no lista"), ("mostrar(no nada)", "no el valor nada"),
                        ("asegurar { a: 1 }", "no mapa"),
                        ("si falso { } sino si 2 { }", "no numero"),
                        ("mensaje M\nsi M {} { }", "no un mensaje M")]:
        errores = revisar("sea x = 1\n" + fuente)
        assert len(errores) == 1 and errores[0][1] == no_es + que, errores
    errores = revisar("sea x = 1\nfuncion nunca() {\n    si x + 1 { mostrar(x) }\n}")
    assert errores[0][0] == 3 and "esto es una cuenta" in errores[0][1]
    assert "x + 1 > 0" in errores[0][1]
    # lo que puede dar verdadero o falso no se toca
    assert revisar("sea x = 1\nsea ok = x > 0\nsi ok y no (x == 2) { mostrar(x) }") == []


# Mejoras 82 y 83: tiene() con textos, quitar() y la pista de los textos

def test_tiene_y_quitar_explican_que_esperan():
    assert falla('mostrar(tiene("hola", 1))').mensaje == (
        "tiene(): dentro de un texto se busca otro texto, y recibió un número. "
        "Pasalo a texto: tiene(t, texto(1))")
    assert falla('mostrar(tiene("hola", nada))').mensaje == (
        "tiene(): dentro de un texto se busca otro texto, y recibió el valor nada")
    assert "busca en una lista, un mapa o un texto, y recibió un número" in falla(
        "mostrar(tiene(5, 1))").mensaje
    assert correr('mostrar(tiene("hola", "ol"), tiene([1], "1"), tiene({ a: 1 }, 1))')[0] == [
        "verdadero falso falso"]
    mensaje = falla('mostrar(quitar("hola", "h"))').mensaje
    assert "recibió un texto" in mensaje and 'reemplazar(t, parte, "")' in mensaje
    assert "las claves de un mapa son textos" in falla("mostrar(quitar({ a: 1 }, 1))").mensaje
    # quitar saca por valor, no por posición
    assert correr("mostrar(quitar([10, 20, 10], 10), quitar([10, 20], 0))")[0] == ["[20] [10, 20]"]
    # la pista de texto() aparece solo si en la cuenta hay un texto
    assert "usá texto()" in falla('mostrar("a" + 1)').mensaje
    for cuenta in ["1 + verdadero", "nada + 1", "[1] + 2", "{ a: 1 } + 1", '"a" - 1']:
        assert "texto()" not in falla(f"mostrar({cuenta})").mensaje, cuenta
    assert "saca **por valor**" in (RAIZ / "README.md").read_text(encoding="utf-8")
    assert "por valor, no por posición" in mate.texto_de_guia()


# Mejora 84: para posicion, item en lista

def test_para_con_posicion_o_con_clave_y_valor():
    salida, _ = correr("""
        para i, cosa en ["yerba", "azúcar"] { mostrar(i, cosa) }
        para producto, precio en { yerba: 3500, azucar: 1200 } { mostrar(producto, precio) }
        para i, letra en "ab" { mostrar(i, letra) }
        para i, x en [5, 6, 7, 8] {
            si i == 0 { continuar }
            si i == 2 { romper }
            mostrar(i, x)
        }
    """)
    assert salida == ["0 yerba", "1 azúcar", "yerba 3500", "azucar 1200", "0 a", "1 b", "1 6"]
    assert "es la variable del 'para'" in falla("para i, x en [1] { i = 2 }").mensaje
    assert "no pueden ser iguales" in falla("para x, x en [1] { }").mensaje
    assert "'x' ya está definido" in falla("para i, x en [1] { sea x = 2 }").mensaje
    assert "no se puede recorrer numero" in falla("para i, x en 5 { }").mensaje


# Mejora 85: errores de 'usar' con más pistas

def test_usar_prueba_con_mate_y_dice_quien_trajo_el_archivo(tmp_path, capsys):
    (tmp_path / "catalogo.mate").write_text("sea iva = 0.21\n", encoding="utf-8")
    (tmp_path / "roto.mate").write_text("sea a = 1\nsea b = = 2\n", encoding="utf-8")
    (tmp_path / "medio.mate").write_text('usar "roto"\n', encoding="utf-8")
    (tmp_path / "notas.mate.txt").write_text("sea n = 1\n", encoding="utf-8")
    codigo, out, _ = por_main(tmp_path, capsys, 'usar "catalogo"\nusar "catalogo.mate"\nmostrar(iva)')
    assert (codigo, out) == (0, "0.21\n")
    codigo, _, err = por_main(tmp_path, capsys, '# programa\nusar "medio.mate"')
    assert codigo == 1 and "roto.mate:2: error: no esperaba '=' acá" in err
    assert "(este archivo, roto.mate, se trajo con 'usar' desde medio.mate, línea 1)" in err
    assert err.count("se trajo con") == 1 and "    2 | sea b = = 2" in err
    codigo, _, err = por_main(tmp_path, capsys, 'usar "catalgo.mate"')
    assert codigo == 1 and "no pude abrir 'catalgo.mate'" in err
    assert "¿Quisiste decir 'catalogo.mate'?" in err
    _, _, err = por_main(tmp_path, capsys, 'usar "notas.mate"')
    assert "Encontré notas.mate.txt: el Bloc de notas le agregó .txt" in err
    _, _, err = por_main(tmp_path, capsys, 'usar "zzz"')
    assert "Los archivos .mate que hay ahí: catalogo.mate, medio.mate, programa.mate" in err


# Mejora 86: a_mapa(mensaje)

def test_a_mapa_convierte_un_mensaje_en_un_mapa():
    salida, _ = correr("""
        mensaje Pedido { producto: texto, cantidad: numero, nota: texto? }
        sea p = Pedido { producto: "yerba", cantidad: 2 }
        var m = a_mapa(p)
        para campo, valor en m { mostrar("{campo}: {valor}") }
        m.cantidad = "muchas"
        mostrar(tipo(m), p.cantidad, claves(a_mapa(p)), a_mapa({ a: 1 }))
    """)
    assert salida == ["producto: yerba", "cantidad: 2", "nota: nada",
                      'mapa 2 ["producto", "cantidad", "nota"] {a: 1}']
    assert falla("mostrar(a_mapa(5))").mensaje == "a_mapa() espera un mensaje y recibió un número"
    assert "función incluida" in falla("sea a_mapa = 1").mensaje


# Mejora 87: 'probar' con varios archivos o una carpeta

def test_probar_con_una_carpeta_o_varios_archivos(tmp_path, capsys):
    (tmp_path / "a.mate").write_text(
        'mostrar("corre a")\nprueba "uno" { asegurar 1 == 1 }\nprueba "dos" { asegurar 2 == 2 }\n',
        encoding="utf-8")
    (tmp_path / "b.mate").write_text('prueba "tres" { asegurar 1 == 2 }\n', encoding="utf-8")
    (tmp_path / "c.mate").write_text('mostrar("sin pruebas")\n', encoding="utf-8")
    (tmp_path / "notas.txt").write_text("no es un programa", encoding="utf-8")
    capsys.readouterr()
    assert mate.main(["probar", str(tmp_path)]) == 1
    out = capsys.readouterr().out
    assert out.index("a.mate:") < out.index("b.mate:") < out.index("c.mate:")
    assert "2 de 2 pruebas pasaron" in out and "0 de 1 pruebas pasaron" in out
    assert "  (sin pruebas)" in out and "notas.txt" not in out
    assert "En total: 2 de 3 pruebas pasaron, en 3 archivos" in out
    assert out.rstrip().endswith("Con problemas: " + str(tmp_path / "b.mate"))
    assert mate.main(["probar", str(tmp_path / "a.mate"), str(tmp_path / "c.mate")]) == 0
    out = capsys.readouterr().out
    assert out.endswith("En total: 2 de 2 pruebas pasaron, en 2 archivos\n")
    # un archivo que no está no corta a los demás, pero se nota
    assert mate.main(["probar", str(tmp_path / "a.mate"), str(tmp_path / "nohay.mate")]) == 1
    capturado = capsys.readouterr()
    assert "no encuentro 'nohay.mate'" in capturado.err and "En total: 2 de 2" in capturado.out
    vacia = tmp_path / "vacia"
    vacia.mkdir()
    assert mate.main(["probar", str(vacia)]) == 2
    assert "no hay ningún archivo .mate" in capsys.readouterr().err
    # 'correr' sigue llevando un solo archivo
    assert mate.main(["correr", str(tmp_path / "a.mate"), str(tmp_path / "c.mate")]) == 2
    assert "lleva un solo archivo" in capsys.readouterr().err


def test_probar_la_carpeta_de_ejemplos(capsys):
    assert mate.main(["probar", str(RAIZ / "ejemplos")]) == 0
    out = capsys.readouterr().out
    assert re.search(r"En total: (\d+) de \1 pruebas pasaron, en \d+ archivos\n$", out)


def test_el_readme_cuenta_lo_de_la_tanda_7(tmp_path, capsys):
    leeme = (RAIZ / "README.md").read_text(encoding="utf-8")
    for frase in ["a [norte, sur]", "al fallar como f", "3.000 llamadas", "`sea Listo = verdadero`",
                  "Escribí Ping {}", "en el renglón siguiente", "`verdadero y 1`",
                  "para i, item en lista", 'usar "catalogo"', "a_mapa(pedido)",
                  "probar mate\\ejemplos", "En total: 17 de 17 pruebas pasaron"]:
        assert frase in leeme, frase
    # el ejemplo de 'al fallar' del README anda tal cual está escrito
    ejemplo = re.search(r"(?m)^  ```\n(  agente Comprador .*?)^  ```", leeme, re.S).group(1)
    programa = """mensaje Pedido { producto: texto }
mensaje Encargar { producto: texto }
agente Vendedor { al recibir Pedido como p { fallar "no hay {p.producto}" } }
""" + re.sub(r"(?m)^  ", "", ejemplo) + 'enviar Encargar { producto: "café" } a Comprador\n'
    codigo, out, err = por_main(tmp_path, capsys, programa)
    assert (codigo, out, err) == (0, "Vendedor no pudo con café: no hay café\n", "")


# ───────────── Tanda 8 ─────────────

def en_consola(*renglones):
    """Una sesión de la consola: devuelve lo que mostró, sin los dos renglones de bienvenida."""
    pendientes, mostrado = list(renglones), []

    def entrada(_pregunta):
        if not pendientes:
            raise EOFError
        return pendientes.pop(0)

    assert mate.consola(entrada=entrada, mostrar=mostrado.append) == 0
    assert mostrado[0].startswith(f"Mate {mate.VERSION}, consola")
    return mostrado[2:]


# Mejora 88: la consola

def test_la_consola_muestra_los_valores_sueltos_y_recuerda_lo_declarado():
    assert en_consola("2 + 3", "sea x = 5", "x * 2", 'mostrar("hola")', '"5"', "salir",
                      "mostrar(99)") == ["5", "10", "hola", '"5"']
    # lo que queda abierto sigue en el renglón de abajo, y las funciones quedan declaradas
    assert en_consola("funcion doble(n) {", "    devolver n * 2", "}", "doble(4)") == ["8", ""]
    # solo acá se puede volver a declarar algo para corregirlo
    assert en_consola("sea x = 1", "sea x = x + 1", "x", "funcion f() { devolver 1 }",
                      "funcion f() { devolver 2 }", "f()", "salir") == ["2", "2"]
    assert "ya está definido" in falla("sea x = 1\nsea x = 2").mensaje  # en un archivo, no


def test_en_la_consola_un_error_no_corta_y_dice_el_renglon():
    mostrado = en_consola(
        "nohay",                                   # 1
        "funcion rompe() { devolver 1 / 0 }",      # 2
        "rompe()",                                 # 3
        "si verdadero {", "",                      # 4 y 5: el renglón vacío corta
        "sea texto = 1",                           # 6
        "doble",                                   # 7
        "mostrar(1 + 1)", "salir")
    assert mostrado[0] == "error: no existe 'nohay'"
    assert mostrado[1:3] == ["línea 2: error: división por cero",
                             "    cómo se llegó: en rompe(), llamada desde la línea 3"]
    assert mostrado[3] == "error: la llave que se abrió en la línea 4 (si verdadero) " \
                          "nunca se cierra"
    assert "función incluida" in mostrado[4] and "no existe 'doble'" in mostrado[5]
    assert mostrado[6:] == ["2"]


def test_la_consola_con_agentes_ayuda_y_pruebas():
    mostrado = en_consola(
        "mensaje Ping { n: numero }",
        'agente Eco { al recibir Ping como p { si p.n < 0 { fallar "negativo" } responder p.n } }',
        "preguntar Ping { n: 7 } a Eco",
        "preguntar Ping { m: 7 } a Eco",          # el contrato se revisa con lo ya declarado
        "enviar Ping { n: -1 } a Eco",
        "ayuda sea",
        'prueba "x" { asegurar 1 == 1 }',
        "salir")
    assert mostrado[0] == "7"
    assert "Ping no tiene un campo 'm'" in mostrado[1]
    assert "línea 2: error: Eco al recibir Ping: negativo" in mostrado
    assert any(r.startswith("sea: guarda un valor") for r in mostrado)
    assert "las pruebas no corren en la consola" in mostrado[-1]


def test_la_orden_consola(capsys, monkeypatch):
    renglones = iter(["sea precio = 3500", "precio * 2", "funcion con_iva(p) {",
                      "    devolver p * 1.21", "}", "pesos(con_iva(precio))", "salir"])
    preguntas = []

    def entrada(pregunta=""):
        preguntas.append(pregunta)
        return next(renglones)

    monkeypatch.setattr("builtins.input", entrada)
    assert mate.main(["consola"]) == 0
    out = capsys.readouterr().out.splitlines()
    assert out[2:] == ["7000", '"$ 4.235,00"']  # la sesión de ejemplo del README
    assert preguntas == ["  1> ", "  2> ", "  3> ", "  4. ", "  5. ", "  6> ", "  7> "]
    assert mate.main(["consola", "hola.mate"]) == 2
    assert "'consola' va sola" in capsys.readouterr().err
    assert mate.main(["consol"]) == 2
    assert "¿quisiste decir 'consola'?" in capsys.readouterr().err


# Mejora 89: versión 0.3

def test_version_0_3_y_el_readme_lo_dice(capsys):
    assert mate.VERSION == "0.3"
    leeme = (RAIZ / "README.md").read_text(encoding="utf-8")
    assert "Versión 0.3." in leeme and "## Límites de la versión 0.3" in leeme
    assert "versión 0.2" not in leeme.replace("desde la versión 0.2 hasta la 0.3", "")
    assert "desde la versión 0.2 hasta la 0.3" in leeme
    assert mate.main(["--version"]) == 0
    assert capsys.readouterr().out.startswith("Mate 0.3 ")


# Mejora 90: el tope para que Mate siga siendo chico

def test_mate_no_se_pasa_del_tope():
    assert len(mate.PALABRAS) <= mate.TOPE_DE_PALABRAS
    assert len(mate.FUNCIONES) <= mate.TOPE_DE_FUNCIONES
    leeme = (RAIZ / "README.md").read_text(encoding="utf-8")
    assert "## El tope: Mate tiene que seguir siendo chico" in leeme
    # el README dice los números de verdad
    assert f"**Palabras propias: {mate.TOPE_DE_PALABRAS} como mucho.** Hoy son " \
           f"{len(mate.PALABRAS)} " in leeme
    assert f"**Funciones incluidas: {mate.TOPE_DE_FUNCIONES} como mucho.** Hoy son " \
           f"{len(mate.FUNCIONES)}." in leeme
    # cada agregado con su prueba: todas las funciones y las palabras se usan en este archivo
    pruebas = pathlib.Path(__file__).read_text(encoding="utf-8")
    for nombre in mate.FUNCIONES:
        assert re.search(rf"\b{nombre}\(", pruebas), f"falta una prueba que use {nombre}()"
    for palabra in mate.PALABRAS:
        assert re.search(rf"\b{palabra}\b", pruebas), f"falta una prueba que use '{palabra}'"
        assert mate.ayuda_de(palabra), palabra


def test_valores_de_un_mapa():  # (no tenía prueba: lo encontró el control de arriba)
    assert correr("mostrar(valores({ a: 1, b: [2] }), valores({}))")[0] == ["[1, [2]] []"]
    assert "valores()" in falla("mostrar(valores([1]))").mensaje


def test_mayusculas_y_minusculas():  # (tampoco tenían)
    assert correr('mostrar(mayusculas("Ñandú 1"), minusculas("ÁRBOL Ñ"))')[0] == ["ÑANDÚ 1 árbol ñ"]
    assert "mayusculas()" in falla("mostrar(mayusculas(5))").mensaje
    assert "minusculas()" in falla("mostrar(minusculas(nada))").mensaje


# Mejora 91: leer y escribir archivos de texto

def test_leer_y_escribir_archivos(tmp_path, capsys):
    (tmp_path / "ansi.txt").write_bytes("año\r\nñandú".encode("cp1252"))
    (tmp_path / "datos").mkdir()
    codigo, out, err = por_main(tmp_path, capsys, """
        escribir_archivo("compras.txt", unir(["yerba", "azúcar"], "\\n"))
        mostrar(partir(leer_archivo("compras.txt"), "\\n"))
        mostrar(partir(leer_archivo("ansi.txt"), "\\n"))
        escribir_archivo("datos/uno.txt", "1")
        mostrar(leer_archivo("datos/uno.txt"))
        funcion guardar(t) { escribir_archivo("compras.txt", t) }
        guardar("pisado")
        mostrar(leer_archivo("compras.txt"))
    """)
    assert (codigo, err) == (0, "")
    assert out.splitlines() == ['["yerba", "azúcar"]', '["año", "ñandú"]', "1", "pisado"]
    # queda con la marca que el Bloc de notas necesita para mostrar las tildes
    assert (tmp_path / "compras.txt").read_bytes() == b"\xef\xbb\xbfpisado"


def test_los_archivos_solo_de_la_carpeta_y_sin_pisar_programas(tmp_path, capsys):
    carpeta = tmp_path / "programas"
    carpeta.mkdir()
    (tmp_path / "afuera.txt").write_text("secreto", encoding="utf-8")
    (carpeta / "notas.txt").write_text("hola", encoding="utf-8")
    (carpeta / "lista.txt.txt").write_text("hola", encoding="utf-8")
    casos = {
        'leer_archivo("../afuera.txt")': "queda afuera",
        f'leer_archivo("{(tmp_path / "afuera.txt").as_posix()}")': 'sin la ruta: "afuera.txt"',
        'escribir_archivo("../nuevo.txt", "x")': "queda afuera",
        'escribir_archivo("programa.mate", "x")': "para no pisar un programa",
        'escribir_archivo("Otro.MATE", "x")': "para no pisar un programa",
        'escribir_archivo("mate.py", "x")': "para no pisar un programa",
        'escribir_archivo("programa.mate. ", "x")': "para no pisar un programa",
        'escribir_archivo("programa.mate::$DATA", "x")': "para no pisar un programa",
        'escribir_archivo("correr.bat", "x")': "para no pisar un programa",
        'escribir_archivo("notas.txt", 5)': "guarda un texto y recibió numero",
        'escribir_archivo("nohay/notas.txt", "x")': "no existe la carpeta",
        'escribir_archivo("", "x")': "falta el nombre del archivo",
        'escribir_archivo(".", "x")': "es una carpeta",
        'leer_archivo("nota.txt")': "no encuentro el archivo 'nota.txt'",
        'leer_archivo("lista.txt")': "¿Quisiste decir 'lista.txt.txt'?",
        'leer_archivo(5)': "espera texto",
    }
    for llamada, esperado in casos.items():
        valor = "sea t = " if llamada.startswith("leer") else ""
        codigo, out, err = por_main(carpeta, capsys, valor + llamada)
        assert codigo == 1 and esperado in err, (llamada, err)
    assert "¿Quisiste decir 'notas.txt'?" in por_main(
        carpeta, capsys, 'sea t = leer_archivo("nota.txt")')[2]
    assert sorted(p.name for p in tmp_path.iterdir()) == ["afuera.txt", "programas"]
    assert (carpeta / "programa.mate").read_text(encoding="utf-8").startswith("sea t")
    # el error se puede atajar, y dice de qué clase es
    codigo, out, err = por_main(carpeta, capsys, """
        intentar { sea t = leer_archivo("nohay.txt") } si falla e { mostrar(detalle_de(e).clase) }
        leer_archivo("notas.txt")
    """)
    assert out == "archivo\n" and "devuelve un valor y este renglón no lo usa" in err


def test_un_agente_no_toca_archivos(tmp_path, capsys):
    codigo, out, err = por_main(tmp_path, capsys, """
        mensaje Guardar { que: texto }
        mensaje Leer {}
        agente Archivero {
            al recibir Guardar como g { escribir_archivo("notas.txt", g.que) }
            al recibir Leer { responder leer_archivo("notas.txt") }
        }
        enviar Guardar { que: "x" } a Archivero
        intentar { sea t = preguntar Leer {} a Archivero } si falla e { mostrar(e) }
    """)
    assert codigo == 1 and not (tmp_path / "notas.txt").exists()
    assert "escribir_archivo() solo se usa desde el programa principal" in err
    assert out.startswith("leer_archivo() solo se usa desde el programa principal: un agente")


# Mejora 92: hoy() y ahora()

def test_hoy_y_ahora(tmp_path, capsys):
    salida, _ = correr("mostrar(hoy())\nmostrar(ahora())")
    assert re.fullmatch(r"\d\d/\d\d/\d{4}", salida[0])
    assert re.fullmatch(r"\d\d/\d\d/\d{4} \d\d:\d\d", salida[1]) and salida[1].startswith(salida[0])
    import datetime
    assert salida[0] in [(datetime.datetime.now() - datetime.timedelta(seconds=s))
                         .strftime("%d/%m/%Y") for s in (0, 60)]
    # en las pruebas, siempre la misma fecha
    codigo, out, err = por_main(tmp_path, capsys, """
        prueba "la fecha no depende del día" {
            asegurar hoy() == "01/01/2025"
            asegurar ahora() == "01/01/2025 12:00"
            asegurar partir(hoy(), "/") == ["01", "01", "2025"]
        }
    """, orden="probar")
    assert (codigo, err) == (0, "") and "1 de 1 pruebas pasaron" in out
    assert "hoy() lleva 0 valores y recibió 1" in falla("mostrar(hoy(1))").mensaje
    assert "función incluida" in falla("sea hoy = 1").mensaje
    assert "función incluida" in falla("sea ahora = 1").mensaje


# Mejora 94: ayuda <palabra>

def test_ayuda_de_una_palabra_o_de_una_funcion(capsys):
    assert mate.main(["ayuda", "si"]) == 0
    out = capsys.readouterr().out
    assert out.startswith("si: hace una cosa u otra") and "Ejemplo:\n    sea edad = 20" in out
    assert mate.main(["ayuda", "largo"]) == 0
    assert capsys.readouterr().out == (
        "largo (función incluida): cuántos elementos tiene (o letras, o claves)\n\n"
        "Ejemplo:\n    largo(lista)\n")
    for pedido, empieza in {"sino": "sino (va con 'si'): ", "FUNCIÓN": "funcion: ",
                            "pesos()": "pesos (función incluida): ",
                            "print": "En Mate 'print' se escribe 'mostrar'.\nmostrar (función"}.items():
        assert mate.main(["ayuda", pedido]) == 0
        assert capsys.readouterr().out.startswith(empieza), pedido
    assert mate.main(["ayuda", "mostar"]) == 2
    capturado = capsys.readouterr()
    assert capturado.out == "" and "no tengo ayuda sobre 'mostar'. ¿Quisiste decir 'mostrar'?" \
        in capturado.err
    assert "mientras" in capturado.err and "redondear" in capturado.err
    assert mate.main(["ayuda"]) == 0
    assert "ayuda si " in capsys.readouterr().out


def test_hay_ayuda_de_todo_y_los_ejemplos_andan(tmp_path, monkeypatch):
    for nombre in list(mate.PALABRAS) + list(mate.FUNCIONES) + ["lista", "mapa"]:
        texto = mate.ayuda_de(nombre)
        assert texto and "Ejemplo:" in texto, nombre
        assert max(len(r) for r in texto.splitlines()) <= 100, nombre
    assert mate.ayuda_de("cualquier_cosa") is None
    for destino in mate.VER_AYUDA_DE.values():
        assert destino in mate.AYUDA, destino
    # cada ejemplo es un programa entero que corre (y sus pruebas pasan)
    (tmp_path / "catalogo.mate").write_text("sea iva = 0.21\n", encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    for palabra, (que, ejemplo) in mate.AYUDA.items():
        assert palabra in ejemplo or palabra in ("lista", "mapa"), palabra
        programa = mate.analizar(ejemplo)
        assert mate.verificar(programa) == [], palabra
        salida = []
        interprete = mate.Interprete(salida=salida.append)
        resultados = interprete.correr(programa, pruebas=True)
        assert all(error is None for _, error in resultados), (palabra, resultados)
        assert interprete.errores_agentes == [], palabra
        assert salida or resultados, palabra


def test_el_readme_cuenta_lo_de_la_tanda_8():
    leeme = (RAIZ / "README.md").read_text(encoding="utf-8")
    for frase in ["mate.py consola", "### La consola", "ayuda mientras", "| `ayuda si` |",
                  "### Archivos de texto: `leer_archivo` y `escribir_archivo`",
                  "### La fecha y la hora: `hoy` y `ahora`", '`"archivo"`',
                  "`hoy`, `ahora`, `leer_archivo` y `escribir_archivo` son funciones incluidas"]:
        assert frase in leeme, frase
    assert '"archivo"' in mate.texto_de_guia() and "escribir_archivo" in mate.texto_de_guia()


# ───────────── Revisión final: lo que encontraron los revisores ─────────────

def test_dos_puntos_y_salto_de_renglon_no_es_una_ruta_de_windows():
    assert mostrados('mostrar("Descripción:\\n- yerba")') == ["Descripción:\n- yerba"]
    for texto in ['"Año:\\n2025"', '"Atención:\\tcerrado"', '"Opción A:\\nyerba"',
                  '"a o b:\\n"', '"Total:\\n5"', '"Opción B:\\n1.5 kg"']:
        assert len(mostrados(f"mostrar({texto})")) == 1, texto
    for ruta in ['"C:\\temp"', '"C:\\temp\\nuevo"', '"está en D:\\notas.txt"', '"C:\\datos"']:
        assert "ruta" in falla(f"mostrar({ruta})").mensaje, ruta


def test_asegurar_falla_no_se_cumple_por_un_renglon_que_no_usa_el_valor():
    resultados = probar("""
        funcion dividir(a, b) { devolver a / b }
        prueba "numero valido" { asegurar falla { numero("12") } }
        prueba "cuenta que anda" { asegurar falla { 10 / 2 } }
        prueba "fallan de verdad" {
            asegurar falla { 10 / 0 }
            asegurar falla { numero("x") }
            asegurar falla { dividir(1, 0) }
        }
        prueba "nombre mal tipeado" { asegurar falla { dividr(1, 0) } }
    """)
    assert resultados["numero valido"].endswith("se esperaba que esto fallara, y no falló")
    assert resultados["cuenta que anda"].endswith("se esperaba que esto fallara, y no falló")
    assert resultados["fallan de verdad"] is None
    assert "no llegó a probarse: no existe 'dividr'. ¿Quisiste decir 'dividir'?" \
        in resultados["nombre mal tipeado"]


def test_el_renglon_que_no_usa_el_valor_no_se_ataja_y_se_avisa_antes_de_correr():
    error = falla('intentar {\n numero("5")\n mostrar("es")\n} si falla e {\n mostrar("no")\n}')
    assert error.linea == 2 and "numero() devuelve un valor" in error.mensaje
    assert correr('intentar { sea n = numero("x") } si falla e { mostrar("no") }')[0] == ["no"]
    # una cuenta suelta se avisa aunque esté en una parte que no se ejecuta
    with pytest.raises(mate.ErrorMate) as info:
        mate.analizar("mostrar(1)\nsi falso {\n  1 + 1\n}")
    assert info.value.linea == 3 and "calcula un valor" in info.value.mensaje
    assert "calcula un valor" in falla("intentar { [1, 2][0] } si falla { mostrar(1) }").mensaje


def test_como_se_llego_termina_en_el_origen_aunque_haya_muchas_llamadas():
    error = falla("""funcion baja(n) {
    si n == 0 { devolver 1 / 0 }
    devolver baja(n - 1)
}
funcion empezar() {
    devolver baja(200)
}
mostrar(empezar())""")
    interprete = mate.Interprete()
    assert interprete.camino(error).endswith(
        "..., llamada desde empezar() (línea 6), llamada desde la línea 8")
    assert len(error.camino) <= 40


def test_probar_varios_archivos_guarda_todas_las_conversaciones(tmp_path, capsys, monkeypatch):
    (tmp_path / "ag.mate").write_text(
        'mensaje P {}\nagente V { al recibir P como p { responder 1 } }\n'
        'prueba "x" { asegurar preguntar P {} a V == 1 }\n', encoding="utf-8")
    (tmp_path / "sinp.mate").write_text('mostrar("hola")\n', encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    assert mate.main(["probar", "ag.mate", "sinp.mate", "--traza=t.txt"]) == 0
    out = capsys.readouterr().out
    assert "quedó guardada en t.txt" in out and "se sumó a t.txt" in out
    guardado = (tmp_path / "t.txt").read_text(encoding="utf-8-sig")
    assert "Conversación de ag.mate" in guardado and "(programa) pregunta a V: P" in guardado
    assert "Conversación de sinp.mate" in guardado and guardado.count("Resumen:") == 2
    # con un solo archivo se pisa, como siempre
    assert mate.main(["probar", "sinp.mate", "--traza=t.txt"]) == 0
    assert "ag.mate" not in (tmp_path / "t.txt").read_text(encoding="utf-8-sig")


def test_una_letra_que_no_se_puede_leer_no_cierra_la_consola_ni_rompe_leer():
    pendientes = ["sea x = 1", UnicodeDecodeError("charmap", b"\x8d", 0, 1, "x"), "x + 1"]
    mostrado = []

    def entrada(_pregunta):
        if not pendientes:
            raise EOFError
        siguiente = pendientes.pop(0)
        if isinstance(siguiente, Exception):
            raise siguiente
        return siguiente

    assert mate.consola(entrada=entrada, mostrar=mostrado.append) == 0
    assert "una letra que no pude entender" in mostrado[2] and mostrado[3] == "2"

    def teclado_roto(_pregunta):
        raise UnicodeDecodeError("charmap", b"\x8d", 0, 1, "x")

    interprete = mate.Interprete(salida=lambda _: None)
    interprete.entrada = teclado_roto
    with pytest.raises(mate.ErrorMate) as info:
        interprete.correr(mate.analizar('sea n = leer("¿Nombre?")'))
    assert "una letra que no pude entender" in info.value.mensaje


def test_la_entrada_redirigida_con_otra_codificacion_no_da_un_error_interno(tmp_path):
    import os
    import subprocess
    r = subprocess.run(
        [sys.executable, str(RAIZ / "mate.py"), "consola"],
        input='mostrar("Índice")\nmostrar(1 + 1)\nsalir\n'.encode("utf-8"),
        capture_output=True, env={**os.environ, "PYTHONIOENCODING": "cp1252"})
    assert r.returncode == 0 and b"error interno" not in r.stderr + r.stdout
    assert b"ndice" in r.stdout and b"2" in r.stdout


def test_crear_en_una_condicion_con_la_llave_del_bloque_abajo():
    base = "mensaje P {}\nagente V { estado n = 1\n al recibir P como p { responder n } }\n"
    assert mostrados(base + 'sea primero = crear V\nsi primero != crear V\n{\n'
                            '  mostrar("distintos")\n}') == ["distintos"]
    # fuera de una condición la llave de abajo sigue siendo el estado inicial
    assert mostrados(base + "sea v = crear V\n{ n: 7 }\nmostrar(preguntar P {} a v)") == ["7"]


def test_la_guia_dice_bien_lo_de_los_textos_dentro_de_las_llaves():
    guia = mate.texto_de_guia()
    assert "no se\n  puede haber" not in guia and "no se puede haber" not in guia
    assert "puede haber otros textos, con sus comillas" in guia
    assert "variables ('sea' y 'var')" in guia and "21 / 100" in guia


def test_ayuda_de_al_fallar_y_de_varias_palabras(capsys):
    assert mate.main(["ayuda", "al", "fallar"]) == 0
    out = capsys.readouterr().out
    assert out.startswith("al fallar: dentro de un agente") and "al fallar como f" in out
    assert mate.main(["ayuda", "fallar"]) == 0
    assert "ayuda al fallar" in capsys.readouterr().out
    assert mate.main(["ayuda", "si", "falla"]) == 0
    out = capsys.readouterr().out
    assert "la ayuda es de a una palabra" in out and "si: hace una cosa u otra" in out
    assert mate.main(["ayuda", "xx", "yy"]) == 2
    assert "no tengo ayuda sobre 'xx yy'" in capsys.readouterr().err
    assert any("al fallar: dentro" in r for r in en_consola("ayuda al fallar", "salir"))


def test_usar_sin_extension_tambien_da_pistas(tmp_path):
    (tmp_path / "catalogo.mate").write_text("sea iva = 0.21\n", encoding="utf-8")
    (tmp_path / "nota.mate.txt").write_text("sea x = 1\n", encoding="utf-8")
    principal = str(tmp_path / "p.mate")
    with pytest.raises(mate.ErrorMate) as info:
        mate.analizar('usar "catalgo"', principal)
    assert "¿Quisiste decir 'catalogo.mate'?" in info.value.mensaje
    with pytest.raises(mate.ErrorMate) as info:
        mate.analizar('usar "nota"', principal)
    assert "Encontré nota.mate.txt" in info.value.mensaje


def test_un_nombre_que_vino_con_usar_dice_de_donde_viene(tmp_path):
    (tmp_path / "lib.mate").write_text(
        "var contador = 0\nsea iva = 0.21\nmensaje Consulta { producto: texto }\n"
        "funcion f() { devolver 1 }\n", encoding="utf-8")
    principal = str(tmp_path / "p.mate")

    def error_de(fuente):
        programa = mate.analizar(fuente, principal)
        errores = mate.verificar(programa)
        if errores:
            return errores[0][1]
        with pytest.raises(mate.ErrorMate) as info:
            mate.Interprete(salida=lambda _: None).correr(programa)
        return info.value.mensaje

    for fuente in ['usar "lib"\nsea iva = 0.105', 'usar "lib"\nfuncion f() { devolver 2 }',
                   'usar "lib"\nmensaje Consulta { producto: texto }']:
        mensaje = error_de(fuente)
        assert "viene de lib.mate, que se trajo con 'usar'" in mensaje, mensaje
        assert "iva = ..." not in mensaje
    # los 'var' también vienen (una función traída puede necesitarlos), y está documentado
    salida = []
    mate.Interprete(salida=salida.append).correr(
        mate.analizar('usar "lib"\ncontador = 5\nmostrar(contador)', principal))
    assert salida == ["5"]
    assert "variables (`sea` y `var`)" in (RAIZ / "README.md").read_text(encoding="utf-8")
    # en el mismo archivo el error es el de siempre
    assert "ya está definido en este bloque" in falla("sea iva = 1\nsea iva = 2").mensaje


def test_la_posicion_con_decimales_no_dice_que_dio_un_entero():
    error = falla("sea l = [1, 2, 3, 4]\nmostrar(l[largo(l) * 0.5])")
    assert "dio 2" not in error.mensaje and "salió de una cuenta con decimales" in error.mensaje
    assert "redondear" in error.mensaje
    assert "dio 1.5" in falla("sea l = [1, 2, 3, 4]\nmostrar(l[1.5])").mensaje
    assert mostrados("sea l = [1, 2, 3, 4]\nmostrar(l[4 / 2], l[redondear(4 * 0.5)])") == ["3 3"]


def test_el_nombre_de_una_copia_tiene_que_ser_un_texto():
    base = "mensaje P {}\nagente V { al recibir P como p { responder 1 } }\n"
    assert "tiene que ser un texto, y recibió el valor nada" in falla(
        base + "sea nombre = nada\nsea a = crear V llamado nombre").mensaje
    assert "recibió una lista" in falla(base + "sea a = crear V llamado [1]").mensaje
    error = falla(base + "sea a = crear V llamado 5")
    assert "recibió un número" in error.mensaje and "Pasalo a texto" in error.mensaje
    error = falla(base + "sea sur = crear V llamado Sur { }")
    assert 'va entre comillas: crear V llamado "Sur"' in error.mensaje
    assert mostrados(base + 'sea n = 5\nmostrar(crear V llamado "Sucursal {n}")') == [
        "V Sucursal 5"]


def test_en_la_consola_un_renglon_que_termina_en_operador_sigue_abajo():
    assert en_consola("1 +", "2", "sea t = 10 *", "3", "t", "salir") == ["3", "30"]
    mostrado = en_consola("sea x = 1", "x +", "", "salir")
    assert len(mostrado) == 1 and "archivo" not in mostrado[0]
    assert "quedó a medio terminar" in mostrado[0]
    assert "archivo" not in en_consola("sea x =", "salir")[0]
    assert "no un porcentaje" in en_consola("sea iva = 21%", "salir")[0]


def test_si_no_se_puede_guardar_el_archivo_queda_como_estaba(tmp_path, capsys):
    codigo, out, err = por_main(tmp_path, capsys, """
        escribir_archivo("datos.txt", "importante")
        sea raro = de_json("\\"\\\\ud800\\"")
        intentar { escribir_archivo("datos.txt", "nuevo " + raro) } si falla e {
            mostrar(e)
            mostrar(detalle_de(e).clase)
        }
        mostrar("quedó: [" + leer_archivo("datos.txt") + "]")
    """)
    assert codigo == 0 and "una letra que no se puede guardar" in out
    assert "archivo\n" in out and "quedó: [importante]" in out and "permiso" not in out


def test_un_sea_de_un_bloque_de_adentro_no_tapa_un_var_del_programa():
    error = falla("var cuenta = 0\nfuncion contar(lista) {\n    para i en lista {\n"
                  "        sea cuenta = i\n    }\n    devolver cuenta\n}\n"
                  "mostrar(contar([1, 2, 3]))")
    assert error.linea == 4 and "'cuenta' ya existe afuera de este bloque" in error.mensaje
    resultados = probar('var cuenta = 0\nprueba "x" {\n para i en [1, 2] { sea cuenta = i }\n'
                        " asegurar cuenta == 0\n}")
    assert "ya existe afuera" in resultados["x"]
    assert "ya existe afuera" in probar(
        "var cuenta = 0\nmensaje P {}\nagente A { al recibir P {\n si verdadero { sea cuenta = 1 }\n"
        ' responder 1 } }\nprueba "x" { asegurar preguntar P {} a A == 1 }')["x"]
    # directo en la función o la prueba sigue valiendo, y con un 'sea' fijo de afuera también
    assert mostrados("var cuenta = 0\nfuncion f() {\n sea cuenta = 5\n devolver cuenta\n}\n"
                     "mostrar(f(), cuenta)") == ["5 0"]
    assert mostrados("sea total = 1\nfuncion f() {\n para i en [7] { sea total = i\n"
                     " devolver total }\n}\nmostrar(f())") == ["7"]


def test_la_copia_creada_por_un_agente_que_falla_se_deshace():
    salida, _ = correr("""
        mensaje Alta { nombre: texto, falla: logico }
        mensaje Ver {}
        agente Suc { al recibir Ver como v { responder 1 } }
        agente Central {
            estado sucs = []
            al recibir Alta como a {
                sea s = crear Suc llamado a.nombre
                sucs = agregar(sucs, s)
                si a.falla { fallar "no se pudo" }
                responder largo(sucs)
            }
        }
        intentar { mostrar(preguntar Alta { nombre: "Norte", falla: verdadero } a Central) }
        si falla e { mostrar("falló:", e) }
        mostrar(preguntar Alta { nombre: "Norte", falla: falso } a Central)
        intentar { mostrar(preguntar Alta { nombre: "Norte", falla: falso } a Central) }
        si falla e { mostrar(tiene(e, "ya hay un Suc")) }
    """)
    assert salida == ["falló: no se pudo", "1", "verdadero"]


def test_el_tope_de_tamano_vale_para_unir_texto_json_y_agregar(monkeypatch):
    monkeypatch.setattr(mate, "MAX_LARGO", 1000)
    base = "sea a = rango(600)\n"
    for cuenta in ['unir(a, ",")', "a_json(a)", '"{a}{a}"', "texto(a)", "texto([a, a, a])",
                   'unir(rango(400), "---")', "a_json([a, a])"]:
        mensaje = falla(base + f"mostrar(largo({cuenta}))").mensaje
        assert "demasiado largo (más de 1.000 letras)" in mensaje, cuenta
    assert "demasiado larga" in falla("sea b = rango(1000)\nsea c = agregar(b, 1)").mensaje
    # una lista hecha de la misma lista muchas veces no cuelga a mostrar()
    assert "demasiado largo" in falla(base + "sea b = [a, a]\nmostrar([b, b])").mensaje
    assert mostrados('sea c = rango(100)\nmostrar(largo(unir(c, ",")), largo(agregar(c, 1)))') \
        == ["289 101"]


def test_el_readme_aclara_los_decimales_grandes():
    leeme = (RAIZ / "README.md").read_text(encoding="utf-8")
    assert "menos de 10.000 millones" in leeme and "33333333333.333332" in leeme
    assert mostrados("mostrar(100000000000 / 3, 10 / 3)") == ["33333333333.333332 3.33333333333"]


def test_numero_de_un_texto_vacio_es_de_la_clase_numero():
    assert mostrados('intentar { mostrar(numero("")) } si falla e { mostrar(detalle_de(e).clase) }'
                     ) == ["numero"]


def test_el_error_del_final_del_archivo_señala_un_renglon_que_existe(tmp_path, capsys):
    with pytest.raises(mate.ErrorMate) as info:
        mate.analizar("sea x =\n")
    assert info.value.linea == 1
    codigo, _, err = por_main(tmp_path, capsys, "mostrar(1)\nsi verdadero {\n  mostrar(2)\n\n\n")
    assert codigo == 1 and "programa.mate:3: error: la llave que se abrió en la línea 2" in err
    assert "    3 |   mostrar(2)" in err


def test_de_json_arma_los_mensajes_de_adentro():
    base = ("mensaje Item { producto: texto, cantidad: numero }\n"
            "mensaje Pedido { cliente: texto, items: lista de Item, extra: Item? }\n")
    assert mostrados(base + 'mostrar(de_json("[\\{\\"producto\\": \\"y\\", \\"cantidad\\": 2}]", '
                            '"lista de Item"))') == ['[Item { producto: "y", cantidad: 2 }]']
    salida = mostrados(
        base + 'sea p = de_json("\\{\\"cliente\\": \\"Ana\\", \\"items\\": [\\{\\"producto\\": '
               '\\"yerba\\", \\"cantidad\\": 2}], \\"extra\\": \\{\\"producto\\": \\"te\\", '
               '\\"cantidad\\": 1}}", "Pedido")\nmostrar(tipo(p.items[0]), p.extra.producto)')
    assert salida == ["Item te"]
    error = falla(base + 'mostrar(de_json("[\\{\\"producto\\": 5, \\"cantidad\\": 2}]", '
                         '"lista de Item"))')
    assert "Item.producto es de tipo texto" in error.mensaje and error.familia == "contrato"
    # las formas reservadas de a_json están avisadas en el README
    leeme = (RAIZ / "README.md").read_text(encoding="utf-8")
    assert '`{"agente": "Vendedor"}` es un agente' in leeme


def test_un_tipo_que_no_existe_no_arrastra_un_segundo_error():
    assert revisar("mensaje P { pr: lista de Nada }\nmostrar(P { pr: [1] })") == [
        (1, "P.pr: no existe el tipo 'Nada'")]


def test_un_invisible_en_el_medio_de_una_palabra_se_avisa():
    error = falla("sea x = 1\nmos\u200btrar(x)\n")
    assert error.linea == 2 and "carácter invisible después de 'mos'" in error.mensaje
    assert "U+200B" in error.mensaje
    # entre palabras o al final del renglón sigue sin molestar
    assert mostrados("sea\u200b x = 1\nmostrar(x)\u200b\n") == ["1"]


def test_un_porcentaje_con_el_signo_se_explica_en_su_renglon():
    error = falla("sea precio = 100\nsea descuento = 10%\nmostrar(precio - descuento)")
    assert error.linea == 2 and "no un porcentaje" in error.mensaje
    assert "10 / 100 (o 0.1)" in error.mensaje
    assert "21 / 100" in falla("sea iva = 21%\nsea precio = 100").mensaje
    assert "no un porcentaje" in falla("mostrar(100 * 21%)").mensaje
    assert mostrados("sea n = 7\nmostrar(10 % 3, n %\n 2)") == ["1 1"]


def test_si_no_separado_dice_que_va_junto():
    error = falla('sea stock = 3\nsi stock == 0 {\n    mostrar("sin")\n} si no {\n'
                  '    mostrar("hay")\n}')
    assert error.linea == 4 and "'sino', todo junto" in error.mensaje
    assert mostrados('sea listo = falso\nsi no listo { mostrar("falta") }') == ["falta"]


def test_un_nombre_que_no_existe_no_sugiere_una_funcion_poco_parecida():
    assert falla("precio = 5").mensaje == \
        "no existe 'precio'. Para crear la variable escribí: var precio = ..."
    assert falla("sea l = []\nmostrar(ordenar(l, precio))").mensaje == "no existe 'precio'"
    assert "porcion" not in falla("mostrar(precio)").mensaje
    assert "¿Quisiste decir 'mostrar'?" in falla("mostar(1)").mensaje
    assert "¿Quisiste decir 'total'?" in falla("var total = 1\ntotl = 2").mensaje


def test_un_fallar_condicional_no_cuenta_como_responder():
    fuente = """mensaje Vender { producto: texto, cantidad: numero }
agente Deposito {
    estado stock = { azucar: 1 }
    al recibir Vender como v {
        si stock[v.producto] < v.cantidad { fallar "no alcanza" }
        stock[v.producto] -= v.cantidad
    }
}
prueba "vender" {
    asegurar falla { preguntar Vender { producto: "azucar", cantidad: 1 } a Deposito }
}"""
    assert [linea for linea, _ in revisar(fuente)] == [10]
    assert "nunca responde" in revisar(fuente)[0][1]
    # un agente que falla siempre, a propósito, se puede seguir preguntando (y atajando)
    assert mostrados('mensaje P {}\nagente Roto { al recibir P { fallar "roto" } }\n'
                     "intentar { sea r = preguntar P {} a Roto } si falla e { mostrar(e) }") \
        == ["roto"]


def test_al_recibir_un_mensaje_mal_tipeado_sugiere_el_parecido():
    errores = revisar('mensaje Pedido { producto: texto }\nagente V {\n'
                      ' al recibir Pedidos como p { mostrar("vendo") }\n}')
    assert errores == [(3, "V recibe 'Pedidos', que no es un mensaje declarado. "
                           "¿Quisiste decir 'Pedido'?")]


def test_comparar_fechas_con_menor_es_un_error_y_no_un_resultado_equivocado():
    error = falla('sea vence = "01/12/2026"\nsi "21/11/2026" < vence { mostrar("no venció") }')
    assert error.linea == 2 and "las fechas son textos" in error.mensaje
    assert "fechas" in falla('mostrar(ahora() >= "01/01/2025 10:00")').mensaje
    assert mostrados('mostrar("21/11/2026" == "21/11/2026", "ana" < "beto")') == [
        "verdadero verdadero"]
    assert "compararlos con `<` o `>` es un error" in \
        (RAIZ / "README.md").read_text(encoding="utf-8")


def test_el_readme_cuenta_lo_de_la_revision_final():
    leeme = (RAIZ / "README.md").read_text(encoding="utf-8")
    for frase in ["ayuda al fallar", "`sea iva = 21%`", "`sino`, todo junto",
                  "una sección por archivo", "ya no se ataja con `intentar`",
                  "un `fallar` adentro de un `si` no cuenta", "tiene que ser un\ntexto",
                  "esa copia se deshace", "avisa si el Bloc de notas lo guardó",
                  "es la forma de llamarla"]:
        assert frase in leeme, frase
    assert "Revisión final" in (RAIZ / "MEJORAS.md").read_text(encoding="utf-8")


# ── Tanda 9: nombres que no existen antes de correr, la traza con las fallas y un solo
#    formato de errores ──

# Mejora 59: la revisión previa detecta nombres que no existen

def test_un_nombre_que_no_existe_se_avisa_antes_de_correr(tmp_path, capsys):
    codigo, out, err = por_main(tmp_path, capsys, """sea total = 10
funcion poco_usada(x) {
    si x > 100 {
        mostrar(totl)
    }
    devolver x
}
mostrar("arranca")
""")
    archivo = tmp_path / "programa.mate"
    # antes corría (nadie llama a poco_usada con más de 100); ahora ni arranca
    assert (codigo, out) == (1, "")
    assert err.splitlines() == [
        f"{archivo}:4: error: no existe 'totl'. ¿Quisiste decir 'total'?",
        "    4 |         mostrar(totl)"]
    codigo, out, err = por_main(tmp_path, capsys, "mostrar(1)\nsi falso { cuenta = 5 }\n",
                                orden="verificar")
    assert codigo == 1 and "Para crear la variable escribí: var cuenta = ..." in err


@pytest.mark.parametrize("fuente,linea,nombre", [
    ("si falso { mostrar(zzz) }", 1, "zzz"),
    ("funcion f() {\n devolver zzz\n}", 2, "zzz"),
    ("para i en [1] { sea adentro = i }\nfuncion f() { devolver adentro }", 2, "adentro"),
    ("si verdadero { sea a = 1 } sino { mostrar(a) }", 1, "a"),
    ("funcion f(a) { devolver a }\nfuncion g() { devolver a }", 2, "a"),
    ("mensaje P {}\nagente A {\n estado n = 0\n al recibir P como p { responder m }\n}", 4, "m"),
    ("mensaje P {}\nagente A {\n estado n = 0\n al recibir P { responder 1 }\n}\n"
     "agente B {\n al recibir P { responder n }\n}", 7, "n"),
    ("mensaje P {}\nagente A {\n funcion f() { devolver 1 }\n al recibir P { responder 1 }\n}\n"
     "mostrar(f())", 6, "f"),
    ("mensaje P {}\nagente A {\n al recibir P como p { responder 1 }\n"
     " al recibir P2 como q { responder p }\n}\nmensaje P2 {}", 4, "p"),
    ('prueba "a" { sea local = 1 }\nprueba "b" { asegurar local == 1 }', 2, "local"),
    ("intentar { mostrar(1) } si falla e { mostrar(e) }\nmostrar(e)", 2, "e"),
    ("intentar { mostrar(1) } si falla e { mostrar(zzz) }", 1, "zzz"),
    ('mostrar("total: {zzz + 1}")', 1, "zzz"),
    ("sea m = { a: [1, zzz] }", 1, "zzz"),
    ("mensaje P { n: numero }\nagente A { al recibir P { responder 1 } }\n"
     "sea r = preguntar P { n: zzz } a A", 3, "zzz"),
    ("mensaje P {}\nagente A { al recibir P { responder 1 } }\nenviar P {} a zzz", 3, "zzz"),
    ("mensaje P {}\nagente A {\n estado n = 0\n al recibir P { responder n }\n}\n"
     'prueba "s" {\n simular A al recibir P { responder n }\n}', 7, "n"),
    ("mensaje P {}\nagente A {\n estado n = zzz\n al recibir P { responder n }\n}", 3, "zzz"),
    ("sea v = crear A { n: zzz }\nmensaje P {}\nagente A {\n estado n = 0\n"
     " al recibir P { responder n }\n}", 1, "zzz"),
    ("var l = [1]\nl[zzz] = 2", 2, "zzz"),
    ("zzz.campo = 2", 1, "zzz"),
    ("mientras falso { zzz += 1 }", 1, "zzz"),
    ("asegurar 1 == 1, zzz", 1, "zzz"),
    ("mostrar(Total)", 1, "Total"),
])
def test_nombres_que_no_existen_en_cada_rincon(fuente, linea, nombre):
    errores = revisar(fuente)
    assert [(n, t.split(".")[0].split(":")[0]) for n, t in errores] == [
        (linea, f"no existe '{nombre}'")], errores


SIN_AVISOS = """usar "lib9.mate"
mensaje Sumar { a: numero, b: numero }
mensaje Total
mensaje Arrancar { a_quien: agente }

funcion sumador(n) {
    funcion suma(x) { devolver x + n + global_de_abajo }
    devolver suma
}
funcion usa_despues() { devolver definida_despues(2) }
funcion definida_despues(x) {
    var acum = 0
    para i, v en [x, x] {
        si i == 0 {
            sea doble = v * 2
            acum += doble
        } sino { acum += v }
    }
    para letra en "ab" { acum += largo(letra) }
    intentar { acum = acum / 0 } si falla motivo { acum += largo(motivo) - largo(motivo) }
    devolver acum
}
sea global_de_abajo = 1
agente Calc {
    estado usos = 0
    estado historial = []
    estado tope = largo(historial) + base_lib
    funcion anotar(v) {
        historial = agregar(historial, v)
        usos += 1
        devolver ultimo(historial)
    }
    al recibir Sumar como s {
        sea r = anotar(s.a + s.b)
        responder r
    }
    al recibir Total { responder usos }
    al recibir Arrancar como m {
        enviar Pedir { que: "sal" } a m.a_quien
        mostrar("{yo} arrancó, lo pidió {remitente}")
    }
    al fallar como f { mostrar("falló {f.destino}: {f.motivo}") }
}
sea mas3 = sumador(3)
sea copia = crear Calc llamado "B" { usos: global_de_abajo }
mostrar(mas3(1), usa_despues(), con_iva(100))
mostrar(preguntar Sumar { a: 1, b: 2 } a Calc, preguntar Total {} a copia)
enviar Arrancar { a_quien: Deposito } a Calc
var lista = [1, 2]
lista[0] = contador_lib
para clave, v en { a: 1 } { mostrar(clave, v) }

prueba "todo junto" {
    sea local = 7
    simular Deposito al recibir Pedir como p { responder largo(p.que) + local }
    asegurar preguntar Pedir { que: "x" } a Deposito == 8
    asegurar falla { largo() }
    asegurar falla { mas3(1, 2) }
    intentar { tampoco_existo } si falla e { asegurar detalle_de(e).clase == "nombre" }
    asegurar usa_despues() == 8
}
"""


def test_la_revision_de_nombres_no_avisa_de_mas(tmp_path, capsys):
    """Ante la duda no avisa: bloques, funciones hechas por funciones, agentes, 'usar',
    pruebas, 'simular' y nombres declarados más abajo. Este programa usa todo eso y anda."""
    (tmp_path / "lib9.mate").write_text(
        "mensaje Pedir { que: texto }\nsea iva = 0.21\nvar contador_lib = 0\n"
        "funcion con_iva(p) { devolver p * (1 + iva) + base_lib - base_lib }\n"
        "sea base_lib = 5\n"
        "agente Deposito {\n    estado stock = { yerba: 10 }\n"
        "    funcion hay(que) { devolver tiene(stock, que) }\n"
        '    al recibir Pedir como p {\n        si no hay(p.que) { fallar "no hay {p.que}" }\n'
        "        responder stock[p.que]\n    }\n}\n", encoding="utf-8")
    codigo, out, err = por_main(tmp_path, capsys, SIN_AVISOS, orden="probar")
    assert (codigo, err) == (0, ""), out + err
    assert out.splitlines()[:5] == ["5 8 121", "3 1", "a 1", "Calc arrancó, lo pidió nada",
                                    "falló Deposito: no hay sal"]
    assert out.splitlines()[-1] == "1 de 1 pruebas pasaron"


def test_ni_los_ejemplos_ni_la_guia_reciben_avisos_de_nombres():
    for ejemplo in sorted((RAIZ / "ejemplos").glob("*.mate")):
        programa = mate.analizar(ejemplo.read_text(encoding="utf-8"), str(ejemplo))
        assert mate.verificar(programa) == [], ejemplo.name
    guia = mate.texto_de_guia().split("--- ejemplo ---")[1].split("--- fin del ejemplo ---")[0]
    assert revisar(guia) == []
    assert "ANTES DE CORRER" in mate.texto_de_guia()


def test_adentro_de_intentar_y_de_asegurar_falla_no_se_revisan_los_nombres():
    # ahí la falla se ataja, o es lo que se está probando: sigue como antes
    assert mostrados("intentar { mostrar(no_esta) } si falla e { mostrar(e) }") == [
        "no existe 'no_esta'"]
    assert mostrados('intentar { largo() } si falla e { mostrar("atajado") }') == ["atajado"]
    assert revisar('funcion f(a) { devolver a }\nprueba "p" { asegurar falla { f(1, 2) } }') == []
    assert revisar('prueba "p" { asegurar falla { dividr(1, 0) } }') == []
    # pero una función que solo se llama desde un 'intentar' se revisa como cualquiera
    assert revisar("funcion f() { devolver zzz }\nintentar { f() } si falla e { mostrar(e) }") \
        == [(1, "no existe 'zzz'")]


def test_el_mismo_nombre_que_falta_se_avisa_una_sola_vez_y_los_distintos_todos():
    errores = revisar("funcion f() {\n mostrar(uno)\n mostrar(uno)\n mostrar(dos)\n}")
    assert errores == [(2, "no existe 'uno'"), (4, "no existe 'dos'")]
    # un mensaje nombrado sin llaves ya tiene su aviso: no se suma otro
    errores = revisar("mensaje Ping {}\nagente A { al recibir Ping { responder 1 } }\n"
                      "si falso { sea r = preguntar Ping a A }")
    assert len(errores) == 1 and "Escribí Ping {}" in errores[0][1]


def test_la_cantidad_de_valores_de_una_llamada_se_revisa_antes_de_correr(tmp_path, capsys):
    assert revisar("si falso { mostrar(largo([1], 2)) }") == [
        (1, "largo() lleva 1 valor y recibió 2. Por ejemplo: largo(lista)")]
    assert revisar("funcion doble(n) { devolver n * 2 }\nsi falso { mostrar(doble(1, 2)) }") == [
        (2, "doble() espera 1 argumento(s) y recibió 2")]
    assert revisar("mensaje P {}\nagente A {\n funcion f(a, b) { devolver a }\n"
                   " al recibir P { responder f(1) }\n}") == [
        (4, "f() espera 2 argumento(s) y recibió 1")]
    # ante la duda no avisa: un nombre que se le pone a dos cosas, o una función que llega
    # como valor, se controlan recién al correr
    assert revisar("funcion f(a) { devolver a }\nfuncion g(f) { devolver f(1, 2) }") == []
    assert revisar("funcion f(a) { devolver a }\nsea h = f\nsi falso { mostrar(h(1, 2)) }") == []
    assert revisar("mostrar()\nmostrar(1, 2, 3)\nsea r = rango(1, 10, 3)\nsea h = hoy()") == []
    codigo, out, err = por_main(tmp_path, capsys, "mostrar(1)\nsi falso { mostrar(hoy(1)) }\n")
    assert (codigo, out) == (1, "") and ":2: error: hoy() lleva 0 valores y recibió 1" in err


def test_en_la_consola_no_se_avisa_de_nombres_que_todavia_no_se_escribieron():
    renglones = iter(["funcion f(x) { devolver x + falta }", "sea falta = 2", "mostrar(f(1))",
                      "funcion g() { devolver largo() }", "salir"])
    mostrado = []
    mate.consola(entrada=lambda _: next(renglones), mostrar=mostrado.append)
    assert mostrado[2:] == ["3", "error: largo() lleva 1 valor y recibió 0. Por ejemplo: "
                                 "largo(lista)"]


# Mejora 63: una traza que muestra las fallas (y mejora 65: la respuesta que se descarta)

TRAZA = """mensaje Pedido { producto: texto }
mensaje Comprar { producto: texto }
mensaje Avisar { producto: texto }
mensaje Mudo
agente Vendedor {
    al recibir Pedido como p {
        si p.producto != "yerba" { fallar "no vendo {p.producto}" }
        responder 3500
    }
    al recibir Mudo { si 1 > 2 { responder 1 } }
}
agente Comprador {
    al recibir Comprar como c {
        intentar {
            responder preguntar Pedido { producto: c.producto } a Vendedor
        } si falla e {
            responder 0
        }
    }
    al recibir Avisar como a { enviar Pedido { producto: a.producto } a Vendedor }
}
"""


def test_la_traza_numera_sangra_y_muestra_las_fallas():
    salida, interprete = correr(TRAZA + """
        mostrar(preguntar Comprar { producto: "yerba" } a Comprador)
        mostrar(preguntar Comprar { producto: "café" } a Comprador)
        enviar Avisar { producto: "sal" } a Comprador
        intentar { preguntar Mudo {} a Vendedor } si falla e { mostrar("callado") }
    """, traza=True)
    assert salida == [
        '  ·  1. (programa) pregunta a Comprador: Comprar { producto: "yerba" }   (conversación 1)',
        '  ·  2.    Comprador pregunta a Vendedor: Pedido { producto: "yerba" }',
        "  ·  2.    Vendedor responde a Comprador: 3500",
        "  ·  1. Comprador responde a (programa): 3500",
        "3500",
        '  ·  3. (programa) pregunta a Comprador: Comprar { producto: "café" }   (conversación 2)',
        '  ·  4.    Comprador pregunta a Vendedor: Pedido { producto: "café" }',
        "  ·  4.    Vendedor falló: no vendo café",
        "  ·  3. Comprador responde a (programa): 0",
        "0",
        '  ·  5. (programa) → Comprador: Avisar { producto: "sal" }   (conversación 3)',
        '  ·  6. Comprador → Vendedor: Pedido { producto: "sal" }   (conversación 3)',
        "  ·  6. Vendedor falló: no vendo sal",
        "  ·  7. (programa) pregunta a Vendedor: Mudo   (conversación 4)",
        "  ·  7. Vendedor sin respuesta: terminó de atender Mudo sin llegar a un 'responder'",
        "callado"]
    # el último número es la cantidad de mensajes del resumen
    assert interprete.cuenta == {"enviar": 2, "preguntar": 5, "fallaron": 3}
    assert interprete.errores_agentes == ["línea 7: Vendedor al recibir Pedido: no vendo sal"]


def test_el_archivo_de_la_traza_usa_el_mismo_formato(tmp_path, capsys):
    destino = tmp_path / "c.txt"
    codigo, out, err = por_main(
        tmp_path, capsys, TRAZA + 'mostrar(preguntar Comprar { producto: "café" } a Comprador)\n',
        f"--traza={destino}")
    assert (codigo, err) == (0, "") and out.splitlines()[0] == "0"
    guardado = destino.read_text(encoding="utf-8-sig").splitlines()
    assert guardado[2:6] == [
        '  ·  1. (programa) pregunta a Comprador: Comprar { producto: "café" }   (conversación 1)',
        '  ·  2.    Comprador pregunta a Vendedor: Pedido { producto: "café" }',
        "  ·  2.    Vendedor falló: no vendo café",
        "  ·  1. Comprador responde a (programa): 0"]
    assert guardado[-1] == ("Resumen: 2 mensaje(s) entregado(s): 0 con 'enviar' y 2 con "
                            "'preguntar'. Fallaron 1.")


def test_la_respuesta_a_un_enviar_del_programa_se_avisa_solo_en_la_traza(tmp_path, capsys):
    fuente = TRAZA + 'enviar Pedido { producto: "yerba" } a Vendedor\n'
    codigo, out, err = por_main(tmp_path, capsys, fuente)
    assert (codigo, out, err) == (0, "", "")  # sin traza, nada nuevo
    codigo, out, err = por_main(tmp_path, capsys, fuente, "--traza")
    assert (codigo, err) == (0, "")
    assert out.splitlines() == [
        '  ·  1. (programa) → Vendedor: Pedido { producto: "yerba" }   (conversación 1)',
        "  ·  1. la respuesta de Vendedor se descartó (para recibirla, usá 'preguntar' en vez "
        "de 'enviar'): 3500"]
    # entre agentes la respuesta sí llega (es un mensaje más), así que no hay aviso
    salida, _ = correr(AGENTES + """
        mensaje Empezar
        agente Cliente {
            al recibir Empezar { enviar Sumar { a: 1, b: 1 } a Calculadora }
            al recibir Resultado como r { mostrar("llegó {r.valor}") }
        }
        enviar Empezar {} a Cliente
    """, traza=True)
    assert not any("se descartó" in renglon for renglon in salida)
    # y el ejemplo que lo hace a propósito sigue igual sin traza, y lo cuenta con traza
    capsys.readouterr()
    assert mate.main(["correr", str(RAIZ / "ejemplos" / "mercado.mate"), "--traza"]) == 0
    capturado = capsys.readouterr()
    assert capturado.err == "" and capturado.out.count("se descartó") == 2


# Mejora 93: un solo formato para todos los errores

def test_los_errores_comunes_y_los_de_agentes_se_escriben_igual(tmp_path, capsys):
    fuente = """mensaje Ping
agente Roto { al recibir Ping { fallar "me rompí" } }
enviar Ping {} a Roto
prueba "las dos clases de error" {
    enviar Ping {} a Roto
    asegurar 1 == 2
}
"""
    archivo = tmp_path / "programa.mate"
    del_agente = [f"{archivo}:2: error: Roto al recibir Ping: me rompí",
                  '    2 | agente Roto { al recibir Ping { fallar "me rompí" } }']
    codigo, out, err = por_main(tmp_path, capsys, fuente)
    assert (codigo, out) == (1, "") and err.splitlines() == del_agente
    codigo, out, err = por_main(tmp_path, capsys, fuente, orden="probar")
    assert codigo == 1
    assert err.splitlines() == ["errores al correr el programa (antes de las pruebas):"] + del_agente
    assert out.splitlines() == [
        "  ✗ las dos clases de error",
        f"      {archivo}:6: error: no se cumplió lo asegurado: dio 1 y se esperaba 2",
        "          6 |     asegurar 1 == 2",
        "      " + del_agente[0],
        "      " + del_agente[1],
        "0 de 1 pruebas pasaron"]
    # por dentro también: el renglón va siempre adelante
    interprete = mate.Interprete(salida=lambda _: None)
    resultados = interprete.correr(mate.analizar(fuente), pruebas=True)
    assert resultados == [("las dos clases de error",
                           "línea 6: no se cumplió lo asegurado: dio 1 y se esperaba 2\n"
                           "línea 2: Roto al recibir Ping: me rompí")]


def test_el_readme_cuenta_lo_de_la_tanda_9():
    leeme = (RAIZ / "README.md").read_text(encoding="utf-8")
    for frase in ["Nombres que no existen, antes de correr", "ante la duda deja correr",
                  "adentro de `intentar { ... }` y de `asegurar falla { ... }` no revisa",
                  "Vendedor Sur falló: no vendo azucar", "`sin respuesta`", "se descartó",
                  "Todos los errores se escriben igual", "`archivo:renglón: error: lo que pasó`",
                  "`--traza` cambió de formato", "el programa ya no arranca",
                  "`probar` escribe los errores de cada prueba como `correr`"]:
        assert frase in leeme, frase
    mejoras = (RAIZ / "MEJORAS.md").read_text(encoding="utf-8")
    for numero in (59, 63, 65, 93):
        ficha = mejoras.split(f"\n**{numero}. ")[1].split("\n\n")[0]
        assert "Estado: hecha" in ficha and "Nota al hacerla" in ficha, numero


# ───────── Tanda 10: lo que había quedado "para más adelante" ─────────

# Mejora 95: valores por defecto en los parámetros

def test_un_parametro_puede_tener_valor_por_defecto():
    fuente = """
        funcion con_iva(precio, tasa = 0.21) { devolver precio * (1 + tasa) }
        funcion f(a, b = a * 2, c = b + 1) { devolver [a, b, c] }
        mostrar(con_iva(100), con_iva(100, 0.5))
        mostrar(f(1), f(1, 5), f(1, 5, 9))
    """
    assert mostrados(fuente) == ["121 150", "[1, 2, 3] [1, 5, 6] [1, 5, 9]"]
    # el valor se calcula en cada llamada, con lo que valgan las variables en ese momento
    assert mostrados("var base = 1\nfuncion g(x = base) { devolver x }\nmostrar(g())\n"
                     "base = 7\nmostrar(g(), g(3))") == ["1", "7 3"]
    # también en las funciones de un agente, y todos pueden tener valor
    assert mostrados("""
        mensaje Sumar { n: numero }
        agente Caja {
            estado total = 0
            funcion acumular(n, veces = 2) { total += n * veces }
            al recibir Sumar como s {
                acumular(s.n)
                acumular(s.n, 10)
                responder total
            }
        }
        funcion todo(a = 1, b = 2) { devolver a + b }
        mostrar(preguntar Sumar { n: 1 } a Caja, todo(), todo(5), todo(5, 5))
    """) == ["12 3 7 10"]


def test_los_parametros_con_valor_por_defecto_van_al_final_y_se_cuentan():
    error = falla("funcion f(a = 1, b) { devolver a }")
    assert error.linea == 1 and error.mensaje == (
        "f(): 'b' no tiene valor por defecto y está después de 'a', que sí tiene. Los "
        "parámetros con valor por defecto van al final: f(b, a = ...)")
    # la cantidad de valores se revisa antes de correr, con el mínimo y el máximo
    fuente = "funcion f(a, b = 2) { devolver a + b }\n"
    assert revisar(fuente + "si falso { mostrar(f()) }\nsi falso { mostrar(f(1, 2, 3)) }") == [
        (2, "f() espera entre 1 y 2 argumento(s) y recibió 0"),
        (3, "f() espera entre 1 y 2 argumento(s) y recibió 3")]
    assert revisar(fuente + "mostrar(f(1), f(1, 2))") == []
    # y al correr, cuando la función llega como valor
    error = falla(fuente + "sea g = f\nmostrar(g(1, 2, 3))")
    assert error.mensaje == "f() espera entre 1 y 2 argumento(s) y recibió 3"
    # un nombre que no existe en el valor por defecto se avisa antes de correr; uno de los
    # parámetros de antes, no
    assert revisar("funcion f(a, b = otro) { devolver a }") == [(1, "no existe 'otro'")]
    assert revisar("funcion f(a, b = c, c = 1) { devolver a }") == [(1, "no existe 'c'")]
    assert revisar("funcion f(a, b = a) { devolver b }") == []
    assert "el parámetro 'a' está repetido" in falla("funcion f(a, a = 1) { }").mensaje
    # el error de un valor por defecto que falla dice por dónde se llegó
    error = falla("funcion f(a, b = 1 / a) { devolver b }\nmostrar(f(0))")
    assert error.mensaje == "división por cero" and error.linea == 1


# Mejora 96: textos de varios renglones

TRES = '"' * 3


def test_un_texto_de_tres_comillas_ocupa_varios_renglones_y_pierde_la_sangria():
    fuente = f"""sea nombre = "Ana"
funcion carta(quien) {{
    devolver {TRES}
        Hola {{quien}}:
          te debo {{pesos(10 * 2)}} y "gracias".

        Chau \\{{llave\\}}
        {TRES}
}}
mostrar(carta(nombre))
"""
    assert mostrados(fuente) == ['Hola Ana:\n  te debo $ 20,00 y "gracias".\n\nChau {llave}']
    # en un renglón es un texto común; el primer renglón pegado a las comillas no se mide
    assert mostrados(f'mostrar({TRES}simple{TRES}, largo({TRES}\n{TRES}))') == ["simple 0"]
    assert mostrados(f'mostrar({TRES}uno\n    dos\n      tres{TRES} + "!")') == [
        "uno\ndos\n  tres!"]
    # con el cierre más a la izquierda, la sangría queda
    assert mostrados(f'sea t = {TRES}\n    a\n      b\n{TRES} + "."\nmostrar(t)') == [
        "    a\n      b."]
    # lo que sigue al cierre está "en el mismo renglón" que el texto
    assert mostrados(f'funcion f() {{\n  devolver {TRES}\n    a\n    {TRES}\n}}\n'
                     f'mostrar(f())\nmostrar(largo({TRES}\n  a\n  b\n  {TRES}), 1)') == [
        "a", "3 1"]
    # un texto común sigue igual, con dos comillas vacías incluidas
    assert mostrados('mostrar("", "a" + "", largo(""))') == [" a 0"]


def test_los_errores_de_un_texto_de_varios_renglones_dicen_el_renglon():
    error = falla(f"mostrar(1)\nsea t = {TRES}hola\nchau\n")
    assert error.linea == 2 and error.mensaje == mate.SIN_CERRAR_TEXTO
    # un nombre que no existe adentro: el renglón es el de esa parte, no el de las comillas
    assert revisar(f'mostrar({TRES}\n    hola\n    {{nombr}}\n    {TRES})') == [
        (3, "no existe 'nombr'")]
    error = falla(f'mostrar({TRES}a\n  {{1 +}}\n{TRES})')
    assert error.linea == 2 and "quedó a medio escribir" in error.mensaje
    # los renglones de después siguen bien numerados
    error = falla(f'sea t = {TRES}\n  a\n  b\n  {TRES}\nmostrar(t)\nmostrar(1 / 0)')
    assert error.linea == 6 and error.mensaje == "división por cero"
    # una comilla que falta en un texto común se sigue explicando igual
    assert "los textos van en un solo renglón" in falla('mostrar("hola').mensaje


def test_la_consola_espera_el_cierre_de_un_texto_de_varios_renglones():
    assert en_consola(f"sea t = {TRES}", "    hola", "", "    chau", f"    {TRES}",
                      "mostrar(largo(t), t)", "salir") == ["10 hola\n\nchau"]


# Mejora 97: contratos que validan valores

REGLAS = """mensaje Pedido {
    producto: texto,
    cantidad: numero desde 1 hasta 100 = 1,
    prioridad: texto en ["baja", "media", "alta"] = "media",
    descuento: numero hasta 0.5 = 0,
    paginas: numero desde 0,
    etiquetas: lista de texto = [],
    nota: texto?
}
"""


def test_un_campo_puede_tener_valor_por_defecto():
    assert mostrados(REGLAS + 'mostrar(Pedido { producto: "yerba", paginas: 0 })') == [
        'Pedido { producto: "yerba", cantidad: 1, prioridad: "media", descuento: 0, '
        "paginas: 0, etiquetas: [], nota: nada }"]
    # darle nada es no dárselo; y lo que llega de afuera también lo toma
    assert mostrados(REGLAS + """
        sea p = Pedido { producto: "a", paginas: 3, cantidad: nada, prioridad: "alta" }
        mostrar(p.cantidad, p.prioridad)
        sea q = de_json(a_json({ producto: "b", paginas: 1 }), "Pedido")
        mostrar(q.cantidad, q.prioridad, q.etiquetas)
    """) == ["1 alta", "1 media []"]
    # el que no tiene valor por defecto sigue siendo obligatorio
    assert revisar(REGLAS + 'sea p = Pedido { producto: "a" }') == [
        (10, "a Pedido le falta el campo 'paginas'")]


def test_las_reglas_de_un_campo_se_controlan_al_armar_el_mensaje():
    def al_armar(campos):
        paginas = "" if "paginas" in campos else "paginas: 1, "
        error = falla(REGLAS + f'sea n = 500\nsea t = "alto"\n'
                               f'sea p = Pedido {{ producto: "a", {paginas}{campos} }}')
        assert not getattr(error, "antes_de_correr", False) and error.linea == 12
        assert error.familia == "contrato"
        return error.mensaje

    assert al_armar("cantidad: n") == (
        "Pedido.cantidad no puede valer 500: el mensaje dice 'desde 1 hasta 100', así que "
        "tiene que estar entre 1 y 100")
    assert al_armar("descuento: n / 100") == (
        "Pedido.descuento no puede valer 5: el mensaje dice 'hasta 0.5', así que tiene que "
        "ser 0.5 o menos")
    assert al_armar("paginas: 1 - n") == (
        "Pedido.paginas no puede valer -499: el mensaje dice 'desde 0', así que tiene que "
        "ser 0 o más")
    assert al_armar("prioridad: t") == (
        'Pedido.prioridad no puede valer "alto": el mensaje dice que tiene que ser una de '
        'estas opciones: "baja", "media", "alta". ¿Quisiste decir "alta"?')
    # también al cambiarle un campo a un mensaje ya armado, y los bordes valen
    assert mostrados(REGLAS + """
        var p = Pedido { producto: "a", paginas: 0, cantidad: 100, descuento: 0.5 }
        p.cantidad = 1
        sea mucho = 101
        intentar { p.cantidad = mucho } si falla e { mostrar(detalle_de(e).clase, p.cantidad) }
    """) == ["contrato 1"]
    # el tipo se sigue controlando antes que la regla
    assert "es de tipo numero" in falla(
        REGLAS + 'sea t = "x"\nsea p = Pedido { producto: "a", paginas: t }').mensaje


def test_las_reglas_se_controlan_antes_de_correr_si_el_valor_esta_escrito_a_mano():
    assert revisar(REGLAS + 'si falso { sea p = Pedido { producto: "a", paginas: -1, '
                            'cantidad: 0, prioridad: "urgente" } }') == [
        (10, "Pedido.cantidad no puede valer 0: el mensaje dice 'desde 1 hasta 100', así que "
             "tiene que estar entre 1 y 100"),
        (10, "Pedido.paginas no puede valer -1: el mensaje dice 'desde 0', así que tiene que "
             "ser 0 o más"),
        (10, 'Pedido.prioridad no puede valer "urgente": el mensaje dice que tiene que ser '
             'una de estas opciones: "baja", "media", "alta".')]
    assert revisar(REGLAS + 'sea p = Pedido { producto: "a", paginas: 0, cantidad: 100 }') == []
    # opciones de números
    fuente = "mensaje Dado { cara: numero en [1, 2, 3, 4, 5, 6] }\n"
    assert mostrados(fuente + "mostrar(Dado { cara: 6 }.cara)") == ["6"]
    assert revisar(fuente + "sea d = Dado { cara: 7 }") == [
        (2, "Dado.cara no puede valer 7: el mensaje dice que tiene que ser una de estas "
            "opciones: 1, 2, 3, 4, 5, 6.")]


@pytest.mark.parametrize("campo,esperado", [
    ("a: texto desde 1", "P.a: 'desde' y 'hasta' solo van en un campo de tipo numero, y este "
                         "es de tipo texto"),
    ("a: numero desde 5 hasta 1", "P.a: 'desde 5' es más que 'hasta 1', así que ningún valor "
                                  "podría cumplirlo"),
    ('a: numero en [1, "x"]', 'P.a es de tipo numero, y entre sus opciones está "x", que es '
                              "un texto"),
    ("a: numero? = 3", "P.a: un campo con valor por defecto ya puede faltar (toma ese "
                       "valor): sacale el '?'"),
    ('a: numero = "x"', 'P.a es de tipo numero, y su valor por defecto es un texto: "x"'),
    ("a: numero desde 1 = 0", "el valor por defecto no cumple su propia regla: P.a no puede "
                              "valer 0: el mensaje dice 'desde 1', así que tiene que ser 1 o "
                              "más"),
    ("a: numero desde x", "P.a: después de 'desde' va un valor escrito a mano (no una cuenta "
                          "ni una variable), por ejemplo: cantidad: numero desde 1 hasta 100"),
    ("a: numero desde", "P.a: después de 'desde' falta el valor, por ejemplo: cantidad: "
                        "numero desde 1 hasta 100"),
    ('a: numero desde "1"', "P.a: después de 'desde' va un número, y hay un texto"),
    ('a: texto en "baja"', "P.a: después de 'en' va la lista de las opciones que valen, por "
                           'ejemplo: prioridad: texto en ["baja", "media", "alta"]'),
    ("a: lista en [1]", "P.a: las opciones con 'en' solo van en un campo de tipo texto o "
                        "numero, y este es de tipo lista"),
    ("a: numero desde 1 en [1]", "P.a: o va un rango ('desde', 'hasta') o va la lista de "
                                 "opciones ('en'), no las dos cosas"),
    ("a: numero = 1 desde 2", "P.a: las reglas van en este orden: primero 'desde', después "
                              "'hasta' (o 'en [...]') y al final '= valor'. Por ejemplo: "
                              "cantidad: numero desde 1 hasta 100 = 1"),
])
def test_una_regla_mal_escrita_se_avisa_en_la_declaracion(campo, esperado):
    error = falla(f"mostrar(1)\nmensaje P {{ {campo} }}")
    assert (error.linea, error.mensaje) == (2, esperado)


def test_un_mensaje_sin_reglas_sigue_igual_y_las_palabras_de_las_reglas_sirven_de_nombre():
    # 'desde' y 'hasta' no son palabras de Mate: valen como campo y como variable
    assert mostrados("""
        mensaje Tramo { desde: numero, hasta: numero? }
        sea desde = 3
        sea t = Tramo { desde: desde }
        mostrar(t.desde, t.hasta)
    """) == ["3 nada"]
    # sin la coma entre dos campos, el error es el de siempre (la regla va en el mismo renglón)
    error = falla("mensaje P {\n  a: numero\n  desde: texto\n}")
    assert error.mensaje == "esperaba '}' y encontré 'desde'"


# Mejoras 98 y 99: el historial de mensajes en las pruebas y el "sobre" de cada entrega

CONVERSACION = """mensaje Encargar { producto: texto }
mensaje Pedido { producto: texto }
mensaje Cotizacion { total: numero }
mensaje Aviso { nota: texto }
mensaje Precio { producto: texto }
agente Vendedor {
    al recibir Pedido como p {
        si p.producto == "sal" { fallar "no vendo sal" }
        responder Cotizacion { total: 100 }
    }
    al recibir Precio como p { responder 50 }
    al recibir Aviso como a { }
}
agente Comprador {
    estado total = 0
    al recibir Encargar como e { enviar Pedido { producto: e.producto } a Vendedor }
    al recibir Cotizacion como c {
        total = c.total + preguntar Precio { producto: "envío" } a Vendedor
    }
}
enviar Aviso { nota: "antes de las pruebas" } a Vendedor
"""


def test_mensajes_enviados_cuenta_quien_le_mando_que_a_quien():
    resultados = probar(CONVERSACION + """
prueba "la conversación completa" {
    enviar Encargar { producto: "yerba" } a Comprador
    enviar Aviso { nota: "hola" } a Vendedor
    sea h = mensajes_enviados()
    asegurar largo(h) == 5
    asegurar h[0] == { numero: 1, de: "(programa)", a: "Comprador", tipo: "Encargar",
                       mensaje: Encargar { producto: "yerba" }, pregunta: falso,
                       conversacion: 1, respuesta_a: nada }
    asegurar h[1].conversacion == 2 y h[1].tipo == "Aviso"
    asegurar h[2].de == "Comprador" y h[2].a == "Vendedor" y h[2].mensaje.producto == "yerba"
    asegurar h[2].conversacion == 1 y h[2].respuesta_a == nada
    asegurar h[3].tipo == "Cotizacion" y h[3].respuesta_a == 3 y h[3].conversacion == 1
    asegurar h[4].pregunta y h[4].numero == 5 y h[4].conversacion == 1
    asegurar largo(mensajes_enviados("Pedido")) == 1
    asegurar mensajes_enviados("Precio")[0].a == "Vendedor"
}
prueba "cada prueba arranca con el historial vacío" {
    asegurar mensajes_enviados() == []
    sea r = preguntar Precio { producto: "a" } a Vendedor
    asegurar mensajes_enviados()[0].numero == 1
    asegurar mensajes_enviados()[0].conversacion == 1
    asegurar mensajes_enviados()[0].de == "(programa)"
}
prueba "también figura el que falló, y un tipo que no existe se avisa" {
    enviar Encargar { producto: "sal" } a Comprador
    asegurar largo(mensajes_enviados("Pedido")) == 1
    asegurar largo(mensajes_enviados("Cotizacion")) == 0
    asegurar falla { mensajes_enviados("Pedid") }
    asegurar falla { mensajes_enviados(3) }
}
""")
    assert resultados["la conversación completa"] is None
    assert resultados["cada prueba arranca con el historial vacío"] is None
    assert resultados["también figura el que falló, y un tipo que no existe se avisa"] == (
        "línea 8: Vendedor al recibir Pedido: no vendo sal")


def test_mensajes_enviados_solo_existe_dentro_de_una_prueba():
    assert revisar(CONVERSACION + "mostrar(mensajes_enviados())") == [(22, mate.SOLO_EN_PRUEBA)]
    assert revisar("mensaje P {}\nagente A {\n al recibir P {\n  responder "
                   "largo(mensajes_enviados())\n }\n}") == [(4, mate.SOLO_EN_PRUEBA)]
    # una función de ayuda la puede usar si la llama una prueba; al correr, no
    fuente = "funcion cuantos() { devolver largo(mensajes_enviados()) }\n"
    assert probar(fuente + 'prueba "nada todavía" { asegurar cuantos() == 0 }') == {
        "nada todavía": None}
    error = falla(fuente + "mostrar(cuantos())")
    assert error.mensaje == mate.SOLO_EN_PRUEBA
    assert "es una función incluida" in falla("sea mensajes_enviados = 1").mensaje
    # con 'correr' no se guarda ningún historial
    _, interprete = correr(CONVERSACION)
    assert interprete.historial == [] and interprete.conversaciones == 1


def test_el_ejemplo_de_mensajes_enviados_del_readme_anda(tmp_path, capsys):
    leeme = (RAIZ / "README.md").read_text(encoding="utf-8")
    bloque = re.findall(r"(?m)^  ```\n(  prueba .*?)^  ```", leeme, re.S)[2]
    assert "mensajes_enviados()" in bloque
    programa = """mensaje Encargar { producto: texto }
mensaje Pedido { producto: texto }
agente Vendedor { al recibir Pedido como p { } }
agente Comprador {
    al recibir Encargar como e { enviar Pedido { producto: e.producto } a Vendedor }
}
"""
    codigo, out, err = por_main(tmp_path, capsys, programa + re.sub(r"(?m)^  ", "", bloque),
                                orden="probar")
    assert (codigo, err) == (0, "") and out.endswith("1 de 1 pruebas pasaron\n")


def test_la_traza_dice_la_conversacion_y_a_que_mensaje_se_responde():
    salida, interprete = correr(CONVERSACION + """
        enviar Encargar { producto: "yerba" } a Comprador
        enviar Aviso { nota: "a los dos" } a [Vendedor, Vendedor]
        mostrar(preguntar Precio { producto: "pan" } a Vendedor)
    """, traza=True)
    assert salida == [
        '  ·  1. (programa) → Vendedor: Aviso { nota: "antes de las pruebas" }   (conversación 1)',
        '  ·  2. (programa) → Comprador: Encargar { producto: "yerba" }   (conversación 2)',
        # un 'enviar' a varios es una sola conversación
        '  ·  3. (programa) → Vendedor: Aviso { nota: "a los dos" }   (conversación 3)',
        '  ·  4. (programa) → Vendedor: Aviso { nota: "a los dos" }   (conversación 3)',
        # lo que manda un agente mientras atiende sigue en la conversación de ese mensaje
        '  ·  5. Comprador → Vendedor: Pedido { producto: "yerba" }   (conversación 2)',
        "  ·  6. Vendedor → Comprador: Cotizacion { total: 100 }   (conversación 2, en "
        "respuesta al 5)",
        # (lo de más adentro no lo repite: es de la conversación del renglón que lo contiene)
        '  ·  7.    Comprador pregunta a Vendedor: Precio { producto: "envío" }',
        "  ·  7.    Vendedor responde a Comprador: 50",
        '  ·  8. (programa) pregunta a Vendedor: Precio { producto: "pan" }   (conversación 4)',
        "  ·  8. Vendedor responde a (programa): 50",
        "50"]
    assert interprete.conversaciones == 4
    # sin traza, el programa muestra lo mismo que antes
    assert correr(CONVERSACION + 'mostrar(preguntar Precio { producto: "pan" } a Vendedor)')[0] \
        == ["50"]


def test_el_aviso_de_al_fallar_sigue_en_la_conversacion_del_mensaje_que_fallo():
    resultados = probar("""mensaje Arrancar {}
mensaje Pedido { producto: texto }
mensaje Queja { motivo: texto }
agente Deposito { al recibir Pedido como p { fallar "no hay {p.producto}" } }
agente Jefe { al recibir Queja como q { } }
agente Vendedor {
    al recibir Arrancar { enviar Pedido { producto: "yerba" } a Deposito }
    al fallar como f { enviar Queja { motivo: f.motivo } a Jefe }
}
prueba "la queja es de la misma conversación" {
    enviar Arrancar {} a Vendedor
    enviar Arrancar {} a Vendedor
    sea quejas = mensajes_enviados("Queja")
    asegurar largo(quejas) == 2
    asegurar quejas[0].conversacion == 1 y quejas[1].conversacion == 2
    asegurar quejas[0].de == "Vendedor" y quejas[0].mensaje.motivo == "no hay yerba"
    asegurar largo(mensajes_enviados()) == 6
}
""")
    assert resultados == {"la queja es de la misma conversación": None}


def test_el_readme_cuenta_lo_de_la_tanda_10():
    leeme = (RAIZ / "README.md").read_text(encoding="utf-8")
    for frase in ["### Valores por defecto en una función", "funcion con_iva(precio, tasa = 0.21)",
                  "con_iva() espera entre 1 y 2 argumento(s) y recibió 3",
                  "Un texto de **varios renglones** va entre tres comillas",
                  "cantidad: numero desde 1 hasta 100",
                  'prioridad: texto en ["baja", "media", "alta"] = "media"',
                  "Pedido.cantidad no puede valer 500", "`mensajes_enviados()` deja comprobar",
                  "| `respuesta_a` |", "**número de conversación**",
                  "(conversación 1, en respuesta al 3)",
                  "`mensajes_enviados` es una función incluida"]:
        assert frase in leeme, frase
    guia = mate.texto_de_guia()
    for frase in ["funcion con_iva(precio, tasa = 0.21)", f"sea carta = {TRES}",
                  "cantidad: numero desde 1 hasta 100", "mensajes_enviados() solo dentro de",
                  "(conversación 2, en respuesta al 4)"]:
        assert frase in guia, frase
    mejoras = (RAIZ / "MEJORAS.md").read_text(encoding="utf-8")
    for numero in (95, 96, 97, 98, 99):
        ficha = mejoras.split(f"\n**{numero}. ")[1].split("\n\n")[0]
        assert "Estado: hecha" in ficha and "Nota al hacerla" in ficha, numero


# ── Mejora 100: los agentes consultan a una IA de verdad (Claude) ──

CLAVE_DE_MENTIRA = "sk-ant-clave-de-mentira-123"

MOSTRADOR = """
mensaje Consulta { pregunta: texto }
mensaje Atencion { respuesta: texto }
agente Mostrador {
    estado reglas = "Atendés un almacén."
    al recibir Consulta como c {
        responder Atencion { respuesta: consultar_ia(reglas, c.pregunta) }
    }
}
"""


class RespuestaDeMentira:
    def __init__(self, cuerpo):
        self.cuerpo = cuerpo

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False

    def read(self):
        import json
        return self.cuerpo if isinstance(self.cuerpo, bytes) else json.dumps(self.cuerpo).encode()


def dice(texto, motivo="end_turn"):
    """Una respuesta de la IA como la manda Anthropic: con un bloque de pensar adelante."""
    return {"id": "msg_1", "type": "message", "role": "assistant", "model": "claude-opus-5-5",
            "content": [{"type": "thinking", "thinking": "", "signature": "x"},
                        {"type": "text", "text": texto}],
            "stop_reason": motivo, "usage": {"input_tokens": 5, "output_tokens": 7}}


def error_http(codigo, tipo="api_error", mensaje="algo", encabezados=None, detalles=None):
    import io
    import json
    import urllib.error
    from email.message import Message
    cabeza = Message()
    for clave, valor in (encabezados or {}).items():
        cabeza[clave] = valor
    error = {"type": tipo, "message": mensaje}
    if detalles:
        error["details"] = detalles
    cuerpo = json.dumps({"type": "error", "error": error, "request_id": "req_1"}).encode()
    return urllib.error.HTTPError(mate.IA_DIRECCION, codigo, "error", cabeza, io.BytesIO(cuerpo))


@pytest.fixture
def ia(monkeypatch):
    """Una IA de mentira en lugar de la red: anota cada pedido y contesta lo que se le
    prepare (una respuesta, o una excepción para que falle)."""
    import json
    import urllib.request

    class IA:
        pedidos, esperas = [], []
        respuestas = []  # lo que va a contestar, en orden; la última se repite

        def abrir(self, pedido, timeout=None):
            self.pedidos.append({
                "url": pedido.full_url, "metodo": pedido.get_method(), "espera": timeout,
                "encabezados": {k.lower(): v for k, v in pedido.header_items()},
                "cuerpo": json.loads(pedido.data.decode("utf-8"))})
            r = self.respuestas.pop(0) if len(self.respuestas) > 1 else self.respuestas[0]
            if isinstance(r, BaseException):
                raise r
            return RespuestaDeMentira(r)

    falsa = IA()
    falsa.pedidos, falsa.esperas, falsa.respuestas = [], [], [dice("Sí, hay yerba.")]
    monkeypatch.setattr(urllib.request, "urlopen", falsa.abrir)
    monkeypatch.setattr("time.sleep", falsa.esperas.append)
    monkeypatch.setenv("ANTHROPIC_API_KEY", CLAVE_DE_MENTIRA)
    return falsa


def test_consultar_ia_arma_el_pedido_como_lo_espera_anthropic(ia):
    salida, _ = correr(MOSTRADOR + """
        sea a = preguntar Consulta { pregunta: "¿Hay yerba?" } a Mostrador
        mostrar(a.respuesta)
    """)
    assert salida == ["Sí, hay yerba."]  # solo el texto: lo que la IA pensó no se mezcla
    (pedido,) = ia.pedidos
    assert pedido["url"] == "https://api.anthropic.com/v1/messages"
    assert pedido["metodo"] == "POST" and pedido["espera"] == mate.IA_ESPERA
    assert pedido["encabezados"]["x-api-key"] == CLAVE_DE_MENTIRA
    assert pedido["encabezados"]["anthropic-version"] == "2026-10-21"
    assert pedido["encabezados"]["content-type"] == "application/json"
    assert pedido["encabezados"]["anthropic-beta"] == "server-side-fallback-2026-07-01"
    assert pedido["cuerpo"] == {
        "model": "claude-opus-5-5", "max_tokens": 16000, "system": "Atendés un almacén.",
        "messages": [{"role": "user", "content": "¿Hay yerba?"}], "fallbacks": "default"}


def test_el_modelo_se_cambia_con_mate_modelo(ia, monkeypatch):
    monkeypatch.setenv("MATE_MODELO", " claude-haiku-5-5 ")
    assert correr('mostrar(consultar_ia("", "Hola"))')[0] == ["Sí, hay yerba."]
    cuerpo = ia.pedidos[0]["cuerpo"]
    assert cuerpo["model"] == "claude-haiku-5-5"
    # sin instrucciones no se manda 'system', y ese modelo no acepta el respaldo
    assert "system" not in cuerpo and "fallbacks" not in cuerpo
    assert "anthropic-beta" not in ia.pedidos[0]["encabezados"]
    monkeypatch.setenv("MATE_MODELO", "un modelo\ncon salto")
    error = falla('mostrar(consultar_ia("", "Hola"))')
    assert "MATE_MODELO" in error.mensaje and len(ia.pedidos) == 1


def test_sin_clave_explica_como_ponerla_en_powershell():
    error = falla('mostrar(consultar_ia("Sos amable", "Hola"))')
    renglones = error.mensaje.split("\n")
    assert len(renglones) == 2 and error.familia == "ia"
    assert '$env:ANTHROPIC_API_KEY = "tu-clave"' in renglones[0]
    assert "pago" in renglones[1] and "--ia-simulada" in renglones[1]


def test_una_clave_con_letras_raras_se_avisa_sin_mostrarla(ia, monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant secreto\ncon salto")
    error = falla('mostrar(consultar_ia("", "Hola"))')
    assert "letras raras" in error.mensaje and "secreto" not in error.mensaje
    assert ia.pedidos == []
    monkeypatch.setenv("ANTHROPIC_API_KEY", f'  "{CLAVE_DE_MENTIRA}"  ')  # con comillas de más
    assert correr('mostrar(consultar_ia("", "Hola"))')[0] == ["Sí, hay yerba."]
    assert ia.pedidos[0]["encabezados"]["x-api-key"] == CLAVE_DE_MENTIRA


@pytest.mark.parametrize("respuesta, frase", [
    (error_http(401, "authentication_error", "invalid x-api-key"), "la clave no sirve"),
    (error_http(402, "billing_error", "billing"), "no tiene crédito"),
    (error_http(400, "invalid_request_error", "Your credit balance is too low"),
     "no tiene crédito"),
    (error_http(403, "permission_error", "no"), "no tiene permiso"),
    (error_http(404, "not_found_error", "model: claude-opus-5-5"), "no conoce el modelo"),
    (error_http(413, "request_too_large", "big"), "demasiado larga"),
    (error_http(400, "invalid_request_error", "max_tokens: too big"),
     "no aceptó la consulta (Anthropic dijo: max_tokens: too big)"),
    (error_http(429, "rate_limit_error", "spend", detalles={
        "error_code": "enforced_spend_limit_reached"}), "tope de gasto del mes"),
    (error_http(418, "raro", "tetera"), "código 418"),
    (dice("", "refusal"), "no quiso contestar"),
    (dice("Había una vez", "max_tokens"), "llegó cortada"),
    (dice("   "), "contestó sin texto"),
    (b"<html>esto no es JSON</html>", "no pude entender"),
    ({"type": "message"}, "no pude entender"),
    (TimeoutError("timed out"), "tardó más de 3 minutos"),
])
def test_los_errores_de_la_ia_salen_en_castellano_y_sin_reintentar(ia, respuesta, frase):
    ia.respuestas = [respuesta]
    error = falla('mostrar(consultar_ia("", "Hola"))')
    assert error.mensaje.startswith("consultar_ia(): ") and frase in error.mensaje
    assert error.familia == "ia" and error.clase == "falla"
    assert CLAVE_DE_MENTIRA not in error.mensaje
    assert len(ia.pedidos) == 1 and ia.esperas == []


def test_si_la_ia_esta_saturada_se_prueba_de_nuevo(ia):
    import urllib.error
    ia.respuestas = [error_http(529, "overloaded_error", "Overloaded"),
                     urllib.error.URLError(OSError("se cortó")), dice("Ahora sí.")]
    assert correr('mostrar(consultar_ia("", "Hola"))')[0] == ["Ahora sí."]
    assert len(ia.pedidos) == 3 and ia.esperas == [2, 5]
    # el límite de uso dice cuánto esperar; si es mucho, no se queda colgado
    ia.pedidos.clear(), ia.esperas.clear()
    ia.respuestas = [error_http(429, "rate_limit_error", "x", {"retry-after": "7"}),
                     error_http(429, "rate_limit_error", "x", {"retry-after": "600"})]
    error = falla('mostrar(consultar_ia("", "Hola"))')
    assert "límite de uso" in error.mensaje and ia.esperas == [7] and len(ia.pedidos) == 2


@pytest.mark.parametrize("respuesta, frase", [
    (error_http(529, "overloaded_error", "Overloaded"), "saturada"),
    (error_http(500, "api_error", "Internal"), "tuvo un problema"),
    (ConnectionResetError("reset"), "se cortó la conexión"),
])
def test_despues_de_dos_reintentos_avisa(ia, respuesta, frase):
    ia.respuestas = [respuesta]
    assert frase in falla('mostrar(consultar_ia("", "Hola"))').mensaje
    assert len(ia.pedidos) == 3 and ia.esperas == [2, 5]


def test_sin_internet_y_con_el_certificado_roto(ia):
    import ssl
    import urllib.error
    ia.respuestas = [urllib.error.URLError(OSError("getaddrinfo failed"))]
    assert "revisá que haya internet" in falla('mostrar(consultar_ia("", "Hola"))').mensaje
    ia.pedidos.clear()
    ia.respuestas = [urllib.error.URLError(ssl.SSLCertVerificationError("self-signed"))]
    assert "certificado" in falla('mostrar(consultar_ia("", "Hola"))').mensaje
    assert len(ia.pedidos) == 1
    ia.respuestas = [urllib.error.URLError(TimeoutError("timed out"))]
    assert "tardó más de 3 minutos" in falla('mostrar(consultar_ia("", "Hola"))').mensaje


def test_la_clave_nunca_aparece_ni_en_errores_ni_en_la_traza(ia, tmp_path, capsys, monkeypatch):
    # aunque Anthropic la repita en su error, o falle algo que Mate no esperaba
    ia.respuestas = [error_http(400, "invalid_request_error", f"bad key {CLAVE_DE_MENTIRA}")]
    assert CLAVE_DE_MENTIRA not in falla('mostrar(consultar_ia("", "Hola"))').mensaje
    programa = tmp_path / "ia.mate"
    programa.write_text('mostrar(consultar_ia("Sos amable", "Hola"))\n', encoding="utf-8")
    for respuesta in (error_http(401, "authentication_error", f"key {CLAVE_DE_MENTIRA}"),
                      RuntimeError(f"algo rarísimo con {CLAVE_DE_MENTIRA}")):
        ia.respuestas = [respuesta]
        assert mate.main(["correr", str(programa), "--traza"]) == 1
        capturado = capsys.readouterr()
        todo = capturado.out + capturado.err
        assert CLAVE_DE_MENTIRA not in todo and "Traceback" not in todo
        assert "error interno" not in todo and "ia.mate:1: error: consultar_ia():" in todo
    assert "la IA no contestó: consultar_ia(): la clave no sirve" in mate_traza(
        'intentar { mostrar(consultar_ia("", "Hola")) } si falla { mostrar("sin IA") }', ia,
        error_http(401))
    assert CLAVE_DE_MENTIRA not in mate.texto_de_guia() + mate.texto_de_ayuda()


def mate_traza(fuente, ia, respuesta):
    ia.respuestas = [respuesta]
    return "\n".join(correr(fuente, traza=True)[0])


def test_los_errores_de_la_ia_se_atajan_con_intentar(ia):
    ia.respuestas = [error_http(401, "authentication_error", "invalid x-api-key")]
    salida, _ = correr("""
        intentar {
            mostrar(consultar_ia("", "Hola"))
        } si falla e {
            mostrar(detalle_de(e).clase, tiene(e, "la clave no sirve"))
        }
    """)
    assert salida == ["ia verdadero"]


def test_si_la_cuenta_no_acepta_el_respaldo_se_sigue_sin_el(ia):
    ia.respuestas = [error_http(400, "invalid_request_error",
                                "Unexpected value(s) `server-side-fallback-2026-07-01` for "
                                "the `anthropic-beta` header."), dice("Hola.")]
    salida, _ = correr('mostrar(consultar_ia("", "Uno"))\nmostrar(consultar_ia("", "Dos"))')
    assert salida == ["Hola.", "Hola."] and ia.esperas == []
    assert ["fallbacks" in p["cuerpo"] for p in ia.pedidos] == [True, False, False]
    assert ["anthropic-beta" in p["encabezados"] for p in ia.pedidos] == [True, False, False]


def test_los_valores_de_consultar_ia_se_controlan(ia):
    assert "espera texto y recibió" in falla('mostrar(consultar_ia("", 5))').mensaje
    assert "espera texto y recibió" in falla('mostrar(consultar_ia(5, "Hola"))').mensaje
    assert "tercer valor" in falla('mostrar(consultar_ia("", "Hola", 3))').mensaje
    assert "está vacía" in falla('mostrar(consultar_ia("", "  "))').mensaje
    assert "devuelve un valor" in falla('consultar_ia("", "Hola")').mensaje
    assert falla('mostrar(consultar_ia("Hola"))').antes_de_correr
    assert "función incluida" in falla("sea consultar_ia = 1").mensaje
    assert ia.pedidos == []


def test_un_freno_para_que_la_cuenta_no_crezca_sola(ia, monkeypatch):
    monkeypatch.setattr(mate, "MAX_CONSULTAS_IA", 3)
    fuente = 'para i en rango(5) { intentar { sea r = consultar_ia("", "Hola") } si falla { } }'
    error = falla(fuente)
    assert "ya le hizo 3 consultas a la IA" in error.mensaje and error.clase == "limite"
    assert "--sin-limite" in error.mensaje and len(ia.pedidos) == 3
    interprete = mate.Interprete(salida=lambda _: None)
    interprete.max_pasos = None  # --sin-limite
    interprete.correr(mate.analizar(fuente))
    assert len(ia.pedidos) == 8


def probar_mate(fuente, **cambios):
    """Corre las pruebas de ese programa como 'probar'. Devuelve {nombre: error o None}."""
    salida = []
    interprete = mate.Interprete(salida=salida.append)
    for nombre, valor in cambios.items():
        setattr(interprete, nombre, valor)
    programa = mate.analizar(fuente)
    assert mate.verificar(programa) == []
    return dict(interprete.correr(programa, pruebas=True)), salida


def test_en_las_pruebas_nunca_se_sale_a_la_red(ia):
    resultados, salida = probar_mate(MOSTRADOR + """
        mostrar(consultar_ia("", "¿Hola?", "preparada"))
        prueba "fijada por la prueba" {
            simular_ia("Sale $ 100")
            sea a = preguntar Consulta { pregunta: "¿Cuánto sale?" } a Mostrador
            asegurar a.respuesta == "Sale $ 100"
            asegurar consultar_ia("", "otra", "preparada") == "Sale $ 100"
            simular_ia("Ahora otra cosa")
            asegurar consultar_ia("", "otra") == "Ahora otra cosa"
        }
        prueba "en orden" {
            simular_ia(["Uno", "Dos"])
            asegurar consultar_ia("", "a") == "Uno"
            asegurar consultar_ia("", "b") == "Dos"
            asegurar falla { mostrar(consultar_ia("", "c")) }
        }
        prueba "cada prueba arranca sin nada fijado" {
            asegurar consultar_ia("", "a", "la preparada") == "la preparada"
            sea a = preguntar Consulta { pregunta: "¿Hola?" } a Mostrador
        }
    """)
    assert salida == ["preparada"] and ia.pedidos == []  # ni con la clave puesta
    assert resultados["fijada por la prueba"] is None and resultados["en orden"] is None
    sin_simular = resultados["cada prueba arranca sin nada fijado"]
    assert "no sale a la red y no hay una respuesta simulada" in sin_simular
    assert 'simular_ia("lo que contesta")' in sin_simular and "tercer valor" in sin_simular
    resultados, _ = probar_mate("""
        prueba "se acaban" {
            simular_ia(["Uno"])
            sea a = consultar_ia("", "a")
            sea b = consultar_ia("", "b")
        }
    """)
    assert "le hizo 2 consultas a la IA y simular_ia() tenía 1" in resultados["se acaban"]


def test_simular_ia_solo_va_en_una_prueba():
    assert mate.verificar(mate.analizar('simular_ia("Hola")')) == [(1, mate.SIMULAR_IA_SUELTO)]
    assert mate.verificar(mate.analizar(
        'mensaje M {}\nagente A {\n al recibir M {\n  simular_ia("x")\n }\n}')) == [
            (4, mate.SIMULAR_IA_SUELTO)]
    assert "--ia-simulada" in mate.SIMULAR_IA_SUELTO
    # una función suelta la puede usar si la llama una prueba; si no, falla al correr
    fuente = 'funcion preparar() { simular_ia("Hola") }\n'
    resultados, _ = probar_mate(
        fuente + 'prueba "p" { preparar()\n asegurar consultar_ia("", "a") == "Hola" }')
    assert resultados == {"p": None}
    assert falla(fuente + "preparar()").mensaje == mate.SIMULAR_IA_SUELTO
    for mal in ('""', "[]", '["a", 3]', "5"):
        resultados, _ = probar_mate(f'prueba "p" {{ simular_ia({mal}) }}')
        assert "simular_ia() espera el texto" in resultados["p"], mal


def test_ia_simulada_al_correr_y_con_un_archivo_de_respuestas(ia, tmp_path, capsys):
    programa = tmp_path / "tienda.mate"
    programa.write_text(MOSTRADOR + """
        funcion atender(duda) {
            sea a = preguntar Consulta { pregunta: duda } a Mostrador
            mostrar(a.respuesta)
        }
        mostrar(consultar_ia("", "¿Están?", "Sí, estamos."))
        atender("¿Tienen YERBA sin palo?")
        atender("¿Cuál es el horário?")
        atender("¿Hay pan?")
    """, encoding="utf-8")
    respuestas = tmp_path / "respuestas.txt"
    respuestas.write_bytes("﻿# respuestas de mentira\r\n\r\nyerba => Sí, de medio kilo.\r\n"
                           "Horario  =>  De 8 a 20.\\nLos domingos no.\r\n"
                           "* => Eso te lo averiguo.\r\n".encode("utf-8"))
    assert mate.main(["correr", str(programa), f"--ia-simulada={respuestas}", "--traza"]) == 0
    capturado = capsys.readouterr()
    assert [r for r in capturado.out.splitlines() if not r.startswith("  ·")] == [
        "Eso te lo averiguo.", "Sí, de medio kilo.", "De 8 a 20.", "Los domingos no.",
        "Eso te lo averiguo."]
    assert '       Mostrador consulta a la IA (simulada): "¿Tienen YERBA sin palo?"' \
        in capturado.out
    assert '       la IA contesta: "De 8 a 20. Los domingos no."' in capturado.out
    assert '(programa) consulta a la IA (simulada): "¿Están?"' in capturado.out
    assert capturado.err == "" and ia.pedidos == []
    # sin el renglón del *, lo que no está en el archivo usa la respuesta preparada o avisa
    respuestas.write_text("yerba => Sí.\n", encoding="utf-8")
    assert mate.main(["correr", str(programa), f"--ia-simulada={respuestas}"]) == 1
    capturado = capsys.readouterr()
    assert capturado.out.splitlines()[:2] == ["Sí, estamos.", "Sí."]
    assert "no tiene ninguna para esta consulta" in capturado.err
    assert '"¿Cuál es el horário?"' in capturado.err and "* => lo que contesta" in capturado.err
    # --ia-simulada sola: cada consulta da su respuesta preparada
    assert mate.main(["correr", str(programa), "--ia-simulada"]) == 1
    capturado = capsys.readouterr()
    assert capturado.out == "Sí, estamos.\n" and "tercer valor" in capturado.err
    assert ia.pedidos == []
    # y sin la opción, con la clave puesta, va a la IA
    assert mate.main(["correr", str(programa)]) == 0
    assert capsys.readouterr().out == "Sí, hay yerba.\n" * 4 and len(ia.pedidos) == 4


def test_un_archivo_de_respuestas_mal_escrito_se_avisa(tmp_path, capsys):
    programa = tmp_path / "p.mate"
    programa.write_text('mostrar("no llega a correr")\n', encoding="utf-8")
    respuestas = tmp_path / "respuestas.txt"
    for contenido, frase in [("yerba => Sí.\nesto no tiene flecha\n", "respuestas.txt:2: no entiendo"),
                             ("=> Sí.\n", "respuestas.txt:1: no entiendo"),
                             ("# nada\n", "está vacío")]:
        respuestas.write_text(contenido, encoding="utf-8")
        assert mate.main(["correr", str(programa), f"--ia-simulada={respuestas}"]) == 2
        capturado = capsys.readouterr()
        assert frase in capturado.err and capturado.out == "", contenido
    assert mate.main(["correr", str(programa), f"--ia-simulada={tmp_path / 'no_esta.txt'}"]) == 2
    assert "no encuentro el archivo de respuestas" in capsys.readouterr().err
    assert mate.main(["correr", str(programa), f"--ia-simulada={tmp_path}"]) == 2
    assert "no pude leer el archivo de respuestas" in capsys.readouterr().err
    assert mate.main(["correr", str(programa), "--ia-simulada="]) == 2
    assert "le falta el nombre del archivo" in capsys.readouterr().err
    assert mate.main(["correr", str(programa), "--ia-simulado"]) == 2
    assert "¿quisiste decir --ia-simulada?" in capsys.readouterr().err


def test_el_ejemplo_del_agente_con_ia(ia, capsys, monkeypatch):
    ruta = str(RAIZ / "ejemplos" / "07_agente_con_ia.mate")
    assert mate.main(["probar", ruta]) == 0
    assert "3 de 3 pruebas pasaron" in capsys.readouterr().out and ia.pedidos == []
    assert mate.main(["correr", ruta, "--ia-simulada"]) == 0
    assert capsys.readouterr().out == ("Pregunta de Marta: ¿Tienen yerba sin palo?\n"
                                       "Mostrador: ¡Hola! Ya te lo averiguo.\n")
    assert ia.pedidos == []
    # de verdad (acá, contra la IA de mentira): la respuesta preparada no se usa
    ia.respuestas = [dice("Sí, tenemos de medio kilo.")]
    assert mate.main(["correr", ruta]) == 0
    assert capsys.readouterr().out.splitlines()[1] == "Mostrador: Sí, tenemos de medio kilo."
    assert "almacén de barrio" in ia.pedidos[0]["cuerpo"]["system"]
    assert ia.pedidos[0]["cuerpo"]["messages"] == [
        {"role": "user", "content": "¿Tienen yerba sin palo?"}]
    # sin clave el agente no se cae, y el programa muestra cómo ponerla
    monkeypatch.delenv("ANTHROPIC_API_KEY")
    assert mate.main(["correr", ruta]) == 0
    capturado = capsys.readouterr()
    assert "Ahora no te puedo atender" in capturado.out and capturado.err == ""
    assert '$env:ANTHROPIC_API_KEY = "tu-clave"' in capturado.out
    # la clave no está escrita en ningún archivo de Mate
    for archivo in RAIZ.rglob("*"):
        if archivo.is_file() and archivo.suffix in (".mate", ".md", ".bat", ".txt"):
            assert "sk-ant" not in archivo.read_text(encoding="utf-8"), archivo


def test_el_readme_y_la_ayuda_cuentan_lo_de_la_tanda_11():
    leeme = (RAIZ / "README.md").read_text(encoding="utf-8")
    for frase in ["### Un agente que consulta a una IA de verdad",
                  '$env:ANTHROPIC_API_KEY = "tu-clave"', "es **pago**", "platform.claude.com",
                  "| `--ia-simulada` |", "--ia-simulada=respuestas.txt", "`07_agente_con_ia.mate`",
                  '$env:MATE_MODELO = "claude-haiku-5-5"', f"`{mate.IA_MODELO}`",
                  "**La clave nunca va en el programa**", "no contra el servicio real",
                  '`"ia"`', "`consultar_ia` y `simular_ia` son funciones incluidas"]:
        assert frase in leeme, frase
    guia = mate.texto_de_guia()
    for frase in ["consultar_ia(instrucciones, pregunta)", "ANTHROPIC_API_KEY", '"ia"',
                  'simular_ia("Sale $ 100") solo dentro de una prueba', "--ia-simulada"]:
        assert frase in guia, frase
    assert "--ia-simulada" in mate.texto_de_ayuda()
    assert "función incluida" in mate.ayuda_de("consultar_ia")
    mejoras = (RAIZ / "MEJORAS.md").read_text(encoding="utf-8")
    ficha = mejoras.split("\n**100. ")[1].split("\n\n")[0]
    assert "Estado: hecha" in ficha and "Nota al hacerla (tanda 11)" in ficha
    assert "no se probó contra el servicio real" in ficha
    assert "Estado: pendiente*" not in mejoras


# ───────────── Correcciones de la tercera revisión ─────────────

COMPRA = """
mensaje Encargar { producto: texto }
mensaje Pedido { producto: texto }
mensaje Ok { n: numero }
agente Vendedor {
    al recibir Pedido como p { responder Ok { n: 1 } }
}
agente Comprador {
    estado oks = 0
    al recibir Encargar como e { enviar Pedido { producto: e.producto } a Vendedor }
    al recibir Ok como k { oks += 1 }
}
enviar Encargar { producto: "antes" } a Comprador
prueba "uno" {
    enviar Encargar { producto: "yerba" } a Comprador
    asegurar largo(mensajes_enviados()) == 3
}
prueba "dos" {
    enviar Encargar { producto: "azucar" } a Comprador
    sea ok = mensajes_enviados("Ok")[0]
    mostrar("{ok.numero} c{ok.conversacion} r{ok.respuesta_a}")
}
"""


def test_la_traza_de_una_prueba_numera_igual_que_mensajes_enviados(tmp_path, capsys):
    ruta = tmp_path / "compra.mate"
    ruta.write_text(COMPRA, encoding="utf-8")
    assert mate.main(["probar", str(ruta), "--traza"]) == 0
    out = capsys.readouterr().out
    # antes de las pruebas, la numeración de siempre
    assert '·  3. Vendedor → Comprador: Ok { n: 1 }   (conversación 1, en respuesta al 2)' in out
    dos = out.split("✓ dos")[1]
    assert '|   ·  1. (programa) → Comprador: Encargar { producto: "azucar" }   (conversación 1)' in dos
    assert "|   ·  3. Vendedor → Comprador: Ok { n: 1 }   (conversación 1, en respuesta al 2)" in dos
    assert "| 3 c1 r2" in dos  # lo mismo que dice mensajes_enviados()
    assert "conversación 2" not in out and "conversación 3" not in out and " 4. " not in out
    # en el archivo, cada prueba va con su título y numera desde 1
    destino = tmp_path / "conv.txt"
    assert mate.main(["probar", str(ruta), f"--traza={destino}"]) == 0
    capsys.readouterr()
    texto = destino.read_text(encoding="utf-8-sig")
    antes, uno, dos = texto.split('\nPrueba "')
    assert '·  1. (programa) → Comprador: Encargar { producto: "antes" }' in antes
    assert uno.startswith('uno" (los números arrancan de nuevo')
    assert dos.startswith('dos" (los números arrancan de nuevo')
    assert "·  3. Vendedor → Comprador: Ok { n: 1 }   (conversación 1, en respuesta al 2)" in dos
    assert " 4. " not in texto and "Resumen: 9 mensaje(s)" in texto
    # con 'correr' nada cambió
    salida, _ = correr(COMPRA + 'enviar Encargar { producto: "pan" } a Comprador', traza=True)
    assert salida[-1] == "  ·  6. Vendedor → Comprador: Ok { n: 1 }   (conversación 2, en respuesta al 4)"


def test_la_consola_respeta_ia_simulada(capsys, monkeypatch, tmp_path):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-NO-SE-TIENE-QUE-USAR")  # (urlopen falla)
    renglones = iter(['consultar_ia("sos amable", "hola", "preparada")', "salir"])
    monkeypatch.setattr("builtins.input", lambda _="": next(renglones))
    assert mate.main(["consola", "--ia-simulada"]) == 0
    assert capsys.readouterr().out.splitlines()[2:] == ['"preparada"']
    respuestas = tmp_path / "respuestas.txt"
    respuestas.write_text("yerba => Sale $ 3.500\n* => No sé\n", encoding="utf-8")
    renglones = iter(['mostrar(consultar_ia("", "¿y la yerba?"))', "salir"])
    assert mate.main(["consola", f"--ia-simulada={respuestas}"]) == 0
    assert capsys.readouterr().out.splitlines()[2:] == ["Sale $ 3.500"]
    assert mate.main(["consola", f"--ia-simulada={tmp_path / 'no_esta.txt'}"]) == 2
    assert capsys.readouterr().err.strip()
    # sin la opción, la consola sigue yendo a la IA de verdad (acá: la red de mentira falla)
    salida = []
    lineas = iter(['consultar_ia("", "hola", "preparada")'])

    def entrada(_=""):
        try:
            return next(lineas)
        except StopIteration:
            raise EOFError

    mate.consola(entrada, salida.append)
    assert "preparada" not in "\n".join(salida) and "error: consultar_ia()" in "\n".join(salida)


def test_se_puede_probar_que_un_contrato_rechaza_un_valor_escrito_a_mano():
    mensaje = "mensaje A { x: numero desde 1 hasta 10, color: texto en [\"rojo\", \"azul\"] = \"rojo\" }\n"
    programa = mate.analizar(mensaje + """
        prueba "rango" {
            asegurar falla { A { x: 11 } }
            asegurar falla { A { x: 1, color: "verde" } }
        }
        intentar { mostrar(A { x: 11 }) } si falla e { mostrar("atajado: {e}") }
    """)
    assert mate.verificar(programa) == []
    salida = []
    interprete = mate.Interprete(salida=salida.append)
    assert interprete.correr(programa, pruebas=True) == [("rango", None)]
    assert salida == ["atajado: A.x no puede valer 11: el mensaje dice 'desde 1 hasta 10', "
                      "así que tiene que estar entre 1 y 10"]
    # afuera se sigue avisando antes de correr, y en el 'si falla' también
    assert falla(mensaje + "mostrar(A { x: 11 })").antes_de_correr
    assert falla(mensaje + "intentar { fallar \"x\" } si falla e { mostrar(A { x: 11 }) }"
                 ).antes_de_correr
    # y adentro del 'intentar' lo demás (un tipo equivocado, un campo que falta) no cambió
    assert "es de tipo numero" in falla(
        mensaje + 'intentar { mostrar(A { x: "once" }) } si falla e { }').mensaje


def test_el_error_de_una_regla_no_se_contradice_con_los_decimales():
    salida, _ = correr("""
        mensaje A { y: numero desde 0.1 hasta 0.3 }
        mensaje P { precio: numero en [1.1, 2.2, 3.3] }
        intentar { mostrar(A { y: 0.1 + 0.2 }) } si falla e { mostrar(e) }
        intentar { mostrar(P { precio: 1.1 * 3 }) } si falla e { mostrar(e) }
        mostrar(A { y: redondear(0.1 + 0.2, 2) }, P { precio: redondear(1.1 * 3, 2) })
        intentar { mostrar(A { y: 0.5 }) } si falla e { mostrar(e) }
    """)
    assert salida[0].startswith("A.y no puede valer 0.30000000000000004: el mensaje dice "
                                "'desde 0.1 hasta 0.3'")
    assert "Se muestra 0.3, pero las cuentas con decimales dejan un resto" in salida[0]
    assert "redondear(valor, 2)" in salida[0]
    assert salida[1].startswith("P.precio no puede valer 3.3000000000000003: ")
    assert "opciones: 1.1, 2.2, 3.3. Se muestra 3.3, pero" in salida[1]
    assert salida[2] == "A { y: 0.3 } P { precio: 3.3 }"
    # un valor que de verdad está afuera se dice como siempre
    assert salida[3] == ("A.y no puede valer 0.5: el mensaje dice 'desde 0.1 hasta 0.3', "
                         "así que tiene que estar entre 0.1 y 0.3")


def test_tres_comillas_con_una_comilla_pegada_al_cierre():
    assert correr('sea t = \"\"\"\n    Ella dijo "hola\"\"\"\"\nmostrar(t)')[0] == ['Ella dijo "hola"']
    assert correr('mostrar(\"\"\"dijo "si" y "no\"\"\"\")')[0] == ['dijo "si" y "no"']
    assert correr('mostrar(largo(\"\"\"\"\"\"), \"\"\"a\"\"\" + "b")')[0] == ["0 ab"]
    # el renglón que termina en \""" se señala a él, no a unas comillas de más abajo
    error = falla('sea t = \"\"\"\n    dijo hola\\\"\"\"\nmostrar(t)\nsea u = \"\"\" x \"\"\"\n')
    assert error.linea == 2 and 'termina en \\"""' in error.mensaje
    assert "en el renglón de abajo" in error.mensaje
    error = falla('sea t = \"\"\"\n  hola\\\"\"\"\n')
    assert error.linea == 2 and "quedan dos en vez de tres" in error.mensaje
    # un texto sin cerrar de los de siempre da el error de siempre
    assert falla('sea t = \"\"\"\n  hola\n').mensaje == mate.SIN_CERRAR_TEXTO


def test_la_clave_no_aparece_ni_partida_ni_en_mayusculas(ia):
    clave = CLAVE_DE_MENTIRA
    programa = ('intentar { mostrar(consultar_ia("sos amable", "hola")) } '
                "si falla e { mostrar(e) }")
    # el servidor devuelve la clave justo donde se recorta su mensaje
    ia.respuestas = [error_http(400, "invalid_request_error", "x" * 280 + " " + clave)]
    salida, _ = correr(programa, traza=True)
    # otro la devuelve por la mitad, y en mayúsculas
    ia.respuestas = [error_http(403, "permission_error",
                                f"key {clave[:12]} ; full {clave.upper()} ; fin")]
    salida += correr(programa, traza=True)[0]
    todo = "\n".join(salida)
    assert "Anthropic dijo" in todo and "(la clave)" in todo and "; fin" in todo
    for largo in range(8, len(clave) + 1):
        assert clave[:largo].lower() not in todo.lower(), largo
    assert clave[-10:].lower() not in todo.lower()
    # y lo que no es la clave queda tal cual
    assert mate.tapar_clave("el modelo no existe", clave) == "el modelo no existe"
    assert mate.tapar_clave(f"a {clave[3:20]} b", clave) == "a (la clave) b"
    assert mate.tapar_clave("abc", "") == "abc" and mate.tapar_clave("xabcx", "abc") == "x(la clave)x"
