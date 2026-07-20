#!/usr/bin/env python3
"""Plan-Fede.pdf — todo en uno: dieta + gym + suplementos + compras + longevidad."""
from pathlib import Path
from fpdf import FPDF
from fpdf.fonts import FontFace

OUT = Path("/home/user/Fede/Plan-Fede.pdf")
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

# ==== PALETA ====
NAVY   = (15, 23, 42)
SLATE  = (71, 85, 105)
GRAY   = (148, 163, 184)
BG     = (248, 250, 252)
LINE   = (226, 232, 240)

DAY_COLORS = {
    "LUN": (5, 150, 105), "MAR": (5, 150, 105), "MIE": (37, 99, 235),
    "JUE": (5, 150, 105), "VIE": (124, 58, 237),
    "SAB": (37, 99, 235), "DOM": (37, 99, 235),
    "REF": (30, 41, 59),  "GYM": (220, 38, 38),
    "SUP": (139, 92, 246), "LON": (5, 150, 105),
}

COLORS = {
    "gym": (220, 38, 38), "meal": (5, 150, 105), "supp": (139, 92, 246),
    "sleep": (30, 41, 59), "water": (14, 165, 233), "cardio": (234, 88, 12),
    "hobby": (219, 39, 119), "task": (148, 163, 184),
}
ICON = {"gym": "▲", "meal": "●", "supp": "◆", "sleep": "☾",
        "water": "◉", "cardio": "►", "hobby": "★", "task": "▫"}


class Plan(FPDF):
    section_label = ""
    section_color = NAVY

    def header(self):
        pass

    def footer(self):
        self.set_y(-8)
        self.set_font("DejaVu", "", 7)
        self.set_text_color(*GRAY)
        self.cell(0, 4, f"{self.section_label}  ·  Pag. {self.page_no()}  ·  Plan Fede", align="C")


