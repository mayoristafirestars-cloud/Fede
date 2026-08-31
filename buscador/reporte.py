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
            f"{resumen_busqueda.get('combinaciones', 0)} combinaciones consultadas · "
            f"{resumen_busqueda.get('ofertas_crudas', 0)} ofertas · "
            f"proveedores: {', '.join(resumen_busqueda.get('proveedores', [])) or '—'}",
            "tenue", color))
    lineas.append("─" * 78)

    mas_barata = min(ofertas, key=lambda o: o.precio_comparable)
    for i, o in enumerate(ofertas[:top], start=1):
        marca = ""
        if o is ofertas[0]:
            marca = _c(" ★ MEJOR OPCIÓN", "verde", color)
        if o is mas_barata:
            marca += _c(" 💲 MÁS BARATO", "amarillo", color)

        precio = fmt_precio(o.precio_comparable, o.moneda_comparable)
        lineas.append("")
        lineas.append(f"{i:>2}. {_c(precio, 'negrita', color)}"
                      f"  {_c('·', 'tenue', color)} {'+'.join(o.aerolineas)}"
                      f"{marca}")
        lineas.append(f"    IDA    {describir_itinerario(o.ida)}")
        if o.vuelta:
            lineas.append(f"    VUELTA {describir_itinerario(o.vuelta)}")

        extras = [_etiqueta_equipaje(o)]
        if o.asientos_restantes is not None and o.asientos_restantes <= 3:
            extras.append(f"¡quedan {o.asientos_restantes}!")
        if o.self_transfer:
            extras.append("⚠ tramos separados (sin protección de conexión)")
        if o.precio_ars_final and o.moneda != "ARS":
            extras.append(f"≈ {fmt_precio(o.precio_ars_final, 'ARS')} finales")
        lineas.append(_c("    " + "  ·  ".join(extras), "tenue", color))

        if o.motivos:
            lineas.append(_c("    " + " ".join(o.motivos), "cyan", color))

    lineas.append("")
    lineas.append("─" * 78)
    lineas.append(_c(
        f"Precios verificados al {datetime.now():%d/%m/%Y %H:%M}. "
        "La tarifa se confirma recién al pagar en el sitio de la aerolínea.",
        "tenue", color))
    return "\n".join(lineas)


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
