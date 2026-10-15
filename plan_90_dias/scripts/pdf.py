import sys; sys.path.insert(0,'.')
from data import ROADMAP, AREAS, TRACK
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
F='/usr/share/fonts/truetype/dejavu/'
pdfmetrics.registerFont(TTFont('S',F+'DejaVuSans.ttf')); pdfmetrics.registerFont(TTFont('SB',F+'DejaVuSans-Bold.ttf'))
NAVY=colors.HexColor('#16324F'); TEAL=colors.HexColor('#1F8A70'); LIGHT=colors.HexColor('#EEF3F7'); GREY=colors.HexColor('#5B6770')
PH={"Días 1–15":"#2E6F9E","Días 16–30":"#1F8A70","Días 31–60":"#C77D1A","Días 61–90":"#B5473A","Meses 4–12":"#6B4FA0","Años 1–3":"#3B5A7A","Hasta 2035":"#4A4A4A"}
h1=ParagraphStyle('h1',fontName='SB',fontSize=20,textColor=NAVY,spaceAfter=6,leading=24)
h2=ParagraphStyle('h2',fontName='SB',fontSize=13,textColor=TEAL,spaceBefore=8,spaceAfter=4)
body=ParagraphStyle('b',fontName='S',fontSize=10,leading=14,textColor=colors.HexColor('#222'))
cell=ParagraphStyle('c',fontName='S',fontSize=8.2,leading=10.2)
cellb=ParagraphStyle('cb',parent=cell,fontName='SB')
hdr=ParagraphStyle('h',parent=cell,fontName='SB',textColor=colors.white)
def P(t,s=cell): return Paragraph(t,s)
W,H=landscape(A4)
def deco(c,d):
    c.saveState(); c.setFillColor(NAVY); c.rect(0,H-8*mm,W,8*mm,fill=1,stroke=0)
    c.setFont('S',8); c.setFillColor(GREY)
    c.drawString(15*mm,8*mm,'Plan de 90 días — de la idea a un negocio sostenible'); c.drawRightString(W-15*mm,8*mm,f'Página {d.page}'); c.restoreState()
def cover(c,d):
    c.saveState(); c.setFillColor(NAVY); c.rect(0,0,W,H,fill=1,stroke=0)
    c.setFillColor(TEAL); c.rect(0,H*0.38,W,4,fill=1,stroke=0)
    c.setFillColor(colors.white); c.setFont('SB',34); c.drawString(25*mm,H*0.58,'Plan de 90 días')
    c.setFont('S',18); c.drawString(25*mm,H*0.58-30,'De la idea a un negocio sostenible — y cómo sostenerlo hasta 2035')
    c.setFont('S',12); c.setFillColor(colors.HexColor('#BFD3E6'))
    c.drawString(25*mm,H*0.30,'Hoja de ruta · Capacidades estratégicas · Tablero de seguimiento')
    c.restoreState()
doc=SimpleDocTemplate('../Plan_90_dias.pdf',pagesize=landscape(A4),leftMargin=15*mm,rightMargin=15*mm,topMargin=16*mm,bottomMargin=16*mm,title='Plan de 90 días',author='Fede')
s=[PageBreak()]
s+= [Paragraph('Cómo usar este plan',h1),
 Paragraph('Este plan convierte una idea en evidencia en 90 días, con poco riesgo. La lógica es simple: <b>primero me conozco</b> (finanzas, tiempo, ventajas y red), <b>después escucho al mercado</b> (un sector, diez conversaciones, un problema medible), <b>luego pruebo con un piloto pago</b> y, al final, <b>mido y decido</b> si continuar, ajustar o cerrar.',body),Spacer(1,6)]
pr=[("1. Diagnóstico","Días 1–15","Saber cuántos meses puedo sostenerme, cuántas horas tengo y qué puedo ofrecer."),
    ("2. Mercado","Días 16–30","Encontrar un problema frecuente o costoso, quién lo paga y cómo medir la mejora."),
    ("3. Piloto","Días 31–60","Ofrecer una prueba pequeña y cobrada, resuelta con herramientas existentes."),
    ("4. Decisión","Días 61–90","Comparar contra el punto de partida, calcular rentabilidad y decidir con evidencia.")]
t=Table([[P(f'<b>{a}</b><br/><font color="#5B6770">{b}</font>',ParagraphStyle('x',parent=body,fontSize=11)),P(c,body)] for a,b,c in pr],colWidths=[55*mm,200*mm])
t.setStyle(TableStyle([('BACKGROUND',(0,0),(0,-1),LIGHT),('LINEBELOW',(0,0),(-1,-1),0.5,colors.HexColor('#CCD6DF')),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7)]))
s+=[t,Spacer(1,10),Paragraph('Fórmula clave: meses de autonomía',h2),
 Paragraph('<b>Meses de autonomía = ahorros líquidos disponibles ÷ gastos esenciales mensuales.</b> Ejemplo: con 1.200.000 de ahorros y 400.000 de gastos esenciales por mes, tengo 3 meses de autonomía. Ese número define cuánto riesgo puedo asumir y cuánto puedo esperar antes de aceptar un mal acuerdo.',body),
 Paragraph('Tres reglas de oro',h2),
 Paragraph('• <b>Probar pequeño, ampliar con evidencia</b>: nunca arriesgar recursos esenciales en una prueba.<br/>• <b>Cobrar desde el piloto</b>: la disposición a pagar es la única validación real de demanda.<br/>• <b>Decidir por datos, no por orgullo</b>: lo ya gastado no es razón para seguir.',body),PageBreak()]
