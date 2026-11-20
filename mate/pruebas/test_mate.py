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


@pytest.mark.parametrize("nombre", ["hola", "negociacion", "equipo"])
def test_los_ejemplos_pasan_sus_pruebas(nombre, capsys):
    assert mate.main(["probar", str(RAIZ / "ejemplos" / f"{nombre}.mate")]) == 0
    assert "✗" not in capsys.readouterr().out
