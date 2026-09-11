#!/usr/bin/env python3
"""PDF del plan alimentario Fede — Déficit 500 kcal, sin cena.

Diseño moderno con paleta por día. Letra grande y clara.
"""
from fpdf import FPDF
from pathlib import Path

OUT = Path("/home/user/Fede/Plan-Fede-Dieta-Deficit.pdf")

# Paleta base
NAVY = (30, 41, 59)          # texto principal
SLATE = (71, 85, 105)        # secundario
GRAY_LIGHT = (241, 245, 249) # fondo cards
GRAY_MID = (203, 213, 225)   # bordes
WHITE = (255, 255, 255)
GREEN = (34, 197, 94)        # ok
ORANGE = (249, 115, 22)      # alerta

# Paleta por día
DIAS_COLOR = {
    "LUNES":     (59, 130, 246),   # azul
    "MARTES":    (16, 185, 129),   # verde
    "MIÉRCOLES": (245, 158, 11),   # ámbar
    "JUEVES":    (168, 85, 247),   # violeta
    "VIERNES":   (239, 68, 68),    # rojo
    "SÁBADO":    (14, 165, 233),   # cian
    "DOMINGO":   (139, 92, 246),   # púrpura
}

# Datos del plan
PLAN = {
    "LUNES": {
        "subtitulo": "Gym Superior A",
        "kcal_total": 1880,
        "prot_total": 181,
        "comidas": [
            {"hora": "06:00", "icono": "[DES]", "nombre": "Desayuno",
             "kcal": 570, "prot": 32,
             "ingredientes": ["4 huevos duros", "Palta 90 g", "Verdura tomate 100 g",
                              "Queso port salut 20 g", "Oliva 5 ml"]},
            {"hora": "07:30", "icono": "[POST]", "nombre": "Post-entreno",
             "kcal": 210, "prot": 28,
             "ingredientes": ["Whey 35 g", "Creatina 5 g", "Banana chica 80 g"]},
            {"hora": "09:15", "icono": "[SUPL]", "nombre": "Suplementos",
             "kcal": 0, "prot": 0,
             "ingredientes": ["Vit D3", "Omega-3"]},
            {"hora": "12:30", "icono": "[ALM]", "nombre": "Almuerzo (principal)",
             "kcal": 700, "prot": 78,
             "ingredientes": ["Pollo 250 g", "Papa hervida 100 g",
                              "Ensalada completa (hojas + tomate + zanahoria)",
                              "Palta 50 g", "Oliva 15 ml + limón"]},
            {"hora": "13:30", "icono": "[MATE]", "nombre": "Último mate del día",
             "kcal": 0, "prot": 0,
             "ingredientes": ["Después: solo agua o infusiones sin cafeína"]},
            {"hora": "16:30", "icono": "[MER-CENA]", "nombre": "Merienda-cena",
             "kcal": 300, "prot": 33,
             "ingredientes": ["Yogur griego 200 g", "2 huevos duros",
                              "Nueces 15 g", "Canela"]},
            {"hora": "21:30", "icono": "[SNACK]", "nombre": "Snack ancla (opcional)",
             "kcal": 100, "prot": 10,
             "ingredientes": ["Yogur griego 100 g", "Chía 5 g", "Magnesio 300 mg"]},
        ]
    },
    "MARTES": {
        "subtitulo": "Gym Inferior A",
        "kcal_total": 1900,
        "prot_total": 183,
        "comidas": [
            {"hora": "06:00", "icono": "[DES]", "nombre": "Desayuno",
             "kcal": 590, "prot": 34,
             "ingredientes": ["4 huevos duros", "Queso port salut 30 g",
                              "Palta 80 g", "Verdura tomate 100 g", "Oliva 5 ml"]},
            {"hora": "07:30", "icono": "[POST]", "nombre": "Post-entreno",
             "kcal": 210, "prot": 28,
             "ingredientes": ["Whey 35 g", "Creatina 5 g", "Banana chica 80 g"]},
            {"hora": "09:15", "icono": "[SUPL]", "nombre": "Suplementos",
             "kcal": 0, "prot": 0,
             "ingredientes": ["Vit D3", "Omega-3"]},
            {"hora": "12:30", "icono": "[ALM]", "nombre": "Almuerzo (principal)",
             "kcal": 700, "prot": 78,
             "ingredientes": ["Pollo 250 g", "Boniato hervido 100 g",
                              "Ensalada", "Palta 50 g", "Oliva 15 ml + limón"]},
            {"hora": "13:30", "icono": "[MATE]", "nombre": "Último mate del día",
             "kcal": 0, "prot": 0,
             "ingredientes": ["Después: solo agua o infusiones sin cafeína"]},
            {"hora": "16:30", "icono": "[MER-CENA]", "nombre": "Merienda-cena",
             "kcal": 300, "prot": 33,
             "ingredientes": ["Cottage 200 g", "2 huevos duros",
                              "Fruta frutillas 30 g", "Nueces 10 g", "Canela"]},
            {"hora": "21:30", "icono": "[SNACK]", "nombre": "Snack ancla (opcional)",
             "kcal": 100, "prot": 10,
             "ingredientes": ["Yogur griego 100 g", "Chía 5 g", "Magnesio 300 mg"]},
        ]
    },
    "MIÉRCOLES": {
        "subtitulo": "Descanso + Bici Zona 2",
        "kcal_total": 1880,
        "prot_total": 168,
        "comidas": [
            {"hora": "06:00", "icono": "[DES]", "nombre": "Desayuno",
             "kcal": 550, "prot": 32,
             "ingredientes": ["3 huevos duros", "Ricota 80 g", "Palta 60 g",
                              "Verdura tomate 100 g", "Oliva 5 ml"]},
            {"hora": "06:15", "icono": "[SUPL]", "nombre": "Suplementos",
             "kcal": 0, "prot": 0,
             "ingredientes": ["Vit D3", "Omega-3", "Creatina 5 g"]},
            {"hora": "09:30", "icono": "[MM]", "nombre": "Media mañana",
             "kcal": 250, "prot": 22,
             "ingredientes": ["Yogur griego 200 g", "Nueces 10 g",
                              "Fruta arándanos 20 g"]},
            {"hora": "12:30", "icono": "[ALM]", "nombre": "Almuerzo (principal)",
             "kcal": 680, "prot": 72,
             "ingredientes": ["Pescado atún 180 g", "2 huevos duros",
                              "Verdura espinaca 150 g", "Queso 30 g",
                              "Palta 50 g", "Oliva 12 ml"]},
            {"hora": "13:00", "icono": "[BICI]", "nombre": "Bici 40 min Zona 2",
             "kcal": 0, "prot": 0,
             "ingredientes": ["FC 105-118 lpm", "Ruta plana", "Post-almuerzo"]},
            {"hora": "13:30", "icono": "[MATE]", "nombre": "Último mate del día",
             "kcal": 0, "prot": 0,
             "ingredientes": ["Después: solo agua o infusiones sin cafeína"]},
            {"hora": "16:30", "icono": "[MER-CENA]", "nombre": "Merienda-cena",
             "kcal": 300, "prot": 32,
             "ingredientes": ["Pescado sardinas 100 g", "Palta 50 g",
                              "Verdura tomate 100 g", "Aceitunas 10 g",
                              "Oliva 5 ml + limón"]},
            {"hora": "21:30", "icono": "[SNACK]", "nombre": "Snack ancla (opcional)",
             "kcal": 100, "prot": 10,
             "ingredientes": ["Yogur griego 100 g", "Chía 5 g", "Magnesio 300 mg"]},
        ]
    },
    "JUEVES": {
        "subtitulo": "Gym Superior B",
        "kcal_total": 1860,
        "prot_total": 188,
        "comidas": [
            {"hora": "06:00", "icono": "[DES]", "nombre": "Desayuno DIFERENTE",
             "kcal": 550, "prot": 40,
             "ingredientes": ["Yogur griego 200 g", "Fruta frutillas 100 g",
                              "Almendras 15 g", "Canela", "3 huevos duros aparte"]},
            {"hora": "06:15", "icono": "[SUPL]", "nombre": "Suplementos",
             "kcal": 0, "prot": 0,
             "ingredientes": ["Vit D3", "Omega-3"]},
            {"hora": "07:30", "icono": "[POST]", "nombre": "Post-entreno",
             "kcal": 210, "prot": 28,
             "ingredientes": ["Whey 35 g", "Creatina 5 g", "Banana chica 80 g"]},
            {"hora": "12:30", "icono": "[ALM]", "nombre": "Almuerzo (principal)",
             "kcal": 700, "prot": 78,
             "ingredientes": ["Pollo 250 g", "Papa hervida 100 g",
                              "Ensalada nicoise (hojas + tomate + 1 huevo duro)",
                              "Palta 50 g", "Oliva 12 ml"]},
            {"hora": "13:30", "icono": "[MATE]", "nombre": "Último mate del día",
             "kcal": 0, "prot": 0,
             "ingredientes": ["Después: solo agua o infusiones sin cafeína"]},
            {"hora": "16:30", "icono": "[MER-CENA]", "nombre": "Merienda-cena",
             "kcal": 300, "prot": 32,
             "ingredientes": ["Yogur griego 200 g", "2 huevos duros",
                              "Nueces 12 g", "Fruta arándanos 20 g"]},
            {"hora": "21:30", "icono": "[SNACK]", "nombre": "Snack ancla (opcional)",
             "kcal": 100, "prot": 10,
             "ingredientes": ["Yogur griego 100 g", "Chía 5 g", "Magnesio 300 mg"]},
        ]
    },
    "VIERNES": {
        "subtitulo": "Gym Inferior B (tarde)",
        "kcal_total": 1855,
        "prot_total": 154,
        "comidas": [
            {"hora": "06:00", "icono": "[DES]", "nombre": "Desayuno",
             "kcal": 585, "prot": 35,
             "ingredientes": ["4 huevos duros", "Queso 30 g", "Palta 80 g",
                              "Verdura tomate 100 g", "Oliva 5 ml"]},
            {"hora": "06:15", "icono": "[SUPL]", "nombre": "Suplementos",
             "kcal": 0, "prot": 0,
             "ingredientes": ["Vit D3", "Omega-3"]},
            {"hora": "10:00", "icono": "[MM]", "nombre": "Media mañana",
             "kcal": 250, "prot": 20,
             "ingredientes": ["Yogur griego 200 g", "Nueces 10 g",
                              "Fruta frutillas 30 g"]},
            {"hora": "12:00", "icono": "[PRE]", "nombre": "Pre-entreno LIVIANO",
             "kcal": 90, "prot": 1,
             "ingredientes": ["Pasas 30 g", "Café", "Agua con sal 400 ml",
                              "NO comer sólido pesado 11-14 h"]},
            {"hora": "13:30", "icono": "[GYM]", "nombre": "GYM Inferior B",
             "kcal": 0, "prot": 0,
             "ingredientes": ["Rutina completa Trap bar + Búlgara + Hip thrust"]},
            {"hora": "14:45", "icono": "[POST]", "nombre": "Post-entreno",
             "kcal": 210, "prot": 28,
             "ingredientes": ["Whey 35 g", "Creatina 5 g", "Banana 80 g"]},
            {"hora": "15:30", "icono": "[ALM]", "nombre": "Almuerzo-merienda",
             "kcal": 620, "prot": 60,
             "ingredientes": ["Pollo 220 g", "Papa hervida 100 g",
                              "Ensalada", "Palta 60 g", "Almendras 10 g",
                              "Oliva 12 ml"]},
            {"hora": "21:30", "icono": "[SNACK]", "nombre": "Snack ancla (opcional)",
             "kcal": 100, "prot": 10,
             "ingredientes": ["Yogur griego 100 g", "Chía 5 g", "Magnesio 300 mg"]},
        ]
    },
    "SÁBADO": {
        "subtitulo": "Descanso + Bici Zona 2",
        "kcal_total": 1800,
        "prot_total": 172,
        "comidas": [
            {"hora": "06:00", "icono": "[DES]", "nombre": "Desayuno",
             "kcal": 500, "prot": 32,
             "ingredientes": ["3 huevos duros", "Jamón cocido magro 30 g",
                              "Queso port salut 30 g", "Palta 50 g",
                              "Verdura tomate 100 g", "Oliva 5 ml"]},
            {"hora": "06:15", "icono": "[SUPL]", "nombre": "Suplementos",
             "kcal": 0, "prot": 0,
             "ingredientes": ["Vit D3", "Omega-3", "Creatina 5 g"]},
            {"hora": "09:30", "icono": "[MM]", "nombre": "Media mañana",
             "kcal": 230, "prot": 25,
             "ingredientes": ["Cottage 200 g", "Fruta frutillas 50 g",
                              "Nueces 7 g", "Canela"]},
            {"hora": "12:30", "icono": "[ALM]", "nombre": "Almuerzo (principal)",
             "kcal": 650, "prot": 75,
             "ingredientes": ["Pollo 250 g", "Verdura brócoli 150 g",
                              "Verdura zapallo hervido 100 g",
                              "Palta 40 g", "Oliva 12 ml"]},
            {"hora": "13:00", "icono": "[BICI]", "nombre": "Bici 40 min Zona 2",
             "kcal": 0, "prot": 0,
             "ingredientes": ["FC 105-118 lpm", "Ruta plana"]},
            {"hora": "13:30", "icono": "[MATE]", "nombre": "Último mate del día",
             "kcal": 0, "prot": 0,
             "ingredientes": ["Después: solo agua o infusiones sin cafeína"]},
            {"hora": "16:30", "icono": "[MER-CENA]", "nombre": "Merienda-cena",
             "kcal": 320, "prot": 30,
             "ingredientes": ["Pescado sardinas 120 g", "Palta 50 g",
                              "Verdura tomate cherry 80 g", "Galleta de arroz 1",
                              "Oliva 5 ml"]},
            {"hora": "21:30", "icono": "[SNACK]", "nombre": "Snack ancla (opcional)",
             "kcal": 100, "prot": 10,
             "ingredientes": ["Yogur griego 100 g", "Chía 5 g", "Magnesio 300 mg"]},
        ]
    },
    "DOMINGO": {
        "subtitulo": "Descanso + Bici + Batch cooking",
        "kcal_total": 1700,
        "prot_total": 155,
        "comidas": [
            {"hora": "06:00", "icono": "[DES]", "nombre": "Desayuno",
             "kcal": 500, "prot": 28,
             "ingredientes": ["3 huevos duros", "Palta 60 g",
                              "Verdura tomate 100 g", "Queso 30 g", "Oliva 5 ml"]},
            {"hora": "06:15", "icono": "[SUPL]", "nombre": "Suplementos",
             "kcal": 0, "prot": 0,
             "ingredientes": ["Vit D3", "Omega-3", "Creatina 5 g"]},
            {"hora": "09:30", "icono": "[BATCH]", "nombre": "BATCH COOKING",
             "kcal": 0, "prot": 0,
             "ingredientes": ["Pollo 1,8 kg al horno", "20 huevos duros",
                              "Papas y boniatos hervidos", "Verduras al vapor"]},
            {"hora": "12:30", "icono": "[ALM]", "nombre": "Almuerzo (principal)",
             "kcal": 700, "prot": 75,
             "ingredientes": ["Pollo del horno 250 g", "Ensalada completa",
                              "Palta 60 g", "Aceitunas 10 g",
                              "Nueces 10 g", "Oliva 12 ml"]},
            {"hora": "13:30", "icono": "[MATE]", "nombre": "Último mate del día",
             "kcal": 0, "prot": 0,
             "ingredientes": ["Después: solo agua o infusiones sin cafeína"]},
            {"hora": "14:00", "icono": "[BICI]", "nombre": "Bici 40 min Zona 2",
             "kcal": 0, "prot": 0,
             "ingredientes": ["FC 105-118 lpm", "Al sol"]},
            {"hora": "16:30", "icono": "[MER-CENA]", "nombre": "Merienda-cena",
             "kcal": 300, "prot": 32,
             "ingredientes": ["Yogur griego 200 g", "2 huevos duros",
                              "Nueces 10 g", "Cacao amargo 3 g"]},
            {"hora": "21:30", "icono": "[SNACK]", "nombre": "Snack ancla (opcional)",
             "kcal": 100, "prot": 10,
             "ingredientes": ["Yogur griego 100 g", "Chía 5 g", "Magnesio 300 mg",
                              "Cargar tensiómetro para lunes"]},
        ]
    },
}


