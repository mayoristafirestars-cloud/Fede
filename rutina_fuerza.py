#!/usr/bin/env python3
"""Bloque de FUERZA de Fede — 4 días, 8 semanas, con pesos proyectados.

Fuente única de verdad: de acá salen el PDF, `salud/rutina-actual.md` y los
recordatorios del bot de Telegram (con el peso que toca cada semana).

Sin dependencias externas: el bot lo importa tal cual.
"""
from datetime import date, timedelta

INICIO = date(2026, 9, 29)          # lunes de la semana 1
N_SEMANAS = 8

# ─────────────────────── Esquemas por semana ───────────────────────
# Doble progresión: primero suben las reps, después el peso.
# Semana 4 = descarga. Semana 8 = test (1 serie a máximas reps dejando 1).

# (series×reps, RIR)
ESQ_PRINCIPAL = {
    1: ("4×8-10", "3"),      # calibración
    2: ("4×10", "2"),
    3: ("4×8", "2"),
    4: ("3×8", "4"),         # descarga
    5: ("4×10", "2"),
    6: ("4×6-8", "1-2"),
    7: ("4×8", "1-2"),
    8: ("1×máx + 2×6", "1"),  # test
}
PASOS_PRINCIPAL = [0, 0, 1, 0, 1, 2, 2, 2]

ESQ_ACCESORIO = {
    1: ("3×10-12", "2-3"),
    2: ("3×12", "2"),
    3: ("3×10", "2"),
    4: ("2×10", "4"),
    5: ("3×12", "2"),
    6: ("3×10", "1-2"),
    7: ("3×12", "1-2"),
    8: ("3×10", "2"),
}
PASOS_ACCESORIO = [0, 0, 1, 0, 1, 1, 2, 2]

ESQ_CARRY = {
    1: ("3×30 m", "2"), 2: ("3×35 m", "2"), 3: ("3×30 m", "2"), 4: ("2×30 m", "3"),
    5: ("3×35 m", "2"), 6: ("3×30 m", "2"), 7: ("3×35 m", "2"), 8: ("3×40 m", "2"),
}
PASOS_CARRY = [0, 0, 1, 0, 1, 2, 2, 2]

ESQ_SWING = {
    1: "4×12", 2: "4×12", 3: "5×12", 4: "3×10",
    5: "4×12", 6: "5×12", 7: "5×12", 8: "4×12",
}
KG_SWING = [16, 16, 16, 12, 20, 20, 20, 20]

