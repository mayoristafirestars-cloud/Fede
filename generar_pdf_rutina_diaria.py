#!/usr/bin/env python3
"""Rutina-Diaria-Fede.pdf — diseno v2 (moderno)"""
from pathlib import Path
from fpdf import FPDF
from fpdf.fonts import FontFace

OUT = Path("/home/user/Fede/Rutina-Diaria-Fede.pdf")
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

# ==== PALETA ====
NAVY   = (15, 23, 42)      # texto principal
SLATE  = (71, 85, 105)     # texto secundario
GRAY   = (148, 163, 184)   # texto sutil
BG     = (248, 250, 252)   # fondo cards
LINE   = (226, 232, 240)   # bordes

# Colores por dia (banda de color)
DAY_COLORS = {
    "LUN": (5, 150, 105),      # verde bosque
    "MAR": (5, 150, 105),      # verde
    "MIE": (37, 99, 235),      # azul (descanso)
    "JUE": (5, 150, 105),      # verde
    "VIE": (124, 58, 237),     # violeta (comida libre)
    "SAB": (37, 99, 235),      # azul
    "DOM": (37, 99, 235),      # azul
}

# Colores de tipo de accion
COLORS = {
    "gym":    (220, 38, 38),   # rojo (entreno)
    "meal":   (5, 150, 105),   # verde (comida)
    "supp":   (139, 92, 246),  # violeta (suplementos)
    "sleep":  (30, 41, 59),    # azul oscuro (dormir)
    "water":  (14, 165, 233),  # celeste (agua)
    "cardio": (234, 88, 12),   # naranja (cardio)
    "hobby":  (219, 39, 119),  # rosa (hobby)
    "task":   (100, 116, 139), # gris (tareas menores)
}

# Iconos (símbolos Unicode que SI están en DejaVu Sans)
ICON = {
    "gym":    "▲",
    "meal":   "●",
    "supp":   "◆",
    "sleep":  "☾",
    "water":  "◉",
    "cardio": "►",
    "hobby":  "★",
    "task":   "▫",
}


class RutinaPDF(FPDF):
    day_label = ""
    day_color = NAVY

    def header(self):
        if self.page_no() == 1:
            return
        # Banda superior fina con color del dia
        self.set_fill_color(*self.day_color)
        self.rect(0, 0, self.w, 4, "F")
        # Header con dia
        self.set_y(8)
        self.set_font("DejaVu", "B", 9)
        self.set_text_color(*SLATE)
        self.cell(0, 5, "Rutina Diaria — Fede", align="L")
        self.set_font("DejaVu", "", 9)
        self.set_text_color(*self.day_color)
        self.cell(0, 5, self.day_label, align="R", new_x="LMARGIN", new_y="NEXT")
        self.set_y(16)

    def footer(self):
        self.set_y(-12)
        self.set_draw_color(*LINE)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(1)
        self.set_font("DejaVu", "", 8)
        self.set_text_color(*GRAY)
        self.cell(0, 4, f"Pagina {self.page_no()}   ·   Plan de longevidad Fede", align="C")


def action_card(pdf, hora, tipo, titulo, detalle):
    """Card con acento de color a la izquierda."""
    color = COLORS[tipo]
    icon = ICON[tipo]
    x0 = pdf.l_margin
    w = pdf.epw

    # Calcular altura necesaria (dinamica segun texto)
    pdf.set_font("DejaVu", "", 9)
    detail_lines = pdf.multi_cell(w - 32, 4, detalle, split_only=True) if detalle else [""]
    detail_h = max(1, len(detail_lines)) * 4
    card_h = max(14, 6 + 4 + detail_h)

    # Fondo card
    y0 = pdf.get_y()
    pdf.set_fill_color(*BG)
    pdf.rect(x0, y0, w, card_h, "F")

    # Barra lateral izquierda de color
    pdf.set_fill_color(*color)
    pdf.rect(x0, y0, 2.5, card_h, "F")

    # Hora (columna izquierda, en color)
    pdf.set_xy(x0 + 5, y0 + 2)
    pdf.set_font("DejaVu", "B", 10)
    pdf.set_text_color(*color)
    pdf.cell(20, 5, hora)

    # Icono (chico, al lado de hora)
    pdf.set_font("DejaVu", "B", 11)
    pdf.set_text_color(*color)
    pdf.cell(6, 5, icon)

    # Titulo (bold, dark)
    pdf.set_font("DejaVu", "B", 10)
    pdf.set_text_color(*NAVY)
    pdf.cell(0, 5, titulo, new_x="LMARGIN", new_y="NEXT")

    # Detalle (regular, gris)
    if detalle:
        pdf.set_x(x0 + 31)
        pdf.set_font("DejaVu", "", 9)
        pdf.set_text_color(*SLATE)
        pdf.multi_cell(w - 32, 4, detalle, new_x="LMARGIN", new_y="NEXT")

    pdf.set_y(y0 + card_h + 2)


