#!/usr/bin/env python3
"""Bloque de FUERZA CON BARRA de Fede — 4 días, 8 semanas, pesos proyectados.

Fuente única de verdad: de acá salen el PDF, `salud/rutina-actual.md` y los
recordatorios del bot de Telegram (con el peso que toca cada semana).

Los 4 básicos (sentadilla, banca, peso muerto, militar) se programan como
% de un Training Max (TM ≈ 90 % del 1RM estimado). Si en la semana 1 el
peso queda liviano, se cambia el TM acá arriba y se recalcula todo.

Sin dependencias externas: el bot lo importa tal cual.
"""
from datetime import date, timedelta

INICIO = date(2026, 9, 29)          # lunes de la semana 1
N_SEMANAS = 8

# ─────────────── Training Max de los básicos (kg) ───────────────
# Estimados desde los pesos con mancuerna/rumano/hip thrust del 25/09.
# (TM semanas 1-4, suba de TM para semanas 5-8)
TM = {
    "banca":      (60.0, 2.5),  # 1RM est. ~66 kg (mancuernas 20 c/u × 10 → barra ×1,15)
    "sentadilla": (80.0, 5.0),  # 1RM est. ~90 kg (≈ 80 % del peso muerto)
    "muerto":     (100.0, 5.0), # 1RM est. ~110 kg (rumano 70 × 8-10 → ×1,25)
    "militar":    (37.5, 2.5),  # 1RM est. ~42 kg (≈ 62 % de la banca)
}

# ─────────────── Esquema de los básicos (% del TM) ───────────────
# Lista de (porcentaje, series×reps). La primera es la serie más pesada.
ESQ_BASICO = {
    1: [(0.75, "5×5")],
    2: [(0.80, "5×5")],
    3: [(0.875, "1×3"), (0.775, "4×5")],
    4: [(0.65, "3×5")],                        # descarga
    5: [(0.825, "5×5")],
    6: [(0.90, "1×3"), (0.80, "4×4")],
    7: [(0.95, "1×2"), (0.85, "3×3")],
    8: [(1.00, "1×máx dejando 1"), (0.80, "3×3")],  # test
}
RIR_BASICO = {1: "2-3", 2: "2", 3: "1-2", 4: "4", 5: "2", 6: "1-2", 7: "1-2", 8: "1"}

# ─────────────── Secundarios con barra (progresión lineal) ───────────────
ESQ_SECUNDARIO = {
    1: ("4×8", "2-3"), 2: ("4×8", "2"), 3: ("4×6", "2"), 4: ("3×6", "4"),
    5: ("4×6", "2"), 6: ("4×5", "1-2"), 7: ("4×5", "1-2"), 8: ("4×5", "1-2"),
}
PASOS_SECUNDARIO = [0, 1, 2, 0, 2, 3, 4, 4]

# ─────────────── Accesorios y carries ───────────────
ESQ_ACCESORIO = {
    1: ("3×10-12", "2"), 2: ("3×12", "2"), 3: ("3×10", "1-2"), 4: ("2×10", "4"),
    5: ("3×12", "2"), 6: ("3×10", "1-2"), 7: ("3×12", "1-2"), 8: ("3×10", "1-2"),
}
PASOS_ACCESORIO = [0, 0, 1, 0, 1, 1, 2, 2]

ESQ_CARRY = {
    1: ("3×30 m", "2"), 2: ("3×35 m", "2"), 3: ("3×30 m", "2"), 4: ("2×30 m", "3"),
    5: ("3×35 m", "2"), 6: ("3×30 m", "2"), 7: ("3×35 m", "2"), 8: ("3×40 m", "2"),
}
PASOS_CARRY = [0, 0, 1, 0, 1, 2, 2, 2]