# tipo: P = principal · A = accesorio · C = carry · KB = swing · BW = peso corporal
# (nombre, tipo, base_kg, incremento, unidad, descanso, nota, calibrar)
DIAS = {
    0: {
        "dia": "LUNES", "hora": "07:00", "sesion": "Torso A · Empuje",
        "ejercicios": [
            ("Press banca con mancuernas", "P", 20, 2.5, "c/u", "150 s",
             "Exhalá al subir, bajá en 2 s. Codos a 45°.", False),
            ("Remo con mancuerna a un brazo", "P", 20, 2.5, "", "120 s",
             "Tirá con el codo hacia la cadera, tronco quieto.", False),
            ("Press militar sentado con mancuernas", "A", 12.5, 2.5, "c/u", "90 s",
             "Espalda apoyada, sin arquear la lumbar.", True),
            ("Jalón al pecho agarre neutro", "A", 40, 5, "", "90 s",
             "Pecho arriba, bajá la barra al esternón.", False),
            ("Farmer walk", "C", 22.5, 2.5, "c/u", "90 s",
             "Hombros atrás y abajo, pasos cortos.", True),
            ("Plancha", "BW", None, None, "", "45 s",
             "3 × máximo sostenible (objetivo 45 s). Respirá, no aguantes el aire.", False),
        ],
    },
    1: {
        "dia": "MARTES", "hora": "07:00", "sesion": "Pierna A · Sentadilla",
        "ejercicios": [
            ("Goblet squat", "P", 22.5, 2.5, "", "150 s",
             "Talones al piso, bajá 3 s, rodillas siguen la punta del pie.", True),
            ("Peso muerto rumano con barra", "P", 70, 5, "", "150 s",
             "Cadera atrás, barra pegada a las piernas, espalda neutra.", False),
            ("Sentadilla búlgara con mancuernas", "A", 15, 2.5, "c/u", "90 s",
             "Las reps son por pierna. Torso levemente inclinado.", False),
            ("Prensa 45°", "A", 100, 10, "", "90 s",
             "Exhalá al empujar, no bloquees rodillas arriba. No aguantes el aire.", True),
            ("Dead bug", "BW", None, None, "", "45 s",
             "3 × 10 por lado, lumbar pegada al piso.", False),
        ],
    },
    3: {
        "dia": "JUEVES", "hora": "07:00", "sesion": "Torso B · Tracción",
        "ejercicios": [
            ("Jalón al pecho", "P", 45, 5, "", "150 s",
             "Principal de tracción. Bajá en 2 s.", False),
            ("Press inclinado con mancuernas 30°", "P", 20, 2.5, "c/u", "150 s",
             "Exhalá al subir, omóplatos juntos.", False),
            ("Remo en polea sentado", "A", 40, 5, "", "90 s",
             "Apretá omóplatos al final, sin balancearte.", True),
            ("Flexiones de brazos", "BW", None, None, "", "75 s",
             "3 × máximo dejando 2 en reserva. Si salen más de 20, elevá los pies.", False),
            ("Suitcase carry (una mano)", "C", 20, 2.5, "", "90 s",
             "La distancia es por lado. No te inclines hacia el peso.", True),
            ("Pallof press", "BW", None, None, "", "60 s",
             "3 × 10 por lado, resistí la rotación.", False),
        ],
    },
    4: {
        "dia": "VIERNES", "hora": "13:30", "sesion": "Pierna B · Bisagra",
        "ejercicios": [
            ("Peso muerto con trap bar", "P", 80, 10, "", "180 s",
             "Exhalá al subir. Nada de aguantar el aire a fondo.", True),
            ("Hip thrust con barra", "P", 80, 10, "", "120 s",
             "Pausa 1 s arriba apretando glúteo, mentón al pecho.", False),
            ("Zancada caminando con mancuernas", "A", 12.5, 2.5, "c/u", "90 s",
             "Las reps son pasos por pierna.", True),
            ("Kettlebell swing", "KB", None, None, "", "90-120 s",
             "Explosivo con la cadera, no con los brazos. Series cortas.", False),
            ("Farmer walk pesado", "C", 27.5, 2.5, "c/u", "120 s",
             "El carry más pesado de la semana.", True),
        ],
    },
}

REGLAS = [
    "Calentamiento de 8 min siempre (bici suave + movilidad + 2 series livianas del primer ejercicio).",
    "Exhalá en el esfuerzo. Nunca aguantes el aire a fondo (sube mucho la presión).",
    "Mínimo 1 repetición en reserva: nada de fallo hasta tener el ECG.",
    "Descansá lo indicado; empezá la serie siguiente cuando puedas hablar normal.",
    "Si no te salen las reps con el peso proyectado: repetí ese peso la semana siguiente.",
    "Si en la semana 1 el peso te queda muy liviano (sobran más de 4 reps): subí un escalón y corré toda la proyección.",
    "Si dormiste menos de 5 h: sacá 1 serie de cada principal y no subas peso esa sesión.",
    "Dolor en el pecho, mareo, falta de aire rara o palpitaciones: cortás la sesión.",
    "Miércoles, sábado y domingo: bici zona 2, 40 min (FC 105-118).",
]


# ─────────────────────── Cálculos ───────────────────────

def fecha_semana(n: int) -> date:
    return INICIO + timedelta(weeks=n - 1)


def semana_de(fecha: date) -> int:
    """Semana del bloque (1..8) para una fecha. Antes del inicio → 1, después → 8."""
    n = (fecha - INICIO).days // 7 + 1
    return max(1, min(N_SEMANAS, n))