class PDF(FPDF):
    def __init__(self):
        super().__init__(format="A4", unit="mm")
        self.set_auto_page_break(auto=True, margin=15)
        self.set_margins(left=15, top=15, right=15)


def draw_rect_filled(pdf, x, y, w, h, color):
    pdf.set_fill_color(*color)
    pdf.rect(x, y, w, h, style="F")


def draw_badge(pdf, x, y, w, h, text, color_bg, color_text=WHITE, size=10):
    draw_rect_filled(pdf, x, y, w, h, color_bg)
    pdf.set_text_color(*color_text)
    pdf.set_font("Helvetica", "B", size)
    pdf.set_xy(x, y)
    pdf.cell(w, h, text, align="C")


def cover_page(pdf):
    pdf.add_page()

    # Header hero
    draw_rect_filled(pdf, 0, 0, 210, 80, NAVY)

    pdf.set_text_color(*WHITE)
    pdf.set_font("Helvetica", "B", 32)
    pdf.set_xy(15, 22)
    pdf.cell(180, 12, "PLAN FEDE")

    pdf.set_font("Helvetica", "", 18)
    pdf.set_xy(15, 38)
    pdf.cell(180, 8, "Dieta con deficit de 500 kcal · Sin cena")

    pdf.set_font("Helvetica", "", 12)
    pdf.set_xy(15, 55)
    pdf.cell(180, 6, "Vigente desde: 2026-09-11 · Revision: cada 4 semanas")

    # Cuadro resumen
    y0 = 100
    draw_rect_filled(pdf, 15, y0, 180, 60, GRAY_LIGHT)

    pdf.set_text_color(*NAVY)
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_xy(20, y0 + 6)
    pdf.cell(170, 8, "RESUMEN DEL PLAN")

    pdf.set_font("Helvetica", "", 12)
    pdf.set_text_color(*SLATE)

    resumen = [
        ("Objetivo diario", "~1750-1900 kcal (deficit 500 sobre plan anterior)"),
        ("Proteina", "~180-190 g / dia (mantener masa muscular)"),
        ("Comidas", "4-5 comidas hasta las 16:30"),
        ("Ultima comida solida", "16:30 (merienda-cena)"),
        ("Snack ancla nocturno", "100 kcal opcional a las 21:30"),
        ("Ayuno nocturno", "13-14 horas"),
    ]

    y = y0 + 18
    for label, valor in resumen:
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(*NAVY)
        pdf.set_xy(20, y)
        pdf.cell(55, 6, label + ":")

        pdf.set_font("Helvetica", "", 11)
        pdf.set_text_color(*SLATE)
        pdf.set_xy(75, y)
        pdf.cell(115, 6, valor)
        y += 7

    # Semana en un vistazo
    y0 = 175
    pdf.set_text_color(*NAVY)
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_xy(15, y0)
    pdf.cell(180, 8, "LA SEMANA EN UN VISTAZO")

    y = y0 + 12
    for dia, info in PLAN.items():
        color = DIAS_COLOR[dia]
        # Barrita de color
        draw_rect_filled(pdf, 15, y, 4, 10, color)
        # Fondo card
        draw_rect_filled(pdf, 19, y, 176, 10, GRAY_LIGHT)

        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(*NAVY)
        pdf.set_xy(22, y + 2)
        pdf.cell(35, 6, dia)

        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(*SLATE)
        pdf.set_xy(57, y + 2)
        pdf.cell(90, 6, info["subtitulo"])

        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(*NAVY)
        pdf.set_xy(147, y + 2)
        pdf.cell(48, 6, f"{info['kcal_total']} kcal · {info['prot_total']}g prot")

        y += 12


