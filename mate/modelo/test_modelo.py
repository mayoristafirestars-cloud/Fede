"""Pruebas del adaptador de modelo propio. Correr con:
    python -m pytest mate/modelo -q -p no:cacheprovider
Nada de esto sale a internet: el servicio "de verdad" es uno de mentira en esta máquina.
"""
import importlib.util
import json
import socket
import subprocess
import sys
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

import pytest

CARPETA = Path(__file__).resolve().parent
MATE = CARPETA.parent / "mate.py"
VARIABLES = ("MATE_MODELO_PROPIO_URL", "MATE_MODELO_PROPIO_NOMBRE",
             "MATE_MODELO_PROPIO_CLAVE", "MATE_MODELO_PROPIO_SIMULADO")


@pytest.fixture
def modelo(monkeypatch):
    for nombre in VARIABLES:
        monkeypatch.delenv(nombre, raising=False)
    spec = importlib.util.spec_from_file_location("modelo_a_prueba", CARPETA / "modelo.py")
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


@pytest.fixture
def servicio():
    """Un servicio de mentira en esta máquina, que habla como 'chat completions'."""
    estado = {"contenido": '{"producto":"cinta_5m"}', "codigo": 200, "crudo": None, "pedidos": []}

    class Atiende(BaseHTTPRequestHandler):
        def do_POST(self):
            largo = int(self.headers.get("Content-Length", 0))
            estado["pedidos"].append({
                "cuerpo": json.loads(self.rfile.read(largo).decode("utf-8")),
                "autorizacion": self.headers.get("Authorization"),
            })
            if estado["crudo"] is not None:
                cuerpo = estado["crudo"]
            else:
                cuerpo = json.dumps({"choices": [{"message": {"content": estado["contenido"]}}]})
            self.send_response(estado["codigo"])
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(cuerpo.encode("utf-8"))

        def log_message(self, *a):
            pass

    servidor = HTTPServer(("127.0.0.1", 0), Atiende)
    threading.Thread(target=servidor.serve_forever, daemon=True).start()
    estado["url"] = "http://127.0.0.1:%d/v1/chat/completions" % servidor.server_port
    yield estado
    servidor.shutdown()
    servidor.server_close()


# ---- proveedor simulado ----

def test_sin_configurar_nada_es_simulado_y_devuelve_json(modelo):
    assert modelo.proveedor() == "simulado"
    dato = json.loads(modelo.pedir_al_modelo("Elegí.", "la de 5 m"))
    assert dato == {"simulado": True, "pregunta": "la de 5 m"}


def test_respuesta_valida_simulada(modelo):
    modelo.simular_modelo(['{"producto": "cinta_5m"}'])
    assert modelo.pedir_al_modelo("Elegí.", "la de 5 m") == '{"producto":"cinta_5m"}'
    assert modelo.pedidos_al_modelo() == [
        {"instrucciones": "Elegí.", "pregunta": "la de 5 m", "respuesta": '{"producto":"cinta_5m"}'}]


def test_acepta_el_json_envuelto_en_un_bloque(modelo):
    modelo.simular_modelo(['```json\n{"producto": "cinta_5m"}\n```'])
    assert modelo.pedir_al_modelo("a", "b") == '{"producto":"cinta_5m"}'


@pytest.mark.parametrize("mala", ["Claro, es la cinta de 5 m", '{"producto": ', '["cinta_5m"]', '"cinta"', "   "])
def test_respuesta_invalida_simulada(modelo, mala):
    modelo.simular_modelo([mala])
    with pytest.raises(ValueError, match="el modelo"):
        modelo.pedir_al_modelo("a", "b")
    assert modelo.pedidos_al_modelo() == []


def test_falla_de_conexion_simulada(modelo):
    modelo.simular_modelo(["!conexion", '{"producto":"cinta_5m"}'])
    with pytest.raises(ConnectionError, match="no se pudo llegar"):
        modelo.pedir_al_modelo("a", "b")
    assert modelo.pedir_al_modelo("a", "b") == '{"producto":"cinta_5m"}'


def test_simular_no_usa_la_red_aunque_haya_direccion(modelo, monkeypatch):
    monkeypatch.setenv("MATE_MODELO_PROPIO_URL", "http://127.0.0.1:9/nada")
    assert modelo.proveedor() == "propio"
    modelo.simular_modelo(['{"ok": true}'])
    assert modelo.proveedor() == "simulado"
    assert modelo.pedir_al_modelo("a", "b") == '{"ok":true}'