def section_banner(pdf, label, subtitle, color_key):
    color = DAY_COLORS[color_key]
    pdf.section_label = label
    pdf.section_color = color
    pdf.add_page()
    pdf.set_fill_color(*color)
    pdf.rect(0, 0, pdf.w, 18, "F")
    pdf.set_y(3)
    pdf.set_font("DejaVu", "B", 15)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 6, label, align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("DejaVu", "", 9)
    pdf.cell(0, 4, subtitle, align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_y(22)


def action_row(pdf, hora, tipo, titulo, detalle=""):
    color = COLORS[tipo]
    icon = ICON[tipo]
    x0 = pdf.l_margin
    w = pdf.epw

    inline = detalle and len(detalle) <= 60
    if not detalle:
        h = 6
    elif inline:
        h = 6
    else:
        pdf.set_font("DejaVu", "", 7.5)
        det_lines = pdf.multi_cell(w - 22, 3.2, detalle, dry_run=True, output="LINES")
        h = 4 + len(det_lines) * 3.4

    y0 = pdf.get_y()
    pdf.set_fill_color(*color)
    pdf.rect(x0, y0 + 0.5, 1.5, h - 1, "F")

    pdf.set_xy(x0 + 3, y0)
    pdf.set_font("DejaVu", "B", 9)
    pdf.set_text_color(*color)
    pdf.cell(13, 5, hora)
    pdf.set_font("DejaVu", "B", 9)
    pdf.cell(4, 5, icon)

    pdf.set_font("DejaVu", "B", 9)
    pdf.set_text_color(*NAVY)

    if inline:
        pdf.cell(50, 5, titulo)
        pdf.set_font("DejaVu", "", 8)
        pdf.set_text_color(*SLATE)
        pdf.cell(0, 5, detalle, new_x="LMARGIN", new_y="NEXT")
    else:
        pdf.cell(0, 5, titulo, new_x="LMARGIN", new_y="NEXT")
        if detalle:
            pdf.set_x(x0 + 20)
            pdf.set_font("DejaVu", "", 7.5)
            pdf.set_text_color(*SLATE)
            pdf.multi_cell(w - 22, 3.4, detalle, new_x="LMARGIN", new_y="NEXT")
    pdf.set_y(y0 + h)


def checklist_row(pdf, items):
    x0 = pdf.l_margin
    w = pdf.epw
    pdf.ln(2)
    pdf.set_font("DejaVu", "B", 9)
    pdf.set_text_color(*NAVY)
    pdf.cell(0, 5, "Checklist del dia", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(0.5)
    col_w = w / 2
    y0 = pdf.get_y()
    per_col = (len(items) + 1) // 2
    pdf.set_font("DejaVu", "", 8)
    pdf.set_text_color(*NAVY)
    for i, it in enumerate(items):
        x = x0 if i < per_col else x0 + col_w
        y = y0 + (i if i < per_col else i - per_col) * 4.2
        pdf.set_xy(x, y)
        pdf.cell(4, 4, "☐")
        pdf.cell(col_w - 5, 4, it)
    pdf.set_y(y0 + per_col * 4.2)


def stat_card(pdf, x, y, w, h, label, value, color):
    pdf.set_fill_color(*BG); pdf.rect(x, y, w, h, "F")
    pdf.set_fill_color(*color); pdf.rect(x, y, w, 1.5, "F")
    pdf.set_xy(x + 3, y + 4)
    pdf.set_font("DejaVu", "", 8); pdf.set_text_color(*SLATE)
    pdf.cell(w - 6, 4, label)
    pdf.set_xy(x + 3, y + 10)
    pdf.set_font("DejaVu", "B", 12); pdf.set_text_color(*NAVY)
    pdf.cell(w - 6, 6, value)


def render_day(pdf, day_key, subtitle, actions, checklist_items):
    section_banner(pdf, day_key, subtitle, day_key[:3])
    for act in actions:
        action_row(pdf, *act)
    checklist_row(pdf, checklist_items)


def h2(pdf, text, color=None):
    if color is None:
        color = pdf.section_color
    if pdf.get_y() > pdf.h - 40:
        pdf.add_page()
    pdf.ln(2)
    pdf.set_font("DejaVu", "B", 11)
    pdf.set_text_color(*color)
    pdf.cell(0, 6, text, new_x="LMARGIN", new_y="NEXT")


def bullet(pdf, text, indent=4):
    pdf.set_font("DejaVu", "", 8.5)
    pdf.set_text_color(*NAVY)
    pdf.set_x(pdf.l_margin + indent)
    pdf.multi_cell(pdf.epw - indent, 4, "• " + text, new_x="LMARGIN", new_y="NEXT")


def note(pdf, text):
    pdf.set_font("DejaVu", "", 7.5)
    pdf.set_text_color(*GRAY)
    pdf.multi_cell(0, 3.5, text, new_x="LMARGIN", new_y="NEXT")


def rule_card(pdf, num, titulo, det, color=(5, 150, 105)):
    y0 = pdf.get_y()
    x0 = pdf.l_margin
    pdf.set_fill_color(*BG); pdf.rect(x0, y0, pdf.epw, 8, "F")
    pdf.set_fill_color(*color); pdf.rect(x0, y0, 7, 8, "F")
    pdf.set_xy(x0, y0 + 1.5)
    pdf.set_font("DejaVu", "B", 11); pdf.set_text_color(255, 255, 255)
    pdf.cell(7, 5, num, align="C")
    pdf.set_font("DejaVu", "B", 9); pdf.set_text_color(*NAVY)
    pdf.set_xy(x0 + 10, y0 + 0.8)
    pdf.cell(0, 3.5, titulo, new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("DejaVu", "", 7.5); pdf.set_text_color(*SLATE)
    pdf.set_xy(x0 + 10, y0 + 4)
    pdf.cell(0, 3.5, det, new_x="LMARGIN", new_y="NEXT")
    pdf.set_y(y0 + 9.5)


def exercise_table(pdf, rows, header_color=(220, 38, 38)):
    pdf.set_font("DejaVu", "", 8)
    with pdf.table(
        line_height=4.5,
        text_align="LEFT",
        headings_style=FontFace(emphasis="BOLD", color=(255, 255, 255), fill_color=header_color),
        borders_layout="MINIMAL",
    ) as t:
        for row in rows:
            r = t.row()
            for cell in row:
                r.cell(str(cell))


# =========================================================
def main():
    pdf = Plan(orientation="P", unit="mm", format="A4")
    pdf.set_margins(12, 12, 12)
    pdf.set_auto_page_break(True, margin=10)
    pdf.add_font("DejaVu", "", FONT_REG)
    pdf.add_font("DejaVu", "B", FONT_BOLD)

    # =============== PORTADA ===============
    pdf.section_label = "PORTADA"
    pdf.section_color = NAVY
    pdf.add_page()
    pdf.set_fill_color(*NAVY); pdf.rect(0, 0, pdf.w, 55, "F")
    pdf.set_fill_color(5, 150, 105); pdf.rect(0, 55, pdf.w, 2, "F")
    pdf.set_y(18)
    pdf.set_font("DejaVu", "B", 26); pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 12, "Plan Fede", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("DejaVu", "", 12); pdf.set_text_color(148, 163, 184)
    pdf.cell(0, 7, "Longevidad  ·  dieta Primal  ·  gym  ·  rutina diaria", align="C", new_x="LMARGIN", new_y="NEXT")

    # Stat cards
    pdf.set_y(65)
    cw = (pdf.epw - 8) / 3
    y = pdf.get_y()
    stat_card(pdf, pdf.l_margin,               y, cw, 18, "GYM / SEMANA",   "4 dias", (220, 38, 38))
    stat_card(pdf, pdf.l_margin + cw + 4,      y, cw, 18, "CALORIAS GYM",   "2.250", (5, 150, 105))
    stat_card(pdf, pdf.l_margin + (cw + 4)*2,  y, cw, 18, "AGUA / DIA",     "3 L", (14, 165, 233))
    pdf.set_y(y + 22); y = pdf.get_y()
    stat_card(pdf, pdf.l_margin,               y, cw, 18, "PROTEINA",       "200 g", (139, 92, 246))
    stat_card(pdf, pdf.l_margin + cw + 4,      y, cw, 18, "SUENO OBJETIVO", "7 h", (30, 41, 59))
    stat_card(pdf, pdf.l_margin + (cw + 4)*2,  y, cw, 18, "PESO OBJETIVO",  "95 kg", (234, 88, 12))
    pdf.set_y(y + 26)

    # Indice
    pdf.set_font("DejaVu", "B", 11); pdf.set_text_color(*NAVY)
    pdf.cell(0, 6, "En este PDF (todo en uno)", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(1)
    indice = [
        ("1", "La semana de un vistazo", "1 pag"),
        ("2", "Lunes a Domingo — cronograma dia a dia", "7 pags"),
        ("3", "Rutina de gym (ejercicios detallados)", "2 pags"),
        ("4", "Lista de compras semanal", "1 pag"),
        ("5", "Referencia: suplementos + agua + reglas", "1 pag"),
        ("6", "Plan de longevidad: screening + labs", "1 pag"),
    ]
    for n, t, p in indice:
        y0 = pdf.get_y()
        pdf.set_fill_color(*BG); pdf.rect(pdf.l_margin, y0, pdf.epw, 7, "F")
        pdf.set_fill_color(5, 150, 105); pdf.rect(pdf.l_margin, y0, 6, 7, "F")
        pdf.set_xy(pdf.l_margin, y0 + 1)
        pdf.set_font("DejaVu", "B", 10); pdf.set_text_color(255, 255, 255)
        pdf.cell(6, 5, n, align="C")
        pdf.set_xy(pdf.l_margin + 9, y0 + 1)
        pdf.set_font("DejaVu", "", 9); pdf.set_text_color(*NAVY)
        pdf.cell(0, 5, t)
        pdf.set_x(pdf.l_margin + pdf.epw - 20)
        pdf.set_font("DejaVu", "", 8); pdf.set_text_color(*GRAY)
        pdf.cell(20, 5, p, align="R", new_x="LMARGIN", new_y="NEXT")
        pdf.set_y(y0 + 8)

    # =============== SEMANA DE UN VISTAZO ===============
    section_banner(pdf, "LA SEMANA DE UN VISTAZO", "1 fila = 1 dia", "REF")
    dias_resumen = [
        ("LUN", "GYM 07:00", "Dia A — Empuje + Bisagra", (5, 150, 105)),
        ("MAR", "GYM 07:00", "Dia B — Tiron + Sentadilla", (5, 150, 105)),
        ("MIE", "DESCANSO",  "Caminata Z2 + hobby", (37, 99, 235)),
        ("JUE", "GYM 07:00", "Dia A — Empuje + Bisagra", (5, 150, 105)),
        ("VIE", "GYM 14:00", "Dia B — Cena LIBRE", (124, 58, 237)),
        ("SAB", "DESCANSO",  "Caminata Z2 + familia", (37, 99, 235)),
        ("DOM", "DESCANSO",  "Caminata + Batch cooking", (37, 99, 235)),
    ]
    for d, tag, desc, color in dias_resumen:
        y0 = pdf.get_y()
        pdf.set_fill_color(*BG); pdf.rect(pdf.l_margin, y0, pdf.epw, 10, "F")
        pdf.set_fill_color(*color); pdf.rect(pdf.l_margin, y0, 2.5, 10, "F")
        pdf.set_xy(pdf.l_margin + 6, y0 + 2.5)
        pdf.set_font("DejaVu", "B", 10); pdf.set_text_color(*color)
        pdf.cell(15, 5, d)
        pdf.set_font("DejaVu", "B", 10); pdf.set_text_color(*NAVY)
        pdf.cell(28, 5, tag)
        pdf.set_font("DejaVu", "", 9); pdf.set_text_color(*SLATE)
        pdf.cell(0, 5, desc, new_x="LMARGIN", new_y="NEXT")
        pdf.set_y(y0 + 11)

    pdf.ln(4)
    h2(pdf, "Estructura general de cada dia", color=NAVY)
    pdf.set_font("DejaVu", "", 8.5); pdf.set_text_color(*NAVY)
    for line in [
        "• Despertar con agua (+ pizca de sal los dias gym).",
        "• Pre-entreno LIVIANO 1 h antes del gym (banana o pasas + cafe).",
        "• Post-entreno: whey + agua.",
        "• Desayuno principal 60-75 min despues del entreno.",
        "• Almuerzo 13:00, merienda 16:30, cena 20:30, snack ancla 22:00.",
        "• Ultimo mate/cafe: 14:00.",
        "• Dormir 22:30. Cuarto oscuro, 18-20°C, sin celular.",
    ]:
        pdf.multi_cell(0, 4.5, line, new_x="LMARGIN", new_y="NEXT")

    # =============== LOS 7 DIAS ===============
    render_day(pdf, "LUNES",
               "GYM 07:00  ·  Dia A: Empuje + Bisagra",
               [
                   ("05:30", "water",  "Despertar", "Vaso 300 ml + pizca de sal"),
                   ("05:35", "task",   "Bano rapido y ropa gym", ""),
                   ("05:45", "meal",   "Pre-entreno", "Media banana 80 g + cafe 150 ml + agua con sal 300 ml"),
                   ("06:30", "task",   "Salir al gym", ""),
                   ("06:50", "gym",    "Calentamiento 8 min", "Cinta 5 km/h + movilidad + barra vacia"),
                   ("07:00", "gym",    "ENTRENO Dia A", "Complex A: sent. frontal → RDL → remo pecho → press pie → good morning"),
                   ("08:00", "meal",   "Post-entreno", "Whey 35 g + agua 300 ml"),
                   ("08:15", "task",   "Volver + ducha", ""),
                   ("09:00", "task",   "Sol 15 min", "Ventana o balcon. Cara y brazos."),
                   ("09:30", "meal",   "DESAYUNO Primal", "4 huevos duros + palta 90 g + tomate 100 g + queso 20 g + oliva 5 ml"),
                   ("09:45", "supp",   "Suplementos AM", "Vitamina D3 + Omega-3"),
                   ("13:00", "meal",   "ALMUERZO", "Pollo 220 g + papa hervida 100 g + ensalada (lechuga + rucula + tomate + pepino + palta + aceitunas) + oliva 12 ml"),
                   ("13:15", "supp",   "Omega-3 (2do)", ""),
                   ("14:00", "task",   "ULTIMO MATE del dia", "Despues solo agua o infusiones sin teina"),
                   ("16:30", "meal",   "MERIENDA", "Yogur griego 170 g + nueces 12 g + canela"),
                   ("19:00", "meal",   "CENA", "Merluza 200 g + zapallito 150 g + morron 70 g + anchoas 20 g + huevo duro + oliva 12 ml + limon"),
                   ("22:00", "meal",   "SNACK NOCTURNO", "Yogur griego 170 g + chia 10 g + canela (ancla anti-alcohol)"),
                   ("22:00", "supp",   "Magnesio 300 mg", "Con el snack"),
                   ("22:15", "task",   "15 min lectura", "En cama, papel o e-reader sin luz"),
                   ("22:30", "sleep",  "DORMIR", "Cuarto oscuro, 18-20°C, celular AFUERA"),
               ],
               ["Agua total ~3,0 L", "Sol 15 min", "8000+ pasos",
                "4 comidas + snack", "Sin alcohol",
                "Sin cafeina despues 15:00", "Acostado 22:30"])

    render_day(pdf, "MARTES",
               "GYM 07:00  ·  Dia B: Tiron + Sentadilla",
               [
                   ("05:30", "water",  "Despertar", "Agua 300 ml + sal"),
                   ("05:45", "meal",   "Pre-entreno", "Pasas de uva 30 g (punadito) + cafe 150 ml + agua con sal 300 ml"),
                   ("06:30", "task",   "Salir al gym", ""),
                   ("07:00", "gym",    "ENTRENO Dia B", "Complex B: sent. trasera → remo supino → power clean → RDL → shrug"),
                   ("08:00", "meal",   "Post-entreno", "Whey 35 g + agua 300 ml"),
                   ("09:30", "meal",   "DESAYUNO Primal", "4 huevos duros + queso port salut 30 g + palta 80 g + tomate 100 g + oliva 5 ml"),
                   ("09:45", "supp",   "Suplementos AM", "Vitamina D3 + Omega-3"),
                   ("13:00", "meal",   "ALMUERZO", "Pollo 220 g + boniato hervido 100 g + ensalada + oliva 12 ml + limon"),
                   ("14:00", "task",   "ULTIMO MATE", ""),
                   ("16:30", "meal",   "MERIENDA", "Cottage 200 g + frutillas 30 g + canela"),
                   ("19:00", "meal",   "CENA", "Salmon 180 g + espinaca salteada 150 g + champignones 80 g + ajo + oliva 12 ml + limon"),
                   ("22:00", "meal",   "SNACK NOCTURNO", "Yogur griego 170 g + chia 10 g"),
                   ("22:00", "supp",   "Magnesio 300 mg", ""),
                   ("22:30", "sleep",  "DORMIR", ""),
               ],
               ["Agua ~3,0 L", "Sol 15 min", "8000+ pasos",
                "4 comidas + snack", "Sin alcohol",
                "Sin cafeina despues 15:00", "Acostado 22:30"])

    render_day(pdf, "MIERCOLES",
               "DESCANSO  ·  Dia clave para longevidad",
               [
                   ("06:30", "water",  "Despertar", "Agua 300 ml (sin sal, no entrenas)"),
                   ("07:00", "cardio", "CAMINATA ZONA 2", "30-40 min ritmo firme 5,5-6 km/h. Al sol si podes."),
                   ("07:30", "meal",   "DESAYUNO", "3 huevos duros + ricota 80 g + palta 60 g + tomate 100 g + oliva 5 ml. Sin pan."),
                   ("07:45", "supp",   "Suplementos AM", "Vit D3 + Omega-3 + Creatina 5 g"),
                   ("10:00", "meal",   "MEDIA MANANA", "Yogur griego 200 g + nueces 10 g + frutillas 30 g"),
                   ("13:00", "meal",   "ALMUERZO", "Atun 180 g + 2 huevos duros + espinaca 150 g + queso 30 g + ensalada + palta 60 g + oliva 15 ml"),
                   ("14:00", "task",   "ULTIMO MATE", ""),
                   ("16:30", "meal",   "MERIENDA", "Ricota 150 g + almendras 10 g + cacao amargo 3 g"),
                   ("17:00", "hobby",  "HOBBY", "30-45 min (pescar, cocinar, instrumento, huerta, padel). CLAVE."),
                   ("19:00", "meal",   "CENA", "Pollo 180 g + brocoli 200 g + champignones 80 g + aceitunas 15 g + oliva 12 ml"),
                   ("22:00", "meal",   "SNACK NOCTURNO", "Yogur 170 g + chia 10 g"),
                   ("22:00", "supp",   "Magnesio 300 mg", ""),
                   ("22:30", "sleep",  "DORMIR", ""),
               ],
               ["Caminata Z2 30-40 min HECHA", "Hobby minimo 30 min",
                "Agua ~2,7 L", "Sol 15+ min",
                "Sin alcohol", "Acostado 22:30"])

    render_day(pdf, "JUEVES",
               "GYM 07:00  ·  Dia A: Empuje + Bisagra",
               [
                   ("05:30", "water",  "Despertar + sal", ""),
                   ("05:45", "meal",   "Pre-entreno", "Media banana 80 g + cafe + agua con sal"),
                   ("07:00", "gym",    "ENTRENO Dia A", "Igual lunes"),
                   ("08:00", "meal",   "Post-entreno", "Whey 35 g + agua"),
                   ("09:30", "meal",   "DESAYUNO Primal", "Yogur griego 200 g + frutillas 100 g + almendras 15 g + canela + 3 huevos duros aparte"),
                   ("09:45", "supp",   "Suplementos AM", "Vit D3 + Omega-3"),
                   ("13:00", "meal",   "ALMUERZO", "Pollo 200 g + papa hervida 100 g + huevo duro + ensalada nicoise + palta 50 g + oliva 12 ml"),
                   ("14:00", "task",   "ULTIMO MATE", ""),
                   ("16:30", "meal",   "MERIENDA", "Yogur griego 170 g + nueces 12 g + frutos rojos 20 g"),
                   ("19:00", "meal",   "CENA", "Brotola 200 g + brocoli 200 g + huevo duro + anchoas 20 g + oliva 12 ml"),
                   ("22:00", "meal",   "SNACK NOCTURNO", "Yogur 170 g + chia 10 g"),
                   ("22:00", "supp",   "Magnesio 300 mg", ""),
                   ("22:30", "sleep",  "DORMIR", ""),
               ],
               ["Agua ~3,0 L", "Sol 15 min", "8000+ pasos",
                "4 comidas + snack", "Sin alcohol",
                "Sin cafeina despues 15:00", "Acostado 22:30"])

    render_day(pdf, "VIERNES",
               "GYM 14:00  ·  Dia B  ·  CENA LIBRE",
               [
                   ("06:30", "water",  "Despertar", "Agua 400 ml"),
                   ("07:30", "meal",   "DESAYUNO Primal", "4 huevos duros + queso port salut 30 g + palta 80 g + tomate 100 g + oliva 5 ml"),
                   ("07:45", "supp",   "Suplementos AM", "Vit D3 + Omega-3"),
                   ("10:30", "meal",   "MEDIA MANANA", "Yogur griego 150 g + nueces 10 g + frutillas 30 g"),
                   ("12:30", "meal",   "PRE-ENTRENO LIVIANO", "Pasas 30 g + cafe + agua con sal 400 ml. NO comer solido pesado 11-14 h."),
                   ("13:30", "task",   "Salir al gym", ""),
                   ("14:00", "gym",    "ENTRENO Dia B", ""),
                   ("15:15", "meal",   "Post-entreno", "Whey 35 g + agua (sin fruta — almuerzo viene a las 17 h)"),
                   ("15:30", "task",   "Volver casa + ducha", ""),
                   ("16:00", "meal",   "ALMUERZO-MERIENDA", "Pollo 220 g + papa hervida 150 g + espinaca + rucula + tomates cherry + palta 70 g + almendras + oliva 12 ml"),
                   ("19:00", "meal",   "CENA LIBRE", "UNA: pizza (2 porc) / parrilla (250 g magra) / sushi (12-15 p) / pasta (300 g). Sin alcohol o max 1 vino."),
                   ("22:00", "meal",   "Snack OPCIONAL", "Si la cena fue abundante, salteala. Sino: yogur 100 g"),
                   ("22:30", "sleep",  "DORMIR", ""),
               ],
               ["Comida libre CONSCIENTE (no atracon)",
                "Sin alcohol (o max 1 copa) — anotar",
                "Acostado 22:30", "Agua ~3,2 L"])

    render_day(pdf, "SABADO",
               "DESCANSO  ·  Familia + hobby",
               [
                   ("06:30", "water",  "Despertar", "Agua 300 ml"),
                   ("07:00", "cardio", "CAMINATA ZONA 2", "30-40 min ritmo firme. Al sol."),
                   ("07:30", "meal",   "DESAYUNO", "3 huevos duros + jamon magro 30 g + queso port salut 30 g + palta 50 g + tomate 100 g + oliva 5 ml"),
                   ("07:45", "supp",   "Suplementos AM", "Vit D3 + Omega-3 + Creatina 5 g"),
                   ("10:00", "meal",   "MEDIA MANANA", "Cottage 150 g + frutillas 50 g + nueces 7 g"),
                   ("13:00", "meal",   "ALMUERZO", "Pollo 220 g + brocoli 150 g + zapallitos hervidos 100 g + ensalada + palta 40 g + oliva 12 ml"),
                   ("14:00", "task",   "ULTIMO MATE", ""),
                   ("16:30", "meal",   "MERIENDA", "Huevo duro + tomate 100 g + oliva 5 ml + almendras 10 g"),
                   ("17:00", "hobby",  "HOBBY / familia", "Aprovecha el sabado"),
                   ("19:00", "meal",   "CENA", "Pollo 180 g + 2 huevos duros + queso port salut 25 g + espinaca 150 g + champignones + anchoas 15 g + oliva 10 ml"),
                   ("22:00", "meal",   "SNACK NOCTURNO", "Yogur 170 g + chia 10 g"),
                   ("22:00", "supp",   "Magnesio 300 mg", ""),
                   ("22:30", "sleep",  "DORMIR", ""),
               ],
               ["Caminata Z2 HECHA", "Hobby / familia >30 min",
                "Agua ~2,7 L", "Sol 15+ min",
                "Sin alcohol", "Acostado 22:30"])

    render_day(pdf, "DOMINGO",
               "DESCANSO  ·  BATCH COOKING",
               [
                   ("06:30", "water",  "Despertar", "Agua 300 ml"),
                   ("07:00", "cardio", "CAMINATA Z2", "30-40 min al sol"),
                   ("07:30", "meal",   "DESAYUNO", "3 huevos duros + palta 60 g + tomate 100 g + queso descremado 30 g + oliva 5 ml. Sin pan."),
                   ("07:45", "supp",   "Suplementos AM", "Vit D3 + Omega-3 + Creatina 5 g"),
                   ("10:00", "task",   "BATCH COOKING 90 min", "1) Pollo 1,8 kg horno  2) 20 huevos duros  3) Papa+boniato hervidos  4) Verduras vapor  5) Aderezos"),
                   ("13:30", "meal",   "ALMUERZO", "Pollo horno 220 g + ensalada completa + palta 60 g + aceitunas 15 g + nueces 10 g + oliva 12 ml"),
                   ("14:00", "task",   "ULTIMO MATE", ""),
                   ("16:30", "meal",   "MERIENDA", "Yogur griego 200 g + nueces 10 g + cacao amargo 3 g"),
                   ("17:00", "hobby",  "HOBBY / hijos", "Ideal aire libre"),
                   ("19:00", "task",   "Preparar semana", "Revisar mediciones (peso + cintura del lunes en ayunas)"),
                   ("19:00", "meal",   "CENA Caesar", "Pollo 180 g + lechuga romana 100 g + huevo duro + anchoas 20 g + parmesano 15 g + aderezo (oliva + limon + ajo + yema)"),
                   ("22:00", "meal",   "SNACK NOCTURNO", "Yogur 170 g + chia 10 g"),
                   ("22:00", "supp",   "Magnesio 300 mg", ""),
                   ("22:30", "sleep",  "DORMIR", "Cargar tensiometro para lunes"),
               ],
               ["Caminata Z2 HECHA", "Batch cooking HECHO",
                "Hobby / familia >45 min", "Mediciones del lunes preparadas",
                "Sin alcohol", "Acostado 22:30"])

    # =============== RUTINA DE GYM ===============
    section_banner(pdf, "RUTINA DE GYM", "4 semanas — Complexes A/B/A/B", "GYM")

    h2(pdf, "Calentamiento (8 min — igual los 4 dias)", color=(220, 38, 38))
    for line in [
        "Caminata en cinta 5 km/h — 3 min. FC objetivo 90-95 lpm.",
        "Movilidad: circulos de hombro (10 c/lado), hip circles (10 c/lado), sentadilla goblet peso corporal (10), bisagra sin peso (10).",
        "Activacion barra vacia (20 kg) — 2 min. Pasada completa del complex del dia, 5 reps c/movimiento.",
    ]:
        bullet(pdf, line)

    h2(pdf, "DIA A — Empuje + Bisagra (Lun / Jue)", color=(220, 38, 38))
    exercise_table(pdf, [
        ["#", "Ejercicio", "Reps", "Tecnica clave"],
        ["1", "Sentadilla frontal (barra clavic.)", "6", "Talones al piso, rodillas siguen pie"],
        ["2", "Romanian Deadlift", "6", "Cadera atras, barra cerca del cuerpo"],
        ["3", "Remo al pecho (Pendlay Row)", "6", "Torso horizontal, codos 45°, al esternon"],
        ["4", "Press de pie (OHP)", "6", "Gluteos apretados, sin hiperextender lumbar"],
        ["5", "Good Morning", "6", "Bisagra lenta, sensacion en isquios"],
    ])
    note(pdf, "Series totales: S1: 3 | S2: 3 | S3: 4 | S4: 4  ·  Carga arranque: 30 kg (barra 20 + 5 c/lado)")

    h2(pdf, "Finalizador Dia A (opcional — solo si FC < 110 al terminar)", color=(220, 38, 38))
    exercise_table(pdf, [
        ["Ejercicio", "Series", "Reps", "RIR", "Carga S1"],
        ["Press banco con mancuernas", "2", "10", "3", "14 kg / mano"],
        ["Extension triceps polea (rope)", "2", "12", "3", "15 kg"],
    ])

    h2(pdf, "DIA B — Tiron + Sentadilla (Mar / Vie)", color=(220, 38, 38))
    exercise_table(pdf, [
        ["#", "Ejercicio", "Reps", "Tecnica clave"],
        ["1", "Sentadilla trasera", "6", "Profundidad paralela o hasta lo que permita"],
        ["2", "Remo con barra supino", "6", "Codos pegados, aprieta dorsal al final"],
        ["3", "Power Clean a la cintura", "4", "Si no domina: High Pull (tiron a menton)"],
        ["4", "Romanian Deadlift", "6", "Igual que Dia A"],
        ["5", "Shrug con barra", "8", "Sin rotar hombros, solo subir/bajar"],
    ])
    note(pdf, "Series totales: S1: 3 | S2: 3 | S3: 4 | S4: 4  ·  Carga arranque: 30 kg (25 kg si el Power Clean se ve mal)")

    h2(pdf, "Finalizador Dia B (opcional)", color=(220, 38, 38))
    exercise_table(pdf, [
        ["Ejercicio", "Series", "Reps", "RIR", "Carga S1"],
        ["Jalon al pecho polea (agarre ancho)", "2", "10", "3", "45 kg"],
        ["Curl biceps mancuernas alterno", "2", "10 c/lado", "3", "10 kg / mano"],
    ])

    h2(pdf, "Progresion de cargas S1 a S4", color=(220, 38, 38))
    exercise_table(pdf, [
        ["Semana", "Carga", "Series", "Pausa", "Objetivo"],
        ["S1", "30 kg", "3", "90 seg", "Grabar patron motor. Tecnica primero."],
        ["S2", "32,5 kg", "3", "75 seg", "Subir carga si S1 se vio bien."],
        ["S3", "35 kg", "4", "60 seg", "Sumar serie. Mas volumen."],
        ["S4", "37,5 kg", "4", "60 seg", "Semana tope. Despues DELOAD."],
    ])

    h2(pdf, "6 reglas de la sesion", color=(220, 38, 38))
    for r in [
        "Calentamiento 8 min SIEMPRE. No es opcional.",
        "Tecnica antes que carga. Si se rompe la cadena, bajas peso.",
        "FC debajo de 121 lpm. Si sube, descansas mas entre series.",
        "Velocidad: concentrico 2 seg / excentrico 3 seg.",
        "Pausa entre series: 90s (S1) / 75s (S2) / 60s (S3-S4).",
        "Si dormiste mal esa noche: salteas el finalizador.",
    ]:
        bullet(pdf, r)

    # =============== LISTA DE COMPRAS ===============
    section_banner(pdf, "LISTA DE COMPRAS SEMANAL", "Organizada por seccion del super", "REF")

    compras = [
        ("Carniceria", [
            "Pechuga de pollo: 2 kg (BASE)",
            "Jamon cocido magro: 100 g",
        ]),
        ("Pescaderia", [
            "Merluza: 400 g", "Brotola: 400 g", "Salmon: 200 g",
        ]),
        ("Almacen — Conservas", [
            "Atun al natural: 4 latas",
            "Anchoas en aceite: 1 frasco",
            "Aceitunas negras y verdes: 250 g",
        ]),
        ("Lacteos", [
            "Yogur griego proteico sin azucar: 1,5 kg",
            "Ricota descremada: 500 g",
            "Queso port salut descremado: 250 g",
            "Cottage descremado: 350 g",
            "Parmesano: 50 g",
        ]),
        ("Huevos", ["30 unidades"]),
        ("Verduras (libres)", [
            "Lechuga, rucula, espinaca (en cantidad)",
            "Tomate 1 kg, pepino 3, morron 2, cebolla blanca/morada 5",
            "Zanahoria 3, zapallitos 6, brocoli 2, champignones 250 g",
            "Limones 10-12, ajo 1 cabeza",
            "Palta: 7-8 unidades",
        ]),
        ("Frutas / carbos rapidos", [
            "Bananas: 6 unidades (Lun/Jue pre-gym + jueves)",
            "Pasas de uva: 300 g (Mar/Vie pre-gym)",
            "Frutillas: 500 g (jueves + meriendas)",
            "Arandanos: 200 g",
        ]),
        ("Almidonados (hervir domingo)", [
            "Papa: 1 kg", "Boniato: 1 kg",
        ]),
        ("Panaderia", [
            "Pan integral: 1 paquete (1 rebanada x dia gym = 4/sem)",
        ]),
        ("Frutos secos y semillas", [
            "Almendras 100 g", "Nueces peladas 100 g", "Chia 200 g",
        ]),
        ("Aceites y condimentos", [
            "Aceite oliva extra virgen 500 ml",
            "Vinagre, sal marina",
            "Oregano, canela, pimenton, cacao amargo",
        ]),
        ("Bebidas", ["Yerba mate", "Cafe", "Miel: 1 frasco chico"]),
        ("Suplementos (1 vez, duran semanas)", [
            "Whey protein 1 kg (dura ~7 sem)",
            "Creatina monohidrato 250 g (dura ~50 dias)",
            "Omega-3, Vitamina D3, Magnesio glicinato",
        ]),
    ]
    for seccion, items in compras:
        h2(pdf, seccion, color=(5, 150, 105))
        for it in items:
            bullet(pdf, it)

    # =============== REFERENCIA ===============
    section_banner(pdf, "REFERENCIA RAPIDA", "Suplementos + Agua + Reglas de oro", "SUP")

    h2(pdf, "Suplementos", color=(139, 92, 246))
    exercise_table(pdf, [
        ["Suplemento", "Dosis", "Cuando", "Dias"],
        ["Vitamina D3", "2000-4000 UI", "Con desayuno", "TODOS"],
        ["Omega-3", "2-3 g", "Almuerzo o cena", "TODOS"],
        ["Creatina", "5 g", "Post-entreno o desayuno", "TODOS"],
        ["Whey protein", "35 g", "Post-entreno", "Lun/Mar/Jue/Vie"],
        ["Magnesio glicinato", "300 mg", "22:00 snack", "TODOS"],
        ["Sal extra", "2 g", "Repartir en el dia", "1ra semana"],
    ], header_color=(139, 92, 246))

    h2(pdf, "Agua total por dia", color=(14, 165, 233))
    exercise_table(pdf, [
        ["Momento", "Cantidad", "Notas"],
        ["Al despertar", "300-400 ml", "Con pizca de sal los dias gym"],
        ["Manana", "500-800 ml", ""],
        ["Con almuerzo", "200-300 ml", ""],
        ["Tarde (15-20 h)", "500-700 ml", "Incluye mate hasta 14 h"],
        ["Con cena", "200 ml", "Cortar antes para dormir"],
        ["TOTAL DIA GYM", "3,0-3,2 L", ""],
        ["TOTAL DIA DESCANSO", "2,7-3,0 L", ""],
    ], header_color=(14, 165, 233))

    h2(pdf, "Reglas de oro", color=NAVY)
    reglas = [
        ("1", "Proteina en CADA comida", "Sin excepcion — preserva musculo."),
        ("2", "Ultima cafeina antes de las 15:00", "Cafe + mate. Despues solo agua o infusiones."),
        ("3", "Snack nocturno = ancla anti-alcohol", "Yogur griego + chia todas las noches."),
        ("4", "Sin pantallas 15 min antes de dormir", "Bajar luces, leer, respirar."),
        ("5", "FC max 121 lpm hasta ECG", "Si el reloj sube, descansas mas entre series."),
    ]
    for n, t, d in reglas:
        rule_card(pdf, n, t, d)

    # =============== PLAN DE LONGEVIDAD ===============
    section_banner(pdf, "PLAN DE LONGEVIDAD", "Screening medico + labs + hobby + fases", "LON")

    h2(pdf, "Screening PRIORIDAD ALTA (este mes)", color=(220, 38, 38))
    for line in [
        "Analisis de sangre completo (con extras de longevidad — abajo)",
        "ECG basal (obligatorio antes de intensidad alta)",
        "Tension arterial: 3 mediciones en farmacia (dias distintos)",
        "Consulta con clinico presencial",
        "Dermatologo (mapa de lunares — NUNCA fuiste)",
        "Colonoscopia (con abuela con cancer, prioridad ALTA)",
        "PSA + control urologico",
    ]:
        bullet(pdf, line)

    h2(pdf, "Screening PRIORIDAD MEDIA (30-60 dias)", color=(234, 88, 12))
    for line in [
        "Ecografia abdominal (descartar higado graso)",
        "Ergometria (si el clinico lo indica tras ECG)",
        "Oftalmologo (fondo de ojos + control ocular)",
        "Comprar tensiometro digital de brazo (medir 2x/sem en casa)",
    ]:
        bullet(pdf, line)

    h2(pdf, "Labs a pedir explicitamente (longevidad)", color=(139, 92, 246))
    exercise_table(pdf, [
        ["Marcador", "Por que", "Frecuencia"],
        ["ApoB", "Mejor predictor CV que LDL", "Anual"],
        ["Lp(a)", "Riesgo CV genetico", "1 sola vez"],
        ["hs-CRP", "Inflamacion de bajo grado", "Anual"],
        ["HbA1c + HOMA-IR", "Glucemia + resistencia insulina", "Anual"],
        ["PSA", "Prostata", "Anual"],
        ["25-OH Vitamina D", "Nivel real para dosificar D3", "2x/ano"],
        ["Testosterona total + libre", "Post 45. Energia/musculo.", "Anual"],
        ["Homocisteina", "CV + neuro (opcional)", "1 vez"],
    ], header_color=(139, 92, 246))

    h2(pdf, "Fases del plan", color=NAVY)
    rule_card(pdf, "1", "FASE 1 — Fundacion (Sem 1-4)", "Habitos + gym + turnos + labs + hobby elegido", color=(5, 150, 105))
    rule_card(pdf, "2", "FASE 2 — Amplificacion (Sem 5-12)", "VO2max si ECG OK + ajustes por labs + sueno 7h + psicologo", color=(37, 99, 235))
    rule_card(pdf, "3", "FASE 3 — Sostenimiento (Meses 4-12)", "Peso -10 kg + cintura -8 cm + anual completo + gym 5x", color=(124, 58, 237))

    h2(pdf, "Metricas — revisar cada 3 meses", color=NAVY)
    exercise_table(pdf, [
        ["Metrica", "Hoy", "6 meses", "12 meses"],
        ["Peso", "105 kg", "100 kg", "95 kg"],
        ["Cintura", "102 cm", "96 cm", "92 cm"],
        ["ICC", "0,94", "0,90", "0,88"],
        ["Sueno", "6 h", "7 h", "7,5 h"],
        ["Plancha", "10-15 s", "45 s", "60 s"],
        ["Flexiones", "15-20", "25-30", "30+"],
        ["Pasos/dia", "8.000", "9.000", "10.000"],
        ["Hobby", "0", "1 activo", "1 consolidado"],
    ], header_color=NAVY)

    h2(pdf, "Lo que NO hacemos (evidencia)", color=(220, 38, 38))
    for line in [
        "NMN, resveratrol, 'anti-aging pills': sin evidencia solida.",
        "Ayunos extremos 48h+: no aportan mas que el deficit calorico.",
        "Quemadores de grasa: contraindicados con perfil cardiovascular.",
        "Testosterona sin diagnostico: solo con endocrinologo si hay hipogonadismo real.",
    ]:
        bullet(pdf, line)

    pdf.output(str(OUT))
    print(f"PDF generado: {OUT}")
    print(f"Tamano: {OUT.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    main()
