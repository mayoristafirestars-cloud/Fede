# Sistema tributario argentino y PyMEs (octubre 2026): dolores y oportunidades regtech

> Investigación al 21/10/2026. Las fuentes van entre corchetes. **[EST]** marca estimaciones propias o cálculos ilustrativos. Ojo: muchos portales (iProfesional, Blog del Contador) muestran fechas de 2026 en notas viejas de 2017 a 2024. Las cifras normativas conviene validarlas en el Boletín Oficial, ARCA y los fiscos provinciales antes de usarlas comercialmente.

---

## 1. Resumen ejecutivo

- Una PyME argentina convive con **37 tributos** (18 nacionales, 8 provinciales y 11 municipales) y además con **30 regímenes de retención, percepción e información**. En total son al menos **67 obligaciones distintas**, según el IARAF de enero de 2026 [https://www.bloomberglinea.com/economia/alto-grado-de-complejidad-cuantos-impuestos-paga-una-pyme-en-argentina/].
- La presión tributaria agregada baja (IARAF: 20,8% del PBI nacional y 26,7% consolidado en 2026, la menor en 20 años, sobre todo por la baja de derechos de exportación) [https://www.infobae.com/economia/2026/07/27/por-la-baja-de-las-retenciones-la-argentina-tendra-en-2026-la-menor-presion-tributaria-de-los-ultimos-20-anos/]. Lo que **no baja es la complejidad**, ni la carga de los impuestos "en cascada" (IIBB, cheque, sellos y tasas municipales), que el IARAF estima en alrededor del 8% del PBI sumada a los derechos de exportación.
- **El dolor más caro y menos resuelto es la plata atrapada en saldos a favor de IIBB** que generan SIRCREB, SIRTAC, SIRCUPA, las percepciones en compras y las retenciones de clientes. La encuesta de la UIA a 137 empresas registró **$98.579 millones**, un **promedio de $719 millones por empresa** a marzo de 2025 (+86% interanual). El **77%** pidió devolución y no la consiguió, y el **54%** de los saldos está en provincias donde la empresa ni siquiera tiene establecimiento [https://www.uia.org.ar/politica-tributaria/4167/informe-saldos-a-favor-de-ingresos-brutos-2025/ y https://uia.org.ar/notas/los-saldos-a-favor-de-ingresos-brutos-ya-superan-los-500-millones-por-empresa/].
- **Hay ventanas regulatorias concretas que fuerzan demanda:**
  - **1/12/2026:** ARCA rechaza las facturas electrónicas que no informen la condición frente al IVA del receptor.
  - Embargos de ARCA a personas jurídicas: **+52% interanual** (135.744 medidas entre enero y agosto de 2026), con embargo de cobranzas a clientes del deudor.
  - Nuevo régimen ARBA de "alícuota equilibrada" (RN 38/2025 y RN 18/2026), al que hay que saber entrar.
  - Ampliación de $50.000 millones para devolución de saldos de IVA (agosto de 2026).
- **Oportunidad regtech principal [EST]:** un servicio de "**control y recupero de saldos a favor de IIBB multijurisdicción**" para mayoristas y distribuidoras de Convenio Multilateral. Combinaría conciliación automática de retenciones y percepciones contra padrones y extractos, pedidos de exclusión o atenuación y gestión de devoluciones o compensaciones, y se cobraría con fee mensual más un porcentaje del recupero. Casi no hay jugadores dedicados. Los ERP (Xubio, Colppy, Contabilium, Tango, Holistor) liquidan, pero **no gestionan el recupero**.

---

## 2. Mapa de impuestos que pega a una PyME comercial (2026)

| Nivel | Tributo | Parámetros clave 2026 | Dolor típico |
|---|---|---|---|
| Nacional | **IVA** | General 21%, reducida 10,5% (alimentos básicos y otros), 27% en servicios públicos a inscriptos. Saldo técnico (crédito fiscal mayor que débito) solo trasladable a períodos siguientes. Saldo de **libre disponibilidad** (por retenciones y percepciones de IVA) compensable, devolvible o transferible (RG 5634/2025) [https://rsm.global/argentina/sites/default/files/media/documents/Boletin%20Informativo%201%C2%B0%20Enero%202025.pdf] | Percepciones y retenciones de IVA de grandes agentes que generan saldos. Caputo anunció en agosto de 2026 **$50.000 M extra** para devoluciones, limitado a exportadores, RIMI y saldos de libre disponibilidad [https://eleconomista.com.ar/economia/pymes-caputo-anuncio-una-devolucion-iva-50000-millones-n97111] |
| Nacional | **Ganancias sociedades** | Escala progresiva 25% / 30% / 35% con tramos ajustados por IPC (oct/oct) y 7% sobre dividendos [https://www.iprofesional.com/impuestos/446069-impuesto-a-las-ganancias-arca-publico-la-escala-2026-para-las-empresas]. El proyecto de la reforma laboral proponía bajar a 27% y 31,5%. **No confirmé que haya quedado en la Ley 27.802** | Anticipos sobre utilidades infladas, retenciones de Ganancias sufridas |
| Nacional | **Impuesto a los débitos y créditos (cheque)** | 0,6% + 0,6% (general). Micro y pequeñas computan el 100% a cuenta de Ganancias, medianas tramo 1 industriales el 60%. Micro: hasta 30% a cuenta de contribuciones patronales (tope 15% de la contribución) **hasta dic-2026** [https://www.ambito.com/novedades-fiscales/las-micro-pymes-seguiran-el-beneficio-computar-creditos-y-debitos-bancarios-como-pago-cuenta-contribuciones-patronales-n6231069] | Cascada sobre facturación bruta, muy pesada para alto volumen y bajo margen. El beneficio vence en dic-2026 y no hay cronograma oficial de eliminación (solo la propuesta del IARAF de quitarlo en 3 años) |
| Nacional | **Contribuciones patronales** | 18% (PyMEs e industria) / 20,4% (grandes de comercio y servicios) más obra social y ART, con un costo laboral total del orden del 25-30% sobre el bruto **[EST]**. La **Ley 27.802 de Modernización Laboral** (sancionada el 27/2/2026, Decreto reglamentario 407/2026) creó el Fondo de Asistencia Laboral, que reduce contribuciones hasta 3 puntos, y un incentivo de 48 meses para nuevas contrataciones [https://web.cpcecba.org.ar/?p=64388; https://www.marval.com/Publicacion/el-congreso-aprueba-la-ley-de-modernizacion-laboral-17499] | Liquidación de sueldos compleja, nuevos beneficios que hay que saber pedir |
| Nacional | **Monotributo** | Cuotas desde ago-2026 (+16,8%): cat. A $49.527, D ~$84.600, K $1,61 M (servicios) y $702.103 (bienes) [https://www.iprofesional.com/impuestos/465371-monotributo-cuanto-se-paga-en-octubre-2026-segun-categoria] | Recategorización, exclusiones por cruces bancarios. Muchos proveedores de mayoristas son monotributistas |
| Nacional | **Bienes Personales – acciones y participaciones** | La sociedad paga como responsable sustituto (0,5%) **[verificar alícuota 2026]** | Menor |
| Provincial | **Ingresos Brutos** | Comercio orientativo: CABA 3-5% (escala por ingresos), PBA 3,5-5%, Córdoba 4-5% (baja a 2,5% para ingresos 2025 ≤ $88,1 M), Santa Fe 4-4,5%, Mendoza 3-4% [https://yo-facturo.com/blog/ingresos-brutos-2026-todas-las-provincias/; https://legislaturacba.gob.ar/informe-de-sintesis-presupuesto-2026-y-normativa-tributaria-para-la-provincia-de-cordoba]. Mayoristas con alícuotas algo menores que minoristas, según la provincia. Convenio Multilateral: CM03 y CM04 mensual, CM05 anual (coeficientes), por SIFERE | **El impuesto más distorsivo**: cascada, 24 fiscos con normas distintas, regímenes de recaudación superpuestos |
| Provincial | **Sellos** | ~1-1,2% sobre contratos (varía) **[EST]** | Contratos de distribución, mutuos, prendas |
| Municipal | **Tasa de Seguridad e Higiene (TISH / DReI)** | Se cobra **sobre facturación** (de hecho funciona como un "IIBB municipal"). Hay municipios con alícuotas de 0,5-1%+ y aumentos fuertes: en Mendoza, Guaymallén acumuló +22% en 2025, y la Capital de Catamarca anunció subas de hasta 120% en 2026 [https://www.losandes.com.ar/politica/a-pagar-cuanto-subieron-las-tasas-municipales-y-cual-es-la-comuna-aumento-cero-n5980458; https://www.elancasti.com.ar/politica-y-economia/advierten-que-la-municipalidad-la-capital-aumentara-120-algunos-tributos-n512487] | Crece la litigiosidad: la SCBA exige una prestación "concreta, efectiva e individualizada" (Coca-Cola FEMSA c/ La Matanza) [https://www.ambito.com/economia/tasas-municipales-cada-vez-mas-empresas-cuestionan-impuestos-comunales-la-justicia-n6093656]. Algunos municipios cobran tasas a empresas sin local (venta online o por distribución) |

**Ranking internacional:** el último *Paying Taxes / Doing Business* del Banco Mundial (2019-2020) ubicaba a Argentina en el **puesto 169 de 190 en pago de impuestos**, con **311-312 horas anuales** de cumplimiento y una **tasa total sobre utilidades de ~106%**. El índice se discontinuó en 2021, pero sigue siendo la referencia [https://eleconomista.com.ar/negocios/doing-business-2019-argentina-esta-ubicada-posicion-119-n21569; https://www.ambito.com/opiniones/impuestos/las-empresas-argentinas-invierten-312-horas-al-ano-pagar-n5108876]. Para comparar: OCDE de altos ingresos ~159 h y Singapur 49 h.

---

## 3. El dolor estrella: retenciones, percepciones y saldos a favor de IIBB

### 3.1 Cómo se arma la trampa

Una distribuidora sufre IIBB "por adelantado" por cuatro vías simultáneas, todas calculadas **sobre montos brutos**:

1. **Percepciones en compras:** el proveedor, si es agente ARBA, AGIP, API, etc., le percibe un % según el padrón de riesgo. ARBA usaba 16 grupos de alícuotas fijas.
2. **SIRCREB:** retención sobre **cada acreditación bancaria** (cobros, transferencias), con alícuotas según padrón, que en la práctica van de ~0,01% a 5% según la jurisdicción y el riesgo **[EST]**. Se suman SIRCUPA (billeteras virtuales) y **SIRTAC** (tarjetas).
3. **Retenciones de clientes agentes:** supermercados, cadenas y grandes empresas.
4. **Retenciones o percepciones aduaneras** en importaciones.

Para un negocio de **margen bajo y alto volumen** (mayorista con margen bruto del 8-15%), el impuesto real se calcula sobre la venta, pero los anticipos se acumulan sobre compras y sobre cobros, y además en jurisdicciones donde el coeficiente de Convenio es chico. La UIA mide que **la alícuota efectiva termina ~80% por encima de la nominal**: industria nominal 2,4% contra 3,35% efectiva con anticipos [https://www.ambito.com/novedades-fiscales/saldos-favor-ingresos-brutos-una-preocupacion-que-no-encuentra-solucion-n5990284].

### 3.2 Magnitud (datos duros)

- **UIA, encuesta 2025** (137 empresas): **$98.579 M** acumulados, un **promedio de $719 M por empresa**, +86% nominal en un año. El 54% de los saldos está en provincias donde la empresa no tiene establecimiento. El **77%** pidió devolución sin éxito [https://www.uia.org.ar/politica-tributaria/4167/informe-saldos-a-favor-de-ingresos-brutos-2025/; https://uia.org.ar/notas/los-saldos-a-favor-de-ingresos-brutos-ya-superan-los-500-millones-por-empresa/].
- **UIA, encuesta 2024** (107 empresas): $41.285 M, promedio $526 M. En **comercio** (10 empresas): $3.567 M, promedio **$357 M**. El **14%** considera su saldo "irrecuperable" [https://www.cronista.com/economia-politica/ingresos-brutos-hay-mas-empresas-obligadas-a-retener-y-crecen-los-saldos-irrecuperables/].
- **Tiempos de recupero (UIA 2023):** 39,6% tarda de 1 a 12 meses, 23,2% un año o más, 11,2% de 1 a 3 años y 10,8% lo da por perdido. Los regímenes más problemáticos son **SIRCREB y SIRTAC**, y las provincias más difíciles para recuperar son Misiones, Catamarca, Santiago del Estero y Córdoba [https://www.ambito.com/novedades-fiscales/saldos-favor-ingresos-brutos-una-preocupacion-que-no-encuentra-solucion-n5990284].
- **KPMG:** solo el **16%** de los contribuyentes relevados **no** tiene saldos a favor de IIBB [https://kpmg.com/ar/es/home/media/novedades-tax/2025/11/novedades-clave-en-impuestos-indirectos.html].
- **ARBA** reconoce que su stock de saldos a favor llegó a equivaler a **~3 meses de recaudación** y dice haberlo bajado a 0,9 meses [https://www.canal26.com/economia/2026/03/02/la-herramienta-de-arba-que-evita-saldos-a-favor-y-acelera-devoluciones-como-acceder/].
- **Los umbrales para ser agente están desactualizados:** San Juan ~$1 M de ventas anuales (sin actualizar desde 2010) y Santiago del Estero desde 2017. Eso convierte a muchas PyMEs en **agentes de recaudación**, con costo de sistemas y riesgo de multas. En PBA el umbral es de $3.900 M para percepción mayorista en ciertos rubros (RN 7/2026) [https://www.cronista.com/economia-politica/ingresos-brutos-hay-mas-empresas-obligadas-a-retener-y-crecen-los-saldos-irrecuperables/; https://kpmg.com/ar/es/home/media/novedades-tax/2026/02/05-de-febrero.html].

### 3.3 Estimación para una distribuidora típica [EST, cálculo ilustrativo]

Supuestos: ventas de $1.000 M por mes (~US$ 0,7 M) y compras de $870 M por mes (margen bruto del 13%). La empresa está en Convenio Multilateral: 70% PBA, 20% CABA y 10% otras.

| Concepto mensual | Supuesto | Monto |
|---|---|---|
| IIBB determinado | ~1,5-2% promedio ponderado (mayorista) | $15-20 M |
| Percepciones sufridas en compras | 1,5-2,5% sobre $870 M | $13-22 M |
| SIRCREB sobre cobros bancarizados | 0,8-1,5% sobre ~$800 M | $6-12 M |
| Retenciones de clientes grandes y SIRTAC | 0,5% sobre ventas | $5 M |
| **Anticipos totales** | | **$24-39 M** |
| **Saldo a favor que se acumula** | anticipos menos impuesto | **$4-24 M por mes, es decir $50-290 M por año** |

Con inflación del 25-30% anual, cada $100 M inmovilizados por un año pierden ~$20-25 M en términos reales, más el costo de oportunidad del capital de trabajo (tasas activas PyME). **Para un mayorista que gana el 2-3% neto sobre ventas, un saldo inmovilizado equivalente a 1-2 meses de ganancia no es raro.** Esto coincide con el orden de magnitud de la UIA para comercio (~$357 M promedio en 2024).

**Proyección de mercado [EST]:** si en el país hay unas 15.000-25.000 empresas comerciales e industriales de Convenio Multilateral con saldos relevantes y un promedio de $100-500 M cada una, el stock atrapado rondaría **$1,5-12 billones**. Es muy grueso y sirve solo como orden de magnitud.

### 3.4 Herramientas para destrabar (y por qué cuestan)

- **Certificados de exclusión o atenuación:** reducen las **retenciones, no siempre las percepciones**. Cada provincia tiene su propio trámite y vencimiento, y **CABA no tiene certificado de no retención**: solo compensación (Res. AGIP 352/2022) o atenuación [https://eleconomista.com.ar/economia/saldos-favor-cuales-son-opciones-recuperarlos-ganancias-iva-e-ingresos-brutos-n97603].
- **ARBA "Riesgo 0 – SAF 0" / alícuota equilibrada** (RN 38/2025 y RN 18/2026, vigente desde el 24/7/2026): recálculo individual de alícuotas y ajuste automático de oficio. **~12.000 PyMEs adheridas en el primer trimestre de 2026**. Exige riesgo fiscal adecuado y no tener deudas como agente [https://www.lacapitalmdp.com/mas-de-12-000-pymes-ya-se-sumaron-al-nuevo-regimen-de-arba-que-evita-acumulacion-de-saldos-a-favor-en-ingresos-brutos/; https://contadoresenred.com/arba-suma-requisitos-para-acceder-al-beneficio-de-alicuota-equilibrada-riesgo-0-saf-0/amp/].
- **ARBA, demanda de repetición digital (RN 16):** hasta **$3,5 M en 72 horas** y compensación inmediata con deudas. Para montos de mayoristas (cientos de millones) el trámite sigue siendo el ordinario.
- **CABA:** devolución expeditiva hasta $15 M. Hay imputación recíproca CABA–Santa Fe (Res. AGIP 535/2025), un primer "clearing" interjurisdiccional [https://www.airedesantafe.com.ar/santa-fe/santa-fe-y-ciudad-buenos-aires-implementan-un-sistema-inedito-devolver-ingresos-brutos-n635767/amp].
- **Entre Ríos (ATER):** app para reducir la alícuota de SIRCREB y SIRCUPA. **La Pampa:** exclusión de oficio de pequeños contribuyentes (RG 11/2026). **ARBA RN 10/2026:** exclusión de cuentas recaudadoras [https://siap.blogdelcontador.com.ar/?p=85809].
- **Vía judicial:** acción de repetición o amparo para salir del padrón. Lenta y cara [https://www.consejosalta.org.ar/2015/09/como-lograr-en-la-justicia-la-devolucion-de-saldos-a-favor-de-ingresos-brutos-y-ser-excluido-del-padron-de-retenciones/].

**Conclusión:** la solución existe, pero está **fragmentada en 24 fiscos, con requisitos cambiantes, vencimientos de certificados y conciliaciones manuales**, que es justo el tipo de trabajo que el software y los agentes de IA hacen bien.

---

## 4. Factura electrónica y cumplimiento formal (2025-2026)

- **Condición frente al IVA del receptor (RG 5616/2024):** obligatoria por web service desde el 15/4/2025, con **rechazo automático de la solicitud de CAE desde el 1/12/2026** si el campo va vacío. ARCA ya mandó notificaciones. Alcanza a monotributistas (factura C). **Los sistemas propios o integrados por web service son los más expuestos** [https://siap.blogdelcontador.com.ar/?p=90212; https://tributosimple.com/arca-rechazara-facturas-electronicas-si-no-informas-la-condicion-frente-al-iva-de-tu-cliente/]. Es una oportunidad de corto plazo: auditar y adaptar integraciones de facturación de mayoristas con ERPs caseros.
- **RG 5866/2026** (29/6/2026): nuevo esquema de facturación para seguros y entidades financieras, escalonado entre 1/9/2026 y 1/3/2027, y actualización del régimen de puntos de venta [https://siap.blogdelcontador.com.ar/?p=86043].
- **Régimen de Transparencia Fiscal al Consumidor (Ley 27.743, RG 5614/2024):** desde el 1/4/2025 es obligatorio discriminar IVA e impuestos internos nacionales en tickets y facturas a consumidor final. Las provincias y municipios fueron *invitados* a sumar IIBB y tasas, con adhesión despareja [https://blogdelcontador.com.ar/news-45389-transparencia-fiscal-arca-resolucion-general-5614-2024].
- **FCE MiPyME:** obligatoria cuando una PyME factura a una "empresa grande" por encima del mínimo. El monto fue de **$5.549.862 desde el 14/4/2026**, según una fuente secundaria (verificar en ARCA) [https://siap.blogdelcontador.com.ar/categoria_normativa/factura-de-credito-electronica-mipyme-fce/]. Las distribuidoras que venden a supermercados o cadenas emiten y gestionan FCE: aceptación, rechazo, plazos y negociación en el MAV. Hay un nicho en la gestión de cobro y descuento de FCE.
- **Libro IVA Digital, SIRE (retenciones y percepciones de IVA y Ganancias), SIFERE y SIRCAR:** múltiples aplicativos donde hay que **conciliar los "mis retenciones" contra la contabilidad**.

---

## 5. Fiscalización, penalidades y costo de cumplir

- **Embargos de ARCA:** **135.744 medidas** contra personas jurídicas entre enero y agosto de 2026 (**+52%**). ARCA pasó a **notificar a los clientes** del deudor para que depositen las cobranzas en el fisco. Hay planes de pago caídos sin renegociación. CAME y FAPCEP piden un régimen especial PyME. Solo hubo alivio para clínicas y sin fines de lucro [https://www.lagaceta.com.ar/nota/1139877/economia/crece-presion-pymy-profesionales-para-arca-habilite-planes-pago-frene-embargos.html; https://www.ambito.com/economia/arca-crece-la-presion-planes-pago-y-suspension-embargos-contras-las-pymes-n6285505; https://www.noticiasnqn.com.ar/noticias/2026/05/15/335346-arca-comenzo-a-ejecutar-embargos-sobre-cuentas-de-pymes]. Es una oportunidad para alertas tempranas (deuda en cuenta corriente ARCA y domicilio fiscal electrónico), armado de planes y monitoreo de ejecuciones fiscales.
- **Cruces de datos:** ARCA cruza facturación electrónica, acreditaciones bancarias y en billeteras, SIRCREB, padrones y el "SIPER" de riesgo. Los fiscos provinciales hacen lo propio. Las inconsistencias empeoran la categoría de riesgo, y con eso **suben las alícuotas de percepción y retención**: un círculo vicioso.
- **Costo de contadores [EST]:** los consejos profesionales publican honorarios *sugeridos* indexados por IPC (CPCECABA desde mar-2024), pero no son obligatorios [https://www.econoblog.com.ar/135797/actualizan-honorarios-de-contadores-por-ipc-desde-marzo-de-2024]. En el mercado, una SRL o SA comercial con IVA, IIBB en Convenio y 10-30 empleados paga típicamente **$400.000-1.500.000 por mes** por abono contable e impositivo, más sueldos por legajo y balance anual aparte. **Estimación no verificada con tabla oficial.** El recupero de saldos y los certificados de exclusión suelen cobrarse aparte o directamente no se hacen.
- **Horas:** la referencia es de ~311 horas al año (Banco Mundial). Para un mayorista multijurisdicción con agentes de recaudación propios es plausible duplicarlo **[EST]**.

---

## 6. Informalidad e "Inocencia Fiscal"

- **Informalidad laboral (INDEC, EPH):** **45% en el segundo trimestre de 2026** (+1 punto interanual), unas **6,1 millones de personas** de 13,6 millones de ocupados. Crece la proporción de cuentapropistas [https://www.noticiasnqn.com.ar/noticias/2026/09/17/353002-el-desempleo-volvio-a-subir-en-argentina-llego-al-7_9por_ciento-y-crecio-la-informalidad; https://chequeado.com/el-explicador/la-desocupacion-fue-del-78-en-el-comienzo-de-2026-aumento-la-informalidad-y-la-subocupacion/]. Para mayoristas implica clientes minoristas informales o monotributistas que compran "en negro" y presionan para vender sin factura, y competencia desleal.
- **Ley 27.799 de Inocencia Fiscal** (BO 2/1/2026; Decreto 93/2026; RG ARCA 5820/2026): régimen simplificado de Ganancias para personas humanas con ingresos de hasta $1.000 M y patrimonio de hasta $10.000 M, con presunción de exactitud y efecto liberatorio. Sube el umbral de evasión simple a **$100 M** y el de agravada a $1.000 M, y la prescripción baja a 3 años [https://abogados.com.ar/reglamentacion-de-la-ley-de-inocencia-fiscal-prescripcion-y-dj-simplificada-de-impuesto-a-las-ganancias/38522; https://web.cpcecba.org.ar/?p=63368].
- **"Inocencia Fiscal II"** (proyecto enviado el 24/7/2026, **no sancionado** a la fecha consultada): elimina los topes, pone la carga de la prueba en ARCA, exige bancarización (art. 40 bis) y prevé devolución con intereses en 45 días hábiles si se anula una determinación [https://www.ambito.com/opiniones/dolares-del-colchon-que-cambia-el-proyecto-inocencia-fiscal-ii-el-regimen-simplificado-ganancias-n6305445]. Implicancia: **se formaliza capital ("dólares del colchón")** de dueños de PyMEs, lo que abre demanda de asesoramiento para reingresar fondos, bancarizar y profesionalizar la gestión.

---

## 7. Cambios en camino (2026-2027)

- **Reforma "escalonada" de Caputo** (anunciada en nov-2025): baja progresiva de IVA, impuesto al cheque y derechos de exportación, eliminación de ~20 tributos menores e invitación a provincias y municipios a bajar IIBB y tasas, con un posible nuevo Consenso Fiscal [https://blogdelcontador.com.ar/news-46356-que-impuestos-bajaran-primero-y-cuales-se-eliminaran-con-la-reforma-tributaria-escalonada-de-caputo; https://www.cronista.com/economia-politica/caputo-quiere-eliminar-impuestos-y-bajar-ingresos-brutos-cuales-son-los-limites-reales/]. **No hay cronograma legal** para eliminar el impuesto al cheque. El IARAF propone eliminarlo en 3 años [https://www.forbesargentina.com/money/argentina-utopica-cuando-podrian-eliminar-impuesto-cheque-retenciones-n67381/amp].
- **Ley 27.802 (Modernización Laboral, 2026):** FAL, reducción de contribuciones, actualización de quebrantos y RIMI (Decreto 242/2026, con devolución de IVA por inversiones para MiPyMEs) [https://ecosistemastartup.com/arca-aumenta-50-000m-para-devolver-iva-a-pymes-requisitos-2026/].
- **Provincias:**
  - ARBA (Girard) pide una reforma nacional, pero la condiciona al crecimiento [https://eleconomista.com.ar/economia/arba-pidio-una-reforma-tributaria-nacional-propone-pacto-privados-bajar-impuestos-como-funcionaria-n97712/amp].
  - Córdoba bajó la alícuota de comercio para los chicos.
  - CABA pasó a escalas progresivas por ingresos (junio de 2026).
  - En Catamarca hay un proyecto para eliminar IIBB entre 2027 y 2029 [https://www.elancasti.com.ar/edicion-impresa/monti-insiste-la-eliminacion-los-ingresos-brutos-n617544/amp].
  - La Corte (caso Pernod Ricard) declaró inconstitucionales las alícuotas diferenciales por radicación, una "aduana interior", lo que habilita reclamos de repetición.
- **Lectura de riesgo para el negocio:** la eliminación de IIBB **no es inminente**. Incluso si avanza, los regímenes de recaudación y el stock de saldos a favor van a seguir **3-5 años o más [EST]**. Un producto de recupero de saldos tiene horizonte, aunque conviene diseñarlo para pivotear hacia "cumplimiento multi-fisco" en general.

---

## 8. Matriz de dolores y oportunidades

| # | Dolor | Quién lo sufre | Tamaño en plata o tiempo [EST salvo cita] | ¿Lo resuelve software, IA o servicio? | Competencia actual |
|---|---|---|---|---|---|
| 1 | **Saldos a favor de IIBB inmovilizados** | Mayoristas, distribuidoras, industria, todo contribuyente de CM | $50-300 M por año por distribuidora mediana. Promedio UIA $719 M por empresa | **Sí, alto potencial.** Conciliación automática de "Mis retenciones" (ARBA, AGIP, SIRCREB, SIRTAC, SIFERE) contra el libro, detección de percepciones mal aplicadas (alícuota de padrón incorrecta), proyección del saldo, armado y seguimiento de certificados de exclusión, atenuación, alícuota equilibrada ARBA, compensaciones y demandas de repetición. Modelo: SaaS más *success fee* del 5-15% de lo recuperado o liberado | Casi nula y específica. Estudios tributarios grandes (Big 4, Tristán y Asociados) lo hacen *ad hoc* y caro. ERPs que solo registran |
| 2 | Liquidación IIBB Convenio Multilateral (coeficientes, CM03, CM05, SIFERE) y agentes de recaudación (DDJJ de retenciones y percepciones, padrones) | PyMEs que venden en varias provincias, PyMEs nombradas agentes por umbrales viejos | Horas de contador por mes. Multas por agente | Sí. Hay oferta parcial | Holistor, Tango, Bejerman, Contabilium, SOS-Contador (7.000+ contadores), **Genio Contable** (IA, mayo de 2026, concilia ARCA, AGIP y ARBA y promete -83% de trabajo operativo) [https://www.iprofesional.com/impuestos/454685-son-argentinos-y-crearon-una-ia-que-permite-liquidar-impuestos-facil-como-funciona], librería open source @ar-agents/iibb |
| 3 | Rechazo de facturas desde el 1/12/2026 y cumplimiento de FE, FCE y Transparencia Fiscal | Empresas con sistemas propios, integraciones por web service, mayoristas con ERPs viejos | Si no factura, no vende | Sí, servicio de corto plazo: auditoría y adaptación de integraciones, middleware de facturación | Proveedores de FE (Xubio desde ~$123.000 + IVA por mes el plan básico, según un competidor [https://app.spomsolutions.com/comparar/alternativas-a-xubio]), TusFacturas, Contabilium |
| 4 | Embargos, intimaciones, deuda ARCA y planes caídos | PyMEs con baches de caja | 135.744 embargos entre enero y agosto de 2026 (+52%) | Sí: monitoreo diario del domicilio fiscal electrónico (ARCA y provincias), alertas, simulador de planes, gestión de cautelares | Contadores. No hay un producto masivo de "alerta fiscal" |
| 5 | Tasas municipales (TISH) sobre facturación, en aumento | Comercios con varias sucursales o venta a varios municipios | Hasta 1% o más de la facturación, con subas del 20-120% | Parcial: auditoría de base, reclamo y repetición por falta de prestación (jurisprudencia SCBA), mapa de alícuotas | Estudios jurídicos tributarios |
| 6 | Saldos de libre disponibilidad de IVA y Ganancias (retenciones y percepciones) | Exportadores, PyMEs que venden a grandes agentes | Variable. Nuevo cupo de $50.000 M para devoluciones | Sí: detección de elegibilidad, armado de trámites de devolución o transferencia (RG 5634) | Estudios. Algunos fintech de transferencia de saldos (mercado gris) |
| 7 | Complejidad general (67 obligaciones, 311 h/año) y costo de contadores | Toda PyME | $400 k-1,5 M por mes de honorarios [EST] | IA asistente para estudios contables (B2B2B): el canal de distribución es el contador | Genio Contable, Acont, SOS-Contador, Colppy, Xubio |

---

## 9. Recomendación para el equipo

1. **Producto núcleo:** "**Recupero y prevención de saldos a favor de IIBB**" para mayoristas y distribuidoras de Convenio Multilateral, con facturación de $300 M a $20.000 M al año.
   - Paso 1: un **diagnóstico gratuito** que conecta credenciales (clave fiscal, CIT ARBA, AGIP), baja retenciones y percepciones de los padrones y de "Mis retenciones" y calcula el saldo inmovilizado y la pérdida real por inflación.
   - Paso 2: cobrar un fee mensual de **US$ 150-500 [EST]** más un **éxito del 5-10% sobre el saldo liberado**, sea por devolución, compensación o reducción de alícuota futura.
   - Gancho de venta: "tenés $X millones atrapados".
2. **Canal:** vender a través de estudios contables, con *white label* o revenue share, porque son los que hoy tienen la clave fiscal y la relación. También a través de cámaras: CADAM (distribuidores y autoservicios mayoristas, que ya reclama por saldos técnicos [https://www.lagaceta.com.ar/nota/1042162/economia/por-caida-consumo-presion-impositiva-comerciantes-mayoristas-pidieron-medidas-urgentes.html]), CAME, FECOI y federaciones de distribuidores.
3. **Módulos adyacentes de rápida monetización:**
   - Chequeo de FE antes del 1/12/2026 (urgente, ventana de 6 semanas).
   - Alerta de embargos y deuda.
   - Mapa y auditoría de tasas municipales.
4. **Riesgos:**
   - Cambios normativos constantes, con 24 fiscos y más de 2.000 municipios.
   - Depender de *scraping* de portales fiscales (no hay APIs públicas para todo).
   - Resistencia de contadores si se sienten reemplazados (posicionarse como su herramienta).
   - Eventual baja de IIBB a largo plazo.
   - Datos sensibles (claves fiscales): exige seguridad y un marco contractual.

---

### Datos a verificar antes de usar comercialmente
- Montos exactos de la escala de Ganancias para sociedades 2026 y si la Ley 27.802 bajó las alícuotas.
- Alícuotas vigentes de IIBB mayorista por provincia (Leyes Impositivas 2026) y de SIRCREB por jurisdicción.
- Mínimo de FCE ($5.549.862) en el micrositio de ARCA.
- Estado parlamentario de "Inocencia Fiscal II".
- Honorarios contables reales: encuesta propia a 10-20 estudios.