def day_page(pdf, dia, info):
    pdf.add_page()

    color = DIAS_COLOR[dia]

    # Header hero del día
    draw_rect_filled(pdf, 0, 0, 210, 45, color)

    pdf.set_text_color(*WHITE)
    pdf.set_font("Helvetica", "B", 26)
    pdf.set_xy(15, 12)
    pdf.cell(180, 10, dia)

    pdf.set_font("Helvetica", "", 14)
    pdf.set_xy(15, 25)
    pdf.cell(180, 6, info["subtitulo"])

    # Badges totales con borde blanco sobre color
    pdf.set_draw_color(255, 255, 255)
    pdf.set_line_width(0.4)
    pdf.rect(130, 12, 30, 10, style="D")
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(*WHITE)
    pdf.set_xy(130, 12)
    pdf.cell(30, 10, f"{info['kcal_total']} kcal", align="C")

    pdf.rect(163, 12, 32, 10, style="D")
    pdf.set_xy(163, 12)
    pdf.cell(32, 10, f"{info['prot_total']}g proteina", align="C")

    # Comidas
    y = 55
    for comida in info["comidas"]:
        # Card
        card_h = 6 + 6 + (len(comida["ingredientes"]) * 5) + 5
        if y + card_h > 280:  # nueva página si no entra
            pdf.add_page()
            y = 20

        # Sombra sutil (rectangulo gris claro desplazado)
        # Fondo card
        draw_rect_filled(pdf, 15, y, 180, card_h, WHITE)
        # Borde
        pdf.set_draw_color(*GRAY_MID)
        pdf.set_line_width(0.3)
        pdf.rect(15, y, 180, card_h, style="D")

        # Barrita de color a la izquierda
        draw_rect_filled(pdf, 15, y, 3, card_h, color)

        # Header interno de la card
        # Hora
        pdf.set_text_color(*NAVY)
        pdf.set_font("Helvetica", "B", 14)
        pdf.set_xy(22, y + 3)
        pdf.cell(25, 7, comida["hora"])

        # Nombre
        pdf.set_font("Helvetica", "B", 13)
        pdf.set_text_color(*NAVY)
        pdf.set_xy(48, y + 3)
        pdf.cell(90, 7, comida["nombre"])

        # Badges kcal y prot (solo si hay valores)
        if comida["kcal"] > 0 or comida["prot"] > 0:
            # kcal
            draw_rect_filled(pdf, 140, y + 3, 25, 7, color)
            pdf.set_text_color(*WHITE)
            pdf.set_font("Helvetica", "B", 10)
            pdf.set_xy(140, y + 3)
            pdf.cell(25, 7, f"{comida['kcal']} kcal", align="C")
            # prot
            draw_rect_filled(pdf, 168, y + 3, 22, 7, NAVY)
            pdf.set_xy(168, y + 3)
            pdf.cell(22, 7, f"{comida['prot']}g p", align="C")

        # Línea separadora sutil
        pdf.set_draw_color(*GRAY_MID)
        pdf.set_line_width(0.2)
        pdf.line(22, y + 12, 188, y + 12)

        # Ingredientes
        pdf.set_text_color(*SLATE)
        pdf.set_font("Helvetica", "", 11)
        ing_y = y + 14
        for ing in comida["ingredientes"]:
            pdf.set_xy(22, ing_y)
            pdf.cell(5, 5, "-")
            pdf.set_xy(28, ing_y)
            pdf.cell(160, 5, ing)
            ing_y += 5

        y += card_h + 3


