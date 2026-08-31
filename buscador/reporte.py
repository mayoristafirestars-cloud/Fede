"""Presentación de resultados: consola, Markdown y HTML."""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from buscador.aeropuertos import nombre as nombre_aeropuerto
from buscador.modelos import Consulta, Itinerario, Oferta

_ROSA = {
    "reset": "\033[0m", "negrita": "\033[1m", "tenue": "\033[2m",
    "verde": "\033[32m", "amarillo": "\033[33m", "cyan": "\033[36m", "rojo": "\033[31m",
}


def _c(texto: str, color: str, usar_color: bool = True) -> str:
    if not usar_color:
        return texto
    return f"{_ROSA[color]}{texto}{_ROSA['reset']}"


def fmt_duracion(minutos: int) -> str:
    horas, mins = divmod(max(minutos, 0), 60)
    if horas and mins:
        return f"{horas}h {mins:02d}m"
    if horas:
        return f"{horas}h"
    return f"{mins}m"


def fmt_precio(monto: float, moneda: str) -> str:
    if moneda == "ARS":
        return f"${monto:,.0f}".replace(",", ".")
    return f"{moneda} {monto:,.0f}".replace(",", ".")


def _dias_desfase(salida: datetime, llegada: datetime) -> str:
    delta = (llegada.date() - salida.date()).days
    return f" +{delta}d" if delta > 0 else ""


def describir_itinerario(it: Itinerario) -> str:
    escalas = it.escalas
    if escalas == 0:
        detalle = "directo"
    else:
        vias = " / ".join(s.destino for s in it.segmentos[:-1])
        esperas = " + ".join(fmt_duracion(m) for m in it.layovers_min)
        detalle = f"{escalas} escala{'s' if escalas > 1 else ''} vía {vias} (espera {esperas})"

    return (
        f"{it.origen}→{it.destino}  "
        f"{it.salida:%d/%m %H:%M} → {it.llegada:%H:%M}{_dias_desfase(it.salida, it.llegada)}  "
        f"{fmt_duracion(it.duracion_min)}  ·  {detalle}"
    )


def _etiqueta_equipaje(o: Oferta) -> str:
    partes = []
    partes.append("carry-on ✓" if o.equipaje.mano_incluido else "carry-on ✗")
    if o.equipaje.bodega_incluidas:
        partes.append(f"bodega x{o.equipaje.bodega_incluidas}")
    else:
        partes.append("sin bodega")
    return ", ".join(partes)


def render_consola(
    ofertas: list[Oferta],
    consulta: Consulta,
    top: int = 10,
    color: bool = True,
    resumen_busqueda: Optional[dict] = None,
    barata: Optional[Oferta] = None,
    rapida: Optional[Oferta] = None,
) -> str:
    if not ofertas:
        return _c("No se encontraron vuelos con esos criterios.", "rojo", color)

    lineas: list[str] = []
    cab = (f"{nombre_aeropuerto(consulta.origen)} → {nombre_aeropuerto(consulta.destino)}"
           f"  ·  {consulta.pasajeros} pasajero{'s' if consulta.pasajeros > 1 else ''}"
           f"  ·  {consulta.cabina.lower()}")
    lineas.append("")
    lineas.append(_c(cab, "negrita", color))
    if resumen_busqueda:
        lineas.append(_c(
            f"{resumen_busqueda.get('combinaciones', 0)} búsquedas · "
            f"{resumen_busqueda.get('ofertas_crudas', 0)} ofertas · "
            f"vía {', '.join(resumen_busqueda.get('proveedores', [])) or '—'}",
            "tenue", color))
        for nota in resumen_busqueda.get("sondeo", []):
            lineas.append(_c(nota, "tenue", color))
    lineas.append("─" * 78)

    barata = barata or min(ofertas, key=lambda o: o.precio_comparable)
    rapida = rapida or min(ofertas, key=lambda o: o.duracion_total_min)

    for i, o in enumerate(ofertas[:top], start=1):
        etiquetas = []
        if o is ofertas[0]:
            etiquetas.append(_c("★ MEJOR OPCIÓN", "verde", color))
        if o is barata and o is not ofertas[0]:
            etiquetas.append(_c("💲 EL MÁS BARATO", "amarillo", color))
        if o is rapida and o is not ofertas[0] and o is not barata:
            etiquetas.append(_c("⚡ EL MÁS RÁPIDO", "cyan", color))

        precio = fmt_precio(o.precio_comparable, o.moneda_comparable)
        cabecera = f"{i:>2}. {_c(precio, 'negrita', color)}"
        if o.precio_ars_final is not None and o.moneda != "ARS":
            cabecera += _c(f"  ({fmt_precio(o.precio, o.moneda)})", "tenue", color)
        cabecera += f"  {_c('·', 'tenue', color)} {'+'.join(o.aerolineas)}"
        if o.puntaje is not None:
            cabecera += _c(f"  {o.puntaje:g}/100", "tenue", color)
        if etiquetas:
            cabecera += "  " + " ".join(etiquetas)

        lineas.append("")
        lineas.append(cabecera)
        lineas.append(f"    IDA    {describir_itinerario(o.ida)}")
        if o.vuelta:
            lineas.append(f"    VUELTA {describir_itinerario(o.vuelta)}")
        elif o.datos_proveedor.get("falta_tramo_de_vuelta"):
            lineas.append(_c("    VUELTA (el precio incluye la vuelta; el horario "
                             "se elige al reservar)", "tenue", color))

        extras = [_etiqueta_equipaje(o)]
        if o.asientos_restantes is not None and o.asientos_restantes <= 3:
            extras.append(f"¡quedan {o.asientos_restantes}!")
        if o.self_transfer:
            extras.append("⚠ tramos separados")
        if o.indicativo:
            extras.append("≈ precio de referencia, no cotización en vivo")
        lineas.append(_c("    " + "  ·  ".join(extras), "tenue", color))

        desglose = _linea_desglose(o)
        if desglose:
            lineas.append(_c("    " + desglose, "tenue", color))
        if o.motivos:
            lineas.append(_c("    " + " ".join(o.motivos), "cyan", color))

    lineas.append("")
    lineas.append("─" * 78)
    lineas.extend(_pie(ofertas[0], color))
    return "\n".join(lineas)


