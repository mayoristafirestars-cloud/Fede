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
        ("Carbos objetivo", "60–80 g/dia"),
        ("Calorias dias gym", "2.250 kcal"),
        ("Calorias dias descanso", "2.050 kcal"),
        ("Macros dias gym", "P 200 g | C 80 g | G 105 g"),
        ("Macros dias descanso", "P 185 g | C 60 g | G 105 g"),
        ("Hidratacion dia gym", "3,2–3,5 L (con sal)"),
        ("Horario entreno", "08:00 AM (Lun/Mie/Vie)"),
        ("Comida libre", "Viernes a la noche"),
        ("Estilo", "Mediterraneo (palta, oliva, pescado azul)"),
        ("Vigente desde", "21/04/2026"),
    ]
    for k, v in datos:
        pdf.set_font("DejaVu", "B", 10)
        pdf.cell(55, 6, k, border="B")
        pdf.set_font("DejaVu", "", 10)
        pdf.cell(0, 6, v, border="B", new_x="LMARGIN", new_y="NEXT")

    pdf.ln(5)
    H3(pdf, "Que cambia vs el plan anterior")
    cambios = [
        "OUT: arroz, fideos, papa/batata diaria, avena, dulces.",
        "IN: mas palta, oliva, frutos secos, pescado azul, huevo, queso descremado.",
        "Mantenes: pan integral 1 rebanada en desayuno, yogur proteico, ricota, queso.",
        "Frutas limitadas a frutos rojos + palta + limon. Banana SOLO pre-gym.",
        "Sumar 2 g de sal extra/dia los primeros 7 dias (evitar low-carb flu).",
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
        ["06:30", "Pre-entreno (banana + cafe)", "110", "1", "27", "0"],
        ["08:00", "Entreno (complex 50-60 min)", "—", "—", "—", "—"],
        ["09:15", "Post-entreno (whey + frutos rojos)", "200", "32", "12", "3"],
        ["10:30", "Desayuno principal", "530", "38", "18", "35"],
        ["13:00", "Almuerzo", "580", "50", "12", "35"],
        ["16:30", "Merienda", "220", "20", "5", "13"],
        ["20:30", "Cena", "470", "45", "8", "28"],
        ["22:00", "Snack nocturno (yogur + chia)", "140", "15", "6", "6"],
        ["TOTAL", "", "~2.250", "~200", "~80", "~105"],
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
    H2(pdf, "Lunes — GYM 08:00")
    meal(pdf, "06:30", "Pre-entreno", "~110 kcal | P 1 / C 27 / G 0",
         ["Banana mediana: 100 g (pesada sin cascara)",
          "Cafe negro sin azucar: 150 ml",
          "Agua + pizca de sal: 300 ml"])
    meal(pdf, "09:15", "Post-entreno", "~200 kcal | P 32 / C 12 / G 3",
         ["Whey protein: 35 g",
          "Agua: 300 ml",
          "Arandanos o frutilla: 80 g (licuar todo)"])
    meal(pdf, "10:30", "Desayuno — Tostada proteica con palta", "~530 kcal | P 38 / C 18 / G 35",
         ["Pan integral: 30 g (1 rebanada)",
          "Huevos enteros: 3 unidades (150 g) revueltos sin aceite",
          "Palta: 70 g",
          "Tomate: 100 g rodajas",
          "Queso port salut descremado: 20 g",
          "Aceite oliva: 5 ml",
          "Cafe o mate sin azucar"])
    meal(pdf, "13:00", "Almuerzo — Pollo con ensalada mediterranea", "~580 kcal | P 50 / C 12 / G 35",
         ["Pechuga pollo grille: 220 g (peso COCIDO)",
          "Lechuga: 80 g",
          "Rucula: 50 g",
          "Tomate: 100 g",
          "Pepino: 80 g",
          "Palta: 60 g",
          "Aceitunas negras: 20 g (7 unidades)",
          "Almendras: 10 g",
          "Queso feta o ricota: 30 g",
          "Aceite oliva: 15 ml + limon + oregano"])
    meal(pdf, "16:30", "Merienda", "~220 kcal | P 20 / C 5 / G 13",
         ["Yogur griego proteico sin azucar: 170 g",
          "Nueces peladas: 12 g (5-6 mitades)",
          "Canela: 1 g"])
    meal(pdf, "20:30", "Cena — Merluza con zapallitos y huevo", "~470 kcal | P 45 / C 8 / G 28",
         ["Merluza al horno: 220 g (peso COCIDO)",
          "Zapallito verde rodajas: 150 g",
          "Morron rojo: 70 g",
          "Ajo: 1 diente (3 g)",
          "Huevo duro: 1 unidad (50 g)",
          "Aceite oliva: 15 ml",
          "Limon"])
    meal(pdf, "22:00", "Snack nocturno ANCLA", "~140 kcal | P 15 / C 6 / G 6",
         ["Yogur griego natural sin azucar: 170 g",
          "Chia: 10 g",
          "Canela: 1 g"])

    # ===== MARTES =====
    H2(pdf, "Martes — descanso")
    meal(pdf, "07:30", "Desayuno — Huevos con palta y queso", "~500 kcal | P 38 / C 15 / G 32",
         ["Huevos enteros: 3 unidades (150 g) revueltos",
          "Pan integral: 30 g (1 rebanada)",
          "Palta: 60 g",
          "Tomate: 100 g",
          "Ricota descremada: 50 g",
          "Aceite oliva: 5 ml"])
    meal(pdf, "10:00", "Media manana", "~220 kcal",
         ["Yogur griego proteico: 200 g",
          "Nueces: 10 g",
          "Arandanos: 30 g"])
    meal(pdf, "13:00", "Almuerzo — Tortilla de espinaca y atun", "~550 kcal | P 50 / C 10 / G 33",
         ["Huevos enteros: 3 unidades (150 g)",
          "Atun al natural escurrido: 100 g",
          "Espinaca cocida: 150 g",
          "Queso descremado rallado: 30 g",
          "Cebolla: 30 g",
          "Lechuga: 60 g + tomate 100 g + palta 40 g",
          "Aceite oliva: 15 ml"])
    meal(pdf, "16:30", "Merienda", "~220 kcal",
         ["Ricota descremada: 150 g",
          "Almendras: 10 g",
          "Cacao amargo en polvo: 3 g (mezclar)"])
    meal(pdf, "20:30", "Cena — Pollo a la mediterranea", "~470 kcal | P 40 / C 8 / G 28",
         ["Pechuga pollo grille: 180 g (cocido)",
          "Brocoli al vapor: 200 g",
          "Champignones salteados: 80 g",
          "Aceitunas verdes: 15 g (5 unidades)",
          "Aceite oliva: 12 ml + limon + oregano"])
    meal(pdf, "22:00", "Snack nocturno", "~140 kcal",
         ["Yogur griego natural: 170 g + chia 10 g"])

    # ===== MIERCOLES =====
    H2(pdf, "Miercoles — GYM 08:00")
    meal(pdf, "06:30", "Pre-entreno (igual lunes)", "~110 kcal",
         ["Banana: 100 g", "Cafe negro: 150 ml", "Agua con sal: 300 ml"])
    meal(pdf, "09:15", "Post-entreno (rotamos a frutilla)", "~200 kcal",
         ["Whey: 35 g", "Agua: 300 ml", "Frutilla: 80 g"])
    meal(pdf, "10:30", "Desayuno — Omelette con queso y palta", "~530 kcal | P 38 / C 18 / G 35",
         ["Huevos enteros: 2 unidades (100 g)",
          "Claras: 60 g (2 claras)",
          "Queso port salut descremado: 30 g",
          "Pan integral: 30 g (1 rebanada)",
          "Palta: 60 g + tomate 100 g",
          "Aceite oliva: 5 ml"])
    meal(pdf, "13:00", "Almuerzo — Carne magra con ensalada", "~580 kcal | P 50 / C 12 / G 35",
         ["Peceto o cuadrada al horno: 200 g (cocido)",
          "Lechuga: 80 g + rucula 50 g + tomate 100 g",
          "Cebolla morada: 30 g + zanahoria 40 g",
          "Palta: 60 g",
          "Aceitunas: 15 g + nueces 10 g",
          "Aceite oliva: 15 ml + vinagre"])
    meal(pdf, "16:30", "Merienda", "~220 kcal",
         ["Queso cottage descremado: 200 g",
          "Pera CHICA: 60 g (1/2 unidad)",
          "Canela: 1 g"])
    meal(pdf, "20:30", "Cena — Salmon con verduras", "~470 kcal | P 45 / C 8 / G 28",
         ["Salmon grille: 180 g (cocido)",
          "Espinaca salteada: 150 g",
          "Champignones: 80 g",
          "Ajo: 1 diente",
          "Aceite oliva: 12 ml + limon"])
    meal(pdf, "22:00", "Snack nocturno", "~140 kcal",
         ["Yogur griego: 170 g + chia 10 g"])

    # ===== JUEVES =====
    H2(pdf, "Jueves — descanso")
    meal(pdf, "07:30", "Desayuno — Crepe proteico", "~500 kcal | P 38 / C 15 / G 32",
         ["Huevos enteros: 2 unidades (100 g)",
          "Claras: 60 g",
          "Ricota descremada: 100 g",
          "Canela: 1 g",
          "Cocinar como panqueque grande",
          "Arandanos arriba: 80 g",
          "Almendras: 10 g"])
    meal(pdf, "10:00", "Media manana", "~220 kcal",
         ["Yogur griego proteico: 200 g + nueces 10 g"])
    meal(pdf, "13:00", "Almuerzo — Ensalada nicoise (atun y huevo)", "~550 kcal | P 50 / C 10 / G 33",
         ["Atun al natural escurrido: 180 g",
          "Huevos duros: 2 unidades (100 g)",
          "Lechuga: 80 g + rucula 50 g",
          "Tomate: 100 g + pepino 80 g + cebolla 30 g",
          "Aceitunas negras: 20 g (7 unidades)",
          "Palta: 60 g",
          "Anchoas (opcional): 10 g",
          "Aceite oliva: 15 ml + limon"])
    meal(pdf, "16:30", "Merienda", "~220 kcal",
         ["Ricota descremada: 150 g",
          "Frutos rojos mix: 50 g",
          "Almendras: 7 g"])
    meal(pdf, "20:30", "Cena — Brotola con brocoli", "~470 kcal | P 40 / C 8 / G 28",
         ["Brotola al horno: 220 g (cocido)",
          "Brocoli al vapor: 200 g",
          "Huevo duro: 1 unidad (50 g)",
          "Aceite oliva: 12 ml + limon"])
    meal(pdf, "22:00", "Snack nocturno", "~140 kcal",
         ["Yogur griego: 170 g + chia 10 g"])

    # ===== VIERNES =====
    H2(pdf, "Viernes — GYM 08:00 (cena = COMIDA LIBRE)")
    meal(pdf, "06:30", "Pre-entreno (igual lunes)", "~110 kcal",
         ["Banana: 100 g + cafe 150 ml + agua con sal"])
    meal(pdf, "09:15", "Post-entreno (rotamos a frambuesa)", "~200 kcal",
         ["Whey: 35 g + agua 300 ml + frambuesas o mix 100 g"])
    meal(pdf, "10:30", "Desayuno — Omelette completo", "~530 kcal | P 38 / C 18 / G 35",
         ["Huevos enteros: 2 unidades (100 g)",
          "Claras: 60 g",
          "Queso port salut descremado: 30 g",
          "Espinaca: 80 g",
          "Pan integral: 30 g (1 rebanada)",
          "Palta: 50 g + tomate 80 g",
          "Aceite oliva: 5 ml"])
    meal(pdf, "13:00", "Almuerzo — Salmon con ensalada verde", "~580 kcal | P 50 / C 12 / G 35",
         ["Salmon grille: 200 g (cocido)",
          "Espinaca fresca: 80 g + rucula 50 g",
          "Tomates cherry: 100 g",
          "Palta: 60 g",
          "Almendras fileteadas: 12 g",
          "Queso feta o ricota: 30 g",
          "Aceite oliva: 12 ml + limon"])
    meal(pdf, "16:30", "Merienda (liviana)", "",
         ["Yogur griego: 150 g + nueces 10 g"])
    meal(pdf, "20:30", "CENA LIBRE", "~600-900 kcal",
         ["Porcion normal, no hasta reventar.",
          "Elegi UNA: parrilla moderada (250 g carne magra + ensalada, sin achuras ni choripan), sushi (12-15 piezas sin tempura), milanesa al horno + ensalada, pizza (2 porciones masa fina).",
          "Alcohol: idealmente cero. Si vas a tomar, UNA copa de vino tinto. Avisa al psicologo en bitacora."])
    meal(pdf, "22:00", "Snack nocturno", "opcional hoy",
         ["Si la cena fue abundante, salteala."])

    # ===== SABADO =====
    H2(pdf, "Sabado — descanso")
    meal(pdf, "07:30", "Desayuno — Revuelto Gramajo low-carb", "~500 kcal | P 38 / C 15 / G 32",
         ["Huevos enteros: 3 unidades (150 g)",
          "Jamon cocido magro: 30 g (1 fetita)",
          "Queso port salut descremado: 30 g",
          "Pan integral: 30 g (1 rebanada)",
          "Tomate: 100 g + palta 40 g",
          "Aceite oliva: 5 ml"])
    meal(pdf, "10:00", "Media manana", "",
         ["Queso cottage: 150 g + arandanos 50 g + nueces 7 g"])
    meal(pdf, "13:00", "Almuerzo — Milanesa al horno (harina almendra)", "~550 kcal",
         ["Pechuga pollo o cuadrada: 200 g (cocido)",
          "Empanar con: harina almendra 25 g + clara 30 g",
          "Zapallitos asados: 150 g",
          "Lechuga: 60 g + tomate 100 g + aceitunas 15 g",
          "Aceite oliva: 12 ml"])
    meal(pdf, "16:30", "Merienda", "",
         ["Huevo duro: 1 unidad",
          "Tomate: 100 g + aceite oliva 5 ml",
          "Almendras: 10 g"])
    meal(pdf, "20:30", "Cena — Omelette con vegetales y queso", "~470 kcal",
         ["Huevos enteros: 3 unidades (150 g)",
          "Queso port salut descremado: 30 g",
          "Espinaca salteada: 150 g",
          "Champignones: 80 g",
          "Aceite oliva: 12 ml"])
    meal(pdf, "22:00", "Snack nocturno", "",
         ["Yogur griego: 170 g + chia 10 g"])

    # ===== DOMINGO =====
    H2(pdf, "Domingo — descanso + BATCH COOKING")
    meal(pdf, "07:30", "Desayuno — Huevos poche con palta", "~500 kcal",
         ["Huevos poche: 3 unidades (150 g)",
          "Pan integral: 30 g (1 rebanada)",
          "Palta: 60 g + tomate 100 g",
          "Queso descremado: 20 g"])
    P(pdf, "10:00–12:00 BATCH COOKING (ver guia abajo). Durante: mate sin azucar + arandanos 40 g.", color=GRAY)
    meal(pdf, "13:30", "Almuerzo — Asado low-carb", "~550 kcal",
         ["Bife de chorizo desgrasado o vacio magro: 220 g (cocido)",
          "Provoleta chica (opcional): 30 g",
          "Lechuga: 80 g + tomate 100 g + cebolla 30 g",
          "Palta: 50 g",
          "Aceite oliva: 10 ml",
          "SIN PAN. Sin chorizo. Sin chinchulines. Sin papa."])
    meal(pdf, "16:30", "Merienda", "",
         ["Yogur griego proteico: 200 g",
          "Nueces: 10 g + cacao amargo 3 g"])
    meal(pdf, "20:30", "Cena liviana — Ensalada Caesar low-carb", "~470 kcal",
         ["Pechuga pollo grille: 180 g (cocido)",
          "Lechuga romana: 100 g",
          "Huevo duro: 1 unidad",
          "Anchoas (opcional): 10 g",
          "Queso parmesano rallado: 15 g",
          "Aceite oliva: 12 ml + limon + ajo + 1 yema (aderezo)"])
    meal(pdf, "22:00", "Snack nocturno", "",
         ["Yogur griego: 170 g + chia 10 g"])

    # ===== RESUMEN ROTACION =====
    H2(pdf, "Resumen rotacion semanal")
    table(pdf, [
        ["Dia", "Almuerzo", "Cena"],
        ["Lunes", "Pollo + ensalada mediterranea", "Merluza + zapallitos"],
        ["Martes", "Tortilla espinaca + atun", "Pollo a la mediterranea"],
        ["Miercoles", "Carne magra + ensalada", "Salmon con verduras"],
        ["Jueves", "Ensalada nicoise (atun + huevo)", "Brotola con brocoli"],
        ["Viernes", "Salmon + ensalada verde", "LIBRE"],
        ["Sabado", "Milanesa al horno (harina almendra)", "Omelette con verduras"],
        ["Domingo", "Asado low-carb", "Ensalada Caesar low-carb"],
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
    P(pdf, "• Pollo 1,5 kg | Carne magra 600 g | Salmon 400 g | Merluza/brotola 600 g | Atun 4 latas | Huevos 30 | Yogur griego proteico 1,5 kg | Ricota 500 g | Port salut descremado 250 g | Cottage 350 g | Parmesano 50 g | Whey protein.", indent=2)
    P(pdf, "Grasas buenas:", size=10)
    P(pdf, "• Palta 6-7 unidades | Oliva extra virgen 500 ml | Aceitunas 250 g | Almendras 100 g | Nueces 100 g | Chia 200 g.", indent=2)
    P(pdf, "Vegetales (libres):", size=10)
    P(pdf, "• Lechuga, rucula, espinaca | Tomate, pepino, morron, cebolla, zanahoria, zapallitos, brocoli, champignones | Limones 10 | Ajo.", indent=2)
    P(pdf, "Frutas LIMITADAS:", size=10)
    P(pdf, "• Bananas: 3 unidades (solo dias gym) | Arandanos 300 g | Frutillas 250 g.", indent=2)
    P(pdf, "Otros:", size=10)
    P(pdf, "• Pan integral (1 rebanada/dia) | Harina de almendra 200 g | Mate, cafe, canela, cacao amargo, oregano, sal marina.", indent=2)

    H3(pdf, "Batch cooking domingo (90 min)")
    batch = [
        "1. Pollo al horno: 1,2 kg pechuga con limon, oregano, ajo, oliva. 35 min a 180 °C. Portionar.",
        "2. Huevos duros: 10 huevos. Pelados en heladera.",
        "3. Vegetales asados: zapallito + morron + cebolla + champignones con oliva y ajo. 25 min a 200 °C.",
        "4. Aderezo Caesar low-carb: licuar 1 yema + 2 anchoas + 1 ajo + 30 ml oliva + limon + parmesano. Dura 5 dias.",
        "5. Aderezo verde: licuar palta + limon + ajo + oliva.",
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
