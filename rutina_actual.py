#!/usr/bin/env python3
"""Rutina dura de 6 días (8 semanas) — mensajes del bot con los kilos de la semana.

Fuente: rutina_actual.json, el mismo plan del PDF Plan-Fede-Rutina-6-dias-DURA.pdf
(lo arma el entrenador en salud/rutina-actual.md). Va en la misma carpeta que el bot.

Kilo de cada ejercicio con carga = máximo estimado (peso × (1 + reps/30)) × factor × % de la
semana, redondeado a 2,5 kg (mancuernas: 2 kg por mano). Sin dependencias externas.
"""
import json
from datetime import date, timedelta
from pathlib import Path

INICIO = date(2026, 11, 16)          # lunes de la semana 1
PLAN = json.loads((Path(__file__).resolve().parent / "rutina_actual.json").read_text(encoding="utf-8"))
N_SEMANAS = PLAN["semanas"]
NOMBRES_DIA = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]


def _maximo(par):
    if not par:
        return None
    kg, reps = par
    return kg * (1 + min(max(reps or 1, 1), 10) / 30)


_M = PLAN.get("marcas", {})
MAXIMOS = {k: _maximo(_M.get(k)) for k in ("sq", "bp", "dl", "ohp")}
if not MAXIMOS["dl"] and MAXIMOS["sq"]:
    MAXIMOS["dl"] = MAXIMOS["sq"] * 1.1
if not MAXIMOS["ohp"] and MAXIMOS["bp"]:
    MAXIMOS["ohp"] = MAXIMOS["bp"] * 0.62


def activo(fecha: date) -> bool:
    return fecha >= INICIO


def semana_de(fecha: date) -> int:
    return max(1, min(N_SEMANAS, (fecha - INICIO).days // 7 + 1))


def es_descarga(n: int) -> bool:
    return n % 4 == 0


def dia_del_plan(dia_idx: int):
    nombre = NOMBRES_DIA[dia_idx]
    return next((d for d in PLAN["dias"] if d["dia"] == nombre), None)


def _fmt(kg: float) -> str:
    return f"{kg:g}".replace(".", ",")


def linea(ej: dict, n: int) -> str:
    s = str(n)
    if ej.get("tipo") == "carga":
        series, reps, pct = PLAN["esquemas"][ej["esquema"]][s]
        if pct is None:
            return f"{ej['nombre']}: {series}×{reps} · {ej.get('nota', 'test')}"
        kg = (MAXIMOS[ej["base"]] or 0) * ej.get("factor", 1) * pct
        if ej.get("mancuerna"):
            peso = f"{_fmt(max(2, round(kg / 2 / 2) * 2))} kg c/u"
        else:
            peso = f"{_fmt(round(kg / 2.5) * 2.5)} kg"
        desc = f" · desc {ej['descanso']}" if ej.get("descanso") else ""
        return f"{ej['nombre']}: {peso} · {series}×{reps}{desc}"
    return f"{ej['nombre']}: {ej.get('fijo', {}).get(s, '')}"


def _items(lista) -> str:
    return " · ".join(f"{a} ({b})" for a, b in lista)


def mensaje_sesion(dia_idx: int, fecha: date | None = None) -> str | None:
    """Texto del recordatorio de gym del día, o None si ese día no hay sesión."""
    fecha = fecha or date.today()
    d = dia_del_plan(dia_idx)
    if not d:
        return None
    n = semana_de(fecha)
    cab = f"🏋️ {d['nombre']} empieza en 30 min — semana {n}/{N_SEMANAS}"
    if es_descarga(n):
        cab += " (DESCARGA)"
    out = [cab, ""]
    out.append(f"🔥 Calentamiento: {_items(d.get('calentamiento', []))}")
    out.append(f"🤸 Movilidad: {_items(d.get('movilidad', []))}")
    out.append(f"⚡ Activación: {_items(d.get('activacion', []))}")
    out.append("")
    for i, ej in enumerate(d["ejercicios"], 1):
        out.append(f"{i}. {linea(ej, n)}")
    final = d.get("final", {}).get(str(n))
    if final:
        out += ["", f"🏁 Final: {final}"]
    out += ["", f"🧘 Vuelta a la calma: {_items(d.get('calma', []))}", ""]
    if n == 1:
        out.append("📏 Calibración: si el básico sale con más de 3 en reserva, subí 2,5-5 kg y avisá con /nota.")
    if n >= 3 and not es_descarga(n):
        out.append("⚠️ Sin ECG + tensión registrada, no pases de la semana 3: repetí los kilos de la S3.")
    if fecha > INICIO + timedelta(weeks=N_SEMANAS) - timedelta(days=1):
        out.append("✅ Bloque terminado — pedí el siguiente.")
    out.append("FC ≤121 (picos ≤131) · RIR ≥1 en básicos · Si dormiste <5 h: sacá back-off y técnicas")
    return "\n".join(out)


if __name__ == "__main__":
    hoy = date.today()
    for i in range(7):
        m = mensaje_sesion(i, max(hoy, INICIO) + timedelta(days=(i - max(hoy, INICIO).weekday()) % 7))
        print(f"===== {NOMBRES_DIA[i]} =====\n{m}\n")
