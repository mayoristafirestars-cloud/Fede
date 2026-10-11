#!/usr/bin/env python3
"""Genera Plan-Fede-Recordatorios.ics para importar a Calendar del iPhone.
Todos los eventos son recurrentes semanales con alarma a la hora exacta."""

from pathlib import Path

OUT = Path("/home/user/Fede/Plan-Fede-Recordatorios.ics")

# Dia base para arrancar (proximo lunes tipo). La recurrencia semanal se
# repite indefinidamente.
BASE_DATES = {
    "MO": "20260105",
    "TU": "20260106",
    "WE": "20260107",
    "TH": "20260108",
    "FR": "20260109",
    "SA": "20260110",
    "SU": "20260111",
}

TZ = "America/Argentina/Buenos_Aires"

# Cada evento: (dia_semana, hora HHMM, resumen corto, descripcion larga)
EVENTS = [
    # ---- LUNES (gym A) ----
    ("MO", "0530", "💧 Despertar (agua + sal)",       "Vaso 300 ml agua + pizca de sal."),
    ("MO", "0600", "🍌 Pre-entreno en 30 min",         "Media banana (80 g) + café negro 150 ml + agua con sal 300 ml."),
    ("MO", "0730", "🥤 Post-entreno en 30 min",        "Whey 35 g + agua 300 ml."),
    ("MO", "0900", "🍳 Desayuno en 30 min",             "4 huevos duros + palta 90 g + tomate 100 g + queso port salut 20 g + oliva 5 ml."),
    ("MO", "0915", "💊 Suplementos AM",                 "Vitamina D3 + Omega-3."),
    ("MO", "1230", "🍽️ Almuerzo en 30 min",            "Pollo 220 g + papa hervida 100 g + ensalada (lechuga + rucula + tomate + pepino + palta + aceitunas) + oliva 12 ml + limón."),
    ("MO", "1330", "☕ Último mate/café del día",       "Después solo agua o infusiones sin cafeína."),
    ("MO", "1600", "🥛 Merienda en 30 min",             "Yogur griego 170 g + nueces 12 g + canela."),
    ("MO", "1830", "🐟 Cena en 30 min",                 "Merluza 200 g + zapallito 150 g + morrón 70 g + anchoas 20 g + huevo duro + oliva 12 ml."),
    ("MO", "2130", "🌙 Snack ancla + magnesio",         "Yogur griego 170 g + chía 10 g + magnesio 300 mg. Bajá luces."),
    ("MO", "2200", "😴 A dormir en 30 min",             "Celular afuera del cuarto."),

    # ---- MARTES (gym B) ----
    ("TU", "0530", "💧 Despertar (agua + sal)",         "Vaso 300 ml + pizca de sal."),
    ("TU", "0600", "🍇 Pre-entreno en 30 min",          "Pasas de uva 30 g + café 150 ml + agua con sal 300 ml."),
    ("TU", "0730", "🥤 Post-entreno en 30 min",         "Whey 35 g + agua 300 ml."),
    ("TU", "0900", "🍳 Desayuno en 30 min",             "4 huevos duros + queso port salut 30 g + palta 80 g + tomate 100 g + oliva 5 ml."),
    ("TU", "0915", "💊 Suplementos AM",                 "Vit D3 + Omega-3."),
    ("TU", "1230", "🍽️ Almuerzo en 30 min",            "Pollo 220 g + boniato hervido 100 g + ensalada + oliva 12 ml."),
    ("TU", "1330", "☕ Último mate del día",             "Después solo agua o infusiones sin cafeína."),
    ("TU", "1600", "🥛 Merienda en 30 min",             "Cottage 200 g + frutillas 30 g + canela."),
    ("TU", "1830", "🐟 Cena en 30 min",                 "Salmón 180 g + espinaca salteada 150 g + champignones 80 g + oliva 12 ml."),
    ("TU", "2130", "🌙 Snack ancla + magnesio",         "Yogur griego 170 g + chía 10 g + magnesio 300 mg."),
    ("TU", "2200", "😴 A dormir",                        "Celular afuera del cuarto."),

    # ---- MIERCOLES (descanso + bici) ----
    ("WE", "0530", "💧 Despertar (agua)",               "Vaso 300 ml de agua (sin sal, no entrenás)."),
    ("WE", "0600", "🍳 Desayuno en 30 min",             "3 huevos duros + ricota 80 g + palta 60 g + tomate 100 g + oliva 5 ml. Sin pan."),
    ("WE", "0615", "💊 Suplementos AM",                 "Vit D3 + Omega-3 + Creatina 5 g."),
    ("WE", "0930", "🥛 Media mañana en 30 min",         "Yogur griego 200 g + nueces 10 g + arándanos 20 g."),
    ("WE", "1230", "🍽️ Almuerzo en 30 min",            "Atún 180 g + 2 huevos duros + espinaca 150 g + queso 30 g + ensalada + palta 60 g + oliva 15 ml."),
    ("WE", "1300", "🚴 Bici 40 min en 30 min",          "Zona 2 (FC 105-118 lpm), ruta plana, post-almuerzo."),
    ("WE", "1330", "☕ Último mate del día",             "Después solo agua o infusiones sin cafeína."),
    ("WE", "1600", "🥛 Merienda en 30 min",             "Ricota 150 g + almendras 10 g + cacao amargo 3 g."),
    ("WE", "1630", "⭐ Momento hobby (30-45 min)",       "Pescar, cocinar, huerta, música... lo que te guste."),
    ("WE", "1830", "🐟 Cena SARDINAS en 30 min",        "Sardinas 120 g + tomate 100 g + palta 60 g + aceitunas 15 g + oliva + limón."),
    ("WE", "2130", "🌙 Snack ancla + magnesio",         "Yogur griego 170 g + chía 10 g + magnesio 300 mg."),
    ("WE", "2200", "😴 A dormir",                        "Celular afuera del cuarto."),

    # ---- JUEVES (gym A) ----
    ("TH", "0530", "💧 Despertar (agua + sal)",         "Agua + sal."),
    ("TH", "0600", "🍌 Pre-entreno en 30 min",          "Media banana 80 g + café + agua con sal."),
    ("TH", "0730", "🥤 Post-entreno en 30 min",         "Whey 35 g + agua."),
    ("TH", "0900", "🍳 Desayuno diferente en 30 min",   "Yogur griego 200 g + frutillas 100 g + almendras 15 g + canela + 3 huevos duros aparte."),
    ("TH", "0915", "💊 Suplementos AM",                 "Vit D3 + Omega-3."),
    ("TH", "1230", "🍽️ Almuerzo en 30 min",            "Pollo 200 g + papa hervida 100 g + huevo duro + ensalada nicoise + palta 50 g + oliva 12 ml."),
    ("TH", "1330", "☕ Último mate",                     "Después solo agua o infusiones sin cafeína."),
    ("TH", "1600", "🥛 Merienda en 30 min",             "Yogur griego 170 g + nueces 12 g + frutos rojos 20 g."),
    ("TH", "1830", "🐟 Cena en 30 min",                 "Brótola 200 g + brócoli al vapor 200 g + huevo duro + anchoas 20 g + oliva 12 ml."),
    ("TH", "2130", "🌙 Snack ancla + magnesio",         "Yogur 170 g + chía 10 g + magnesio 300 mg."),
    ("TH", "2200", "😴 A dormir",                        "Celular afuera."),

    # ---- VIERNES (gym 14:00, cena LIBRE) ----
    ("FR", "0530", "💧 Despertar (agua 400 ml)",         "Agua 400 ml."),
    ("FR", "0600", "🍳 Desayuno en 30 min",              "4 huevos duros + queso 30 g + palta 80 g + tomate 100 g + oliva 5 ml."),
    ("FR", "0615", "💊 Suplementos AM",                  "Vit D3 + Omega-3."),
    ("FR", "1000", "🥛 Media mañana en 30 min",          "Yogur griego 150 g + nueces 10 g + frutillas 30 g."),
    ("FR", "1200", "🍇 Pre-entreno LIVIANO en 30 min",   "Pasas 30 g + café + agua con sal 400 ml. NO comer sólido pesado 11-14 h."),
    ("FR", "1330", "🏋️ Gym en 30 min",                   "Complex B: sent. trasera → remo supino → high pull → RDL → shrug."),
    ("FR", "1445", "🥤 Post-entreno en 30 min",          "Whey 35 g + agua."),
    ("FR", "1530", "🍽️ Almuerzo-merienda en 30 min",    "Pollo 220 g + papa hervida 150 g + espinaca + rucula + tomate cherry + palta 70 g + almendras + oliva."),
    ("FR", "1830", "🎉 CENA LIBRE en 30 min",             "Elegí UNA: pizza 2 porciones / parrilla 250 g magra / sushi 12-15 piezas / pasta 300 g. Máx 1 vino tinto."),
    ("FR", "2200", "😴 A dormir",                         "Celular afuera."),

    # ---- SABADO (descanso + bici) ----
    ("SA", "0530", "💧 Despertar (agua)",                "Vaso 300 ml."),
    ("SA", "0600", "🍳 Desayuno en 30 min",              "3 huevos duros + jamón cocido magro 30 g + queso port salut 30 g + palta 50 g + tomate 100 g + oliva 5 ml."),
    ("SA", "0615", "💊 Suplementos AM",                  "Vit D3 + Omega-3 + Creatina 5 g."),
    ("SA", "0930", "🥛 Media mañana en 30 min",          "Cottage 150 g + frutillas 50 g + nueces 7 g."),
    ("SA", "1230", "🍽️ Almuerzo en 30 min",             "Pollo 220 g + brócoli 150 g + zapallitos hervidos 100 g + ensalada + palta 40 g + oliva 12 ml."),
    ("SA", "1300", "🚴 Bici 40 min en 30 min",           "Zona 2, ruta plana."),
    ("SA", "1330", "☕ Último mate",                      "Después solo agua o infusiones."),
    ("SA", "1600", "🐟 Merienda SARDINAS en 30 min",     "Sardinas 100 g + palta 50 g + tomate cherry 80 g + galleta de arroz 1."),
    ("SA", "1630", "⭐ Hobby / familia",                  "30-45 min."),
    ("SA", "1830", "🍽️ Cena en 30 min",                  "Pollo 180 g + 2 huevos duros + queso 25 g + espinaca al vapor 150 g + champignones + anchoas 15 g + oliva."),
    ("SA", "2130", "🌙 Snack ancla + magnesio",          "Yogur 170 g + chía 10 g + magnesio 300 mg."),
    ("SA", "2200", "😴 A dormir",                         ""),

    # ---- DOMINGO (descanso + bici + batch cooking) ----
    ("SU", "0530", "💧 Despertar (agua)",                "Vaso 300 ml."),
    ("SU", "0600", "🍳 Desayuno en 30 min",              "3 huevos duros + palta 60 g + tomate 100 g + queso 30 g + oliva 5 ml."),
    ("SU", "0615", "💊 Suplementos AM",                  "Vit D3 + Omega-3 + Creatina 5 g."),
    ("SU", "0930", "🍳 BATCH COOKING en 30 min (90 min)","Pollo 1,8 kg al horno + 20 huevos duros + papa/boniato hervidos + verduras al vapor + aderezos."),
    ("SU", "1300", "🚴 Bici 40 min en 30 min",           "Zona 2, al sol."),
    ("SU", "1300", "🍽️ Almuerzo en 30 min",             "Pollo del horno 220 g + ensalada completa + palta 60 g + aceitunas + nueces + oliva."),
    ("SU", "1330", "☕ Último mate",                      ""),
    ("SU", "1600", "🥛 Merienda en 30 min",              "Yogur griego 200 g + nueces 10 g + cacao amargo 3 g."),
    ("SU", "1630", "⭐ Hobby / hijos",                    "Ideal aire libre."),
    ("SU", "1830", "🍽️ Cena Caesar en 30 min",           "Pollo 180 g + lechuga romana + huevo duro + anchoas 20 g + parmesano 15 g + aderezo (oliva + limón + ajo + yema)."),
    ("SU", "2130", "🌙 Snack ancla + magnesio",          "Yogur 170 g + chía 10 g + magnesio 300 mg."),
    ("SU", "2200", "😴 A dormir",                         "Cargar tensiómetro para lunes."),
]