# tipo: P = básico con barra (% TM) · S = secundario con barra · A = accesorio
#       C = carry · BW = peso corporal
# (nombre, tipo, base_kg | clave_TM, incremento, unidad, descanso, nota, calibrar)
DIAS = {
    0: {
        "dia": "LUNES", "hora": "07:00", "sesion": "Torso A · Press banca",
        "ejercicios": [
            ("Press banca con barra", "P", "banca", None, "", "3 min",
             "Pies firmes, omóplatos juntos. Bajá al pecho en 2 s, sin rebotar.", False),
            ("Remo con barra", "S", 45, 2.5, "", "2 min",
             "Torso a 45°, tirá la barra al ombligo. Sin tirón con la cadera.", False),
            ("Jalón al pecho", "A", 45, 5, "", "90 s",
             "Pecho arriba, bajá la barra al esternón.", False),
            ("Superserie: Fondos asistidos + Curl con barra", "A", 20, 2.5, "", "90 s",
             "Fondos 3×máx dejando 2 y sin descanso curl con barra (el kg es del curl).", True),
            ("Face pull en polea", "A", 15, 2.5, "", "60 s",
             "Tirá la soga a la frente, codos altos. Salud de hombro.", True),
        ],
    },
    1: {
        "dia": "MARTES", "hora": "07:00", "sesion": "Pierna A · Sentadilla",
        "ejercicios": [
            ("Sentadilla trasera con barra", "P", "sentadilla", None, "", "3 min",
             "Barra sobre trapecio, bajá hasta la paralela como mínimo, rodillas afuera.", False),
            ("Peso muerto rumano con barra", "S", 70, 2.5, "", "2 min",
             "Cadera atrás, barra pegada a las piernas, espalda neutra.", False),
            ("Sentadilla búlgara con mancuernas", "A", 15, 2.5, "c/u", "90 s",
             "Las reps son por pierna.", False),
            ("Curl femoral en máquina", "A", 30, 5, "", "75 s",
             "Subida explosiva, bajada en 3 s.", True),
            ("Rueda abdominal", "BW", None, None, "", "60 s",
             "3 × 8-12. Si no sale desde las rodillas completa, rango corto.", False),
        ],
    },
    3: {
        "dia": "JUEVES", "hora": "07:00", "sesion": "Torso B · Press militar",
        "ejercicios": [
            ("Press militar de pie con barra", "P", "militar", None, "", "3 min",
             "Glúteos y abdomen apretados, barra en línea recta, cabeza pasa adelante al final.", False),
            ("Press inclinado con barra", "S", 35, 2.5, "", "2 min",
             "Banco a 30°, bajá a la clavícula.", False),
            ("Dominadas (asistidas si hace falta)", "BW", None, None, "", "2 min",
             "4 × máximo dejando 1. Cuando salgan 8 limpias, sumá peso con cinturón.", False),
            ("Remo en polea sentado", "A", 45, 5, "", "90 s",
             "Apretá omóplatos al final, sin balancearte.", False),
            ("Superserie: Extensión de tríceps en polea + Curl martillo", "A", 20, 2.5, "", "75 s",
             "Sin descanso entre los dos. Martillo con 10-12,5 kg c/u (el kg es del tríceps).", True),
        ],
    },
    4: {
        "dia": "VIERNES", "hora": "13:30", "sesion": "Pierna B · Peso muerto",
        "ejercicios": [
            ("Peso muerto convencional con barra", "P", "muerto", None, "", "3-4 min",
             "Barra sobre el medio del pie, espalda neutra, empujá el piso. Cada rep desde el piso.", False),
            ("Sentadilla frontal con barra", "S", 40, 2.5, "", "2 min",
             "Codos altos, torso vertical. Si la muñeca molesta, agarre cruzado.", True),
            ("Hip thrust con barra", "S", 80, 5, "", "2 min",
             "Pausa 1 s arriba apretando glúteo.", False),
            ("Zancada caminando con mancuernas", "A", 15, 2.5, "c/u", "90 s",
             "Las reps son pasos por pierna.", True),
            ("Farmer walk pesado", "C", 27.5, 2.5, "c/u", "2 min",
             "El carry más pesado de la semana. Hombros atrás.", True),
        ],
    },
}

REGLAS = [
    "Calentamiento 8 min (bici + movilidad) y aproximación antes del básico: barra sola ×10, 50 % ×5, 70 % ×3, 85 % ×1 del peso del día.",
    "Respiración con barra: tomá aire y apretá el abdomen antes de bajar, soltalo durante la subida. Nunca más de 1 repetición sin respirar.",
    "Mínimo 1 repetición en reserva: nada de fallo hasta tener el ECG. La semana 8 también es dejando 1.",
    "Semana 1 = calibración: si el 5×5 sale sobrado (más de 3 en reserva), subí 5 kg por serie y anotalo con /nota. Se ajusta el TM y se recalcula todo.",
    "Si no te salen las reps del peso proyectado: repetí esa semana antes de seguir.",
    "Sentadilla y banca con barras de seguridad o ayudante. Siempre.",
    "Si dormiste menos de 5 h: hacé el básico solo hasta las series livianas y cortá ahí.",
    "Dolor en el pecho, mareo, falta de aire rara o palpitaciones: cortás la sesión.",
    "Miércoles, sábado y domingo: bici zona 2, 40 min (FC 105-118).",
]