def day_banner(pdf, label, subtitle, color_key):
    """Pagina nueva con banner del dia."""
    color = DAY_COLORS[color_key]
    pdf.day_label = label
    pdf.day_color = color
    pdf.add_page()

    # Banner grande arriba
    pdf.set_fill_color(*color)
    pdf.rect(0, 0, pdf.w, 32, "F")
    # Titulo del dia
    pdf.set_y(9)
    pdf.set_font("DejaVu", "B", 20)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 9, label, align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("DejaVu", "", 11)
    pdf.cell(0, 6, subtitle, align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.set_y(38)


def checklist_box(pdf, items):
    """Checklist con checkboxes visuales."""
    x0 = pdf.l_margin
    w = pdf.epw

    # Titulo
    pdf.ln(3)
    pdf.set_font("DejaVu", "B", 11)
    pdf.set_text_color(*NAVY)
    pdf.cell(0, 6, "Checklist del dia", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(1)

    # Fondo card
    y0 = pdf.get_y()
    card_h = 4 + len(items) * 6 + 2
    pdf.set_fill_color(*BG)
    pdf.rect(x0, y0, w, card_h, "F")
    pdf.set_draw_color(*LINE)
    pdf.rect(x0, y0, w, card_h, "D")

    pdf.set_xy(x0 + 4, y0 + 3)
    pdf.set_font("DejaVu", "", 10)
    pdf.set_text_color(*NAVY)
    for it in items:
        pdf.set_x(x0 + 4)
        pdf.cell(6, 5.5, "☐")
        pdf.cell(0, 5.5, it, new_x="LMARGIN", new_y="NEXT")

    pdf.set_y(y0 + card_h + 3)


def stat_card(pdf, x, y, w, h, label, value, color):
    """Mini card para estadisticas."""
    pdf.set_fill_color(*BG)
    pdf.rect(x, y, w, h, "F")
    pdf.set_fill_color(*color)
    pdf.rect(x, y, w, 1.5, "F")

    pdf.set_xy(x + 3, y + 4)
    pdf.set_font("DejaVu", "", 8)
    pdf.set_text_color(*SLATE)
    pdf.cell(w - 6, 4, label)

    pdf.set_xy(x + 3, y + 10)
    pdf.set_font("DejaVu", "B", 12)
    pdf.set_text_color(*NAVY)
    pdf.cell(w - 6, 6, value)


def render_day(pdf, day_key, subtitle, actions, checklist_items):
    day_banner(pdf, day_key, subtitle, day_key[:3])
    for act in actions:
        action_card(pdf, *act)
    checklist_box(pdf, checklist_items)


def main():
    pdf = RutinaPDF(orientation="P", unit="mm", format="A4")
    pdf.set_margins(14, 20, 14)
    pdf.set_auto_page_break(True, margin=15)
    pdf.add_font("DejaVu", "", FONT_REG)
    pdf.add_font("DejaVu", "B", FONT_BOLD)

    # ==================== PORTADA ====================
    pdf.add_page()

    # Fondo hero
    pdf.set_fill_color(*NAVY)
    pdf.rect(0, 0, pdf.w, 80, "F")
    # Franja de color abajo del hero
    pdf.set_fill_color(5, 150, 105)
    pdf.rect(0, 80, pdf.w, 2, "F")

    # Titulo
    pdf.set_y(24)
    pdf.set_font("DejaVu", "B", 30)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 14, "Rutina Diaria", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("DejaVu", "", 14)
    pdf.set_text_color(148, 163, 184)
    pdf.cell(0, 8, "Fede  ·  Cronograma hora por hora", align="C", new_x="LMARGIN", new_y="NEXT")

    # Cards de resumen (3 columnas)
    pdf.set_y(95)
    card_w = (pdf.epw - 8) / 3
    y = pdf.get_y()
    stat_card(pdf, pdf.l_margin,                        y, card_w, 20, "GYM POR SEMANA", "4 dias", (220, 38, 38))
    stat_card(pdf, pdf.l_margin + card_w + 4,           y, card_w, 20, "CALORIAS GYM",   "2.250 kcal", (5, 150, 105))
    stat_card(pdf, pdf.l_margin + (card_w + 4) * 2,     y, card_w, 20, "AGUA / DIA",     "3 L",     (14, 165, 233))
    pdf.set_y(y + 26)
    stat_card(pdf, pdf.l_margin,                        pdf.get_y(), card_w, 20, "PROTEINA",       "200 g", (139, 92, 246))
    stat_card(pdf, pdf.l_margin + card_w + 4,           pdf.get_y(), card_w, 20, "SUENO OBJETIVO", "7 h",   (30, 41, 59))
    stat_card(pdf, pdf.l_margin + (card_w + 4) * 2,     pdf.get_y(), card_w, 20, "PESO OBJETIVO",  "95 kg", (234, 88, 12))
    pdf.set_y(pdf.get_y() + 30)

    # Semana de un vistazo
    pdf.set_font("DejaVu", "B", 12)
    pdf.set_text_color(*NAVY)
    pdf.cell(0, 6, "La semana de un vistazo", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    dias_resumen = [
        ("LUN", "GYM 07:00", "Dia A — Empuje + Bisagra", (5, 150, 105)),
        ("MAR", "GYM 07:00", "Dia B — Tiron + Sentadilla", (5, 150, 105)),
        ("MIE", "DESCANSO",  "Caminata Z2 + hobby",       (37, 99, 235)),
        ("JUE", "GYM 07:00", "Dia A — Empuje + Bisagra",  (5, 150, 105)),
        ("VIE", "GYM 14:00", "Dia B — Cena LIBRE",        (124, 58, 237)),
        ("SAB", "DESCANSO",  "Caminata Z2 + familia",     (37, 99, 235)),
        ("DOM", "DESCANSO",  "Caminata + Batch cooking",  (37, 99, 235)),
    ]
    for d, tag, desc, color in dias_resumen:
        x0 = pdf.l_margin
        w = pdf.epw
        y0 = pdf.get_y()
        pdf.set_fill_color(*BG)
        pdf.rect(x0, y0, w, 9, "F")
        pdf.set_fill_color(*color)
        pdf.rect(x0, y0, 2.5, 9, "F")

        pdf.set_xy(x0 + 6, y0 + 2)
        pdf.set_font("DejaVu", "B", 10)
        pdf.set_text_color(*color)
        pdf.cell(15, 5, d)

        pdf.set_font("DejaVu", "B", 10)
        pdf.set_text_color(*NAVY)
        pdf.cell(30, 5, tag)

        pdf.set_font("DejaVu", "", 9)
        pdf.set_text_color(*SLATE)
        pdf.cell(0, 5, desc, new_x="LMARGIN", new_y="NEXT")
        pdf.set_y(y0 + 10)

    pdf.ln(3)
    # Nota
    pdf.set_font("DejaVu", "", 8)
    pdf.set_text_color(*GRAY)
    pdf.multi_cell(0, 4, "Este PDF es para tener EN LA HELADERA o en el celular. Cada dia con su cronograma completo (comidas, gym, suplementos, agua, sol, dormir). Al final de cada dia, un checklist para tildar.")

    # ==================== LUNES ====================
    render_day(pdf, "LUNES",
               "GYM 07:00  ·  Dia A: Empuje + Bisagra",
               [
                   ("05:30", "water",  "Despertar",             "Vaso 300 ml + pizca de sal"),
                   ("05:35", "task",   "Bano rapido y ropa gym", ""),
                   ("05:45", "meal",   "Pre-entreno",           "Media banana 80 g  +  cafe negro 150 ml  +  agua 300 ml"),
                   ("06:30", "task",   "Salir al gym",          ""),
                   ("06:50", "gym",    "Calentamiento 8 min",   "Cinta 5 km/h + movilidad + barra vacia"),
                   ("07:00", "gym",    "ENTRENO Dia A",         "Complex A: sent. frontal → RDL → remo pecho → press pie → good morning"),
                   ("08:00", "meal",   "Post-entreno",          "Whey 35 g + agua 300 ml"),
                   ("08:15", "task",   "Volver a casa + ducha", ""),
                   ("09:00", "task",   "Sol 15 min con desayuno", "Ventana o balcon. Cara y brazos."),
                   ("09:30", "meal",   "DESAYUNO",              "3 huevos duros  +  pan integral 30 g  +  palta 70 g  +  tomate 100 g  +  queso port salut 20 g  +  oliva 5 ml"),
                   ("09:45", "supp",   "Suplementos AM",        "Vitamina D3  +  Omega-3"),
                   ("13:00", "meal",   "ALMUERZO",              "Pollo 220 g  +  papa hervida 100 g  +  ensalada (lechuga + rucula + tomate + pepino + palta + aceitunas)  +  oliva 12 ml + limon"),
                   ("13:15", "supp",   "Omega-3 (2do)",         ""),
                   ("14:00", "task",   "ULTIMO MATE del dia",   "Despues solo agua o infusiones sin teina"),
                   ("16:30", "meal",   "MERIENDA",              "Yogur griego 170 g  +  nueces 12 g  +  canela"),
                   ("20:30", "meal",   "CENA",                  "Merluza 200 g  +  zapallito 150 g  +  morron 70 g  +  anchoas 20 g  +  huevo duro  +  oliva 12 ml + limon"),
                   ("22:00", "meal",   "SNACK NOCTURNO ANCLA",  "Yogur griego 170 g  +  chia 10 g  +  canela"),
                   ("22:00", "supp",   "Magnesio glicinato",    "300 mg con el snack"),
                   ("22:15", "task",   "15 min lectura en cama", "Papel o e-reader sin luz"),
                   ("22:30", "sleep",  "DORMIR",                "Cuarto oscuro, 18-20°C, celular AFUERA"),
               ],
               ["Agua total ~3,0 L", "Sol 15 min", "8000+ pasos",
                "4 comidas + snack nocturno", "Sin alcohol",
                "Sin cafeina despues de 15:00", "Acostado 22:30"])

    # ==================== MARTES ====================
    render_day(pdf, "MARTES",
               "GYM 07:00  ·  Dia B: Tiron + Sentadilla",
               [
                   ("05:30", "water",  "Despertar",             "Agua 300 ml + sal"),
                   ("05:45", "meal",   "Pre-entreno",           "Pasas de uva 30 g (punadito)  +  cafe 150 ml  +  agua con sal 300 ml"),
                   ("06:30", "task",   "Salir al gym",          ""),
                   ("07:00", "gym",    "ENTRENO Dia B",         "Complex B: sent. trasera → remo supino → power clean → RDL → shrug"),
                   ("08:00", "meal",   "Post-entreno",          "Whey 35 g + agua 300 ml"),
                   ("09:30", "meal",   "DESAYUNO",              "3 huevos duros  +  queso port salut 30 g  +  pan integral 30 g  +  palta 60 g  +  tomate 100 g  +  oliva 5 ml"),
                   ("09:45", "supp",   "Suplementos AM",        "Vitamina D3  +  Omega-3"),
                   ("13:00", "meal",   "ALMUERZO",              "Pollo 220 g  +  boniato hervido 100 g  +  ensalada  +  oliva 12 ml + limon"),
                   ("14:00", "task",   "ULTIMO MATE",           ""),
                   ("16:30", "meal",   "MERIENDA",              "Cottage 200 g  +  frutillas 30 g  +  canela"),
                   ("20:30", "meal",   "CENA",                  "Salmon 180 g  +  espinaca salteada 150 g  +  champignones 80 g  +  ajo  +  oliva 12 ml + limon"),
                   ("22:00", "meal",   "SNACK NOCTURNO",        "Yogur 170 g + chia 10 g"),
                   ("22:00", "supp",   "Magnesio 300 mg",       ""),
                   ("22:30", "sleep",  "DORMIR",                ""),
               ],
               ["Agua ~3,0 L", "Sol 15 min", "8000+ pasos",
                "4 comidas + snack", "Sin alcohol",
                "Sin cafeina despues 15:00", "Acostado 22:30"])

    # ==================== MIERCOLES ====================
    render_day(pdf, "MIERCOLES",
               "DESCANSO  ·  Dia clave para longevidad",
               [
                   ("06:30", "water",  "Despertar",             "Agua 300 ml (sin sal, no entrenas)"),
                   ("07:00", "cardio", "CAMINATA ZONA 2",       "30-40 min a ritmo firme 5,5-6 km/h. Al sol si podes."),
                   ("07:30", "meal",   "DESAYUNO",              "3 huevos duros  +  ricota 80 g  +  palta 60 g  +  tomate 100 g  +  oliva 5 ml. Sin pan."),
                   ("07:45", "supp",   "Suplementos AM",        "Vit D3  +  Omega-3  +  Creatina 5 g"),
                   ("10:00", "meal",   "MEDIA MANANA",          "Yogur griego 200 g  +  nueces 10 g  +  frutillas 30 g"),
                   ("13:00", "meal",   "ALMUERZO",              "Atun 180 g  +  2 huevos duros  +  espinaca 150 g  +  queso 30 g  +  ensalada  +  palta 60 g  +  oliva 15 ml"),
                   ("14:00", "task",   "ULTIMO MATE",           ""),
                   ("16:30", "meal",   "MERIENDA",              "Ricota 150 g  +  almendras 10 g  +  cacao amargo 3 g (mezclar)"),
                   ("17:00", "hobby",  "HOBBY",                 "30-45 min de lo que elijas (pescar, cocinar, instrumento, huerta, padel). CLAVE."),
                   ("20:30", "meal",   "CENA",                  "Pollo 180 g  +  brocoli 200 g  +  champignones 80 g  +  aceitunas 15 g  +  oliva 12 ml"),
                   ("22:00", "meal",   "SNACK NOCTURNO",        "Yogur 170 g + chia 10 g"),
                   ("22:00", "supp",   "Magnesio 300 mg",       ""),
                   ("22:30", "sleep",  "DORMIR",                ""),
               ],
               ["Caminata Z2 30-40 min HECHA",
                "Hobby minimo 30 min",
                "Agua ~2,7 L", "Sol 15+ min",
                "Sin alcohol", "Acostado 22:30"])

    # ==================== JUEVES ====================
    render_day(pdf, "JUEVES",
               "GYM 07:00  ·  Dia A: Empuje + Bisagra",
               [
                   ("05:30", "water",  "Despertar + sal",       ""),
                   ("05:45", "meal",   "Pre-entreno",           "Media banana 80 g  +  cafe  +  agua con sal"),
                   ("07:00", "gym",    "ENTRENO Dia A",         "Igual lunes"),
                   ("08:00", "meal",   "Post-entreno",          "Whey 35 g + agua"),
                   ("09:30", "meal",   "DESAYUNO diferente",    "Yogur griego proteico 200 g  +  frutillas 100 g  +  almendras 15 g  +  canela  +  2 huevos duros aparte  +  pan integral 30 g"),
                   ("09:45", "supp",   "Suplementos AM",        "Vit D3  +  Omega-3"),
                   ("13:00", "meal",   "ALMUERZO",              "Pollo 200 g  +  papa hervida 100 g  +  huevo duro  +  ensalada nicoise  +  palta 50 g  +  oliva 12 ml"),
                   ("14:00", "task",   "ULTIMO MATE",           ""),
                   ("16:30", "meal",   "MERIENDA",              "Yogur griego 170 g  +  nueces 12 g  +  frutos rojos 20 g"),
                   ("20:30", "meal",   "CENA",                  "Brotola 200 g  +  brocoli 200 g  +  huevo duro  +  anchoas 20 g  +  oliva 12 ml"),
                   ("22:00", "meal",   "SNACK NOCTURNO",        "Yogur 170 g + chia 10 g"),
                   ("22:00", "supp",   "Magnesio 300 mg",       ""),
                   ("22:30", "sleep",  "DORMIR",                ""),
               ],
               ["Agua ~3,0 L", "Sol 15 min", "8000+ pasos",
                "4 comidas + snack", "Sin alcohol",
                "Sin cafeina despues 15:00", "Acostado 22:30"])

    # ==================== VIERNES ====================
    render_day(pdf, "VIERNES",
               "GYM 14:00  ·  Dia B  ·  CENA LIBRE",
               [
                   ("06:30", "water",  "Despertar",             "Agua 400 ml"),
                   ("07:30", "meal",   "DESAYUNO",              "3 huevos duros  +  queso port salut 30 g  +  palta 60 g  +  tomate 100 g  +  oliva 5 ml. Sin pan."),
                   ("07:45", "supp",   "Suplementos AM",        "Vit D3  +  Omega-3"),
                   ("10:30", "meal",   "MEDIA MANANA",          "Yogur griego 150 g  +  nueces 10 g  +  frutillas 30 g"),
                   ("12:30", "meal",   "PRE-ENTRENO LIVIANO",   "Pasas de uva 30 g (punadito)  +  cafe  +  agua con sal 400 ml. NO comer solido pesado 11-14 h."),
                   ("13:30", "task",   "Salir al gym",          ""),
                   ("14:00", "gym",    "ENTRENO Dia B",         ""),
                   ("15:15", "meal",   "Post-entreno",          "Whey 35 g + agua (sin fruta — almuerzo viene a las 17 h)"),
                   ("15:30", "task",   "Volver casa + ducha",   ""),
                   ("17:00", "meal",   "ALMUERZO-MERIENDA",     "Pollo 220 g  +  papa hervida 100 g  +  espinaca  +  rucula  +  tomates cherry  +  palta  +  almendras  +  pan integral 30 g  +  oliva 12 ml"),
                   ("20:30", "meal",   "CENA LIBRE",            "UNA opcion: pizza (2 porciones) / parrilla (250 g magra) / sushi (12-15 piezas) / pasta (300 g). Sin alcohol o max 1 copa vino."),
                   ("22:00", "meal",   "Snack OPCIONAL",        "Si la cena fue abundante, salteala. Sino: yogur 100 g"),
                   ("22:30", "sleep",  "DORMIR",                ""),
               ],
               ["Comida libre elegida CONSCIENTE (no atracon)",
                "Sin alcohol (o max 1 copa) — anotar si tomas",
                "Acostado 22:30", "Agua ~3,2 L"])

    # ==================== SABADO ====================
    render_day(pdf, "SABADO",
               "DESCANSO  ·  Familia + hobby",
               [
                   ("06:30", "water",  "Despertar",             "Agua 300 ml"),
                   ("07:00", "cardio", "CAMINATA ZONA 2",       "30-40 min ritmo firme. Al sol."),
                   ("07:30", "meal",   "DESAYUNO",              "3 huevos duros  +  jamon cocido magro 30 g  +  queso port salut 30 g  +  palta 50 g  +  tomate 100 g  +  oliva 5 ml"),
                   ("07:45", "supp",   "Suplementos AM",        "Vit D3  +  Omega-3  +  Creatina 5 g"),
                   ("10:00", "meal",   "MEDIA MANANA",          "Cottage 150 g  +  frutillas 50 g  +  nueces 7 g"),
                   ("13:00", "meal",   "ALMUERZO",              "Pollo 220 g  +  brocoli 150 g  +  zapallitos hervidos 100 g  +  ensalada  +  palta 40 g  +  oliva 12 ml"),
                   ("14:00", "task",   "ULTIMO MATE",           ""),
                   ("16:30", "meal",   "MERIENDA",              "Huevo duro  +  tomate 100 g  +  oliva 5 ml  +  almendras 10 g"),
                   ("17:00", "hobby",  "HOBBY / familia",       "Aprovecha el sabado"),
                   ("20:30", "meal",   "CENA",                  "Pollo 180 g  +  2 huevos duros  +  queso port salut 25 g  +  espinaca 150 g  +  champignones  +  anchoas 15 g  +  oliva 10 ml"),
                   ("22:00", "meal",   "SNACK NOCTURNO",        "Yogur 170 g + chia 10 g"),
                   ("22:00", "supp",   "Magnesio 300 mg",       ""),
                   ("22:30", "sleep",  "DORMIR",                ""),
               ],
               ["Caminata Z2 HECHA", "Hobby / familia >30 min",
                "Agua ~2,7 L", "Sol 15+ min",
                "Sin alcohol", "Acostado 22:30"])

    # ==================== DOMINGO ====================
    render_day(pdf, "DOMINGO",
               "DESCANSO  ·  BATCH COOKING",
               [
                   ("06:30", "water",  "Despertar",             "Agua 300 ml"),
                   ("07:00", "cardio", "CAMINATA Z2",           "30-40 min al sol"),
                   ("07:30", "meal",   "DESAYUNO",              "3 huevos duros  +  palta 60 g  +  tomate 100 g  +  queso descremado 30 g  +  oliva 5 ml. Sin pan."),
                   ("07:45", "supp",   "Suplementos AM",        "Vit D3  +  Omega-3  +  Creatina 5 g"),
                   ("10:00", "task",   "BATCH COOKING 90 min",  "1) Pollo 1,8 kg horno  2) 20 huevos duros  3) Papa+boniato hervidos  4) Verduras vapor  5) Aderezos"),
                   ("13:30", "meal",   "ALMUERZO",              "Pollo horno 220 g  +  ensalada completa  +  palta 60 g  +  aceitunas 15 g  +  nueces 10 g  +  oliva 12 ml"),
                   ("14:00", "task",   "ULTIMO MATE",           ""),
                   ("16:30", "meal",   "MERIENDA",              "Yogur griego 200 g  +  nueces 10 g  +  cacao amargo 3 g"),
                   ("17:00", "hobby",  "HOBBY / hijos",         "Ideal aire libre"),
                   ("19:00", "task",   "Preparar semana",       "Revisar mediciones (peso + cintura del lunes en ayunas)"),
                   ("20:30", "meal",   "CENA Caesar low-carb",  "Pollo 180 g  +  lechuga romana 100 g  +  huevo duro  +  anchoas 20 g  +  parmesano 15 g  +  aderezo (oliva + limon + ajo + yema)"),
                   ("22:00", "meal",   "SNACK NOCTURNO",        "Yogur 170 g + chia 10 g"),
                   ("22:00", "supp",   "Magnesio 300 mg",       ""),
                   ("22:30", "sleep",  "DORMIR",                "Cargar tensiometro para lunes"),
               ],
               ["Caminata Z2 HECHA", "Batch cooking HECHO",
                "Hobby / familia >45 min", "Mediciones del lunes preparadas",
                "Sin alcohol", "Acostado 22:30"])

    # ==================== SUPLEMENTOS Y AGUA ====================
    pdf.day_label = "REFERENCIA"
    pdf.day_color = NAVY
    pdf.add_page()
    pdf.set_fill_color(*NAVY)
    pdf.rect(0, 0, pdf.w, 32, "F")
    pdf.set_y(9)
    pdf.set_font("DejaVu", "B", 20)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 9, "Referencia rapida", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("DejaVu", "", 11)
    pdf.cell(0, 6, "Suplementos  ·  Agua  ·  Reglas", align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.set_y(40)
    pdf.set_font("DejaVu", "B", 12)
    pdf.set_text_color(*NAVY)
    pdf.cell(0, 6, "Suplementos", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(1)

    pdf.set_font("DejaVu", "", 9)
    with pdf.table(
        line_height=5,
        text_align="LEFT",
        headings_style=FontFace(emphasis="BOLD", color=(255, 255, 255), fill_color=(139, 92, 246)),
        borders_layout="MINIMAL",
    ) as t:
        r = t.row(); r.cell("Suplemento"); r.cell("Dosis"); r.cell("Cuando"); r.cell("Dias")
        for row in [
            ["Vitamina D3", "2000-4000 UI", "Con desayuno", "TODOS"],
            ["Omega-3 (EPA+DHA)", "2-3 g", "Almuerzo o cena", "TODOS"],
            ["Creatina monohidrato", "5 g", "Post-entreno (gym) o desayuno (descanso)", "TODOS"],
            ["Whey protein", "35 g", "Post-entreno", "Lun/Mar/Jue/Vie"],
            ["Magnesio glicinato", "300 mg", "22:00 con snack nocturno", "TODOS"],
            ["Sal extra", "2 g", "Repartir en el dia", "Primera semana"],
        ]:
            r = t.row()
            for cell in row:
                r.cell(cell)

    pdf.ln(5)
    pdf.set_font("DejaVu", "B", 12)
    pdf.set_text_color(*NAVY)
    pdf.cell(0, 6, "Agua total por dia", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(1)
    pdf.set_font("DejaVu", "", 9)
    with pdf.table(
        line_height=5,
        text_align="LEFT",
        headings_style=FontFace(emphasis="BOLD", color=(255, 255, 255), fill_color=(14, 165, 233)),
        borders_layout="MINIMAL",
    ) as t:
        r = t.row(); r.cell("Momento"); r.cell("Cantidad"); r.cell("Notas")
        for row in [
            ["Al despertar", "300-400 ml", "Con pizca de sal los dias gym"],
            ["Manana (hasta almuerzo)", "500-800 ml", ""],
            ["Con almuerzo", "200-300 ml", ""],
            ["Tarde (15-20 h)", "500-700 ml", "Incluye mate hasta 14 h"],
            ["Con cena", "200 ml", "Cortar antes para dormir"],
            ["TOTAL DIA GYM", "3,0-3,2 L", ""],
            ["TOTAL DIA DESCANSO", "2,7-3,0 L", ""],
        ]:
            r = t.row()
            for cell in row:
                r.cell(cell)

    pdf.ln(5)
    pdf.set_font("DejaVu", "B", 12)
    pdf.set_text_color(*NAVY)
    pdf.cell(0, 6, "Reglas de oro", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(1)
    pdf.set_font("DejaVu", "", 10)
    pdf.set_text_color(*NAVY)
    reglas = [
        ("1", "Proteina en CADA comida", "Sin excepcion. Es el nutriente que preserva musculo."),
        ("2", "Ultima cafeina antes de las 15:00", "Cafe + mate. Despues solo agua o infusiones sin teina."),
        ("3", "Snack nocturno = ancla anti-alcohol", "Yogur griego + chia todas las noches. No opcional."),
        ("4", "Sin pantallas 15 min antes de dormir", "Bajar luces, leer, respirar."),
        ("5", "FC max 121 lpm hasta ECG", "Si el reloj sube, descansas mas entre series."),
    ]
    for n, titulo, det in reglas:
        y0 = pdf.get_y()
        x0 = pdf.l_margin
        pdf.set_fill_color(*BG)
        pdf.rect(x0, y0, pdf.epw, 10, "F")
        pdf.set_fill_color(5, 150, 105)
        pdf.rect(x0, y0, 8, 10, "F")

        pdf.set_xy(x0, y0 + 2)
        pdf.set_font("DejaVu", "B", 12)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(8, 6, n, align="C")

        pdf.set_font("DejaVu", "B", 10)
        pdf.set_text_color(*NAVY)
        pdf.set_xy(x0 + 11, y0 + 1)
        pdf.cell(0, 4, titulo, new_x="LMARGIN", new_y="NEXT")

        pdf.set_font("DejaVu", "", 8)
        pdf.set_text_color(*SLATE)
        pdf.set_xy(x0 + 11, y0 + 5)
        pdf.cell(0, 4, det, new_x="LMARGIN", new_y="NEXT")
        pdf.set_y(y0 + 12)

    pdf.output(str(OUT))
    print(f"PDF generado: {OUT}")
    print(f"Tamano: {OUT.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    main()
