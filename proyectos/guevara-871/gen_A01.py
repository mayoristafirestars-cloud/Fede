ME,MI,MF = 20,15,20
LIV,NIC,GAR = 490,140,300
DEEP,PATIO,PAR = 530,300,20
x_liv0=ME; x_liv1=x_liv0+LIV
x_tA0=x_liv1; x_tA1=x_tA0+MI
x_nic0=x_tA1; x_nic1=x_nic0+NIC
x_tB0=x_nic1; x_tB1=x_tB0+MI
x_gar0=x_tB1; x_gar1=x_gar0+GAR
W=x_gar1+ME
y_int=DEEP; y_f0=DEEP; y_f1=DEEP+MF
y_nb0=410; y_nb1=430
y_pat=y_f1+PATIO; y_par=y_pat+PAR
V_W=400; vx0=(x_liv0+x_liv1)/2-V_W/2; vx1=vx0+V_W
P_W=250; px0=(x_gar0+x_gar1)/2-P_W/2; px1=px0+P_W
D_W=90;  dy0=450; dy1=dy0+D_W
CT=-490                      # linea de corte A-A (arriba)

O=[];A=O.append
def rect(x,y,w,h,c): A(f'<rect class="{c}" x="{x}" y="{y}" width="{w}" height="{h}"/>')
def txt(x,y,s,c="tx",a="middle",rot=None):
    t=f' transform="rotate({rot},{x},{y})"' if rot else ''
    A(f'<text class="{c}" x="{x}" y="{y}" text-anchor="{a}"{t}>{s}</text>')
def line(x1,y1,x2,y2,c): A(f'<line class="{c}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/>')
def chainH(bps,y,labels):
    line(bps[0],y,bps[-1],y,"cot")
    for b in bps: line(b,y-9,b,y+9,"cot")
    alt=0
    for i,l in enumerate(labels):
        if not l: continue
        x0,x1=bps[i],bps[i+1]; xm=(x0+x1)/2
        if (x1-x0) < 70:                      # cota corta: se escalona y se acota con directriz
            alt ^= 1
            yy = y-34 if alt else y-58
            txt(xm,yy,l,"ck")
            line(xm,yy+6,xm,y-6,"cot")
        else:
            txt(xm,y-8,l,"ck")
def chainV(bps,x,labels):
    line(x,bps[0],x,bps[-1],"cot")
    for b in bps: line(x-9,b,x+9,b,"cot")
    for i,l in enumerate(labels):
        if l: txt(x-8,(bps[i]+bps[i+1])/2,l,"ck",rot=-90)
def nivel(x,y,v):
    A(f'<path class="niv" d="M {x} {y} l -13 -20 l 26 0 z"/>'); txt(x,y-26,v,"nv")

