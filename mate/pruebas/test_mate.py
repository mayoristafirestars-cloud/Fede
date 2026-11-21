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
    # ...ni anota en el registro de errores de uso de verdad (tampoco las que corren mate.py
    # como programa aparte: heredan esta variable)
    monkeypatch.setenv("MATE_SIN_REGISTRO", "1")


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
    # (se rompe algo que usa 'sea' por dentro, cuando ya se sabe por qué renglón va)
    def roto(self, nombre):
        raise RuntimeError("algo se rompió adentro")
    monkeypatch.setattr(mate.Entorno, "no_tapar", roto)
    codigo, _, err = por_main(tmp_path, capsys, "sea a = 1\nmostrar(a)")
    assert codigo == 1
    assert "error interno de Mate (no es culpa tuya): RuntimeError: algo se rompió adentro" in err
    assert "programa.mate:1" in err and "--depurar" in err and "Traceback" not in err
    with pytest.raises(RuntimeError):
        por_main(tmp_path, capsys, "sea b = 1", "--depurar")


def test_ctrl_c_dice_en_que_linea_estaba(tmp_path, capsys, monkeypatch):
    def cortar(self, nombre):
        raise KeyboardInterrupt
    monkeypatch.setattr(mate.Entorno, "no_tapar", cortar)
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
    assert falla('pesos("hola")').mensaje.startswith(
        'pesos() espera numero y recibió texto ("hola"). Si viene de una planilla')
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

GRADUALES = sorted(p.name for p in (RAIZ / "ejemplos").glob("[0-9][0-9]_*.mate"))


def test_estan_los_seis_ejemplos_graduales():  # (y el 7.º, la IA; el 8.º, aprende; el 9.º, Python...)
    assert [n[:2] for n in GRADUALES] == ["01", "02", "03", "04", "05", "06", "07", "08", "09",
                                          "10", "11"]
    assert GRADUALES[0] == "01_hola.mate" and GRADUALES[-3] == "09_con_python.mate"
    assert GRADUALES[-4] == "08_agente_que_aprende.mate"
    assert GRADUALES[-2] == "10_mostrador_mayorista.mate"
    assert GRADUALES[-1] == "11_mostrador_con_frenos.mate"
    for nombre in GRADUALES:  # están comentados: al menos un comentario cada cuatro renglones
        renglones = [r.strip() for r in (RAIZ / "ejemplos" / nombre).read_text(
            encoding="utf-8").splitlines() if r.strip()]
        assert 4 * sum(r.startswith("#") for r in renglones) >= len(renglones), nombre


@pytest.mark.parametrize("nombre", GRADUALES)
def test_los_ejemplos_graduales_corren_y_pasan_sus_pruebas(nombre, capsys, tmp_path):
    # (en una copia: el ejemplo 8 guarda su memoria al lado, y las pruebas no ensucian)
    import shutil
    ruta = str(shutil.copy(RAIZ / "ejemplos" / nombre, tmp_path / nombre))
    shutil.copy(RAIZ / "ejemplos" / "ayudas.py", tmp_path)  # (el del ejemplo 9)
    shutil.copy(RAIZ / "ejemplos" / "precios.csv", tmp_path)  # (el del ejemplo 10)
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
    for ejemplo in list((RAIZ / "ejemplos").glob("*.mate")) + [
            RAIZ / "ejemplos" / "ayudas.py", RAIZ / "ejemplos" / "precios.csv"]:
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
                  "probar mate\\ejemplos", "En total: 30 de 30 pruebas pasaron, en 15 archivos"]:
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


# Mejora 89: versión 0.3 (después 0.4: agentes que recuerdan y aprenden; y ahora 0.5: más
# rápido y con puente a Python)

def test_version_0_5_y_el_readme_lo_dice(capsys):
    assert mate.VERSION == "0.5"
    leeme = (RAIZ / "README.md").read_text(encoding="utf-8")
    assert "Versión 0.5." in leeme and "## Límites de la versión 0.5" in leeme
    assert "versión 0.2" not in leeme.replace("desde la versión 0.2 hasta la 0.5", "")
    assert "desde la versión 0.2 hasta la 0.5" in leeme and "versión 0.3" not in leeme
    assert mate.main(["--version"]) == 0
    assert capsys.readouterr().out.startswith("Mate 0.5 ")


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
    (tmp_path / "ayudas.py").write_text(  # (el de 'ayuda python', tal cual lo dice su ejemplo)
        "def doble(numero):\n    return numero * 2\n", encoding="utf-8")
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


# ───────────── Versión 0.4: agentes que recuerdan y aprenden de sus errores ─────────────
# Todo lo que escriben estas pruebas va a tmp_path: nunca a la carpeta de Mate.

CUENTA_CLIENTES = """
mensaje Llego { quien: texto }
mensaje Cuantos {}
agente Mostrador {
    estado recordado atendidos = 0
    estado saludo = "Hola"
    al recibir Llego como l {
        atendidos += 1
        si l.quien == "nadie" { fallar "no vino nadie" }
    }
    al recibir Cuantos { responder atendidos }
}
"""

APRENDIZ = """
mensaje Consulta { pregunta: texto }
mensaje Novedad { texto: texto }
mensaje QueSabes {}
agente Mostrador {
    estado reglas = "Atendés un almacén."
    al recibir Consulta como c {
        intentar {
            responder consultar_ia(reglas, c.pregunta, "Ya te averiguo.")
        } si falla motivo {
            responder "No pude: {motivo}"
        }
    }
    al recibir Novedad como n { aprender(n.texto) }
    al recibir QueSabes { responder lecciones() }
}
"""


def archivos_de(carpeta):
    return sorted(p.name for p in carpeta.iterdir())


def memoria_de(carpeta, nombre="programa"):
    import json
    return json.loads((carpeta / f"{nombre}.memoria.json").read_text(encoding="utf-8-sig"))


def orden_mate(capsys, *argumentos):
    capsys.readouterr()
    codigo = mate.main([str(a) for a in argumentos])
    capturado = capsys.readouterr()
    return codigo, capturado.out, capturado.err


def test_estado_recordado_no_rompe_a_quien_usa_esa_palabra_de_nombre():
    assert "recordado" not in mate.PALABRAS  # no gasta una palabra: solo vale tras 'estado'
    salida, _ = correr("""
        mensaje Ver {}
        agente A {
            estado recordado = 5
            estado recordado visto = recordado + 1
            al recibir Ver { responder [recordado, visto] }
        }
        sea recordado = "afuera"
        mostrar(preguntar Ver {} a A, recordado)
    """)
    assert salida == ["[5, 6] afuera"]
    declarados = mate.analizar("agente A {\n estado recordado = 5\n estado recordado n = 1\n}")[0][3]
    assert [(type(e) is mate.EstadoRecordado, e[1]) for e in declarados] == [
        (False, "recordado"), (True, "n")]
    assert "'si' es una palabra propia de Mate" in falla(
        "agente A { estado recordado si = 1 }").mensaje
    # sin archivo (acá, o en la consola) un estado recordado es un estado común
    assert correr(CUENTA_CLIENTES + "enviar Llego { quien: \"a\" } a Mostrador\n"
                  "mostrar(preguntar Cuantos {} a Mostrador)")[0] == ["1"]


def test_la_memoria_sigue_de_una_corrida_a_la_otra(tmp_path, capsys):
    programa = CUENTA_CLIENTES + """
        enviar Llego { quien: "Ana" } a Mostrador
        mostrar(preguntar Cuantos {} a Mostrador)
    """
    assert por_main(tmp_path, capsys, programa) == (0, "1\n", "")
    assert archivos_de(tmp_path) == ["programa.mate", "programa.memoria.json"]
    assert por_main(tmp_path, capsys, programa) == (0, "2\n", "")
    assert por_main(tmp_path, capsys, programa, "--traza")[1].endswith("3\n")
    guardado = memoria_de(tmp_path)
    # solo lo marcado con 'recordado' se guarda, y el archivo se entiende al abrirlo
    assert guardado["agentes"] == {"Mostrador": {"estado": {"atendidos": 3}, "lecciones": []}}
    assert "programa.mate" in guardado["que_es"] and "--olvidar" in guardado["que_es"]
    crudo = (tmp_path / "programa.memoria.json").read_bytes()
    assert crudo.startswith(b"\xef\xbb\xbf") and b'\n      "estado": {' in crudo
    assert archivos_de(tmp_path) == ["programa.mate", "programa.memoria.json"]
    # con el nombre que le pone el Bloc de notas, el archivo de memoria se llama igual
    assert mate.archivo_de("C:/x/mi.MATE.txt", "memoria.json") == "C:/x/mi.memoria.json"
    assert mate.archivo_de("mi_mostrador.mate", "bitacora.txt") == "mi_mostrador.bitacora.txt"


def test_un_programa_que_no_usa_lo_nuevo_no_crea_archivos(tmp_path, capsys):
    programa = AGENTES + """
        mensaje Romper {}
        agente Flojo { al recibir Romper { fallar "no quiero" } }
        mostrar((preguntar Sumar { a: 1, b: 2 } a Calculadora).valor)
        intentar { sea x = preguntar Romper {} a Flojo } si falla e { mostrar(e) }
        enviar Romper {} a Flojo
    """
    codigo, salida, err = por_main(tmp_path, capsys, programa)
    assert (codigo, salida) == (1, "3\nno quiero\n") and "no quiero" in err
    assert archivos_de(tmp_path) == ["programa.mate"]
    assert por_main(tmp_path, capsys, programa, "--olvidar")[0] == 1
    assert archivos_de(tmp_path) == ["programa.mate"]
    # los ejemplos de siempre tampoco dejan nada al lado
    import shutil
    for ejemplo in ["equipo.mate", "catalogo.mate", "07_agente_con_ia.mate"]:
        shutil.copy(RAIZ / "ejemplos" / ejemplo, tmp_path / ejemplo)
    assert mate.main(["correr", str(tmp_path / "equipo.mate")]) == 0
    assert mate.main(["correr", str(tmp_path / "07_agente_con_ia.mate")]) == 0  # sin clave
    capsys.readouterr()
    assert archivos_de(tmp_path) == ["07_agente_con_ia.mate", "catalogo.mate", "equipo.mate",
                                     "programa.mate"]


def test_probar_no_lee_ni_escribe_la_memoria(tmp_path, capsys):
    programa = CUENTA_CLIENTES + """
        enviar Llego { quien: "Ana" } a Mostrador
        enviar Llego { quien: "nadie" } a Mostrador
        prueba "arranca limpia" {
            asegurar preguntar Cuantos {} a Mostrador == 0
            aprender("algo", Mostrador)
        }
        prueba "y la siguiente también" {
            asegurar lecciones(Mostrador) == []
            enviar Llego { quien: "Eva" } a Mostrador
            asegurar preguntar Cuantos {} a Mostrador == 1
        }
    """
    assert por_main(tmp_path, capsys, programa)[0] == 1  # (el agente falla con "nadie")
    assert por_main(tmp_path, capsys, programa)[0] == 1
    assert orden_mate(capsys, "corregir", tmp_path / "programa.mate", "Mostrador", "Sé amable")[0] == 0
    antes = {p.name: p.read_bytes() for p in tmp_path.iterdir()}
    assert sorted(antes) == ["programa.bitacora.txt", "programa.mate", "programa.memoria.json"]
    assert memoria_de(tmp_path)["agentes"]["Mostrador"]["estado"] == {"atendidos": 2}
    codigo, salida, _ = por_main(tmp_path, capsys, programa, orden="probar")
    assert "2 de 2 pruebas pasaron" in salida
    charla = tmp_path / "charla.txt"
    assert por_main(tmp_path, capsys, programa, f"--traza={charla}", orden="probar")[0] == 1
    charla.unlink()
    assert {p.name: p.read_bytes() for p in tmp_path.iterdir()} == antes
    codigo, _, err = por_main(tmp_path, capsys, programa, "--olvidar", orden="probar")
    assert codigo == 2 and "--olvidar va con 'correr'" in err


def test_cada_copia_con_nombre_tiene_su_memoria(tmp_path, capsys):
    programa = CUENTA_CLIENTES + """
        sea centro = crear Mostrador llamado "Centro"
        sea norte = crear Mostrador llamado "Norte" { atendidos: 100 }
        sea suelta = crear Mostrador
        enviar Llego { quien: "a" } a centro
        enviar Llego { quien: "b" } a [norte, norte, suelta]
        mostrar(preguntar Cuantos {} a Mostrador, preguntar Cuantos {} a centro,
                preguntar Cuantos {} a norte, preguntar Cuantos {} a suelta)
    """
    codigo, salida, err = por_main(tmp_path, capsys, programa)
    assert (codigo, salida) == (0, "0 1 102 1\n")
    # la copia sin nombre no recuerda, y Mate lo avisa una sola vez
    assert err.count("aviso:") == 1 and 'crear Mostrador llamado "Centro"' in err
    assert "las copias de Mostrador creadas sin nombre no recuerdan" in err
    # lo recordado le gana al valor que le da 'crear', que es solo el inicial
    assert por_main(tmp_path, capsys, programa)[1] == "0 2 104 1\n"
    assert {a: f["estado"] for a, f in memoria_de(tmp_path)["agentes"].items()} == {
        "Mostrador": {"atendidos": 0}, "Mostrador Centro": {"atendidos": 2},
        "Mostrador Norte": {"atendidos": 104}}


def test_se_recuerdan_listas_mapas_y_mensajes_pero_no_agentes(tmp_path, capsys):
    programa = """
        mensaje Pedido { producto: texto, cantidad: numero desde 1 }
        mensaje Anotar { pedido: Pedido }
        mensaje Ver {}
        agente Libreta {
            estado recordado pedidos = []
            estado recordado ultimo_pedido = nada
            estado recordado datos = { abierto: verdadero, precio: 3.5 }
            estado recordado amigo = nada
            al recibir Anotar como a {
                pedidos = agregar(pedidos, a.pedido)
                ultimo_pedido = a.pedido
                amigo = remitente
                datos.precio = datos.precio + 1
            }
            al recibir Ver { responder [largo(pedidos), ultimo_pedido, datos] }
        }
        mensaje Arrancar {}
        agente Cliente {
            al recibir Arrancar {
                enviar Anotar { pedido: Pedido { producto: "yerba", cantidad: 2 } } a Libreta
            }
        }
        mostrar(preguntar Ver {} a Libreta)
        enviar Arrancar {} a Cliente
    """
    codigo, salida, err = por_main(tmp_path, capsys, programa)
    assert (codigo, salida) == (0, "[0, nada, {abierto: verdadero, precio: 3.5}]\n")
    assert "Libreta.amigo no se pudo guardar en la memoria" in err and "no agentes" in err
    codigo, salida, err = por_main(tmp_path, capsys, programa)
    assert salida == ('[1, Pedido { producto: "yerba", cantidad: 2 }, '
                      "{abierto: verdadero, precio: 4.5}]\n")
    assert "amigo" not in memoria_de(tmp_path)["agentes"]["Libreta"]["estado"]


def test_si_el_tipo_guardado_ya_no_coincide_avisa_y_usa_el_inicial(tmp_path, capsys):
    programa = CUENTA_CLIENTES + "enviar Llego { quien: \"a\" } a Mostrador\n" \
                          "mostrar(preguntar Cuantos {} a Mostrador)"
    assert por_main(tmp_path, capsys, programa)[1] == "1\n"
    memoria = tmp_path / "programa.memoria.json"
    memoria.write_text(memoria.read_text(encoding="utf-8-sig").replace(
        '"atendidos": 1', '"atendidos": "muchos",\n "viejo": 3'), encoding="utf-8")
    codigo, salida, err = por_main(tmp_path, capsys, programa)
    assert (codigo, salida) == (0, "1\n")
    assert err == ("aviso: Mostrador.atendidos está guardado en la memoria como texto y en el "
                   "programa ahora es numero: no uso lo guardado y arranca con su valor "
                   "inicial\n")
    # lo que el programa ya no declara como recordado se va del archivo
    assert memoria_de(tmp_path)["agentes"]["Mostrador"]["estado"] == {"atendidos": 1}
    # un mensaje guardado que ya no cumple su contrato tampoco rompe nada
    con_mensaje = """
        mensaje P { n: numero desde 1 }
        mensaje Ver {}
        agente A {
            estado recordado p = P { n: 5 }
            al recibir Ver { responder p.n }
        }
        mostrar(preguntar Ver {} a A)
    """
    (tmp_path / "programa.memoria.json").unlink()
    assert por_main(tmp_path, capsys, con_mensaje)[1] == "5\n"
    memoria.write_text(memoria.read_text(encoding="utf-8-sig").replace('"n": 5', '"n": 0'),
                       encoding="utf-8")
    codigo, salida, err = por_main(tmp_path, capsys, con_mensaje)
    assert (codigo, salida) == (0, "5\n")
    assert "lo que A.p tenía guardado en la memoria ya no sirve" in err and "desde 1" in err


def test_una_memoria_rota_se_avisa_claro_y_no_se_pisa(tmp_path, capsys):
    programa = CUENTA_CLIENTES + "enviar Llego { quien: \"a\" } a Mostrador\n" \
                          "mostrar(preguntar Cuantos {} a Mostrador)"
    memoria = tmp_path / "programa.memoria.json"
    (tmp_path / "programa.mate").write_text(programa, encoding="utf-8")
    rotas = {
        '{\n "agentes": {\n  "Mostrador": { "estado": { "atendidos": 7, } }\n }\n}':
            "en el renglón 3 hay algo mal escrito",
        "[1, 2]": 'le falta la parte "agentes"',
        '{"agentes": {"Mostrador": {"estado": [1]}}}': 'lo que guarda de "Mostrador" no tiene',
        '{"agentes": {"Mostrador": {"lecciones": "sé amable"}}}': "no tiene la forma de siempre",
        '{"agentes": {"Mostrador": {"estado": {"atendidos": NaN}}}}': "un número que no es válido",
        '{"agentes": {"Mostrador": {"estado": {"atendidos": 1e999}}}}': "un número que no es",
    }
    for contenido, explicacion in rotas.items():
        memoria.write_text(contenido, encoding="utf-8")
        for orden in (["correr"], ["corregir", "Mostrador", "algo"], ["lecciones"]):
            codigo, salida, err = orden_mate(capsys, orden[0], tmp_path / "programa.mate", *orden[1:])
            assert (codigo, salida) == (2, ""), (contenido, orden)
            assert "no entiendo el archivo de memoria programa.memoria.json" in err
            assert explicacion in err and "Bloc de notas" in err and "Traceback" not in err
            assert memoria.read_text(encoding="utf-8") == contenido  # no se pisa
    # 'probar' ni la mira
    assert por_main(tmp_path, capsys, programa + '\nprueba "p" { asegurar 1 == 1 }',
                    orden="probar")[0] == 0
    assert memoria.read_text(encoding="utf-8") == list(rotas)[-1]
    # con --olvidar se empieza de cero aunque no se entienda
    codigo, salida, err = por_main(tmp_path, capsys, programa, "--olvidar")
    assert (codigo, salida) == (0, "1\n") and "arrancan de cero" in err
    assert memoria_de(tmp_path)["agentes"]["Mostrador"]["estado"] == {"atendidos": 1}
    # vacío, o guardado por el Bloc de notas como "Unicode" o ANSI, se lee igual
    memoria.write_text("  \n", encoding="utf-8")
    assert por_main(tmp_path, capsys, programa)[1:] == ("1\n", "")
    memoria.write_text('{"agentes": {"Mostrador": {"estado": {"atendidos": 40}}}}',
                       encoding="utf-16")
    assert por_main(tmp_path, capsys, programa)[1:] == ("41\n", "")
    # las lecciones escritas a mano valen; las que no se entienden se saltean con aviso
    memoria.write_text('{"agentes": {"Mostrador": {"lecciones": ["Sé breve", 7, {"texto": ""}, '
                       '{"texto": "%s"}]}}}' % ("largo " * 80), encoding="utf-8")
    codigo, salida, err = por_main(tmp_path, capsys, programa)
    assert (codigo, salida) == (0, "1\n")
    assert err.count("no se entiende") == 2 and "uso solo el principio" in err
    lecciones = memoria_de(tmp_path)["agentes"]["Mostrador"]["lecciones"]
    assert lecciones[0] == {"fecha": "", "texto": "Sé breve"}
    assert len(lecciones) == 2 and len(lecciones[1]["texto"]) <= mate.LARGO_DE_LECCION + 3


def test_la_memoria_se_guarda_aunque_el_programa_termine_con_error(tmp_path, capsys, monkeypatch):
    programa = CUENTA_CLIENTES + """
        enviar Llego { quien: "a" } a Mostrador
        enviar Llego { quien: "nadie" } a Mostrador
        enviar Llego { quien: "b" } a Mostrador
        mostrar(preguntar Cuantos {} a Mostrador)
        mostrar(1 / 0)
    """
    codigo, salida, err = por_main(tmp_path, capsys, programa)
    assert (codigo, salida) == (1, "2\n") and "división por cero" in err
    # el mensaje que falló no cuenta (el agente volvió a como estaba), los otros dos sí
    assert memoria_de(tmp_path)["agentes"]["Mostrador"]["estado"] == {"atendidos": 2}
    assert "programa.memoria.json.tmp" not in archivos_de(tmp_path)
    # si no se puede escribir, avisa y el archivo anterior queda entero
    anterior = (tmp_path / "programa.memoria.json").read_bytes()

    def no_se_puede(*_a):
        raise PermissionError("abierto en otro programa")

    monkeypatch.setattr(mate.os, "replace", no_se_puede)
    codigo, salida, err = por_main(tmp_path, capsys, programa)
    assert (codigo, salida) == (1, "4\n")
    assert "aviso: no pude guardar la memoria en" in err and "Traceback" not in err
    assert (tmp_path / "programa.memoria.json").read_bytes() == anterior
    assert not [a for a in archivos_de(tmp_path) if a.endswith(".tmp")]
    monkeypatch.undo()
    # y también si lo cortan con Ctrl+C a mitad de camino
    def cortar(_pregunta):
        raise KeyboardInterrupt

    monkeypatch.setattr(mate, "por_teclado", cortar)
    cortado = CUENTA_CLIENTES + 'enviar Llego { quien: "a" } a Mostrador\n' \
                         'mostrar(preguntar Cuantos {} a Mostrador)\nsea x = leer("¿Seguimos?")'
    codigo, salida, err = por_main(tmp_path, capsys, cortado)
    # (desde la 0.5, Ctrl+C en un leer() se avisa sin cartel de error; el código sigue en 130)
    assert (codigo, salida, err) == (130, "3\n", f"\n{mate.CORTE_EN_EL_TECLADO}\n")
    assert memoria_de(tmp_path)["agentes"]["Mostrador"]["estado"] == {"atendidos": 3}


def test_olvidar_empieza_de_cero_pero_no_borra_las_lecciones(tmp_path, capsys):
    programa = CUENTA_CLIENTES + "enviar Llego { quien: \"a\" } a Mostrador\n" \
                          "mostrar(preguntar Cuantos {} a Mostrador)"
    archivo = tmp_path / "programa.mate"
    assert por_main(tmp_path, capsys, programa)[1] == "1\n"
    assert por_main(tmp_path, capsys, programa)[1] == "2\n"
    assert orden_mate(capsys, "corregir", archivo, "Mostrador", "Sé amable")[0] == 0
    codigo, salida, err = por_main(tmp_path, capsys, programa, "--olvidar")
    assert (codigo, salida) == (0, "1\n")
    assert "aviso: --olvidar: los agentes arrancan de cero" in err and "lecciones" in err
    ficha = memoria_de(tmp_path)["agentes"]["Mostrador"]
    assert ficha["estado"] == {"atendidos": 1}
    assert [leccion["texto"] for leccion in ficha["lecciones"]] == ["Sé amable"]
    assert por_main(tmp_path, capsys, programa)[1] == "2\n"
    for orden in ("probar", "verificar"):
        codigo, _, err = por_main(tmp_path, capsys, programa, "--olvidar", orden=orden)
        assert codigo == 2 and "--olvidar va con 'correr'" in err
    assert "--olvidar" in mate.OPCIONES and "--olvidar" in mate.texto_de_ayuda()
    assert mate.main(["correr", str(archivo), "--olvidarr"]) == 2
    assert "¿quisiste decir --olvidar?" in capsys.readouterr().err


BITACORA = """
mensaje Pedido { producto: texto, cantidad: numero desde 1 }
mensaje Encargar { producto: texto, cantidad: numero }
mensaje Ticket { total: numero }
mensaje Pedir { producto: texto } responde Ticket
agente Deposito {
    estado recordado entregas = 0
    al recibir Pedido como p {
        si p.producto == "caviar" { fallar "no hay caviar, clave sk-ant-clave-de-mentira-123" }
        entregas += 1
        responder entregas
    }
    al recibir Pedir como p { responder p.producto }
}
agente Vendedor {
    al recibir Encargar como e {
        intentar {
            responder preguntar Pedido { producto: e.producto, cantidad: e.cantidad } a Deposito
        } si falla motivo {
            responder "sin stock"
        }
    }
}
"""


