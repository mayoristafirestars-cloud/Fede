#!/usr/bin/env python3
"""Dieta actual → recordatorios de comidas del bot.

Fuente: dieta_actual.json, el mismo plan del PDF de la dieta (lo arma el nutricionista en
salud/dieta-actual.md). Va en la misma carpeta que el bot. Cada comida se avisa 30 min antes,
con sus gramos, kcal y proteína (lo que suma al tocar "Hecho"). Sin dependencias externas.
"""
import json
from datetime import datetime, timedelta
from pathlib import Path

DIETA = json.loads((Path(__file__).resolve().parent / "dieta_actual.json").read_text(encoding="utf-8"))
NOMBRES_DIA = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
AVISO_MIN = 30

OBJETIVO_KCAL = round(DIETA["objetivos"]["kcal_entreno"])
OBJETIVO_KCAL_DESCANSO = round(DIETA["objetivos"]["kcal_descanso"])
OBJETIVO_PROT = round(DIETA["objetivos"]["proteina_g"])


def _menos(hora: str, minutos: int) -> str:
    t = datetime.strptime(hora.strip()[:5], "%H:%M") - timedelta(minutes=minutos)
    return t.strftime("%H:%M")


def _icono(nombre: str) -> str:
    n = nombre.lower()
    if "pre" in n and ("entreno" in n or "bici" in n):
        return "🍌"
    if "post" in n or "shake" in n or "batido" in n:
        return "🥤"
    if "desayuno" in n:
        return "🍳"
    if "cena" in n:
        return "🍽️"
    if "snack" in n or "noche" in n:
        return "🌙"
    return "🍽️"


def mensaje_comida(c: dict) -> str:
    items = "\n".join(f"• {a} {b}".rstrip() for a, b in c.get("items", []))
    nota = f"\n{c['nota']}" if c.get("nota") else ""
    return f"{_icono(c['nombre'])} {c['nombre']} en {AVISO_MIN} min ({c['hora']}):\n{items}{nota}\n≈ {round(c.get('kcal', 0))} kcal · {round(c.get('prot', 0))} g proteína"


def es_comida(c: dict) -> bool:
    """Comidas con algo para comer (no 'Entrenamiento' ni 'Bici' que vengan como fila)."""
    return bool(c.get("kcal")) or bool(c.get("prot"))


def recordatorios():
    """[(dia_idx, 'HH:MM', mensaje, kcal, prot, quema)] de las comidas de la semana."""
    out = []
    for d in DIETA["dias"]:
        idx = NOMBRES_DIA.index(d["dia"])
        for c in d["comidas"]:
            if es_comida(c):
                out.append((idx, _menos(c["hora"], AVISO_MIN), mensaje_comida(c),
                            round(c.get("kcal", 0)), round(c.get("prot", 0)), 0))
    return out


def tipo_dia(idx: int) -> str:
    return next((d["tipo"] for d in DIETA["dias"] if d["dia"] == NOMBRES_DIA[idx]), "")


if __name__ == "__main__":
    for r in recordatorios():
        print(r[0], r[1], r[3], r[4], r[2].splitlines()[0])
