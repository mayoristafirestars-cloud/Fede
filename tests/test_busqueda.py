from datetime import date, datetime, timedelta

import pytest

from buscador.busqueda import buscar, planificar
from buscador.modelos import Consulta, Equipaje, Itinerario, Oferta, Segmento
from buscador.proveedores.base import ErrorProveedor, Proveedor

HOY = date.today()
IDA = HOY + timedelta(days=60)
VUELTA = HOY + timedelta(days=67)


def oferta(precio, origen="AEP", destino="BRC", escalas=0, bodega=1, aer="AR", nro="1000"):
    salida = datetime.combine(IDA, datetime.min.time()).replace(hour=8)
    if escalas == 0:
        segs = [Segmento(origen, destino, salida, salida + timedelta(minutes=140), aer, nro)]
    else:
        medio = Segmento(origen, "COR", salida, salida + timedelta(minutes=80), aer, nro)
        segs = [medio, Segmento("COR", destino, medio.llegada + timedelta(minutes=60),
                                medio.llegada + timedelta(minutes=180), aer, nro + "b")]
    return Oferta(
        proveedor="falso", precio=precio, moneda="USD", ida=Itinerario(segs),
        equipaje=Equipaje(bodega_incluidas=bodega),
    )


class ProveedorFalso(Proveedor):
    nombre = "falso"
    costo_por_busqueda = 1

    def __init__(self, ofertas=None, falla=False):
        self._ofertas = ofertas
        self.falla = falla
        self.llamadas: list[tuple] = []

    def disponible(self):
        return True

    def buscar(self, consulta, origen, destino, fecha_ida, fecha_vuelta, limite=20):
        self.llamadas.append((origen, destino, fecha_ida, fecha_vuelta))
        if self.falla:
            raise ErrorProveedor("la API dijo que no")
        if self._ofertas is not None:
            return self._ofertas
        return [oferta(100 + len(self.llamadas), origen, destino)]


@pytest.fixture
def consulta():
    return Consulta(origen="AEP", destino="BRC", fecha_ida=IDA, fecha_vuelta=VUELTA)


class TestPlanificar:
    def test_sin_flexibilidad_es_una_sola_busqueda(self, consulta):
        plan = planificar(consulta)
        assert len(plan) == 1
        assert plan[0].clave() == ("AEP", "BRC", IDA, VUELTA)

    def test_lo_pedido_por_el_usuario_va_primero(self, consulta):
        consulta.flex_dias = 2
        plan = planificar(consulta, radio_terrestre_km=400)
        assert plan[0].clave() == ("AEP", "BRC", IDA, VUELTA)
        assert plan[0].prioridad == 0

    def test_cambiar_de_aeropuerto_pesa_mas_que_correr_un_dia(self, consulta):
        consulta.flex_dias = 1
        plan = planificar(consulta, radio_terrestre_km=100)
        otra_fecha = next(c for c in plan if c.origen == "AEP" and c.fecha_ida != IDA)
        otro_aeropuerto = next(c for c in plan if c.origen == "EZE")
        assert otra_fecha.prioridad < otro_aeropuerto.prioridad

    def test_radio_terrestre_suma_aeropuertos_alternativos(self, consulta):
        sin_radio = {c.origen for c in planificar(consulta, radio_terrestre_km=0)}
        con_radio = {c.origen for c in planificar(consulta, radio_terrestre_km=100)}
        assert sin_radio == {"AEP"}
        assert "EZE" in con_radio

    def test_nunca_planifica_origen_igual_a_destino(self, consulta):
        consulta.destinos_alternativos = ["AEP"]
        assert all(c.origen != c.destino for c in planificar(consulta))

    def test_registra_los_km_por_tierra(self, consulta):
        plan = planificar(consulta, radio_terrestre_km=100)
        assert next(c for c in plan if c.origen == "EZE").km_terrestres > 0


