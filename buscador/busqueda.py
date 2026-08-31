"""Orquestador: convierte una `Consulta` en la mejor lista de ofertas posible.

El problema central no es pedir precios, es decidir QUÉ pedir. Una consulta
con ±3 días de flexibilidad y dos aeropuertos alternativos por punta son
7×7×4 = 196 búsquedas; a 1 request cada una, funde cualquier cuota gratuita.

La estrategia es en dos fases:

1. **Sondeo barato.** Si el proveedor expone un calendario de precios
   (`fechas_mas_baratas`), se usa para saber a qué fechas apuntar antes de
   gastar requests caros. Cuesta 1-2 llamadas y descarta el 80% del espacio.
2. **Búsqueda detallada.** Sólo sobre las combinaciones prometedoras, hasta
   agotar el presupuesto de requests, siempre empezando por la ruta y las
   fechas que el usuario pidió (esas nunca se saltean).
"""
from __future__ import annotations

import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from datetime import date
from typing import Optional

from buscador.modelos import Consulta, Oferta
from buscador.proveedores import Proveedor, proveedores_disponibles
from buscador.proveedores.base import ErrorProveedor

log = logging.getLogger(__name__)


@dataclass
class Combinacion:
    """Una búsqueda concreta a ejecutar."""

    origen: str
    destino: str
    fecha_ida: date
    fecha_vuelta: Optional[date]
    prioridad: int = 0          # menor = se ejecuta antes
    km_terrestres: int = 0      # cuánto hay que manejar para tomar este vuelo

    def clave(self) -> tuple:
        return (self.origen, self.destino, self.fecha_ida, self.fecha_vuelta)


@dataclass
class Resultado:
    ofertas: list[Oferta] = field(default_factory=list)
    combinaciones_consultadas: int = 0
    ofertas_crudas: int = 0
    proveedores: list[str] = field(default_factory=list)
    errores: list[str] = field(default_factory=list)
    sondeo: list[str] = field(default_factory=list)

    def resumen(self) -> dict:
        return {
            "combinaciones": self.combinaciones_consultadas,
            "ofertas_crudas": self.ofertas_crudas,
            "proveedores": self.proveedores,
            "errores": self.errores,
            "sondeo": self.sondeo,
        }


def sondear_fechas(
    consulta: Consulta,
    proveedores: list[Proveedor],
    top: int = 5,
) -> tuple[set[date], list[str]]:
    """Fase 1: pregunta gratis en qué fechas conviene mirar.

    Algunos proveedores devuelven un mes entero de precios mínimos en una
    sola llamada y sin consumir cuota. Con eso se eligen las `top` fechas más
    baratas del rango que pidió el usuario, y la fase cara sólo consulta
    ésas. Es la diferencia entre 49 requests y 5.

    Devuelve el conjunto de fechas de ida a priorizar (vacío si ningún
    proveedor pudo sondear) y los avisos para el resumen.
    """
    if consulta.flex_dias <= 0:
        return set(), []

    permitidas = {ida for ida, _ in consulta.fechas_a_probar()}
    calendario: dict[date, float] = {}
    avisos: list[str] = []

    for proveedor in proveedores:
        try:
            parcial = proveedor.fechas_mas_baratas(consulta, consulta.origen, consulta.destino)
        except ErrorProveedor as e:
            avisos.append(f"sondeo con {proveedor.nombre}: {e}")
            continue
        except Exception as e:
            log.exception("fallo inesperado sondeando con %s", proveedor.nombre)
            avisos.append(f"sondeo con {proveedor.nombre}: {e.__class__.__name__}")
            continue

        for dia, precio in parcial.items():
            if dia in permitidas and (dia not in calendario or precio < calendario[dia]):
                calendario[dia] = precio

    if not calendario:
        return set(), avisos

    mejores = sorted(calendario.items(), key=lambda kv: kv[1])[:top]
    elegidas = {dia for dia, _ in mejores}
    # La fecha que pidió el usuario siempre se consulta, aunque el sondeo la
    # haya descartado: puede tener un motivo para viajar ese día.
    elegidas.add(consulta.fecha_ida)
    avisos.append(
        f"sondeo: {len(calendario)} fechas con precio, se consultan {len(elegidas)}"
    )
    return elegidas, avisos