def notes_page(pdf):
    pdf.add_page()

    # Header
    draw_rect_filled(pdf, 0, 0, 210, 40, NAVY)
    pdf.set_text_color(*WHITE)
    pdf.set_font("Helvetica", "B", 22)
    pdf.set_xy(15, 15)
    pdf.cell(180, 10, "REGLAS Y NOTAS")

    y = 50

    secciones = [
        ("BEBIDAS PERMITIDAS entre 13:30 y 22:00", [
            "Agua (2-3 vasos entre almuerzo y cena, uno antes de dormir)",
            "Mate cocido descafeinado",
            "Infusiones: manzanilla, tilo, hierbabuena, boldo, cedron, poleo",
            "Agua saborizada casera (agua + limon + menta + jengibre)",
            "Cafe descafeinado",
        ], GREEN),
        ("PROHIBIDO", [
            "Cualquier bebida con cafeina despues de las 13:30 (mate, cafe, te)",
            "Alcohol (obligatorio esta etapa por insomnio + apnea)",
            "Snacks entre horas (nueces, frutas, galletitas)",
            "Zero light / edulcorantes en exceso",
            "Cenar despues de las 17:00 (mueve todo)",
        ], ORANGE),
        ("REGLAS DE ORO", [
            "Ultima comida solida: 16:30 - no negociable",
            "Snack ancla 21:30 es opcional (si tenes hambre real)",
            "Suplementos: Vit D3 + Omega-3 diarios, Creatina 5g diarios",
            "Magnesio glicinato 300 mg todas las noches (para sueno)",
            "Hidratacion: 2,5-3 L agua/dia (mas los dias de gym)",
            "Sal: pizca en el vaso de agua de 05:30 (electrolitos)",
        ], NAVY),
        ("REVISION Y PROGRESION", [
            "Semana 1: tolerancia - aguantas el vacio nocturno?",
            "Semana 2: adherencia - estas cumpliendo?",
            "Semana 4: pesada y medicion (peso, cintura, cadera)",
            "Semana 8: revision completa y ajuste",
            "Perdida esperada: 800 g a 1 kg / semana",
        ], NAVY),
    ]

    for titulo, items, color in secciones:
        # Titulo con barrita
        draw_rect_filled(pdf, 15, y, 4, 8, color)
        pdf.set_text_color(*NAVY)
        pdf.set_font("Helvetica", "B", 13)
        pdf.set_xy(22, y + 1)
        pdf.cell(170, 6, titulo)
        y += 12

        pdf.set_font("Helvetica", "", 11)
        pdf.set_text_color(*SLATE)
        for item in items:
            pdf.set_xy(22, y)
            pdf.cell(5, 5, "-")
            pdf.set_xy(28, y)
            pdf.cell(160, 5, item)
            y += 6
        y += 4

    # Footer motivacional
    if y < 260:
        draw_rect_filled(pdf, 15, y + 5, 180, 25, GRAY_LIGHT)
        pdf.set_text_color(*NAVY)
        pdf.set_font("Helvetica", "B", 13)
        pdf.set_xy(20, y + 10)
        pdf.cell(170, 6, "Recorda:")
        pdf.set_font("Helvetica", "", 11)
        pdf.set_text_color(*SLATE)
        pdf.set_xy(20, y + 18)
        pdf.cell(170, 6, "8 semanas de constancia hoy = mas anos de vida y salud manana. Vas bien.")


def main():
    pdf = PDF()
    cover_page(pdf)
    for dia, info in PLAN.items():
        day_page(pdf, dia, info)
    notes_page(pdf)
    pdf.output(str(OUT))
    print(f"OK: {OUT}")


if __name__ == "__main__":
    main()
