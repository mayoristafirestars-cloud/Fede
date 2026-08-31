from buscador.aeropuertos import (
    AEROPUERTOS,
    alternativos,
    buscar_aeropuerto,
    distancia_km,
    nombre,
    normalizar,
)


def test_catalogo_cubre_argentina():
    argentinos = [a for a in AEROPUERTOS.values() if a.pais == "AR"]
    assert len(argentinos) >= 25
    for imprescindible in ("AEP", "EZE", "COR", "MDZ", "BRC", "RSA", "BHI", "USH"):
        assert imprescindible in AEROPUERTOS


def test_codigos_son_iata_de_tres_letras():
    assert all(len(c) == 3 and c.isupper() for c in AEROPUERTOS)


def test_coordenadas_dentro_de_rango():
    for a in AEROPUERTOS.values():
        assert -90 <= a.lat <= 90, a.iata
        assert -180 <= a.lon <= 180, a.iata


def test_distancia_conocida():
    # AEP-BRC: ~1.335 km en línea recta (la ruta por tierra da bastante más).
    d = distancia_km("AEP", "BRC")
    assert d is not None and 1300 < d < 1370

    # EZE-MAD: ~10.050 km, el clásico vuelo a Europa.
    d = distancia_km("EZE", "MAD")
    assert d is not None and 9900 < d < 10200


def test_distancia_es_simetrica_y_cero_consigo_misma():
    assert distancia_km("EZE", "MAD") == distancia_km("MAD", "EZE")
    assert distancia_km("EZE", "EZE") == 0


def test_distancia_con_codigo_desconocido_no_explota():
    assert distancia_km("AEP", "XXX") is None


def test_normalizar_saca_acentos():
    assert normalizar("Córdoba") == "cordoba"
    assert normalizar("  SÃO PAULO ") == "sao paulo"


def test_buscar_por_iata_es_exacto():
    assert [a.iata for a in buscar_aeropuerto("eze")] == ["EZE"]


def test_buscar_por_ciudad_sin_acentos():
    assert "COR" in [a.iata for a in buscar_aeropuerto("cordoba")]


def test_buscar_ciudad_multiaeropuerto_devuelve_todos():
    codigos = [a.iata for a in buscar_aeropuerto("buenos aires")]
    assert set(codigos) == {"AEP", "EZE"}


def test_alternativos_de_santa_rosa_incluye_bahia_blanca():
    assert "BHI" in dict(alternativos("RSA", radio_km=400))


def test_alternativos_respeta_el_radio():
    cercanos = dict(alternativos("RSA", radio_km=350))
    lejanos = dict(alternativos("RSA", radio_km=700))
    assert set(cercanos) <= set(lejanos)
    assert "AEP" in lejanos and "AEP" not in cercanos


def test_alternativos_ordena_por_cercania():
    km = [k for _, k in alternativos("RSA", radio_km=700)]
    assert km == sorted(km)


def test_multiaeropuerto_se_considera_alternativo_mutuo():
    assert "EZE" in dict(alternativos("AEP", radio_km=100))
    assert "AEP" in dict(alternativos("EZE", radio_km=100))


def test_nombre_legible_y_fallback():
    assert nombre("brc") == "San Carlos de Bariloche (BRC)"
    assert nombre("zzz") == "ZZZ"


class TestNombresEscritosAMano:
    """En la línea de comandos nadie escribe los nombres como en el catálogo."""

    def test_los_guiones_valen_como_espacios(self):
        assert [a.iata for a in buscar_aeropuerto("santa-rosa")] == ["RSA"]
        assert set(a.iata for a in buscar_aeropuerto("Buenos-Aires")) == {"AEP", "EZE"}

    def test_el_guion_bajo_tambien(self):
        assert [a.iata for a in buscar_aeropuerto("santa_rosa")] == ["RSA"]

    def test_no_hace_falta_escribir_el_parentesis_que_desambigua(self):
        # El catálogo dice "Santa Rosa (La Pampa)"; el usuario escribe "santa rosa".
        assert [a.iata for a in buscar_aeropuerto("santa rosa")] == ["RSA"]

    def test_espacios_de_mas_no_molestan(self):
        assert [a.iata for a in buscar_aeropuerto("  mar   del  plata ")] == ["MDQ"]

    def test_sigue_encontrando_por_nombre_de_aeropuerto(self):
        assert "EZE" in [a.iata for a in buscar_aeropuerto("pistarini")]

    def test_normalizar_unifica_separadores(self):
        assert normalizar("São-Paulo") == "sao paulo"
        assert normalizar(" EL  CALAFATE ") == "el calafate"
