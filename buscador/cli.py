"""Línea de comandos del buscador de pasajes.

    python -m buscador RSA BRC --ida 15/10 --vuelta 22/10 --flex 3 --cerca 400
"""
from __future__ import annotations

import argparse
import json
import logging
import sys
from dataclasses import asdict
from datetime import date, datetime, timedelta

from buscador.aeropuertos import buscar_aeropuerto, nombre as nombre_aeropuerto
from buscador.busqueda import buscar
from buscador.config import env_int
from buscador.modelos import Consulta
from buscador.precios_ar import aplicar_costo_real, cotizaciones
from buscador.ranking import Preferencias, mas_barata, mas_rapida, rankear
from buscador.reporte import render_consola, render_markdown

log = logging.getLogger("buscador")


def parsear_fecha(texto: str, referencia: date | None = None) -> date:
    """Acepta 15/10, 15/10/2026, 2026-10-15 y atajos como +45d o 'hoy'.

    Con día y mes sin año, elige el próximo que todavía no pasó: pedir un
    vuelo para el 15/10 en noviembre significa el 15/10 del año que viene.
    """
    texto = texto.strip().lower()
    hoy = referencia or date.today()

    if texto in {"hoy", "today"}:
        return hoy
    if texto in {"mañana", "manana", "tomorrow"}:
        return hoy + timedelta(days=1)
    if texto.startswith("+") and texto.endswith("d"):
        return hoy + timedelta(days=int(texto[1:-1]))

    for formato in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%d/%m", "%d-%m"):
        try:
            momento = datetime.strptime(texto, formato).date()
        except ValueError:
            continue
        if "%Y" not in formato:
            momento = momento.replace(year=hoy.year)
            if momento < hoy:
                momento = momento.replace(year=hoy.year + 1)
        return momento

    raise argparse.ArgumentTypeError(
        f"no entiendo la fecha {texto!r}. Probá 15/10, 2026-10-15 o +45d"
    )


def resolver_aeropuerto(texto: str) -> str:
    """Convierte 'bariloche' o 'BRC' en un código IATA, o falla con opciones."""
    candidatos = buscar_aeropuerto(texto)
    if not candidatos:
        raise SystemExit(
            f"No reconozco el aeropuerto {texto!r}. Usá un código IATA de tres "
            "letras (por ejemplo BRC) o el nombre de la ciudad."
        )
    if len(candidatos) > 1 and len(texto.strip()) != 3:
        # Buenos Aires y São Paulo tienen más de un aeropuerto: se avisa cuál
        # se eligió y cómo pedir el otro.
        opciones = ", ".join(f"{a.iata} ({a.nombre})" for a in candidatos)
        print(f"⚠ {texto!r} coincide con varios aeropuertos: {opciones}.",
              f"Se usa {candidatos[0].iata}; agregá --cerca para incluir los demás.",
              file=sys.stderr)
    return candidatos[0].iata