def test_argumentos_mal_pasados(modelo):
    with pytest.raises(TypeError):
        modelo.pedir_al_modelo("a", 5)
    with pytest.raises(TypeError):
        modelo.simular_modelo("no es una lista")


# ---- modelo propio (servicio de mentira en esta máquina) ----

def test_respuesta_valida_del_servicio(modelo, servicio, monkeypatch):
    monkeypatch.setenv("MATE_MODELO_PROPIO_URL", servicio["url"])
    monkeypatch.setenv("MATE_MODELO_PROPIO_NOMBRE", "mi-modelo")
    monkeypatch.setenv("MATE_MODELO_PROPIO_CLAVE", "clave-de-mentira")
    assert modelo.proveedor() == "propio"
    assert modelo.pedir_al_modelo("Elegí el producto.", "la de 5 m") == '{"producto":"cinta_5m"}'
    pedido = servicio["pedidos"][0]
    assert pedido["autorizacion"] == "Bearer clave-de-mentira"
    assert pedido["cuerpo"]["model"] == "mi-modelo"
    assert pedido["cuerpo"]["messages"][1] == {"role": "user", "content": "la de 5 m"}
    assert pedido["cuerpo"]["messages"][0]["content"].startswith("Elegí el producto.")


def test_respuesta_invalida_del_servicio(modelo, servicio, monkeypatch):
    monkeypatch.setenv("MATE_MODELO_PROPIO_URL", servicio["url"])
    servicio["contenido"] = "Es la cinta de 5 metros."
    with pytest.raises(ValueError, match="no es JSON"):
        modelo.pedir_al_modelo("a", "b")
    servicio["crudo"] = '{"otra": "forma"}'
    with pytest.raises(ValueError, match="forma que no conozco"):
        modelo.pedir_al_modelo("a", "b")


def test_el_servicio_contesta_con_error_y_no_muestra_la_clave(modelo, servicio, monkeypatch):
    monkeypatch.setenv("MATE_MODELO_PROPIO_URL", servicio["url"])
    monkeypatch.setenv("MATE_MODELO_PROPIO_CLAVE", "clave-de-mentira")
    servicio["codigo"] = 401
    servicio["crudo"] = '{"error": "clave-de-mentira no vale"}'
    with pytest.raises(ConnectionError, match="401") as error:
        modelo.pedir_al_modelo("a", "b")
    assert "clave-de-mentira" not in str(error.value)


def test_falla_de_conexion_de_verdad(modelo, monkeypatch):
    libre = socket.socket()
    libre.bind(("127.0.0.1", 0))
    puerto = libre.getsockname()[1]
    libre.close()
    monkeypatch.setenv("MATE_MODELO_PROPIO_URL",
                       "http://usuario:secreto@127.0.0.1:%d/v1/chat/completions?k=secreto" % puerto)
    with pytest.raises(ConnectionError, match="no se pudo llegar") as error:
        modelo.pedir_al_modelo("a", "b")
    assert "secreto" not in str(error.value)


def test_direccion_mal_escrita(modelo, monkeypatch):
    monkeypatch.setenv("MATE_MODELO_PROPIO_URL", "localhost:11434")
    with pytest.raises(ValueError, match="http"):
        modelo.pedir_al_modelo("a", "b")


def test_forzar_el_simulado(modelo, monkeypatch):
    monkeypatch.setenv("MATE_MODELO_PROPIO_URL", "http://127.0.0.1:9/nada")
    monkeypatch.setenv("MATE_MODELO_PROPIO_SIMULADO", "1")
    assert modelo.proveedor() == "simulado"


# ---- desde Mate ----

def test_el_programa_de_muestra_pasa_sus_pruebas(tmp_path):
    import os
    entorno = {k: v for k, v in os.environ.items() if k not in VARIABLES}
    entorno["MATE_SIN_REGISTRO"] = "1"
    for orden in ("probar", "correr"):
        corrida = subprocess.run(
            [sys.executable, str(MATE), orden, str(CARPETA / "probar_modelo.mate")],
            capture_output=True, text=True, encoding="utf-8", env=entorno, cwd=str(tmp_path))
        assert corrida.returncode == 0, corrida.stdout + corrida.stderr
    assert "cinta_5m" in corrida.stdout
