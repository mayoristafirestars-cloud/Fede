def T(x,y,s,c="td",a="start",rot=None):
    t=f' transform="rotate({rot},{x},{y})"' if rot else ''
    return f'<text class="{c}" x="{x}" y="{y}" text-anchor="{a}"{t}>{s}</text>'
def R(x,y,w,h,c): return f'<rect class="{c}" x="{x}" y="{y}" width="{w}" height="{h}"/>'
def L(x1,y1,x2,y2,c): return f'<line class="{c}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/>'
def cota(x1,y1,x2,y2,lab,off=0):
    o=[L(x1,y1,x2,y2,"cot")]
    if y1==y2:
        o+= [L(x1,y1-8,x1,y1+8,"cot"),L(x2,y2-8,x2,y2+8,"cot")]
        o.append(f'<circle class="bal" cx="{(x1+x2)/2}" cy="{y1-16}" r="15"/>')
        o.append(T((x1+x2)/2,y1-10,lab,"bl","middle"))
    else:
        o+= [L(x1-8,y1,x1+8,y1,"cot"),L(x2-8,y2,x2+8,y2,"cot")]
        o.append(f'<circle class="bal" cx="{x1-16}" cy="{(y1+y2)/2}" r="15"/>')
        o.append(T(x1-16,(y1+y2)/2+6,lab,"bl","middle"))
    return "".join(o)

E=[]
# esquema: casa | cocina actual | hueco | patio
E.append(R(0,0,240,300,"wex")); E.append(T(120,150,"CASA","lc","middle"))
E.append(T(120,178,"EXISTENTE","lb","middle"))
E.append(R(240,0,220,300,"wex"))
E.append(R(252,12,196,276,"loc"))
E.append(T(350,120,"COCINA ACTUAL","lc","middle")); E.append(T(350,148,"→ LAVADERO","lb","middle"))
E.append(R(460,40,300,260,"whu"))
E.append(R(472,52,276,236,"loc2"))
E.append(T(610,150,"HUECO","lc","middle")); E.append(T(610,178,"→ COCINA NUEVA","lb","middle"))
E.append(T(610,206,"(muros y contrapiso ya hechos)","lb","middle"))
E.append(T(900,150,"PATIO","lc","middle")); E.append(T(900,178,"asador existente","lb","middle"))
# puerta actual al patio
E.append(R(330,288,90,12,"hue")); E.append(L(330,300,420,300,"ab"))
E.append(T(375,336,"puerta actual","lb","middle"))
# vano existente en el hueco
E.append(R(700,288,60,12,"hue")); E.append(L(700,300,760,300,"ab"))
E.append(T(730,336,"vano c/dintel","lb","middle"))
# cotas
E.append(cota(252,-70,448,-70,"A"))
E.append(cota(472,-70,748,-70,"C"))
E.append(cota(252,12,252,288,"B"))
E.append(cota(472,52,472,288,"D"))
E.append(cota(330,380,420,380,"I"))
E.append(cota(700,380,760,380,"F"))
E.append(cota(460,430,760,430,"K"))
esq="".join(E)

filas=[("A","Ancho de la cocina actual (interior)"),
       ("B","Largo de la cocina actual (interior)"),
       ("C","Ancho del hueco (interior, entre caras de muro)"),
       ("D","Largo del hueco (interior)"),
       ("E","Altura libre del muro del hueco, del contrapiso al coronamiento"),
       ("F","Ancho del vano existente con dintel"),
       ("G","Altura de ese vano, del contrapiso al dintel"),
       ("H","Espesor de los muros del hueco"),
       ("I","Ancho de la puerta actual cocina → patio"),
       ("J","Altura libre de la cocina actual (piso a cielorraso)"),
       ("K","Distancia del hueco a la medianera más cercana"),
       ("L","Distancia del hueco al asador"),
       ("M","Desnivel entre piso de cocina y contrapiso del patio"),
       ("N","Distancia de la pileta actual al muro del hueco")]
tf=[]
for i,(lt,de) in enumerate(filas):
    y=i*46
    tf.append(L(0,y,1180,y,"tl"))
    tf.append(f'<circle class="bal" cx="30" cy="{y+29}" r="15"/>')
    tf.append(T(30,y+35,lt,"bl","middle"))
    tf.append(T(70,y+35,de,"td"))
    tf.append(L(900,y,900,y+46,"tl"))
    tf.append(T(1035,y+35,". . . . . . . . . . . .  m","tdd","middle"))
tf.append(L(0,len(filas)*46,1180,len(filas)*46,"tl"))
tabla="".join(tf)

chk=["Estado del coronamiento de los muros del hueco: ¿tiene capa aisladora o albardilla?",
     "¿Hay encadenado superior en los muros del hueco?",
     "¿El contrapiso del hueco está sano o hay que romperlo para pasar instalaciones?",
     "¿Dónde descarga hoy la bajada pluvial de la casa? ¿A qué distancia del muro?",
     "¿Hay capa aisladora horizontal en la base de los muros? (cateo)",
     "Ubicación del desagüe cloacal y de la cámara de inspección más cercana",
     "Ubicación del medidor de gas y recorrido actual de la cañería",
     "Tablero eléctrico: ubicación y si tiene disyuntor y jabalina",
     "Estructura del tanque elevado: estado del hormigón y de la columna",
     "Foto del muro de la cocina desde adentro, a la altura del zócalo"]
