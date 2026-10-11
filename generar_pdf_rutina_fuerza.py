#!/usr/bin/env python3
"""PDF del bloque de fuerza de Fede (8 semanas, pesos proyectados).

Los datos salen de rutina_fuerza.py. Uso: python generar_pdf_rutina_fuerza.py
"""
from datetime import timedelta
from pathlib import Path

from fpdf import FPDF

import rutina_fuerza as rf

OUT = Path(__file__).resolve().parent / "Plan-Fede-Rutina-Fuerza.pdf"

NAVY = (30, 41, 59)
SLATE = (71, 85, 105)
GRAY_LIGHT = (241, 245, 249)
GRAY_MID = (203, 213, 225)
WHITE = (255, 255, 255)
GREEN = (34, 197, 94)
ORANGE = (249, 115, 22)
RED = (239, 68, 68)
AMBER = (245, 158, 11)

COLOR_DIA = {
    "LUNES": (59, 130, 246),
    "MARTES": (16, 185, 129),
    "JUEVES": (168, 85, 247),
    "VIERNES": (239, 68, 68),
}


def t(s: str) -> str:
    """Las fuentes base del PDF son latin-1: reemplazo lo que no entra."""
    for a, b in (("—", "-"), ("−", "-"), ("≤", "<="), ("⚠", "!"), ("’", "'"), ("“", '"'), ("”", '"')):
        s = s.replace(a, b)
    return s.encode("latin-1", "ignore").decode("latin-1")


def rect(pdf, x, y, w, h, color):
    pdf.set_fill_color(*color)
    pdf.rect(x, y, w, h, style="F")


def txt(pdf, x, y, w, h, s, size=10, style="", color=NAVY, align="L"):
    pdf.set_font("Helvetica", style, size)
    pdf.set_text_color(*color)
    pdf.set_xy(x, y)
    pdf.cell(w, h, t(s), align=align)