def planificar(
    consulta: Consulta,
    radio_terrestre_km: int = 0,
    fechas_permitidas: set[date] | None = None,
) -> list[Combinacion]:
    """Arma la lista ordenada de búsquedas a ejecutar.

    El orden importa: si el presupuesto se agota a mitad de camino, queremos
    haber consultado primero lo que el usuario efectivamente pidió.
    `fechas_permitidas` es el recorte que dejó la fase de sondeo.
    """
    from buscador.aeropuertos import alternativos

    origenes: dict[str, int] = {consulta.origen: 0}
    destinos: dict[str, int] = {consulta.destino: 0}
    for extra in consulta.origenes_alternativos:
        origenes.setdefault(extra, 0)
    for extra in consulta.destinos_alternativos:
        destinos.setdefault(extra, 0)

    if radio_terrestre_km > 0:
        for codigo, km in alternativos(consulta.origen, radio_terrestre_km):
            origenes.setdefault(codigo, km)
        for codigo, km in alternativos(consulta.destino, radio_terrestre_km):
            destinos.setdefault(codigo, km)

    combinaciones: list[Combinacion] = []
    for (ida, vuelta) in consulta.fechas_a_probar():
        if fechas_permitidas and ida not in fechas_permitidas:
            continue
        desfase_fecha = abs((ida - consulta.fecha_ida).days)
        if vuelta and consulta.fecha_vuelta:
            desfase_fecha += abs((vuelta - consulta.fecha_vuelta).days)
        for origen, km_o in origenes.items():
            for destino, km_d in destinos.items():
                if origen == destino:
                    continue
                desfase_ruta = (0 if origen == consulta.origen else 1) + \
                               (0 if destino == consulta.destino else 1)
                combinaciones.append(Combinacion(
                    origen=origen,
                    destino=destino,
                    fecha_ida=ida,
                    fecha_vuelta=vuelta,
                    # La ruta exacta pesa más que la fecha exacta: cambiar de
                    # aeropuerto implica manejar horas, correr un día no.
                    prioridad=desfase_ruta * 10 + desfase_fecha,
                    km_terrestres=km_o + km_d,
                ))

    combinaciones.sort(key=lambda c: (c.prioridad, c.km_terrestres, c.fecha_ida))
    return combinaciones


def _consultar(
    proveedor: Proveedor,
    consulta: Consulta,
    comb: Combinacion,
    limite: int,
) -> tuple[list[Oferta], Optional[str]]:
    try:
        ofertas = proveedor.buscar(
            consulta, comb.origen, comb.destino, comb.fecha_ida, comb.fecha_vuelta, limite
        )
        for o in ofertas:
            o.desglose_precio.setdefault("km_terrestres", float(comb.km_terrestres))
        return ofertas, None
    except ErrorProveedor as e:
        return [], f"{proveedor.nombre}: {e}"
    except Exception as e:  # una API caída no puede tumbar la búsqueda entera
        log.exception("fallo inesperado en %s", proveedor.nombre)
        return [], f"{proveedor.nombre}: error inesperado ({e.__class__.__name__}: {e})"