def test_la_bitacora_anota_sola_las_fallas_de_los_agentes(tmp_path, capsys, monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", CLAVE_DE_MENTIRA)
    programa = BITACORA + """
        mostrar(preguntar Encargar { producto: "yerba", cantidad: 2 } a Vendedor)
        mostrar(preguntar Encargar { producto: "caviar", cantidad: 1 } a Vendedor)
        mostrar(preguntar Encargar { producto: "pan", cantidad: 0 } a Vendedor)
        intentar { sea t = preguntar Pedir { producto: "pan" } a Deposito } si falla e { mostrar("mal") }
        enviar Pedido { producto: "caviar", cantidad: 3 } a Deposito
    """
    codigo, salida, err = por_main(tmp_path, capsys, programa)
    assert (codigo, salida) == (1, "1\nsin stock\nsin stock\nmal\n")
    assert archivos_de(tmp_path) == ["programa.bitacora.txt", "programa.mate",
                                     "programa.memoria.json"]
    texto = (tmp_path / "programa.bitacora.txt").read_text(encoding="utf-8-sig")
    titulos = [r for r in texto.splitlines() if r.startswith("#")]
    assert titulos[0] == ("# Bitácora de programa.mate: las fallas de sus agentes, la más "
                          "nueva abajo.")
    assert "fecha | agente | qué pasó | qué mensaje atendía | el motivo" in titulos[1]
    renglones = [r.split(" | ") for r in texto.splitlines() if r and not r.startswith("#")]
    assert all(re.fullmatch(r"\d\d/\d\d/\d{4} \d\d:\d\d", r[0]) for r in renglones)
    assert [r[1:3] for r in renglones] == [
        ["Deposito", "falló"],
        ["Vendedor", "falló (lo atajó con 'intentar')"],
        ["Vendedor", "contrato rechazado (lo atajó con 'intentar')"],
        ["Deposito", "contrato rechazado"],
        ["Deposito", "falló"]]
    assert renglones[0][3] == 'Pedido { producto: "caviar", cantidad: 1 }'
    assert renglones[1][3] == 'Encargar { producto: "caviar", cantidad: 1 }'
    assert "Pedido.cantidad no puede valer 0" in renglones[2][4]
    assert "el contrato dice que a Pedir se le responde Ticket" in renglones[3][4]
    # la clave de la IA nunca queda escrita, aunque venga adentro de un error
    assert renglones[0][4] == "no hay caviar, clave (la clave)"
    assert "sk-ant" not in texto and CLAVE_DE_MENTIRA[-8:] not in texto
    # con tamaño acotado: se quedan las últimas
    monkeypatch.setattr(mate, "MAX_BITACORA", 7)
    assert por_main(tmp_path, capsys, programa)[0] == 1
    texto = (tmp_path / "programa.bitacora.txt").read_text(encoding="utf-8-sig")
    renglones = [r for r in texto.splitlines() if r and not r.startswith("#")]
    assert len(renglones) == 7 and "las últimas 7" in texto
    assert "Deposito | contrato rechazado" in renglones[0]  # se fueron las 3 más viejas
    # la orden que la resume
    codigo, salida, err = orden_mate(capsys, "bitácora", tmp_path / "programa.mate")
    assert (codigo, err) == (0, "")
    assert salida.startswith("Bitácora de programa.mate: 7 falla(s) anotada(s), del ")
    for frase in ["Por agente:", "     5 veces  Deposito", "     2 veces  Vendedor",
                  "Qué pasó:", "contrato rechazado (lo atajó con 'intentar')",
                  "Los motivos que más se repiten:", "     4 veces  no hay caviar",
                  "Las últimas:", "programa.bitacora.txt (se abre con el Bloc de notas"]:
        assert frase in salida, frase
    assert "sk-ant" not in salida
    # un renglón editado a mano que no se entiende no rompe la orden
    with open(tmp_path / "programa.bitacora.txt", "a", encoding="utf-8") as f:
        f.write("esto lo escribí yo\n")
    codigo, salida, err = orden_mate(capsys, "bitacora", tmp_path / "programa.mate")
    assert codigo == 0 and "7 falla(s)" in salida and "1 renglón(es) del archivo no tienen" in salida


def test_la_bitacora_es_solo_para_programas_con_memoria_o_lecciones(tmp_path, capsys):
    sin_memoria = BITACORA.replace("estado recordado entregas", "estado entregas") + """
        mostrar(preguntar Encargar { producto: "caviar", cantidad: 1 } a Vendedor)
    """
    archivo = tmp_path / "programa.mate"
    assert por_main(tmp_path, capsys, sin_memoria) == (0, "sin stock\n", "")
    assert archivos_de(tmp_path) == ["programa.mate"]
    codigo, salida, _ = orden_mate(capsys, "bitacora", archivo)
    assert codigo == 0 and salida.startswith("programa.mate no tiene fallas anotadas.")
    # en cuanto el agente tiene una lección, sus fallas se empiezan a anotar
    assert orden_mate(capsys, "corregir", archivo, "Deposito", "Avisá si no hay")[0] == 0
    assert por_main(tmp_path, capsys, sin_memoria) == (0, "sin stock\n", "")
    assert archivos_de(tmp_path) == ["programa.bitacora.txt", "programa.mate",
                                     "programa.memoria.json"]
    # con 'probar' no se anota nada
    (tmp_path / "programa.bitacora.txt").unlink()
    con_prueba = BITACORA + """
        prueba "falla" {
            asegurar preguntar Encargar { producto: "caviar", cantidad: 1 } a Vendedor == "sin stock"
        }
    """
    assert por_main(tmp_path, capsys, con_prueba, orden="probar")[0] == 0
    assert "programa.bitacora.txt" not in archivos_de(tmp_path)
    # la orden, mal usada
    codigo, _, err = orden_mate(capsys, "bitacora")
    assert codigo == 2 and "a 'bitacora' le falta el programa" in err
    codigo, _, err = orden_mate(capsys, "bitacora", archivo, "Deposito")
    assert codigo == 2 and "lleva solo el programa" in err
    codigo, _, err = orden_mate(capsys, "bitacora", tmp_path / "no_esta.mate")
    assert codigo == 2 and "no encuentro 'no_esta.mate'" in err
    assert orden_mate(capsys, "bitacoras", archivo)[2].startswith(
        "no conozco la orden 'bitacoras', ¿quisiste decir 'bitacora'?")


def test_la_ia_que_no_contesta_queda_en_la_bitacora_sin_la_clave(tmp_path, capsys, ia):
    programa = APRENDIZ.replace("estado reglas", "estado recordado reglas") + """
        mostrar(preguntar Consulta { pregunta: "¿Hay yerba?" } a Mostrador)
    """
    ia.respuestas = [error_http(401, "authentication_error", f"invalid x-api-key {CLAVE_DE_MENTIRA}")]
    codigo, salida, err = por_main(tmp_path, capsys, programa)
    assert codigo == 0 and salida.startswith("No pude: consultar_ia(): la clave no sirve")
    texto = (tmp_path / "programa.bitacora.txt").read_text(encoding="utf-8-sig")
    (renglon,) = [r for r in texto.splitlines() if r and not r.startswith("#")]
    assert " | Mostrador | la IA no contestó (lo atajó con 'intentar') | " in renglon
    assert 'Consulta { pregunta: "¿Hay yerba?" } | consultar_ia(): la clave no sirve' in renglon
    todo = texto + (tmp_path / "programa.memoria.json").read_text(encoding="utf-8-sig")
    assert "sk-ant" not in todo and CLAVE_DE_MENTIRA not in todo


def test_corregir_anota_lecciones_sin_tocar_el_programa(tmp_path, capsys):
    archivo = tmp_path / "mi_mostrador.mate"
    archivo.write_text(APRENDIZ + 'mostrar(preguntar QueSabes {} a Mostrador)\n', encoding="utf-8")
    original = archivo.read_bytes()
    leccion = "Si piden menos de 10 unidades, avisá que no hay envío"
    codigo, salida, err = orden_mate(capsys, "corregir", archivo, "Mostrador", leccion)
    assert (codigo, err) == (0, "")
    assert salida.startswith("Anotado. Mostrador tiene 1 lección(es):\n"
                             f"  1. {leccion}   (del ")
    assert "consultar_ia()" in salida and "--borrar=1" in salida
    assert archivos_de(tmp_path) == ["mi_mostrador.mate", "mi_mostrador.memoria.json"]
    guardada = memoria_de(tmp_path, "mi_mostrador")["agentes"]["Mostrador"]
    assert guardada["estado"] == {} and guardada["lecciones"][0]["texto"] == leccion
    assert re.fullmatch(r"\d\d/\d\d/\d{4} \d\d:\d\d", guardada["lecciones"][0]["fecha"])
    # sin comillas las palabras llegan sueltas: se juntan. Y da igual 'mostrador' que 'Mostrador'
    codigo, salida, _ = orden_mate(capsys, "corregir", archivo, "mostrador", "Los", "lunes  no", "hay pan")
    assert codigo == 0 and "  2. Los lunes no hay pan   (del " in salida
    # la misma no se anota dos veces
    codigo, salida, _ = orden_mate(capsys, "corregir", archivo, "Mostrador", "Los lunes no hay pan")
    assert (codigo, salida) == (0, "Mostrador ya tenía anotada esa lección: no la repito.\n")
    # el programa las ve con lecciones(), en la próxima corrida
    assert orden_mate(capsys, "correr", archivo)[1] == f'["{leccion}", "Los lunes no hay pan"]\n'
    assert archivo.read_bytes() == original
    # también a una copia con nombre
    codigo, salida, _ = orden_mate(capsys, "corregir", archivo, "Mostrador Centro", "Cerrá a las 20")
    assert codigo == 0 and salida.startswith("Anotado. Mostrador Centro tiene 1 lección(es):")
    # lo que está mal se explica
    codigo, salida, err = orden_mate(capsys, "corregir", archivo, "Mostrado", "algo")
    assert (codigo, salida) == (2, "")
    assert err == ("mi_mostrador.mate no tiene un agente 'Mostrado'. ¿Quisiste decir "
                   "'Mostrador'? Sus agentes son: Mostrador\n")
    codigo, _, err = orden_mate(capsys, "corregir", archivo, "Mostrador")
    assert codigo == 2 and "le faltan el agente y la lección" in err
    codigo, _, err = orden_mate(capsys, "corregir", archivo)
    assert codigo == 2 and "Los agentes de ese programa son: Mostrador" in err
    codigo, _, err = orden_mate(capsys, "corregir")
    assert codigo == 2 and 'corregir mi_mostrador.mate Mostrador "Los lunes no hay pan"' in err
    codigo, _, err = orden_mate(capsys, "corregir", archivo, "Mostrador", "   ")
    assert codigo == 2 and "la lección está vacía" in err
    codigo, _, err = orden_mate(capsys, "corregir", archivo, "Mostrador", "muy largo " * 40)
    assert codigo == 2 and "tiene 399 letras y el tope es 300" in err and "se paga" in err
    codigo, _, err = orden_mate(capsys, "corregir", archivo, "Mostrador", "algo", "--borrar=1")
    assert codigo == 2 and "--borrar va con 'lecciones'" in err
    archivo.write_text("agente {", encoding="utf-8")
    codigo, _, err = orden_mate(capsys, "corregir", archivo, "Mostrador", "algo")
    assert codigo == 2 and "tiene un error y no puedo ver qué agentes tiene" in err
    assert "verificar" in err


def test_listar_y_borrar_lecciones(tmp_path, capsys):
    archivo = tmp_path / "programa.mate"
    archivo.write_text(APRENDIZ, encoding="utf-8")
    codigo, salida, _ = orden_mate(capsys, "lecciones", archivo)
    assert codigo == 0 and "todavía no tienen lecciones" in salida
    assert 'corregir' in salida and 'Mostrador "la lección"' in salida
    assert archivos_de(tmp_path) == ["programa.mate"]
    for leccion in ["Uno", "Dos", "Tres"]:
        assert orden_mate(capsys, "corregir", archivo, "Mostrador", leccion)[0] == 0
    assert orden_mate(capsys, "corregir", archivo, "Mostrador Norte", "Cuatro")[0] == 0
    codigo, salida, _ = orden_mate(capsys, "lecciones", archivo)
    renglones = [re.sub(r"   \(del .*\)$", "", r) for r in salida.splitlines()]
    assert renglones == ["Mostrador tiene 3 lección(es):", "  1. Uno", "  2. Dos", "  3. Tres",
                         "Mostrador Norte tiene 1 lección(es):", "  1. Cuatro"]
    codigo, salida, _ = orden_mate(capsys, "lecciones", archivo, "mostrador norte")
    assert salida.startswith("Mostrador Norte tiene 1 lección(es):") and "Uno" not in salida
    codigo, salida, _ = orden_mate(capsys, "lecciones", archivo, "Mostrador", "--borrar=2")
    assert codigo == 0 and salida.startswith("Borrada. A Mostrador le quedan 2 lección(es):")
    assert "  2. Tres" in salida and "Dos" not in salida
    for mal, explicacion in [("--borrar=5", "del 1 al 2"), ("--borrar=dos", "recibió 'dos'"),
                             ("--borrar=0", "del 1 al 2")]:
        codigo, _, err = orden_mate(capsys, "lecciones", archivo, "Mostrador", mal)
        assert codigo == 2 and explicacion in err, mal
    codigo, _, err = orden_mate(capsys, "lecciones", archivo, "--borrar=1")
    assert codigo == 2 and "hay que decir de qué agente" in err
    codigo, _, err = orden_mate(capsys, "lecciones", archivo, "Mostrador", "--borrar")
    assert codigo == 2 and "le falta el número de la lección" in err
    codigo, _, err = orden_mate(capsys, "correr", archivo, "--borrar=1")
    assert codigo == 2 and "--borrar va con 'lecciones'" in err
    codigo, salida, _ = orden_mate(capsys, "lecciones", archivo, "Mostrador", "--borrar=todas")
    assert codigo == 0 and salida == "Borrada. A Mostrador le quedan 0 lección(es).\n"
    codigo, _, err = orden_mate(capsys, "lecciones", archivo, "Mostrador", "--borrar=1")
    assert codigo == 2 and "Mostrador no tiene lecciones para borrar" in err
    assert orden_mate(capsys, "lecciones", archivo, "Mostrador Norte", "--borrar=1")[0] == 0
    assert archivos_de(tmp_path) == ["programa.mate"]  # sin nada que recordar, no queda archivo
    codigo, salida, _ = orden_mate(capsys, "lecciones", archivo, "Mostrador")
    assert codigo == 0 and salida.startswith("Mostrador todavía no tiene lecciones.")


def test_el_tope_de_lecciones_se_queda_con_las_mas_nuevas_y_avisa(tmp_path, capsys, monkeypatch):
    monkeypatch.setattr(mate, "MAX_LECCIONES", 3)
    archivo = tmp_path / "programa.mate"
    archivo.write_text(APRENDIZ + """
        enviar Novedad { texto: "Cinco" } a Mostrador
        enviar Novedad { texto: "Seis" } a Mostrador
        mostrar(preguntar QueSabes {} a Mostrador)
    """, encoding="utf-8")
    for leccion in ["Uno", "Dos", "Tres"]:
        assert "El tope es" not in orden_mate(capsys, "corregir", archivo, "Mostrador", leccion)[1]
    codigo, salida, _ = orden_mate(capsys, "corregir", archivo, "Mostrador", "Cuatro")
    assert codigo == 0 and "Mostrador tiene 3 lección(es)" in salida
    assert "(El tope es 3: para anotar esta se borró la más vieja.)" in salida
    assert "Uno" not in salida and "  3. Cuatro" in salida
    # lo mismo cuando aprende solo: avisa una vez por corrida
    codigo, salida, err = orden_mate(capsys, "correr", archivo)
    assert (codigo, salida) == (0, '["Cuatro", "Cinco", "Seis"]\n')
    assert err == ("aviso: Mostrador ya tenía 3 lecciones, que es el tope: para anotar la "
                   "nueva se olvidó de la más vieja\n")
    assert [leccion["texto"] for leccion in memoria_de(tmp_path)["agentes"]["Mostrador"][
        "lecciones"]] == ["Cuatro", "Cinco", "Seis"]
    # y una lección demasiado larga es un error que se puede atajar
    salida, interprete = correr(APRENDIZ + 'enviar Novedad { texto: "%s" } a Mostrador'
                                % ("largo " * 80))
    assert "aprender(): la lección tiene 479 letras y el tope es 300" in interprete.errores_agentes[0]
    salida, interprete = correr(APRENDIZ + 'enviar Novedad { texto: "  " } a Mostrador')
    assert "aprender(): la lección está vacía" in interprete.errores_agentes[0]


def test_un_agente_se_anota_lecciones_y_las_lee(tmp_path, capsys):
    programa = APRENDIZ + """
        mensaje Tropezar { texto: texto }
        agente Torpe {
            al recibir Tropezar como t {
                aprender(t.texto)
                fallar "me caí"
            }
            al recibir QueSabes { responder lecciones() }
        }
        enviar Novedad { texto: "Los lunes   no hay pan" } a Mostrador
        enviar Novedad { texto: "Los lunes no hay pan" } a Mostrador
        enviar Novedad { texto: "Cerramos a las 20" } a Mostrador
        intentar { enviar Tropezar { texto: "no sirve" } a Torpe } si falla e { mostrar(e) }
        mostrar(preguntar QueSabes {} a Mostrador, preguntar QueSabes {} a Torpe)
    """
    codigo, salida, err = por_main(tmp_path, capsys, programa, "--traza")
    assert codigo == 1 and "me caí" in err
    # no se repite, y lo que aprendió un agente mientras fallaba no queda
    assert salida.splitlines()[-1] == '["Los lunes no hay pan", "Cerramos a las 20"] []'
    assert salida.count('Mostrador aprende: "') == 2
    agentes = memoria_de(tmp_path)["agentes"]
    assert list(agentes) == ["Mostrador"]
    assert [leccion["texto"] for leccion in agentes["Mostrador"]["lecciones"]] == [
        "Los lunes no hay pan", "Cerramos a las 20"]
    # en la próxima corrida las sigue teniendo, sin duplicarlas
    codigo, salida, _ = por_main(tmp_path, capsys, programa)
    assert salida.splitlines()[-1] == '["Los lunes no hay pan", "Cerramos a las 20"] []'
    # afuera de un agente no van, y el error dice cómo se hace
    for mal in ['aprender("algo")', "sea x = lecciones()", 'aprender("algo", Mostrador)']:
        error = falla(APRENDIZ + mal)
        assert "solo va dentro de un agente" in error.mensaje, mal
        assert "la orden 'corregir'" in error.mensaje
    assert falla("sea x = aprender()").mensaje.startswith("aprender() lleva 1 o 2 valores")
    assert "aprender() espera texto y recibió numero" in falla(APRENDIZ + """
        mensaje Mal {}
        agente Otro { al recibir Mal { aprender(5)  responder 1 } }
        sea x = preguntar Mal {} a Otro
    """.replace("  responder", "\n responder")).mensaje
    # aprender() suelta en un renglón vale (hace algo); lecciones() suelta, no
    assert "lecciones" not in mate.HACEN_ALGO and "aprender" in mate.HACEN_ALGO


def test_consultar_ia_agrega_solas_las_lecciones_del_agente(tmp_path, capsys, ia):
    archivo = tmp_path / "programa.mate"
    archivo.write_text(APRENDIZ + """
        sea centro = crear Mostrador llamado "Centro"
        mostrar(preguntar Consulta { pregunta: "¿Hay yerba?" } a Mostrador)
        mostrar(preguntar Consulta { pregunta: "¿Y pan?" } a centro)
        mostrar(consultar_ia("Sos breve.", "Hola"))
    """, encoding="utf-8")
    # sin lecciones, las instrucciones viajan tal cual (como en la 0.3)
    assert orden_mate(capsys, "correr", archivo)[0] == 0
    assert [p["cuerpo"]["system"] for p in ia.pedidos] == [
        "Atendés un almacén.", "Atendés un almacén.", "Sos breve."]
    assert archivos_de(tmp_path) == ["programa.mate"]
    ia.pedidos.clear()
    assert orden_mate(capsys, "corregir", archivo, "Mostrador", "No hay envío por menos de 10")[0] == 0
    assert orden_mate(capsys, "corregir", archivo, "Mostrador", "Los lunes no hay pan")[0] == 0
    assert orden_mate(capsys, "corregir", archivo, "Mostrador Centro", "Cerrá a las 20")[0] == 0
    codigo, salida, err = orden_mate(capsys, "correr", archivo, "--traza")
    assert (codigo, err) == (0, "")
    del_agente, de_la_copia, del_programa = [p["cuerpo"]["system"] for p in ia.pedidos]
    assert del_agente == (
        "Atendés un almacén.\n\n"
        "LECCIONES APRENDIDAS (correcciones que te hicieron antes: tenelas siempre en cuenta)\n"
        "1. No hay envío por menos de 10\n2. Los lunes no hay pan")
    # la copia tiene las del agente del que es copia, y después las suyas
    assert de_la_copia == del_agente + "\n3. Cerrá a las 20"
    assert del_programa == "Sos breve."  # el programa principal no tiene lecciones
    assert ia.pedidos[0]["cuerpo"]["messages"] == [{"role": "user", "content": "¿Hay yerba?"}]
    # y se ve en la traza
    assert '  ·        Mostrador consulta a la IA: "¿Hay yerba?"\n' \
           '  ·           con la lección 1: "No hay envío por menos de 10"\n' \
           '  ·           con la lección 2: "Los lunes no hay pan"\n' in salida
    assert 'con la lección 3: "Cerrá a las 20"' in salida
    assert mate.con_lecciones("", ["Una"]) == mate.TITULO_DE_LECCIONES + "\n1. Una"


def test_en_las_pruebas_se_fijan_lecciones_y_se_ve_lo_que_llego_a_la_ia(tmp_path, capsys):
    programa = APRENDIZ + """
        prueba "la lección le llega a la IA" {
            aprender("No hay envío por menos de 10", Mostrador)
            aprender("Los lunes no hay pan", Mostrador)
            simular_ia("No, por 5 no hay envío.")
            asegurar preguntar Consulta { pregunta: "¿Me mandan 5?" } a Mostrador == "No, por 5 no hay envío."
            sea consultas = consultas_ia()
            asegurar largo(consultas) == 1
            asegurar consultas[0].agente == "Mostrador" y consultas[0].pregunta == "¿Me mandan 5?"
            asegurar consultas[0].respuesta == "No, por 5 no hay envío."
            asegurar tiene(consultas[0].instrucciones, "Atendés un almacén.")
            asegurar tiene(consultas[0].instrucciones, "LECCIONES APRENDIDAS")
            asegurar tiene(consultas[0].instrucciones, "1. No hay envío por menos de 10")
            asegurar lecciones(Mostrador) == ["No hay envío por menos de 10", "Los lunes no hay pan"]
        }
        prueba "cada prueba arranca sin lecciones y sin consultas" {
            asegurar lecciones(Mostrador) == [] y consultas_ia() == []
            enviar Novedad { texto: "Cerramos a las 20" } a Mostrador
            sea sabe = lecciones(Mostrador)
            asegurar sabe == ["Cerramos a las 20"]
            enviar Consulta { pregunta: "¿Abren?" } a Mostrador
            asegurar tiene(ultimo(consultas_ia()).instrucciones, "1. Cerramos a las 20")
        }
        prueba "una consulta que falla queda sin respuesta" {
            simular_ia(["una sola"])
            sea a = preguntar Consulta { pregunta: "uno" } a Mostrador
            sea b = preguntar Consulta { pregunta: "dos" } a Mostrador
            asegurar empieza_con(b, "No pude")
            asegurar consultas_ia()[1].respuesta == nada
        }
        prueba "hay que decir de qué agente" {
            asegurar falla { aprender("algo") }, "en una prueba hay que decir de qué agente"
            asegurar falla { sea x = lecciones() }, "lecciones(Mostrador)"
            asegurar falla { aprender("algo", 5) }, "espera un agente"
        }
    """
    codigo, salida, err = por_main(tmp_path, capsys, programa, orden="probar")
    assert (codigo, err) == (0, ""), salida
    assert "4 de 4 pruebas pasaron" in salida
    assert archivos_de(tmp_path) == ["programa.mate"]
    # fuera de una prueba, consultas_ia() se avisa antes de correr
    error = falla(APRENDIZ + "mostrar(consultas_ia())")
    assert error.antes_de_correr and error.mensaje == mate.CONSULTAS_IA_SUELTO
    # y dentro de un agente cada uno aprende solo lo suyo
    _, interprete = correr(APRENDIZ + """
        mensaje Mal {}
        agente Otro { al recibir Mal { aprender("algo", Mostrador) } }
        enviar Mal {} a Otro
    """)
    assert "dentro de un agente va sin decir a cuál" in interprete.errores_agentes[0]


def test_el_ejemplo_del_agente_que_aprende(tmp_path, capsys, ia):
    import shutil
    original = RAIZ / "ejemplos" / "08_agente_que_aprende.mate"
    en_la_carpeta = archivos_de(RAIZ / "ejemplos")
    assert not [a for a in en_la_carpeta if a.endswith((".json", ".txt", ".tmp"))]
    codigo, salida, _ = orden_mate(capsys, "probar", original)
    assert codigo == 0 and "4 de 4 pruebas pasaron" in salida and ia.pedidos == []
    assert archivos_de(RAIZ / "ejemplos") == en_la_carpeta  # 'probar' no deja nada
    ruta = shutil.copy(original, tmp_path / original.name)
    codigo, salida, err = orden_mate(capsys, "correr", ruta, "--ia-simulada")
    assert (codigo, err) == (0, "") and ia.pedidos == []
    assert salida.splitlines() == [
        "Marta: ¿Me mandan 5 paquetes de yerba a casa?",
        "Mostrador: ¡Hola! Ya te lo averiguo.",
        "Clientes atendidos hasta hoy, contando las otras veces que corrió: 1",
        "Lecciones que tiene el Mostrador: 1",
        "  - Los domingos el almacén está cerrado."]
    assert "hasta hoy, contando las otras veces que corrió: 2" in orden_mate(
        capsys, "correr", ruta, "--ia-simulada")[1]
    # el paso 2 de los comentarios: corregirlo desde afuera
    leccion = "Si piden menos de 10 unidades, avisá que no hay envío."
    assert leccion in original.read_text(encoding="utf-8")
    assert orden_mate(capsys, "corregir", ruta, "Mostrador", leccion)[0] == 0
    ia.respuestas = [dice("Por 5 paquetes no hacemos envío.")]
    codigo, salida, err = orden_mate(capsys, "correr", ruta)
    assert "Mostrador: Por 5 paquetes no hacemos envío." in salida
    assert ": 3\n" in salida and "Lecciones que tiene el Mostrador: 2" in salida
    assert ia.pedidos[0]["cuerpo"]["system"].endswith(
        "LECCIONES APRENDIDAS (correcciones que te hicieron antes: tenelas siempre en cuenta)\n"
        f"1. Los domingos el almacén está cerrado.\n2. {leccion}")
    assert archivos_de(tmp_path) == [original.name, "08_agente_que_aprende.memoria.json"]
    # todas las órdenes que nombran sus comentarios existen
    comentarios = original.read_text(encoding="utf-8")
    for orden in ["corregir mate\\ejemplos", "lecciones mate\\ejemplos", "--borrar=1",
                  "bitacora mate\\ejemplos", "--olvidar", "--ia-simulada --traza"]:
        assert orden in comentarios, orden


def test_el_readme_la_guia_y_la_ayuda_cuentan_lo_de_la_0_4(capsys):
    leeme = (RAIZ / "README.md").read_text(encoding="utf-8")
    for frase in ["## Mate aprende", "3. **Aprender de sus errores.**",
                  "estado recordado atendidos = 0", "mi_mostrador.memoria.json",
                  "mi_mostrador.bitacora.txt", "| `--olvidar` |", "| `bitacora archivo.mate` |",
                  '| `corregir archivo.mate Mostrador "..."` |', "| `lecciones archivo.mate` |",
                  "--borrar=2", "`08_agente_que_aprende.mate`", mate.TITULO_DE_LECCIONES,
                  'aprender("No hay envío por menos de 10", Mostrador)', "consultas_ia()",
                  f"{mate.MAX_LECCIONES} lecciones", f"{mate.LARGO_DE_LECCION} letras",
                  f"últimas {mate.MAX_BITACORA}", "Con `probar` nada de esto se lee ni se guarda",
                  "`aprender`, `lecciones` y `consultas_ia` son funciones incluidas",
                  "el tope se subió a 45"]:
        assert frase in leeme, frase
    guia = mate.texto_de_guia()
    for frase in ["estado recordado atendidos = 0", "programa.memoria.json", "--olvidar",
                  'aprender("texto", Mostrador)', "consultas_ia() da la", "programa.bitacora.txt",
                  'corregir programa.mate Agente "texto"']:
        assert frase in guia, frase
    ayuda = mate.texto_de_ayuda()
    for frase in ["corregir  archivo.mate Mostrador", "lecciones archivo.mate",
                  "bitacora  archivo.mate", "--olvidar", "--borrar=2"]:
        assert frase in ayuda, frase
    assert "estado recordado atendidos = 0" in mate.ayuda_de("recordado")
    assert "función incluida" in mate.ayuda_de("aprender")
    assert mate.main(["ayuda", "bitacora"]) == 0 and "Órdenes:" in capsys.readouterr().out
    mejoras = (RAIZ / "MEJORAS.md").read_text(encoding="utf-8")
    seccion = mejoras.split("\n## Lo que vino después de las 100\n")[1].split("\n## ")[0]
    for frase in ["**101. Memoria de agente", "**102. Bitácora de errores", "**103. Lecciones",
                  "Nota de lo decidido"]:
        assert frase in seccion, frase
    # (101 a 103, y 104 a 108: el registro de uso; después vinieron las de la 0.5)
    assert seccion.count("Estado: hecha") >= 8


# ── 0.4, segunda parte: el lenguaje anota sus errores de uso para seguir mejorando ──

def renglones_anotados(registro):
    """Los renglones del registro de errores de uso, cada uno partido en sus siete partes."""
    if not registro.exists():
        return []
    texto = registro.read_text(encoding="utf-8-sig")
    return [r.split(" | ") for r in texto.splitlines() if r and not r.startswith("#")]


@pytest.fixture
def con_registro(tmp_path, monkeypatch, capsys):
    """Corre Mate como desde la línea de comandos, anotando en un registro de mentira.
    Devuelve (función que corre y da (código, salida, errores), ruta del registro)."""
    monkeypatch.delenv("MATE_SIN_REGISTRO", raising=False)
    registro = tmp_path / "registro" / "errores_de_uso.txt"
    registro.parent.mkdir()

    def correr_mate(*args, **mas):
        capsys.readouterr()
        codigo = mate.main([str(a) for a in args], registro=mas.get("registro", registro))
        capturado = capsys.readouterr()
        return codigo, capturado.out, capturado.err

    return correr_mate, registro


def test_cada_error_mostrado_deja_un_renglon_en_el_registro(tmp_path, con_registro):
    correr_mate, registro = con_registro
    bien = tmp_path / "bien.mate"
    bien.write_text('mostrar("hola")\n', encoding="utf-8")
    assert correr_mate("correr", bien) == (0, "hola\n", "")
    assert not registro.exists()  # lo que sale bien no anota nada, ni crea el archivo
    mal = tmp_path / "mi_secreto.mate"
    mal.write_text('sea total = 5\nmostrar(totl)\nmostrar(otro)\n', encoding="utf-8")
    codigo, out, err = correr_mate("correr", mal, "--traza")
    assert codigo == 1 and "no existe 'totl'. ¿Quisiste decir 'total'?" in err
    [(fecha, version, orden, categoria, sugerencia, seguidas, mensaje)] = \
        renglones_anotados(registro)
    assert re.fullmatch(r"\d\d/\d\d/\d{4} \d\d:\d\d", fecha)
    assert version == f"Mate {mate.VERSION}" and orden == "correr --traza"
    assert categoria == "antes de correr: no existe '<nombre>'"
    assert (sugerencia, seguidas) == ("con sugerencia", "1 vez")
    assert mensaje == ("no existe '<nombre>'. ¿Quisiste decir '<nombre>'? "
                       "(y 1 error(es) más en la misma corrida)")
    # ni el nombre del archivo, ni la carpeta, ni el contenido del programa
    todo = registro.read_text(encoding="utf-8-sig")
    for dato in ["mi_secreto", str(tmp_path), "totl", "total = 5", "mostrar(otro)"]:
        assert dato not in todo, dato
    # arriba dice qué es, que no sale de la computadora y cómo se apaga
    assert todo.startswith("# Registro de errores de uso de Mate")
    for frase in ["Mate no lo manda a ningún lado", "No guarda tus programas",
                  "informe --borrar", "MATE_SIN_REGISTRO", "--sin-registro"]:
        assert frase in todo, frase
    # al lado del registro no queda nada más, y en la carpeta del programa nada nuevo
    assert [a.name for a in registro.parent.iterdir()] == ["errores_de_uso.txt"]
    assert sorted(a.name for a in tmp_path.iterdir()) == [
        "bien.mate", "mi_secreto.mate", "registro"]


def test_el_registro_dice_en_que_etapa_fue_cada_error(tmp_path, con_registro):
    correr_mate, registro = con_registro

    def anotado(fuente, orden="correr", *opciones):
        archivo = tmp_path / "programa.mate"
        archivo.write_text(fuente, encoding="utf-8")
        correr_mate(orden, archivo, *opciones)
        return renglones_anotados(registro)[-1]

    assert anotado('sea x = (1 + \n')[3].startswith("al leer el programa: ")
    assert anotado('mostrar(nada_de_esto)', "verificar")[2:4] == [
        "verificar", "antes de correr: no existe '<nombre>'"]
    renglon = anotado('mostrar("Marta Gómez" + 1)')
    assert renglon[3] == "al correr: no se puede hacer texto + numero"
    assert "Marta" not in " ".join(renglon)
    # lo que el programa dice con 'fallar' o con 'asegurar' es de la persona: no se guarda
    renglon = anotado('fallar "No hay yerba para Marta Gómez"')
    assert renglon[3:] == ["al correr: el programa cortó con 'fallar'", "sin sugerencia",
                           "1 vez", "<lo que el programa dijo con 'fallar'>"]
    renglon = anotado('asegurar 1 == 2, "la cuenta de Marta"')
    assert renglon[3] == "al correr: no se cumplió un 'asegurar'" and "Marta" not in renglon[6]
    renglon = anotado("""
        mensaje Consulta { cliente: texto }
        agente Mostrador {
            al recibir Consulta como c { fallar "Sin stock para {c.cliente}" }
        }
        enviar Consulta { cliente: "Marta Gómez" } a Mostrador
    """)
    assert renglon[3] == "al correr, en un agente: el programa cortó con 'fallar'"
    assert "Marta" not in " ".join(renglon) and "Mostrador" not in " ".join(renglon)
    renglon = anotado("""
        mensaje Consulta { cliente: texto }
        agente Mostrador {
            al recibir Consulta como c { mostrar(c.cliente + 1) }
        }
        enviar Consulta { cliente: "Marta Gómez" } a Mostrador
    """)
    assert renglon[3] == "al correr, en un agente: no se puede hacer texto + numero"
    assert "Mostrador" not in renglon[6] and "Consulta" not in renglon[6]


def test_los_errores_de_la_linea_de_comandos_tambien_se_anotan(tmp_path, con_registro):
    correr_mate, registro = con_registro
    ok = tmp_path / "lista de marta.mate"
    ok.write_text('mostrar("ok")', encoding="utf-8")
    assert correr_mate("corer", ok)[0] == 2
    assert correr_mate("correr", ok, "--trasa")[0] == 2
    assert correr_mate("correr", ok, "--inventada")[0] == 2
    assert correr_mate("correr")[0] == 2
    assert correr_mate("correr", tmp_path / "no_esta.mate")[0] == 2
    assert correr_mate("correr", ok, ok)[0] == 2
    assert correr_mate(ok, "probar")[0] == 2
    assert correr_mate("lecciones", ok, "Fulano")[0] == 2
    renglones = renglones_anotados(registro)
    assert [(r[2], r[3], r[4]) for r in renglones] == [
        ("(orden desconocida)", "al escribir la orden: orden que no existe", "con sugerencia"),
        ("correr", "al escribir la orden: opción que no existe", "con sugerencia"),
        ("correr", "al escribir la orden: opción que no existe", "sin sugerencia"),
        ("correr", "al escribir la orden: falta el archivo", "sin sugerencia"),
        ("correr", "al escribir la orden: no está el archivo", "sin sugerencia"),
        ("correr", "al escribir la orden: más de un archivo", "sin sugerencia"),
        ("correr", "al escribir la orden: el archivo antes que la orden", "con sugerencia"),
        ("lecciones", "al escribir la orden: <dato> no tiene un agente '<nombre>'",
         "sin sugerencia"),
    ]
    assert renglones[0][6] == "no conozco la orden '<nombre>', ¿quisiste decir 'correr'?"
    assert renglones[1][6] == "no conozco la opción --<opción>, ¿quisiste decir --traza?"
    todo = registro.read_text(encoding="utf-8-sig")
    for dato in ["marta", "corer", "trasa", "inventada", "no_esta", "Fulano", str(tmp_path)]:
        assert dato not in todo, dato
    # la ayuda sola, una versión, un programa sin errores: nada
    antes = len(renglones)
    assert correr_mate()[0] == 2 and correr_mate("ayuda")[0] == 0
    assert correr_mate("correr", ok)[0] == 0
    assert len(renglones_anotados(registro)) == antes


def test_tapar_datos_no_deja_pasar_nada_de_la_persona(monkeypatch):
    monkeypatch.setenv("USERNAME", "Federico")
    monkeypatch.setenv("ANTHROPIC_API_KEY", CLAVE_DE_MENTIRA)
    casos = {
        'no pude abrir C:\\Users\\Federico\\Mis Cosas\\lista de precios.mate: no tengo permiso':
            "no pude abrir <ruta>: no tengo permiso",
        "no encuentro 'x.mate' en /home/federico/mis cosas\narchivos .mate que sí hay ahí: "
        "a.mate, precios 2026.mate":
            "no encuentro '<nombre>' en <ruta> archivos .mate que sí hay ahí: <archivo>, "
            "precios <archivo>",
        'Pedido.cliente espera texto y recibió numero (44445555), venía "Marta"':
            'Pedido.cliente espera texto y recibió numero (<número>), venía "<texto>"',
        f"la IA dijo que la clave {CLAVE_DE_MENTIRA} no sirve": None,
        "la clave sk-ant-api03-OtraClaveDistinta123 y el token a1B2c3D4e5F6g7H8i9J0k1L2m3N4":
            "la clave <clave> y el token <clave>",
        "escribile a marta.gomez@ejemplo.com.ar o mirá https://ejemplo.com/a?b=1 ya":
            "escribile a <correo> o mirá <dirección> ya",
        "a 'si' le falta la condición, y 'Mostrador' no existe; el usuario federico":
            "a 'si' le falta la condición, y '<nombre>' no existe; el usuario <usuario>",
        'el texto """varios\nrenglones de Marta""" y «otro» más':
            'el texto "<texto>" y "<texto>" más',
        "mapa no tiene un campo 'dni' (tiene: nombre, telefono)":
            "mapa no tiene un campo '<nombre>' (tiene: <nombres>)",
        "no conozco la opción --secreta=clave.txt ni -x, sí --traza=charla.txt":
            "no conozco la opción --<opción>=<valor> ni --<opción>, sí --traza=<valor>",
        "un | suelto": "un / suelto",
    }
    for mensaje, esperado in casos.items():
        tapado = mate.tapar_datos(mensaje)
        assert "\n" not in tapado and CLAVE_DE_MENTIRA not in tapado
        if esperado is not None:
            assert tapado == esperado
    # lo que la persona escribió en la orden se tapa donde aparezca
    assert mate.tapar_datos("Fulano no tiene lecciones en ventas",
                            ["corregir", "C:\\datos\\ventas.mate", "Fulano"]) == \
        "<dato> no tiene lecciones en <dato>"
    assert len(mate.tapar_datos("palabra " * 200)) <= 303
    # la categoría no lleva números ni lo que sigue al primer punto
    assert mate.categoria_de("al correr", "la posición 5 está fuera de rango: la lista "
                             "tiene 2") == "al correr: la posición N está fuera de rango"


def test_el_mismo_error_seguido_queda_marcado(tmp_path, con_registro, monkeypatch):
    correr_mate, registro = con_registro
    mal = tmp_path / "mal.mate"
    mal.write_text("mostrar(totl)\n", encoding="utf-8")
    otro = tmp_path / "otro.mate"
    otro.write_text('mostrar("a" + 1)\n', encoding="utf-8")
    for _ in range(3):
        correr_mate("correr", mal)
    correr_mate("correr", otro)
    correr_mate("correr", mal)
    correr_mate("verificar", mal)  # el mismo error, con otra orden: empieza de nuevo
    assert [r[5] for r in renglones_anotados(registro)] == [
        "1 vez", "2 veces seguidas", "3 veces seguidas", "1 vez", "1 vez", "1 vez"]
    # "seguido" es dentro de un rato: al otro día ya no cuenta
    ahora = mate.datetime.datetime.now()
    for minutos, esperado in [(0, "2 veces seguidas"), (mate.MINUTOS_SEGUIDO - 1,
                                                        "3 veces seguidas"),
                              (mate.MINUTOS_SEGUIDO * 3, "1 vez")]:
        ahora += mate.datetime.timedelta(minutes=minutos)
        mate.anotar_error_de_uso(str(registro), "verificar", "antes de correr",
                                 "no existe 'x'", ahora=ahora)
        assert renglones_anotados(registro)[-1][5] == esperado


def test_el_registro_tiene_tope_y_no_se_rompe_con_un_archivo_editado(tmp_path, monkeypatch):
    registro = tmp_path / "errores_de_uso.txt"
    monkeypatch.setattr(mate, "MAX_REGISTRO", 5)
    for i in range(8):
        mate.anotar_error_de_uso(str(registro), "correr", "al correr", f"error número {i}0")
    renglones = renglones_anotados(registro)
    assert len(renglones) == 5 and renglones[-1][6] == "error número 70"
    # alguien lo edita a mano y deja renglones que no se entienden: no se pierden ni rompen
    with registro.open("a", encoding="utf-8") as f:
        f.write("esto lo escribí yo\n99/99/2026 | Mate | x | y | z | w | q\n")
    mate.anotar_error_de_uso(str(registro), "correr", "al correr", "uno más")
    entradas, crudos, raros = mate.entradas_del_registro(str(registro))
    assert (len(entradas), len(crudos), raros) == (3, 5, 2)
    assert entradas[-1]["mensaje"] == "uno más" and entradas[-1]["seguidas"] == 1
    assert not (tmp_path / "errores_de_uso.txt.tmp").exists()
    # guardado como lo guarda el Bloc de notas en "Unicode", se sigue leyendo
    registro.write_bytes(registro.read_text(encoding="utf-8-sig").encode("utf-16"))
    assert len(mate.entradas_del_registro(str(registro))[0]) == 3
    # si no se puede escribir (la carpeta no existe, o es un archivo), no molesta
    mate.anotar_error_de_uso(str(tmp_path / "no" / "hay" / "errores.txt"), "correr",
                             "al correr", "nada")
    (tmp_path / "soy_carpeta.txt").mkdir()
    mate.anotar_error_de_uso(str(tmp_path / "soy_carpeta.txt"), "correr", "al correr", "nada")
    assert sorted(a.name for a in tmp_path.iterdir()) == ["errores_de_uso.txt",
                                                         "soy_carpeta.txt"]


def test_un_registro_que_no_se_puede_escribir_no_cambia_nada(tmp_path, con_registro,
                                                             monkeypatch):
    correr_mate, registro = con_registro
    mal = tmp_path / "mal.mate"
    mal.write_text("mostrar(totl)\n", encoding="utf-8")
    con = correr_mate("correr", mal)

    def no_se_puede(*_a, **_k):
        raise PermissionError("carpeta de solo lectura")

    monkeypatch.setattr(mate, "escribir_entero", no_se_puede)
    assert correr_mate("correr", mal) == con  # mismo código, misma salida, ni un aviso
    assert len(renglones_anotados(registro)) == 1


def test_el_registro_se_apaga_y_no_anota_con_probar_ni_como_modulo(tmp_path, con_registro,
                                                                  monkeypatch, capsys):
    correr_mate, registro = con_registro
    mal = tmp_path / "mal.mate"
    mal.write_text("mostrar(totl)\n", encoding="utf-8")
    con_fallas = tmp_path / "fallas.mate"
    con_fallas.write_text('prueba "no da" { asegurar 1 == 2 }\n', encoding="utf-8")
    # la orden 'probar' no toca el registro: ni con un programa mal escrito ni con pruebas
    # que fallan ni con una carpeta
    assert correr_mate("probar", mal)[0] == 1
    assert correr_mate("probar", con_fallas)[0] == 1
    assert correr_mate("probar", tmp_path)[0] == 1
    assert correr_mate("probar")[0] == 2
    # usado como módulo (sin decirle dónde anotar) tampoco
    assert mate.main(["correr", str(mal)]) == 1
    assert mate.main(["correr", str(mal)], registro=None) == 1
    # con la opción y con la variable, apagado
    assert correr_mate("correr", mal, "--sin-registro")[0] == 1
    assert correr_mate("correr", mal, "--SIN-REGISTRO")[0] == 1
    for valor in ["1", "si", "cualquier cosa"]:
        monkeypatch.setenv("MATE_SIN_REGISTRO", valor)
        assert mate.registro_apagado() and correr_mate("correr", mal)[0] == 1
    assert not registro.exists()
    for valor in ["", "0", "no"]:
        monkeypatch.setenv("MATE_SIN_REGISTRO", valor)
        assert not mate.registro_apagado()
    # dentro de una corrida de pytest, la línea de comandos de verdad (registro=True) no anota
    monkeypatch.delenv("MATE_SIN_REGISTRO")
    assert "PYTEST_CURRENT_TEST" in os.environ
    assert mate.donde_se_registra(True, []) is None
    monkeypatch.delenv("PYTEST_CURRENT_TEST")
    assert mate.donde_se_registra(True, []) == str(RAIZ / "errores_de_uso.txt")
    assert mate.donde_se_registra(True, ["correr", "--sin-registro"]) is None
    assert mate.ruta_del_registro() == str(RAIZ / "errores_de_uso.txt")
    capsys.readouterr()


def test_mate_corrido_como_programa_anota_al_lado_de_mate_py(tmp_path):
    """La línea de comandos de verdad, con una copia de mate.py en una carpeta temporal."""
    (tmp_path / "mate").mkdir()
    (tmp_path / "mate" / "mate.py").write_bytes((RAIZ / "mate.py").read_bytes())
    (tmp_path / "programas").mkdir()
    mal = tmp_path / "programas" / "mal.mate"
    mal.write_text("mostrar(totl)\n", encoding="utf-8")
    registro = tmp_path / "mate" / "errores_de_uso.txt"
    entorno = {k: v for k, v in os.environ.items()
               if k not in ("PYTEST_CURRENT_TEST", "MATE_SIN_REGISTRO")}
    entorno["PYTHONIOENCODING"] = "utf-8"
    entorno["PYTHONDONTWRITEBYTECODE"] = "1"

    def correr_mate(*args, **mas):
        return subprocess.run([sys.executable, str(tmp_path / "mate" / "mate.py"), *args],
                              capture_output=True, encoding="utf-8", cwd=tmp_path / "programas",
                              env=dict(entorno, **mas))

    # dentro de pytest, o con la variable, nada
    assert correr_mate("correr", "mal.mate", PYTEST_CURRENT_TEST="x").returncode == 1
    assert correr_mate("correr", "mal.mate", MATE_SIN_REGISTRO="1").returncode == 1
    assert correr_mate("probar", "mal.mate").returncode == 1
    assert correr_mate("correr", "mal.mate", "--sin-registro").returncode == 1
    assert not registro.exists()
    r = correr_mate("correr", "mal.mate")
    assert r.returncode == 1 and r.stdout == ""
    assert r.stderr == "mal.mate:1: error: no existe 'totl'\n    1 | mostrar(totl)\n"
    r = correr_mate("correr", "mal.matepython", "mate.py", "correr", "mal.mate")
    assert r.returncode == 2 and "se pegó dos veces" in r.stderr
    assert [renglon[3] for renglon in renglones_anotados(registro)] == [
        "antes de correr: no existe '<nombre>'",
        "al escribir la orden: comando pegado dos veces"]
    # la carpeta del programa queda como estaba, y al lado de mate.py solo el registro
    assert [a.name for a in (tmp_path / "programas").iterdir()] == ["mal.mate"]
    assert sorted(a.name for a in (tmp_path / "mate").iterdir()) == [
        "errores_de_uso.txt", "mate.py"]
    r = correr_mate("informe")
    assert r.returncode == 0 and "Hay 2 error(es) de uso anotado(s)" in r.stdout
    assert str(registro) in r.stdout
    assert correr_mate("informe", "--borrar").returncode == 0 and not registro.exists()


def test_el_registro_no_se_sube_y_las_pruebas_no_lo_tocan():
    ignorados = (RAIZ / ".gitignore").read_text(encoding="utf-8").split()
    assert "errores_de_uso.txt" in ignorados and "errores_de_uso.txt.tmp" in ignorados
    assert mate.NOMBRE_DEL_REGISTRO == "errores_de_uso.txt"
    assert os.environ.get("MATE_SIN_REGISTRO") == "1"  # (lo pone sin_red_ni_clave)


def test_un_error_interno_de_mate_tambien_se_anota(tmp_path, con_registro, monkeypatch):
    correr_mate, registro = con_registro
    archivo = tmp_path / "x.mate"
    archivo.write_text('mostrar("dato de Marta")\n', encoding="utf-8")

    def rota(*_a, **_k):
        raise ZeroDivisionError("dato de Marta")

    monkeypatch.setattr(mate, "verificar", rota)
    codigo, _, err = correr_mate("correr", archivo)
    assert codigo == 1 and "error interno de Mate" in err
    [renglon] = renglones_anotados(registro)
    assert renglon[3] == "por dentro de Mate: error interno (ZeroDivisionError)"
    assert renglon[6] == "error interno de Mate"  # (sin el detalle: puede traer datos)


def test_la_consola_anota_sus_errores(tmp_path, con_registro, monkeypatch, capsys):
    correr_mate, registro = con_registro
    renglones = iter(["mostrar(zzz)", 'fallar "secreto de Marta"', "sea x = 1sea x = 1",
                      "sea x = 1", "mostrar(x)", "salir"])
    monkeypatch.setattr("builtins.input", lambda _="": next(renglones))
    codigo, out, _ = correr_mate("consola")
    assert codigo == 0 and out.splitlines()[-1] == "1"
    assert [(r[2], r[3], r[6]) for r in renglones_anotados(registro)] == [
        ("consola", "en la consola: no existe '<nombre>'", "no existe '<nombre>'"),
        ("consola", "en la consola: el programa cortó con 'fallar'",
         "<lo que el programa dijo con 'fallar'>"),
        ("consola", "en la consola: renglón pegado dos veces",
         "parece que el renglón se pegó dos veces (y Mate mostró el renglón bien escrito)"),
    ]


# La orden 'informe'

def test_informe_resume_el_registro(tmp_path, con_registro):
    correr_mate, registro = con_registro
    codigo, out, err = correr_mate("informe")
    assert codigo == 0 and err == "" and "Todavía no hay errores de uso anotados." in out
    assert "Nada de eso sale por internet" in out and str(registro) in out
    assert not registro.exists()  # mirar el informe no crea el archivo
    mal = tmp_path / "mal.mate"
    mal.write_text("mostrar(totl)\n", encoding="utf-8")
    otro = tmp_path / "otro.mate"
    otro.write_text('sea total = 1\nmostrar(totl)\n', encoding="utf-8")
    for _ in range(3):
        correr_mate("correr", mal)
    correr_mate("corer", mal)
    correr_mate("verificar", otro)
    correr_mate("correr", tmp_path / "nohay.mate")
    antes = registro.read_bytes()
    codigo, out, err = correr_mate("informe")
    assert codigo == 0 and err == ""
    assert registro.read_bytes() == antes  # el informe solo lee
    renglones = out.splitlines()
    assert renglones[0] == "Informe de errores de uso de Mate"
    assert re.fullmatch(r"Hay 6 error\(es\) de uso anotado\(s\), del \d\d/\d\d/\d{4} \d\d:\d\d "
                        r"al \d\d/\d\d/\d{4} \d\d:\d\d \(Mate 0\.5\)\.", renglones[1])
    assert renglones[3:6] == [
        "Los más frecuentes:",
        "    4 veces  antes de correr: no existe '<nombre>'",
        "             el mensaje: no existe '<nombre>'. ¿Quisiste decir '<nombre>'?"]
    assert "    1 vez   al escribir la orden: orden que no existe" in renglones
    seguidos = renglones.index("Los que se repitieron seguido (la persona volvió a intentar "
                               "y le salió el mismo error: el mensaje no alcanzó):")
    assert renglones[seguidos + 1:seguidos + 3] == [
        "  hasta 3 veces seguidas (2 repetición(es) en total)  antes de correr: no existe "
        "'<nombre>'", ""]
    assert 'Con sugerencia de Mate (un "¿quisiste decir...?" o el comando bien escrito): ' \
           "2 de 6." in renglones
    sin = renglones.index("Los más frecuentes que no traían ninguna sugerencia:")
    assert renglones[sin + 1] == "    1 vez   al escribir la orden: no está el archivo"
    assert "Con qué orden pasaron: correr 4, (orden desconocida) 1, verificar 1" in renglones
    assert f"Está todo en {registro} (se abre con el Bloc de notas; no sale de esta " \
           "computadora)." in renglones
    assert any("informe --para-mejorar" in r for r in renglones[-3:])
    assert any("informe --borrar" in r for r in renglones[-3:])
    # un renglón roto a mano se cuenta aparte
    with registro.open("a", encoding="utf-8") as f:
        f.write("esto no es un renglón del registro\n")
    out = correr_mate("informe")[1]
    assert "(1 renglón(es) del archivo no tienen la forma de siempre y no los conté)" in out
    # y un archivo que solo tiene renglones rotos no rompe nada
    registro.write_text("cualquier | cosa\n\n", encoding="utf-8")
    codigo, out, err = correr_mate("informe")
    assert codigo == 0 and "tiene 1 renglón(es) que no entiendo" in out
    # con el registro apagado se puede mirar igual, y lo dice
    registro.write_bytes(antes)
    correr_mate("informe")
    assert correr_mate("informe", "--sin-registro")[0] == 0
    assert registro.read_bytes() == antes


def test_informe_para_mejorar_arma_el_pedido(tmp_path, con_registro):
    correr_mate, registro = con_registro
    mal = tmp_path / "ventas de marta.mate"
    mal.write_text('mostrar("Marta" + 1)\n', encoding="utf-8")
    correr_mate("correr", mal)
    correr_mate("correr", mal)
    codigo, out, err = correr_mate("informe", "--para-mejorar")
    assert codigo == 0 and err == ""
    assert out.startswith("(Copiá desde el renglón de abajo hasta el final")
    for frase in [f"Uso Mate (versión {mate.VERSION})", "un solo archivo de Python",
                  "Hay 2 error(es) de uso anotado(s)",
                  "    2 veces  al correr: no se puede hacer texto + numero",
                  "hasta 2 veces seguidas",
                  "Con estos datos te pido propuestas concretas para mejorar Mate:",
                  "escribí el mensaje nuevo completo", "¿Cuál conviene arreglar primero",
                  "Mate tiene que seguir siendo chico"]:
        assert frase in out, frase
    # es para pegarle a otro: ni la carpeta, ni el archivo, ni los datos
    for dato in [str(tmp_path), "marta", "Marta", "Está todo en"]:
        assert dato not in out, dato
    # sin datos no hay pedido que armar
    correr_mate("informe", "--borrar")
    assert "Todavía no hay errores de uso anotados." in correr_mate(
        "informe", "--para-mejorar")[1]


def test_informe_borrar_y_sus_errores(tmp_path, con_registro):
    correr_mate, registro = con_registro
    ok = tmp_path / "ok.mate"
    ok.write_text('mostrar("ok")', encoding="utf-8")
    assert correr_mate("informe", "--borrar") == (
        0, "No hay registro de errores de uso para borrar.\n", "")
    correr_mate("corer", ok)
    assert registro.exists()
    codigo, out, err = correr_mate("informe", "--borrar")
    assert codigo == 0 and err == "" and out.startswith("Borrado el registro de errores de uso")
    assert not registro.exists()
    correr_mate("corer", ok)
    assert correr_mate("INFORME", "--borrar=todo")[0] == 0 and not registro.exists()
    # lo que no va
    codigo, _, err = correr_mate("informe", ok)
    assert codigo == 2 and "'informe' va sola" in err
    codigo, _, err = correr_mate("informe", "--borrar=2")
    assert codigo == 2 and "con 'informe', --borrar va sola" in err
    codigo, _, err = correr_mate("correr", ok, "--para-mejorar")
    assert codigo == 2 and "--para-mejorar va con 'informe'" in err
    # --borrar sola sigue sin ir con las otras órdenes, y con las lecciones lleva el número
    for orden in (["correr", ok], ["lecciones", ok, "Mostrador"]):
        codigo, _, err = correr_mate(*orden, "--borrar")
        assert codigo == 2 and "a --borrar le falta el número de la lección" in err
    assert correr_mate("informes")[2] == "no conozco la orden 'informes', ¿quisiste decir " \
                                         "'informe'?\n"
    assert correr_mate("ayuda", "informe")[1].startswith(f"Mate {mate.VERSION}")


# Las mejoras que salieron del uso real

PEGADOS = [
    (["correr", "mio.matepython", "mate\\mate.py", "correr", "mio.mate"],
     "python mate\\mate.py correr mio.mate"),
    (["--trazapython", "mate\\mate.py", "correr", "mio.mate", "--traza"],
     "python mate\\mate.py correr mio.mate --traza"),
    (["probar", "mate\\ejemplospy", "-3", "mate\\mate.py", "probar", "mate\\ejemplos"],
     "py -3 mate\\mate.py probar mate\\ejemplos"),
    (["correr", "mio.matemate", "correr", "mio.mate"], "mate correr mio.mate"),
    (["correr", "mi lista.mate.\\mate.bat", "correr", "mi lista.mate"],
     '.\\mate.bat correr "mi lista.mate"'),
    (["guiapython3", "mate/mate.py", "guia"], "python3 mate/mate.py guia"),
    # tres veces
    (["correr", "a.matepython", "mate.py", "correr", "a.matepython", "mate.py", "correr",
      "a.mate"], "python mate.py correr a.mate"),
    # dos comandos distintos pegados: el último
    (["correr", "a.matepython", "mate\\mate.py", "verificar", "b.mate"],
     "python mate\\mate.py verificar b.mate"),
]


@pytest.mark.parametrize("argv,una_vez", PEGADOS)
def test_el_comando_pegado_dos_veces_lo_dice_y_muestra_el_bueno(argv, una_vez, capsys):
    assert mate.comando_pegado(argv) == una_vez
    assert mate.main(argv) == 2
    capturado = capsys.readouterr()
    assert capturado.out == "" and capturado.err == (
        "parece que el comando se pegó dos veces en el mismo renglón. Escribilo una sola "
        f"vez:\n  {una_vez}\n")


def test_lo_que_no_es_un_comando_pegado_sigue_como_antes(tmp_path, capsys):
    ok = tmp_path / "ok.mate"
    ok.write_text('mostrar("corrió")', encoding="utf-8")
    for argv in [["correr", str(ok)], ["correr", str(ok), str(ok)], ["ayuda", "ayuda"],
                 ["probar", str(ok), str(ok)], ["correr", "happy.mate", "mate.py"],
                 ["correr", str(ok), "--traza", "--traza"], ["lecciones", "a.mate", "a.mate"],
                 ["corregir", "a.mate", "Mostrador", "usá python y mate"], []]:
        assert mate.comando_pegado(argv) is None, argv
    assert mate.main(["correr", str(ok), str(ok)]) == 2
    assert "lleva un solo archivo y recibió 2" in capsys.readouterr().err
    assert mate.main(["correr", str(ok), "--trazapython"]) == 2
    assert capsys.readouterr().err == ("no conozco la opción --trazapython, ¿quisiste decir "
                                       "--traza?\n")


def test_en_la_consola_un_renglon_pegado_dos_veces_avisa(monkeypatch, capsys):
    assert mate.renglon_duplicado("sea x = 1sea x = 1") == "sea x = 1"
    assert mate.renglon_duplicado("  ayuda agenteayuda agente ") == "ayuda agente"
    assert mate.renglon_duplicado("mostrar(1)mostrar(1)mostrar(1)") == "mostrar(1)"
    for renglon in ["sea x = 1", "sea jaja = 1", "mostrar(1) mostrar(1)", "1111", "[1][1]",
                    "xx", "", "sea x = 1sea x = 2"]:
        assert mate.renglon_duplicado(renglon) is None, renglon
    renglones = iter(["sea x = 1sea x = 1", "ayuda agenteayuda agente", "sea x = 7",
                      "mostrar(x)", "python mate\\mate.py correr hola.mate",
                      "PS C:\\Users\\fede> python mate\\mate.py consola", "salir"])
    monkeypatch.setattr("builtins.input", lambda _="": next(renglones))
    assert mate.main(["consola"]) == 0
    assert capsys.readouterr().out.splitlines()[2:] == [
        "error: parece que el renglón se pegó dos veces. Escribilo una sola vez:  sea x = 1",
        "error: parece que el renglón se pegó dos veces. Escribilo una sola vez:  "
        "ayuda agente",
        "7",  # (el renglón pegado no corrió: x se declara recién acá)
        "error: eso es de PowerShell, y acá adentro (en la consola de Mate) van renglones "
        "de Mate. Para volver a PowerShell escribí salir, y pegá el comando allá",
        "error: eso es de PowerShell, y acá adentro (en la consola de Mate) van renglones "
        "de Mate. Para volver a PowerShell escribí salir, y pegá el comando allá",
    ]


def test_tres_comillas_de_mas_dice_cuantas_hay_y_donde(tmp_path, capsys):
    # se pegó un bloque dentro de otro: quedan cinco juegos de tres comillas
    fuente = (f'mostrar("hola")\nsea a = {TRES}\n  uno\n{TRES}\nsea b = {TRES}\n'
              f'  dos\nsea c = {TRES}\n  tres\n{TRES}\nmostrar(a)\n')
    error = falla(fuente)
    assert error.linea == 9
    assert error.mensaje == (
        mate.SIN_CERRAR_TEXTO + '. En este archivo hay 5 juegos de tres comillas ("""), en '
        "los renglones 2, 4, 5, 7 y 9: es una cantidad impar, y como van de a pares (uno "
        "abre y otro cierra) sobra o falta uno. Suele pasar al pegar un bloque dentro de "
        "otro. Leyendo de arriba para abajo, el que queda sin pareja es el del renglón 9, "
        "pero el que sobra o el que falta puede estar más arriba")
    codigo, out, err = por_main(tmp_path, capsys, fuente)
    assert codigo == 1 and out == "" and ":9: error: a este texto de varios renglones" in err
    assert "hay 5 juegos de tres comillas" in err and f"    9 | {TRES}" in err
    # dos en el mismo renglón se cuentan las dos, y una tira de seis son dos juegos
    assert "en los renglones 1, 1 y 2:" in falla(
        f'sea a = {TRES}uno{TRES}\nsea b = {TRES}\n dos').mensaje
    assert "hay 3 juegos de tres comillas" in falla(f'sea a = {TRES}{TRES}\nsea b = {TRES}x').mensaje
    # con un solo juego (falta el cierre y nada más) el mensaje es el de siempre
    assert falla(f"sea t = {TRES}hola\nchau\n").mensaje == mate.SIN_CERRAR_TEXTO
    assert mate.comillas_de_mas(f"sea t = {TRES}hola", 1) == ""
    # con muchísimos, la lista se corta
    muchos = "".join(f"sea t{i} = {TRES}a{TRES}\n" for i in range(10)) + f"sea u = {TRES}\n"
    assert "en los renglones 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8...:" in falla(
        muchos).mensaje
    # los textos bien cerrados siguen andando, sean pares o impares los que hay adentro
    assert mostrados(f'sea a = {TRES}\n  uno\n  {TRES}\nmostrar(a)') == ["uno"]
    assert mostrados(f'mostrar({TRES}Ella dijo "hola"{TRES})') == ['Ella dijo "hola"']
    # en la consola un texto abierto sigue en el renglón de abajo, como siempre
    assert mate.falta_cerrar(f"sea t = {TRES}a{TRES}\nsea u = {TRES}") == "texto"


@pytest.mark.parametrize("primero,que", [
    ("PS C:\\Users\\fede> python mate\\mate.py correr mio.mate", "pantalla"),
    ("PS C:\\Users\\Juan Perez\\Desktop>", "pantalla"),
    ("  PS D:\\> notepad mio.mate", "pantalla"),
    ("python mate\\mate.py correr mio.mate", "comando"),
    ("python3 mate/mate.py probar mate/ejemplos", "comando"),
    ("py -3 mate\\mate.py correr mio.mate --traza", "comando"),
    ("Python.exe C:\\cosas\\mate\\mate.py verificar mio.mate", "comando"),
    ("notepad mio.mate", "comando"),
    (".\\mate correr mio.mate", "comando"),
    ("mate.bat probar mio.mate", "comando"),
    ("cd C:\\Users\\fede\\Desktop", "comando"),
])
def test_un_archivo_que_empieza_con_powershell_lo_dice(primero, que, tmp_path, capsys):
    assert mate.pegado_de_powershell(primero) == que
    fuente = f'\n\n{primero}\nmostrar("hola")\n'
    error = falla(fuente)
    assert error.linea == 3 and error.mensaje == mate.PEGADO_EN_EL_ARCHIVO[que]
    assert "este renglón no es de Mate" in error.mensaje
    assert "se pegó" in error.mensaje and "Bloc de notas" in error.mensaje
    codigo, out, err = por_main(tmp_path, capsys, fuente, orden="verificar")
    assert codigo == 1 and out == ""
    assert err.splitlines()[0].endswith(f"programa.mate:3: error: {error.mensaje}")
    assert err.splitlines()[1] == f"    3 | {primero.rstrip()}"


def test_lo_que_no_es_powershell_no_se_confunde(tmp_path, capsys):
    for renglon in ['mostrar("hola")', "sea cd = 5", "cd = 5", "sea python = 1",
                    "# python mate\\mate.py correr hola.mate", "sea ps = 3", "PS > 2",
                    'mostrar("PS C:\\\\Users> hola")', "mate", "py + 1", "notepad",
                    'sea mate = "correr"', "mostrar(python)", ""]:
        assert mate.pegado_de_powershell(renglon) is None, renglon
    # solo importa el primer renglón escrito: más abajo puede ser un texto que lo nombra
    fuente = f'sea ayuda = {TRES}\npython mate\\\\mate.py correr hola.mate\n{TRES}\nmostrar(ayuda)'
    assert mostrados(fuente) == ["python mate\\mate.py correr hola.mate"]
    # y también avisa en un archivo traído con 'usar'
    (tmp_path / "lib.mate").write_text("PS C:\\Users\\fede> dir\n", encoding="utf-8")
    codigo, _, err = por_main(tmp_path, capsys, 'usar "lib"\nmostrar(1)\n')
    assert codigo == 1 and "lib.mate:1: error: este renglón no es de Mate" in err


def test_el_readme_la_guia_y_la_ayuda_cuentan_el_registro_de_errores_de_uso(capsys):
    leeme = (RAIZ / "README.md").read_text(encoding="utf-8")
    for frase in ["### El lenguaje también aprende: el registro de errores de uso",
                  "`errores_de_uso.txt`", "**al lado de `mate.py`**",
                  "**No guarda tus programas**", "**Nunca sale de tu computadora.**",
                  "**Con `probar` no se anota nada**", '$env:MATE_SIN_REGISTRO = "1"',
                  "| `informe` |", "| `informe --para-mejorar` |", "| `informe --borrar` |",
                  "| `--sin-registro` |", f"últimos {mate.MAX_REGISTRO} renglones",
                  "parece que el comando se pegó dos veces en el mismo renglón",
                  "`sea x = 1sea x = 1`", "cantidad impar de `\"\"\"`", "`PS C:\\...>`"]:
        assert frase in leeme, frase
    ayuda = mate.texto_de_ayuda()
    for frase in ["  informe  ", "informe --para-mejorar", "informe --borrar",
                  "--sin-registro", "errores_de_uso.txt", "MATE_SIN_REGISTRO",
                  "no sale de esta computadora"]:
        assert frase in ayuda, frase
    for opcion in ["--para-mejorar", "--sin-registro"]:
        assert opcion in mate.OPCIONES
    guia = mate.texto_de_guia()
    assert "python mate\\mate.py informe" in guia and "--para-mejorar" in guia
    assert "una sola vez por renglón" in guia
    mejoras = (RAIZ / "MEJORAS.md").read_text(encoding="utf-8")
    seccion = mejoras.split("\n## Lo que vino después de las 100\n")[1].split("\n## ")[0]
    for frase in ["**104. Registro de errores de uso**", "**105. La orden `informe`**",
                  "**106. El comando pegado dos veces**", "**107. Tres comillas de más**",
                  "**108. La pantalla de PowerShell adentro del archivo**",
                  "**Nada sale de la computadora.**"]:
        assert frase in seccion, frase
    assert seccion.count("Nota de lo decidido") >= 8  # (de la 109 en adelante: la 0.5)


# ── Correcciones de la revisión de la 0.4 ──

def test_el_registro_tapa_un_dato_aunque_traiga_un_apostrofo(tmp_path, con_registro):
    for mensaje, tapado in [
        ("'O'Higgins 4500 depto 3' no es un número", "'<nombre>' no es un número"),
        ("'debe $ 5.000 a D'Angelo, Juan' no es un número", "'<nombre>' no es un número"),
        ("no pude abrir 'clientes D'Angelo Juan.mate'", "no pude abrir '<nombre>'"),
        ("no existe 'totl'. ¿Quisiste decir 'total'?",
         "no existe '<nombre>'. ¿Quisiste decir '<nombre>'?"),
        ("'x' no es un campo de 'D'Angelo'", "'<nombre>' no es un campo de '<nombre>'"),
        ("falta el 'al recibir' de 'Pedido'", "falta el 'al recibir' de '<nombre>'"),
        # una comilla que queda suelta: se tapa todo, de la primera a la última
        ("'D' Angelo Juan' no es un número", "'<texto>' no es un número"),
    ]:
        assert mate.tapar_datos(mensaje) == tapado, mensaje
    correr_mate, registro = con_registro
    programa = tmp_path / "q.mate"
    programa.write_text('mostrar(numero("O\'Higgins 4500 depto 3"))\n', encoding="utf-8")
    assert correr_mate("correr", programa)[0] == 1
    [renglon] = renglones_anotados(registro)
    assert renglon[3] == "al correr: '<nombre>' no es un número"
    assert renglon[6] == "'<nombre>' no es un número"
    assert "Higgins" not in registro.read_text(encoding="utf-8-sig")


def test_anotar_un_error_con_un_texto_enorme_no_tarda():
    import time
    for texto in ["'" + "a-b_c" * 300_000 + "' no es un número", "abcdefghij" * 100_000,
                  'x \\" ' * 100_000, "juan@" * 50_000, "'a' \"b' " * 50_000]:
        empezo = time.time()
        tapado = mate.tapar_datos(texto)
        assert time.time() - empezo < 2 and len(tapado) <= 303
    assert mate.tapar_datos("'" + "a-b_c" * 300_000 + "' no es un número") == \
        "'<nombre>' no es un número"
    # y lo que quedó cortado por la mitad no se escapa
    assert "Perez" not in mate.tapar_datos('dijo "' + "Juan Perez " * 1000)
    assert "Perez" not in mate.tapar_datos("'" + "Juan Perez " * 1000)


def test_ctrl_c_a_mitad_de_un_mensaje_no_guarda_lo_que_cambio_ese_mensaje(
        tmp_path, capsys, monkeypatch):
    import urllib.request

    def cortar(*_a, **_k):  # Ctrl+C mientras el agente espera a la IA
        raise KeyboardInterrupt

    monkeypatch.setattr(urllib.request, "urlopen", cortar)
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-clave-de-mentira-para-la-prueba")
    programa = """
        mensaje Hola {}
        mensaje Lento {}
        mensaje Pasar {}
        agente A {
            estado recordado n = 0
            al recibir Hola { n += 1
                responder n }
            al recibir Lento { n += 100
                sea x = consultar_ia("Contestá corto", "¿Seguimos?")
                responder n }
        }
        agente B {
            estado recordado veces = 0
            al recibir Pasar { veces += 1
                responder preguntar Lento {} a A }
        }
        mostrar(preguntar Hola {} a A)
        mostrar(preguntar Pasar {} a B)
    """
    codigo, salida, err = por_main(tmp_path, capsys, programa)
    assert (codigo, salida) == (130, "1\n") and "Ctrl+C" in err
    agentes = memoria_de(tmp_path)["agentes"]
    assert agentes["A"]["estado"] == {"n": 1}  # el +100 del mensaje cortado no queda
    assert agentes["B"]["estado"] == {"veces": 0}  # ni lo del que esperaba la respuesta


@pytest.mark.parametrize("fuente, mostrado", [
    ("sea aprender = 3\nmostrar(aprender)", ["3"]),
    ('sea lecciones = ["lunes", "martes"]\nmostrar(lecciones)', ['["lunes", "martes"]']),
    ("var consultas_ia = 1\nconsultas_ia += 1\nmostrar(consultas_ia)", ["2"]),
    ("funcion aprender(a, b, c) { devolver a + b + c }\nmostrar(aprender(1, 2, 3))", ["6"]),
    ("funcion f(lecciones, aprender) { devolver lecciones + aprender }\nmostrar(f(1, 2))", ["3"]),
    ("""mensaje Ver {}
        agente A {
            estado lecciones = [1]
            al recibir Ver { lecciones = agregar(lecciones, 2)
                responder lecciones }
        }
        mostrar(preguntar Ver {} a A)""", ["[1, 2]"]),
    ("para lecciones en [1, 2] { si lecciones > 1 { sea aprender = lecciones\n"
     "mostrar(aprender) } }", ["2"]),
])
def test_un_programa_de_antes_puede_usar_los_nombres_nuevos_de_la_04(
        fuente, mostrado, tmp_path, capsys):
    assert set(mate.SE_PUEDEN_TAPAR) == {"aprender", "lecciones", "consultas_ia", "leer_tabla",
                                         "agregar_a_archivo", "simular_teclado"}
    assert mostrados(fuente) == mostrado
    # y sigue sin crear ningún archivo: llamar a algo propio no es "usar lo de aprender"
    codigo, salida, err = por_main(tmp_path, capsys, fuente)
    assert (codigo, salida.split("\n")[:-1], err) == (0, mostrado, "")
    assert archivos_de(tmp_path) == ["programa.mate"]
    assert por_main(tmp_path, capsys, fuente, orden="probar")[0] == 0


def test_las_demas_funciones_incluidas_siguen_sin_poder_taparse():
    for nombre in ["texto", "largo", "consultar_ia", "simular_ia", "mostrar"]:
        assert f"'{nombre}' es una función incluida de Mate" in falla(f"sea {nombre} = 3").mensaje
    # y las tres de la 0.4 siguen siendo funciones para quien no les puso su nombre a nada
    assert "aprender() solo va dentro de un agente" in falla('aprender("x")').mensaje
    assert "lleva" in falla("mensaje V {}\nagente A { al recibir V { aprender() } }").mensaje
    assert "es una función incluida de Mate y no se le puede asignar" in \
        falla("lecciones = 3").mensaje


def test_un_mapa_recordado_vuelve_como_mapa_aunque_parezca_un_agente_o_un_mensaje(
        tmp_path, capsys):
    programa = """
        mensaje Hola { quien: texto }
        mensaje Pedido { n: numero }
        agente Vendedor {
            estado recordado mejor = {agente: "nadie"}
            estado recordado fichas = []
            estado recordado forma = {tipo: "Pedido", campos: {n: 1}}
            estado recordado envuelto = {mapa: {mapa: 1}}
            estado recordado pedido = Pedido { n: 1 }
            estado recordado n = 0
            al recibir Hola como h {
                n += 1
                mejor = {agente: h.quien}
                fichas = agregar(fichas, {agente: "Vendedor", ventas: n})
                fichas = agregar(fichas, {agente: "Vendedor"})
                responder [n, mejor, tipo(mejor), largo(fichas), tipo(fichas[1]), tipo(forma),
                           forma.campos.n, envuelto, tipo(pedido)]
            }
        }
        mostrar(preguntar Hola { quien: "Vendedor" } a Vendedor)
    """
    for vez in (1, 2, 3):
        codigo, salida, err = por_main(tmp_path, capsys, programa)
        assert (codigo, err) == (0, ""), err
        assert salida == (f'[{vez}, {{agente: "Vendedor"}}, "mapa", {vez * 2}, "mapa", "mapa", '
                          '1, {mapa: {mapa: 1}}, "Pedido"]\n')
    estado = memoria_de(tmp_path)["agentes"]["Vendedor"]["estado"]
    assert estado["mejor"] == {"agente": "Vendedor"} and len(estado["fichas"]) == 6
    assert estado["forma"] == {"mapa": {"tipo": "Pedido", "campos": {"n": 1}}}
    assert estado["pedido"] == {"tipo": "Pedido", "campos": {"n": 1}}
    # a_json y de_json siguen como estaban
    assert mostrados('mensaje P { n: numero }\nmostrar(a_json({tipo: "P", campos: {n: 1}}))\n'
                     'mostrar(tipo(de_json(a_json(P { n: 1 }))))') == [
        '{"tipo": "P", "campos": {"n": 1}}', "P"]


CAJA_QUE_RECUERDA = """
mensaje Suma { n: numero }
agente Caja {
    estado recordado total = 0
    al recibir Suma como s {
        total += s.n
        si s.n < 0 { fallar "número negativo" }
        responder lecciones()
    }
}
"""


def test_los_comandos_que_mate_sugiere_se_pueden_pegar_con_nombres_con_espacios(
        tmp_path, capsys):
    carpeta = tmp_path / "sub carpeta"
    carpeta.mkdir()
    programa = carpeta / "principal ñ.mate"
    programa.write_text(CAJA_QUE_RECUERDA + 'sea centro = crear Caja llamado "Centro"\n'
                        "enviar Suma { n: -1 } a Caja\n", encoding="utf-8")
    codigo, salida, _ = orden_mate(capsys, "lecciones", programa)
    assert codigo == 0 and f'corregir "{programa}" Caja "la lección"' in salida
    codigo, salida, _ = orden_mate(capsys, "corregir", programa, "Caja Centro", "para la copia")
    assert codigo == 0 and salida.splitlines()[-1].endswith(
        f'lecciones "{programa}" "Caja Centro" --borrar=1')
    # el nombre de la copia también vale en dos palabras, sin comillas
    codigo, salida, _ = orden_mate(capsys, "lecciones", programa, "Caja", "Centro", "--borrar=1")
    assert (codigo, salida) == (0, "Borrada. A Caja Centro le quedan 0 lección(es).\n")
    codigo, salida, _ = orden_mate(capsys, "corregir", programa, "Caja", "Centro", "ojo con esto")
    assert codigo == 0 and salida.startswith("Anotado. Caja Centro tiene 1 lección(es):\n"
                                             "  1. ojo con esto ")
    assert "Caja" not in memoria_de(carpeta, "principal ñ")["agentes"]
    # (si no hay una copia con ese nombre, es parte de la lección, como siempre)
    codigo, salida, _ = orden_mate(capsys, "corregir", programa, "Caja", "Cerrá", "temprano")
    assert codigo == 0 and "  1. Cerrá temprano " in salida
    assert mate.para_pegar("hola.mate") == "hola.mate" and mate.para_pegar("") == '""'
    # el encabezado de la bitácora trae el programa como se lo nombró al correrlo
    assert orden_mate(capsys, "correr", programa)[0] == 1
    encabezado = (carpeta / "principal ñ.bitacora.txt").read_text(encoding="utf-8-sig")
    assert f'bitacora "{programa}"\n' in encabezado
    sin_espacios = tmp_path / "caja.mate"
    sin_espacios.write_text(programa.read_text(encoding="utf-8"), encoding="utf-8")
    assert orden_mate(capsys, "correr", sin_espacios)[0] == 1
    assert f" bitacora {sin_espacios}\n" in \
        (tmp_path / "caja.bitacora.txt").read_text(encoding="utf-8-sig")


def test_la_memoria_es_del_programa_que_se_corre_y_se_avisa(tmp_path, capsys):
    agentes = tmp_path / "agentes míos.mate"
    agentes.write_text(CAJA_QUE_RECUERDA, encoding="utf-8")
    principal = tmp_path / "principal.mate"
    principal.write_text('usar "agentes míos.mate"\nmostrar(preguntar Suma { n: 1 } a Caja)\n',
                         encoding="utf-8")
    assert orden_mate(capsys, "correr", principal) == (0, "[]\n", "")  # sin nada raro, ni un aviso
    codigo, salida, _ = orden_mate(capsys, "corregir", agentes, "Caja", "una lección")
    assert codigo == 0 and "desde la próxima corrida de agentes míos.mate" in salida
    assert "son del programa que se corre" in salida
    codigo, salida, err = orden_mate(capsys, "correr", principal)
    assert (codigo, salida) == (0, "[]\n")
    assert err == ("aviso: agentes míos.mate tiene su propia memoria (agentes míos.memoria.json) "
                   "y acá no se usa: la memoria y las lecciones son del programa que se corre. "
                   "Para que a un agente le llegue una lección en este programa:  "
                   f'{mate.como_se_llama()} corregir {principal} Caja "la lección"\n')
    assert orden_mate(capsys, "corregir", principal, "Caja", "una lección")[0] == 0
    assert orden_mate(capsys, "correr", principal)[1] == '["una lección"]\n'
    leeme = (RAIZ / "README.md").read_text(encoding="utf-8")
    assert "**La memoria es del programa que corrés.**" in leeme
    assert '"Mostrador Centro"' in leeme


def test_un_argumento_vacio_al_final_no_es_un_comando_pegado(tmp_path, capsys):
    programa = tmp_path / "mi_mostrador.mate"
    programa.write_text(CAJA_QUE_RECUERDA, encoding="utf-8")
    assert mate.comando_pegado(["correr", str(programa), ""]) is None
    assert mate.comando_pegado(["corregir", "sub carpeta/principal ñ.mate", "Caja", ""]) is None
    codigo, _, err = orden_mate(capsys, "corregir", programa, "Caja", "")
    assert codigo == 2
    assert err == "la lección está vacía: escribí qué tiene que tener en cuenta el agente\n"
    codigo, _, err = orden_mate(capsys, "correr", programa, "")
    assert codigo == 2 and err.startswith("'correr' lleva un solo archivo y recibió 2")
    codigo, _, err = orden_mate(capsys, "lecciones", programa, "")
    assert codigo == 2 and "pegó dos veces" not in err
    # el comando pegado de verdad se sigue avisando
    assert mate.comando_pegado(["correr", "mio.matepython", "mate\\mate.py", "correr",
                                "mio.mate"]) == "python mate\\mate.py correr mio.mate"


def test_informe_avisa_si_hay_un_informe_mate_y_no_mezcla_borrar_con_para_mejorar(
        tmp_path, con_registro, monkeypatch):
    correr_mate, registro = con_registro
    monkeypatch.chdir(tmp_path)
    codigo, salida, err = correr_mate("informe")
    assert codigo == 0 and err == ""
    (tmp_path / "informe.mate").write_text('mostrar("soy informe")\n', encoding="utf-8")
    codigo, salida, err = correr_mate("informe")
    assert codigo == 0 and "Todavía no hay errores de uso anotados" in salida
    assert err == ("aviso: en esta carpeta hay un informe.mate, pero 'informe' sola es una orden "
                   "de Mate (muestra los errores de uso). Para correr tu programa:  "
                   f"{mate.como_se_llama()} correr informe.mate\n")
    assert correr_mate("correr", "informe.mate") == (0, "soy informe\n", "")
    (tmp_path / "lecciones.mate").write_text("mostrar(1)\n", encoding="utf-8")
    codigo, _, err = correr_mate("lecciones")
    assert codigo == 2 and "para correrlo, correr lecciones.mate" in err
    leeme = (RAIZ / "README.md").read_text(encoding="utf-8")
    assert "`bitacora`, `corregir`, `lecciones` e `informe` son órdenes" in leeme
    # --para-mejorar y --borrar juntas: no se borra nada
    assert correr_mate("correr", "no_esta.mate")[0] == 2
    antes = registro.read_bytes()
    for opciones in (["--para-mejorar", "--borrar"], ["--borrar", "--para-mejorar"]):
        codigo, salida, err = correr_mate("informe", *opciones, registro=None)
        assert (codigo, salida) == (2, "")
        assert "--para-mejorar y --borrar no van juntas, y no borré nada" in err
    assert registro.read_bytes() == antes
    assert correr_mate("informe", "--borrar")[0] == 0 and not registro.exists()


def test_olvidar_con_la_memoria_rota_avisa_que_se_pierden_las_lecciones_y_guarda_el_archivo(
        tmp_path, capsys):
    programa = CUENTA_CLIENTES + "enviar Llego { quien: \"a\" } a Mostrador\n" \
                          "mostrar(preguntar Cuantos {} a Mostrador)"
    rota = ('{"agentes": {"Mostrador": {"estado": {"atendidos": 2,}, '
            '"lecciones": [{"fecha":"x","texto":"valiosa"}]}}}')
    (tmp_path / "programa.memoria.json").write_text(rota, encoding="utf-8")
    codigo, salida, err = por_main(tmp_path, capsys, programa, "--olvidar")
    assert (codigo, salida) == (0, "1\n")
    assert "los agentes arrancan de cero" in err and "las lecciones no se borran" not in err
    assert "se pierden también las lecciones" in err and "programa.memoria.rota.json" in err
    assert "Bloc de notas" in err and "'corregir'" in err
    assert (tmp_path / "programa.memoria.rota.json").read_text(encoding="utf-8") == rota
    assert memoria_de(tmp_path)["agentes"]["Mostrador"] == {
        "estado": {"atendidos": 1}, "lecciones": []}
    # si no se puede guardar aparte, no corre ni pisa nada
    (tmp_path / "programa.memoria.json").write_text(rota, encoding="utf-8")
    (tmp_path / "programa.memoria.rota.json").unlink()
    (tmp_path / "programa.memoria.rota.json").mkdir()
    (tmp_path / "programa.memoria.rota.json" / "algo").write_text("x", encoding="utf-8")
    codigo, salida, err = por_main(tmp_path, capsys, programa, "--olvidar")
    assert (codigo, salida) == (2, "") and "no pude guardarlo aparte" in err
    assert (tmp_path / "programa.memoria.json").read_text(encoding="utf-8") == rota
    leeme = (RAIZ / "README.md").read_text(encoding="utf-8")
    assert "`mi_mostrador.memoria.rota.json`" in leeme and "**también se pierden**" in leeme


def test_una_leccion_puede_empezar_con_guion_y_no_queda_en_el_registro(tmp_path, con_registro):
    correr_mate, registro = con_registro
    programa = tmp_path / "mi_mostrador.mate"
    programa.write_text(CAJA_QUE_RECUERDA, encoding="utf-8")
    leccion = "-10% a Juan Perez de Lanus, tel 4444-5555"
    codigo, salida, err = correr_mate("corregir", programa, "Caja", leccion)
    assert (codigo, err) == (0, "") and f"  1. {leccion} " in salida
    codigo, salida, _ = correr_mate("corregir", programa, "Caja", "--no mandes nada")
    assert codigo == 0 and "  2. --no mandes nada " in salida
    # una opción de verdad después de la lección sigue siendo una opción
    codigo, salida, _ = correr_mate("corregir", programa, "Caja", "Sé amable", "--sin-registro")
    assert codigo == 0 and "  3. Sé amable " in salida
    assert not registro.exists()
    # una sola palabra con guion se parece a una opción: se explica
    codigo, _, err = correr_mate("corregir", programa, "Caja", "-urgente")
    assert codigo == 2 and "no conozco la opción -urgente" in err
    assert "Si era parte de la lección, escribila entre comillas y sin el guion adelante" in err
    # y lo que la persona escribió con un guion adelante nunca queda en el registro
    assert correr_mate("correr", programa, "-10% a Juan Perez de Lanus, tel 4444-5555")[0] == 2
    assert correr_mate("lecciones", programa, "--no mandes nada a Perez")[0] == 2
    anotado = registro.read_text(encoding="utf-8-sig")
    assert len(renglones_anotados(registro)) == 3
    for dato in ["Juan", "Perez", "Lanus", "mandes", "urgente"]:
        assert dato not in anotado, dato


def test_una_opcion_parecida_a_borrar_se_sugiere(tmp_path, capsys):
    programa = tmp_path / "mi_mostrador.mate"
    programa.write_text(CAJA_QUE_RECUERDA, encoding="utf-8")
    for escrita in ("--borra=1", "-borrar=1", "--borar=1"):
        codigo, _, err = orden_mate(capsys, "lecciones", programa, "Caja", escrita)
        assert codigo == 2
        assert err == f"no conozco la opción {escrita}, ¿quisiste decir --borrar=1?\n"
    codigo, _, err = orden_mate(capsys, "correr", programa, "--trasa=c.txt")
    assert err == "no conozco la opción --trasa=c.txt, ¿quisiste decir --traza=c.txt?\n"
    codigo, _, err = orden_mate(capsys, "correr", programa, "--olvidr")
    assert err == "no conozco la opción --olvidr, ¿quisiste decir --olvidar?\n"
    codigo, _, err = orden_mate(capsys, "correr", programa, "--xyz")
    assert codigo == 2 and err.rstrip().endswith("--sin-registro, --borrar, --guardar")


def test_un_renglon_danado_no_rompe_las_tildes_de_los_demas(tmp_path, con_registro):
    correr_mate, registro = con_registro
    programa = tmp_path / "caja.mate"
    programa.write_text(CAJA_QUE_RECUERDA + "enviar Suma { n: -1 } a Caja\n", encoding="utf-8")
    assert correr_mate("correr", programa)[0] == 1
    bitacora = tmp_path / "caja.bitacora.txt"
    for archivo in (bitacora, registro):
        with open(archivo, "ab") as f:
            f.write(b"\xff\xfe binario\n")
    codigo, salida, err = correr_mate("bitacora", programa)
    assert (codigo, err) == (0, "")
    assert "1 falla(s) anotada(s)" in salida and "falló" in salida and "número negativo" in salida
    assert "Ã" not in salida and "(1 renglón(es) del archivo no tienen la forma" in salida
    codigo, salida, err = correr_mate("informe")
    assert (codigo, err) == (0, "") and "Hay 1 error(es) de uso anotado(s)" in salida
    assert "Ã" not in salida and "(1 renglón(es) del archivo no tienen la forma" in salida
    # y al volver a escribirlos quedan parejos
    assert correr_mate("correr", programa)[0] == 1
    for archivo in (bitacora, registro):
        assert "falló" in archivo.read_bytes().decode("utf-8-sig") or archivo == registro
    assert "2 falla(s) anotada(s)" in correr_mate("bitacora", programa)[1]
    # un archivo guardado como ANSI desde el Bloc de notas también se lee
    bitacora.write_bytes(bitacora.read_bytes().decode("utf-8-sig").encode("cp1252"))
    assert "falló" in correr_mate("bitacora", programa)[1]


def test_lecciones_en_un_programa_sin_agentes_lo_dice(tmp_path, capsys):
    programa = tmp_path / "hola.mate"
    programa.write_text('mostrar("hola")\n', encoding="utf-8")
    assert orden_mate(capsys, "lecciones", programa) == (
        0, "hola.mate no tiene agentes, así que no hay lecciones: las lecciones son de los "
           "agentes.\n", "")
    assert archivos_de(tmp_path) == ["hola.mate"]


def test_una_corrida_que_anduvo_bien_corta_las_veces_seguidas(tmp_path, con_registro):
    correr_mate, registro = con_registro
    bien = tmp_path / "bien.mate"
    bien.write_text('mostrar("hola")\n', encoding="utf-8")
    assert correr_mate("correr", bien)[0] == 0 and not registro.exists()  # no crea el archivo
    assert correr_mate("correr", tmp_path / "nada.mate")[0] == 2
    assert correr_mate("correr", tmp_path / "nada.mate")[0] == 2
    assert correr_mate("correr", bien) == (0, "hola\n", "")
    assert correr_mate("verificar", bien)[0] == 0  # (la marca se pone una sola vez)
    texto = registro.read_text(encoding="utf-8-sig")
    assert texto.count(mate._CORTE_DE_RACHA) == 1 and texto.endswith(mate._CORTE_DE_RACHA + "\n")
    assert correr_mate("correr", tmp_path / "nada.mate")[0] == 2
    assert correr_mate("correr", tmp_path / "nada.mate")[0] == 2
    assert [r[5] for r in renglones_anotados(registro)] == [
        "1 vez", "2 veces seguidas", "1 vez", "2 veces seguidas"]
    assert mate._CORTE_DE_RACHA not in registro.read_text(encoding="utf-8-sig")
    # 'probar' no toca el registro, y con el registro apagado tampoco
    antes = registro.read_bytes()
    con_prueba = tmp_path / "p.mate"
    con_prueba.write_text('prueba "p" { asegurar 1 == 1 }\n', encoding="utf-8")
    assert correr_mate("probar", con_prueba)[0] == 0
    assert correr_mate("correr", bien, "--sin-registro")[0] == 0
    assert registro.read_bytes() == antes
    leeme = (RAIZ / "README.md").read_text(encoding="utf-8")
    assert "ni una corrida\nque anduvo bien en el medio" in leeme


# ─────────────── Versión 0.5: intérprete más rápido y puente a Python ───────────────

# ── 109: el programa se arma una vez (más rápido), y hace lo mismo que antes ──

def test_el_medidor_de_velocidad_corre_y_sus_programas_dan_lo_esperado(capsys):
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "velocidad", pathlib.Path(__file__).with_name("velocidad.py"))
    velocidad = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(velocidad)
    esperado = {
        "bucle con cuentas": ["13333133333"],
        "llamadas a funciones": ["10946 899970000"],
        "listas y mapas": ["119980 600 3000 3500"],
        "mensajes entre agentes": ["31996000"],
    }
    for nombre, fuente in velocidad.PROGRAMAS.items():
        if nombre in esperado:  # (el de textos tarda más: lo corre main, abajo)
            assert velocidad.medir(mate, fuente, 1)[1] == esperado[nombre], nombre
    assert velocidad.main(["--vueltas=1"]) == 0
    out = capsys.readouterr().out
    assert out.startswith(f"Mate {mate.VERSION} con Python ")
    for nombre in list(velocidad.PROGRAMAS) + ["en total"]:
        assert nombre in out
    with pytest.raises(SystemExit) as info:
        velocidad.main(["--cualquiera"])
    assert "no conozco '--cualquiera'" in str(info.value)