def construir_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="buscador",
        description="Busca pasajes aéreos y los ordena por lo que realmente te cuestan.",
        epilog=(
            "Ejemplos:\n"
            "  python -m buscador RSA BRC --ida 15/10 --vuelta 22/10\n"
            "  python -m buscador Buenos-Aires Madrid --ida +60d --flex 3 --pago dolares\n"
            "  python -m buscador RSA MDZ --ida 10/11 --cerca 400 --perfil mochilero\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("origen", help="código IATA o ciudad de salida")
    p.add_argument("destino", help="código IATA o ciudad de llegada")

    f = p.add_argument_group("fechas")
    f.add_argument("--ida", required=True, help="fecha de ida (15/10, 2026-10-15, +45d)")
    f.add_argument("--vuelta", help="fecha de vuelta; omitila para un solo tramo")
    f.add_argument("--flex", type=int, default=0, metavar="N",
                   help="probar también N días antes y después (default: 0)")

    v = p.add_argument_group("viajeros")
    v.add_argument("--adultos", type=int, default=1)
    v.add_argument("--ninos", type=int, default=0, help="de 2 a 11 años")
    v.add_argument("--infantes", type=int, default=0, help="menores de 2 años, en falda")
    v.add_argument("--cabina", default="ECONOMY",
                   choices=["ECONOMY", "PREMIUM_ECONOMY", "BUSINESS", "FIRST"])

    e = p.add_argument_group("equipaje")
    e.add_argument("--sin-carry-on", action="store_true",
                   help="viajás sólo con una mochila chica bajo el asiento")
    e.add_argument("--bodega", type=int, default=0, metavar="N",
                   help="cuántas valijas despachadas necesitás (default: 0)")

    r = p.add_argument_group("filtros")
    r.add_argument("--directo", action="store_true", help="sólo vuelos sin escalas")
    r.add_argument("--max-escalas", type=int, metavar="N")
    r.add_argument("--sin-aerolinea", default="", metavar="AR,FO",
                   help="códigos IATA de aerolíneas a excluir, separados por coma")
    r.add_argument("--precio-max", type=float, metavar="MONTO")
    r.add_argument("--cerca", type=int, default=0, metavar="KM",
                   help="incluir aeropuertos alternativos hasta KM por ruta")

    o = p.add_argument_group("criterio")
    o.add_argument("--perfil", default="ocio",
                   choices=["mochilero", "ocio", "comodo", "trabajo", "solo-precio"],
                   help="cuánto vale tu tiempo frente a la plata (default: ocio)")
    o.add_argument("--pago", default="tarjeta", choices=["tarjeta", "dolares"],
                   help="cómo vas a pagar: cambia el precio real (default: tarjeta)")
    o.add_argument("--moneda", default="ARS", help="moneda a pedirle al proveedor")

    s = p.add_argument_group("salida")
    s.add_argument("--top", type=int, default=8, help="cuántas opciones mostrar")
    s.add_argument("--markdown", action="store_true")
    s.add_argument("--json", action="store_true")
    s.add_argument("--sin-color", action="store_true")
    s.add_argument("--verboso", "-v", action="store_true")

    t = p.add_argument_group("proveedores")
    t.add_argument("--proveedor", action="append", default=[], metavar="NOMBRE",
                   help="usar sólo estos (serpapi, travelpayouts, demo)")
    t.add_argument("--presupuesto", type=int, default=env_int("PRESUPUESTO_REQUESTS", 40),
                   metavar="N", help="tope de llamadas a las APIs")
    return p


def _a_json(ofertas, consulta, resumen) -> str:
    def itinerario(it):
        if it is None:
            return None
        return {
            "origen": it.origen, "destino": it.destino,
            "salida": it.salida.isoformat(), "llegada": it.llegada.isoformat(),
            "duracion_min": it.duracion_min, "escalas": it.escalas,
            "esperas_min": it.layovers_min,
            "segmentos": [asdict(s) | {"salida": s.salida.isoformat(),
                                       "llegada": s.llegada.isoformat()}
                          for s in it.segmentos],
        }

    return json.dumps({
        "consulta": {
            "origen": consulta.origen, "destino": consulta.destino,
            "ida": consulta.fecha_ida.isoformat(),
            "vuelta": consulta.fecha_vuelta.isoformat() if consulta.fecha_vuelta else None,
            "pasajeros": consulta.pasajeros,
        },
        "resumen": resumen,
        "ofertas": [{
            "proveedor": o.proveedor, "precio": o.precio, "moneda": o.moneda,
            "precio_final_ars": o.precio_ars_final, "puntaje": o.puntaje,
            "indicativo": o.indicativo,
            "aerolineas": o.aerolineas, "escalas": o.escalas_totales,
            "duracion_min": o.duracion_total_min,
            "equipaje": asdict(o.equipaje),
            "desglose": o.desglose_precio, "motivos": o.motivos,
            "url": o.url_reserva,
            "ida": itinerario(o.ida), "vuelta": itinerario(o.vuelta),
        } for o in ofertas],
    }, ensure_ascii=False, indent=2, default=str)


def main(argv: list[str] | None = None) -> int:
    args = construir_parser().parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verboso else logging.WARNING,
        format="%(levelname)s %(name)s: %(message)s",
    )

    fecha_ida = parsear_fecha(args.ida)
    fecha_vuelta = parsear_fecha(args.vuelta) if args.vuelta else None
    if fecha_vuelta and fecha_vuelta < fecha_ida:
        raise SystemExit("La fecha de vuelta es anterior a la de ida.")

    consulta = Consulta(
        origen=resolver_aeropuerto(args.origen),
        destino=resolver_aeropuerto(args.destino),
        fecha_ida=fecha_ida,
        fecha_vuelta=fecha_vuelta,
        adultos=args.adultos, ninos=args.ninos, infantes=args.infantes,
        cabina=args.cabina, moneda=args.moneda.upper(),
        flex_dias=max(args.flex, 0),
        solo_directos=args.directo,
        max_escalas=args.max_escalas,
        aerolineas_excluidas=[a.strip().upper() for a in args.sin_aerolinea.split(",") if a.strip()],
        precio_max=args.precio_max,
        requiere_equipaje_bodega=args.bodega > 0,
    )

    resultado = buscar(
        consulta,
        presupuesto_requests=args.presupuesto,
        radio_terrestre_km=args.cerca,
        solo_proveedores=args.proveedor or None,
    )

    if not resultado.ofertas:
        for e in resultado.errores:
            print(f"⚠ {e}", file=sys.stderr)
        print("No se encontraron vuelos con esos criterios.")
        return 1

    # El precio comparable es el costo real en pesos, no el de vidriera.
    forma_de_pago = "dolares" if args.pago == "dolares" else "tarjeta_pesos"
    try:
        cotiz = cotizaciones()
        aplicar_costo_real(
            resultado.ofertas,
            forma_de_pago=forma_de_pago,
            quiere_carry_on=not args.sin_carry_on,
            piezas_bodega=args.bodega,
            cotiz=cotiz,
        )
        tipo_cambio = 1.0 if consulta.moneda == "ARS" else cotiz.tarjeta
    except RuntimeError as e:
        print(f"⚠ {e}", file=sys.stderr)
        tipo_cambio = 1.0

    preferencias = (
        Preferencias.solo_precio(moneda="ARS") if args.perfil == "solo-precio"
        else Preferencias.perfil(args.perfil, tipo_cambio=tipo_cambio, moneda="ARS")
    )
    ofertas = rankear(resultado.ofertas, consulta, preferencias)

    if args.json:
        print(_a_json(ofertas, consulta, resultado.resumen()))
        return 0
    if args.markdown:
        print(render_markdown(ofertas, consulta, top=args.top))
        return 0

    print(render_consola(
        ofertas, consulta, top=args.top,
        color=not args.sin_color and sys.stdout.isatty(),
        resumen_busqueda=resultado.resumen(),
        barata=mas_barata(ofertas), rapida=mas_rapida(ofertas),
    ))
    for e in resultado.errores:
        print(f"⚠ {e}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