class TestBuscar:
    def test_devuelve_ofertas_y_resumen(self, consulta, monkeypatch):
        falso = ProveedorFalso()
        monkeypatch.setattr("buscador.busqueda.proveedores_disponibles", lambda solo=None: [falso])

        r = buscar(consulta)
        assert len(r.ofertas) == 1
        assert r.combinaciones_consultadas == 1
        assert r.proveedores == ["falso"]
        assert not r.errores

    def test_respeta_el_presupuesto_de_requests(self, consulta, monkeypatch):
        consulta.flex_dias = 3
        falso = ProveedorFalso()
        monkeypatch.setattr("buscador.busqueda.proveedores_disponibles", lambda solo=None: [falso])

        r = buscar(consulta, presupuesto_requests=5)
        assert len(falso.llamadas) <= 5
        assert r.combinaciones_consultadas <= 5

    def test_un_proveedor_caido_no_tumba_la_busqueda(self, consulta, monkeypatch):
        roto, sano = ProveedorFalso(falla=True), ProveedorFalso()
        sano.nombre = "sano"
        monkeypatch.setattr("buscador.busqueda.proveedores_disponibles",
                            lambda solo=None: [roto, sano])

        r = buscar(consulta, presupuesto_requests=10)
        assert r.ofertas, "las ofertas del proveedor sano tienen que llegar"
        assert any("la API dijo que no" in e for e in r.errores)

    def test_deduplica_el_mismo_vuelo_de_dos_proveedores(self, consulta, monkeypatch):
        misma = oferta(150)
        a, b = ProveedorFalso([misma]), ProveedorFalso([oferta(150)])
        b.nombre = "otro"
        monkeypatch.setattr("buscador.busqueda.proveedores_disponibles", lambda solo=None: [a, b])

        r = buscar(consulta, presupuesto_requests=10)
        assert r.ofertas_crudas == 2
        assert len(r.ofertas) == 1

    def test_sin_proveedores_avisa_en_vez_de_romper(self, consulta, monkeypatch):
        monkeypatch.setattr("buscador.busqueda.proveedores_disponibles", lambda solo=None: [])
        r = buscar(consulta)
        assert r.ofertas == []
        assert r.errores and ".env" in r.errores[0]

    def test_demo_solo_entra_si_no_hay_proveedor_real(self, consulta, monkeypatch):
        from buscador.proveedores.demo import Demo
        real, demo = ProveedorFalso(), Demo()
        monkeypatch.setattr("buscador.busqueda.proveedores_disponibles",
                            lambda solo=None: [real, demo])

        r = buscar(consulta, presupuesto_requests=10)
        assert r.proveedores == ["falso"]


class TestFiltrosDuros:
    def _buscar_con(self, consulta, ofertas, monkeypatch):
        monkeypatch.setattr("buscador.busqueda.proveedores_disponibles",
                            lambda solo=None: [ProveedorFalso(ofertas)])
        return buscar(consulta, presupuesto_requests=5).ofertas

    def test_solo_directos(self, consulta, monkeypatch):
        ofertas = [oferta(100, escalas=1), oferta(200, escalas=0)]
        consulta.solo_directos = True
        assert [o.precio for o in self._buscar_con(consulta, ofertas, monkeypatch)] == [200]

    def test_max_escalas(self, consulta, monkeypatch):
        consulta.max_escalas = 0
        ofertas = [oferta(100, escalas=1)]
        assert self._buscar_con(consulta, ofertas, monkeypatch) == []

    def test_precio_maximo(self, consulta, monkeypatch):
        consulta.precio_max = 150
        ofertas = [oferta(100), oferta(300)]
        assert [o.precio for o in self._buscar_con(consulta, ofertas, monkeypatch)] == [100]

    def test_exige_equipaje_de_bodega(self, consulta, monkeypatch):
        consulta.requiere_equipaje_bodega = True
        ofertas = [oferta(100, bodega=0), oferta(180, bodega=1)]
        assert [o.precio for o in self._buscar_con(consulta, ofertas, monkeypatch)] == [180]

    def test_excluye_aerolineas(self, consulta, monkeypatch):
        consulta.aerolineas_excluidas = ["AR"]
        ofertas = [oferta(100, aer="AR"), oferta(160, aer="FO")]
        assert [o.precio for o in self._buscar_con(consulta, ofertas, monkeypatch)] == [160]