def test_armado_cuenta_los_mismos_pasos_y_anota_el_mismo_renglon():
    # (788 pasos son los que contaba la 0.4 con este mismo programa: el freno no cambió)
    salida, interprete = correr("""
        funcion f(n) {
            si n < 2 { devolver n }
            devolver f(n - 1) + f(n - 2)
        }
        var t = 0
        para i en rango(10) {
            si i % 2 == 0 { continuar }
            mientras t < i * 3 { t += 1 }
            intentar { t = t + f(i) / (i - 5) } si falla e { t = t - 1 }
        }
        mostrar(t, f(10))
    """)
    assert salida == ["36.75 55"]
    assert interprete.pasos == 788 and interprete.linea_actual == 3


def test_devolver_romper_y_continuar_salen_de_donde_tienen_que_salir():
    assert mostrados("""
        funcion buscar(lista, x) {
            para i, valor en lista {
                intentar {
                    si valor == x { devolver i }
                } si falla e { devolver -1 }
            }
            devolver nada
        }
        funcion sin_devolver() { sea a = 1 }
        funcion corta() {
            mientras verdadero {
                para c en "abc" {
                    si c == "b" { romper }
                    mostrar(c)
                }
                devolver "listo"
            }
        }
        mostrar(buscar([5, 6, 7], 7), buscar([5], 9), sin_devolver(), corta())
        var pares = []
        para n en rango(6) {
            si n % 2 == 1 { continuar }
            pares = agregar(pares, n)
        }
        mostrar(pares)
    """) == ["a", "2 nada nada listo", "[0, 2, 4]"]
    # fuera de lugar, los mismos errores de siempre (por la puerta de atrás del intérprete)
    interprete = mate.Interprete()
    for fuente, dice in [("devolver 1", "'devolver' solo va dentro de una función"),
                         ("funcion f() { romper }\nf()", "'romper' y 'continuar' solo van")]:
        with pytest.raises(mate.ErrorMate) as info:
            interprete.correr(mate.Parser(mate.tokenizar(fuente)).programa()
                              if "romper" not in fuente else
                              [("funcion", 1, "g", [], [("romper", 1)], []),
                               ("expr", 2, ("llamar", 2, ("nombre", 2, "g"), []))])
        assert dice in info.value.mensaje, fuente