rect(-40,-190,W+80,190,"wex")
rect(0,y_pat,px0-25,PAR,"wex"); rect(px1+25,y_pat,W-(px1+25),PAR,"wex")
rect(0,0,ME,y_f1,"wnw"); rect(W-ME,0,ME,y_f1,"wnw")
rect(0,y_f0,x_tA1,MF,"wnw"); rect(x_tB0,y_f0,W-x_tB0,MF,"wnw")
rect(x_tA0,y_nb0,MI,y_f1-y_nb0,"wnw"); rect(x_tB0,0,MI,y_f1,"wnw")
rect(x_nic0,y_nb0,NIC,MF,"wnw")
rect(vx0,y_f0,V_W,MF,"hueco")
line(vx0,y_f0+5,vx1,y_f0+5,"carp"); line(vx0,y_f0+15,vx1,y_f0+15,"carp")
line(vx0,y_f0,vx0,y_f1,"carp"); line(vx1,y_f0,vx1,y_f1,"carp")
rect(px0,y_f0,P_W,MF,"hueco"); line(px0,y_f1,px1,y_f1,"carpg")
line(px0,y_f0,px0,y_f1,"carp"); line(px1,y_f0,px1,y_f1,"carp")
rect(x_tA0,dy0,MI,D_W,"hueco")
line(x_tA0,dy0,x_tA1,dy0,"carp"); line(x_tA0,dy1,x_tA1,dy1,"carp")
A(f'<line class="hoja" x1="{x_tA1}" y1="{dy1}" x2="{x_tA1}" y2="{dy1-D_W}"/>')
A(f'<path class="barr" d="M {x_tA1} {dy1-D_W} A {D_W} {D_W} 0 0 1 {x_tA1-D_W} {dy1}"/>')
for xe in (ME/2, x_tA0+MI/2, x_tB0+MI/2, W-ME/2): line(xe,CT-40,xe,y_par+80,"eje")
line(-150,y_f0+MF/2,W+150,y_f0+MF/2,"eje")
rect(x_liv0+8,8,LIV-16,60,"mob"); txt(265,46,"MESADA / COCINA","mb")
rect(x_liv0+30,190,220,85,"mob"); txt(140,240,"SOFÁ","mb")
A('<circle class="mob" cx="380" cy="235" r="55"/>'); txt(380,240,"MESA","mb")
rect(x_gar0+55,60,190,450,"mob"); txt(x_gar0+150,290,"AUTO 4,50 × 1,80","mb",rot=-90)
rect(x_nic0+30,y_nb1+18,80,55,"mob"); txt(x_nic0+70,y_nb1+50,"felpudo","mb")
nivel(265,330,"+0.25"); nivel(x_gar0+150,470,"+0.10"); nivel(595,y_f1+80,"±0.00")
txt(300,130,"1 · ESTAR–COMEDOR","lc"); txt(300,158,"32,00 m²","lb")
txt(300,182,"porcelanato mate R10","lb")
txt(x_gar0+150,130,"2 · GARAGE","lc"); txt(x_gar0+150,158,"15,90 m²","lb")
txt(595,y_nb1+95,"3","lc"); txt(595,y_nb1+120,"ACCESO","lb")
txt(W/2,y_f1+165,"PATIO DE FRENTE — SUELO PERMEABLE (C.A.S.)","lb")
txt(W/2,y_f1+195,"CÉSPED · ZONA DEL PERRO","lb")
txt(px0+P_W/2,y_par+42,"PASO VEHICULAR","lb")
txt(210,y_par+42,"PAREDÓN EXISTENTE h=1,20 (SE BAJA)","lb")
txt(W/2,-100,"CASA EXISTENTE","lc"); txt(W/2,-72,"ESTAR-COMEDOR · COCINA VIEJA → LAVADERO","lb")
for yy in (CT, y_par+110):
    A(f'<line class="cortl" x1="150" y1="{yy}" x2="240" y2="{yy}"/>')
    A(f'<path class="cortf" d="M 240 {yy} l -18 -9 l 0 18 z"/>')
    txt(126,yy+9,"A","cn")
line(200,CT,200,y_par+110,"corte")
chainH([0,ME,vx0,vx1,x_tA0,x_tA1,x_nic1,x_tB1,px0,px1,W-ME,W], -250,
       ["0,20","0,45","4,00","0,45","0,15","1,40","0,15","0,25","2,50","0,25","0,20"])
chainH([0,ME,x_liv1,x_tA1,x_nic1,x_tB1,x_gar1,W], -330,
       ["0,20","4,90","0,15","1,40","0,15","3,00","0,20"])
chainH([0,W], -415, ["10,00"])
chainV([0,y_int,y_f1,y_pat,y_par], -70, ["5,30","0,20","3,00","0,20"])
chainV([0,y_f1,y_par], -125, ["5,50","3,20"])
chainV([0,y_par], -180, ["8,70"])
line(-170,y_par+PAR+20,W+170,y_par+PAR+20,"lm"); txt(W+180,y_par+PAR+25,"L.M.","lb","start")
plan="".join(O)
sg=[]
for i in range(5):
    sg.append(f'<rect x="{i*100}" y="0" width="100" height="14" fill="{"#111" if i%2==0 else "#fff"}" stroke="#111" stroke-width="1.5"/>')
    sg.append(f'<text class="sg" x="{i*100}" y="-8" text-anchor="middle">{i}</text>')