def test_dedupe_conserva_la_tarifa_mas_barata(consulta, monkeypatch):
    cara, barata = oferta(220), oferta(150)
    a, b = ProveedorFalso([cara]), ProveedorFalso([barata])
    b.nombre = "otro"
    monkeypatch.setattr("buscador.busqueda.proveedores_disponibles", lambda solo=None: [a, b])

    r = buscar(consulta, presupuesto_requests=10)
    assert [o.precio for o in r.ofertas] == [150]


def test_mismo_vuelo_con_y_sin_equipaje_son_ofertas_distintas(consulta, monkeypatch):
    sin_bodega, con_bodega = oferta(100, bodega=0), oferta(180, bodega=1)
    monkeypatch.setattr("buscador.busqueda.proveedores_disponibles",
                        lambda solo=None: [ProveedorFalso([sin_bodega, con_bodega])])

    r = buscar(consulta, presupuesto_requests=5)
    assert sorted(o.precio for o in r.ofertas) == [100, 180]


class TestSondeoDeFechas:
    """Fase 1: preguntar gratis dónde mirar antes de gastar créditos."""

    def _proveedor_con_calendario(self, calendario):
        prov = ProveedorFalso()
        prov.fechas_mas_baratas = lambda consulta, origen, destino: calendario  # type: ignore[method-assign]
        return prov

    def test_sin_flexibilidad_no_hay_nada_que_sondear(self, consulta):
        from buscador.busqueda import sondear_fechas

        prov = self._proveedor_con_calendario({IDA: 100.0})
        fechas, avisos = sondear_fechas(consulta, [prov])
        assert fechas == set() and avisos == []

    def test_elige_las_fechas_mas_baratas(self, consulta):
        from buscador.busqueda import sondear_fechas

        consulta.flex_dias = 3
        calendario = {IDA + timedelta(days=d): 1000.0 - d * 10 for d in range(-3, 4)}
        fechas, _ = sondear_fechas(consulta, [self._proveedor_con_calendario(calendario)],
                                   top=3)
        # Las tres más baratas son las de mayor desplazamiento hacia adelante.
        assert {IDA + timedelta(days=d) for d in (1, 2, 3)} <= fechas

    def test_la_fecha_pedida_siempre_se_consulta(self, consulta):
        from buscador.busqueda import sondear_fechas

        consulta.flex_dias = 3
        calendario = {IDA + timedelta(days=d): 100.0 for d in range(1, 4)}
        calendario[IDA] = 999_999.0        # carísima, el sondeo la descartaría
        fechas, _ = sondear_fechas(consulta, [self._proveedor_con_calendario(calendario)],
                                   top=2)
        assert IDA in fechas

    def test_ignora_fechas_fuera_del_rango_pedido(self, consulta):
        from buscador.busqueda import sondear_fechas

        consulta.flex_dias = 1
        calendario = {IDA + timedelta(days=d): 100.0 for d in (-30, 0, 30)}
        fechas, _ = sondear_fechas(consulta, [self._proveedor_con_calendario(calendario)])
        assert fechas == {IDA}

    def test_un_sondeo_que_falla_no_rompe_la_busqueda(self, consulta):
        from buscador.busqueda import sondear_fechas

        consulta.flex_dias = 2
        roto = ProveedorFalso()
        roto.fechas_mas_baratas = lambda *a, **kw: (_ for _ in ()).throw(  # type: ignore[method-assign]
            ErrorProveedor("no soportado"))
        fechas, avisos = sondear_fechas(consulta, [roto])
        assert fechas == set()
        assert any("no soportado" in a for a in avisos)

    def test_el_sondeo_recorta_el_plan(self, consulta, monkeypatch):
        consulta.flex_dias = 3
        calendario = {IDA + timedelta(days=d): 1000.0 + abs(d) for d in range(-3, 4)}
        prov = self._proveedor_con_calendario(calendario)
        monkeypatch.setattr("buscador.busqueda.proveedores_disponibles", lambda solo=None: [prov])

        sin_sondeo = len(planificar(consulta))
        r = buscar(consulta, presupuesto_requests=100)
        assert r.combinaciones_consultadas < sin_sondeo
        assert r.sondeo, "el resumen tiene que contar que hubo sondeo"
