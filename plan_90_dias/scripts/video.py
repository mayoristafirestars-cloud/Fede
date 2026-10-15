import sys,os,subprocess; sys.path.insert(0,'.')
from data import ROADMAP, AREAS
from PIL import Image, ImageDraw, ImageFont
from gtts import gTTS
F='/usr/share/fonts/truetype/dejavu/'
def f(sz,b=False): return ImageFont.truetype(F+('DejaVuSans-Bold.ttf' if b else 'DejaVuSans.ttf'),sz)
W,H=1920,1080; NAVY=(22,50,79); TEAL=(31,138,112); BG=(246,248,250); INK=(34,34,34); GREY=(91,103,112)
PH={"Días 1–15":(46,111,158),"Días 16–30":(31,138,112),"Días 31–60":(199,125,26),"Días 61–90":(181,71,58),"Meses 4–12":(107,79,160),"Años 1–3":(59,90,122),"Hasta 2035":(74,74,74)}
def wrap(d,t,font,maxw):
    out=[];line=''
    for w in t.split():
        x=(line+' '+w).strip()
        if d.textlength(x,font=font)<=maxw: line=x
        else: out.append(line); line=w
    out.append(line); return out
def base(title,color=NAVY,kicker=None):
    im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im)
    d.rectangle([0,0,W,150],fill=color)
    if kicker: d.text((90,28),kicker,font=f(30),fill=(210,225,238))
    d.text((90,62 if kicker else 45),title,font=f(54,True),fill='white')
    return im,d
def bullets(d,items,y=210,sz=38,x=110,maxw=1700,gap=26):
    for it in items:
        if isinstance(it,tuple): head,txt=it
        else: head,txt=None,it
        d.ellipse([x,y+14,x+16,y+30],fill=TEAL)
        lines=wrap(d,(head+': ' if head else '')+txt,f(sz),maxw-60)
        first=True
        for ln in lines:
            if first and head and ln.startswith(head):
                d.text((x+40,y),head+':',font=f(sz,True),fill=NAVY)
                rest=ln[len(head)+1:]; d.text((x+40+d.textlength(head+':',font=f(sz,True)),y),rest,font=f(sz),fill=INK)
            else: d.text((x+40,y),ln,font=f(sz),fill=INK)
            first=False; y+=sz+12
        y+=gap
    return y
slides=[]
def add(im,narr): slides.append((im,narr))
# 1 cover
im=Image.new('RGB',(W,H),NAVY); d=ImageDraw.Draw(im)
d.rectangle([0,690,W,698],fill=TEAL)
d.text((140,330),'Plan de 90 días',font=f(110,True),fill='white')
d.text((140,480),'De la idea a un negocio sostenible',font=f(54),fill=(210,225,238))
d.text((140,560),'y cómo sostenerlo hasta 2035',font=f(54),fill=(210,225,238))
d.text((140,760),'Hoja de ruta  ·  Capacidades  ·  Tablero de seguimiento',font=f(36),fill=(160,190,215))
add(im,"Bienvenido. En este video te explico un plan de noventa días para pasar de una idea a un negocio sostenible, y cómo seguir construyéndolo durante los próximos años. Vamos a ver la hoja de ruta, las capacidades que conviene desarrollar, y un tablero para medir el avance.")
# 2 logic
im,d=base('La lógica del plan')
steps=[("1","Diagnóstico","Días 1–15",PH["Días 1–15"]),("2","Mercado","Días 16–30",PH["Días 16–30"]),("3","Piloto","Días 31–60",PH["Días 31–60"]),("4","Decisión","Días 61–90",PH["Días 61–90"])]
for i,(n,t,s,c) in enumerate(steps):
    x=110+i*440; d.rounded_rectangle([x,260,x+390,620],radius=28,fill=c)
    d.text((x+40,290),n,font=f(110,True),fill='white'); d.text((x+40,450),t,font=f(50,True),fill='white'); d.text((x+40,530),s,font=f(36),fill=(240,240,240))
    if i<3: d.polygon([(x+400,420),(x+430,440),(x+400,460)],fill=GREY)