def test_un_bloque_sin_declaraciones_no_arma_entorno_y_uno_con_sea_si():
    antes = mate.Entorno.nacidos
    correr("var t = 0\nmientras t < 50 { si t >= 0 { t += 1 } }")
    assert mate.Entorno.nacidos - antes < 10  # (el del intérprete y poco más: no 100)
    # ...y lo declarado adentro de un bloque sigue sin verse afuera, vuelta por vuelta
    assert mostrados("""
        var veces = 0
        mientras veces < 3 {
            sea doble = veces * 2
            veces += 1
        }
        intentar { si verdadero { sea adentro = 1 } } si falla e { mostrar(e) }
        funcion f() { si verdadero { sea x = 1 } devolver 2 }
        mostrar(veces, f())
    """) == ["3 2"]
    assert "'t' ya existe afuera de este bloque" in falla(
        "var t = 1\nsi verdadero { si verdadero { sea t = 2 } }").mensaje


def test_las_cuentas_rapidas_dan_lo_mismo_que_las_completas():
    assert mostrados("""
        sea grande = 4611686018427387904
        mostrar(grande + 1, grande - 1, grande * 2, grande / 2, grande % 10, grande > 1)
        mostrar(7 / 2, 6 / 3, -7 / 2, -6 / 3, 7 % 3, -7 % 3, 2 * 3.5, 0.1 + 0.2, 1.5 - 2)
        mostrar(1 == 1.0, 1 != 1.5, 2 < 2.5, 2.5 >= 2, "a" == "a", "a" != "a", [1] == [1])
        mostrar(verdadero == verdadero, nada == nada, "a" < "b", 1 == verdadero)
    """)[:3] == [
        "4611686018427387905 4611686018427387903 9223372036854775808 2305843009213693952 4 "
        "verdadero",
        "3.5 2 -3.5 -2 1 2 7 0.3 -0.5",
        "verdadero verdadero verdadero verdadero verdadero falso verdadero"]
    for fuente, dice in [
            ("mostrar(1 / 0)", "división por cero"), ("mostrar(1 % 0)", "división por cero"),
            ("mostrar(1.5 / 0)", "división por cero"),
            ("var x = 1.5\npara i en rango(20) { x = x * x * 1000000.5 }", "demasiado grande"),
            ("var x = 1.5\npara i en rango(1100) { x = x + x }", "demasiado grande"),
            ("var b = 2\npara i en rango(20) { b = b * b }", "demasiado grande"),
            ('mostrar(1 == "1")', "no se puede comparar un texto con un número"),
            ('mostrar("a" < 1)', "no se puede comparar"),
            ('mostrar("01/01/2025" < "02/01/2025")', "las fechas son textos"),
            ("mostrar(verdadero + 1)", "no se puede hacer"),
            ("mostrar(1 y 2)", "la condición tiene que ser verdadero o falso"),
            ("mostrar(no 3)", "la condición tiene que ser verdadero o falso"),
            ("si 1 { }", "la condición tiene que ser verdadero o falso"),
            ("mientras nada { }", "la condición tiene que ser verdadero o falso")]:
        assert dice in falla(fuente).mensaje, fuente


def test_el_error_sigue_saliendo_con_el_renglon_de_mas_adentro():
    for fuente, linea in [
            ("sea lista = [1, 2]\nmostrar(1,\n   lista[\n   5])", 3),
            ("sea m = { a: 1 }\nmostrar(m.a +\n   m.b)", 3),
            ("funcion b(x) {\n  devolver x /\n     0\n}\nmostrar(\n  b(1))", 2),
            ("sea x = 1\nmostrar(\n  x(2))", 3),
            ("si falso {\n  sea a = 1\n} sino si 5 {\n}", 1),
            ("mostrar(\n  no_esta)", 2), ("mostrar(-\n  \"a\")", 1)]:
        programa = mate.analizar(fuente)  # (sin la revisión previa: el error es el de correr)
        with pytest.raises(mate.ErrorMate) as info:
            mate.Interprete(salida=lambda t: None).correr(programa)
        assert info.value.linea == linea, (fuente, info.value.linea, info.value.mensaje)


def test_la_misma_funcion_armada_sirve_para_todas_sus_llamadas_y_sus_valores_por_defecto():
    assert mostrados("""
        funcion f(a, b = a * 2, c = b + 1) { devolver [a, b, c] }
        funcion contador() {
            var n = 0
            funcion uno_mas() {
                n += 1
                devolver n
            }
            devolver uno_mas
        }
        sea uno = contador()
        sea otro = contador()
        mostrar(f(1), f(1, 5), f(1, 5, 9), uno(), uno(), otro())
    """) == ["[1, 2, 3] [1, 5, 6] [1, 5, 9] 1 2 1"]
    assert "f() espera entre 1 y 3 argumento(s) y recibió 0" in falla(
        "funcion f(a, b = 1, c = 2) { devolver a }\nsea x = [f]\nmostrar(x[0]())").mensaje
    # un parámetro con nombre de función incluida sigue siendo un error, llamada por llamada
    interprete = mate.Interprete()
    programa = [("funcion", 1, "g", ["largo"], [("devolver", 1, ("num", 1, 1))], []),
                ("expr", 2, ("llamar", 2, ("nombre", 2, "mostrar"),
                             [("llamar", 2, ("nombre", 2, "g"), [("num", 2, 5)])]))]
    for _ in range(2):
        with pytest.raises(mate.ErrorMate) as info:
            interprete.correr(programa)
        assert "'largo' es una función incluida de Mate" in info.value.mensaje
        interprete = mate.Interprete()


def test_el_readme_y_mejoras_cuentan_la_velocidad_con_numeros():
    leeme = (RAIZ / "README.md").read_text(encoding="utf-8")
    mejoras = (RAIZ / "MEJORAS.md").read_text(encoding="utf-8")
    assert "## Qué tan rápido es" in leeme and "mate\\pruebas\\velocidad.py" in leeme
    for texto in (leeme, mejoras):
        for programa in ["bucle con cuentas", "llamadas a funciones", "listas y mapas",
                         "textos", "mensajes entre agentes"]:
            assert programa in texto, programa
    assert "**109. Un intérprete más rápido**" in mejoras
    assert "**110. Puente a Python (`usar python`)**" in mejoras


# ── 110: puente a Python ──

AYUDAS_PY = '''
import math

veces = 0


def doble(numero):
    return numero * 2


def raiz(numero):
    if numero < 0:
        raise ValueError("no hay raíz de un negativo")
    return math.sqrt(numero)


def agrandar(lista, mapa):
    lista.append("de más")
    mapa["nueva"] = True
    return lista, mapa


def eco(valor=None, *resto):
    return valor


def contar():
    global veces
    veces += 1
    return veces


def conjunto():
    return {1, 2}


def clave_rara():
    return {1: "uno"}


def no_es_numero():
    return float("nan")


def enorme():
    return 10 ** 5000


def con_nombre(a, *, b):
    return a


def se_va():
    raise SystemExit(3)


def falta_clave(mapa):
    return mapa["no está"]


def varios():
    return (1, "dos", [3.5, None, True], {"k": ()})


def _interna():
    return 1


def se_contiene():
    lista = []
    lista.append(lista)
    return lista
'''


def con_python(tmp_path, fuente, python=AYUDAS_PY, nombre="ayudas.py"):
    """Deja el .py al lado de un programa.mate y devuelve la ruta del programa."""
    (tmp_path / nombre).write_text(python, encoding="utf-8")
    programa = tmp_path / "programa.mate"
    programa.write_text(fuente, encoding="utf-8")
    return str(programa)


def correr_con_python(tmp_path, fuente, **mas):
    """Lo que muestra ese programa (que tiene un ayudas.py al lado)."""
    ruta = con_python(tmp_path, 'usar python "ayudas.py"\n' + fuente, **mas)
    salida = []
    interprete = mate.Interprete(salida=salida.append)
    programa = mate.analizar((tmp_path / "programa.mate").read_text(encoding="utf-8"), ruta)
    assert mate.verificar(programa) == []
    interprete.correr(programa)
    return salida


def falla_con_python(tmp_path, fuente, **mas):
    with pytest.raises(mate.ErrorMate) as info:
        correr_con_python(tmp_path, fuente, **mas)
    return info.value


def test_usar_python_llama_funciones_de_un_archivo_que_esta_al_lado(tmp_path):
    assert correr_con_python(tmp_path, """
        mostrar(ayudas.doble(21), ayudas.raiz(16), ayudas.doble("ja"), ayudas.eco())
        mostrar(ayudas.varios())
        mostrar(ayudas.eco(verdadero), ayudas.eco(nada), ayudas.eco(1.5), ayudas.eco(1, 2, 3))
        mostrar(tipo(ayudas.eco(verdadero)), tipo(ayudas.raiz(4)), tipo(ayudas.varios()))
        mostrar(ayudas, ayudas.doble, tipo(ayudas), tipo(ayudas.doble))
        funcion triple(n) { devolver ayudas.doble(n) + n }
        mostrar(triple(5))
    """) == ["42 4 jaja nada", '[1, "dos", [3.5, nada, verdadero], {k: []}]',
             "verdadero nada 1.5 1", "logico numero lista",
             "<python ayudas.py> <funcion ayudas.doble> python funcion", "15"]
    # el programa no dejó nada al lado: ni la carpeta que arma Python cuando importa
    assert sorted(p.name for p in tmp_path.iterdir()) == ["ayudas.py", "programa.mate"]


def test_a_python_los_valores_van_y_vuelven_copiados(tmp_path):
    assert correr_con_python(tmp_path, """
        sea lista = [1, [2]]
        sea mapa = { a: 1 }
        sea vuelta = ayudas.agrandar(lista, mapa)
        mostrar(lista, mapa)
        mostrar(vuelta)
        intentar { fallar "motivo" } si falla e { mostrar(ayudas.eco(e) == "motivo") }
    """) == ['[1, [2]] {a: 1}', '[[1, [2], "de más"], {a: 1, nueva: verdadero}]', "verdadero"]


def test_un_error_dentro_del_python_es_un_error_de_mate_con_su_renglon(tmp_path, capsys):
    error = falla_con_python(tmp_path, "sea a = 1\nmostrar(\n  ayudas.raiz(-1))")
    assert error.linea == 4 and error.familia == "python" and error.clase == "falla"
    assert error.mensaje == (
        "ayudas.raiz() falló adentro del Python (línea 13 de ayudas.py): un valor que no "
        'sirve para lo que se quiso hacer. Python dice: "ValueError: no hay raíz de un '
        'negativo"')
    # se ataja con 'intentar', y detalle_de dice que fue del Python
    assert correr_con_python(tmp_path, """
        intentar {
            mostrar(ayudas.raiz("x"))
        } si falla e {
            mostrar(detalle_de(e).clase, detalle_de(e).linea, tiene(e, "TypeError"))
        }
        intentar { ayudas.se_va() } si falla e { mostrar(tiene(e, "quiso cerrar el programa")) }
        intentar { ayudas.falta_clave({}) } si falla e { mostrar(tiene(e, "KeyError: no está")) }
        mostrar("sigue")
    """) == ["python 4 verdadero", "verdadero", "verdadero", "sigue"]
    # por la línea de comandos sale como cualquier error: archivo, renglón y sin 'Traceback'
    ruta = con_python(tmp_path, 'usar python "ayudas.py"\nfuncion f() { devolver ayudas.raiz(-4) }\n'
                                "mostrar(f())")
    assert mate.main(["correr", ruta]) == 1
    err = capsys.readouterr().err
    assert "programa.mate:2: error: ayudas.raiz() falló adentro del Python" in err
    assert "cómo se llegó: en f(), llamada desde la línea 3" in err and "Traceback" not in err


def test_solo_cruzan_valores_simples_y_los_errores_lo_explican(tmp_path):
    for llamada, dice in [
            ("ayudas.conjunto()", "devolvió algo que Mate no conoce (en Python se llama 'set')"),
            ("ayudas.clave_rara()", "una clave que no es un texto"),
            ("ayudas.no_es_numero()", "devolvió un número que Mate no usa"),
            ("ayudas.enorme()", "devolvió un número demasiado grande para Mate"),
            ("ayudas.se_contiene()", "se tiene a sí mismo adentro"),
            ("ayudas.doble(mostrar)", "solo se le pasan números, textos, verdadero o falso, "
                                      "nada, listas y mapas, y recibió una función"),
            ("ayudas.doble([ayudas])", "y recibió un archivo de Python"),
            ("ayudas.doble(P { n: 1 })", "recibió un mensaje P. Pasalo como mapa: a_mapa(...)"),
            ("ayudas.doble()", "ayudas.doble() lleva 1 valor y recibió 0 (así está escrita "
                               "en ayudas.py)"),
            ("ayudas.doble(1, 2)", "lleva 1 valor y recibió 2"),
            ("ayudas.contar(1)", "lleva 0 valores y recibió 1"),
            ("ayudas.con_nombre(1)", "no se puede llamar desde Mate: en ayudas.py pide 'b'"),
            ("ayudas()", "un archivo de Python no es una función"),
            ("ayudas[0]", "un archivo de Python no tiene posiciones ni claves"),
            ("a_json(ayudas)", "no se puede pasar a JSON"),
            ("M { f: ayudas.doble }", "los mensajes llevan datos, no funciones"),
            ("M { f: ayudas }", "los mensajes llevan datos, no funciones")]:
        error = falla_con_python(
            tmp_path, f"mensaje P {{ n: numero }}\nmensaje M {{ f: cualquiera }}\n"
                      f"sea x = {llamada}")
        assert dice in error.mensaje and error.linea == 4, (llamada, error.mensaje)
    assert "'ayudas' es el archivo de Python que trajo 'usar python'" in falla_con_python(
        tmp_path, "ayudas = 1").mensaje
    assert "'ayudas' ya está definido" in falla_con_python(tmp_path, "sea ayudas = 1").mensaje
    assert "un archivo de Python no tiene campos" in falla_con_python(
        tmp_path, "intentar { ayudas.doble = 1 } si falla e { fallar e }").mensaje


def test_una_funcion_de_python_sola_en_un_renglon_vale_y_sin_parentesis_no(tmp_path):
    assert correr_con_python(tmp_path, """
        ayudas.contar()
        ayudas.contar()
        mostrar(ayudas.contar())
    """) == ["3"]
    error = falla_con_python(tmp_path, "sea f = ayudas.doble\nf")
    assert "a 'ayudas.doble' le faltan los paréntesis: ayudas.doble(...)" in error.mensaje


def test_las_funciones_que_no_estan_se_avisan_antes_de_correr(tmp_path):
    ruta = con_python(tmp_path, 'usar python "ayudas.py"\n'
                                "funcion f() { devolver ayudas.dobel(1) }\n"
                                "mostrar(ayudas._interna(), ayudas.dobel(2), ayudas.math)\n"
                                "intentar { ayudas.nada_de_esto() } si falla e { mostrar(e) }\n")
    programa = mate.analizar((tmp_path / "programa.mate").read_text(encoding="utf-8"), ruta)
    errores = [(int(linea), texto) for linea, texto in mate.verificar(programa)]
    assert errores[0] == (2, "ayudas.py no tiene una función 'dobel'. ¿Quisiste decir 'doble'?")
    assert [linea for linea, _ in errores] == [2, 3, 3]  # (una vez por nombre; 'intentar' no)
    assert "no tiene una función '_interna' (tiene: agrandar, " in errores[1][1]
    assert "no tiene una función 'math'" in errores[2][1]  # lo importado no cuenta
    # y si igual se llega a correr (adentro de un 'intentar'), dice lo mismo
    assert correr_con_python(tmp_path, """
        intentar { ayudas.dobel(1) } si falla e { mostrar(e) }
        intentar { ayudas._interna() } si falla e { mostrar(e) }
        intentar { ayudas.math.sqrt(4) } si falla e { mostrar(tiene(e, "no tiene una función 'math'")) }
    """) == ["ayudas.py no tiene una función 'dobel'. ¿Quisiste decir 'doble'?",
             "'_interna' empieza con guion bajo, y esas funciones de ayudas.py no se ven desde "
             "Mate: en Python así se marcan las que son de uso interno", "verdadero"]
    # si otra cosa se llama igual que el archivo, no se adivina: se revisa al correr
    assert correr_con_python(
        tmp_path, "funcion f(ayudas) { devolver ayudas.x }\nmostrar(f({ x: 7 }))") == ["7"]
    vacio = falla_con_python(tmp_path, "intentar { ayudas.f() } si falla e { fallar e }",
                             python="import math\n_x = 1\n")
    assert "ayudas.py no tiene ninguna función para usar desde Mate" in vacio.mensaje


def test_verificar_avisa_si_el_archivo_de_python_no_esta(tmp_path, capsys):
    (tmp_path / "ayudas.py").write_text("def f():\n    return 1\n", encoding="utf-8")
    (tmp_path / "notas.py.txt").write_text("def f():\n    return 1\n", encoding="utf-8")
    for escrito, dice in [
            ("ayuda.py", "no encuentro el archivo de Python 'ayuda.py' (lo busqué en "),
            ("ayuda.py", "¿Quisiste decir 'ayudas.py'?"),
            ("otra_cosa.py", "Los archivos .py que hay ahí: ayudas.py"),
            ("notas.py", "Encontré notas.py.txt: el Bloc de notas le agregó .txt"),
            ("sub/ayudas.py", "Esa carpeta no existe")]:
        for orden in ("verificar", "correr", "probar"):
            codigo, out, err = por_main(tmp_path, capsys, f'mostrar(1)\nusar python "{escrito}"',
                                        orden=orden)
            assert codigo == 1 and out == "", (escrito, orden)
            assert "programa.mate:2: error: " in err and dice in err, (escrito, orden, err)
    codigo, out, _ = por_main(tmp_path, capsys, 'usar python "ayudas.py"\nmostrar(ayudas.f())',
                              orden="verificar")
    assert codigo == 0 and out.strip().endswith("sin errores")


def test_el_archivo_de_python_no_puede_salir_de_la_carpeta_del_programa(tmp_path):
    adentro = tmp_path / "programas"
    (adentro / "sub").mkdir(parents=True)
    (tmp_path / "afuera.py").write_text("def f():\n    return 1\n", encoding="utf-8")
    (adentro / "sub" / "hondo.py").write_text("def f():\n    return 2\n", encoding="utf-8")
    programa = adentro / "p.mate"

    def error_de(escrito):
        with pytest.raises(mate.ErrorMate) as info:
            mate.analizar(f'usar python "{escrito}"', str(programa))
        assert info.value.linea == 1
        return info.value.mensaje

    for escrito in ["../afuera.py", "sub/../../afuera.py", str(tmp_path / "afuera.py"),
                    "/afuera.py", "C:/afuera.py"]:
        mensaje = error_de(escrito)
        assert "solo trae archivos de la carpeta del programa" in mensaje, escrito
        assert 'nombralo sin la ruta: usar python "afuera.py"' in mensaje, escrito
    try:
        (adentro / "atajo.py").symlink_to(tmp_path / "afuera.py")
    except OSError:  # (en Windows, sin permiso para hacer accesos directos)
        pass
    else:
        assert "queda afuera" in error_de("atajo.py")
    # una carpeta de adentro sí vale, y el nombre es el del archivo
    arbol = mate.analizar('usar python "sub/hondo.py"\nmostrar(hondo.f())', str(programa))
    assert mate.verificar(arbol) == []
    salida = []
    mate.Interprete(salida=salida.append).correr(arbol)
    assert salida == ["2"]