def escape(s: str) -> str:
    """Escape para valores iCal."""
    return s.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", "\\n")


DTSTAMP_FIXED = "20260101T000000Z"


def make_event(idx: int, dia: str, hora: str, summary: str, description: str) -> str:
    fecha = BASE_DATES[dia]  # YYYYMMDD
    hh, mm = hora[:2], hora[2:]
    end_mm = int(mm) + 15
    end_hh = int(hh)
    if end_mm >= 60:
        end_hh += 1
        end_mm -= 60
    end_hh_s = str(end_hh).zfill(2)
    end_mm_s = str(end_mm).zfill(2)
    # UTC (Argentina = UTC-3, entonces sumamos 3 horas al hora local)
    dtstart_utc_hh = str((int(hh) + 3) % 24).zfill(2)
    dtend_utc_hh = str((end_hh + 3) % 24).zfill(2)
    dtstart = f"{fecha}T{dtstart_utc_hh}{mm}00Z"
    dtend = f"{fecha}T{dtend_utc_hh}{end_mm_s}00Z"
    uid = f"plan-fede-{dia}-{hora}-{idx}@planfede"

    lines = [
        "BEGIN:VEVENT",
        f"UID:{uid}",
        f"DTSTAMP:{DTSTAMP_FIXED}",
        f"DTSTART:{dtstart}",
        f"DTEND:{dtend}",
        f"SUMMARY:{escape(summary)}",
        f"DESCRIPTION:{escape(description)}",
        f"RRULE:FREQ=WEEKLY;BYDAY={dia}",
        "STATUS:CONFIRMED",
        "TRANSP:OPAQUE",
        "SEQUENCE:0",
        "BEGIN:VALARM",
        "ACTION:DISPLAY",
        f"DESCRIPTION:{escape(summary)}",
        "TRIGGER:-PT0M",
        "END:VALARM",
        "END:VEVENT",
    ]
    return "\r\n".join(lines)


def main():
    parts = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Plan Fede//ES",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        "X-WR-CALNAME:Plan Fede",
        "X-WR-TIMEZONE:America/Argentina/Buenos_Aires",
    ]

    for i, (dia, hora, summary, desc) in enumerate(EVENTS):
        parts.append(make_event(i, dia, hora, summary, desc))

    parts.append("END:VCALENDAR")

    # Line endings CRLF (RFC 5545)
    content = "\r\n".join(parts) + "\r\n"
    OUT.write_text(content, encoding="utf-8")
    print(f"Archivo generado: {OUT}")
    print(f"Eventos: {len(EVENTS)}")
    print(f"Tamaño: {OUT.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    main()