d.text((110,700),'Probar pequeño  →  medir  →  decidir con evidencia',font=f(48,True),fill=NAVY)
d.text((110,790),'Nunca arriesgar recursos esenciales en una prueba.',font=f(40),fill=GREY)
add(im,"La lógica es simple y tiene cuatro etapas. Primero, un diagnóstico de mi situación. Segundo, escuchar al mercado para encontrar un problema real. Tercero, probarlo con un piloto pequeño y cobrado. Y cuarto, medir los resultados y decidir con evidencia. La idea central es probar en pequeño, aprender, y recién después ampliar, sin arriesgar nunca los recursos esenciales.")
narr={
"Días 1–15":"Etapa uno, días uno a quince: conocerme. Anoto ingresos, gastos esenciales, deudas y ahorros líquidos para tener un diagnóstico financiero. Calculo mis meses de autonomía. Reservo horas semanales realistas para el plan. Hago una lista de mis habilidades, experiencia y resultados demostrables. Y activo mi red: identifico diez personas o empresas a las que puedo contactar.",
"Días 16–30":"Etapa dos, días dieciséis a treinta: escuchar al mercado. Elijo un sector que conozca o donde tenga acceso a compradores. Converso con unos diez potenciales clientes para detectar problemas frecuentes o costosos. Pregunto cómo los resuelven hoy, cuánto les cuesta y quién decide la compra. Selecciono un problema medible que pueda probar con pocos recursos, y registro la situación inicial para poder demostrar una mejora.",
"Días 31–60":"Etapa tres, días treinta y uno a sesenta: el piloto. Diseño una oferta concreta, con alcance, precio, duración y condiciones. Busco una prueba pequeña pero cobrada, porque pagar es la única validación real de demanda. Implemento con herramientas existentes y trabajo manual, sin grandes inversiones. Y controlo los riesgos: uso solo datos autorizados y reviso las decisiones sensibles.",
"Días 61–90":"Etapa cuatro, días sesenta y uno a noventa: medir y decidir. Comparo el resultado con la situación inicial. Registro ingresos, herramientas, horas, costos e impuestos para saber si es rentable. Consulto si el cliente quiere renovar. Y decido: continuar, ajustar o cerrar, según la evidencia, no por orgullo ni por lo que ya gasté.",
}
for ph in ["Días 1–15","Días 16–30","Días 31–60","Días 61–90"]:
    rows=[r for r in ROADMAP if r[0]==ph]
    im,d=base({'Días 1–15':'Diagnóstico','Días 16–30':'Mercado','Días 31–60':'Piloto','Días 61–90':'Medir y decidir'}[ph],PH[ph],ph)
    y=200
    for r in rows:
        d.rounded_rectangle([90,y,W-90,y+150],radius=18,fill='white',outline=(210,218,226),width=2)
        d.rectangle([90,y,104,y+150],fill=PH[ph])
        d.text((135,y+18),r[1],font=f(38,True),fill=NAVY)
        ln=wrap(d,r[2],f(30),1050)
        for k,l in enumerate(ln[:2]): d.text((135,y+72+k*38),l,font=f(30),fill=INK)
        d.text((1250,y+30),'Indicador',font=f(24),fill=GREY)
        for k,l in enumerate(wrap(d,r[4],f(30,True),520)[:2]): d.text((1250,y+64+k*38),l,font=f(30,True),fill=PH[ph])
        y+=170
    add(im,narr[ph])
    if ph=="Días 1–15":
        im,d=base('Meses de autonomía',PH[ph],'La fórmula clave')
        d.text((W//2,380),'Ahorros líquidos  ÷  Gastos esenciales mensuales',font=f(64,True),fill=NAVY,anchor='mm')
        d.text((W//2,500),'=  meses que puedo sostenerme',font=f(56),fill=TEAL,anchor='mm')
        d.rounded_rectangle([360,620,W-360,860],radius=24,fill='white',outline=(210,218,226),width=2)
        d.text((W//2,690),'Ejemplo: 1.200.000 ÷ 400.000 = 3 meses',font=f(48,True),fill=INK,anchor='mm')
        d.text((W//2,790),'Más autonomía = más poder para rechazar malos acuerdos',font=f(36),fill=GREY,anchor='mm')
        add(im,"La fórmula clave es esta: ahorros líquidos dividido gastos esenciales mensuales. Por ejemplo, con un millón doscientos mil de ahorro y cuatrocientos mil de gastos esenciales, tengo tres meses de autonomía. Ese número define cuánto riesgo puedo asumir, y cuánto puedo esperar antes de aceptar un mal acuerdo.")
# Long term
im,d=base('Después de los 90 días',(107,79,160))
cols=[("Meses 4–12",["Repetir lo que funciona con otro cliente","Documentar procesos y crear herramientas reutilizables"]),
      ("Años 1–3",["Contratos recurrentes y relaciones de largo plazo","Diversificar clientes, proveedores y canales"]),
      ("Hasta 2035",["Revisar cada trimestre tecnología, demanda y resultados","Mantener opciones ante distintos futuros"])]
for i,(t,its) in enumerate(cols):
    x=90+i*590; d.rounded_rectangle([x,220,x+550,880],radius=24,fill='white',outline=(210,218,226),width=2)
    d.rounded_rectangle([x,220,x+550,330],radius=24,fill=PH[t]); d.rectangle([x,300,x+550,330],fill=PH[t])
    d.text((x+40,245),t,font=f(48,True),fill='white'); yy=380
    for it in its:
        for k,l in enumerate(wrap(d,it,f(36),460)): d.text((x+40,yy),l,font=f(36),fill=INK); yy+=48
        yy+=40
add(im,"Si el piloto funciona, viene el largo plazo. Entre el mes cuatro y el doce, busco otro cliente con el mismo problema para comprobar que la solución es repetible, y documento procesos para depender menos de mis horas. Entre el año uno y el tres, construyo contratos recurrentes y diversifico clientes, proveedores y canales, para que ningún cliente concentre demasiado mis ingresos. Y hasta 2035, reviso la estrategia cada trimestre para adaptarme a distintos futuros.")
# Areas: 3 slides
groups=[AREAS[0:5],AREAS[5:10],AREAS[10:14]]
gn=["Las capacidades que conviene construir. Conocimiento del sector: hablar con compradores y ver cómo trabajan, en lugar de aprender herramientas sin conocer problemas. Inteligencia artificial: automatizar una tarea y medir calidad, costo y errores, sin confiar en resultados sin revisarlos. Juicio estratégico: registrar predicciones y compararlas con lo que pasó. Creatividad: proponer varias alternativas y probar una. Y liderazgo: definir responsabilidades, plazos y revisiones, sin prometer certezas que no tengo.",
    "Seguimos. Confianza: cumplir acuerdos y comunicar errores temprano, porque en juegos repetidos la conducta de hoy afecta los acuerdos de mañana. Negociación: definir qué haré si no hay trato, ya que una mejor alternativa aumenta mi poder. Relaciones: aportar valor antes de pedir favores. Información: escuchar a clientes, proveedores y especialistas, nunca depender de rumores. Y distribución: construir canales propios para no depender completamente de una plataforma.",
    "Y por último. Activos propios: convertir lo aprendido en procesos, marca y herramientas reutilizables, para no empezar siempre desde cero. Autonomía financiera: revisar gastos, deuda y reservas, porque poder esperar permite rechazar malos acuerdos. Inversión gradual: probar pequeño y ampliar con evidencia. Y adaptación: revisar resultados y dependencias cada trimestre, en vez de apostar todo a una sola predicción."]
for gi,g in enumerate(groups):
    im,d=base('Capacidades a construir',TEAL,f'Parte {gi+1} de 3')
    d.text((110,180),'Práctica',font=f(26,True),fill=GREY); d.text((1260,180),'Evitar',font=f(26,True),fill=(154,47,36))
    y=225
    for a in g:
        d.rounded_rectangle([90,y,W-90,y+150],radius=16,fill='white',outline=(210,218,226),width=2)
        d.text((120,y+16),a[0],font=f(34,True),fill=NAVY)
        for k,l in enumerate(wrap(d,a[2],f(28),1080)[:2]): d.text((120,y+64+k*36),l,font=f(28),fill=INK)
        for k,l in enumerate(wrap(d,'✗ '+a[4],f(28),540)[:3]): d.text((1260,y+28+k*36),l,font=f(28),fill=(154,47,36))
        y+=165
    add(im,gn[gi])
# Game theory
im,d=base('Tres ideas de teoría de juegos')
bullets(d,[("Juegos repetidos","con clientes y socios vas a interactuar muchas veces; la reputación de cumplir vale más que una ventaja puntual."),
           ("Mejor alternativa sin acuerdo","tu poder de negociación depende de qué harías si no hay trato."),
           ("Opciones reales","invertir de a poco te da el derecho, no la obligación, de ampliar cuando aprendas más.")],y=240,sz=42,gap=50)
add(im,"Detrás de todo esto hay tres ideas de teoría de juegos. Primera: los juegos repetidos. Vas a interactuar muchas veces con las mismas personas, así que la reputación de cumplir vale más que cualquier ventaja puntual. Segunda: tu mejor alternativa sin acuerdo. Tu poder de negociación depende de qué harías si no hay trato; ahorros, otros clientes y canales propios la mejoran. Tercera: las opciones reales. Invertir de a poco te da el derecho, pero no la obligación, de ampliar cuando sepas más.")
# Tracking
im,d=base('Tablero de seguimiento')
d.text((110,190),'Cada indicador: punto de partida  →  meta a 90 días  →  resultado  →  próxima acción',font=f(34),fill=GREY)
grp=[("Estrategia",["Objetivo principal","Sector elegido","Problema a resolver","Comprador accesible","Oferta de prueba","Métrica de éxito"]),
     ("Finanzas personales",["Horas por semana","Gastos esenciales","Ahorros líquidos","Meses de autonomía"]),
     ("Comercial",["Conversaciones","Propuestas","Pilotos pagos","Clientes que renuevan","Dependencia del mayor cliente"]),
     ("Economía y aprendizaje",["Ingresos y costos","Horas trabajadas","Resultado después de costos","Errores y retrabajos","Qué aprendí / qué cambio","Decisión"])]
for i,(t,its) in enumerate(grp):
    x=90+i*440; d.rounded_rectangle([x,270,x+410,960],radius=20,fill='white',outline=(210,218,226),width=2)
    d.text((x+30,295),t,font=f(34,True),fill=TEAL); yy=370
    for it in its:
        for l in wrap(d,'• '+it,f(30),360): d.text((x+30,yy),l,font=f(30),fill=INK); yy+=42
        yy+=18
add(im,"Para no perder el rumbo, usá el tablero de seguimiento. Cada indicador tiene un punto de partida, una meta a noventa días, el resultado y la próxima acción. Están agrupados en estrategia, finanzas personales, actividad comercial, y economía y aprendizaje. Actualizalo cada semana: qué aprendí, qué voy a cambiar, y cuál es la próxima acción con fecha.")
# Decision
im,d=base('La decisión del día 90')
dec=[("CONTINUAR",(31,138,112),"Hay mejora medible, el cliente pagó, quiere renovar y el resultado es positivo."),
     ("AJUSTAR",(199,125,26),"Hay interés, pero precio, alcance, comprador o costos todavía no cierran."),
     ("CERRAR",(181,71,58),"Nadie paga o no hay mejora. Documentar lo aprendido y volver a investigar.")]
for i,(t,c,x_) in enumerate(dec):
    y=230+i*230; d.rounded_rectangle([90,y,520,y+190],radius=20,fill=c); d.text((305,y+95),t,font=f(50,True),fill='white',anchor='mm')
    for k,l in enumerate(wrap(d,x_,f(38),1250)): d.text((570,y+45+k*52),l,font=f(38),fill=INK)
add(im,"Al día noventa hay tres decisiones posibles. Continuar, si hay una mejora medible, el cliente pagó, quiere renovar y el resultado después de costos es positivo. Ajustar, si hay interés pero el precio, el alcance, el comprador o los costos todavía no cierran. Y cerrar, si nadie paga o no hay mejora: en ese caso documento lo aprendido y vuelvo a la etapa de investigación. Cerrar a tiempo también es un buen resultado.")
# Closing
im=Image.new('RGB',(W,H),NAVY); d=ImageDraw.Draw(im)
d.text((140,170),'Tu primera acción esta semana',font=f(70,True),fill='white')
for i,t in enumerate(["Anotá ingresos, gastos, deudas y ahorros","Calculá tus meses de autonomía","Bloqueá tus horas semanales en la agenda","Escribí tu lista de diez contactos"]):
    y=340+i*140; d.ellipse([140,y,230,y+90],fill=TEAL); d.text((185,y+45),str(i+1),font=f(50,True),fill='white',anchor='mm'); d.text((280,y+15),t,font=f(50),fill='white')
add(im,"Para arrancar, cuatro acciones para esta misma semana. Uno: anotá tus ingresos, gastos, deudas y ahorros. Dos: calculá tus meses de autonomía. Tres: bloqueá en tu agenda las horas semanales que vas a dedicar. Y cuatro: escribí tu lista de diez contactos. Con eso, el plan ya está en marcha. ¡Éxitos!")
os.makedirs('v',exist_ok=True); parts=[]
for i,(im,n) in enumerate(slides):
    p=f'v/s{i:02d}'; im.save(p+'.png'); gTTS(n,lang='es',tld='com.mx').save(p+'.mp3')
    dur=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',p+'.mp3']))+1.2
    subprocess.run(['ffmpeg','-y','-loglevel','error','-loop','1','-i',p+'.png','-i',p+'.mp3','-af','apad,atempo=1.12','-t',str(dur/1.12),
      '-vf',f'fade=in:0:12,fade=out:st={dur/1.12-0.4}:d=0.4,format=yuv420p','-r','25','-c:v','libx264','-tune','stillimage','-c:a','aac','-ar','44100','-ac','2',p+'.mp4'],check=True)
    parts.append(p+'.mp4'); print(i,round(dur/1.12,1))
open('v/list.txt','w').write(''.join(f"file '{os.path.basename(x)}'\n" for x in parts))
subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i','v/list.txt','-c','copy','../Plan_90_dias_video.mp4'],check=True)