def test_el_nombre_del_archivo_de_python_tiene_que_servir_de_nombre(tmp_path):
    for escrito, dice in [
            ("Mis-Ayudas.py", "'Mis-Ayudas' no sirve: tiene mayúsculas, espacios, guiones"),
            ("2da.py", "'2da' no sirve"), ("mis ayudas.py", "no sirve"),
            ("largo.py", "'largo' no sirve: es una función incluida de Mate"),
            ("para.py", "'para' no sirve: es una palabra de Mate"),
            ("ayudas", "su nombre termina en .py"), ("ayudas.txt", "su nombre termina en .py"),
            (".py", "su nombre termina en .py"), ("", "su nombre termina en .py")]:
        with pytest.raises(mate.ErrorMate) as info:
            mate.analizar(f'usar python "{escrito}"', str(tmp_path / "p.mate"))
        assert dice in info.value.mensaje, escrito
    for fuente, dice in [("usar python", "esperaba el nombre del archivo de Python entre "
                                         'comillas (usar python "ayudas.py")'),
                         ("usar python ayudas", "esperaba el nombre del archivo de Python"),
                         ('funcion f() { usar python "a.py" }', "'usar' solo puede declararse")]:
        with pytest.raises(mate.ErrorMate) as info:
            mate.analizar(fuente, str(tmp_path / "p.mate"))
        assert dice in info.value.mensaje, fuente
    # 'python' no es una palabra reservada: sigue sirviendo de nombre (y no gasta del tope)
    assert "python" not in mate.PALABRAS and len(mate.PALABRAS) == 36
    assert mostrados("sea python = 3\nmostrar(python + 1)") == ["4"]


def test_un_py_mal_escrito_o_que_falla_al_abrirlo_se_explica(tmp_path, capsys):
    marca = tmp_path / "se_ejecuto.txt"
    con_efecto = f"open({str(marca)!r}, 'w').close()\ndef f():\n    return 1\n"
    ruta = con_python(tmp_path, 'usar python "ayudas.py"\nmostrar(ayudas.f())', python=con_efecto)
    # 'verificar' lee el .py pero NO lo ejecuta
    assert mate.main(["verificar", ruta]) == 0 and not marca.exists()
    assert mate.main(["correr", ruta]) == 0 and marca.exists()
    capsys.readouterr()
    for python, dice in [
            ("def f(:\n    return 1\n", "ayudas.py está mal escrito en su línea 1 y Python no "
                                        "lo pudo leer. Python dice: "),
            ("import no_existe_este_modulo\n", "ayudas.py falló apenas se lo abrió, antes de "
                                               "llamar a ninguna de sus funciones (línea 1 de "
                                               "ayudas.py): un 'import' de algo que no está "
                                               "instalado"),
            ("x = 1\ny = x / 0\n", "(línea 2 de ayudas.py): una división por cero"),
            ("raise SystemExit(2)\n", "quiso cerrar el programa")]:
        ruta = con_python(tmp_path, 'mostrar("antes")\nusar python "ayudas.py"\n', python=python)
        assert mate.main(["correr", ruta]) == 1
        capturado = capsys.readouterr()
        assert capturado.out == "" and "Traceback" not in capturado.err
        assert "programa.mate:2: error: " in capturado.err and dice in capturado.err, python
    # un .py guardado por el Bloc de notas en ANSI (con tildes) se lee igual
    (tmp_path / "ayudas.py").write_bytes('def saludo():\n    return "ñandú"\n'.encode("cp1252"))
    (tmp_path / "programa.mate").write_text('usar python "ayudas.py"\nmostrar(ayudas.saludo())',
                                            encoding="utf-8")
    assert mate.main(["correr", str(tmp_path / "programa.mate")]) == 0
    assert capsys.readouterr().out == "ñandú\n"


def test_usar_python_anda_con_probar_con_agentes_y_desde_otro_archivo(tmp_path, capsys):
    (tmp_path / "ayudas.py").write_text(AYUDAS_PY, encoding="utf-8")
    (tmp_path / "lib.mate").write_text(
        'usar python "ayudas.py"\nfuncion cuadruple(n) { devolver ayudas.doble(ayudas.doble(n)) }\n',
        encoding="utf-8")
    programa = tmp_path / "programa.mate"
    programa.write_text("""
        usar "lib.mate"
        usar python "ayudas.py"
        usar python "ayudas.py"
        mensaje Doblar { n: numero }
        agente Calculista {
            estado hechas = 0
            al recibir Doblar como d {
                hechas += 1
                responder ayudas.doble(d.n) + hechas
            }
        }
        mostrar(cuadruple(2), preguntar Doblar { n: 5 } a Calculista)
        prueba "desde una prueba" {
            asegurar ayudas.doble(4) == 8
            asegurar preguntar Doblar { n: 1 } a Calculista == 3
            asegurar falla { ayudas.raiz(-1) }
        }
        prueba "esta falla" { asegurar ayudas.raiz(9) == 4 }
    """, encoding="utf-8")
    assert mate.main(["correr", str(programa)]) == 0
    assert capsys.readouterr().out == "8 11\n"
    assert mate.main(["probar", str(programa)]) == 1
    out = capsys.readouterr().out
    assert "✓ desde una prueba" in out and "✗ esta falla" in out
    assert "dio 3 y se esperaba 4" in out and "1 de 2 pruebas pasaron" in out
    assert sorted(p.name for p in tmp_path.iterdir()) == ["ayudas.py", "lib.mate", "programa.mate"]
    # dos archivos distintos con el mismo nombre no pueden convivir
    (tmp_path / "sub").mkdir()
    (tmp_path / "sub" / "ayudas.py").write_text("def f():\n    return 1\n", encoding="utf-8")
    programa.write_text('usar python "ayudas.py"\nusar python "sub/ayudas.py"\n', encoding="utf-8")
    assert mate.main(["correr", str(programa)]) == 1
    assert "programa.mate:2: error: 'ayudas' ya está definido" in capsys.readouterr().err