# Roadmap
s.append(Paragraph('1. Hoja de ruta',h1))
rows=[[P(x,hdr) for x in ['Etapa','Objetivo','Acción concreta','Resultado esperado','Indicador','Estado']]]
sty=[('BACKGROUND',(0,0),(-1,0),NAVY),('GRID',(0,0),(-1,-1),0.4,colors.HexColor('#C9D3DC')),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('TOPPADDING',(0,0),(-1,-1),3.5),('BOTTOMPADDING',(0,0),(-1,-1),3.5)]
for i,r in enumerate(ROADMAP,1):
    rows.append([P(r[0],ParagraphStyle('e',parent=cellb,textColor=colors.white)),P(r[1],cellb),P(r[2]),P(r[3]),P(r[4]),P('☐ Pendiente')])
    sty.append(('BACKGROUND',(0,i),(0,i),colors.HexColor(PH[r[0]])))
    if i%2==0: sty.append(('BACKGROUND',(1,i),(-1,i),LIGHT))
t=Table(rows,colWidths=[24*mm,42*mm,72*mm,52*mm,50*mm,26*mm],repeatRows=1); t.setStyle(TableStyle(sty)); s+=[t,PageBreak()]
# Areas
s.append(Paragraph('2. Capacidades a construir (con lógica de teoría de juegos)',h1))
rows=[[P(x,hdr) for x in ['Área','Qué construir','Práctica concreta','Lógica de teoría de juegos','Qué evitar']]]
sty=[('BACKGROUND',(0,0),(-1,0),TEAL),('GRID',(0,0),(-1,-1),0.4,colors.HexColor('#C9D3DC')),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4),('BACKGROUND',(0,1),(0,-1),LIGHT)]
for i,r in enumerate(AREAS,1):
    rows.append([P(r[0],cellb),P(r[1]),P(r[2]),P(r[3]),P('✗ '+r[4],ParagraphStyle('v',parent=cell,textColor=colors.HexColor('#9A2F24')))])
t=Table(rows,colWidths=[38*mm,52*mm,56*mm,62*mm,58*mm],repeatRows=1); t.setStyle(TableStyle(sty))
s+=[t,PageBreak()]
# Tracking
s.append(Paragraph('3. Tablero de seguimiento',h1))
s.append(Paragraph('Completar al inicio (punto de partida), fijar la meta a 90 días y actualizar cada semana.',body)); s.append(Spacer(1,4))
rows=[[P(x,hdr) for x in ['Indicador o decisión','Punto de partida','Meta a 90 días','Resultado','Próxima acción']]]+[[P(x,cellb),'','','',''] for x in TRACK]
t=Table(rows,colWidths=[75*mm,45*mm,45*mm,45*mm,56*mm],rowHeights=[16]+[15.6]*len(TRACK),repeatRows=1)
t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),NAVY),('GRID',(0,0),(-1,-1),0.4,colors.HexColor('#C9D3DC')),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('BACKGROUND',(0,1),(0,-1),LIGHT)]))
s+=[t,PageBreak(),Paragraph('4. Regla de decisión al día 90',h1)]
dec=[("CONTINUAR","#1F8A70","El cliente ve una mejora medible, pagó, quiere renovar y el resultado después de costos es positivo."),
     ("AJUSTAR","#C77D1A","Hay interés y alguna mejora, pero el precio, el alcance, el comprador o los costos no cierran todavía."),
     ("CERRAR","#B5473A","Nadie paga, no hay mejora demostrable o el trabajo no es sostenible. Documentar lo aprendido y volver al paso de investigación.")]
t=Table([[P(f'<b>{a}</b>',ParagraphStyle('d',fontName='SB',fontSize=14,textColor=colors.white,alignment=1)),P(c,ParagraphStyle('dd',parent=body,fontSize=11,leading=15))] for a,b,c in dec],colWidths=[45*mm,210*mm],rowHeights=[22*mm]*3)
t.setStyle(TableStyle([('BACKGROUND',(0,i),(0,i),colors.HexColor(b)) for i,(a,b,c) in enumerate(dec)]+[('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LINEBELOW',(0,0),(-1,-1),0.5,colors.HexColor('#CCD6DF'))]))
s+=[t,Spacer(1,8),Paragraph('Tres ideas de teoría de juegos que sostienen todo',h2),
 Paragraph('• <b>Juegos repetidos</b>: con clientes y socios vas a interactuar muchas veces; la reputación de cumplir vale más que cualquier ventaja puntual.<br/>• <b>Mejor alternativa sin acuerdo</b>: tu poder de negociación depende de qué harías si no hay trato. Ahorros, otros clientes y canales propios la mejoran.<br/>• <b>Opciones reales</b>: invertir de a poco te da derecho, no obligación, de ampliar cuando aprendas más.',body),Spacer(1,4),Paragraph('Tu primera acción esta semana',h2),
 Paragraph('1) Anotá ingresos, gastos esenciales, deudas y ahorros. 2) Calculá tus meses de autonomía. 3) Bloqueá en tu agenda las horas semanales que vas a dedicar. 4) Escribí la lista de diez contactos. Con eso, la etapa de diagnóstico ya está en marcha.',body)]
doc.build(s,onFirstPage=cover,onLaterPages=deco)
print('ok')
