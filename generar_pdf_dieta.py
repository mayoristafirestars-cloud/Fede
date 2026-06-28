#!/usr/bin/env python3
"""Genera Dieta-Fede-Semanal.pdf — version low-carb hardcodeada (rapida y robusta)"""
from pathlib import Path
from fpdf import FPDF
from fpdf.fonts import FontFace

OUT = Path("/home/user/Fede/Dieta-Fede-Semanal.pdf")
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
TEAL = (15, 118, 110)
DARK = (30, 30, 30)
GRAY = (100, 100, 100)


def H2(pdf, text):
    pdf.add_page()
    pdf.set_fill_color(*TEAL)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("DejaVu", "B", 13)
    pdf.cell(0, 9, text, fill=True, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    pdf.set_text_color(*DARK)


def H3(pdf, text):
    if pdf.get_y() > pdf.h - 40:
        pdf.add_page()
    pdf.ln(2)
    pdf.set_font("DejaVu", "B", 11)
    pdf.set_text_color(*TEAL)
    pdf.cell(0, 6, text, new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(*DARK)


def P(pdf, text, size=9, color=DARK, indent=0):
    pdf.set_font("DejaVu", "", size)
    pdf.set_text_color(*color)
    if indent:
        pdf.set_x(pdf.l_margin + indent)
    pdf.multi_cell(pdf.epw - indent, 4.5, text, new_x="LMARGIN", new_y="NEXT")


def table(pdf, rows, col_widths=None):
    pdf.set_font("DejaVu", "", 8)
    kw = {"line_height": 4.5, "text_align": "LEFT",
          "headings_style": FontFace(emphasis="BOLD", color=(255, 255, 255), fill_color=TEAL)}
    if col_widths:
        kw["col_widths"] = col_widths
    with pdf.table(**kw) as t:
        for row in rows:
            tr = t.row()
            for cell in row:
                tr.cell(str(cell))
    pdf.ln(2)


def meal(pdf, hora, nombre, kcal_macro, ingredientes):
    pdf.ln(1)
    pdf.set_font("DejaVu", "B", 10)
    pdf.set_text_color(*DARK)
    pdf.cell(0, 5, f"{hora} — {nombre}", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("DejaVu", "", 8)
    pdf.set_text_color(*GRAY)
    pdf.cell(0, 4, kcal_macro, new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("DejaVu", "", 9)
    pdf.set_text_color(*DARK)
    for ing in ingredientes:
        pdf.set_x(pdf.l_margin + 4)
        pdf.multi_cell(pdf.epw - 4, 4.5, "• " + ing, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(1)


def main():
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.set_margins(15, 15, 15)
    pdf.set_auto_page_break(True, margin=15)
    pdf.add_font("DejaVu", "", FONT_REG)
    pdf.add_font("DejaVu", "B", FONT_BOLD)

    # ===== PORTADA =====
    pdf.add_page()
    pdf.set_fill_color(*TEAL)
    pdf.rect(0, 0, pdf.w, 50, "F")
    pdf.set_y(13)
    pdf.set_font("DejaVu", "B", 24)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 12, "Dieta Low-Carb", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("DejaVu", "", 13)
    pdf.cell(0, 7, "Fede — Mediterranea, 7 dias", align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.ln(18)
    pdf.set_text_color(*DARK)
    pdf.set_font("DejaVu", "B", 11)
    pdf.cell(0, 7, "Datos del plan", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("DejaVu", "", 10)
    datos = [
        ("Tipo", "Low-carb estricto mediterraneo"),
        ("Frecuencia gym", "4 dias/semana (Lun / Mar / Jue / Vie)"),
        ("Carbos dias gym", "~95 g/dia"),
        ("Carbos dias descanso", "~50 g/dia"),
        ("Calorias dias gym", "2.250 kcal"),
        ("Calorias dias descanso", "2.050 kcal"),
        ("Macros dias gym", "P 200 g | C 95 g | G 100 g"),
        ("Macros dias descanso", "P 185 g | C 55 g | G 105 g"),
        ("Huevos", "SIEMPRE hervidos"),
        ("Almidon peri-entreno", "Papa o boniato HERVIDO 100 g"),
        ("Carbos rapidos", "Frutillas + miel (no banana)"),
        ("Hidratacion dia gym", "3,2–3,5 L (con sal)"),
        ("Horario entreno", "Lun/Mar/Jue 07:00 AM | Vie 14:00 hs"),
        ("Comida libre", "Viernes a la noche"),
        ("Vigente desde", "21/04/2026"),
    ]
    for k, v in datos:
        pdf.set_font("DejaVu", "B", 10)
        pdf.cell(55, 6, k, border="B")
        pdf.set_font("DejaVu", "", 10)
        pdf.cell(0, 6, v, border="B", new_x="LMARGIN", new_y="NEXT")

    pdf.ln(5)
    H3(pdf, "Reglas clave de este plan")
    cambios = [
        "HUEVOS: SIEMPRE hervidos. Cero revueltos, omelette, poche.",
        "PAPA O BONIATO: HERVIDO (al agua, sin manteca ni aceite). En los 4 almuerzos de gym.",
        "FRUTILLAS reemplazan a la banana pre y post entreno.",
        "PECHUGA DE POLLO como proteina base (batch cooking domingo).",
        "Carbos peri-entreno: frutillas + miel pre + frutillas post + papa hervida en almuerzo.",
        "Snack nocturno (yogur + chia): no se discute, ancla anti-recaida.",
        "Sumar 2 g de sal extra/dia los primeros 7 dias.",
        "Sumar magnesio glicinato 300 mg/noche desde el dia 1.",
    ]
    for c in cambios:
        P(pdf, "• " + c, indent=4)

    # ===== HIDRATACION =====
    H2(pdf, "Hidratacion (3,2–3,5 L con sal)")
    table(pdf, [
        ["Franja", "Cantidad", "Notas"],
        ["06:15 al despertar", "400 ml", "Vaso grande + pizca de sal (electrolitos)"],
        ["06:45 pre-gym", "300 ml", "Con la banana"],
        ["08:00-09:00 entreno", "600-800 ml", "Sorbos cada 10 min"],
        ["09:30 post-entreno", "300 ml", "Con el batido"],
        ["10:30-13:00", "500 ml", "Entre desayuno y almuerzo"],
        ["13:00 almuerzo", "300 ml", ""],
        ["15:00-19:00", "600 ml", "Incluye mate sin azucar"],
        ["20:30 cena", "200 ml", "Cortar antes para dormir"],
    ])

    # ===== TIMING =====
    H2(pdf, "Estructura del dia (timing)")
    H3(pdf, "Dia de gym (Lun/Mie/Vie)")
    table(pdf, [
        ["Hora", "Momento", "Kcal", "P", "C", "G"],
        ["05:30", "Pre-entreno (frutillas + miel + cafe)", "110", "1", "25", "0"],
        ["07:00", "Entreno (complex 50-60 min)", "—", "—", "—", "—"],
        ["08:15", "Post-entreno (whey + frutillas)", "200", "32", "12", "3"],
        ["09:30", "Desayuno (huevos duros + pan + palta)", "530", "38", "18", "35"],
        ["13:00", "Almuerzo (pollo + papa hervida + ensalada)", "580", "50", "30", "28"],
        ["16:30", "Merienda", "220", "20", "5", "13"],
        ["20:30", "Cena", "470", "45", "8", "28"],
        ["22:00", "Snack nocturno (yogur + chia)", "140", "15", "6", "6"],
        ["TOTAL", "", "~2.250", "~200", "~95", "~100"],
    ])
    H3(pdf, "Dia de descanso")
    table(pdf, [
        ["Hora", "Momento", "Kcal", "P", "C", "G"],
        ["07:30", "Desayuno", "500", "38", "15", "32"],
        ["10:00", "Media manana", "220", "22", "6", "12"],
        ["13:00", "Almuerzo", "550", "50", "10", "33"],
        ["16:30", "Merienda", "220", "20", "5", "13"],
        ["20:30", "Cena", "470", "40", "8", "28"],
        ["22:00", "Snack nocturno", "140", "15", "6", "6"],
        ["TOTAL", "", "~2.050", "~185", "~60", "~105"],
    ])

    # ===== LUNES =====
    H2(pdf, "Lunes — GYM 07:00 (Dia A)")
    meal(pdf, "05:30", "Pre-entreno", "~110 kcal | P 1 / C 25 / G 0",
         ["Frutillas: 200 g",
          "Miel: 10 g (1 cucharadita)",
          "Cafe negro sin azucar: 150 ml",
          "Agua + pizca de sal: 300 ml"])
    meal(pdf, "08:15", "Post-entreno", "~200 kcal | P 32 / C 12 / G 3",
         ["Whey protein: 35 g",
          "Agua: 300 ml",
          "Frutillas: 100 g (licuar todo)"])
    meal(pdf, "09:30", "Desayuno — Plato proteico con huevos duros", "~530 kcal | P 38 / C 18 / G 35",
         ["Huevos DUROS: 3 unidades (150 g)",
          "Pan integral: 30 g (1 rebanada)",
          "Palta: 70 g",
          "Tomate: 100 g rodajas",
          "Queso port salut descremado: 20 g",
          "Aceite oliva: 5 ml (sobre palta y tomate)",
          "Cafe o mate sin azucar"])
    meal(pdf, "13:00", "Almuerzo — Pollo con papa hervida y ensalada", "~580 kcal | P 50 / C 30 / G 28",
         ["Pechuga pollo grille: 220 g (peso COCIDO)",
          "Papa o boniato HERVIDO: 100 g (cocido al agua)",
          "Lechuga: 80 g + rucula 50 g",
          "Tomate: 100 g + pepino 80 g",
          "Palta: 60 g",
          "Aceitunas negras: 20 g (7 unidades)",
          "Aceite oliva: 12 ml + limon + oregano"])
    meal(pdf, "16:30", "Merienda", "~220 kcal | P 20 / C 5 / G 13",
         ["Yogur griego proteico sin azucar: 170 g",
          "Nueces peladas: 12 g (5-6 mitades)",
          "Canela: 1 g"])
    meal(pdf, "20:30", "Cena — Merluza con zapallitos y anchoas", "~470 kcal | P 45 / C 8 / G 28",
         ["Merluza al horno: 200 g (peso COCIDO)",
          "Zapallito verde rodajas: 150 g",
          "Morron rojo: 70 g",
          "Ajo: 1 diente (3 g)",
          "Anchoas en aceite (escurridas): 20 g (4 filetes)",
          "Huevo duro: 1 unidad (50 g)",
          "Aceite oliva: 12 ml",
          "Limon"])
    meal(pdf, "22:00", "Snack nocturno ANCLA", "~140 kcal | P 15 / C 6 / G 6",
         ["Yogur griego natural sin azucar: 170 g",
          "Chia: 10 g",
          "Canela: 1 g"])

    # ===== MARTES (gym) =====
    H2(pdf, "Martes — GYM 07:00 (Dia B)")
    meal(pdf, "05:30", "Pre-entreno (igual lunes)", "~110 kcal",
         ["Frutillas: 200 g + miel 10 g", "Cafe negro: 150 ml", "Agua con sal: 300 ml"])
    meal(pdf, "08:15", "Post-entreno", "~200 kcal",
         ["Whey: 35 g", "Agua: 300 ml", "Frutillas: 100 g"])
    meal(pdf, "09:30", "Desayuno — Huevos duros con queso y palta", "~530 kcal | P 38 / C 18 / G 35",
         ["Huevos DUROS: 3 unidades (150 g)",
          "Queso port salut descremado: 30 g",
          "Pan integral: 30 g (1 rebanada)",
          "Palta: 60 g + tomate 100 g",
          "Aceite oliva: 5 ml"])
    meal(pdf, "13:00", "Almuerzo — Pollo con boniato hervido y ensalada", "~580 kcal | P 50 / C 30 / G 28",
         ["Pechuga pollo grille: 220 g (cocido)",
          "Boniato HERVIDO: 100 g (cocido al agua)",
          "Lechuga: 80 g + rucula 50 g + tomate 100 g",
          "Cebolla morada: 30 g",
          "Palta: 60 g",
          "Aceitunas: 15 g + nueces 10 g",
          "Aceite oliva: 12 ml + vinagre o limon"])
    meal(pdf, "16:30", "Merienda", "~220 kcal",
         ["Queso cottage descremado: 200 g",
          "Frutos rojos mix: 30 g",
          "Canela: 1 g"])
    meal(pdf, "20:30", "Cena — Salmon con verduras", "~470 kcal | P 45 / C 8 / G 28",
         ["Salmon grille: 180 g (cocido)",
          "Espinaca salteada: 150 g",
          "Champignones: 80 g",
          "Ajo: 1 diente",
          "Aceite oliva: 12 ml + limon"])
    meal(pdf, "22:00", "Snack nocturno", "~140 kcal",
         ["Yogur griego: 170 g + chia 10 g"])

    # ===== MIERCOLES (descanso) =====
    H2(pdf, "Miercoles — descanso")
    meal(pdf, "07:30", "Desayuno — Huevos duros con palta y ricota", "~480 kcal | P 38 / C 12 / G 32",
         ["Huevos DUROS: 3 unidades (150 g)",
          "Ricota descremada: 80 g",
          "Palta: 60 g",
          "Tomate: 100 g rodajas",
          "Aceite oliva: 5 ml (sobre la palta)",
          "(Sin pan hoy)"])
    meal(pdf, "10:00", "Media manana", "~220 kcal",
         ["Yogur griego proteico: 200 g",
          "Nueces: 10 g",
          "Frutillas: 30 g"])
    meal(pdf, "13:00", "Almuerzo — Atun con espinaca y huevos duros", "~550 kcal | P 50 / C 10 / G 33",
         ["Atun al natural escurrido: 180 g",
          "Huevos DUROS: 2 unidades (100 g)",
          "Espinaca cocida o cruda: 150 g",
          "Queso descremado: 30 g",
          "Cebolla: 30 g",
          "Lechuga: 60 g + tomate 100 g + palta 60 g",
          "Aceite oliva: 15 ml + limon"])
    meal(pdf, "16:30", "Merienda", "~220 kcal",
         ["Ricota descremada: 150 g",
          "Almendras: 10 g",
          "Cacao amargo: 3 g (mezclar)"])
    meal(pdf, "20:30", "Cena — Pollo a la mediterranea", "~470 kcal | P 40 / C 8 / G 28",
         ["Pechuga pollo grille: 180 g (cocido)",
          "Brocoli al vapor: 200 g",
          "Champignones salteados: 80 g",
          "Aceitunas verdes: 15 g (5 unidades)",
          "Aceite oliva: 12 ml + limon + oregano"])
    meal(pdf, "22:00", "Snack nocturno", "~140 kcal",
         ["Yogur griego: 170 g + chia 10 g"])

    # ===== JUEVES (gym) =====
    H2(pdf, "Jueves — GYM 07:00 (Dia A)")
    meal(pdf, "05:30", "Pre-entreno (igual lunes)", "~110 kcal",
         ["Frutillas: 200 g + miel 10 g + cafe 150 ml + agua con sal 300 ml"])
    meal(pdf, "08:15", "Post-entreno", "~200 kcal",
         ["Whey 35 g + agua 300 ml + frutillas 100 g"])
    meal(pdf, "09:30", "Desayuno — Yogur proteico con frutillas + huevos duros", "~530 kcal | P 38 / C 18 / G 35",
         ["Yogur griego proteico sin azucar: 200 g",
          "Frutillas: 100 g",
          "Almendras: 15 g",
          "Canela: 1 g",
          "+ Huevos DUROS: 2 unidades (100 g) aparte",
          "Pan integral: 30 g (1 rebanada)"])
    meal(pdf, "13:00", "Almuerzo — Pollo con papa hervida y ensalada nicoise", "~580 kcal | P 50 / C 30 / G 28",
         ["Pechuga pollo grille: 200 g (cocido)",
          "Papa o boniato HERVIDO: 100 g",
          "Huevo duro: 1 unidad (50 g)",
          "Lechuga: 80 g + rucula 50 g",
          "Tomate: 100 g + pepino 80 g + cebolla 30 g",
          "Aceitunas negras: 20 g (7 unidades)",
          "Palta: 50 g",
          "Aceite oliva: 12 ml + limon"])
    meal(pdf, "16:30", "Merienda", "~220 kcal",
         ["Yogur griego: 170 g + nueces 12 g + frutos rojos 20 g"])
    meal(pdf, "20:30", "Cena — Brotola con brocoli y anchoas", "~470 kcal | P 45 / C 8 / G 28",
         ["Brotola al horno: 200 g (cocido)",
          "Brocoli al vapor: 200 g",
          "Huevo duro: 1 unidad (50 g)",
          "Anchoas (escurridas): 20 g (4 filetes) — encima del brocoli con limon",
          "Aceite oliva: 12 ml + limon"])
    meal(pdf, "22:00", "Snack nocturno", "~140 kcal",
         ["Yogur griego: 170 g + chia 10 g"])

    # ===== VIERNES =====
    H2(pdf, "Viernes — GYM 14:00 (Dia B, cena = COMIDA LIBRE)")
    meal(pdf, "07:30", "Desayuno — Huevos duros con palta y queso", "~480 kcal | P 38 / C 12 / G 32",
         ["Huevos DUROS: 3 unidades (150 g)",
          "Queso port salut descremado: 30 g",
          "Palta: 60 g",
          "Tomate: 100 g",
          "Aceite oliva: 5 ml",
          "(Sin pan hoy — se mueve al almuerzo post-entreno)"])
    meal(pdf, "10:30", "Media manana", "~200 kcal",
         ["Yogur griego proteico: 150 g",
          "Nueces: 10 g",
          "Frutillas: 30 g"])
    meal(pdf, "12:30", "Pre-entreno LIVIANO", "~110 kcal | P 1 / C 25 / G 0",
         ["Frutillas: 200 g",
          "Miel: 10 g",
          "Cafe negro sin azucar: 150 ml",
          "Agua + pizca de sal: 400 ml",
          "NO comer solido pesado entre 11:00 y 14:00."])
    meal(pdf, "15:15", "Post-entreno", "~200 kcal | P 32 / C 12 / G 3",
         ["Whey protein: 35 g",
          "Agua: 300 ml",
          "Frutillas: 100 g (licuar)"])
    meal(pdf, "17:00", "Almuerzo-merienda — Pollo con papa hervida", "~580 kcal | P 50 / C 30 / G 28",
         ["Pechuga pollo grille: 220 g (cocido)",
          "Papa o boniato HERVIDO: 100 g",
          "Espinaca fresca: 80 g + rucula 50 g",
          "Tomates cherry: 100 g",
          "Palta: 60 g",
          "Almendras fileteadas: 12 g",
          "Aceite oliva: 12 ml + limon"])
    meal(pdf, "20:30", "CENA LIBRE", "~600-900 kcal",
         ["Porcion normal, no hasta reventar.",
          "Elegi UNA: parrilla moderada (250 g carne magra + ensalada, sin achuras ni choripan), sushi (12-15 piezas sin tempura), milanesa al horno + ensalada, pizza (2 porciones masa fina).",
          "Alcohol: idealmente cero. Si vas a tomar, UNA copa de vino tinto. Avisa al psicologo en bitacora."])
    meal(pdf, "22:00", "Snack nocturno", "opcional hoy",
         ["Si la cena fue abundante, salteala."])

    # ===== SABADO =====
    H2(pdf, "Sabado — descanso")
    meal(pdf, "07:30", "Desayuno — Huevos duros con jamon, queso y palta", "~480 kcal | P 38 / C 12 / G 32",
         ["Huevos DUROS: 3 unidades (150 g)",
          "Jamon cocido magro: 30 g (1 fetita)",
          "Queso port salut descremado: 30 g",
          "Palta: 50 g",
          "Tomate: 100 g",
          "Aceite oliva: 5 ml (sobre la palta)",
          "(Sin pan hoy)"])
    meal(pdf, "10:00", "Media manana", "",
         ["Queso cottage: 150 g + frutillas 50 g + nueces 7 g"])
    meal(pdf, "13:00", "Almuerzo — Pollo con verduras al vapor", "~550 kcal",
         ["Pechuga pollo grille: 220 g (cocido)",
          "Brocoli al vapor: 150 g",
          "Zapallitos hervidos: 100 g",
          "Lechuga: 60 g + tomate 100 g + aceitunas 15 g",
          "Palta: 40 g",
          "Aceite oliva: 12 ml + limon"])
    meal(pdf, "16:30", "Merienda", "",
         ["Huevo DURO: 1 unidad",
          "Tomate: 100 g + aceite oliva 5 ml",
          "Almendras: 10 g"])
    meal(pdf, "20:30", "Cena — Pollo con vegetales al vapor y anchoas", "~470 kcal",
         ["Pechuga pollo grille: 180 g (cocido)",
          "Huevos DUROS: 2 unidades (100 g)",
          "Queso port salut descremado: 25 g",
          "Espinaca al vapor: 150 g",
          "Champignones: 80 g",
          "Anchoas (escurridas): 15 g (3 filetes) — encima",
          "Aceite oliva: 10 ml"])
    meal(pdf, "22:00", "Snack nocturno", "",
         ["Yogur griego: 170 g + chia 10 g"])

    # ===== DOMINGO =====
    H2(pdf, "Domingo — descanso + BATCH COOKING")
    meal(pdf, "07:30", "Desayuno — Huevos duros con palta y queso", "~480 kcal",
         ["Huevos DUROS: 3 unidades (150 g)",
          "Palta: 60 g",
          "Tomate: 100 g",
          "Queso descremado: 30 g",
          "Aceite oliva: 5 ml (sobre palta y tomate)",
          "(Sin pan hoy)"])
    P(pdf, "10:00–12:00 BATCH COOKING (ver guia abajo). Durante: mate sin azucar + arandanos 40 g.", color=GRAY)
    meal(pdf, "13:30", "Almuerzo — Pechuga de pollo al horno con ensalada", "~550 kcal",
         ["Pechuga pollo al horno: 220 g (cocido)",
          "Lechuga: 80 g + tomate 100 g + cebolla 30 g",
          "Pepino: 80 g + zanahoria rallada 40 g",
          "Palta: 60 g",
          "Aceitunas: 15 g + nueces 10 g",
          "Aceite oliva: 12 ml + limon + oregano"])
    meal(pdf, "16:30", "Merienda", "",
         ["Yogur griego proteico: 200 g",
          "Nueces: 10 g + cacao amargo 3 g"])
    meal(pdf, "20:30", "Cena liviana — Ensalada Caesar low-carb", "~470 kcal",
         ["Pechuga pollo grille: 180 g (cocido)",
          "Lechuga romana: 100 g",
          "Huevo duro: 1 unidad",
          "Anchoas: 20 g (4 filetes) — algunas en el aderezo, otras encima",
          "Queso parmesano rallado: 15 g",
          "Aceite oliva: 12 ml + limon + ajo + 1 yema (aderezo)"])
    meal(pdf, "22:00", "Snack nocturno", "",
         ["Yogur griego: 170 g + chia 10 g"])

    # ===== RESUMEN ROTACION =====
    H2(pdf, "Resumen rotacion semanal")
    table(pdf, [
        ["Dia", "Tipo", "Almuerzo", "Cena"],
        ["Lunes", "GYM (A)", "Pollo + papa hervida + ensalada", "Merluza + zapallitos + anchoas"],
        ["Martes", "GYM (B)", "Pollo + boniato hervido + ensalada", "Salmon con verduras"],
        ["Miercoles", "DESCANSO", "Atun + espinaca + huevos duros", "Pollo a la mediterranea"],
        ["Jueves", "GYM (A)", "Pollo + papa hervida + ensalada", "Brotola + brocoli + anchoas"],
        ["Viernes", "GYM (B)", "Pollo + papa hervida (17h post)", "LIBRE"],
        ["Sabado", "DESCANSO", "Pollo + vegetales al vapor", "Pollo + huevos duros + anchoas"],
        ["Domingo", "DESCANSO", "Pollo al horno con ensalada", "Caesar low-carb"],
    ])

    # ===== REGLAS Y LISTA =====
    H2(pdf, "Reglas + Lista de compras + Batch cooking")
    H3(pdf, "3 reglas de oro")
    reglas = [
        "1. Carbos: vegetales, frutos rojos y palta SIEMPRE. Pan integral solo en desayuno (1 rebanada). Banana solo pre-gym. Cero arroz, fideos, papa diaria, batata diaria, avena, dulces.",
        "2. Proteina en CADA comida. Sin excepcion.",
        "3. Snack nocturno = ancla anti-recaida alcohol. No es opcional.",
    ]
    for r in reglas:
        P(pdf, r, indent=2)

    H3(pdf, "Lista de compras semanal")
    P(pdf, "Proteinas:", size=10)
    P(pdf, "• Pechuga de pollo 2 kg (BASE) | Merluza/brotola 600 g | Salmon 200 g | Atun al natural 4 latas | Anchoas 1 frasco | Huevos 30 | Jamon cocido magro 100 g | Yogur griego proteico 1,5 kg | Ricota descremada 500 g | Port salut descremado 250 g | Cottage 350 g | Parmesano 50 g | Whey protein.", indent=2)
    P(pdf, "Grasas buenas:", size=10)
    P(pdf, "• Palta 7-8 unidades | Oliva extra virgen 500 ml | Aceitunas 250 g | Almendras 100 g | Nueces 100 g | Chia 200 g.", indent=2)
    P(pdf, "Vegetales (libres):", size=10)
    P(pdf, "• Lechuga, rucula, espinaca | Tomate, pepino, morron, cebolla, zanahoria, zapallitos, brocoli, champignones | Limones 10 | Ajo.", indent=2)
    P(pdf, "Frutas:", size=10)
    P(pdf, "• Frutillas 2 kg (pre + post entreno + meriendas) | Arandanos 200 g | Frambuesas opc 100 g.", indent=2)
    P(pdf, "Almidonados (peri-entreno):", size=10)
    P(pdf, "• Papa 1 kg + Boniato 1 kg (hervir el domingo).", indent=2)
    P(pdf, "Otros:", size=10)
    P(pdf, "• Pan integral (1 rebanada por dia gym = 4/semana) | Miel 1 frasco chico | Mate, cafe, canela, oregano, sal marina.", indent=2)

    H3(pdf, "Batch cooking domingo (90 min)")
    batch = [
        "1. Pollo al horno: 1,8 kg pechuga con limon, oregano, ajo, oliva. 35 min a 180 °C. Portionar 200-220 g.",
        "2. Huevos DUROS: 20 huevos. Hervir 10 min, pelados en heladera. Duran 5 dias.",
        "3. Papa y boniato HERVIDOS: 500 g de cada uno. Hervir 20 min, cortar en cubos. Duran 4-5 dias.",
        "4. Verduras al vapor: brocoli + zapallitos + espinaca para varios dias.",
        "5. Aderezo Caesar low-carb: licuar 1 yema + 2 anchoas + 1 ajo + 30 ml oliva + limon + parmesano. Dura 5 dias.",
        "6. Aderezo verde: licuar palta + limon + ajo + oliva.",
    ]
    for b in batch:
        P(pdf, b, indent=2)

    H3(pdf, "Suplementacion ajustada")
    sup = [
        "• Igual que suplementacion.md (creatina, omega-3, vitamina D, whey).",
        "• SUMAR: 2 g de sal extra/dia los primeros 7 dias (evitar mareo por baja insulina).",
        "• SUMAR: magnesio glicinato 300 mg/noche desde el dia 1.",
        "• Potasio cubierto por palta, espinaca, brocoli del menu.",
    ]
    for s in sup:
        P(pdf, s, indent=2)

    H3(pdf, "Ajuste por progreso")
    aj = [
        "• Semana 1: posible 'low-carb flu' (fatiga, dolor de cabeza). Subi sal y agua. Si dura mas de 5 dias, avisame.",
        "• Semana 2-3: evaluar peso y cintura.",
        "• Si peso no baja en 3 semanas: revisar adherencia. Si esta OK: bajar 100 kcal de grasas.",
        "• Si rendimiento en gym cae mucho: sumar 1 banana extra pre-gym (+20 g carbos).",
        "• Con analisis en mano: revisar lipidograma (LDL/HDL/trigliceridos) y ajustar tipo de grasas.",
    ]
    for a in aj:
        P(pdf, a, indent=2)

    pdf.output(str(OUT))
    print(f"PDF generado: {OUT}")
    print(f"Tamano: {OUT.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    main()