def test_en_la_consola_usar_python_se_puede_traer_de_nuevo(tmp_path, monkeypatch):
    (tmp_path / "ayudas.py").write_text("def f():\n    return 1\n", encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    renglones = iter(['usar python "ayudas.py"', "ayudas.f()", "PISAR", 'usar python "ayudas.py"',
                      "ayudas.f()", "ayudas", "salir"])

    def entrada(_pregunta):
        renglon = next(renglones)
        if renglon == "PISAR":  # (como si el dueño corrigiera el .py con el Bloc de notas)
            (tmp_path / "ayudas.py").write_text("def f():\n    return 2\n", encoding="utf-8")
            renglon = "1 + 1"
        return renglon

    mostrado = []
    mate.consola(entrada, mostrado.append)
    assert mostrado[2:] == ["1", "2", "2", "<python ayudas.py>"]


def test_el_registro_no_guarda_lo_que_dijo_el_python(tmp_path, con_registro):
    correr_mate, registro = con_registro
    ruta = con_python(tmp_path, 'usar python "ayudas.py"\nmostrar(ayudas.secreto())',
                      python='def secreto():\n    raise ValueError("clave de Marta: 1234")\n')
    codigo, _, err = correr_mate("correr", ruta)
    assert codigo == 1 and "clave de Marta: 1234" in err  # en pantalla sí se ve
    anotado = registro.read_text(encoding="utf-8-sig")
    assert "Marta" not in anotado and "1234" not in anotado and "secreto" not in anotado
    assert "al correr: falló algo de un archivo traído con 'usar python'" in anotado
    assert "<lo que pasó en el archivo de Python del programa>" in anotado


def test_el_ejemplo_9_muestra_lo_que_dicen_sus_comentarios(capsys):
    assert mate.main(["correr", str(RAIZ / "ejemplos" / "09_con_python.mate")]) == 0
    assert capsys.readouterr().out == (
        "La raíz de 144 es 12\n"
        "Del 1 al 15 de marzo van 14 días\n"
        "La venta del medio fue de $ 1.200 y la mayor de $ 3.500\n"
        "Esas fechas no se entienden: van como 01/03/2026\n")
    assert mate.main(["probar", str(RAIZ / "ejemplos" / "09_con_python.mate")]) == 0
    assert "3 de 3 pruebas pasaron" in capsys.readouterr().out
    # correrlo no deja nada nuevo en la carpeta de ejemplos
    assert not (RAIZ / "ejemplos" / "__pycache__").exists()
    assert sorted(p.name for p in (RAIZ / "ejemplos").glob("*.py")) == ["ayudas.py"]


def test_la_documentacion_cuenta_el_puente_a_python_y_su_riesgo(capsys):
    leeme = (RAIZ / "README.md").read_text(encoding="utf-8")
    assert "### Funciones escritas en Python: `usar python`" in leeme
    for texto in [leeme, mate.ayuda_de("python"), mate.texto_de_guia(), mate.texto_de_ayuda(),
                  (RAIZ / "ejemplos" / "ayudas.py").read_text(encoding="utf-8"),
                  (RAIZ / "ejemplos" / "09_con_python.mate").read_text(encoding="utf-8")]:
        assert 'usar python "ayudas.py"' in texto
        assert "todos los permisos" in " ".join(texto.split())
    for frase in ["`09_con_python.mate`", "once programas cortos", "también con `probar`",
                  "`\"python\"`", "copiados", "python mate\\mate.py ayuda python"]:
        assert frase in leeme, frase
    assert mate.ayuda_de("usar") and "'ayuda python'" in mate.ayuda_de("usar")
    assert mate.main(["ayuda", "python"]) == 0
    assert "mostrar(ayudas.doble(21))" in capsys.readouterr().out


# ── 0.5, cuarta parte: datos de verdad y charla por teclado (mejoras 111 a 113) ──

def con_teclado(monkeypatch, tecleado):
    """Lo que 'se escribe' en el teclado al correr de verdad: un texto por cada leer(), y
    cuando se acaban, lo que pasa al apretar Ctrl+Z (no hay más)."""
    pendientes, preguntas = list(tecleado), []

    def teclear(pregunta):
        preguntas.append(pregunta)
        if not pendientes:
            raise EOFError
        siguiente = pendientes.pop(0)
        if isinstance(siguiente, BaseException):
            raise siguiente
        return siguiente

    monkeypatch.setattr(mate, "por_teclado", teclear)
    return preguntas


# 111: leer_tabla

def test_leer_tabla_lee_la_planilla_como_la_guarda_excel(tmp_path, capsys):
    # separada por punto y coma, con la marca del principio y saltos de Windows
    (tmp_path / "precios.csv").write_bytes(
        "﻿producto;precio;stock;codigo;nota\r\n"
        "Yerba 1 kg;3.500;12;00123;\r\n"
        "\r\n"
        'Azúcar;$ 1.250,50;3,5;A1;"con ; adentro"\r\n'
        ";;;;\r\n".encode("utf-8"))
    codigo, salida, err = por_main(tmp_path, capsys, """
        sea filas = leer_tabla("precios.csv")
        mostrar(filas)
        mostrar(tipo(filas), largo(filas), filas[0].precio + 1, pesos(filas[1].precio))
        para fila en filas { mostrar("{fila.producto}: {fila.stock}") }
    """)
    assert (codigo, err) == (0, "")
    assert salida.splitlines() == [
        '[{producto: "Yerba 1 kg", precio: 3500, stock: 12, codigo: "00123", nota: ""}, '
        '{producto: "Azúcar", precio: 1250.5, stock: 3.5, codigo: "A1", nota: "con ; adentro"}]',
        "lista 2 3501 $ 1.250,50", "Yerba 1 kg: 12", "Azúcar: 3.5"]
    assert archivos_de(tmp_path) == ["precios.csv", "programa.mate"]  # leer no crea nada


@pytest.mark.parametrize("crudo,esperado", [
    # separada por comas: el precio con coma va entre comillas, como lo guarda Excel
    ('producto,precio\nPan,"1.200,50"\nLeche,900\n'.encode("utf-8"),
     '[{producto: "Pan", precio: 1200.5}, {producto: "Leche", precio: 900}]'),
    # en ANSI de Windows (lo que guarda un Excel viejo): la ñ y las tildes llegan bien
    ("producto;precio\nÑoquis;2.300\nAzúcar;1.100\n".encode("cp1252"),
     '[{producto: "Ñoquis", precio: 2300}, {producto: "Azúcar", precio: 1100}]'),
    # el renglón "sep=" que a veces pone Excel, y columnas vacías a la derecha
    (b"sep=;\nproducto;precio;;\nPan;1200;;\n", '[{producto: "Pan", precio: 1200}]'),
    # separada por tabulaciones (copiada de la planilla al Bloc de notas)
    (b"producto\tprecio\nPan\t1.200\n", '[{producto: "Pan", precio: 1200}]'),
    # títulos con mayúsculas y espacios: quedan tal cual; una sola columna también sirve
    ("Precio de lista\n$ 3.500\n".encode("utf-8"), '[{Precio de lista: 3500}]'),
    # solo los títulos: una lista vacía
    (b"producto;precio\n", "[]"),
    # un dato de varios renglones entre comillas
    (b'producto;nota\nPan;"dos\nrenglones"\nLeche;fin\n',
     '[{producto: "Pan", nota: "dos\\nrenglones"}, {producto: "Leche", nota: "fin"}]'),
])
def test_leer_tabla_acepta_las_formas_de_guardar_un_csv(crudo, esperado, tmp_path, capsys):
    (tmp_path / "lista.csv").write_bytes(crudo)
    codigo, salida, err = por_main(tmp_path, capsys, 'mostrar(leer_tabla("lista.csv"))')
    assert (codigo, salida, err) == (0, esperado + "\n", "")


@pytest.mark.parametrize("celda,valor", [
    ("3.500", 3500), ("3.500,50", 3500.5), ("$ 3.500", 3500), ("$3.500,5", 3500.5),
    ("1.234.567", 1234567), ("3,5", 3.5), ("12", 12), ("-$ 100", -100), ("0", 0), ("0,5", 0.5),
    (" 40 ", 40), ("00123", "00123"), ("011 4444", "011 4444"), ("Yerba", "Yerba"), ("", ""),
    ("  con espacios  ", "con espacios"), ("12/05/2026", "12/05/2026"), ("21%", "21%"),
    ("1,234.50", "1,234.50"), ("3.50", 3.5), ("A1", "A1"),
])
def test_los_numeros_de_una_planilla_se_leen_a_la_argentina(celda, valor):
    leido = mate.valor_de_celda(celda)
    assert leido == valor and type(leido) is type(valor)


def test_el_separador_se_decide_por_la_fila_de_titulos():
    assert mate.separador_de("producto;precio") == ";"
    assert mate.separador_de("producto,precio") == ","
    assert mate.separador_de('"precio, con IVA";producto') == ";"
    assert mate.separador_de("producto") == ";"  # ante la duda, lo que usa Excel acá
    assert mate.separador_de("producto\tprecio\tstock") == "\t"


@pytest.mark.parametrize("crudo,frases", [
    # una fila con columnas de más: dice el renglón del archivo y cómo se arregla
    (b"producto,precio\nPan,900\nLeche,1.200,50\n",
     ["el renglón 3 de 'lista.csv' tiene 3 columnas y los títulos son 2 (producto, precio)",
      "le sobra algo", '"3.500,50"', "separadas por coma", 'El renglón dice: "Leche,1.200,50"']),
    # de menos (y el renglón en blanco de arriba también cuenta para decir cuál es)
    (b"producto;precio;stock\n\nPan;900;4\nLeche\n",
     ["el renglón 4 de 'lista.csv' tiene 1 columna y los títulos son 3",
      "le falta un dato, o un separador", "separadas por punto y coma"]),
    (b"", ["'lista.csv' está vacío", "una primera fila con los títulos"]),
    (b"\n \n;;\n", ["'lista.csv' está vacío"]),
    (b"producto;;precio\nPan;x;900\n", ["la columna 2 no tiene título", "el renglón 1"]),
    (b"producto;precio;precio\nPan;1;2\n",
     ["hay dos columnas con el mismo título, 'precio'"]),
    # lo que viene de Excel sin convertir (un .xlsx con otro nombre): cómo guardarlo
    (b"PK\x03\x04\x14\x00\x06\x00\x08\x00\x00\x00!\x00\x81\x8d\x90\x9d",
     ["'lista.csv' es una planilla de Excel", "Guardar como", "CSV (delimitado por comas)"]),
])
def test_leer_tabla_explica_lo_que_esta_mal_en_la_planilla(crudo, frases, tmp_path, capsys):
    (tmp_path / "lista.csv").write_bytes(crudo)
    codigo, salida, err = por_main(tmp_path, capsys, 'mostrar(leer_tabla("lista.csv"))')
    assert (codigo, salida) == (1, "")
    assert "programa.mate:1: error: leer_tabla(): " in err and "Traceback" not in err
    for frase in frases:
        assert frase in err, frase


def test_leer_tabla_dice_donde_busco_el_archivo_que_no_esta(tmp_path, capsys):
    (tmp_path / "precio.csv").write_text("a;b\n1;2\n", encoding="utf-8")
    codigo, _, err = por_main(tmp_path, capsys, 'sea t = leer_tabla("precios.csv")')
    assert codigo == 1
    assert f"leer_tabla(): no encuentro el archivo 'precios.csv' en {tmp_path}" in err
    assert "¿Quisiste decir 'precio.csv'?" in err
    # la planilla de Excel sin convertir: no hace falta ni que exista para explicarlo
    codigo, _, err = por_main(tmp_path, capsys, 'sea t = leer_tabla("Lista Mayo.XLSX")')
    assert codigo == 1 and "es una planilla de Excel" in err
    assert 'leer_tabla("Lista Mayo.csv")' in err and "Guardar como" in err
    # afuera de la carpeta del programa no se lee, igual que leer_archivo()
    codigo, _, err = por_main(tmp_path, capsys, 'sea t = leer_tabla("../precios.csv")')
    assert codigo == 1 and "solo trabaja con archivos de la carpeta del programa" in err
    codigo, _, err = por_main(tmp_path, capsys, "sea t = leer_tabla(3)")
    assert codigo == 1 and "leer_tabla()" in err
    # y se ataja con 'intentar': es de la familia de los archivos
    codigo, salida, _ = por_main(tmp_path, capsys, """
        intentar { sea t = leer_tabla("no_esta.csv") } si falla e { mostrar(detalle_de(e).clase) }
    """)
    assert (codigo, salida) == (0, "archivo\n")


def test_un_agente_no_lee_tablas_ni_agrega_a_archivos(tmp_path, capsys):
    (tmp_path / "p.csv").write_text("a;b\n1;2\n", encoding="utf-8")
    for llamada in ['leer_tabla("p.csv")', 'agregar_a_archivo("p.txt", "x")']:
        codigo, _, err = por_main(tmp_path, capsys, f"""
            mensaje Ver {{}}
            agente A {{ al recibir Ver {{ sea t = [{llamada}]
                responder 1 }} }}
            mostrar(preguntar Ver {{}} a A)
        """)
        assert codigo == 1 and "solo se usa desde el programa principal" in err, llamada
    assert archivos_de(tmp_path) == ["p.csv", "programa.mate"]


# 112: agregar_a_archivo

def test_agregar_a_archivo_suma_renglones_sin_pisar(tmp_path, capsys):
    programa = """
        agregar_a_archivo("pedidos.txt", "2 de yerba ñ")
        agregar_a_archivo("pedidos.txt", "1 de azúcar\\n")
        mostrar(leer_archivo("pedidos.txt"))
    """
    codigo, salida, err = por_main(tmp_path, capsys, programa)
    assert (codigo, salida, err) == (0, "2 de yerba ñ\n1 de azúcar\n\n", "")
    crudo = (tmp_path / "pedidos.txt").read_bytes()
    assert crudo.startswith(b"\xef\xbb\xbf")  # la marca, para el Bloc de notas
    assert crudo.decode("utf-8-sig").splitlines() == ["2 de yerba ñ", "1 de azúcar"]
    # otra corrida sigue sumando al final
    assert por_main(tmp_path, capsys, programa)[0] == 0
    assert (tmp_path / "pedidos.txt").read_text(encoding="utf-8-sig").splitlines() == [
        "2 de yerba ñ", "1 de azúcar"] * 2
    assert not [a for a in archivos_de(tmp_path) if a.endswith(".tmp")]


def test_agregar_a_archivo_respeta_lo_que_dejo_el_bloc_de_notas(tmp_path, capsys):
    # sin salto al final: lo nuevo va en su propio renglón
    (tmp_path / "a.txt").write_bytes("uno".encode("utf-8"))
    # en ANSI de Windows: no se mezclan codificaciones (queda todo en UTF-8, con las tildes bien)
    (tmp_path / "b.txt").write_bytes("señor\r\nazúcar\r\n".encode("cp1252"))
    (tmp_path / "c.txt").write_bytes(b"")
    codigo, _, err = por_main(tmp_path, capsys, """
        para nombre en ["a.txt", "b.txt", "c.txt"] { agregar_a_archivo(nombre, "ñandú") }
    """)
    assert (codigo, err) == (0, "")
    assert (tmp_path / "a.txt").read_text(encoding="utf-8").splitlines() == ["uno", "ñandú"]
    assert (tmp_path / "b.txt").read_text(encoding="utf-8-sig").splitlines() == [
        "señor", "azúcar", "ñandú"]
    assert (tmp_path / "c.txt").read_text(encoding="utf-8-sig") == "ñandú\n"
    assert not [a for a in archivos_de(tmp_path) if a.endswith(".tmp")]


@pytest.mark.parametrize("llamada,frase", [
    ('agregar_a_archivo("pedidos.txt", 3)', "agregar_a_archivo() guarda un texto y recibió"),
    ('agregar_a_archivo("otro.mate", "x")', "no escribe en 'otro.mate' para no pisar un programa"),
    ('agregar_a_archivo("../afuera.txt", "x")', "solo trabaja con archivos de la carpeta"),
    ('agregar_a_archivo("no_hay/p.txt", "x")', "no existe la carpeta donde iría 'no_hay/p.txt'"),
    ('agregar_a_archivo("", "x")', "falta el nombre del archivo"),
    ('agregar_a_archivo("p.txt")', "agregar_a_archivo("),
    ('sea x = 1\nleer_tabla("p.csv")', "leer_tabla"),  # suelta no sirve: hay que usar lo que da
])
def test_agregar_a_archivo_tiene_los_cuidados_de_escribir_archivo(
        llamada, frase, tmp_path, capsys):
    codigo, salida, err = por_main(tmp_path, capsys, llamada)
    assert (codigo, salida) == (1, "") and frase in err and "Traceback" not in err
    assert archivos_de(tmp_path) == ["programa.mate"]


def test_con_probar_agregar_a_archivo_no_toca_el_archivo_de_verdad(tmp_path, capsys):
    (tmp_path / "pedidos.txt").write_bytes(b"lo de ayer\n")
    programa = """
        funcion anotar(pedido) { agregar_a_archivo("pedidos.txt", pedido) }
        anotar("del programa")
        agregar_a_archivo("nuevo.txt", "no se crea")
        mostrar(leer_archivo("pedidos.txt"))
        prueba "lo agregado se ve adentro de la prueba" {
            anotar("de la prueba")
            asegurar leer_archivo("pedidos.txt") == "lo de ayer\\ndel programa\\nde la prueba\\n"
            asegurar leer_archivo("nuevo.txt") == "no se crea\\n"
        }
        prueba "cada prueba arranca sin lo que agregó la anterior" {
            asegurar leer_archivo("pedidos.txt") == "lo de ayer\\ndel programa\\n"
            agregar_a_archivo("tabla.csv", "producto;precio")
            agregar_a_archivo("tabla.csv", "Pan;1.200")
            asegurar leer_tabla("tabla.csv") == [{ producto: "Pan", precio: 1200 }]
        }
    """
    codigo, salida, err = por_main(tmp_path, capsys, programa, orden="probar")
    assert (codigo, err) == (0, "") and "2 de 2 pruebas pasaron" in salida
    assert salida.startswith("lo de ayer\ndel programa\n")
    assert archivos_de(tmp_path) == ["pedidos.txt", "programa.mate"]
    assert (tmp_path / "pedidos.txt").read_bytes() == b"lo de ayer\n"
    # con 'correr' sí se escribe
    assert por_main(tmp_path, capsys, programa)[0] == 0
    assert (tmp_path / "pedidos.txt").read_bytes().decode("utf-8").splitlines() == [
        "lo de ayer", "del programa"]
    assert (tmp_path / "nuevo.txt").exists()


# 113: charla por teclado

CHARLA = """
funcion charlar() {
    var dichos = []
    mientras verdadero {
        sea dicho = leer("Cliente:", "chau")
        si minusculas(dicho) == "chau" { romper }
        dichos = agregar(dichos, dicho)
    }
    devolver dichos
}
"""


def test_simular_teclado_fija_lo_que_se_teclea_en_una_prueba(tmp_path, capsys):
    codigo, salida, err = por_main(tmp_path, capsys, CHARLA + """
        mostrar(charlar())
        prueba "una charla de dos consultas" {
            simular_teclado(["  ¿Hay ñoquis?  ", "", "y azúcar", "CHAU", "esto no se lee"])
            asegurar charlar() == ["¿Hay ñoquis?", "", "y azúcar"]
            asegurar leer("¿Algo más?", "no") == "esto no se lee"
            asegurar leer("¿Algo más?", "no") == "no"    # se acabó lo tecleado: la preparada
        }
        prueba "cada prueba arranca sin nada tecleado" {
            asegurar charlar() == []
            simular_teclado("uno solo")
            asegurar leer("¿Qué?") == "uno solo"
            asegurar falla { leer("¿Y ahora?") }
        }
    """, orden="probar")
    assert (codigo, err) == (0, "")
    assert salida.startswith("[]\n") and "2 de 2 pruebas pasaron" in salida  # nunca esperó


def test_simular_teclado_explica_lo_que_esta_mal(tmp_path, capsys):
    codigo, salida, _ = por_main(tmp_path, capsys, """
        prueba "se queda sin textos" {
            simular_teclado(["a"])
            sea uno = leer("¿Uno?")
            sea dos = leer("¿Dos?")
        }
        prueba "una lista vacía" { simular_teclado([]) }
        prueba "algo que no es texto" { simular_teclado(["a", 3]) }
        prueba "sin nada preparado" { sea x = leer("¿Qué?") }
    """, orden="probar")
    assert codigo == 1 and "0 de 4 pruebas pasaron" in salida
    assert "la prueba llegó a 2 leer() y simular_teclado() tenía 1 texto(s)" in salida
    assert 'leer("Cliente:", "chau")' in salida
    assert salida.count("simular_teclado() espera lo que 'teclea' la persona") == 2
    assert "recibió una lista (vacía, o con algo que no es un texto)" in salida
    assert 'o fijá antes lo que se teclea: simular_teclado(["3"])' in salida
    # fuera de una prueba no va: se avisa antes de correr
    codigo, salida, err = por_main(tmp_path, capsys, 'mostrar("antes")\nsimular_teclado(["a"])')
    assert (codigo, salida) == (1, "") and mate.SIMULAR_TECLADO_SUELTO in err
    assert "simular_teclado" in mate.SOLO_EN_PRUEBAS and "simular_teclado" in mate.HACEN_ALGO


def test_al_correr_de_verdad_leer_usa_el_teclado(tmp_path, capsys, monkeypatch):
    preguntas = con_teclado(monkeypatch, ["  ¿Hay ñandú?  ", "﻿azúcar", "chau"])
    codigo, salida, err = por_main(tmp_path, capsys, CHARLA + "mostrar(charlar())")
    assert (codigo, salida, err) == (0, '["¿Hay ñandú?", "azúcar"]\n', "")
    assert preguntas == ["Cliente:"] * 3
    # si se acaba lo tecleado (Ctrl+Z, o no hay teclado), vale la respuesta preparada
    con_teclado(monkeypatch, ["hola"])
    assert por_main(tmp_path, capsys, CHARLA + "mostrar(charlar())")[1] == '["hola"]\n'
    # ...también si la entrada está cerrada y ni siquiera se puede leer
    con_teclado(monkeypatch, ["hola", OSError("no hay entrada")])
    assert por_main(tmp_path, capsys, CHARLA + "mostrar(charlar())")[:2] == (0, '["hola"]\n')
    con_teclado(monkeypatch, [OSError("no hay entrada")])
    codigo, _, err = por_main(tmp_path, capsys, 'sea x = leer("¿Qué?")')
    assert codigo == 1 and "leer(): no hay nadie para contestar" in err


def test_ctrl_c_en_la_charla_termina_prolijo_y_guarda_la_memoria(tmp_path, capsys, monkeypatch):
    programa = """
        mensaje Consulta { texto: texto }
        agente Mostrador {
            estado recordado atendidos = 0
            al recibir Consulta como c {
                atendidos += 1
                responder atendidos
            }
        }
        mientras verdadero {
            sea dicho = leer("Cliente:", "chau")
            si dicho == "chau" { romper }
            mostrar(preguntar Consulta { texto: dicho } a Mostrador)
        }
        mostrar("esto no se llega a mostrar")
    """
    con_teclado(monkeypatch, ["yerba", "pan", KeyboardInterrupt()])
    codigo, salida, err = por_main(tmp_path, capsys, programa)
    assert (codigo, salida, err) == (130, "1\n2\n", f"\n{mate.CORTE_EN_EL_TECLADO}\n")
    assert memoria_de(tmp_path)["agentes"]["Mostrador"]["estado"] == {"atendidos": 2}
    # la próxima corrida sigue la cuenta
    con_teclado(monkeypatch, ["azúcar", "chau"])
    codigo, salida, err = por_main(tmp_path, capsys, programa)
    assert (codigo, salida, err) == (0, "3\nesto no se llega a mostrar\n", "")
    # Ctrl+C en cualquier otro momento sigue siendo un corte con su línea (ver más arriba)
    assert issubclass(mate.CorteEnElTeclado, KeyboardInterrupt)


def test_un_programa_de_antes_puede_usar_los_nombres_nuevos_de_la_05(tmp_path, capsys):
    fuente = ('sea leer_tabla = [1, 2]\nvar simular_teclado = "a"\n'
              "funcion agregar_a_archivo(a, b) { devolver a + b }\n"
              'mostrar(leer_tabla, simular_teclado, agregar_a_archivo(1, 2))')
    codigo, salida, err = por_main(tmp_path, capsys, fuente)
    assert (codigo, salida, err) == (0, "[1, 2] a 3\n", "")
    assert archivos_de(tmp_path) == ["programa.mate"]


# El ejemplo completo: el mostrador mayorista

def test_el_ejemplo_del_mostrador_mayorista(tmp_path, capsys, monkeypatch, ia):
    import shutil
    original = RAIZ / "ejemplos" / "10_mostrador_mayorista.mate"
    en_la_carpeta = archivos_de(RAIZ / "ejemplos")
    assert "precios.csv" in en_la_carpeta
    codigo, salida, err = orden_mate(capsys, "probar", original)
    assert (codigo, err) == (0, "") and "6 de 6 pruebas pasaron" in salida and ia.pedidos == []
    assert archivos_de(RAIZ / "ejemplos") == en_la_carpeta  # 'probar' no deja nada
    ruta = shutil.copy(original, tmp_path / original.name)
    shutil.copy(RAIZ / "ejemplos" / "precios.csv", tmp_path)
    # una charla de verdad, con la IA simulada: busca en la lista de precios
    con_teclado(monkeypatch, ["¿Tenés yerba?", "", "AZUCAR y harina", "clavos", "Chau"])
    codigo, salida, err = orden_mate(capsys, "correr", ruta, "--ia-simulada")
    assert (codigo, err) == (0, "") and ia.pedidos == []
    renglones = salida.splitlines()
    assert renglones[0] == "Mostrador mayorista: cargué 6 productos de precios.csv."
    assert "Mostrador: Yerba mate (bolsón de 10 paquetes de 1 kg): $ 35.000,00" in renglones
    assert ("Mostrador: Azúcar (bolsa de 10 kg): $ 9.800,50 / "
            "Harina 000 (bolsa de 25 kg): $ 14.500,00") in renglones
    assert "   (consulta número 3 desde que abrió el mostrador)" in renglones
    assert renglones[-1] == "Hasta luego. En esta charla atendí 3 consulta(s)."
    anotado = (tmp_path / "consultas_atendidas.txt").read_text(encoding="utf-8-sig").splitlines()
    assert len(anotado) == 3 and " | ¿Tenés yerba? | Yerba mate" in anotado[0]
    assert memoria_de(tmp_path, "10_mostrador_mayorista")["agentes"]["Mostrador"]["estado"] == {
        "atendidos": 3}
    # otra corrida, cortada con Ctrl+C: recuerda las de antes y guarda la nueva
    con_teclado(monkeypatch, ["arroz", KeyboardInterrupt()])
    codigo, salida, err = orden_mate(capsys, "correr", ruta, "--ia-simulada")
    assert (codigo, err) == (130, f"\n{mate.CORTE_EN_EL_TECLADO}\n")
    assert "   (consulta número 4 desde que abrió el mostrador)" in salida
    assert memoria_de(tmp_path, "10_mostrador_mayorista")["agentes"]["Mostrador"]["estado"] == {
        "atendidos": 4}
    assert len((tmp_path / "consultas_atendidas.txt").read_bytes().splitlines()) == 4
    # con la IA de verdad, la lista de precios viaja en las instrucciones
    con_teclado(monkeypatch, ["¿Cuánto sale la yerba?", "chau"])
    codigo, salida, err = orden_mate(capsys, "correr", ruta)
    assert (codigo, err) == (0, "") and "Mostrador: Sí, hay yerba." in salida
    (pedido,) = ia.pedidos
    assert pedido["cuerpo"]["messages"] == [{"role": "user", "content": "¿Cuánto sale la yerba?"}]
    assert "- Azúcar (bolsa de 10 kg): $ 9.800,50\n" in pedido["cuerpo"]["system"]
    assert "$ 18.900,00 - SIN STOCK" in pedido["cuerpo"]["system"]
    assert CLAVE_DE_MENTIRA not in salida + err
    # una planilla con un renglón roto: el error dice cuál
    (tmp_path / "precios.csv").write_text(
        "producto;presentacion;precio;stock\nYerba;bolsón;35.000\n", encoding="utf-8")
    codigo, salida, err = orden_mate(capsys, "correr", ruta, "--ia-simulada")
    assert codigo == 1 and "el renglón 2 de 'precios.csv' tiene 3 columnas" in err


def test_la_documentacion_cuenta_los_datos_y_la_charla(capsys):
    leeme = (RAIZ / "README.md").read_text(encoding="utf-8")
    for frase in ["### Una lista de precios de Excel: `leer_tabla`", "### Charlar por teclado",
                  "### Anotar en un archivo: `agregar_a_archivo`",
                  "CSV (delimitado por comas) (*.csv)", "`10_mostrador_mayorista.mate`",
                  "once programas cortos", "el tope se subió de 45 a 48",
                  'simular_teclado(["2 de yerba", "1 de azúcar", "chau"])',
                  "**Con `probar` no escribe el archivo de verdad.**", "Ctrl+C",
                  "`3.500` es tres mil", "qué renglón del archivo es"]:
        assert frase in leeme, frase
    guia = mate.texto_de_guia()
    for frase in ['leer_tabla("precios.csv")', 'agregar_a_archivo("pedidos.txt", renglon)',
                  'simular_teclado(["hola", "chau"]) solo dentro de una prueba',
                  'sea dicho = leer("Cliente:", "chau")', "Ctrl+C", "3.500 es 3500"]:
        assert frase in guia, frase
    for texto in [mate.texto_de_ayuda(), mate.ayuda_de("leer_tabla"),
                  mate.ayuda_de("agregar_a_archivo"), mate.ayuda_de("simular_teclado"),
                  mate.ayuda_de("leer")]:
        assert max(len(r) for r in texto.splitlines()) <= 100
    assert 'leer_tabla("precios.csv")' in mate.texto_de_ayuda()
    assert "Guardar como" in mate.ayuda_de("leer_tabla")
    assert "Ctrl+C" in mate.ayuda_de("leer") and "romper" in mate.ayuda_de("leer")
    assert mate.main(["ayuda", "agregar_a_archivo"]) == 0
    assert "Con 'probar' no toca el archivo" in " ".join(capsys.readouterr().out.split())
    mejoras = (RAIZ / "MEJORAS.md").read_text(encoding="utf-8")
    for frase in ["**111. Leer una planilla: `leer_tabla`**",
                  "**112. Anotar en un archivo: `agregar_a_archivo`**",
                  "**113. Charla por teclado que se puede probar y cortar: `simular_teclado` "
                  "y Ctrl+C**", "**El tope de funciones pasó de 45 a 48**"]:
        assert frase in mejoras, frase
    assert mate.TOPE_DE_FUNCIONES == 48 == len(mate.FUNCIONES)
    ejemplo = (RAIZ / "ejemplos" / "10_mostrador_mayorista.mate").read_text(encoding="utf-8")
    for frase in ["python mate\\mate.py correr mate\\ejemplos\\10_mostrador_mayorista.mate "
                  "--ia-simulada", "CSV (delimitado por comas) (*.csv)", "precios.csv"]:
        assert frase in ejemplo, frase


def test_los_ejemplos_largos_de_la_ayuda_de_funciones_andan(tmp_path, monkeypatch):
    (tmp_path / "precios.csv").write_text("producto;precio\nYerba;3.500\n", encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    for nombre, (_, ejemplo) in mate.AYUDA_DE_FUNCION.items():
        assert nombre in mate.FUNCIONES and nombre in ejemplo, nombre
        programa = mate.analizar(ejemplo)
        assert mate.verificar(programa) == [], nombre
        salida = []
        interprete = mate.Interprete(salida=salida.append)
        resultados = interprete.correr(programa, pruebas=True)
        assert all(error is None for _, error in resultados), (nombre, resultados)
        # (la charla de 'ayuda leer' no muestra nada: sin teclado, sale sola con "chau")
        assert salida or resultados or nombre == "leer", nombre
    assert archivos_de(tmp_path) == ["precios.csv"]  # (con las pruebas, nada se escribe)


# ── 0.5: frenos para la IA, tope de gasto y lecciones propuestas ──

RESERVA = "Eso te lo confirma una persona, ya te paso."

CON_FRENOS = """
mensaje Consulta { pregunta: texto }
agente Mostrador {
    estado lista = [{ producto: "Yerba", precio: 3500 }, { producto: "Azúcar", precio: 1200.5 }]
    frenos {
        precios: lista
        prohibido: ["descuento", "garantía extendida"]
        largo: 120
        reserva: "Eso te lo confirma una persona, ya te paso."
        %s
    }
    al recibir Consulta como c {
        responder consultar_ia("Atendés un almacén.", c.pregunta, "Hola.")
    }
}
funcion consultar(pregunta) {
    devolver preguntar Consulta { pregunta: pregunta } a Mostrador
}
"""


def hoy_iso():
    import datetime
    return datetime.date.today().isoformat()


@pytest.mark.parametrize("texto,esperado", [
    ("Sale $ 3.500", [3500]), ("sale $3500.", [3500]), ("son $3.500,00 cada una", [3500]),
    ("$ 3.500.-", [3500]), ("AR$ 1.234.567,89", [1234567.89]), ("3500 pesos", [3500]),
    ("3.500 pesos y 1 peso", [3500, 1]), ("3500$", [3500]), ("3 mil pesos", [3000]),
    ("$ 2 millones", [2000000]), ("dos por 2 millones de pesos", [2000000]),
    ("sale 3500 por unidad", [3500]), ("cuesta 3.500", [3500]), ("vale 4000.", [4000]),
    ("el precio es de 1200 la bolsa", [1200]), ("precio: 1.200,50", [1200.5]),
    ("cuesta 3500 más IVA", [3500]), ("la yerba $ 3.500 y el azúcar $ 1.200,50", [3500, 1200.5]),
    ("$ 3,5", [3.5]), ("$ 3500.50", [3500.5]),
    # lo que NO es un importe: cantidades, teléfonos, fechas, horarios, porcentajes
    ("Hay 40 bolsones", []), ("llamá al 11 4567-8901", []), ("el 15/12/2026 a las 18:30", []),
    ("10% menos", []), ("sale 2 por 1", []), ("vale 3 puntos", []), ("sale 150 gramos", []),
    ("tenemos 3500 unidades", []), ("sale el 15/12", []), ("cuesta 20% más", []),
    ("pedido 3500 del 2026", []), ("", []),
])
def test_que_cuenta_como_un_importe_en_pesos(texto, esperado):
    vistos = mate.importes_de(texto)
    assert [min(valores) for _, valores in vistos] == esperado, vistos


def test_un_importe_dudoso_vale_si_alguna_lectura_esta_permitida():
    assert mate.importes_de("$ 3,500")[0][1] == {3.5, 3500.0}
    assert mate.importes_de("$ 3.500")[0][1] == {3500.0}  # con punto, siempre son miles
    assert mate.reglas_rotas("Sale $ 3,500", {"precios": {3500.0}}) == []
    assert mate.reglas_rotas("Sale $ 12.000", {"precios": {12.0, 3500.0}})[0][0] == "precios"
    assert mate.reglas_rotas("Sale $ 1.200,50", {"precios": {1200.5}}) == []
    (regla, motivo, leccion), = mate.reglas_rotas("$ 1, $ 2, $ 3, $ 4 y $ 1", {"precios": set()})
    assert "los importes $ 1, $ 2, $ 3 y otros, que no están entre" in motivo
    assert len(leccion) <= mate.LARGO_DE_LECCION
    assert mate.numeros_permitidos([{"p": 1, "x": "2"}, [3.5, True], 4]) == {1.0, 3.5, 4.0}


def test_los_frenos_revisan_cada_respuesta_antes_de_devolverla(tmp_path, capsys):
    codigo, salida, err = por_main(tmp_path, capsys, CON_FRENOS % "" + """
        prueba "lo que cumple pasa tal cual" {
            simular_ia("La yerba sale $ 3.500 y el azúcar 1.200,50 pesos. Hay 40.")
            asegurar consultar("¿yerba?") == "La yerba sale $ 3.500 y el azúcar 1.200,50 pesos. Hay 40."
            asegurar largo(consultas_ia()) == 1
            asegurar ultimo(consultas_ia()).freno == ""
            asegurar ultimo(consultas_ia()).devuelto == ultimo(consultas_ia()).respuesta
        }
        prueba "un precio inventado: un segundo intento y la reserva" {
            simular_ia("La yerba sale $ 9.999")
            asegurar consultar("¿yerba?") == "Eso te lo confirma una persona, ya te paso."
            sea c = consultas_ia()
            asegurar largo(c) == 2
            asegurar c[0].pregunta == "¿yerba?" y c[0].respuesta == "La yerba sale $ 9.999"
            asegurar c[0].freno == "nombró el importe $ 9.999, que no está entre los precios permitidos"
            asegurar empieza_con(c[1].pregunta, "¿yerba?\\n\\n[Aviso del sistema: tu respuesta anterior")
            asegurar tiene(c[1].pregunta, "porque nombró el importe $ 9.999")
            asegurar c[0].devuelto == c[1].devuelto y c[1].devuelto == "Eso te lo confirma una persona, ya te paso."
        }
        prueba "si el segundo intento cumple, vale ese" {
            simular_ia(["Te hago un Descuentos", "No hacemos rebajas."])
            asegurar consultar("¿precio?") == "No hacemos rebajas."
            asegurar tiene(consultas_ia()[0].freno, "prohibido") y consultas_ia()[1].freno == ""
        }
        prueba "prohibido: sin tildes ni mayúsculas, y desde el comienzo de la palabra" {
            simular_ia("Tiene GARANTIA  extendida")
            asegurar consultar("x") == "Eso te lo confirma una persona, ya te paso."
            simular_ia("Sin contradescuentos raros")
            asegurar consultar("x") == "Sin contradescuentos raros"
        }
        prueba "largo" {
            simular_ia(unir(rango(100), ""))
            asegurar consultar("x") == "Eso te lo confirma una persona, ya te paso."
            asegurar tiene(consultas_ia()[0].freno, "letras y el máximo es 120")
        }
        prueba "si el segundo intento falla, también sale la reserva" {
            simular_ia(["$ 1"])
            asegurar consultar("x") == "Eso te lo confirma una persona, ya te paso."
            asegurar largo(consultas_ia()) == 2 y ultimo(consultas_ia()).respuesta == nada
        }
    """, orden="probar")
    assert (codigo, err) == (0, ""), salida
    assert "6 de 6 pruebas pasaron" in salida
    assert archivos_de(tmp_path) == ["programa.mate"]  # 'probar' no deja nada


def test_un_agente_sin_frenos_consulta_igual_que_antes(tmp_path, capsys):
    codigo, salida, err = por_main(tmp_path, capsys, MOSTRADOR + """
        prueba "sin frenos" {
            simular_ia("Sale $ 9.999 con descuento")
            sea a = preguntar Consulta { pregunta: "¿Hay?" } a Mostrador
            asegurar a.respuesta == "Sale $ 9.999 con descuento"
            asegurar claves(ultimo(consultas_ia())) == ["agente", "instrucciones", "pregunta", "respuesta"]
        }
    """, orden="probar")
    assert (codigo, err) == (0, "") and "1 de 1 pruebas pasaron" in salida
    # 'frenos' no es una palabra de Mate: sigue sirviendo de nombre
    assert "frenos" not in mate.PALABRAS and len(mate.PALABRAS) == 36
    salida, _ = correr("""
        mensaje Ver {}
        agente A {
            estado frenos = 2
            al recibir Ver { responder frenos + 1 }
        }
        sea frenos = preguntar Ver {} a A
        mostrar(frenos)
    """)
    assert salida == ["3"]


@pytest.mark.parametrize("frenos,esperado", [
    ("frenos { presios: [1] }", "'presios' no es una regla de 'frenos'. ¿Quisiste decir 'precios'?"),
    ("frenos { largo: 10\n largo: 20 }", "la regla 'largo' está dos veces en los frenos de A"),
    ("frenos { }", "estos 'frenos' están vacíos"),
    ("frenos { largo: 10 }\n frenos { largo: 20 }", "A ya tiene sus 'frenos' (línea 4)"),
    ("frenos { largo:\n 10 }", "a la regla 'largo' le falta el valor, en el mismo renglón"),
    ("frenos { 10 }", "dentro de 'frenos' va una regla por renglón"),
    ("frenos { largo: \"mucho\"\n reserva: \"x\" }", "'largo' no lleva un texto"),
    ("frenos { reserva: 5 }", "'reserva' no lleva un número"),
    ("frenos { prohibido: \"descuento\"\n reserva: \"x\" }", "'prohibido' no lleva un texto"),
    ("frenos { consultas_por_dia: nada }", "'consultas_por_dia' no lleva el valor nada"),
    ("frenos { precios: [1] }", "a los frenos de A les falta 'reserva'"),
    ("frenos { largo: totl\n reserva: \"x\" }", "'totl'"),
    ("frenos: 5", "dentro de un agente solo van 'estado', 'al recibir', 'funcion' y 'frenos'"),
])
def test_los_frenos_mal_escritos_se_avisan_antes_de_correr(frenos, esperado):
    error = falla("""
        mensaje Ver {}
        agente A {
            %s
            al recibir Ver { responder consultar_ia("", "hola", "Hola.") }
        }
    """ % frenos)
    assert esperado in error.mensaje, error.mensaje


@pytest.mark.parametrize("regla,esperado", [
    ("largo: cuanto", "en los frenos de A, 'largo' recibió un texto y lleva otra cosa"),
    ("largo: cero", "'largo' lleva un número entero mayor que cero y recibió 0"),
    ("consultas_por_dia: dos_y_medio", "'consultas_por_dia' lleva un número entero y recibió 2.5"),
    ("prohibido: [1, 2]", "'prohibido' lleva una lista de textos"),
    ("prohibido: [\"\"]", "'prohibido' lleva una lista de textos"),
    ("reserva: vacio", "'reserva' está vacía"),
    ("precios: cuanto", "'precios' recibió un texto y lleva otra cosa"),
    ("largo: consultar_ia(\"\", \"a\", \"b\")", "dentro de 'frenos' no se puede consultar a la IA"),
])
def test_un_freno_con_un_valor_que_no_va_falla_al_consultar_y_dice_el_renglon(regla, esperado):
    fuente = """
        mensaje Ver {}
        agente A {
            estado cuanto = "mucho"
            estado vacio = "  "
            estado numeros = [0, 2.5]
            frenos {
                reserva: "x"
                %s
            }
            al recibir Ver { responder consultar_ia("", "hola", "Hola.") }
        }
        prueba "p" { mostrar(preguntar Ver {} a A) }
    """ % regla.replace("cero", "numeros[0]").replace("dos_y_medio", "numeros[1]")
    if regla.startswith("reserva"):
        fuente = fuente.replace('reserva: "x"\n', "")
    programa = mate.analizar(fuente)
    assert mate.verificar(programa) == []
    (_, error), = mate.Interprete().correr(programa, pruebas=True)
    assert esperado in error and ("línea 8" in error or "línea 9" in error), error


def test_la_reserva_que_queda_en_nada_es_un_error_claro():
    programa = mate.analizar("""
        mensaje Ver {}
        agente A {
            estado texto_de_reserva = nada
            frenos {
                largo: 10
                reserva: texto_de_reserva
            }
            al recibir Ver { responder consultar_ia("", "hola", "Hola.") }
        }
        prueba "p" { mostrar(preguntar Ver {} a A) }
    """)
    (_, error), = mate.Interprete().correr(programa, pruebas=True)
    assert "a los frenos de A les falta 'reserva' (quedó en nada)" in error


def test_al_correr_el_freno_queda_en_la_traza_la_bitacora_y_como_propuesta(tmp_path, capsys):
    fuente = CON_FRENOS % "" + """
        mostrar(consultar("¿Cuánto sale la yerba?"))
    """
    (tmp_path / "respuestas.txt").write_text(
        "yerba => La yerba sale $ 9.999\n* => Hola.\n", encoding="utf-8")
    codigo, salida, err = por_main(tmp_path, capsys, fuente, "--traza",
                                   f"--ia-simulada={tmp_path / 'respuestas.txt'}")
    assert codigo == 0
    renglones = [r.strip(" ·") for r in salida.splitlines()]
    assert ("freno de Mostrador: la respuesta no pasa (nombró el importe $ 9.999, que no está "
            "entre los precios permitidos). Consulta una vez más") in renglones
    assert ("freno de Mostrador: el segundo intento tampoco pasa (nombró el importe $ 9.999, "
            "que no está entre los precios permitidos). Devuelve el texto de reserva: "
            f'"{RESERVA}"') in renglones
    assert renglones[-1] == RESERVA
    assert err.startswith("aviso: saltó un freno de Mostrador y quedó una lección propuesta")
    assert "propuestas" in err and str(tmp_path / "programa.mate") in err
    assert archivos_de(tmp_path) == ["programa.bitacora.txt", "programa.mate",
                                     "programa.memoria.json", "respuestas.txt"]
    bitacora = (tmp_path / "programa.bitacora.txt").read_text(encoding="utf-8-sig")
    (renglon,) = [r for r in bitacora.splitlines() if r and not r.startswith("#")]
    partes = renglon.split(" | ")
    assert partes[1:4] == ["Mostrador", "saltó un freno (contestó con el texto de reserva)",
                           'la consulta "¿Cuánto sale la yerba?"']
    assert partes[4] == ("nombró el importe $ 9.999, que no está entre los precios permitidos. "
                         'La IA había contestado: "La yerba sale $ 9.999"')
    ficha = memoria_de(tmp_path)["agentes"]["Mostrador"]
    assert ficha["lecciones"] == [] and ficha["estado"] == {}
    (propuesta,) = ficha["propuestas"]
    assert propuesta["texto"].startswith("No nombres ningún importe que no esté en los precios")
    assert "saltó un freno: nombró el importe $ 9.999" in propuesta["motivo"]
    assert ficha["gasto"] == {hoy_iso(): {"consultas": 0, "simuladas": 2, "tokens": 0}}
    # otra corrida igual: la propuesta no se repite, y ya no avisa
    codigo, salida, err = por_main(tmp_path, capsys, fuente,
                                   f"--ia-simulada={tmp_path / 'respuestas.txt'}")
    assert (codigo, salida, err) == (0, RESERVA + "\n", "")
    ficha = memoria_de(tmp_path)["agentes"]["Mostrador"]
    assert len(ficha["propuestas"]) == 1 and ficha["gasto"][hoy_iso()]["simuladas"] == 4
    # una respuesta que pasa no deja nada en la bitácora
    (tmp_path / "respuestas.txt").write_text("* => Sale $ 3.500\n", encoding="utf-8")
    codigo, salida, err = por_main(tmp_path, capsys, fuente,
                                   f"--ia-simulada={tmp_path / 'respuestas.txt'}")
    assert (codigo, salida, err) == (0, "Sale $ 3.500\n", "")
    assert len((tmp_path / "programa.bitacora.txt").read_text(encoding="utf-8-sig")
               .strip().splitlines()) == 7  # (4 de título, uno vacío y los 2 frenos)


def test_un_programa_con_frenos_que_no_consulta_no_crea_archivos(tmp_path, capsys):
    codigo, salida, err = por_main(tmp_path, capsys, CON_FRENOS % "" + 'mostrar("listo")')
    assert (codigo, salida, err) == (0, "listo\n", "")
    assert archivos_de(tmp_path) == ["programa.mate"]


def test_con_la_ia_de_verdad_el_segundo_intento_lleva_el_aviso_y_se_cuentan_los_tokens(
        tmp_path, capsys, ia):
    ia.respuestas = [dice("Sale $ 9.999"), dice("Sale $ 3.500")]
    codigo, salida, err = por_main(tmp_path, capsys, CON_FRENOS % "" + """
        mostrar(consultar("¿Cuánto sale la yerba?"))
    """)
    assert (codigo, salida) == (0, "Sale $ 3.500\n")
    primero, segundo = ia.pedidos
    assert primero["cuerpo"]["messages"][0]["content"] == "¿Cuánto sale la yerba?"
    assert primero["cuerpo"]["system"] == "Atendés un almacén."  # (las reglas no viajan)
    dicho = segundo["cuerpo"]["messages"][0]["content"]
    assert dicho.startswith("¿Cuánto sale la yerba?\n\n[Aviso del sistema: tu respuesta anterior")
    assert "nombró el importe $ 9.999, que no está entre los precios permitidos" in dicho
    ficha = memoria_de(tmp_path)["agentes"]["Mostrador"]
    assert ficha["gasto"] == {hoy_iso(): {"consultas": 2, "simuladas": 0, "tokens": 24}}
    bitacora = (tmp_path / "programa.bitacora.txt").read_text(encoding="utf-8-sig")
    assert "saltó un freno (el segundo intento salió bien)" in bitacora
    for archivo in tmp_path.iterdir():
        assert CLAVE_DE_MENTIRA not in archivo.read_text(encoding="utf-8-sig")
    assert CLAVE_DE_MENTIRA not in salida + err


def test_el_tope_de_consultas_vale_entre_corridas_del_mismo_dia(tmp_path, capsys, ia):
    import json
    fuente = CON_FRENOS % "consultas_por_dia: 3" + """
        mostrar(consultar("uno"))
        mostrar(consultar("dos"))
    """
    codigo, salida, err = por_main(tmp_path, capsys, fuente)
    assert (codigo, salida, err) == (0, "Sí, hay yerba.\nSí, hay yerba.\n", "")
    codigo, salida, err = por_main(tmp_path, capsys, fuente, "--traza")
    assert codigo == 0 and len(ia.pedidos) == 3  # la cuarta no se hizo
    assert salida.splitlines()[-1] == RESERVA
    assert ("tope de Mostrador: ya hizo 3 consulta(s) a la IA hoy y su tope es 3 por día. No "
            "consulta y devuelve el texto de reserva") in salida
    assert memoria_de(tmp_path)["agentes"]["Mostrador"]["gasto"][hoy_iso()] == {
        "consultas": 3, "simuladas": 0, "tokens": 36}
    bitacora = (tmp_path / "programa.bitacora.txt").read_text(encoding="utf-8-sig")
    assert bitacora.count("llegó al tope de gasto") == 1
    # con --ia-simulada lleva una cuenta aparte: se puede ver el tope sin gastar
    codigo, salida, err = por_main(tmp_path, capsys, fuente + """
        mostrar(consultar("tres"))
        mostrar(consultar("cuatro"))
    """, "--ia-simulada")
    assert (codigo, salida) == (0, f"Hola.\nHola.\nHola.\n{RESERVA}\n") and len(ia.pedidos) == 3
    assert memoria_de(tmp_path)["agentes"]["Mostrador"]["gasto"][hoy_iso()] == {
        "consultas": 3, "simuladas": 3, "tokens": 36}
    # 'probar' no mira ni toca la cuenta de verdad: cada prueba arranca de cero
    antes = (tmp_path / "programa.memoria.json").read_bytes()
    codigo, salida, err = por_main(tmp_path, capsys, CON_FRENOS % "consultas_por_dia: 3" + """
        prueba "una" {
            simular_ia("Hay.")
            asegurar consultar("a") == "Hay." y consultar("b") == "Hay." y consultar("c") == "Hay."
            asegurar consultar("d") == "Eso te lo confirma una persona, ya te paso."
            asegurar tiene(ultimo(consultas_ia()).freno, "tope de gasto: ya hizo 3 consulta(s) simuladas")
            asegurar ultimo(consultas_ia()).respuesta == nada y largo(consultas_ia()) == 4
        }
        prueba "otra, de cero" {
            simular_ia("Hay.")
            asegurar consultar("a") == "Hay."
        }
    """, orden="probar")
    assert (codigo, err) == (0, "") and "2 de 2 pruebas pasaron" in salida
    assert (tmp_path / "programa.memoria.json").read_bytes() == antes
    # al otro día arranca de cero (y lo de ayer queda para la cuenta)
    memoria = memoria_de(tmp_path)
    gasto = memoria["agentes"]["Mostrador"]["gasto"]
    gasto["2026-01-05"] = gasto.pop(hoy_iso())
    (tmp_path / "programa.memoria.json").write_text(json.dumps(memoria), encoding="utf-8")
    codigo, salida, err = por_main(tmp_path, capsys, fuente)
    assert (codigo, salida) == (0, "Sí, hay yerba.\nSí, hay yerba.\n") and len(ia.pedidos) == 5
    assert sorted(memoria_de(tmp_path)["agentes"]["Mostrador"]["gasto"]) == sorted(
        ["2026-01-05", hoy_iso()])


def test_el_tope_de_tokens_y_el_tope_sin_reserva(tmp_path, capsys, ia):
    fuente = """
        mensaje Consulta { pregunta: texto }
        agente Mostrador {
            frenos { tokens_por_dia: 20 }
            al recibir Consulta como c { responder consultar_ia("", c.pregunta, "Hola.") }
        }
        para i en rango(4) {
            intentar {
                mostrar(preguntar Consulta { pregunta: "¿Hay?" } a Mostrador)
            } si falla e {
                mostrar(detalle_de(e).clase, e)
            }
        }
    """
    codigo, salida, err = por_main(tmp_path, capsys, fuente)
    assert codigo == 0 and len(ia.pedidos) == 2  # 12 tokens cada una: la tercera ya no va
    renglones = salida.splitlines()
    assert renglones[:2] == ["Sí, hay yerba.", "Sí, hay yerba."]
    assert renglones[2].startswith("tope consultar_ia(): Mostrador ya gastó 24 tokens hoy y su "
                                   "tope es 20 por día: por hoy no consulta más.")
    assert "ponele una 'reserva'" in renglones[2]
    # con --ia-simulada no hay tokens: ese tope no salta
    codigo, salida, err = por_main(tmp_path, capsys, fuente, "--ia-simulada")
    assert (codigo, salida) == (0, "Hola.\n" * 4)


def test_el_segundo_intento_tambien_cuenta_para_el_tope(tmp_path, capsys):
    codigo, salida, err = por_main(tmp_path, capsys, CON_FRENOS % "consultas_por_dia: 1" + """
        prueba "sin lugar para el segundo intento" {
            simular_ia("Sale $ 9.999")
            asegurar consultar("a") == "Eso te lo confirma una persona, ya te paso."
            asegurar largo(consultas_ia()) == 1
            asegurar tiene(consultas_ia()[0].freno, "$ 9.999")
        }
    """, orden="probar")
    assert (codigo, err) == (0, "") and "1 de 1 pruebas pasaron" in salida


def test_las_copias_cuentan_con_el_agente_original(tmp_path, capsys):
    fuente = CON_FRENOS % "consultas_por_dia: 2" + """
        sea centro = crear Mostrador llamado "Centro"
        sea norte = crear Mostrador llamado "Norte"
        mostrar(preguntar Consulta { pregunta: "a" } a centro)
        mostrar(preguntar Consulta { pregunta: "b" } a norte)
        mostrar(preguntar Consulta { pregunta: "c" } a Mostrador)
    """
    codigo, salida, err = por_main(tmp_path, capsys, fuente, "--ia-simulada")
    assert (codigo, salida) == (0, f"Hola.\nHola.\n{RESERVA}\n")
    agentes = memoria_de(tmp_path)["agentes"]
    assert list(agentes) == ["Mostrador"] and agentes["Mostrador"]["gasto"][hoy_iso()][
        "simuladas"] == 2


def test_la_cuenta_de_consultas_de_verdad_se_guarda_en_el_momento(tmp_path, capsys, ia,
                                                                 monkeypatch):
    visto = []

    def teclear(_pregunta):  # entre una consulta y la otra: ¿ya está en el disco?
        visto.append(memoria_de(tmp_path)["agentes"]["Mostrador"])
        return "seguir"

    monkeypatch.setattr(mate, "por_teclado", teclear)
    codigo, salida, err = por_main(tmp_path, capsys, """
        mensaje Consulta { pregunta: texto }
        agente Mostrador {
            estado recordado atendidos = 0
            frenos { consultas_por_dia: 10 }
            al recibir Consulta como c {
                atendidos += 1
                responder consultar_ia("", c.pregunta)
            }
        }
        mostrar(preguntar Consulta { pregunta: "uno" } a Mostrador)
        leer("¿Sigo?")
        mostrar(preguntar Consulta { pregunta: "dos" } a Mostrador)
    """)
    assert (codigo, err) == (0, "")
    # en el medio está la cuenta; lo que el agente recuerda se guarda al final, como siempre
    assert visto == [{"estado": {}, "lecciones": [], "gasto": {
        hoy_iso(): {"consultas": 1, "simuladas": 0, "tokens": 12}}}]
    assert memoria_de(tmp_path)["agentes"]["Mostrador"] == {
        "estado": {"atendidos": 2}, "lecciones": [],
        "gasto": {hoy_iso(): {"consultas": 2, "simuladas": 0, "tokens": 24}}}


def test_la_memoria_tolera_cuentas_y_propuestas_mal_escritas(tmp_path):
    import json
    archivo = tmp_path / "programa.memoria.json"
    archivo.write_text(json.dumps({"agentes": {"Mostrador": {
        "estado": {}, "lecciones": [],
        "propuestas": ["suelta", {"texto": " "}, {"texto": "Vale", "fecha": 5}, 7],
        "gasto": {"ayer": {"consultas": 1}, "2026-11-20": {"consultas": "3"},
                  "2026-11-21": {"consultas": 2, "tokens": 9}, "2026-11-19": [], "2026-11-18": {}},
    }, "Otro": {"estado": {}, "lecciones": [], "propuestas": "nada", "gasto": 5}}}),
        encoding="utf-8")
    memoria, avisos = mate.leer_memoria(str(archivo))
    assert avisos == []
    assert memoria == {
        "Mostrador": {"estado": {}, "lecciones": [],
                      "propuestas": [{"fecha": "", "texto": "Vale", "motivo": ""}],
                      "gasto": {"2026-11-21": {"consultas": 2, "simuladas": 0, "tokens": 9}}},
        "Otro": {"estado": {}, "lecciones": []}}
    # se guardan los últimos DIAS_DE_GASTO días
    muchos = {f"2026-{mes:02}-{dia:02}": {"consultas": 1} for mes in (9, 10) for dia in range(1, 29)}
    assert len(mate.gasto_limpio(muchos)) == mate.DIAS_DE_GASTO == 30
    assert min(mate.gasto_limpio(muchos)) == "2026-09-27"
    assert mate.tokens_de({"usage": {"input_tokens": 5, "output_tokens": 7}}) == 12
    assert mate.tokens_de({"usage": {"input_tokens": "5"}}) is None and mate.tokens_de({}) is None


def con_propuestas(tmp_path, capsys):
    """Un programa al que ya le saltaron dos frenos distintos: quedan dos propuestas."""
    archivo = tmp_path / "programa.mate"
    (tmp_path / "respuestas.txt").write_text(
        "yerba => La yerba sale $ 9.999\nprecio => Te hago un descuento\n* => Hola.\n",
        encoding="utf-8")
    fuente = CON_FRENOS % "" + """
        mostrar(consultar("¿Cuánto sale la yerba?"))
        mostrar(consultar("¿Me hacés precio?"))
    """
    assert por_main(tmp_path, capsys, fuente,
                    f"--ia-simulada={tmp_path / 'respuestas.txt'}")[0] == 0
    return archivo


def test_la_orden_propuestas_muestra_aprueba_y_descarta(tmp_path, capsys):
    archivo = con_propuestas(tmp_path, capsys)
    codigo, salida, err = orden_mate(capsys, "propuestas", archivo)
    assert (codigo, err) == (0, "")
    renglones = salida.splitlines()
    assert renglones[0] == ("Lecciones propuestas, sin aprobar (2). Ningún agente las usa "
                            "todavía:")
    assert renglones[1].startswith("  1. Para Mostrador: No nombres ningún importe")
    assert renglones[2].startswith("       Por qué: saltó un freno: nombró el importe $ 9.999")
    assert renglones[3].startswith('  2. Para Mostrador: No hables de "descuento"')
    assert f"propuestas {archivo} aprobar 1" in salida and "descartar 1" in salida
    # sin aprobar, no viajan en las consultas
    assert orden_mate(capsys, "lecciones", archivo)[1].startswith(
        "Los agentes de programa.mate todavía no tienen lecciones.")
    # errores de uso
    for argumentos, esperado in [
            (["borrar", "1"], "después del programa va 'aprobar' o 'descartar'"),
            (["aprobar"], "a 'aprobar' le falta el número de la propuesta (del 1 al 2"),
            (["aprobar", "3"], "y recibió '3'"), (["descartar", "uno"], "y recibió 'uno'"),
            (["aprobar", "1", "todas"], "y recibió '1 todas'")]:
        codigo, salida, err = orden_mate(capsys, "propuestas", archivo, *argumentos)
        assert codigo == 2 and esperado in err, err
    assert len(memoria_de(tmp_path)["agentes"]["Mostrador"]["propuestas"]) == 2
    # aprobar: pasa a ser una lección
    codigo, salida, err = orden_mate(capsys, "propuestas", archivo, "aprobar", "2")
    assert (codigo, err) == (0, "")
    assert salida.startswith("Listo: aprobé 1 propuesta.")
    assert '  1. No hables de "descuento"' in salida and "Quedan 1 propuesta(s)" in salida
    ficha = memoria_de(tmp_path)["agentes"]["Mostrador"]
    assert [leccion["texto"][:9] for leccion in ficha["lecciones"]] == ["No hables"]
    assert len(ficha["propuestas"]) == 1
    # descartar: se va sin dejar rastro
    codigo, salida, err = orden_mate(capsys, "propuestas", archivo, "descartar", "todas")
    assert (codigo, salida, err) == (0, "Listo: descarté 1 propuesta. Quedan 0 sin aprobar.\n", "")
    assert "propuestas" not in memoria_de(tmp_path)["agentes"]["Mostrador"]
    codigo, salida, err = orden_mate(capsys, "propuestas", archivo)
    assert codigo == 0 and salida.startswith("programa.mate no tiene lecciones propuestas.")
    assert orden_mate(capsys, "propuestas", archivo, "aprobar", "1")[0] == 2
    codigo, salida, err = orden_mate(capsys, "propuestas")
    assert codigo == 2 and "a 'propuestas' le falta el programa" in err
    # la aprobada no se vuelve a proponer cuando el mismo freno salta de nuevo
    assert por_main(tmp_path, capsys, archivo.read_text(encoding="utf-8"),
                    f"--ia-simulada={tmp_path / 'respuestas.txt'}")[0] == 0
    ficha = memoria_de(tmp_path)["agentes"]["Mostrador"]
    assert [p["texto"][:10] for p in ficha["propuestas"]] == ["No nombres"]


def test_una_propuesta_no_se_usa_hasta_que_se_aprueba(tmp_path, capsys, ia):
    archivo = con_propuestas(tmp_path, capsys)
    fuente = CON_FRENOS % "" + 'mostrar(consultar("¿Hay?"))'
    assert por_main(tmp_path, capsys, fuente)[0] == 0
    assert ia.pedidos[-1]["cuerpo"]["system"] == "Atendés un almacén."
    assert orden_mate(capsys, "propuestas", archivo, "aprobar", "1", "2")[0] == 0
    assert por_main(tmp_path, capsys, fuente)[0] == 0
    instrucciones = ia.pedidos[-1]["cuerpo"]["system"]
    assert mate.TITULO_DE_LECCIONES in instrucciones
    assert "1. No nombres ningún importe" in instrucciones and '2. No hables de "descuento"' \
        in instrucciones


def test_aprobar_respeta_el_tope_de_lecciones(tmp_path, capsys, monkeypatch):
    monkeypatch.setattr(mate, "MAX_LECCIONES", 2)
    archivo = con_propuestas(tmp_path, capsys)
    assert orden_mate(capsys, "corregir", archivo, "Mostrador", "Vieja")[0] == 0
    assert orden_mate(capsys, "corregir", archivo, "Mostrador", 'No hables de "descuento": de '
                      "eso acá no se habla. Si te lo preguntan, decí que lo ve una persona.")[0] == 0
    codigo, salida, err = orden_mate(capsys, "propuestas", archivo, "aprobar", "todas")
    assert (codigo, err) == (0, "") and salida.startswith("Listo: aprobé 2 propuestas.")
    assert "(1 ya estaba(n) entre las lecciones: no se repite(n).)" in salida
    assert "(El tope es 2 lecciones por agente: para anotar estas se borró la más vieja.)" in salida
    textos = [leccion["texto"][:10] for leccion in memoria_de(tmp_path)["agentes"]["Mostrador"][
        "lecciones"]]
    assert textos == ["No hables ", "No nombres"]


def test_las_propuestas_tienen_tope(monkeypatch):
    monkeypatch.setattr(mate, "MAX_PROPUESTAS", 3)
    propuestas = []
    for n in range(5):
        propuestas = mate.sumar_propuesta(propuestas, [], f"Lección {n}", "motivo", "hoy")
    assert [p["texto"] for p in propuestas] == ["Lección 2", "Lección 3", "Lección 4"]
    assert mate.sumar_propuesta(propuestas, [], "Lección 3", "otro", "hoy") is propuestas
    assert mate.sumar_propuesta(propuestas, [{"texto": "Ya aprobada"}], "Ya aprobada", "m",
                                "hoy") is propuestas


def test_proponer_redacta_la_leccion_y_la_deja_sin_aprobar(tmp_path, capsys, ia):
    archivo = tmp_path / "programa.mate"
    archivo.write_text(MOSTRADOR, encoding="utf-8")
    # sin clave: una redacción fija, y lo dice
    import os
    clave = os.environ.pop("ANTHROPIC_API_KEY")
    try:
        codigo, salida, err = orden_mate(capsys, "proponer", archivo, "mostrador",
                                         "Ofreció envíos y no hacemos envíos.")
    finally:
        os.environ["ANTHROPIC_API_KEY"] = clave
    assert (codigo, err) == (0, "") and ia.pedidos == []
    assert salida.splitlines()[:3] == [
        "Quedó propuesta para Mostrador (todavía NO la usa: falta que la apruebes):",
        "  1. Una respuesta tuya estuvo mal: Ofreció envíos y no hacemos envíos. No lo repitas.",
        "Es una redacción fija: no hay clave para la IA (con la clave puesta en "
        "ANTHROPIC_API_KEY la redacta la IA, y esa consulta se paga)."]
    assert f"propuestas {archivo} aprobar 1" in salida and f"corregir {archivo} Mostrador" in salida
    ficha = memoria_de(tmp_path)["agentes"]["Mostrador"]
    assert ficha["lecciones"] == [] and "gasto" not in ficha
    assert ficha["propuestas"][0]["motivo"] == "lo dijo el dueño: Ofreció envíos y no hacemos envíos."
    # con clave: la redacta la IA, se avisa que se paga y entra en la cuenta del día
    ia.respuestas = [dice('"No ofrezcas envíos:\n el negocio no los hace."')]
    codigo, salida, err = orden_mate(capsys, "proponer", archivo, "Mostrador",
                                     "Ofreció envíos y no hacemos envíos", "Te lo mando mañana")
    assert (codigo, err) == (0, "")
    assert "  2. No ofrezcas envíos: el negocio no los hace." in salida
    assert "La redactó la IA (fue una consulta de verdad, paga)." in salida
    (pedido,) = ia.pedidos
    assert pedido["cuerpo"]["system"] == mate.INSTRUCCIONES_PARA_REDACTAR
    assert pedido["cuerpo"]["messages"][0]["content"] == (
        "Lo que estuvo mal, según el dueño: Ofreció envíos y no hacemos envíos\n"
        "Lo que había contestado el asistente: Te lo mando mañana")
    ficha = memoria_de(tmp_path)["agentes"]["Mostrador"]
    assert ficha["gasto"] == {hoy_iso(): {"consultas": 1, "simuladas": 0, "tokens": 12}}
    assert len(ficha["propuestas"]) == 2 and ficha["lecciones"] == []
    assert CLAVE_DE_MENTIRA not in salida + (tmp_path / "programa.memoria.json").read_text(
        encoding="utf-8-sig")
    # si la IA se va de largo, o no contesta, va la redacción fija
    ia.respuestas = [dice("muy largo " * 40)]
    codigo, salida, err = orden_mate(capsys, "proponer", archivo, "Mostrador", "Dijo otra cosa")
    assert codigo == 0 and "  3. Una respuesta tuya estuvo mal: Dijo otra cosa. No lo repitas." in salida
    assert "lo que redactó la IA estaba vacío o pasaba las 300 letras" in salida
    ia.respuestas = [error_http(401, "authentication_error", f"invalid {CLAVE_DE_MENTIRA}")]
    codigo, salida, err = orden_mate(capsys, "proponer", archivo, "Mostrador", "Y otra más")
    assert codigo == 0 and "porque la IA no contestó: consultar_ia(): la clave no sirve" in salida
    assert CLAVE_DE_MENTIRA not in salida + err
    # --ia-simulada: nunca sale a la red
    antes = len(ia.pedidos)
    (tmp_path / "respuestas.txt").write_text("saludó => Saludá siempre.\n", encoding="utf-8")
    codigo, salida, err = orden_mate(capsys, "proponer", archivo, "Mostrador", "No saludó",
                                     f"--ia-simulada={tmp_path / 'respuestas.txt'}")
    assert codigo == 0 and "  5. Saludá siempre." in salida and "IA simulada" in salida
    codigo, salida, err = orden_mate(capsys, "proponer", archivo, "Mostrador", "Fue seco",
                                     "--ia-simulada")
    assert codigo == 0 and "con --ia-simulada sola no hay IA" in salida
    assert len(ia.pedidos) == antes
    # la misma no se propone dos veces
    codigo, salida, err = orden_mate(capsys, "proponer", archivo, "Mostrador", "Fue seco",
                                     "--ia-simulada")
    assert codigo == 0 and salida.startswith("Mostrador ya tenía esa lección")
    assert len(memoria_de(tmp_path)["agentes"]["Mostrador"]["propuestas"]) == 6
    # y lo que falta o sobra se explica
    for argumentos, esperado in [
            ([], "a 'proponer' le falta el programa"),
            ([archivo], "a 'proponer' le faltan el agente y qué estuvo mal"),
            ([archivo, "Mostrador"], "a 'proponer' le faltan el agente y qué estuvo mal"),
            ([archivo, "Mostrado", "x"], "no tiene un agente 'Mostrado'. ¿Quisiste decir 'Mostrador'?"),
            ([archivo, "Mostrador", "a", "b", "c"], "nada más"),
            ([archivo, "Mostrador", "largo " * 60], "tiene 359 letras y el tope es 220")]:
        codigo, salida, err = orden_mate(capsys, "proponer", *argumentos, "--ia-simulada")
        assert codigo == 2 and esperado in err, err
    assert len(ia.pedidos) == antes


def test_la_bitacora_muestra_cuanto_consulto_cada_agente(tmp_path, capsys):
    import datetime
    import json
    archivo = tmp_path / "programa.mate"
    archivo.write_text(CON_FRENOS % "", encoding="utf-8")
    hoy = datetime.date.today()
    ayer = hoy - datetime.timedelta(days=1)
    (tmp_path / "programa.memoria.json").write_text(json.dumps({"agentes": {"Mostrador": {
        "estado": {}, "lecciones": [], "gasto": {
            hoy.isoformat(): {"consultas": 12, "simuladas": 4, "tokens": 8450},
            ayer.isoformat(): {"consultas": 1, "simuladas": 0, "tokens": 22300},
            "2026-01-02": {"consultas": 30, "simuladas": 0, "tokens": 0}}}}}), encoding="utf-8")
    codigo, salida, err = orden_mate(capsys, "bitacora", archivo)
    assert (codigo, err) == (0, "")
    renglones = salida.splitlines()
    assert renglones[0] == "programa.mate no tiene fallas anotadas."
    assert renglones[2] == ("Consultas a la IA (la cuenta la llevan los agentes que tienen "
                            "'frenos'):")
    assert renglones[3] == "  Mostrador"
    assert renglones[4] == ("    hoy:              12 consultas, 8.450 tokens  (y 4 simuladas, "
                            "que no se pagan)")
    assert renglones[5] == f"    {ayer.strftime('%d/%m/%Y')}:       1 consulta, 22.300 tokens"
    assert renglones[6].startswith("    últimos 3 día(s) con consultas (se guardan 30): "
                                   "43 consultas, 30.750 tokens")
    # con fallas anotadas, la cuenta va al final
    assert por_main(tmp_path, capsys, CON_FRENOS % "" + 'mostrar(consultar("¿yerba?"))',
                    "--ia-simulada")[0] == 0
    (tmp_path / "programa.bitacora.txt").write_text(
        "01/01/2026 10:00 | Mostrador | falló | Consulta {} | algo\n", encoding="utf-8")
    codigo, salida, err = orden_mate(capsys, "bitacora", archivo)
    assert codigo == 0 and salida.startswith("Bitácora de programa.mate: 1 falla(s)")
    assert salida.index("Las últimas:") < salida.index("Consultas a la IA") < salida.index(
        "Está todo en")
    # un programa sin frenos ve la bitácora como siempre
    otro = tmp_path / "otro.mate"
    otro.write_text(MOSTRADOR, encoding="utf-8")
    codigo, salida, err = orden_mate(capsys, "bitacora", otro)
    assert codigo == 0 and "Consultas a la IA" not in salida
    assert "La bitácora se arma sola" in salida


def test_el_ejemplo_del_mostrador_con_frenos(tmp_path, capsys, ia):
    import shutil
    original = RAIZ / "ejemplos" / "11_mostrador_con_frenos.mate"
    en_la_carpeta = archivos_de(RAIZ / "ejemplos")
    codigo, salida, err = orden_mate(capsys, "probar", original)
    assert (codigo, err) == (0, "") and "6 de 6 pruebas pasaron" in salida and ia.pedidos == []
    assert archivos_de(RAIZ / "ejemplos") == en_la_carpeta  # 'probar' no deja nada
    ruta = shutil.copy(original, tmp_path / original.name)
    shutil.copy(RAIZ / "ejemplos" / "precios.csv", tmp_path)
    codigo, salida, err = orden_mate(capsys, "correr", ruta, "--ia-simulada", "--traza")
    assert codigo == 0 and ia.pedidos == []
    reserva = "Eso te lo confirma una persona. Ya te paso con alguien."
    visto = [r for r in salida.splitlines() if r.startswith(("Cliente:", "Mostrador:"))]
    assert visto == [
        "Cliente:   ¿Cuánto sale el bolsón de yerba?", "Mostrador: El bolsón de yerba sale $ 35.000.",
        "Cliente:   ¿Y el café?", f"Mostrador: {reserva}",
        "Cliente:   ¿Me hacés precio si llevo dos?", f"Mostrador: {reserva}"]
    assert "freno de Mostrador: la respuesta no pasa (nombró el importe $ 12.000" in salida
    assert f'Devuelve el texto de reserva: "{reserva}"' in salida
    assert "$ 12.000" not in "\n".join(visto)  # el precio inventado no le llegó al cliente
    ficha = memoria_de(tmp_path, "11_mostrador_con_frenos")["agentes"]["Mostrador"]
    assert len(ficha["propuestas"]) == 2 and ficha["gasto"][hoy_iso()]["simuladas"] == 5
    codigo, salida, err = orden_mate(capsys, "propuestas", ruta)
    assert codigo == 0 and "Lecciones propuestas, sin aprobar (2)" in salida
    # con la IA de verdad, lo que ella diga pasa por los mismos frenos
    ia.respuestas = [dice("El bolsón sale $ 35.000."), dice("El café sale $ 99."),
                     dice("Café no trabajamos."), dice("No hacemos rebajas."),
                     dice("Todo sale lo que dice la lista.")]
    codigo, salida, err = orden_mate(capsys, "correr", ruta)
    assert codigo == 0 and len(ia.pedidos) == 5
    assert "Mostrador: Café no trabajamos." in salida
    # ("rebajas" está entre lo prohibido: el segundo intento, que cumple, es el que llega)
    assert "Mostrador: Todo sale lo que dice la lista." in salida and "rebajas" not in salida


def test_la_documentacion_cuenta_los_frenos(capsys):
    leeme = (RAIZ / "README.md").read_text(encoding="utf-8")
    for frase in ["## Frenos", "### Qué pasa cuando un freno salta", "### Tope de gasto",
                  "### Lecciones propuestas", "### El freno de precios, con detalle",
                  "### Lo que los frenos no hacen", "`11_mostrador_con_frenos.mate`",
                  "once programas cortos", "consultas_por_dia: 100", "tokens_por_dia",
                  "python mate\\mate.py propuestas mi_mostrador.mate aprobar 1",
                  "python mate\\mate.py proponer mi_mostrador.mate Mostrador",
                  "**Una propuesta no se usa hasta que la aprobás.**",
                  "**Mate no calcula plata**", "| `propuestas archivo.mate` |",
                  "**no gastaron nada**", '`"tope"`']:
        assert frase in leeme, frase
    # lo que el README muestra de la traza y de las órdenes es lo que Mate dice de verdad
    assert "Lecciones propuestas, sin aprobar (1). Ningún agente las usa todavía:" in leeme
    assert ("freno de Mostrador: la respuesta no pasa (nombró el importe $ 12.000, que no está "
            "entre los precios permitidos). Consulta una vez más") in leeme
    for regla, (_, ejemplo, _) in mate.REGLAS_DE_FRENO.items():
        assert f"| `{regla}` |" in leeme, regla
    guia = mate.texto_de_guia()
    for frase in ["FRENOS: reglas que el agente declara", "consultas_por_dia: 100",
                  'reserva: "Eso te lo confirma una persona, ya te paso."', '"tope"',
                  "propuestas programa.mate aprobar 1", "freno (qué regla rompió",
                  'python mate\\mate.py proponer archivo.mate Agente "qué estuvo mal"']:
        assert frase in guia, frase
    for regla in mate.REGLAS_DE_FRENO:
        assert regla in guia and regla in mate.ayuda_de("frenos"), regla
    ayuda = mate.texto_de_ayuda()
    for frase in ["frenos { ... }", "propuestas archivo.mate aprobar 1", "proponer  archivo.mate"]:
        assert frase in ayuda, frase
    for texto in [ayuda, mate.ayuda_de("frenos"), guia]:
        assert max(len(r) for r in texto.splitlines()) <= 100
    assert mate.main(["ayuda", "reserva"]) == 0
    assert capsys.readouterr().out.startswith("reserva (va con 'frenos')")
    assert mate.main(["propuesta"]) == 2
    assert "¿quisiste decir 'propuestas'?" in capsys.readouterr().err
    mejoras = (RAIZ / "MEJORAS.md").read_text(encoding="utf-8")
    for frase in ["**114. Frenos para la IA**",
                  "**115. Tope de gasto por día y la cuenta de consultas**",
                  "**116. Lecciones propuestas: Mate las redacta y el dueño las aprueba**",
                  "siguen siendo 36 de 40 y 48 de 48"]:
        assert frase in mejoras, frase
    assert mate.TOPE_DE_FUNCIONES == 48 == len(mate.FUNCIONES) and len(mate.PALABRAS) == 36
    ejemplo = (RAIZ / "ejemplos" / "11_mostrador_con_frenos.mate").read_text(encoding="utf-8")
    for frase in ["python mate\\mate.py correr mate\\ejemplos\\11_mostrador_con_frenos.mate "
                  "--ia-simulada --traza",
                  "python mate\\mate.py propuestas mate\\ejemplos\\11_mostrador_con_frenos.mate "
                  "aprobar 1", "python mate\\mate.py bitacora"]:
        assert frase in ejemplo, frase


# ───────── 0.5: que otra persona pueda instalarlo y aprenderlo (mejoras 117 a 119) ─────────

CURSO = RAIZ / "curso"
CLASES = sorted(p.name[:-len(".md")] for p in CURSO.glob("clase_[0-9][0-9]_*.md"))
SECCIONES_DE_CLASE = ["## Qué vas a lograr", "## El programa", "## Cómo se corre",
                      "## Lo que tiene que salir", "## El error más común", "## Ejercicio",
                      "## Solución"]


def con_sangria(texto):
    """Un programa como figura en el texto de una clase: cada renglón con cuatro espacios."""
    return "\n".join("    " + r if r.strip() else "" for r in texto.rstrip("\n").split("\n"))


def copia_del_curso(tmp_path):
    import shutil
    destino = tmp_path / "curso"
    shutil.copytree(CURSO, destino, ignore=shutil.ignore_patterns(
        "*.memoria.json", "*.bitacora.txt", "consultas_atendidas.txt", "practica.mate"))
    return destino


def test_el_curso_tiene_doce_clases_completas():
    assert [c[:8] for c in CLASES] == [f"clase_{n:02d}" for n in range(1, 13)]
    indice = (CURSO / "README.md").read_text(encoding="utf-8")
    for clase in CLASES:
        texto = (CURSO / f"{clase}.md").read_text(encoding="utf-8")
        numero = int(clase[6:8])
        assert texto.startswith(f"# Clase {numero}: "), clase
        lugares = [texto.index(seccion) for seccion in SECCIONES_DE_CLASE]
        assert lugares == sorted(lugares), clase
        # el programa y la solución que muestra el texto son los de los archivos
        programa = (CURSO / f"{clase}.mate").read_text(encoding="utf-8")
        solucion = (CURSO / f"{clase[:8]}_solucion.mate").read_text(encoding="utf-8")
        assert con_sangria(programa) in texto, clase
        assert con_sangria(solucion) in texto, clase
        # el comando está en forma Windows, y los renglones entran en el Bloc de notas
        assert f"python mate\\mate.py correr mate\\curso\\{clase}.mate" in texto, clase
        assert "python3" not in texto and "mate/curso" not in texto, clase
        largos = [r for r in texto.splitlines() if len(r) > 100 and "python mate\\mate.py" not in r]
        assert largos == [], clase
        assert f"`{clase}.md`" in indice and f"`{clase}.mate`" in indice, clase
    # nada más que el curso en esa carpeta: textos, programas y los dos archivos de datos
    resto = sorted(p.name for p in CURSO.iterdir() if p.suffix not in (".md", ".mate")
                   and "memoria" not in p.name and "bitacora" not in p.name
                   and p.name != "consultas_atendidas.txt")
    assert resto == ["precios.csv", "respuestas.txt"]


@pytest.mark.parametrize("clase", CLASES)
def test_cada_clase_del_curso_verifica_prueba_y_muestra_lo_que_dice(clase, tmp_path, capsys,
                                                                     monkeypatch):
    # (en una copia: desde la clase 10, 'correr' deja la memoria y la bitácora al lado)
    curso = copia_del_curso(tmp_path)
    monkeypatch.chdir(tmp_path)
    texto = (curso / f"{clase}.md").read_text(encoding="utf-8")
    for nombre in (f"{clase}.mate", f"{clase[:8]}_solucion.mate"):
        ruta = str(curso / nombre)
        fuente = (curso / nombre).read_text(encoding="utf-8")
        assert mate.main(["verificar", ruta]) == 0, nombre
        capsys.readouterr()
        assert mate.main(["probar", ruta]) == 0, nombre
        salida = capsys.readouterr().out
        assert "✗" not in salida, nombre
        if "prueba " in fuente:
            assert re.search(r"(\d+) de \1 pruebas pasaron", salida), nombre
        opciones = ["--ia-simulada"] if "consultar_ia(" in fuente else []
        assert mate.main(["correr", ruta] + opciones) == 0, nombre
        capturado = capsys.readouterr()
        assert all(r.startswith("aviso: ") for r in capturado.err.splitlines()), nombre
        assert capturado.out.strip(), nombre
        if "leer(" not in fuente:  # (lo de una charla depende de lo que se escriba)
            for renglon in capturado.out.splitlines():
                assert "    " + renglon in texto, (nombre, renglon)
    # 'probar' no dejó nada al lado de los programas que todavía no se corrieron
    assert not list(tmp_path.rglob("consultas_atendidas.txt"))


def test_probar_el_curso_no_deja_archivos(capsys):
    antes = sorted(p.name for p in CURSO.iterdir())
    assert mate.main(["probar", str(CURSO)]) == 0
    assert re.search(r"En total: (\d+) de \1 pruebas pasaron, en 24 archivos\n$",
                     capsys.readouterr().out)
    assert sorted(p.name for p in CURSO.iterdir()) == antes


def test_la_orden_curso_lista_las_clases_y_muestra_una(tmp_path, capsys, monkeypatch):
    monkeypatch.chdir(RAIZ.parent)
    monkeypatch.delenv("MATE_ORDEN", raising=False)
    assert mate.main(["curso"]) == 0
    capturado = capsys.readouterr()
    assert capturado.err == ""
    for frase in ["El curso de Mate: 12 clases cortas", " 1. Hola, tu primer programa",
                  "12. El mostrador completo", "clase_07_lista_de_precios.md",
                  f"{mate.como_se_llama()} curso 1", "notepad ", "clase_01_hola.md",
                  f"{mate.como_se_llama()} correr ", "clase_01_hola.mate",
                  "Ninguna clase necesita clave ni internet"]:
        assert frase in capturado.out, frase
    assert max(len(r) for r in capturado.out.splitlines()) <= 100
    # las rutas se escriben cortas desde la carpeta donde está parada la persona
    assert str(RAIZ) not in capturado.out
    # ...y completas (y entre comillas si hay espacios) cuando el curso queda en otro lado
    con_espacio = tmp_path / "mis cosas" / "curso"
    con_espacio.parent.mkdir()
    import shutil
    shutil.copytree(CURSO, con_espacio)
    assert mate.orden_curso([], print, carpeta=con_espacio) == 0
    assert f'notepad "{con_espacio / "clase_01_hola.md"}"' in capsys.readouterr().out
    # 'curso 3' muestra el texto de la clase, tal cual
    assert mate.main(["curso", "3"]) == 0
    assert capsys.readouterr().out == (CURSO / "clase_03_decisiones.md").read_text(
        encoding="utf-8")
    assert mate.main(["curso", "03"]) == 0
    assert capsys.readouterr().out.startswith("# Clase 3: Que el programa decida\n")


def test_la_orden_curso_explica_lo_que_no_entiende(tmp_path, capsys, monkeypatch):
    monkeypatch.delenv("MATE_ORDEN", raising=False)
    assert mate.main(["curso", "13"]) == 2
    assert "el curso no tiene una clase 13: van del 1 al 12" in capsys.readouterr().err
    for mal in (["curso", "tres"], ["curso", "1", "2"], ["curso", "²"], ["curso", "-1"]):
        assert mate.main(mal) == 2, mal
        capturado = capsys.readouterr()
        assert capturado.out == "" and capturado.err.strip(), mal
    assert mate.main(["curso", "tres"]) == 2
    assert ("después de 'curso' va solo el número de la clase (del 1 al 12) y recibió 'tres'"
            in capsys.readouterr().err)
    assert mate.main(["cursos"]) == 2
    assert "¿quisiste decir 'curso'?" in capsys.readouterr().err
    # si falta la carpeta (alguien copió solo mate.py), lo dice en vez de romperse
    avisos = []
    assert mate.orden_curso([], lambda texto, *_: avisos.append(texto),
                            carpeta=tmp_path / "no_esta") == 2
    assert "no encuentro las clases del curso" in avisos[0] and "al lado de mate.py" in avisos[0]
    # 'curso' es una orden: un curso.mate propio se corre con 'correr', y Mate lo avisa
    (tmp_path / "curso.mate").write_text('mostrar("mío")\n', encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    assert mate.main(["curso"]) == 0
    capturado = capsys.readouterr()
    assert "correr curso.mate" in capturado.err and "El curso de Mate" in capturado.out
    assert mate.main(["correr", "curso.mate"]) == 0
    assert capsys.readouterr().out == "mío\n"
    # 'ayuda curso' muestra la ayuda general, que la nombra
    assert mate.main(["ayuda", "curso"]) == 0
    assert "  curso 1 " in capsys.readouterr().out
    assert "curso" in mate.ORDENES_SABIDAS and mate.orden_usada(["curso", "3"]) == "curso"


def test_con_la_orden_instalada_los_comandos_sugeridos_dicen_mate(capsys, monkeypatch):
    monkeypatch.delenv("MATE_ORDEN", raising=False)
    de_siempre = mate.como_se_llama()
    assert de_siempre in ("python mate\\mate.py", "python3 mate/mate.py")
    monkeypatch.setenv("MATE_ORDEN", "cualquier cosa")  # solo vale la palabra 'mate'
    assert mate.como_se_llama() == de_siempre
    monkeypatch.setenv("MATE_ORDEN", "mate")
    assert mate.como_se_llama() == "mate"
    assert mate.main(["curso"]) == 0
    salida = capsys.readouterr().out
    assert "\n  mate curso 1\n" in salida and "\n  mate correr " in salida
    assert de_siempre not in salida


def test_instalar_bat_esta_escrito_con_cuidado():
    # (no se puede correr acá: se controla su forma, que es donde un .bat se rompe)
    crudo = (RAIZ / "instalar.bat").read_bytes()
    assert crudo.isascii()  # sin tildes: la consola de Windows las mostraría mal
    assert b"\r\n" in crudo and b"\n" not in crudo.replace(b"\r\n", b"")
    renglones = crudo.decode("ascii").split("\r\n")
    texto = "\n".join(renglones)
    codigo = [r for r in renglones if not r.lower().startswith(("rem", "echo "))]
    # cada salto va a una etiqueta que existe, y no queda ninguna etiqueta sin usar
    etiquetas = {r[1:].strip() for r in renglones if r.startswith(":")}
    saltos = set(re.findall(r"\bgoto (\w+)", "\n".join(codigo)))
    assert saltos == etiquetas and "fin" in etiquetas
    # sin bloques entre paréntesis (se rompen con carpetas como "mate (1)") y sin expansión
    # demorada (se rompe con un signo de admiración en la ruta)
    assert not [r for r in codigo if r.rstrip().endswith("(") or r.lstrip().startswith(")")]
    assert "DisableDelayedExpansion" in texto and "!" not in texto
    # no toca el PATH ni el registro, no baja nada y no pide permisos
    for prohibido in ["setx", "reg add", "reg delete", "regedit", "powershell", "curl",
                      "bitsadmin", "runas", "path=", "rmdir", "rd /s", "format"]:
        assert prohibido not in "\n".join(codigo).lower(), prohibido
    # lo único que escribe o borra es el lanzador, y siempre entre comillas
    def sin_comillas(renglon):  # (adentro de las comillas, un > no manda nada a un archivo)
        return re.sub(r'"[^"]*"', '""', renglon.replace(">nul", ""))

    escribe = [r for r in codigo if re.search(r"(?<![2^])>", sin_comillas(r))]
    assert len(escribe) == 5 and all(re.match(r'>>?"%LANZADOR%" echo ', r) for r in escribe)
    borra = [r for r in codigo if re.match(r"\s*(del|erase)\b", r)]
    assert borra and all(r.startswith('del "%LANZADOR%"') for r in borra)
    assert not re.search(r'(?<!")%(AQUI|LANZADOR|CARPETA)%', "\n".join(
        r for r in renglones if not r.lower().startswith(("rem", "set "))))
    for frase in ['set "AQUI=%~dp0"', 'set "CARPETA=%LOCALAPPDATA%\\Microsoft\\WindowsApps"',
                  '>>"%LANZADOR%" echo "%AQUI%mate.bat" %%*', 'echo set "MATE_ORDEN=mate"',
                  "sys.version_info[:2] >= (3, 10)", "py -3 -c", 'if /i "%~1"=="quitar"',
                  "Add python.exe to PATH", "No toque el PATH", "Para deshacerlo", "pause",
                  "exit /b %CODIGO%", 'findstr /c:"%MARCA%" "%LANZADOR%"']:
        assert frase in texto, frase
    # los renglones que se muestran no llevan signos que la consola tomaría como órdenes
    for renglon in renglones:
        if renglon.lower().startswith("echo "):
            assert not re.search(r"[&|<>]", renglon), renglon
            assert len(renglon) <= 90, renglon
    # mate.bat: prueba a Python corriéndolo y no espera una tecla si lo llama el lanzador
    lanzado = (RAIZ / "mate.bat").read_bytes().decode("ascii")
    assert 'python -c "import sys" >nul 2>nul' in lanzado and "where python" not in lanzado
    assert 'if defined MATE_ORDEN set "ESPERAR="' in lanzado


def test_la_pagina_para_compartir_es_un_solo_archivo_y_su_ejemplo_anda(tmp_path, capsys,
                                                                       monkeypatch):
    import html
    pagina = (RAIZ.parent / "docs" / "index.html").read_text(encoding="utf-8")
    assert pagina.startswith("<!doctype html>") and '<html lang="es">' in pagina
    assert '<meta name="viewport" content="width=device-width, initial-scale=1">' in pagina
    assert "prefers-color-scheme: dark" in pagina
    # sin nada de afuera: ni hojas de estilo, ni programas, ni imágenes, ni letras ajenas
    for ajeno in ["<link", "<img", "<iframe", "@import", "url(", "src=", "fonts.g", "cdn"]:
        assert ajeno not in pagina.lower(), ajeno
    assert re.findall(r'href="([^"#][^"]*)"', pagina) == []  # solo enlaces de la misma página
    # sin el nombre de nadie: la dirección del proyecto se arma sola al publicarla
    assert not re.search(r"github\.com/\w", pagina) and not re.search(r"\w@\w", pagina)
    assert "mayorista" not in pagina.lower()
    for frase in ["Para quién es", "Un mostrador con IA", "Se lee en castellano",
                  "Mensajes con contrato", "Frenos", "Aprende de las correcciones",
                  "Cómo bajarlo e instalarlo", "instalar.bat", "Add python.exe to PATH",
                  "El curso", "mate curso", "Para qué no sirve todavía",
                  "No atiende por WhatsApp", "hecho por una sola persona",
                  "python mate\\mate.py curso", 'data-ruta="tree/HEAD/mate/curso"',
                  'data-ruta="archive/HEAD.zip"', f"Mate {mate.VERSION}"]:
        assert frase in pagina, frase
    # el ejemplo de la página es un programa entero: verifica, corre y pasa su prueba
    ejemplo = html.unescape(re.search(r'<code id="ejemplo">(.*?)</code>', pagina, re.S).group(1))
    assert "<" not in ejemplo and max(len(r) for r in ejemplo.splitlines()) <= 80
    ruta = tmp_path / "mostrador.mate"
    ruta.write_text(ejemplo + "\n", encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    assert mate.main(["verificar", str(ruta)]) == 0
    capsys.readouterr()
    assert mate.main(["correr", str(ruta), "--ia-simulada"]) == 0
    assert capsys.readouterr().out == "La yerba sale $ 3.500.\n"
    assert mate.main(["probar", str(ruta)]) == 0
    assert "1 de 1 pruebas pasaron" in capsys.readouterr().out


def test_el_readme_arranca_por_que_es_como_se_instala_y_por_donde_empezar(tmp_path, capsys,
                                                                          monkeypatch):
    leeme = (RAIZ / "README.md").read_text(encoding="utf-8")
    titulos = re.findall(r"(?m)^## (.+)$", leeme)
    assert titulos[:4] == ["Instalarlo", "Por dónde empezar", "El curso", "Qué busca Mate"]
    assert titulos.index("Qué cambió en la 0.5") < titulos.index(
        "Qué cambió y puede frenar un programa viejo")
    primer_pantallazo = leeme[:leeme.index("## Por dónde empezar")]
    for frase in ["Mate es un lenguaje de programación chico, con palabras en castellano",
                  "Versión 0.5", "Add python.exe to PATH", "instalar.bat", "mate --version",
                  "No toca el PATH ni el registro", ".\\mate\\instalar.bat quitar",
                  "Todavía no se probó en una Windows de verdad", "python mate\\mate.py curso"]:
        assert frase in primer_pantallazo, frase
    for frase in ["| `curso` |", "`docs\\index.html`", "python mate\\mate.py curso 1",
                  "notepad mate\\curso\\clase_01_hola.md", "`MATE_ORDEN`",
                  "correr curso.mate", "no atiende por WhatsApp"]:
        assert frase in leeme, frase
    # todo lo de la 0.5 está en 'Qué cambió en la 0.5'
    novedades = leeme.split("## Qué cambió en la 0.5")[1].split("\n## ")[0]
    for frase in ["entre 2 y 5 veces más rápido", "usar python", "leer_tabla",
                  "agregar_a_archivo", "simular_teclado", "frenos", "consultas_por_dia",
                  "`propuestas` y `proponer`", "El curso", "instalar.bat", "docs\\index.html",
                  "mate.bat"]:
        assert frase in novedades, frase
    for ancla in re.findall(r"\]\(#([^)]+)\)", novedades + primer_pantallazo):
        assert any(ancla == re.sub(r"[^\w\- ]", "", t.lower()).replace(" ", "-")
                   for t in re.findall(r"(?m)^#{2,3} (.+)$", leeme)), ancla
    # el programa del primer pantallazo anda tal cual está escrito
    ejemplo = re.search(r"```\n(mensaje Consulta .*?)```", primer_pantallazo, re.S).group(1)
    ruta = tmp_path / "primero.mate"
    ruta.write_text(ejemplo, encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    assert mate.main(["correr", str(ruta), "--ia-simulada"]) == 0
    assert capsys.readouterr().out == "La yerba sale $ 3.500.\n"
    # las fichas de las mejoras, y la ayuda
    mejoras = (RAIZ / "MEJORAS.md").read_text(encoding="utf-8")
    for numero, titulo in [(117, "El curso: doce clases y la orden `curso`"),
                           (118, "Instalador para Windows: `instalar.bat`"),
                           (119, "Una página para compartir y un README que se entiende de "
                                 "entrada")]:
        ficha = mejoras.split(f"\n**{numero}. {titulo}**")[1].split("\n\n")[0]
        assert "Estado: hecha" in ficha and "Nota de lo decidido" in ficha, numero
    assert "Sin probar en Windows real" in mejoras
    assert mate.TOPE_DE_FUNCIONES == 48 == len(mate.FUNCIONES) and len(mate.PALABRAS) == 36
    ayuda = mate.texto_de_ayuda()
    assert "  curso  " in ayuda and "  curso 1  " in ayuda
    assert max(len(r) for r in ayuda.splitlines()) <= 100
    assert "mate.py curso" in mate.__doc__ and mate.VERSION == "0.5"


# ───────────────────── Correcciones de la revisión de la 0.5 (mejora 120) ─────────────────────

def test_la_consulta_cobrada_que_termina_en_error_cuenta_para_el_tope(tmp_path, capsys, ia):
    # Una respuesta cortada, sin texto o frenada por un filtro llegó con código 200: Anthropic
    # la cobra. Tiene que sumar a la cuenta del día, y el tope tiene que frenar las siguientes.
    ia.respuestas = [dice("cortada a la mit", motivo="max_tokens"), dice(""),
                     dice("x", motivo="refusal"), dice("Hola.")]
    fuente = CON_FRENOS % "consultas_por_dia: 2\n        tokens_por_dia: 1000" + """
        para i en rango(6) {
            intentar { mostrar(consultar("pregunta {i}")) } si falla e { mostrar("falló") }
        }
    """
    codigo, salida, err = por_main(tmp_path, capsys, fuente)
    assert codigo == 0 and len(ia.pedidos) == 2  # ni una más que el tope
    assert salida.splitlines() == ["falló", "falló"] + [RESERVA] * 4
    assert memoria_de(tmp_path)["agentes"]["Mostrador"]["gasto"] == {
        hoy_iso(): {"consultas": 2, "simuladas": 0, "tokens": 24}}
    assert "llegó a su tope (ya hizo 2 consulta(s) a la IA hoy y su tope es 2 por día)" in err
    # lo que no llegó a cobrarse (un error del servicio, o sin red) no se cuenta
    (tmp_path / "programa.memoria.json").unlink()
    ia.respuestas = [error_http(400, mensaje="no"), dice("Hola.")]
    codigo, salida, err = por_main(tmp_path, capsys, fuente)
    assert salida.splitlines() == ["falló", "Hola.", "Hola."] + [RESERVA] * 3
    assert memoria_de(tmp_path)["agentes"]["Mostrador"]["gasto"][hoy_iso()]["consultas"] == 2


def test_al_llegar_al_tope_avisa_en_pantalla_una_vez(tmp_path, capsys, ia):
    fuente = CON_FRENOS % "consultas_por_dia: 1" + """
        mostrar(consultar("uno"))
        mostrar(consultar("dos"))
        mostrar(consultar("tres"))
    """
    codigo, salida, err = por_main(tmp_path, capsys, fuente)
    assert (codigo, salida) == (0, f"Sí, hay yerba.\n{RESERVA}\n{RESERVA}\n")
    assert err.count("aviso:") == 1 and err.startswith(
        "aviso: Mostrador llegó a su tope (ya hizo 1 consulta(s) a la IA hoy y su tope es 1 "
        "por día). Desde ahora contesta con el texto de reserva, sin consultar. Mañana vuelve "
        "a consultar sola. El tope se cambia en los 'frenos' del agente, y la cuenta se ve con:")
    assert f"bitacora {tmp_path / 'programa.mate'}" in err
    # --olvidar no borra la cuenta de las consultas de verdad (es plata): sigue frenado
    codigo, salida, err = por_main(tmp_path, capsys, fuente, "--olvidar")
    assert salida == f"{RESERVA}\n" * 3 and len(ia.pedidos) == 1
    # borrar el archivo de memoria sí la reinicia
    (tmp_path / "programa.memoria.json").unlink()
    codigo, salida, err = por_main(tmp_path, capsys, fuente)
    assert salida.startswith("Sí, hay yerba.\n") and len(ia.pedidos) == 2


def test_en_un_ensayo_el_tope_cuenta_solo_esa_corrida(tmp_path, capsys):
    # El mismo ensayo (--ia-simulada) da lo mismo todas las veces que se corra en el día:
    # así el curso no "se rompe" a la corrida número once.
    fuente = CON_FRENOS % "consultas_por_dia: 2" + """
        mostrar(consultar("uno"))
        mostrar(consultar("dos"))
        mostrar(consultar("tres"))
    """
    for vuelta in range(3):
        codigo, salida, err = por_main(tmp_path, capsys, fuente, "--ia-simulada")
        assert (codigo, salida) == (0, f"Hola.\nHola.\n{RESERVA}\n"), vuelta
        assert err.startswith(
            "aviso: Mostrador llegó a su tope (ya hizo 2 consulta(s) simuladas a la IA en esta "
            "corrida y su tope es 2 por día). Desde ahora contesta con el texto de reserva, sin "
            "consultar. Es un ensayo: en la próxima corrida con --ia-simulada la cuenta "
            "arranca de cero.") and err.count("aviso:") == 1
    assert memoria_de(tmp_path)["agentes"]["Mostrador"]["gasto"][hoy_iso()]["simuladas"] == 6


def test_el_curso_da_lo_mismo_aunque_se_corra_muchas_veces_en_el_dia(tmp_path, capsys):
    import shutil
    shutil.copytree(RAIZ / "curso", tmp_path / "curso")
    clase = str(tmp_path / "curso" / "clase_10_frenos.mate")
    salidas = set()
    for _ in range(12):  # (cada corrida hace 5 consultas simuladas y el tope es 50)
        capsys.readouterr()
        assert mate.main(["correr", clase, "--ia-simulada"]) == 0
        salidas.add(capsys.readouterr().out)
    assert len(salidas) == 1 and "Mostrador: La yerba sale $ 3.500." in salidas.pop()


def test_guardar_la_memoria_no_pisa_lo_que_anoto_otra_ventana(tmp_path, capsys, monkeypatch):
    # Con la charla abierta, desde otra ventana se corrige al agente y corre otra charla.
    fuente = CON_FRENOS % "consultas_por_dia: 40" + """
        var seguir = verdadero
        mientras seguir {
            sea t = leer("Cliente:", "chau")
            si t == "chau" { seguir = falso } sino { mostrar(consultar(t)) }
        }
    """
    archivo = tmp_path / "programa.mate"
    archivo.write_text(fuente, encoding="utf-8")
    tecleado = iter(["a", "b", "OTRA VENTANA", "c", "chau"])

    def teclear(_pregunta):
        dicho = next(tecleado)
        if dicho != "OTRA VENTANA":
            return dicho
        assert mate.main(["corregir", str(archivo), "Mostrador", "No hay envíos los domingos"]) == 0
        otra = iter(["x", "y", "z", "chau"])
        monkeypatch.setattr(mate, "por_teclado", lambda _p: next(otra))
        assert mate.main(["correr", str(archivo), "--ia-simulada"]) == 0
        monkeypatch.setattr(mate, "por_teclado", teclear)
        return next(tecleado)

    monkeypatch.setattr(mate, "por_teclado", teclear)
    assert mate.main(["correr", str(archivo), "--ia-simulada"]) == 0
    ficha = memoria_de(tmp_path)["agentes"]["Mostrador"]
    assert [leccion["texto"] for leccion in ficha["lecciones"]] == ["No hay envíos los domingos"]
    assert ficha["gasto"][hoy_iso()]["simuladas"] == 6


def test_el_tope_de_verdad_es_uno_solo_aunque_haya_dos_ventanas(tmp_path, capsys, ia,
                                                               monkeypatch):
    import json
    fuente = CON_FRENOS % "consultas_por_dia: 3" + """
        mostrar(consultar("uno"))
        sea t = leer("Cliente:", "x")
        mostrar(consultar("dos"))
        mostrar(consultar("tres"))
    """

    def otra_ventana(_pregunta):  # mientras espera, otra corrida gasta 2 y se anota una lección
        memoria = memoria_de(tmp_path)
        ficha = memoria["agentes"]["Mostrador"]
        ficha["gasto"][hoy_iso()]["consultas"] += 2
        ficha["gasto"][hoy_iso()]["tokens"] += 100
        ficha["lecciones"].append({"fecha": "", "texto": "Los lunes no hay pan"})
        (tmp_path / "programa.memoria.json").write_text(json.dumps(memoria), encoding="utf-8")
        return "sigo"

    monkeypatch.setattr(mate, "por_teclado", otra_ventana)
    codigo, salida, err = por_main(tmp_path, capsys, fuente)
    assert (codigo, salida) == (0, f"Sí, hay yerba.\n{RESERVA}\n{RESERVA}\n")
    assert len(ia.pedidos) == 1 and "llegó a su tope (ya hizo 3 consulta(s)" in err
    ficha = memoria_de(tmp_path)["agentes"]["Mostrador"]
    assert ficha["gasto"][hoy_iso()] == {"consultas": 3, "simuladas": 0, "tokens": 112}
    assert [leccion["texto"] for leccion in ficha["lecciones"]] == ["Los lunes no hay pan"]


def test_fundir_memoria_suma_lo_de_esta_corrida_a_lo_que_dice_el_archivo():
    dia = "2026-11-21"
    leida = {"A": {"estado": {"n": 1}, "lecciones": [{"fecha": "", "texto": "vieja"}],
                   "gasto": {dia: {"consultas": 1, "simuladas": 0, "tokens": 10}}}}
    nueva = {"A": {"estado": {"n": 2},
                   "lecciones": [{"fecha": "", "texto": "vieja"}, {"fecha": "", "texto": "mía"}],
                   "propuestas": [{"fecha": "", "texto": "aprobada afuera", "motivo": ""},
                                  {"fecha": "", "texto": "propuesta mía", "motivo": ""}],
                   "gasto": {dia: {"consultas": 3, "simuladas": 1, "tokens": 30}}}}
    en_disco = {"A": {"estado": {"n": 1},
                      "lecciones": [{"fecha": "", "texto": "aprobada afuera"}],  # borró 'vieja'
                      "gasto": {dia: {"consultas": 5, "simuladas": 0, "tokens": 50}}},
                "B": {"estado": {}, "lecciones": [{"fecha": "", "texto": "de otro"}]}}
    junta = mate.fundir_memoria(leida, nueva, en_disco)
    assert junta["B"] == en_disco["B"] and junta["A"]["estado"] == {"n": 2}
    assert [x["texto"] for x in junta["A"]["lecciones"]] == ["aprobada afuera", "mía"]
    assert [x["texto"] for x in junta["A"]["propuestas"]] == ["propuesta mía"]
    assert junta["A"]["gasto"] == {dia: {"consultas": 7, "simuladas": 1, "tokens": 70}}
    # si esta corrida no cambió nada, queda lo del archivo tal cual
    assert mate.fundir_memoria(leida, leida, en_disco) == en_disco


@pytest.mark.parametrize("respuesta", [
    "La yerba sale 4000 hoy.", "Sale 4000 x kilo.", "Precio: 4000 x kg",
    "El kilo sale $ **4.000**.", "Sale $ 3.500, pero te lo dejo a 2.000.", "Total: 9.999",
    "sale 4000 ahora", "sale 4000 nomás", "sale aprox. 4000", "$ -4000", "USD 40",
    "40 dólares", "4000.-", "precio de lista 4000", "El precio es **$4000**", "4000 mangos"])
def test_el_freno_de_precios_ve_las_formas_comunes_de_decir_un_importe(respuesta):
    frenos = {"precios": {3500.0, 1200.0}}
    assert [regla for regla, _, _ in mate.reglas_rotas(respuesta, frenos)] == ["precios"]


@pytest.mark.parametrize("respuesta", [
    "La yerba sale 3500 hoy.", "Sale $ **3.500** el kilo", "sale 500 gramos", "vale 300 puntos",
    "Tenemos 4000 unidades en stock", "sale 1200 el de 500", "cuesta 1200 x kg",
    "Llamanos al 4555-3500", "sale 2 por 1", "En total son 150 productos", "3500.-",
    "Abrimos el 21/11/2026 a las 9:30", "sale a las 1500 hs", "Vale 1.200 pesos, 500 g."])
def test_el_freno_de_precios_no_salta_con_cantidades_ni_con_precios_de_la_lista(respuesta):
    assert mate.reglas_rotas(respuesta, {"precios": {3500.0, 1200.0}}) == []


def test_un_precio_que_quedo_como_texto_se_avisa_y_la_tabla_entiende_mas_formas(
        tmp_path, capsys):
    assert [mate.valor_de_celda(c) for c in ["3500.-", "1.200 $", "$ 3.500,-", "1,234.50",
                                             "consultar", "00123"]] == [
        3500, 1200, 3500, "1,234.50", "consultar", "00123"]
    fuente = """
        mensaje Consulta { pregunta: texto }
        agente Mostrador {
            estado filas = [{ producto: "yerba 500", precio: "1,234.50", codigo: "00123" },
                            { producto: "azucar", precio: 1200 }]
            frenos { precios: filas  reserva: "FRENADO" }
            al recibir Consulta como c {
                responder consultar_ia("", c.pregunta, "La yerba sale $ 1,234.50.")
            }
        }
        mostrar(preguntar Consulta { pregunta: "yerba" } a Mostrador)
        mostrar(preguntar Consulta { pregunta: "yerba" } a Mostrador)
    """
    codigo, salida, err = por_main(tmp_path, capsys, fuente, "--ia-simulada")
    assert (codigo, salida) == (0, "FRENADO\nFRENADO\n")
    assert err.count("'precios' trae 1 dato(s) que parecen importes pero no son números") == 1
    assert '(por ejemplo "1,234.50")' in err and "escribilos como número" in err


def test_probar_no_pisa_archivos_de_datos_con_escribir_archivo(tmp_path, capsys):
    (tmp_path / "pedidos.txt").write_text("pedido real de ayer\n", encoding="utf-8")
    codigo, salida, err = por_main(tmp_path, capsys, """
        agregar_a_archivo("pedidos.txt", "principal")
        prueba "mezcla" {
            agregar_a_archivo("pedidos.txt", "uno")
            escribir_archivo("pedidos.txt", "PISADO")
            asegurar leer_archivo("pedidos.txt") == "PISADO"
            agregar_a_archivo("pedidos.txt", "dos")
            asegurar leer_archivo("pedidos.txt") == "PISADO\\ndos\\n"
            escribir_archivo("nuevo.txt", "hola")
            asegurar leer_archivo("nuevo.txt") == "hola"
            asegurar falla { escribir_archivo("nohay/x.txt", "x") }
        }
        prueba "cada prueba arranca de lo que dejó el programa" {
            asegurar leer_archivo("pedidos.txt") == "pedido real de ayer\\nprincipal\\n"
            asegurar falla { leer_archivo("nuevo.txt") }
        }
    """, orden="probar")
    assert (codigo, err) == (0, "") and "2 de 2 pruebas pasaron" in salida
    assert (tmp_path / "pedidos.txt").read_text(encoding="utf-8") == "pedido real de ayer\n"
    assert archivos_de(tmp_path) == ["pedidos.txt", "programa.mate"]


def test_usar_python_no_sale_de_la_carpeta_del_programa_por_un_archivo_traido(
        tmp_path, capsys):
    afuera, adentro = tmp_path / "afuera", tmp_path / "prog"
    (adentro / "sub").mkdir(parents=True)
    afuera.mkdir()
    (afuera / "mal.py").write_text("def f():\n    return 'AFUERA'\n", encoding="utf-8")
    (afuera / "lib.mate").write_text(
        'usar python "mal.py"\nfuncion de_afuera() { devolver mal.f() }\n', encoding="utf-8")
    codigo, salida, err = por_main(adentro, capsys, 'usar "../afuera/lib.mate"\n'
                                                    "mostrar(de_afuera())")
    assert codigo == 1 and "AFUERA" not in salida
    assert "'usar python' solo trae archivos de la carpeta del programa que se corre" in err
    assert "(lib.mate) está en otra carpeta" in err and "lib.mate:1: error:" in err
    # desde una carpeta de adentro sí vale
    (adentro / "sub" / "bien.py").write_text("def f():\n    return 'adentro'\n", encoding="utf-8")
    (adentro / "sub" / "lib.mate").write_text(
        'usar python "bien.py"\nfuncion de_adentro() { devolver bien.f() }\n', encoding="utf-8")
    codigo, salida, err = por_main(adentro, capsys, 'usar "sub/lib.mate"\nmostrar(de_adentro())')
    assert (codigo, salida, err) == (0, "adentro\n", "")


@pytest.mark.parametrize("nombre,motivo", [
    ("programa.memoria.json", "ese archivo lo lleva Mate"),
    ("programa.bitacora.txt", "ese archivo lo lleva Mate"),
    ("Programa.Memoria.JSON. ", "ese archivo lo lleva Mate"),
    ("x.pyw", "para no pisar un programa"), ("X.PYW.", "para no pisar un programa")])
def test_las_funciones_de_archivos_no_escriben_en_lo_que_lleva_mate_ni_en_pyw(
        tmp_path, capsys, nombre, motivo):
    for funcion in ("agregar_a_archivo", "escribir_archivo"):
        codigo, salida, err = por_main(tmp_path, capsys,
                                       f'{funcion}("{nombre}", "ZZZ")\nmostrar("escribió")')
        assert codigo == 1 and salida == "" and motivo in err, (funcion, err)
        assert archivos_de(tmp_path) == ["programa.mate"]
    # la memoria de OTRO programa es un archivo cualquiera
    codigo, salida, err = por_main(tmp_path, capsys,
                                   'escribir_archivo("otro.memoria.json", "x")\nmostrar("sí")')
    assert (codigo, salida) == (0, "sí\n")


@pytest.mark.parametrize("regla,esperado", [
    ("consultas_por_dia: -5", "'consultas_por_dia' lleva un número entero y dice -5"),
    ("consultas_por_dia: 2.5", "'consultas_por_dia' lleva un número entero y dice 2.5"),
    ("tokens_por_dia: -1", "'tokens_por_dia' lleva un número entero y dice -1"),
    ("largo: 0", "'largo' lleva un número entero mayor que cero y dice 0"),
    ('reserva: "  "', "'reserva' está vacía"),
])
def test_un_valor_fijo_que_no_sirve_en_los_frenos_se_avisa_antes_de_correr(
        tmp_path, capsys, regla, esperado):
    fuente = CON_FRENOS.replace('reserva: "Eso te lo confirma una persona, ya te paso."',
                                "" if regla.startswith("reserva") else 'reserva: "x"')
    fuente = fuente.replace("largo: 120", "") % regla
    codigo, salida, err = por_main(tmp_path, capsys, fuente + 'mostrar("no llega a correr")')
    assert (codigo, salida) == (1, "") and esperado in err
    assert re.match(r".*programa\.mate:\d+: error: en los frenos de Mostrador", err)
    assert mate.verificar(mate.analizar(CON_FRENOS % "consultas_por_dia: 0")) == []


def test_un_error_al_calcular_los_frenos_no_se_ataja_ni_se_confunde_con_la_ia(tmp_path, capsys):
    # Como en el mostrador del curso: la consulta va dentro de 'intentar', para cuando no hay
    # internet. Unos frenos mal escritos no pueden pasar por "la IA no contestó".
    fuente = """
        mensaje Consulta { pregunta: texto }
        funcion solo_precios(filas) {
            var precios = []
            para fila en filas { precios = precios + [fila.precios] }
            devolver precios
        }
        agente Mostrador {
            estado lista = [{ producto: "Yerba", precio: 3500 }]
            frenos {
                precios: solo_precios(lista)
                reserva: "Eso lo ve una persona."
                %s
            }
            al recibir Consulta como c {
                intentar {
                    responder consultar_ia("", c.pregunta, "Hola.")
                } si falla motivo {
                    responder "(la IA no contestó. Motivo: {motivo})"
                }
            }
        }
        mostrar(preguntar Consulta { pregunta: "¿Hay yerba?" } a Mostrador)
        mostrar("sigue atendiendo")
    """
    codigo, salida, err = por_main(tmp_path, capsys, fuente % "", "--ia-simulada")
    assert (codigo, salida) == (1, "")
    assert "programa.mate:11: error: los frenos de Mostrador están mal escritos: " in err
    assert "no tiene un campo 'precios'. ¿Quisiste decir 'precio'?" in err
    assert "unos frenos que fallan no frenan nada" in err and "en solo_precios()" in err
    bien = fuente.replace("fila.precios", "fila.precio")
    codigo, salida, err = por_main(tmp_path, capsys, bien % "largo: lista", "--ia-simulada")
    assert (codigo, salida) == (1, "")
    assert "programa.mate:13: error: en los frenos de Mostrador, 'largo' recibió una lista" in err
    codigo, salida, err = por_main(tmp_path, capsys, bien % "", "--ia-simulada")
    assert (codigo, salida, err) == (0, "Hola.\nsigue atendiendo\n", "")


def test_proponer_respeta_el_tope_del_dia_y_cuenta_lo_cobrado_que_fallo(tmp_path, capsys, ia):
    archivo = tmp_path / "programa.mate"
    archivo.write_text(CON_FRENOS % "consultas_por_dia: 2", encoding="utf-8")
    # una respuesta cortada se cobró: entra en la cuenta aunque vaya la redacción fija
    ia.respuestas = [dice("No ofr", motivo="max_tokens"), dice("No ofrezcas envíos.")]
    codigo, salida, err = orden_mate(capsys, "proponer", archivo, "Mostrador", "Ofreció envíos")
    assert codigo == 0 and "porque la IA no contestó: consultar_ia(): la respuesta llegó cortada" \
        in salida
    assert memoria_de(tmp_path)["agentes"]["Mostrador"]["gasto"][hoy_iso()] == {
        "consultas": 1, "simuladas": 0, "tokens": 12}
    codigo, salida, err = orden_mate(capsys, "proponer", archivo, "Mostrador", "Dijo otra cosa")
    assert codigo == 0 and "La redactó la IA" in salida and len(ia.pedidos) == 2
    # ya llegó al tope de hoy: no consulta más, y lo dice
    codigo, salida, err = orden_mate(capsys, "proponer", archivo, "Mostrador", "Fue seco")
    assert (codigo, err) == (0, "") and len(ia.pedidos) == 2
    assert "  3. Una respuesta tuya estuvo mal: Fue seco. No lo repitas." in salida
    assert ("Es una redacción fija: no consulté a la IA porque Mostrador ya hizo 2 consulta(s) a "
            "la IA hoy y su tope es 2 por día") in salida
    assert memoria_de(tmp_path)["agentes"]["Mostrador"]["gasto"][hoy_iso()]["consultas"] == 2


def test_cortar_con_ctrl_c_en_leer_termina_con_130_como_en_la_0_4(tmp_path, capsys, monkeypatch):
    def cortar(_pregunta):
        raise KeyboardInterrupt

    monkeypatch.setattr(mate, "por_teclado", cortar)
    codigo, salida, err = por_main(tmp_path, capsys,
                                   'mostrar("antes")\nsea n = leer("Nombre:")\nmostrar(n)')
    assert (codigo, salida) == (130, "antes\n")
    assert err == f"\n{mate.CORTE_EN_EL_TECLADO}\n" and "error" not in err


def test_un_titulo_arriba_de_los_encabezados_de_la_planilla_se_explica():
    with pytest.raises(mate.ErrorMate) as info:
        mate.tabla_de_texto("Lista de precios Noviembre;;\nproducto;precio;stock\nYerba;3500;4\n",
                            "precios.csv")
    mensaje = info.value.mensaje
    assert mensaje.startswith("leer_tabla(): la primera fila de 'precios.csv' tiene que ser la "
                              "de los títulos de las columnas")
    assert '("Lista de precios Noviembre")' in mensaje and "comillas:" not in mensaje
    assert 'en el renglón 2 ("producto;precio;stock")' in mensaje and "borrá las filas" in mensaje
    assert "tiene 1 dato y el renglón 2 tiene 3" in mensaje
    # un renglón con un dato de más sigue teniendo su explicación de siempre
    with pytest.raises(mate.ErrorMate) as info:
        mate.tabla_de_texto("producto;precio\nYerba;3500;4\n", "precios.csv")
    assert "le sobra algo" in info.value.mensaje
    with pytest.raises(mate.ErrorMate) as info:
        mate.tabla_de_texto("producto;precio\nYerba;3500\nPan;100;x\n", "precios.csv")
    assert "le sobra algo" in info.value.mensaje


@pytest.mark.parametrize("fuente,esperado", [
    ('sea dicho = "3"\nmostrar(dicho * 3500)',
     "no se puede hacer texto * numero. Lo que se lee con leer() o viene de un archivo es un "
     "texto, aunque tenga cifras: para hacer cuentas pasalo antes a número con numero(...)"),
    ("sea precio = $ 3500", "los importes se escriben sin el signo $, solo el número: 3500"),
    ('sea precios = [{ producto: "a" }]\nmostrar(precios.producto)',
     "lista no tiene campos: es una lista. Para ver 'producto' de uno de sus elementos, pedilo "
     "primero (por ejemplo lista[0].producto)"),
    ('sea t = leer_tabla(precios.csv)',
     "no existe 'precios'. Si precios.csv es el nombre de un archivo, va entre comillas: "
     '"precios.csv"'),
    ('sea fila = { Producto: "Yerba" }\nmostrar(fila.producto)',
     "mapa no tiene un campo 'producto'. ¿Quisiste decir 'Producto'? (las mayúsculas y las "
     "tildes cuentan. Si este dato viene de una planilla, el título de la columna está escrito "
     "'Producto'"),
    ('sea stock = ""\nsi stock == 0 { mostrar(1) }',
     'Ese texto está vacío: si viene de una planilla, es una celda vacía'),
    ('sea precio = "consultar"\nsi precio == 0 { mostrar(1) }',
     'Ese texto no es un número: si viene de una planilla, es una celda que no tiene un número'),
    ('sea precio = "12"\nsi precio == 12 { mostrar(1) }', 'numero("12") o texto(...)'),
    ('mensaje C {}\nagente A {\n frenos {\n  reserva: ""texto""\n  largo: 10\n }\n'
     ' al recibir C { responder 1 }\n}',
     "en la regla 'reserva' sobra algo después del valor ('texto'). Va una regla por renglón. "
     "Si es un texto, lleva UNA comilla de cada lado"),
])
def test_los_errores_comunes_de_principiante_dicen_como_arreglarlos(fuente, esperado):
    assert esperado in falla(fuente).mensaje
    # y lo que estaba bien sigue andando
    assert correr('sea m = { txt: 1 }\nmostrar(m.txt, "sale $ 3")')[0] == ["1 sale $ 3"]
    assert mate.verificar(mate.analizar(
        'mensaje C {}\nagente A {\n frenos { reserva: "x"  largo: 10 }\n'
        ' al recibir C { responder 1 }\n}')) == []


@pytest.mark.parametrize("planilla,esperado", [
    ("Producto;Precio;Stock\nYerba;3500;4\n",
     "A precios.csv le falta la columna 'producto'. La primera fila tiene que decir "
     "producto;precio;stock, en minúscula, y dice: Producto;Precio;Stock."),
    ("producto;precio;stock\nYerba;3500;4\nAzúcar 1 kg;1200;\n",
     "En precios.csv, el producto 2 (Azúcar 1 kg) no tiene el stock en números (si no hay, va 0)"),
    ("producto;precio;stock\nYerba;3500;4\nPan;consultar;2\n",
     'En precios.csv, el producto 2 (Pan) no tiene el precio en números: dice "consultar".'),
    ("producto;precio;stock\n", "precios.csv no tiene productos debajo de los títulos."),
])
def test_el_mostrador_del_curso_revisa_la_planilla_antes_de_atender(
        tmp_path, capsys, monkeypatch, planilla, esperado):
    import shutil
    for nombre in ("clase_12_mostrador.mate", "clase_12_solucion.mate"):
        shutil.copy(CURSO / nombre, tmp_path / "programa.mate")
        (tmp_path / "precios.csv").write_bytes(planilla.replace("\n", "\r\n").encode("cp1252"))
        monkeypatch.setattr(mate, "por_teclado", lambda _p: "yerba")
        capsys.readouterr()
        codigo = mate.main(["correr", str(tmp_path / "programa.mate"), "--ia-simulada"])
        capturado = capsys.readouterr()
        assert (codigo, capturado.out) == (1, ""), nombre  # no llegó a decir "cargué N productos"
        assert esperado in capturado.err and "Corregilo en Excel" in capturado.err, nombre


def test_el_mostrador_del_curso_busca_sin_tildes(tmp_path, capsys, monkeypatch):
    curso = copia_del_curso(tmp_path)
    tecleado = iter(["azucar", "AZÚCAR", "chau"])
    monkeypatch.setattr(mate, "por_teclado", lambda _p: next(tecleado))
    capsys.readouterr()
    assert mate.main(["correr", str(curso / "clase_12_mostrador.mate"), "--ia-simulada"]) == 0
    assert capsys.readouterr().out.count("Mostrador: Azúcar 1 kg: $ 1.250,50\n") == 2


def test_curso_n_reescribe_los_comandos_para_la_carpeta_donde_esta_la_persona(
        tmp_path, capsys, monkeypatch):
    monkeypatch.delenv("MATE_ORDEN", raising=False)
    # parado al lado de la carpeta mate, sin la orden corta: tal cual (lo prueba otra prueba)
    # desde otra carpeta: la orden larga con la ruta completa de mate.py, y las rutas enteras
    monkeypatch.chdir(tmp_path)
    assert mate.main(["curso", "1"]) == 0
    salida = capsys.readouterr().out
    assert salida.startswith("(Los comandos de esta clase están escritos para la carpeta donde "
                             "estás parado ahora:\nse pueden copiar tal cual.)\n\n# Clase 1: ")
    assert f"    python {RAIZ / 'mate.py'} correr {CURSO / 'clase_01_hola.mate'}\n" in salida
    assert "mate\\curso" not in salida and "python mate\\mate.py" not in salida
    assert f"notepad {CURSO / 'practica.mate'}" in salida
    # con la orden instalada: 'mate', desde cualquier carpeta
    monkeypatch.setenv("MATE_ORDEN", "mate")
    assert mate.main(["curso", "12"]) == 0
    salida = capsys.readouterr().out
    assert f"    mate correr {CURSO / 'clase_12_mostrador.mate'} --ia-simulada\n" in salida
    assert f"    mate probar {CURSO / 'clase_12_mostrador.mate'}\n" in salida
    assert "python" not in salida.replace("Python", "") and "mate\\" not in salida
    assert f"`{RAIZ / 'README.md'}`" in salida and f"`{RAIZ / 'ejemplos'}`" in salida
    # una carpeta con espacios va entre comillas
    import shutil
    con_espacio = tmp_path / "mis cosas" / "mate" / "curso"
    shutil.copytree(CURSO, con_espacio)
    assert mate.orden_curso(["1"], print, carpeta=con_espacio) == 0
    import os
    corta = os.path.join("mis cosas", "mate", "curso", "clase_01_hola.mate")
    assert f'mate correr "{corta}"' in capsys.readouterr().out


def test_guia_e_informe_se_guardan_en_un_archivo_que_el_bloc_de_notas_lee_bien(
        tmp_path, capsys, monkeypatch):
    monkeypatch.chdir(tmp_path)
    codigo, salida, err = orden_mate(capsys, "guia", "--guardar=guia.txt")
    assert (codigo, err) == (0, "")
    assert salida == "Quedó guardado en guia.txt. Para abrirlo:  notepad guia.txt\n"
    crudo = (tmp_path / "guia.txt").read_bytes()
    assert crudo.startswith(b"\xef\xbb\xbf")  # con la marca: el Bloc de notas muestra las tildes
    assert crudo.decode("utf-8-sig") == mate.texto_de_guia() + "\n"
    codigo, salida, err = orden_mate(capsys, "informe", "--para-mejorar",
                                     '--guardar="para mejorar.txt"')
    assert (codigo, err) == (0, "") and 'notepad "para mejorar.txt"' in salida
    assert (tmp_path / "para mejorar.txt").read_text(encoding="utf-8-sig").strip()
    for argumentos, esperado in [
            (["guia", "--guardar"], "a --guardar le falta el nombre del archivo"),
            (["guia", "--guardar="], "a --guardar le falta el nombre del archivo"),
            (["guia", "--guardar=mate.py"], "para no pisar un programa"),
            (["guia", "--guardar=x.mate"], "para no pisar un programa"),
            (["correr", "x.mate", "--guardar=x.txt"], "--guardar va con 'guia' o con 'informe'"),
            (["guia", "--guardar=no/existe/guia.txt"], "no pude guardar en")]:
        codigo, salida, err = orden_mate(capsys, *argumentos)
        assert codigo in (1, 2) and esperado in err and salida == "", argumentos
    assert sorted(p.name for p in tmp_path.iterdir()) == ["guia.txt", "para mejorar.txt"]
    codigo, salida, err = orden_mate(capsys, "guia", "--guardr=guia.txt")
    assert "¿quisiste decir --guardar=guia.txt?" in err


def test_con_un_python_viejo_mate_lo_dice_en_castellano_y_mate_bat_elige_el_nuevo():
    import ast
    import types
    fuente = (RAIZ / "mate.py").read_text(encoding="utf-8")
    for version in [(3, 7), (3, 8), (3, 9)]:  # el archivo se puede leer con un Python viejo...
        ast.parse(fuente, feature_version=version)
    principio = fuente[:fuente.index("import ast\n")]  # ...y lo primero que hace es mirar cuál es
    assert "import sys" in principio and "import " not in principio.split("import sys")[1]
    viejo = types.SimpleNamespace(version_info=(3, 8, 10, "final", 0))
    with pytest.raises(SystemExit) as info:
        exec(principio.replace("import sys\n", ""), {"sys": viejo})
    assert str(info.value).startswith(
        "Mate necesita Python 3.10 o mas nuevo, y este es Python 3.8.\nInstala uno nuevo desde "
        "https://www.python.org/downloads/")
    exec(principio.replace("import sys\n", ""),
         {"sys": types.SimpleNamespace(version_info=(3, 10, 0, "final", 0))})
    lanzador = (RAIZ / "mate.bat").read_bytes().decode("ascii").split("\r\n")
    prueba_de_version = '-c "import sys; sys.exit(0 if sys.version_info[:2] >= (3, 10) else 3)"'
    instalador = (RAIZ / "instalar.bat").read_bytes().decode("ascii")
    assert f"python {prueba_de_version} >nul 2>nul" in instalador  # la misma prueba en los dos
    con_version = [i for i, r in enumerate(lanzador) if prueba_de_version in r]
    sin_version = [i for i, r in enumerate(lanzador) if r.endswith('-c "import sys" >nul 2>nul')]
    assert len(con_version) == 2 and len(sin_version) == 2
    assert max(con_version) < min(sin_version)  # primero se busca uno que sirva
    assert lanzador[con_version[0]].startswith("python ")
    assert lanzador[con_version[1]].startswith("py -3 ")


def test_las_correcciones_de_la_revision_de_la_0_5_estan_documentadas():
    leeme = (RAIZ / "README.md").read_text(encoding="utf-8")
    for frase in ["python mate\\mate.py guia --guardar=guia.txt", "| `--guardar=guia.txt` |",
                  "can't open file", "**dentro de la carpeta `mate`**",
                  "Para pasárselo a otra persona", "Mate lo avisa en pantalla, una vez",
                  "Cuenta toda consulta que se cobra", "`--olvidar` no borra la cuenta",
                  "cuenta solo esa corrida", "En la consola", "La orden `proponer` entra en la misma",
                  "Con `probar` no se toca el disco", "`.pyw`", "¿Desea terminar el trabajo por lotes",
                  "`propuestas`, `proponer` y `curso` son órdenes", "U+FEFF",
                  "no se ataja con `intentar`", "Los totales.", "`sale 3500 hoy`", "`USD 40`",
                  "le **suma** lo de esa corrida", "en la carpeta del programa que se corre",
                  "la primera\n    fila tiene que ser la de los títulos", "mejora 120"]:
        assert frase in leeme, frase
    assert "guia > guia.txt" not in leeme and "--para-mejorar >\n" not in leeme
    mejoras = (RAIZ / "MEJORAS.md").read_text(encoding="utf-8")
    ficha = mejoras.split("\n**120. Correcciones de la revisión de la 0.5**")[1].split(
        "\n## Lo que se descartó")[0]
    assert "Estado: hecha" in ficha and "Nota de lo decidido" in ficha
    assert "Quedó afuera" in ficha and "Sigue sin probarse en una Windows de verdad" in ficha
    for clase, frases in {
            "clase_01_hola": ["can't open file", "cd .."],
            "clase_06_teclado": ["¿Desea terminar el trabajo por lotes (S/N)?"],
            "clase_08_agente": ["sale al final del mismo renglón"],
            "clase_09_agente_con_ia": ["ese pedazo de texto"],
            "clase_10_frenos": ["Ese aviso sale solo la primera vez", "llegó a su tope",
                                "`--olvidar` no borra esa cuenta"],
            "clase_11_aprende": ["sale solo esa primera vez"],
            "clase_12_mostrador": ["Tampoco dice totales", "revisar_lista(precios)",
                                   "5 de 5 pruebas pasaron", "llegó a su tope",
                                   "los frenos de Mostrador están mal escritos"]}.items():
        texto = (CURSO / f"{clase}.md").read_text(encoding="utf-8")
        for frase in frases:
            assert frase in texto, (clase, frase)
    pagina = (RAIZ.parent / "docs" / "index.html").read_text(encoding="utf-8")
    for frase in ["todavía no tiene una dirección de internet para bajarlo", "ahí adentro",
                  "ese no es: es de otro programa", "La IA no puede decir totales ni sumas",
                  "ese ZIP trae el proyecto entero"]:
        assert frase in pagina, frase
    ayuda, guia = mate.texto_de_ayuda(), mate.texto_de_guia()
    assert "--guardar=guia.txt" in ayuda and max(len(r) for r in ayuda.splitlines()) <= 100
    assert "Con 'probar' ninguna de las dos toca el disco" in guia
    assert "no se ataja con 'intentar'" in guia and "--guardar=guia.txt" in mate.__doc__
    assert mate.TOPE_DE_FUNCIONES == 48 == len(mate.FUNCIONES) and len(mate.PALABRAS) == 36