def kg(ej: tuple, n: int) -> float | None:
    nombre, tipo, base, inc, *_ = ej
    if tipo == "KB":
        return KG_SWING[n - 1]
    if base is None:
        return None
    pasos = {"P": PASOS_PRINCIPAL, "A": PASOS_ACCESORIO, "C": PASOS_CARRY}[tipo]
    return base + inc * pasos[n - 1]


def esquema(ej: tuple, n: int) -> tuple[str, str]:
    tipo = ej[1]
    if tipo == "P":
        return ESQ_PRINCIPAL[n]
    if tipo == "A":
        return ESQ_ACCESORIO[n]
    if tipo == "C":
        return ESQ_CARRY[n]
    if tipo == "KB":
        return ESQ_SWING[n], "2-3"
    return "3×", "2"


def fmt_kg(v: float | None) -> str:
    if v is None:
        return "—"
    s = f"{v:.1f}".rstrip("0").rstrip(".")
    return s.replace(".", ",")


def linea(ej: tuple, n: int) -> str:
    nombre, tipo, base, inc, unidad, descanso, nota, _ = ej
    if tipo == "BW":
        return f"{nombre} — {nota}"
    sr, rir = esquema(ej, n)
    peso = f"{fmt_kg(kg(ej, n))} kg{(' ' + unidad) if unidad else ''}"
    return f"{nombre} — {peso} · {sr} · RIR {rir} · {descanso}"


def tipo_semana(n: int) -> str:
    return {4: "DESCARGA", 8: "TEST"}.get(n, "CARGA")


def mensaje_sesion(dia_idx: int, fecha: date | None = None) -> str:
    """Texto del recordatorio del bot con los pesos de la semana que corresponde."""
    info = DIAS[dia_idx]
    fecha = fecha or date.today()
    n = semana_de(fecha)
    t = tipo_semana(n)
    cab = f"🏋️ {info['sesion']} en 30 min — semana {n}/8"
    if t != "CARGA":
        cab += f" ({t})"
    lineas = [cab, ""]
    for i, ej in enumerate(info["ejercicios"], 1):
        lineas.append(f"{i}. {linea(ej, n)}")
    lineas.append("")
    if n == 1:
        lineas.append("📏 Semana de calibración: si sobran más de 4 reps, subí un escalón.")
    if n == 8:
        lineas.append("🏁 Test: 1 serie a máximas reps dejando 1, anotalo con /nota.")
    if fecha > fecha_semana(N_SEMANAS) + timedelta(days=6):
        lineas.append("✅ Bloque terminado — pedí el siguiente.")
    lineas.append("Exhalá en el esfuerzo · RIR mínimo 1 · Dormiste <5 h: −1 serie")
    return "\n".join(lineas)


def tabla_markdown(dia_idx: int) -> str:
    """Tabla del día con el peso de cada semana."""
    info = DIAS[dia_idx]
    cols = " | ".join(f"S{n}" for n in range(1, N_SEMANAS + 1))
    out = [f"| Ejercicio | {cols} | Descanso |", "|---|" + "---|" * N_SEMANAS + "---|"]
    for ej in info["ejercicios"]:
        nombre, tipo, base, inc, unidad, descanso, nota, calibrar = ej
        if tipo == "BW":
            out.append(f"| {nombre} | " + " | ".join(["—"] * N_SEMANAS) + f" | {descanso} |")
            continue
        celdas = [fmt_kg(kg(ej, n)) for n in range(1, N_SEMANAS + 1)]
        etiqueta = nombre + (f" (kg {unidad})" if unidad else " (kg)") + (" ⚠ calibrar" if calibrar else "")
        out.append(f"| {etiqueta} | " + " | ".join(celdas) + f" | {descanso} |")
    return "\n".join(out)


if __name__ == "__main__":
    for d in DIAS:
        print(mensaje_sesion(d, INICIO + timedelta(days=d)))
        print("-" * 40)