def portada(pdf):
    pdf.add_page()
    rect(pdf, 0, 0, 210, 72, NAVY)
    txt(pdf, 15, 18, 180, 12, "PLAN GYM FEDE", 30, "B", WHITE)
    txt(pdf, 15, 34, 180, 8, "Fuerza con barra - 4 dias - 8 semanas", 17, "", WHITE)
    fin = rf.fecha_semana(rf.N_SEMANAS)
    txt(pdf, 15, 50, 180, 6,
        f"Del {rf.INICIO.strftime('%d/%m/%Y')} al {(fin + timedelta(days=4)).strftime('%d/%m/%Y')} - pesos proyectados semana a semana",
        11, "", WHITE)

    y = 84
    rect(pdf, 15, y, 180, 58, GRAY_LIGHT)
    txt(pdf, 20, y + 5, 170, 8, "COMO FUNCIONA", 14, "B")
    items = [
        "4 basicos con barra: sentadilla, press banca, peso muerto y press militar.",
        "Se programan en % de tu Training Max (TM = 90% del maximo estimado).",
        "Semanas 1-2: 5x5. Semanas 3, 6 y 7: serie pesada de 2-3 reps al 87-95% + volumen.",
        "Secundarios con barra (remo, rumano, inclinado, frontal, hip thrust) suben cada semana.",
        "Semana 4 = descarga. Semana 8 = test: serie pesada a maximas reps dejando 1.",
        "Semana 1 calibra: si el 5x5 sale sobrado, +5 kg y se recalcula todo el bloque.",
        "El bot te manda los pesos del dia 30 min antes de cada sesion.",
    ]
    yy = y + 16
    for it in items:
        txt(pdf, 20, yy, 5, 5, "-", 10, "", SLATE)
        txt(pdf, 25, yy, 165, 5, it, 10, "", SLATE)
        yy += 5.8

    y = 152
    txt(pdf, 15, y, 180, 8, "LAS 8 SEMANAS", 14, "B")
    y += 11
    ancho = 180 / rf.N_SEMANAS
    for n in range(1, rf.N_SEMANAS + 1):
        x = 15 + (n - 1) * ancho
        tipo = rf.tipo_semana(n)
        color = AMBER if tipo == "DESCARGA" else RED if tipo == "TEST" else NAVY
        rect(pdf, x + 0.5, y, ancho - 1, 22, color)
        txt(pdf, x + 0.5, y + 2, ancho - 1, 6, f"S{n}", 12, "B", WHITE, "C")
        txt(pdf, x + 0.5, y + 9, ancho - 1, 5, rf.fecha_semana(n).strftime("%d/%m"), 9, "", WHITE, "C")
        txt(pdf, x + 0.5, y + 15, ancho - 1, 5, tipo.capitalize(), 7, "B", WHITE, "C")

    y += 27
    txt(pdf, 15, y, 60, 6, "TRAINING MAX (sem 1-4 -> 5-8):", 8, "B", SLATE)
    x = 64
    nombres = {"banca": "Banca", "sentadilla": "Sentadilla", "muerto": "Peso muerto", "militar": "Militar"}
    for clave, (base, suba) in rf.TM.items():
        txt(pdf, x, y, 33, 6, f"{nombres[clave]} {rf.fmt_kg(base)}->{rf.fmt_kg(base + suba)}", 7.5, "B", NAVY)
        x += 33
    y += 10
    txt(pdf, 15, y, 180, 8, "LA SEMANA", 14, "B")
    y += 11
    semana = [
        ("LUNES", "07:00", rf.DIAS[0]["sesion"]),
        ("MARTES", "07:00", rf.DIAS[1]["sesion"]),
        ("MIERCOLES", "-", "Bici zona 2 - 40 min"),
        ("JUEVES", "07:00", rf.DIAS[3]["sesion"]),
        ("VIERNES", "13:30", rf.DIAS[4]["sesion"]),
        ("SABADO", "-", "Bici zona 2 - 40 min"),
        ("DOMINGO", "-", "Bici zona 2 - 40 min"),
    ]
    for dia, hora, ses in semana:
        color = COLOR_DIA.get(dia, GRAY_MID)
        rect(pdf, 15, y, 4, 9, color)
        rect(pdf, 19, y, 176, 9, GRAY_LIGHT)
        txt(pdf, 22, y + 1.5, 32, 6, dia, 10, "B")
        txt(pdf, 55, y + 1.5, 16, 6, hora, 10, "", SLATE)
        txt(pdf, 72, y + 1.5, 120, 6, ses, 10, "B" if dia in COLOR_DIA else "", NAVY if dia in COLOR_DIA else SLATE)
        y += 10


