# 03 — Potencial de mercado en Argentina: SaaS para mayoristas y distribuidoras

*Investigación al 20/10/2026. Las cifras marcadas **[EST]** son estimaciones propias o de cámaras sin metodología pública. El resto viene de fuentes oficiales o de prensa, citadas en línea.*

---

## 1. ¿Cuántos mayoristas y distribuidores hay en Argentina?

### 1.1 Dato oficial: empresas empleadoras registradas (OEDE / SIPA, 2024)

La fuente más sólida es la serie anual de empresas privadas del **Observatorio de Empleo y Dinámica Empresarial (OEDE)**. Se arma con el padrón de ARCA/AFIP y con el SIPA, y se actualizó en junio de 2026 ([planilla nacional_serie_empresas_2.xlsx](https://www.argentina.gob.ar/sites/default/files/nacional_serie_empresas_2.xlsx), [página OEDE](https://www.argentina.gob.ar/trabajo/estadisticas/oede-estadisticas-nacionales)). Solo cuenta empresas **con al menos un empleado registrado**, así que deja afuera a los monotributistas sin personal y a la informalidad.

**Comercio al por mayor (CIIU rev3, división 51): 35.379 empresas en 2024**, contra 34.395 en 2022 y 35.050 en 2023. La cifra crece levemente, aunque el total de empresas del país cayó de 573.008 a 558.317.

| Tamaño (OEDE, 2024) | Empresas | % |
|---|---|---|
| Micro | 19.768 | 56% |
| Pequeñas | 10.832 | 31% |
| Medianas | 3.035 | 9% |
| Grandes | 1.744 | 5% |
| **Total** | **35.379** | 100% |

Por tramo de empleo, unas 27.500 empresas tienen hasta ~9 empleados, ~6.600 tienen entre 10 y 49, ~1.130 entre 50 y 199 y ~170 tienen 200 o más. La asignación de los códigos de tramo es una inferencia propia a partir del cuadro 10.

**Apertura por rubro (CIIU a 4 dígitos, 2024, misma fuente):**

| Rubro (CIIU) | Empresas 2024 | ¿Es target? |
|---|---|---|
| 5122 Alimentos (almacén, golosinas, fiambres, etc.) | 7.381 | Núcleo |
| 5123 Bebidas | 1.513 | Núcleo |
| 5124 Cigarrillos / tabaco | 196 | Núcleo (canal kiosco) |
| 5131 Textiles, prendas, calzado (Flores, Once, Avellaneda) | 2.687 | Alto (subregistrado) |
| 5132 Librería, papel, cartón | 1.010 | Alto |
| 5133 Farmacéuticos, veterinarios, cosméticos, perfumería (droguerías, limpieza/perfumería) | 1.903 | Alto |
| 5135 Muebles, iluminación, artefactos | 1.273 | Medio-alto |
| 5139 Uso doméstico/personal n.c.p. (bazar, juguetes, regalería) | 1.704 | Alto |
| 5143 Madera, materiales de construcción, ferretería, sanitarios | 3.246 | Alto |
| 5190 Mercancías n.c.p. | 3.150 | Medio |
| 5119 Consignación de mercancías n.c.p. | 1.341 | Medio |
| 5159 Máquinas y materiales n.c.p. (incluye material eléctrico) | 2.152 | Medio |
| 5151/5152/5154 Maquinaria y equipos | 2.113 | Bajo |
| 5111/5121 Granos, hacienda, materias primas agro | 2.773 | Bajo (otro negocio) |
| 5141/5142/5149 Combustibles, metales, intermedios | 2.501 | Bajo |
| 503 Autopartes (mezcla mayorista y minorista) | 7.802 | Medio; ~25% mayorista **[EST]** |

**Lectura:** en los rubros "de distribución a comercios" (alimentos, bebidas, golosinas, limpieza/perfumería, librería, bazar/juguetes, textil, ferretería/construcción, eléctrico, autopartes) hay **unas 27.000–28.000 empresas empleadoras** **[EST, suma propia de los códigos de la tabla]**.

### 1.2 Lo que el registro formal no ve

- **Informalidad y monotributo.** Los mayoristas textiles de Flores (Av. Avellaneda), Once y La Salada y muchas distribuidoras familiares del interior operan como monotributistas o con personal no registrado, y no aparecen en el OEDE. Calculamos entre **10.000 y 20.000 unidades mayoristas adicionales** **[EST]**, con baja capacidad de pago de SaaS.
- **Pocos jugadores grandes.** El panel de la [Encuesta de Autoservicios Mayoristas del INDEC (julio 2026)](https://www.indec.gob.ar/uploads/informesdeprensa/autoservicios_mayoristas_09_26DA5CEEFE06.pdf) tiene **32 empresas con 193 bocas** (974.384 m²) y **12.915 empleados**. Ahí están Maxiconsumo, Diarco, Vital, Makro, Yaguar, Nini, Oscar David y otros. Facturaron **$401.070 millones en julio de 2026**, unos USD 270 M/mes o ~USD 3.200 M/año al tipo de cambio actual **[EST]**. Sus ventas reales cayeron **-1,1% interanual** en julio y **-2,7% en el acumulado enero-julio 2026**, después de un 2025 con **-6,7%**. El 59% de esas ventas está en el interior. Estas cadenas son clientes enterprise con ERP propio (SAP, desarrollos a medida), **no son el target** de un SaaS PyME. Sí son el competidor que empuja a las distribuidoras medianas a digitalizarse.
- **Cámaras sectoriales.** CADAM agrupa a los autoservicios mayoristas y organizó el "Black Mayorista", con más de 190 comercios adheridos en 2025 ([MDZ](https://www.mdzol.com/dinero/comercios-mayoristas-lanzan-semana-descuentos-40-n1376787)). También existen las cámaras de distribuidores de golosinas (ADGYA y regionales), de bebidas y de ferreterías. Ninguna publica un censo de socios. Las usamos como canal comercial, no como fuente de conteo.

### 1.3 Universo propuesto

| Universo | Empresas | Base |
|---|---|---|
| Mayoristas formales totales (OEDE div. 51 + parte de autopartes) | ~37.000 | Oficial + [EST] |
| + mayoristas informales/monotributo | ~47.000–57.000 | [EST] |
| Rubros de distribución a comercios (formales) | ~28.000 | Oficial, suma propia |
| Ídem, sin las micro más chicas (pequeñas, medianas y ~30% de las micro) | ~13.000–17.000 | [EST] |

---

## 2. Puntos de venta atendidos: el canal tradicional

- **NielsenIQ (junio 2026):** el canal tradicional más los autoservicios independientes explican **el 35% de las ventas de consumo masivo**, con **más de 194.700 puntos de venta independientes** relevados ([Mercado](https://mercado.com.ar/negocios/nielseniq-el-canal-tradicional-ya-explica-35-de-las-ventas-de-consumo-masivo)). A fines de 2025, el reparto era: tradicional (almacenes) 34%, supermercados de cadena 31% y autoservicios independientes 14%. En el último bimestre de 2025 los almacenes crecieron 8% y las cadenas cayeron 4% ([Mercado](https://mercado.com.ar/tendencias/autoservicios-y-almacenes-ganan-traccion-en-el-consumo-masivo-durante-2025)).
- **Kioscos:** la UKRA, con datos de ARCA, habla de 112.000 kioscos formales a mediados de 2024, 96.000 a mediados de 2025 y **"menos de 60.000" en marzo de 2026** según datos de tabacaleras. Cierran entre 50 y 70 por día ([El Economista](https://eleconomista.com.ar/economia/cierre-masivo-kioscos-ya-bajaron-16000-persianas-avanzan-cadenas-n85298), [La Capital](https://www.lacapital.com.ar/informacion-general/con-datos-arca-comerciantes-aseguran-que-cierran-70-kioscos-dia-argentina-n10247268.html)). Estas son cifras de cámara **[EST]**.
- **Autoservicios chinos:** CEDEAPSA estima **unos 13.000 locales**, frente a ~19.000 antes de la pandemia ([iProfesional](https://www.iprofesional.com/negocios/434608-carrefour-vende-sus-activos-por-que-los-super-chinos-quieren-el-negocio-y-cual-es-su-plan)).
- **Scanntech (Radar, julio 2026):** los autoservicios chicos promedian 3,4 unidades por ticket y los independientes self-service 5,5. Es la señal de un formato de compra chica y frecuente que se repone seguido desde el mayorista.
- **Scentia 2026:** en febrero cayeron autoservicios independientes (-3,8%), kioscos y almacenes (-1,9%) y supermercados (-5,9%). El canal tradicional resiste mejor, sobre todo en el interior ([Bloomberg Línea](https://www.bloomberglinea.com/latinoamerica/argentina/el-consumo-masivo-sigue-sin-recuperarse-en-argentina-y-acumula-una-caida-de-33-en-2026/)).

**Implicancia:** cada distribuidora de consumo masivo atiende típicamente entre 300 y 3.000 puntos de venta con preventistas **[EST]**. El canal tradicional, con ~195.000 o más puntos independientes, explica un tercio del consumo masivo y pierde menos que las cadenas. Su abastecimiento depende de pedidos tomados por preventista, teléfono o WhatsApp. Esa es la operación que un SaaS puede digitalizar.

---

## 3. Digitalización de PyMEs y del canal

- **e-commerce B2C:** CACE/Kantar informan **$19,5 billones facturados en el primer semestre de 2026 (+28% nominal)**, 181,5 M de órdenes y un ticket de $107.597. Alimentos y bebidas es el primer rubro por facturación ([Mercado](https://mercado.com.ar/tendencias/cace-el-comercio-electronico-facturo-19-533-815-millones-en-el-primer-semestre)). Con una inflación interanual de ~33%, el crecimiento real es nulo o levemente negativo ([El Economista](https://eleconomista.com.ar/economia/ecommerce-argentina-crece-28-pero-siempre-significa-ganar-mas-n98420/amp)).
- **WhatsApp como canal de venta:** según el reporte NubeCommerce 2026 de Tiendanube, el **71,5% de los emprendedores argentinos vendió por WhatsApp en 2025**, segundo canal después de Instagram ([Wati/Tiendanube](https://www.wati.io/geo-argentina-es/blog/recommended/whatsapp-canal-ventas-pymes-argentina)). No encontramos un dato específico de mayoristas. Por casos y avisos laborales, la toma de pedidos B2B sigue siendo preventista + WhatsApp + Excel ([Develop Argentina](https://developargentina.com/blog/plan-ecommerce-b2b-pymes-industriales-2025)) **[cualitativo]**.
- **B2B en plataformas:** Tiendanube lanzó un **módulo B2B nativo en México (mayo 2026)** para "mover los pedidos mayoristas que miles de PyMEs manejaban por WhatsApp o Excel" ([descubre.vc](https://www.descubre.vc/noticia/tiendanube-registra-mayor-volumen-de-ventas-en-argentina-pero-advierte-sobre-rentabilidad-ajustada-2026-09-18)). Es una validación del problema y, a la vez, una amenaza competitiva si llega a Argentina.
- **Medios de pago en mayoristas (INDEC, julio 2026):** efectivo 24%, "otros medios" (QR, billeteras, transferencias) 34%, crédito 26%, débito 16%. El 78% se factura con comprobante B, es decir a minoristas monotributistas ([INDEC](https://www.indec.gob.ar/uploads/informesdeprensa/autoservicios_mayoristas_09_26DA5CEEFE06.pdf)). Hay espacio para conciliación de cobros digitales y cuenta corriente de clientes.
- **Ventas online de comercios con local:** según CAME, crecieron 19,4% interanual en septiembre de 2026 ([Noticias NQN/CAME](https://www.noticiasnqn.com.ar/noticias/2026/10/04/355263-las-ventas-minoristas-pyme-subieron-0_3por_ciento-en-septiembre)).
- **Brecha de datos:** no encontramos encuestas 2025-26 de la Fundación Observatorio PyME sobre adopción de ERP/CRM en el comercio mayorista. La referencia más citada sigue siendo "Travesía 4.0" (CIPPEC/BID/UIA, 2019), según la cual solo ~6% de las PyMEs industriales tiene tecnología digital avanzada. Suponemos que **menos del 30% de las distribuidoras PyME usa un sistema de pedidos móvil o un portal B2B** **[EST]**.

---

## 4. Contexto macro 2025-2026 y efecto en los mayoristas

| Variable | Dato | Fuente |
|---|---|---|
| Inflación | 1,9% mensual en sept 2026 (1,7% en ago); 23,6% acumulada en el año; **33,4% interanual** | [Canal 26 / INDEC](https://www.canal26.com/economia/2026/10/13/la-inflacion-de-septiembre-fue-de-19-y-acumula-un-alza-de-236-en-lo-que-va-del-2026/) |
| Tipo de cambio | Oficial ~$1.495/$1.545 (1/10/2026), con brecha mínima y techo de banda ~$1.850 | [hacecuentas](https://hacecuentas.com/blog/informe-financiero-argentina-2026-10) (sin verificar con BCRA) |
| Consumo masivo | -3,3% acumulado 2026 (Scentia) | [Bloomberg Línea](https://www.bloomberglinea.com/latinoamerica/argentina/el-consumo-masivo-sigue-sin-recuperarse-en-argentina-y-acumula-una-caida-de-33-en-2026/) |
| Autoservicios mayoristas | -2,7% real en ene-jul 2026; empleo -7,3% interanual | [INDEC](https://www.indec.gob.ar/uploads/informesdeprensa/autoservicios_mayoristas_09_26DA5CEEFE06.pdf) |
| Ventas minoristas PyME (CAME) | +0,3% interanual en sept 2026; -2,1% acumulado | [CAME vía Todo Jujuy](https://www.todojujuy.com/las-ventas-minoristas-pyme-aumentaron-03-interanual-septiembre-n296981) |
| Importaciones de bienes de consumo | ~USD 900-980 M/mes en 2026 (941 M en agosto) | [INDEC ICA](https://www.indec.gob.ar/uploads/informesdeprensa/ica_09_266E5973E036.pdf) |
| Crédito PyME | Tasa activa del BNA ~28-37% TNA; descubierto >45% TNA | [Boletín Oficial](https://www.boletinoficial.gob.ar/detalleAviso/primera/338497/20260218), [Sitio Andino](https://www.sitioandino.com.ar/n/198011-tasas-de-interes-exorbitantes-asfixian-a-las-pymes) (fecha dudosa) |

**Efectos sobre el negocio mayorista y la propuesta de valor:**
1. **Listas de precios que siguen cambiando.** Con inflación de ~2% mensual los proveedores todavía actualizan listas cada 2 a 6 semanas. Hay que propagar esos cambios a miles de SKUs, a varias listas por cliente y canal y a los preventistas en la calle. Es un dolor concreto y automatizable. El dolor es menor que con 2023 (25% mensual), pero ahora **el margen importa más que la cobertura inflacionaria**.
2. **Márgenes comprimidos y volumen estancado.** Con consumo plano o en baja, la ganancia sale de eficiencia (menos errores de pedido, ruteo, menos stock inmovilizado y cobranza) y de vender más por cliente (sugerencias, promociones). CAME menciona presión de costos de reposición y "competencia de canales mayoristas" ([CAME](https://www.noticiasnqn.com.ar/noticias/2026/10/04/355263-las-ventas-minoristas-pyme-subieron-0_3por_ciento-en-septiembre)).
3. **Apertura importadora.** La entrada de importados (textil, bazar, juguetes, electro, ferretería) y la compra directa vía courier presionan a los mayoristas de esos rubros. Los obliga a rotar catálogo más rápido y a manejar costos en USD. Un SaaS que cotice en USD, convierta a ARS y aplique márgenes por lista es un diferencial.
4. **Crédito caro.** La cuenta corriente de clientes, el control de deuda y la cobranza digital (QR, transferencias) liberan capital de trabajo. Hay oportunidad de monetizar con fintech (embedded finance o factoring de cuentas a cobrar).
5. **Tipo de cambio estable.** Permite **cotizar el SaaS en USD con ajuste mensual en ARS**, algo impensable en 2022-23.

---

## 5. Disposición a pagar: precios de SaaS PyME en Argentina

Precios de lista relevados el 20/09/2026 ([SpomSolutions, comparativa](https://app.spomsolutions.com/blog/cuanto-cuesta-erp-argentina-2026); la fuente es un competidor, conviene validarla). USD calculados a ~$1.500 **[EST]**.

| Producto | Plan | ARS/mes + IVA | ≈ USD/mes |
|---|---|---|---|
| Alegra | Emprendedor → Plus | 20.000 → 80.000 | 13 → 53 |
| Contabilium | Standard → Full | 122.000 → 245.000 | 81 → 163 |
| Xubio | Básico → Pro | 123.100 → 375.900 | 82 → 250 |
| Colppy | Essential → Enterprise | 128.500 → 310.900 | 86 → 207 |
| Tango Nube | Básica (2 usuarios) → Pro (5) | 731.000 → 912.000 | 487 → 608 |
| Apps B2B de Shopify (referencia global) | Pro | — | ~20 |

**Conclusiones sobre precios:**
- Una PyME argentina ya paga **USD 80–250/mes** por facturación y gestión. Un ERP de gama media como Tango supera los **USD 500/mes**.
- Un SaaS vertical para distribuidoras (pedidos de preventistas, portal B2B o WhatsApp, listas de precios, cuenta corriente y ruteo) puede cobrar **USD 60–150/mes** a una micro o pequeña y **USD 250–600/mes** a una mediana, con precio por usuario o vendedor. Una referencia es USD 15–25 por preventista por mes **[EST]**.
- **ARPU anual ponderado** usado abajo: conservador USD 720, base USD 1.440, optimista USD 2.400.
- Factores que bajan el precio: hábito de "software pirata o a medida del sobrino", sensibilidad al precio en recesión y la memoria de los cepos. Factores que lo suben: el ahorro en horas de carga de pedidos y errores, y la integración con facturación de ARCA.

---

## 6. TAM / SAM / SOM (USD/año)

**Supuestos explícitos**
- **TAM:** todas las empresas mayoristas, formales e informales, que podrían usar un software de gestión de ventas y pedidos. Conservador 45.000, base 50.000, optimista 55.000 (OEDE 35.379 + autopartes ~2.000 + informales 8.000–18.000 **[EST]**).
- **SAM:** mayoristas y distribuidoras de los rubros "a comercio" (consumo masivo, golosinas, bebidas, limpieza/perfumería, librería, bazar/juguetes/regalería, textil, ferretería/construcción, eléctrico, autopartes), con fuerza de venta o cartera de clientes recurrente y tamaño de pequeña o más (más las micro más activas). Conservador 12.000, base 15.000, optimista 18.000 **[EST, a partir de las 28.000 empresas de esos rubros × 44% pequeñas o más + parte de las micro]**.
- **SOM:** penetración del SAM a 3–5 años: 2% / 5% / 10%.
- **ARPU:** USD 720 / 1.440 / 2.400 por año.

| Escenario | TAM (empresas × ARPU) | SAM | SOM (3-5 años) |
|---|---|---|---|
| Conservador | 45.000 × 720 = **USD 32 M** | 12.000 × 720 = **USD 8,6 M** | 240 clientes × 720 = **USD 0,17 M ARR** |
| Base | 50.000 × 1.440 = **USD 72 M** | 15.000 × 1.440 = **USD 21,6 M** | 750 clientes × 1.440 = **USD 1,1 M ARR** |
| Optimista | 55.000 × 2.400 = **USD 132 M** | 18.000 × 2.400 = **USD 43 M** | 1.800 clientes × 2.400 = **USD 4,3 M ARR** |

**Ingresos adicionales posibles (no incluidos):**
- Take rate o fee sobre pedidos B2B o cobros: en el panel INDEC solo los autoservicios mayoristas facturan unos USD 3.200 M/año, y el universo de distribuidoras PyME probablemente lo multiplica varias veces **[EST]**. Un fee de 0,1–0,3% sobre el GMV que pase por la plataforma puede igualar o superar la suscripción.
- Una "app del comerciante" para los ~195.000 puntos de venta independientes, con monetización indirecta: datos para fabricantes (el tipo de dato que hoy venden NielsenIQ y Scanntech), trade marketing y financiamiento.

**Lectura:** Argentina sola es un mercado **chico a mediano**, con un SAM de ~USD 20 M/año en el escenario base. Alcanza para un negocio rentable de USD 1–4 M de ARR, pero no para un caso de venture a escala sin expansión regional o monetización transaccional.

---

## 7. Expansión a LatAm

| País | Tamaño del universo mayorista | Notas |
|---|---|---|
| **México** | CDMX 16.235 y Edomex 17.839 unidades mayoristas (Censo Económico 2019, [INEGI CDMX](https://en.www.inegi.org.mx/contenidos/programas/ce/2019/doc/mcdmx_ce19.pdf), [INEGI Edomex](https://en.www.inegi.org.mx/contenidos/programas/ce/2019/doc/mmex_ce19.pdf)); nacional **~150.000–170.000** **[EST]**. Censo 2024: 5,47 M de unidades económicas en total ([INEGI](https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2025/ce/CE_2024_Def_EdMx.pdf)) | Mercado 4 a 5 veces más grande que el argentino. Canal tradicional de "tienditas" (~1 M). Hay competencia fuerte (Tiendanube B2B, Jüsto/Frubana, apps de CPG). Pago en USD/MXN más estable. |
| **Chile** | ~1,58 M de empresas (SII 2024, [DF](https://www.df.cl/economia-y-politica/df-tax/ecos-de-la-operacion-renta-sube-cantidad-de-empresas-y-ventas-pero-por)); comercio ~34% (ELE 2017); mayoristas **~25.000–35.000** **[EST]** | Mayor disposición a pagar (ARPU 1,5 a 2 veces el argentino) y facturación electrónica obligatoria (DTE SII). |
| **Uruguay** | **~4.000–6.000** mayoristas **[EST]** | Chico pero cercano culturalmente, dolarizado de hecho, buen mercado piloto. |
| **Paraguay** | **~3.000–5.000** **[EST]** | Hub importador (Ciudad del Este) con mucho comercio mayorista de importados. Facturación electrónica SIFEN en expansión. |

**Potencial regional (base, solo SAM de suscripción) [EST]:** sumando México (~USD 60–90 M), Chile (~USD 15–25 M) y Uruguay+Paraguay (~USD 4–6 M) al SAM argentino (~USD 22 M), se llega a **~USD 100–140 M/año**. La adaptación fiscal (CFDI en México, DTE en Chile, SIFEN en Paraguay) es el principal costo de entrada a cada país.

---

## 8. Advertencias y próximos pasos de validación

1. Las cifras OEDE son **empresas empleadoras**, no establecimientos ni monotributistas. El CNE del INDEC no tiene una edición reciente publicada que permita un recuento completo.
2. La UKRA, CEDEAPSA y las fuentes de precios de software tienen sesgo de parte (cámara o competidor). Hay que validarlas con 20–30 entrevistas a distribuidoras.
3. Para afinar el SAM conviene pedir a ARCA o al GPS de Empresas un cruce CLANAE 46 (rev4) × tramo de facturación × provincia, y mapear socios de las cámaras sectoriales (CADAM, distribuidores de golosinas y bebidas, ferreterías, librerías).
4. Hay que vigilar la llegada a Argentina del módulo B2B de Tiendanube, que hoy está solo en México.