sg.append('<text class="sg" x="500" y="-8" text-anchor="middle">5 m</text>')
escala="".join(sg)
RX=1340
def vlines(xs,h): return "".join(f'<line x1="{x}" y1="0" x2="{x}" y2="{h}" stroke="#111" stroke-width="1.2"/>' for x in xs)
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="-360 -570 2840 1750" width="2300">
<defs>
 <pattern id="pmamp" width="16" height="16" patternTransform="rotate(45)" patternUnits="userSpaceOnUse">
  <rect width="16" height="16" fill="#ececec"/><line x1="0" y1="0" x2="0" y2="16" stroke="#7a7a7a" stroke-width="2.2"/></pattern>
 <pattern id="pnew" width="9" height="9" patternTransform="rotate(45)" patternUnits="userSpaceOnUse">
  <rect width="9" height="9" fill="#c8342a"/><line x1="0" y1="0" x2="0" y2="9" stroke="#6e1610" stroke-width="2.6"/></pattern>
</defs>
<style>
 svg{{background:#fff}} text{{font-family:'Helvetica Neue',Arial,sans-serif;fill:#111}}
 .wex{{fill:url(#pmamp);stroke:#333;stroke-width:3}} .wnw{{fill:url(#pnew);stroke:#6e1610;stroke-width:3}}
 .hueco{{fill:#fff;stroke:none}} .carp{{stroke:#111;stroke-width:2.2;fill:none}}
 .carpg{{stroke:#111;stroke-width:3.5;fill:none}} .hoja{{stroke:#111;stroke-width:3.5}}
 .barr{{fill:none;stroke:#111;stroke-width:1.4;stroke-dasharray:8 6}}
 .mob{{fill:none;stroke:#5b6b76;stroke-width:1.6}}
 .eje{{stroke:#1a63c4;stroke-width:1;stroke-dasharray:34 8 6 8;opacity:.75}}
 .cot{{stroke:#111;stroke-width:1.2}} .lm{{stroke:#1a63c4;stroke-width:2.5;stroke-dasharray:26 9 6 9}}
 .corte{{stroke:#111;stroke-width:1.4;stroke-dasharray:30 8 6 8}}
 .cortl{{stroke:#111;stroke-width:5}} .cortf{{fill:#111}} .niv{{fill:#fff;stroke:#111;stroke-width:2}}
 .ck{{font-size:19px}} .tx{{font-size:19px}} .lb{{font-size:19px;fill:#333}}
 .lc{{font-size:25px;font-weight:700}} .mb{{font-size:15px;fill:#5b6b76}}
 .nv{{font-size:19px;font-weight:700}} .cn{{font-size:26px;font-weight:700}} .sg{{font-size:17px}}
 .th{{font-size:21px;font-weight:700}} .td{{font-size:19px}}
 .rt1{{font-size:29px;font-weight:700}} .rt2{{font-size:19px}} .rt3{{font-size:17px;fill:#555}}
 .adv{{font-size:19px;fill:#8f1d15;font-weight:700}}
</style>
<g>{plan}</g>
<g transform="translate(1180,-380)"><circle r="46" fill="none" stroke="#111" stroke-width="2.5"/>
 <path d="M 0 -60 l -13 26 l 13 -8 l 13 8 z" fill="#111"/>
 <text x="0" y="12" text-anchor="middle" style="font-size:30px;font-weight:700">N</text></g>
<g transform="translate(0,{y_par+190})">{escala}
 <text class="sg" x="0" y="42" text-anchor="start">ESCALA GRÁFICA — ESC. 1:50</text></g>

<g transform="translate({RX},-430)">
 <text class="th" x="0" y="-14">PLANILLA DE LOCALES</text>
 <rect x="0" y="0" width="1000" height="176" fill="none" stroke="#111" stroke-width="2.5"/>
 <line x1="0" y1="44" x2="1000" y2="44" stroke="#111" stroke-width="2.5"/>
 <line x1="0" y1="88" x2="1000" y2="88" stroke="#111" stroke-width="1.2"/>
 <line x1="0" y1="132" x2="1000" y2="132" stroke="#111" stroke-width="1.2"/>
 {vlines((70,420,570,790),176)}
 <text class="th" x="35" y="30" text-anchor="middle">N°</text><text class="th" x="245" y="30" text-anchor="middle">DENOMINACIÓN</text>
 <text class="th" x="495" y="30" text-anchor="middle">SUP.</text><text class="th" x="680" y="30" text-anchor="middle">SOLADO</text>
 <text class="th" x="895" y="30" text-anchor="middle">CIELORRASO</text>
 <text class="td" x="35" y="74" text-anchor="middle">1</text><text class="td" x="86" y="74">ESTAR–COMEDOR / COCINA</text>
 <text class="td" x="495" y="74" text-anchor="middle">32,00 m²</text><text class="td" x="680" y="74" text-anchor="middle">PORC. MATE R10</text>
 <text class="td" x="895" y="74" text-anchor="middle">YESO</text>
 <text class="td" x="35" y="118" text-anchor="middle">2</text><text class="td" x="86" y="118">GARAGE</text>
 <text class="td" x="495" y="118" text-anchor="middle">15,90 m²</text><text class="td" x="680" y="118" text-anchor="middle">LLANEADO</text>
 <text class="td" x="895" y="118" text-anchor="middle">LOSA VISTA</text>
 <text class="td" x="35" y="162" text-anchor="middle">3</text><text class="td" x="86" y="162">ACCESO (SEMICUBIERTO)</text>
 <text class="td" x="495" y="162" text-anchor="middle">1,40 m²</text><text class="td" x="680" y="162" text-anchor="middle">PORC. R11</text>
 <text class="td" x="895" y="162" text-anchor="middle">LOSA VISTA</text>
</g>
<g transform="translate({RX},-150)">
 <text class="th" x="0" y="-14">PLANILLA DE CARPINTERÍAS</text>
 <rect x="0" y="0" width="1000" height="176" fill="none" stroke="#111" stroke-width="2.5"/>
 <line x1="0" y1="44" x2="1000" y2="44" stroke="#111" stroke-width="2.5"/>
 <line x1="0" y1="88" x2="1000" y2="88" stroke="#111" stroke-width="1.2"/>
 <line x1="0" y1="132" x2="1000" y2="132" stroke="#111" stroke-width="1.2"/>
 {vlines((70,240,420,530,760),176)}
 <text class="th" x="35" y="30" text-anchor="middle">REF</text><text class="th" x="155" y="30" text-anchor="middle">MEDIDA</text>
 <text class="th" x="330" y="30" text-anchor="middle">TIPO</text><text class="th" x="475" y="30" text-anchor="middle">CANT.</text>
 <text class="th" x="645" y="30" text-anchor="middle">MATERIAL</text><text class="th" x="880" y="30" text-anchor="middle">VIDRIO</text>
 <text class="td" x="35" y="74" text-anchor="middle">V1</text><text class="td" x="155" y="74" text-anchor="middle">4,00 × 2,00</text>
 <text class="td" x="330" y="74" text-anchor="middle">CORREDIZA</text><text class="td" x="475" y="74" text-anchor="middle">1</text>
 <text class="td" x="645" y="74" text-anchor="middle">ALUMINIO RPT</text><text class="td" x="880" y="74" text-anchor="middle">DVH 3+3 LAM.</text>
 <text class="td" x="35" y="118" text-anchor="middle">P1</text><text class="td" x="155" y="118" text-anchor="middle">0,90 × 2,40</text>
 <text class="td" x="330" y="118" text-anchor="middle">BATIENTE</text><text class="td" x="475" y="118" text-anchor="middle">1</text>
 <text class="td" x="645" y="118" text-anchor="middle">MADERA MACIZA</text><text class="td" x="880" y="118" text-anchor="middle">—</text>
 <text class="td" x="35" y="162" text-anchor="middle">P2</text><text class="td" x="155" y="162" text-anchor="middle">2,50 × 2,40</text>
 <text class="td" x="330" y="162" text-anchor="middle">PORTÓN SECC.</text><text class="td" x="475" y="162" text-anchor="middle">1</text>
 <text class="td" x="645" y="162" text-anchor="middle">CHAPA + LISTONES</text><text class="td" x="880" y="162" text-anchor="middle">—</text>
</g>
<g transform="translate({RX},110)">
 <text class="th" x="0" y="-14">REFERENCIAS</text>
 <rect x="0" y="8" width="46" height="30" fill="url(#pmamp)" stroke="#333" stroke-width="2"/>
 <text class="td" x="62" y="31">MAMPOSTERÍA EXISTENTE QUE PERMANECE</text>
 <rect x="0" y="52" width="46" height="30" fill="url(#pnew)" stroke="#6e1610" stroke-width="2"/>
 <text class="td" x="62" y="75">MAMPOSTERÍA NUEVA 0,20 + SATE 100 mm (K 0,29)</text>
 <line x1="0" y1="106" x2="46" y2="106" class="eje"/><text class="td" x="62" y="112">EJE DE REPLANTEO</text>
 <path class="niv" d="M 23 142 l -13 -20 l 26 0 z"/><text class="td" x="62" y="140">NIVEL DE PISO TERMINADO</text>
</g>
<g transform="translate({RX},310)">
 <text class="th" x="0" y="0">NOTAS</text>
 <text class="td" x="0" y="34">1 · SE DEMUELEN 47,68 m² DE CONSTRUCCIÓN PRECARIA (h ≤ 1,50 m).</text>
 <text class="td" x="0" y="66">2 · MUROS NUEVOS: LADRILLO HUECO 0,18 + SATE EPS 100 mm. TECHO: LOSA + EPS 120–140 mm.</text>
 <text class="td" x="0" y="98">3 · SOLADOS ANTIDESLIZANTES R10 EN INTERIOR Y R11 EN SEMICUBIERTO Y EXTERIOR.</text>
 <text class="td" x="0" y="130">4 · PATIO DE FRENTE PERMEABLE: APORTA A LOS 62 m² DE C.A.S. (0,20 SOBRE 310 m²).</text>
 <text class="td" x="0" y="162">5 · DESAGÜES PLUVIALES ALEJADOS DEL PERÍMETRO DE FUNDACIÓN.</text>
 <text class="adv" x="0" y="200">6 · COTAS 5,50 Y 3,00 PRELIMINARES — VERIFICAR EN OBRA ANTES DE REPLANTEAR.</text>
</g>
<g transform="translate({RX},560)">
 <rect x="0" y="0" width="1000" height="300" fill="none" stroke="#111" stroke-width="3"/>
 <line x1="0" y1="70" x2="1000" y2="70" stroke="#111" stroke-width="2"/>
 <line x1="0" y1="146" x2="1000" y2="146" stroke="#111" stroke-width="2"/>
 <line x1="0" y1="212" x2="1000" y2="212" stroke="#111" stroke-width="2"/>
 <line x1="600" y1="212" x2="600" y2="300" stroke="#111" stroke-width="2"/>
 <text class="rt3" x="14" y="24">OBRA</text>
 <text class="rt1" x="14" y="56">REFORMA DE FRENTE — VIVIENDA UNIFAMILIAR</text>
 <text class="rt3" x="14" y="92">UBICACIÓN</text>
 <text class="rt2" x="14" y="118">A. GUEVARA 871 — SANTA ROSA, LA PAMPA</text>
 <text class="rt2" x="14" y="140">EJIDO 047, CIRC. I, RADIO f, MZ. 48, PARC. 21 · DISTRITO R3 I</text>
 <text class="rt3" x="14" y="170">CONTENIDO</text>
 <text class="rt2" x="14" y="200">PLANTA DE ARQUITECTURA — SECTOR FRENTE</text>
 <text class="rt3" x="14" y="240">ESCALA</text><text class="rt2" x="14" y="272">1:50</text>
 <text class="rt3" x="210" y="240">FECHA</text><text class="rt2" x="210" y="272">09/2026</text>
 <text class="rt3" x="410" y="240">LÁMINA</text><text class="rt2" x="410" y="272">A-01</text>
 <text class="adv" x="616" y="252">PRELIMINAR — NO APTO PARA</text>
 <text class="adv" x="616" y="282">OBRA NI PARA TRÁMITE</text>
</g>
</svg>'''
open("A-01-planta.svg","w").write(svg); print("ok")