def pagina_dia(pdf, idx):
    info = rf.DIAS[idx]
    color = COLOR_DIA[info["dia"]]
    pdf.add_page()
    rect(pdf, 0, 0, 210, 28, color)
    txt(pdf, 15, 6, 120, 9, info["dia"], 22, "B", WHITE)
    txt(pdf, 15, 17, 150, 6, f"{info['sesion']} - {info['hora']} - 60 min aprox.", 12, "", WHITE)

    y = 34
    rect(pdf, 15, y, 4, 7, ORANGE)
    txt(pdf, 22, y + 0.5, 170, 6, "CALENTAMIENTO 8 MIN + APROXIMACION AL BASICO: barra sola x10, 50% x5, 70% x3, 85% x1", 9, "B")
    y += 11

    ancho_sem = 16
    x_sem = 195 - ancho_sem * rf.N_SEMANAS
    for i, ej in enumerate(info["ejercicios"], 1):
        nombre, tipo, base, inc, unidad, descanso, nota, calibrar = ej
        alto = 37 if tipo != "BW" else 17
        rect(pdf, 15, y, 180, alto, WHITE)
        pdf.set_draw_color(*GRAY_MID)
        pdf.set_line_width(0.2)
        pdf.rect(15, y, 180, alto, style="D")
        rect(pdf, 15, y, 3, alto, color)
        rect(pdf, 21, y + 3, 7, 7, color)
        txt(pdf, 21, y + 3, 7, 7, str(i), 10, "B", WHITE, "C")
        etiqueta = {"P": "BASICO CON BARRA - % del TM", "S": "SECUNDARIO CON BARRA", "A": "ACCESORIO",
                    "C": "CARRY", "BW": "PESO CORPORAL"}[tipo]
        txt(pdf, 31, y + 2, 120, 5, nombre, 11, "B")
        txt(pdf, 31, y + 7.5, 120, 4, f"{etiqueta} - descanso {descanso}" + ("  - CALIBRAR EN S1" if calibrar else ""), 7, "B",
            RED if calibrar else SLATE)
        pdf.set_font("Helvetica", "", 8)
        pdf.set_text_color(*SLATE)
        pdf.set_xy(31, y + 12)
        pdf.multi_cell(160 if tipo == "BW" else 160, 3.6, t(nota))

        if tipo != "BW":
            yy = y + 18
            txt(pdf, 31, yy + 1, 40, 4, ("kg " + unidad if unidad else "kg") + " por semana", 7, "B", SLATE)
            txt(pdf, 31, yy + 5, 40, 4, "series x reps", 7, "B", (37, 99, 235))
            txt(pdf, 31, yy + 9, 40, 4, "RIR (reps en reserva)", 6, "", SLATE)
            if tipo == "P":
                txt(pdf, 31, yy + 13, 40, 4, "kg = pesada / volumen", 6, "", SLATE)
            for n in range(1, rf.N_SEMANAS + 1):
                x = x_sem + (n - 1) * ancho_sem
                tipo_s = rf.tipo_semana(n)
                fondo = (254, 243, 199) if tipo_s == "DESCARGA" else (254, 226, 226) if tipo_s == "TEST" else GRAY_LIGHT
                rect(pdf, x + 0.3, yy - 1, ancho_sem - 0.6, 18, fondo)
                txt(pdf, x + 0.3, yy - 1, ancho_sem - 0.6, 3.5, f"S{n}", 6, "", SLATE, "C")
                valor = rf.celda_basico(ej, n) if tipo == "P" else rf.fmt_kg(rf.kg(ej, n))
                txt(pdf, x + 0.3, yy + 2.5, ancho_sem - 0.6, 4.5, valor, 7 if "/" in valor else 9, "B", NAVY, "C")
                sr, rir = rf.series_reps(ej, n)
                txt(pdf, x + 0.3, yy + 7.5, ancho_sem - 0.6, 4, sr, 6.2 if len(sr) > 7 else 7.5, "B", (37, 99, 235), "C")
                txt(pdf, x + 0.3, yy + 11.8, ancho_sem - 0.6, 4, f"RIR {rir}", 6, "", SLATE, "C")
        y += alto + 2



def pagina_reglas(pdf):
    pdf.add_page()
    rect(pdf, 0, 0, 210, 36, NAVY)
    txt(pdf, 15, 13, 180, 10, "REGLAS DE ORO", 22, "B", WHITE)
    y = 48
    for r in rf.REGLAS:
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(*SLATE)
        pdf.set_xy(22, y)
        pdf.multi_cell(173, 4.8, t(r))
        alto = pdf.get_y() - y
        rect(pdf, 15, y, 3, alto, RED if "Dolor" in r or "fallo" in r or "aire" in r else NAVY)
        y = pdf.get_y() + 4

    y += 4
    rect(pdf, 15, y, 180, 30, (254, 243, 199))
    txt(pdf, 20, y + 4, 170, 6, "PENDIENTE: ELECTROCARDIOGRAMA + PRESION EN FARMACIA", 11, "B")
    pdf.set_font("Helvetica", "", 9.5)
    pdf.set_text_color(*SLATE)
    pdf.set_xy(20, y + 12)
    pdf.multi_cell(170, 4.6, t(
        "Hasta tenerlos, el tope es 1 repeticion en reserva y nada de aguantar el aire. "
        "Con el ECG normal se habilitan singles pesados y test de maximo real en los basicos."))


def main():
    pdf = FPDF(format="A4")
    pdf.set_auto_page_break(auto=False)
    portada(pdf)
    for idx in rf.DIAS:
        pagina_dia(pdf, idx)
    pagina_reglas(pdf)
    pdf.output(str(OUT))
    print(f"PDF generado: {OUT}")


if __name__ == "__main__":
    main()