def _linea_desglose(o: Oferta) -> str:
    """Muestra de qué está hecho el precio cuando hay algo que no se ve."""
    d = o.desglose_precio
    partes = []
    if d.get("percepcion_rg5617"):
        partes.append(f"percepción 30%: {fmt_precio(d['percepcion_rg5617'], 'ARS')}")
    if d.get("equipaje"):
        partes.append(f"equipaje: {fmt_precio(d['equipaje'], 'ARS')}")
    if d.get("diferencia_vs_mejor"):
        partes.append(f"+{fmt_precio(d['diferencia_vs_mejor'], 'ARS')} de costo total vs. la mejor")
    return "  ·  ".join(partes)


def _pie(mejor: Oferta, color: bool) -> list[str]:
    """Cierre con los avisos que cambian la decisión de compra."""
    pie = []
    d = mejor.desglose_precio
    if d.get("percepcion_rg5617"):
        pie.append(_c(
            f"💡 Pagando en dólares (MEP, débito en USD o stop debit) te ahorrás la "
            f"percepción del 30%: {fmt_precio(d['percepcion_rg5617'], 'ARS')}.",
            "verde", color))
        pie.append(_c(
            "   Si igual pagás en pesos, la percepción es a cuenta de Ganancias y "
            "Bienes Personales: se recupera vía ARCA o SIRADIG.", "tenue", color))
    pie.append(_c(
        f"Consultado el {datetime.now():%d/%m/%Y %H:%M}. La tarifa se confirma recién "
        "al pagar en el sitio de la aerolínea.", "tenue", color))
    return pie


def render_markdown(ofertas: list[Oferta], consulta: Consulta, top: int = 10) -> str:
    if not ofertas:
        return "No se encontraron vuelos con esos criterios."

    out = [
        f"# {nombre_aeropuerto(consulta.origen)} → {nombre_aeropuerto(consulta.destino)}",
        "",
        f"- **Pasajeros:** {consulta.pasajeros}",
        f"- **Ida:** {consulta.fecha_ida:%d/%m/%Y}"
        + (f"  ·  **Vuelta:** {consulta.fecha_vuelta:%d/%m/%Y}" if consulta.fecha_vuelta else ""),
        f"- **Búsqueda:** {datetime.now():%d/%m/%Y %H:%M}",
        "",
        "| # | Precio | Aerolínea | Escalas | Duración | Equipaje |",
        "|---|--------|-----------|---------|----------|----------|",
    ]
    for i, o in enumerate(ofertas[:top], start=1):
        out.append(
            f"| {i} | **{fmt_precio(o.precio_comparable, o.moneda_comparable)}** "
            f"| {'+'.join(o.aerolineas)} | {o.escalas_totales} "
            f"| {fmt_duracion(o.duracion_total_min)} | {_etiqueta_equipaje(o)} |"
        )

    out += ["", "## Detalle de las mejores opciones", ""]
    for i, o in enumerate(ofertas[:min(top, 5)], start=1):
        out.append(f"### {i}. {fmt_precio(o.precio_comparable, o.moneda_comparable)} — {'+'.join(o.aerolineas)}")
        out.append("")
        out.append(f"- **Ida:** {describir_itinerario(o.ida)}")
        if o.vuelta:
            out.append(f"- **Vuelta:** {describir_itinerario(o.vuelta)}")
        if o.motivos:
            out.append(f"- {' '.join(o.motivos)}")
        if o.url_reserva:
            out.append(f"- [Reservar]({o.url_reserva})")
        out.append("")
    return "\n".join(out)