# ─────────────────────── Cálculos ───────────────────────

def redondear(v: float, paso: float = 2.5) -> float:
    return round(v / paso - 1e-9) * paso


def fecha_semana(n: int) -> date:
    return INICIO + timedelta(weeks=n - 1)


def semana_de(fecha: date) -> int:
    """Semana del bloque (1..8) para una fecha. Antes del inicio → 1, después → 8."""
    n = (fecha - INICIO).days // 7 + 1
    return max(1, min(N_SEMANAS, n))


def tm_de(clave: str, n: int) -> float:
    base, suba = TM[clave]
    return base + (suba if n >= 5 else 0)


def series_basico(ej: tuple, n: int) -> list[tuple[float, str]]:
    """[(kg, series×reps), ...] para un básico en la semana n."""
    tm = tm_de(ej[2], n)
    return [(redondear(tm * pct), sr) for pct, sr in ESQ_BASICO[n]]


def kg(ej: tuple, n: int) -> float | None:
    """Peso más pesado del ejercicio en la semana n."""
    tipo = ej[1]
    if tipo == "P":
        return series_basico(ej, n)[0][0]
    if tipo == "BW":
        return None
    base, inc = ej[2], ej[3]
    pasos = {"S": PASOS_SECUNDARIO, "A": PASOS_ACCESORIO, "C": PASOS_CARRY}[tipo]
    return base + inc * pasos[n - 1]


def esquema(ej: tuple, n: int) -> tuple[str, str]:
    tipo = ej[1]
    if tipo == "S":
        return ESQ_SECUNDARIO[n]
    if tipo == "A":
        return ESQ_ACCESORIO[n]
    if tipo == "C":
        return ESQ_CARRY[n]
    return "", "2"


def fmt_kg(v: float | None) -> str:
    if v is None:
        return "—"
    s = f"{v:.1f}".rstrip("0").rstrip(".")
    return s.replace(".", ",")


def detalle_basico(ej: tuple, n: int) -> str:
    """Ej: '1×3 con 47,5 kg + 4×5 con 42,5 kg'."""
    return " + ".join(f"{sr} con {fmt_kg(k)} kg" for k, sr in series_basico(ej, n))


def celda_basico(ej: tuple, n: int) -> str:
    """Para tablas: '47,5/42,5' (serie pesada / series de volumen)."""
    return "/".join(fmt_kg(k) for k, _ in series_basico(ej, n))


def linea(ej: tuple, n: int) -> str:
    nombre, tipo, base, inc, unidad, descanso, nota, _ = ej
    if tipo == "BW":
        return f"{nombre} — {nota.split('.')[0]}"
    if tipo == "P":
        return f"{nombre} — {detalle_basico(ej, n)} · RIR {RIR_BASICO[n]} · {descanso}"
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
        lineas.append("📏 Calibración: si el 5×5 sale sobrado, subí 5 kg y avisá con /nota.")
    if n == 8:
        lineas.append("🏁 Test: serie pesada a máximas reps dejando 1. Anotalo con /nota.")
    if fecha > fecha_semana(N_SEMANAS) + timedelta(days=6):
        lineas.append("✅ Bloque terminado — pedí el siguiente.")
    lineas.append("Aproximación antes del básico · Aire adentro al bajar, afuera al subir · RIR mínimo 1")
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
        if tipo == "P":
            celdas = [celda_basico(ej, n) for n in range(1, N_SEMANAS + 1)]
            etiqueta = f"**{nombre}** (pesada/volumen)"
        else:
            celdas = [fmt_kg(kg(ej, n)) for n in range(1, N_SEMANAS + 1)]
            etiqueta = nombre + (f" (kg {unidad})" if unidad else "") + (" ⚠ calibrar" if calibrar else "")
        out.append(f"| {etiqueta} | " + " | ".join(celdas) + f" | {descanso} |")
    return "\n".join(out)


if __name__ == "__main__":
    for d in DIAS:
        for n in (1, 7):
            print(mensaje_sesion(d, fecha_semana(n) + timedelta(days=d)))
            print("-" * 40)