def buscar(
    consulta: Consulta,
    presupuesto_requests: int = 40,
    limite_por_busqueda: int = 20,
    radio_terrestre_km: int = 0,
    solo_proveedores: list[str] | None = None,
    hilos: int = 4,
    max_combinaciones: int = 60,
) -> Resultado:
    """Ejecuta la búsqueda completa y devuelve las ofertas sin rankear."""
    disponibles = proveedores_disponibles(solo_proveedores)
    reales = [p for p in disponibles if p.nombre != "demo"]
    # El proveedor demo es la red de seguridad: sólo entra si no hay nada real
    # o si se lo pidió explícitamente por nombre.
    usar = reales or [p for p in disponibles if p.nombre == "demo"]
    if solo_proveedores:
        usar = [p for p in disponibles if p.nombre in solo_proveedores]

    resultado = Resultado(proveedores=[p.nombre for p in usar])
    if not usar:
        resultado.errores.append(
            "No hay proveedores disponibles. Cargá credenciales en .env "
            "(ver .env.example) o usá --proveedor demo."
        )
        return resultado

    # Fase 1: sondeo gratis para no gastar créditos en fechas que no valen.
    fechas, avisos = sondear_fechas(consulta, usar)
    resultado.errores.extend(a for a in avisos if "sondeo con" in a)
    resultado.sondeo = [a for a in avisos if not a.startswith("sondeo con")]

    # Fase 2: la búsqueda cara, sólo sobre lo que sobrevivió al sondeo.
    combinaciones = planificar(consulta, radio_terrestre_km, fechas or None)
    log.info("plan: %d combinaciones, presupuesto %d requests",
             len(combinaciones), presupuesto_requests)

    # Dos topes distintos, porque miden cosas distintas:
    #
    # - `presupuesto_requests` cuida la cuota de las APIs pagas.
    # - `max_combinaciones` cuida el tiempo y el ruido. Un proveedor gratis
    #   tiene costo cero y por sí solo nunca agotaría el presupuesto, así que
    #   sin este segundo tope una consulta con flexibilidad y aeropuertos
    #   alternativos dispara cientos de búsquedas: 7 fechas de ida x 7 de
    #   vuelta x 14 pares de aeropuertos son 686. Devuelve miles de ofertas
    #   casi idénticas y tarda una eternidad, sin mejorar el resultado.
    tope = min(len(combinaciones), max(max_combinaciones, 1))
    if tope < len(combinaciones):
        resultado.sondeo.append(
            f"plan recortado: {len(combinaciones)} combinaciones posibles, "
            f"se consultan las {tope} más prometedoras"
        )

    gastado = 0
    tareas: list[tuple[Proveedor, Combinacion]] = []
    for comb in combinaciones[:tope]:
        for proveedor in usar:
            costo = max(proveedor.costo_por_busqueda, 0)
            if gastado + costo > presupuesto_requests and tareas:
                break
            tareas.append((proveedor, comb))
            gastado += costo
        else:
            continue
        break

    # Clave de oferta -> mejor oferta vista con esa identidad. Cuando dos
    # proveedores traen el mismo vuelo y la misma tarifa, gana el precio menor.
    mejores: dict[tuple, Oferta] = {}
    with ThreadPoolExecutor(max_workers=max(hilos, 1)) as pool:
        futuros = {
            pool.submit(_consultar, prov, consulta, comb, limite_por_busqueda): (prov, comb)
            for prov, comb in tareas
        }
        for futuro in as_completed(futuros):
            ofertas, error = futuro.result()
            resultado.combinaciones_consultadas += 1
            if error:
                resultado.errores.append(error)
                continue
            resultado.ofertas_crudas += len(ofertas)
            for o in ofertas:
                clave = o.clave_dedupe()
                previa = mejores.get(clave)
                if previa is None or o.precio_comparable < previa.precio_comparable:
                    mejores[clave] = o

    resultado.ofertas = [o for o in mejores.values() if _pasa_filtros(o, consulta)]
    return resultado


def _pasa_filtros(o: Oferta, consulta: Consulta) -> bool:
    """Filtros duros: lo que el usuario dijo que no acepta, no se muestra."""
    if consulta.solo_directos and not o.es_directo:
        return False
    if consulta.max_escalas is not None and o.escalas_totales > consulta.max_escalas:
        return False
    if consulta.aerolineas_excluidas and any(
        a in consulta.aerolineas_excluidas for a in o.aerolineas
    ):
        return False
    if consulta.requiere_equipaje_bodega and o.equipaje.bodega_incluidas < 1:
        return False
    if consulta.precio_max is not None and o.precio_comparable > consulta.precio_max:
        return False
    return True
