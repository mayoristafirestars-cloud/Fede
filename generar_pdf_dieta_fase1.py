#!/usr/bin/env python3
"""PDF de la Dieta Fase 1 (Consolidación) — Fede.

45 días · 20/9 a 4/11 · ~1800 kcal · 190g proteína
Timing ajustado: gym 07:00-08:15, desayuno portátil en el negocio.
"""
from fpdf import FPDF
from pathlib import Path

OUT = Path("/home/user/Fede/Plan-Fede-Dieta-Fase1.pdf")

# Paleta base
NAVY = (30, 41, 59)
SLATE = (71, 85, 105)
GRAY_LIGHT = (241, 245, 249)
GRAY_MID = (203, 213, 225)
WHITE = (255, 255, 255)
GREEN = (34, 197, 94)
ORANGE = (249, 115, 22)
RED = (239, 68, 68)

# Paleta por día
DIAS_COLOR = {
    "LUNES":     (59, 130, 246),
    "MARTES":    (16, 185, 129),
    "MIÉRCOLES": (245, 158, 11),
    "JUEVES":    (168, 85, 247),
    "VIERNES":   (239, 68, 68),
    "SÁBADO":    (14, 165, 233),
    "DOMINGO":   (139, 92, 246),
}

PLAN = {
    "LUNES": {
        "subtitulo": "Gym Superior A · Desayuno portátil en el negocio",
        "kcal_total": 1900,
        "prot_total": 190,
        "comidas": [
            {"hora": "06:00", "nombre": "Despertar + agua matinal",
             "kcal": 0, "prot": 0,
             "ingredientes": ["300 ml agua", "pizca de sal marina"]},
            {"hora": "06:03", "nombre": "Respiración + estiramiento",
             "kcal": 0, "prot": 0,
             "ingredientes": ["Respiración 4-7-8 · 2 min", "estiramiento suave 3 min"]},
            {"hora": "06:30", "nombre": "Pre-entreno",
             "kcal": 70, "prot": 1,
             "ingredientes": ["80 g banana (media)", "café 150 ml", "agua con sal 300 ml"]},
            {"hora": "07:00", "nombre": "Gym Superior A",
             "kcal": 0, "prot": 0,
             "ingredientes": ["Cadenas + core entre series", "Duración 55-60 min"]},
            {"hora": "08:20", "nombre": "Post-entreno (en shaker)",
             "kcal": 200, "prot": 27,
             "ingredientes": ["35 g whey", "5 g creatina", "80 g banana chica"]},
            {"hora": "09:00", "nombre": "DESAYUNO PORTÁTIL en el negocio",
             "kcal": 545, "prot": 32,
             "ingredientes": ["4 huevos duros", "70 g palta",
                              "100 g tomate", "20 g queso port salut descremado",
                              "5 ml oliva"]},
            {"hora": "09:15", "nombre": "Suplementos",
             "kcal": 0, "prot": 0,
             "ingredientes": ["Vit D3", "Omega-3", "L-Glutamina 5 g"]},
            {"hora": "10:30", "nombre": "Hidratación",
             "kcal": 0, "prot": 0,
             "ingredientes": ["500 ml agua con limón"]},
            {"hora": "12:30", "nombre": "Almuerzo · Pollo grillado",
             "kcal": 620, "prot": 82,
             "ingredientes": ["250 g pollo grillado",
                              "80 g papa hervida",
                              "200 g ensalada mixta (hojas + tomate + zanahoria + pepino)",
                              "40 g palta", "10 ml oliva + limón"]},
            {"hora": "13:05", "nombre": "Box breathing 3 min",
             "kcal": 0, "prot": 0,
             "ingredientes": ["4 inhalo · 4 retengo · 4 exhalo · 4 pausa"]},
            {"hora": "13:15", "nombre": "Caminata 10 min",
             "kcal": 0, "prot": 0,
             "ingredientes": ["Zona 2 tranquila, al aire libre si podés"]},
            {"hora": "13:30", "nombre": "Último mate del día",
             "kcal": 0, "prot": 0,
             "ingredientes": ["Sin azúcar · después: infusiones sin cafeína"]},
            {"hora": "15:00", "nombre": "Hidratación",
             "kcal": 0, "prot": 0,
             "ingredientes": ["500 ml agua"]},
            {"hora": "16:30", "nombre": "Merienda-cena · Yogur y huevos",
             "kcal": 380, "prot": 37,
             "ingredientes": ["200 g yogur griego natural (sin azúcar)",
                              "2 huevos duros", "12 g nueces",
                              "10 g chía", "canela"]},
            {"hora": "21:00", "nombre": "Journal + gratitud (2 min)",
             "kcal": 0, "prot": 0,
             "ingredientes": ["3 cosas del día + 1 gratitud"]},
            {"hora": "21:30", "nombre": "Snack ancla MÍNIMO (opcional)",
             "kcal": 85, "prot": 11,
             "ingredientes": ["100 g yogur griego natural",
                              "5 g chía", "magnesio 300 mg"]},
            {"hora": "21:45", "nombre": "Meditación 10 min",
             "kcal": 0, "prot": 0,
             "ingredientes": ["App: Calm / Insight Timer / YouTube"]},
            {"hora": "22:00", "nombre": "A dormir",
             "kcal": 0, "prot": 0,
             "ingredientes": ["Celular afuera del cuarto", "cuarto 18-20°C"]},
        ]
    },
    "MARTES": {
        "subtitulo": "Gym Inferior A · Desayuno portátil en el negocio",
        "kcal_total": 1965,
        "prot_total": 195,
        "comidas": [
            {"hora": "06:00", "nombre": "Despertar + agua matinal",
             "kcal": 0, "prot": 0,
             "ingredientes": ["300 ml agua", "pizca de sal marina"]},
            {"hora": "06:03", "nombre": "Respiración + estiramiento",
             "kcal": 0, "prot": 0,
             "ingredientes": ["2 + 3 min"]},
            {"hora": "06:30", "nombre": "Pre-entreno",
             "kcal": 90, "prot": 1,
             "ingredientes": ["30 g pasas de uva", "café 150 ml", "agua con sal 300 ml"]},
            {"hora": "07:00", "nombre": "Gym Inferior A",
             "kcal": 0, "prot": 0,
             "ingredientes": ["Cadenas + core entre series", "Duración 60-65 min"]},
            {"hora": "08:20", "nombre": "Post-entreno (en shaker)",
             "kcal": 200, "prot": 27,
             "ingredientes": ["35 g whey", "5 g creatina", "80 g banana chica"]},
            {"hora": "09:00", "nombre": "DESAYUNO PORTÁTIL · Tortilla con jamón",
             "kcal": 565, "prot": 34,
             "ingredientes": ["Tortilla de 3 huevos + 20 g queso rallado descremado",
                              "30 g jamón cocido magro", "70 g palta",
                              "100 g tomate", "5 ml oliva"]},
            {"hora": "09:15", "nombre": "Suplementos",
             "kcal": 0, "prot": 0,
             "ingredientes": ["Vit D3", "Omega-3", "L-Glutamina 5 g"]},
            {"hora": "10:30", "nombre": "Hidratación",
             "kcal": 0, "prot": 0,
             "ingredientes": ["500 ml agua"]},
            {"hora": "12:30", "nombre": "Almuerzo · Milanesas al horno",
             "kcal": 640, "prot": 82,
             "ingredientes": ["250 g milanesas de pollo al horno",
                              "(rebozado: 15 g harina de almendras + 1 huevo)",
                              "80 g boniato al horno",
                              "200 g ensalada verde con rúcula",
                              "40 g palta", "10 ml oliva + limón"]},
            {"hora": "13:05", "nombre": "Box breathing 3 min",
             "kcal": 0, "prot": 0,
             "ingredientes": ["4-4-4-4"]},
            {"hora": "13:15", "nombre": "Caminata 10 min", "kcal": 0, "prot": 0,
             "ingredientes": ["Zona 2 tranquila"]},
            {"hora": "13:30", "nombre": "Último mate", "kcal": 0, "prot": 0,
             "ingredientes": ["Sin azúcar"]},
            {"hora": "15:00", "nombre": "Hidratación", "kcal": 0, "prot": 0,
             "ingredientes": ["500 ml agua"]},
            {"hora": "16:30", "nombre": "Merienda-cena · Cottage con frutillas",
             "kcal": 385, "prot": 40,
             "ingredientes": ["200 g cottage", "2 huevos duros",
                              "30 g frutillas", "10 g nueces",
                              "10 g chía", "canela"]},
            {"hora": "21:30", "nombre": "Snack ancla mínimo (opcional)",
             "kcal": 85, "prot": 11,
             "ingredientes": ["100 g yogur griego", "5 g chía", "Mg 300 mg"]},
            {"hora": "22:00", "nombre": "A dormir", "kcal": 0, "prot": 0,
             "ingredientes": ["Sin pantallas 30 min antes"]},
        ]
    },
    "MIÉRCOLES": {
        "subtitulo": "Descanso · Bici Zona 2",
        "kcal_total": 1820,
        "prot_total": 170,
        "comidas": [
            {"hora": "06:00", "nombre": "Despertar + agua matinal", "kcal": 0, "prot": 0,
             "ingredientes": ["300 ml + sal"]},
            {"hora": "06:15", "nombre": "Desayuno · Ricota mediterránea",
             "kcal": 555, "prot": 33,
             "ingredientes": ["100 g ricota descremada batida con orégano/albahaca",
                              "2 huevos poché", "60 g palta",
                              "100 g tomate", "10 g semillas mixtas (sésamo + girasol + lino)",
                              "5 ml oliva"]},
            {"hora": "06:20", "nombre": "Suplementos",
             "kcal": 0, "prot": 0,
             "ingredientes": ["Vit D3", "Omega-3", "Creatina 5 g", "L-Glutamina 5 g"]},
            {"hora": "09:30", "nombre": "Media mañana · Bowl con arándanos",
             "kcal": 250, "prot": 22,
             "ingredientes": ["200 g yogur griego natural",
                              "10 g nueces", "20 g arándanos"]},
            {"hora": "10:30", "nombre": "Hidratación", "kcal": 0, "prot": 0,
             "ingredientes": ["500 ml agua"]},
            {"hora": "12:30", "nombre": "Almuerzo · Ensalada de atún",
             "kcal": 610, "prot": 72,
             "ingredientes": ["180 g atún al natural", "2 huevos duros",
                              "150 g espinaca salteada al vapor",
                              "30 g queso port salut", "40 g palta",
                              "12 ml oliva + limón"]},
            {"hora": "13:00", "nombre": "Bici Zona 2 · 40 min",
             "kcal": 0, "prot": 0,
             "ingredientes": ["FC 105-118 lpm", "ruta plana"]},
            {"hora": "13:30", "nombre": "Último mate", "kcal": 0, "prot": 0,
             "ingredientes": ["Sin azúcar"]},
            {"hora": "15:00", "nombre": "Hidratación", "kcal": 0, "prot": 0,
             "ingredientes": ["500 ml agua"]},
            {"hora": "16:30", "nombre": "Merienda-cena · Sardinas con palta",
             "kcal": 320, "prot": 32,
             "ingredientes": ["100 g sardinas al natural (drenadas)",
                              "50 g palta", "100 g tomate",
                              "10 g aceitunas negras", "10 g chía",
                              "5 ml oliva + limón"]},
            {"hora": "21:30", "nombre": "Snack ancla mínimo (opcional)",
             "kcal": 85, "prot": 11,
             "ingredientes": ["100 g yogur griego", "5 g chía", "Mg 300 mg"]},
        ]
    },
    "JUEVES": {
        "subtitulo": "Gym Superior B · Desayuno portátil en el negocio",
        "kcal_total": 1785,
        "prot_total": 192,
        "comidas": [
            {"hora": "06:00", "nombre": "Despertar + agua matinal", "kcal": 0, "prot": 0,
             "ingredientes": ["300 ml + sal"]},
            {"hora": "06:03", "nombre": "Respiración + estiramiento",
             "kcal": 0, "prot": 0,
             "ingredientes": ["2 + 3 min"]},
            {"hora": "06:30", "nombre": "Pre-entreno",
             "kcal": 70, "prot": 1,
             "ingredientes": ["80 g banana (media)", "café", "agua con sal"]},
            {"hora": "07:00", "nombre": "Gym Superior B",
             "kcal": 0, "prot": 0,
             "ingredientes": ["Cadenas + core entre series", "Duración 55-60 min"]},
            {"hora": "08:20", "nombre": "Post-entreno (en shaker)",
             "kcal": 200, "prot": 27,
             "ingredientes": ["35 g whey", "5 g creatina", "80 g banana chica"]},
            {"hora": "09:00", "nombre": "DESAYUNO PORTÁTIL · Yogur bowl",
             "kcal": 490, "prot": 40,
             "ingredientes": ["200 g yogur griego natural",
                              "100 g frutillas", "15 g almendras",
                              "canela", "3 huevos duros aparte"]},
            {"hora": "09:15", "nombre": "Suplementos", "kcal": 0, "prot": 0,
             "ingredientes": ["Vit D3", "Omega-3", "L-Glutamina 5 g"]},
            {"hora": "10:30", "nombre": "Hidratación", "kcal": 0, "prot": 0,
             "ingredientes": ["500 ml agua"]},
            {"hora": "12:30", "nombre": "Almuerzo · Pollo mostaza y limón",
             "kcal": 620, "prot": 82,
             "ingredientes": ["250 g pollo (marinado mostaza + limón + oliva)",
                              "80 g papa al horno",
                              "150 g ensalada nicoise (hojas + tomate + 1 huevo duro)",
                              "40 g palta", "10 ml oliva"]},
            {"hora": "13:05", "nombre": "Box breathing", "kcal": 0, "prot": 0,
             "ingredientes": ["3 min"]},
            {"hora": "13:15", "nombre": "Caminata 10 min", "kcal": 0, "prot": 0,
             "ingredientes": ["Zona 2 tranquila"]},
            {"hora": "13:30", "nombre": "Último mate", "kcal": 0, "prot": 0,
             "ingredientes": ["Sin azúcar"]},
            {"hora": "15:00", "nombre": "Hidratación", "kcal": 0, "prot": 0,
             "ingredientes": ["500 ml agua"]},
            {"hora": "16:30", "nombre": "Merienda-cena · Tabla mediterránea",
             "kcal": 390, "prot": 32,
             "ingredientes": ["60 g queso feta o port salut",
                              "60 g pavita fiambre magra",
                              "15 g aceitunas negras", "80 g tomate cherry",
                              "40 g palta", "10 g nueces", "10 g chía"]},
            {"hora": "21:30", "nombre": "Snack ancla mínimo (opcional)",
             "kcal": 85, "prot": 11,
             "ingredientes": ["100 g yogur griego", "5 g chía", "Mg 300 mg"]},
        ]
    },
    "VIERNES": {
        "subtitulo": "Gym Inferior B (tarde 13:30)",
        "kcal_total": 1805,
        "prot_total": 166,
        "comidas": [
            {"hora": "05:30", "nombre": "Agua matinal", "kcal": 0, "prot": 0,
             "ingredientes": ["400 ml + sal"]},
            {"hora": "06:15", "nombre": "Desayuno · Omelette con espinaca",
             "kcal": 570, "prot": 35,
             "ingredientes": ["Omelette de 4 huevos + 100 g espinaca salteada",
                              "30 g queso descremado", "70 g palta",
                              "100 g tomate", "5 ml oliva"]},
            {"hora": "06:20", "nombre": "Suplementos", "kcal": 0, "prot": 0,
             "ingredientes": ["Vit D3", "Omega-3", "L-Glutamina 5 g"]},
            {"hora": "10:00", "nombre": "Media mañana",
             "kcal": 240, "prot": 20,
             "ingredientes": ["200 g yogur griego natural",
                              "10 g nueces", "30 g frutillas"]},
            {"hora": "10:30", "nombre": "Hidratación", "kcal": 0, "prot": 0,
             "ingredientes": ["500 ml agua"]},
            {"hora": "12:00", "nombre": "Pre-entreno LIVIANO",
             "kcal": 90, "prot": 1,
             "ingredientes": ["30 g pasas", "café", "agua con sal 400 ml",
                              "NO comer sólido pesado 11-14 h"]},
            {"hora": "13:30", "nombre": "Gym Inferior B",
             "kcal": 0, "prot": 0,
             "ingredientes": ["Trap bar + Hip thrust + Búlgara", "Duración 55-60 min"]},
            {"hora": "14:45", "nombre": "Post-entreno (en shaker)",
             "kcal": 200, "prot": 27,
             "ingredientes": ["35 g whey", "5 g creatina", "80 g banana"]},
            {"hora": "15:30", "nombre": "Almuerzo-merienda · Bowl con quinoa",
             "kcal": 620, "prot": 72,
             "ingredientes": ["220 g pollo grillado",
                              "60 g quinoa cocida (20 g seco)",
                              "200 g ensalada verde con rúcula",
                              "50 g palta", "10 g almendras",
                              "10 ml oliva + limón"]},
            {"hora": "17:00", "nombre": "Micro-pausa 3 min", "kcal": 0, "prot": 0,
             "ingredientes": ["Lejos del celular", "cuello + hombros"]},
            {"hora": "21:30", "nombre": "Snack ancla mínimo (opcional)",
             "kcal": 85, "prot": 11,
             "ingredientes": ["100 g yogur griego", "5 g chía", "Mg 300 mg"]},
        ]
    },
    "SÁBADO": {
        "subtitulo": "Descanso · Bici Zona 2",
        "kcal_total": 1795,
        "prot_total": 177,
        "comidas": [
            {"hora": "06:00", "nombre": "Despertar + agua matinal", "kcal": 0, "prot": 0,
             "ingredientes": ["300 ml + sal"]},
            {"hora": "06:15", "nombre": "Desayuno · Revueltos con jamón",
             "kcal": 505, "prot": 32,
             "ingredientes": ["3 huevos revueltos (con 3 ml oliva)",
                              "30 g jamón cocido magro",
                              "30 g queso port salut", "50 g palta",
                              "100 g tomate"]},
            {"hora": "06:20", "nombre": "Suplementos", "kcal": 0, "prot": 0,
             "ingredientes": ["Vit D3", "Omega-3", "Creatina 5 g", "L-Glutamina"]},
            {"hora": "09:30", "nombre": "Media mañana · Cottage con frutillas",
             "kcal": 240, "prot": 26,
             "ingredientes": ["200 g cottage", "50 g frutillas",
                              "7 g nueces", "canela", "5 g chía"]},
            {"hora": "10:30", "nombre": "Hidratación", "kcal": 0, "prot": 0,
             "ingredientes": ["500 ml agua"]},
            {"hora": "12:30", "nombre": "Almuerzo · Wok de pollo",
             "kcal": 625, "prot": 78,
             "ingredientes": ["250 g pollo en cubos (soja baja sodio 5 ml + jengibre + ajo)",
                              "150 g brócoli al vapor",
                              "100 g zapallo hervido", "40 g palta",
                              "5 g semillas de sésamo", "10 ml oliva"]},
            {"hora": "13:00", "nombre": "Bici Zona 2 · 40 min",
             "kcal": 0, "prot": 0,
             "ingredientes": ["FC 105-118 lpm"]},
            {"hora": "13:30", "nombre": "Último mate", "kcal": 0, "prot": 0,
             "ingredientes": ["Sin azúcar"]},
            {"hora": "15:00", "nombre": "Hidratación", "kcal": 0, "prot": 0,
             "ingredientes": ["500 ml agua"]},
            {"hora": "16:30", "nombre": "Merienda-cena · Sardinas gourmet",
             "kcal": 340, "prot": 30,
             "ingredientes": ["120 g sardinas al natural", "50 g palta",
                              "80 g tomate cherry",
                              "1 galleta de arroz integral (10 g)",
                              "10 g chía", "5 ml oliva + limón"]},
            {"hora": "21:30", "nombre": "Snack ancla mínimo (opcional)",
             "kcal": 85, "prot": 11,
             "ingredientes": ["100 g yogur griego", "5 g chía", "Mg 300 mg"]},
        ]
    },
    "DOMINGO": {
        "subtitulo": "Descanso · Bici Zona 2 · BATCH COOKING",
        "kcal_total": 1635,
        "prot_total": 187,
        "comidas": [
            {"hora": "06:00", "nombre": "Despertar + agua matinal", "kcal": 0, "prot": 0,
             "ingredientes": ["300 ml + sal"]},
            {"hora": "06:15", "nombre": "Desayuno · Huevos poché con feta",
             "kcal": 510, "prot": 30,
             "ingredientes": ["3 huevos poché", "60 g palta",
                              "100 g tomate",
                              "30 g queso feta o cottage",
                              "10 g semillas mixtas", "5 ml oliva"]},
            {"hora": "06:20", "nombre": "Suplementos", "kcal": 0, "prot": 0,
             "ingredientes": ["Vit D3", "Omega-3", "Creatina 5 g", "L-Glutamina"]},
            {"hora": "09:30", "nombre": "BATCH COOKING · 1 h",
             "kcal": 0, "prot": 0,
             "ingredientes": ["1,8 kg pollo al horno con hierbas",
                              "20 huevos duros",
                              "Papas y boniatos hervidos",
                              "Verduras al vapor variadas",
                              "Armar 5 tuppers desayuno portátil (Lun/Mar/Jue)"]},
            {"hora": "12:30", "nombre": "Almuerzo · Pollo del horno",
             "kcal": 660, "prot": 78,
             "ingredientes": ["250 g pollo del batch",
                              "200 g ensalada completa",
                              "60 g palta", "10 g aceitunas",
                              "10 g nueces", "12 ml oliva + limón"]},
            {"hora": "13:30", "nombre": "Último mate", "kcal": 0, "prot": 0,
             "ingredientes": ["Sin azúcar"]},
            {"hora": "14:00", "nombre": "Bici Zona 2 · 40 min",
             "kcal": 0, "prot": 0,
             "ingredientes": ["FC 105-118 · al sol"]},
            {"hora": "15:00", "nombre": "Hidratación", "kcal": 0, "prot": 0,
             "ingredientes": ["500 ml agua"]},
            {"hora": "16:30", "nombre": "Merienda-cena · Atún con palta",
             "kcal": 380, "prot": 38,
             "ingredientes": ["120 g atún al natural", "50 g palta",
                              "100 g tomate", "1 huevo duro",
                              "10 g aceitunas", "10 g chía",
                              "5 ml oliva + limón"]},
            {"hora": "21:30", "nombre": "Snack ancla mínimo (opcional)",
             "kcal": 85, "prot": 11,
             "ingredientes": ["100 g yogur griego", "5 g chía", "Mg 300 mg",
                              "Cargar tensiómetro para el lunes"]},
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


def cover_page(pdf):
    pdf.add_page()

    draw_rect_filled(pdf, 0, 0, 210, 90, NAVY)

    pdf.set_text_color(*WHITE)
    pdf.set_font("Helvetica", "B", 32)
    pdf.set_xy(15, 20)
    pdf.cell(180, 12, "PLAN FEDE")

    pdf.set_font("Helvetica", "", 18)
    pdf.set_xy(15, 36)
    pdf.cell(180, 8, "Dieta Fase 1 - Consolidacion")

    pdf.set_font("Helvetica", "", 12)
    pdf.set_xy(15, 55)
    pdf.cell(180, 6, "45 dias · 20/9 a 4/11 · Sin cena · Anti-inflamatorio")
    pdf.set_xy(15, 63)
    pdf.cell(180, 6, "Timing gym 07:00-08:15 + desayuno portatil en el negocio")

    y0 = 105
    draw_rect_filled(pdf, 15, y0, 180, 68, GRAY_LIGHT)

    pdf.set_text_color(*NAVY)
    pdf.set_font("Helvetica", "B", 15)
    pdf.set_xy(20, y0 + 6)
    pdf.cell(170, 8, "OBJETIVOS")

    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(*SLATE)

    resumen = [
        ("Peso inicial", "103 kg a objetivo 98 kg al 4/11 (bajar 5 kg)"),
        ("Kcal diarias", "~1800 kcal (deficit 500 aprox sobre TDEE 2900)"),
        ("Proteina", "~190 g / dia (mantener masa muscular)"),
        ("Comidas", "4-5 hasta 16:30 + snack ancla minimo 21:30"),
        ("Ayuno nocturno", "13-14 horas (16:30 a 06:00 dia siguiente)"),
        ("Perdida esperada", "800 g - 1 kg / semana"),
    ]

    y = y0 + 18
    for label, valor in resumen:
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(*NAVY)
        pdf.set_xy(20, y)
        pdf.cell(50, 6, label + ":")
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(*SLATE)
        pdf.set_xy(70, y)
        pdf.cell(120, 6, valor)
        y += 7

    y0 = 185
    pdf.set_text_color(*NAVY)
    pdf.set_font("Helvetica", "B", 15)
    pdf.set_xy(15, y0)
    pdf.cell(180, 8, "LA SEMANA")

    y = y0 + 12
    for dia, info in PLAN.items():
        color = DIAS_COLOR[dia]
        draw_rect_filled(pdf, 15, y, 4, 10, color)
        draw_rect_filled(pdf, 19, y, 176, 10, GRAY_LIGHT)

        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(*NAVY)
        pdf.set_xy(22, y + 2)
        pdf.cell(30, 6, dia)

        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(*SLATE)
        pdf.set_xy(52, y + 2)
        pdf.cell(105, 6, info["subtitulo"])

        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(*NAVY)
        pdf.set_xy(157, y + 2)
        pdf.cell(38, 6, f"{info['kcal_total']} kcal · {info['prot_total']}g")

        y += 12


def day_page(pdf, dia, info):
    pdf.add_page()
    color = DIAS_COLOR[dia]

    draw_rect_filled(pdf, 0, 0, 210, 28, color)

    pdf.set_text_color(*WHITE)
    pdf.set_font("Helvetica", "B", 22)
    pdf.set_xy(15, 6)
    pdf.cell(120, 9, dia)

    pdf.set_font("Helvetica", "", 12)
    pdf.set_xy(15, 17)
    pdf.cell(120, 6, info["subtitulo"])

    pdf.set_draw_color(255, 255, 255)
    pdf.set_line_width(0.4)
    pdf.rect(130, 7, 30, 8, style="D")
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(*WHITE)
    pdf.set_xy(130, 7)
    pdf.cell(30, 8, f"{info['kcal_total']} kcal", align="C")

    pdf.rect(163, 7, 32, 8, style="D")
    pdf.set_xy(163, 7)
    pdf.cell(32, 8, f"{info['prot_total']}g proteina", align="C")

    y = 33
    for comida in info["comidas"]:
        ings = " · ".join(comida["ingredientes"])

        chars_por_linea = 82
        n_lineas = max(1, (len(ings) // chars_por_linea) + (1 if len(ings) % chars_por_linea else 0))
        n_lineas = min(n_lineas, 3)
        if len(ings) > chars_por_linea * 3:
            ings = ings[:chars_por_linea * 3 - 3] + "..."
            n_lineas = 3

        card_h = 10 + (n_lineas * 4.2) + 2

        if y + card_h > 280:
            pdf.add_page()
            y = 20

        draw_rect_filled(pdf, 15, y, 180, card_h, WHITE)
        pdf.set_draw_color(*GRAY_MID)
        pdf.set_line_width(0.2)
        pdf.rect(15, y, 180, card_h, style="D")
        draw_rect_filled(pdf, 15, y, 3, card_h, color)

        pdf.set_text_color(*NAVY)
        pdf.set_font("Helvetica", "B", 12)
        pdf.set_xy(21, y + 2)
        pdf.cell(20, 6, comida["hora"])

        pdf.set_font("Helvetica", "B", 11)
        pdf.set_xy(43, y + 2)
        pdf.cell(95, 6, comida["nombre"])

        if comida["kcal"] > 0 or comida["prot"] > 0:
            draw_rect_filled(pdf, 140, y + 2, 24, 6, color)
            pdf.set_text_color(*WHITE)
            pdf.set_font("Helvetica", "B", 9)
            pdf.set_xy(140, y + 2)
            pdf.cell(24, 6, f"{comida['kcal']} kcal", align="C")

            draw_rect_filled(pdf, 167, y + 2, 22, 6, NAVY)
            pdf.set_xy(167, y + 2)
            pdf.cell(22, 6, f"{comida['prot']}g p", align="C")

        pdf.set_text_color(*SLATE)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_xy(21, y + 9)
        pdf.multi_cell(170, 4.2, ings)

        y += card_h + 1.5


def rules_page(pdf):
    pdf.add_page()

    draw_rect_filled(pdf, 0, 0, 210, 40, NAVY)
    pdf.set_text_color(*WHITE)
    pdf.set_font("Helvetica", "B", 22)
    pdf.set_xy(15, 15)
    pdf.cell(180, 10, "REGLAS DE ORO FASE 1")

    y = 50

    secciones = [
        ("PROHIBIDO 45 DIAS", [
            "CERO azucar anadida (postres, jugos, yogures azucarados)",
            "CERO alcohol (los 45 dias completos)",
            "CERO ultraprocesados (galletitas, snacks, gaseosas)",
            "CERO harinas refinadas (pan blanco, pastas comunes)",
            "CERO cafeina despues de 13:30",
            "CERO edulcorantes artificiales en exceso",
            "CERO comida solida despues de 16:30",
        ], RED),
        ("SI - ANTI-INFLAMATORIO", [
            "Pescado 3 veces por semana (Mar/Mie/Sab)",
            "Fermentados diarios (yogur griego natural sin azucar)",
            "Chia 10-15 g/dia (fibra soluble para microbiota)",
            "Verduras > 400 g/dia (60% cocidas al vapor, 40% crudas)",
            "Ayuno nocturno 13-14 h (16:30 -> 06:00)",
            "Agua 2,5-3 L/dia + electrolitos (sal 05:30, 10:30, 15:00)",
            "Grasas buenas: palta, oliva, pescado, nueces, semillas",
        ], GREEN),
        ("SUPLEMENTACION", [
            "Vitamina D3: 2000-4000 UI/dia (con desayuno)",
            "Omega-3 EPA+DHA: 2 g/dia (con desayuno)",
            "Creatina monohidrato: 5 g/dia (con post-entreno o desayuno)",
            "Magnesio glicinato: 300 mg (21:30, para el sueno)",
            "L-Glutamina: 5 g/dia (con desayuno) - integridad mucosa intestinal",
            "Whey proteina: 35 g post-entreno (Lun/Mar/Jue/Vie)",
        ], NAVY),
        ("BEBIDAS PERMITIDAS 13:30 - 22:00", [
            "Agua (2-3 vasos entre almuerzo y merienda-cena)",
            "Mate cocido descafeinado",
            "Infusiones: manzanilla, tilo, hierbabuena, boldo, cedron, poleo",
            "Agua saborizada casera (agua + limon + menta + jengibre)",
            "Cafe descafeinado",
        ], NAVY),
        ("KIT PORTATIL (Lun/Mar/Jue)", [
            "Preparar el DOMINGO en tuppers para toda la semana",
            "Tupper 1: 4 huevos duros pelados",
            "Tupper 2: palta 70 g + tomate 100 g (con gotas de limon)",
            "Tupper 3: queso port salut 20 g en cubos",
            "Frasquito: 5 ml oliva extra virgen",
            "Shaker gym: whey 35 g + creatina 5 g medidos + banana en mochila",
        ], ORANGE),
        ("REVISION Y PROGRESION", [
            "Semana 1 (20-27/9): tolerancia + arranque",
            "Semana 4 (18/10): remedicion completa (peso, cintura, cadera)",
            "Semana 6 (4/11): fin Fase 1, evaluar a arranca Fase 2 afinamiento",
            "Perdida esperada: 800 g - 1 kg / semana",
        ], NAVY),
    ]

    for titulo, items, color in secciones:
        if y > 250:
            pdf.add_page()
            y = 20

        draw_rect_filled(pdf, 15, y, 4, 8, color)
        pdf.set_text_color(*NAVY)
        pdf.set_font("Helvetica", "B", 12)
        pdf.set_xy(22, y + 1)
        pdf.cell(170, 6, titulo)
        y += 10

        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(*SLATE)
        for item in items:
            pdf.set_xy(22, y)
            pdf.cell(5, 4.5, "-")
            pdf.set_xy(27, y)
            pdf.cell(165, 4.5, item)
            y += 5
        y += 4


def main():
    pdf = PDF()
    cover_page(pdf)
    for dia, info in PLAN.items():
        day_page(pdf, dia, info)
    rules_page(pdf)
    pdf.output(str(OUT))
    print(f"OK: {OUT}")


if __name__ == "__main__":
    main()