ck=[]
for i,c in enumerate(chk):
    y=i*44
    ck.append(f'<rect class="box" x="0" y="{y}" width="26" height="26"/>')
    ck.append(T(42,y+21,c,"td"))
checklist="".join(ck)

svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="-120 -180 2560 1560" width="2200">
<defs>
 <pattern id="pm" width="16" height="16" patternTransform="rotate(45)" patternUnits="userSpaceOnUse">
  <rect width="16" height="16" fill="#ececec"/><line x1="0" y1="0" x2="0" y2="16" stroke="#7a7a7a" stroke-width="2.2"/></pattern>
 <pattern id="ph" width="16" height="16" patternTransform="rotate(45)" patternUnits="userSpaceOnUse">
  <rect width="16" height="16" fill="#f6e9c9"/><line x1="0" y1="0" x2="0" y2="16" stroke="#b58b1f" stroke-width="2.2"/></pattern>
</defs>
<style>
 svg{{background:#fff}} text{{font-family:'Helvetica Neue',Arial,sans-serif;fill:#111}}
 .wex{{fill:url(#pm);stroke:#333;stroke-width:3}} .whu{{fill:url(#ph);stroke:#b58b1f;stroke-width:3}}
 .loc{{fill:#fff;stroke:none}} .loc2{{fill:#fffdf6;stroke:none}}
 .hue{{fill:#fff;stroke:none}} .ab{{stroke:#111;stroke-width:4}}
 .cot{{stroke:#111;stroke-width:1.3}} .bal{{fill:#fff;stroke:#111;stroke-width:2}}
 .bl{{font-size:19px;font-weight:700}} .td{{font-size:22px}} .tdd{{font-size:22px;fill:#888}}
 .lb{{font-size:19px;fill:#444}} .lc{{font-size:24px;font-weight:700}}
 .tl{{stroke:#111;stroke-width:1.4}} .box{{fill:#fff;stroke:#111;stroke-width:2.5}}
 .h1{{font-size:34px;font-weight:700}} .h2{{font-size:24px;font-weight:700}}
 .adv{{font-size:21px;fill:#8f1d15;font-weight:700}} .rt3{{font-size:17px;fill:#555}}
</style>
<text class="h1" x="0" y="-120">PLANILLA DE RELEVAMIENTO — SECTOR COCINA / LAVADERO / PATIO</text>
<text class="td" x="0" y="-80">A. Guevara 871, Santa Rosa · completar en obra con cinta métrica · esquema SIN ESCALA</text>
<g transform="translate(60,60)">{esq}</g>
<text class="h2" x="0" y="600">MEDIDAS A TOMAR</text>
<g transform="translate(0,630)">{tabla}</g>
<g transform="translate(1330,-40)">
 <text class="h2" x="0" y="0">VERIFICACIONES</text>
 <g transform="translate(0,30)">{checklist}</g>
</g>
<g transform="translate(1330,470)">
 <text class="h2" x="0" y="0">LO QUE SE VE EN LAS FOTOS</text>
 <text class="adv" x="0" y="42">⚠ HUMEDAD ACTIVA — resolver antes de terminar nada</text>
 <text class="td" x="0" y="80">· Manchas oscuras que bajan desde el coronamiento: los muros están</text>
 <text class="td" x="0" y="108">  descabezados, sin albardilla ni capa aisladora. Entra agua por arriba.</text>
 <text class="td" x="0" y="136">· Revoque desprendido en la base de la fachada del patio: compatible</text>
 <text class="td" x="0" y="164">  con humedad ascendente por capilaridad. Confirmar con cateo.</text>
 <text class="td" x="0" y="192">· La bajada pluvial descarga al pie del muro. Sobre loess colapsable</text>
 <text class="td" x="0" y="220">  eso es un riesgo de fundación, no un problema estético.</text>
 <text class="h2" x="0" y="270">A FAVOR</text>
 <text class="td" x="0" y="308">· El hueco ya tiene muros perimetrales y contrapiso ejecutados.</text>
 <text class="td" x="0" y="336">· Hay un vano con dintel resuelto: puede ser la puerta al patio.</text>
 <text class="td" x="0" y="364">· Hay viga de hormigón colocada: el recinto estaba previsto para losa.</text>
 <text class="td" x="0" y="392">· Asador existente en el patio: define la galería y el uso de verano.</text>
</g>
<g transform="translate(1330,940)">
 <rect x="0" y="0" width="1080" height="240" fill="none" stroke="#111" stroke-width="3"/>
 <line x1="0" y1="62" x2="1080" y2="62" stroke="#111" stroke-width="2"/>
 <line x1="0" y1="140" x2="1080" y2="140" stroke="#111" stroke-width="2"/>
 <text class="rt3" x="14" y="24">OBRA</text>
 <text class="h2" x="14" y="52">REFORMA — A. GUEVARA 871, SANTA ROSA (LA PAMPA)</text>
 <text class="rt3" x="14" y="86">CONTENIDO</text>
 <text class="td" x="14" y="122">PLANILLA DE RELEVAMIENTO EN OBRA</text>
 <text class="rt3" x="14" y="168">LÁMINA</text><text class="td" x="14" y="200">R-01</text>
 <text class="rt3" x="240" y="168">FECHA</text><text class="td" x="240" y="200">09/2026</text>
 <text class="rt3" x="500" y="168">RELEVÓ</text><text class="tdd" x="500" y="200">. . . . . . . . . . . . . . . . . . .</text>
</g>
</svg>'''
open("R-01-relevamiento.svg","w").write(svg); print("ok")
