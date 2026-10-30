# G5. Vender servicios y software de IA al mundo desde Argentina (estado a octubre de 2026)

Investigación del 30/10/2026 para Federico. Completa `INFORME.md` y `detalle/05-legal-fiscal.md` y no repite lo local (monotributo, Factura E, Com. "A" 8481, Payoneer/Wise como receptores, percepción del 30%, Ley 25.326 y SAS). Esas partes se citan por referencia.

> **No es asesoramiento legal, fiscal ni contable.** Las normas, los precios y los programas de las plataformas cambian. Antes de decidir la estructura societaria, de facturar al exterior o de firmar un DPA, consultá a un contador argentino con práctica internacional y, si corresponde, a un abogado del país del cliente.

**Marcas de confianza:** **[V]** verificado en fuente primaria (oficial, de la plataforma o de la norma) · **[S]** fuente secundaria (estudio jurídico, blog, prensa, proveedor con interés) · **[E]** estimación o inferencia propia · **[NE]** no encontrado o no verificado en esta ronda. En normas se indica si es **vigente** o **proyecto**. Fuentes numeradas en la sección 9, todas consultadas el 30/10/2026. Cupo de búsquedas: ≈20.

---

## 0. Resumen en 12 líneas

1. **Stripe no acepta cuentas de empresas argentinas.** La lista oficial de países incluye solo Brasil y México en LatAm [V][1]. Para usar Stripe directo hace falta una entidad en un país soportado (por ejemplo, una LLC de EE.UU.).
2. **Paddle (Merchant of Record) es la vía más directa para cobrar SaaS desde Argentina** sin abrir empresa afuera: 5% + USD 0,50 por transacción, con IVA y sales tax incluidos [V][2]. Su documentación muestra Argentina con ventas habilitadas y pago en USD, con retiro a banco o Payoneer [S][7]. Antes de integrar, confirmar el alta de vendedor argentino con Paddle.
3. **Lemon Squeezy está migrando a Stripe Managed Payments**, que **no acepta negocios argentinos** (solo EE.UU., Canadá, Europa y 4 países de Asia-Pacífico). Además **excluye servicios profesionales** y productos con intervención humana [V][3][4][5].
4. **Los servicios de IA (consultoría, implementación, "done for you") no entran en un MoR.** Se facturan como monotributista exportador (Factura E) y se cobran por ACH/SEPA vía Payoneer o Wise (ver 05-legal-fiscal) [V][5].
5. **Una LLC de EE.UU. sale ≈ USD 500 el primer año con Atlas** y después USD 100/año de agente registrado [V][8], más **USD 400/año de impuesto de Delaware** a cada LLC [V][9] y contador. **Form 5472 anual obligatorio**, con **multa de USD 25.000** por no presentarlo [V][10]. **BOI ya no aplica a sociedades de EE.UU.** (regla final del 11/08/2026) [V][11].
6. **UE:** un vendedor no establecido en la UE que vende servicios electrónicos a **consumidores** debe registrarse desde el **primer euro** (OSS no-Unión). El umbral de €10.000 es solo para empresas de la UE [S][12][13]. En B2B se aplica la inversión del sujeto pasivo.
7. **EE.UU.:** el sales tax de SaaS depende del estado. El nexo económico típico es USD 100.000 de ventas por estado y alcanza también a vendedores extranjeros [S][14]. Un MoR lo resuelve.
8. **EU AI Act:** el art. 50 (transparencia, por ejemplo avisar que se habla con una IA) **se aplica desde el 02/08/2026**. El Omnibus (Reg. UE 2026/1744) **no lo postergó** y solo movió el alto riesgo del Anexo III al 02/12/2027 [S][15][16].
9. **GDPR:** Argentina tiene **decisión de adecuación** de la UE, así que no hacen falta SCCs para recibir datos desde la UE [S][ver 05-legal-fiscal fuente 41]. Sí hace falta un DPA (art. 28) y, en general, un **representante en la UE (art. 27)**, salvo tratamiento ocasional [V][17].
10. **SOC 2 cuesta ≈ USD 25.000–60.000 el primer año** con Vanta o Drata más auditor [S][18]. Las pymes rara vez lo piden y no conviene hacerlo antes de que un cliente lo exija.
11. **Mercados:** EE.UU. tiene 36,2 M de small businesses [V][19] y ≈ 496.000 empresas hispanas empleadoras [V][20]. Reino Unido 5,7 M (1,4 M con empleados) [V][21]; España 3,31 M [V][22]; Brasil ≈ 24 M de CNPJ pequeños [S][23]; México ≈ 7 M de establecimientos [S][24].
12. **Orden recomendado:** (1) EE.UU., empezando por pymes hispanas y agencias; (2) España; (3) México; (4) Reino Unido; (5) Chile, Colombia y Perú; (6) Brasil al final.

---

## 1. Mercados objetivo

### 1.1 Comparación

| Mercado | Universo de pymes (fuente) | Idioma | Huso vs. AR (UTC−3) | Cobro desde AR | Competencia y disposición a pagar | Notas |
|---|---|---|---|---|---|---|
| **EE.UU. (general)** | 36.186.089 small businesses (<500 empleados), perfil SBA 2025 con datos de 2022 [V][19]. La mayoría no tiene empleados [E] | Inglés | −1 a −5 h (Este −1/−2 h) [E] | Fácil: ACH a Payoneer; tarjeta con Paddle (MoR) [V][2] | Máxima competencia y máxima disposición a pagar; el mercado de referencia de SaaS pyme [E] | 20 estados con ley de privacidad integral [S][25]; sales tax por estado [S][14] |
| **EE.UU. hispano** | ≈ 496.000 empresas empleadoras de dueños hispanos (8,4% del total, ABS con datos de 2024, publicado el 20/11/2025) [V][20] | Español o bilingüe | Ídem | Ídem | Menos herramientas nativas en español [E, no verificado] | **Cuña natural:** idioma + precio en USD + horario compatible |
| **España** | 3.310.824 empresas activas al 01/01/2025 (INE DIRCE) [V][22]; 54,4% sin asalariados [S][22] | Español | +4/+5 h [E] | SEPA a Wise o Payoneer en EUR; B2B con inversión del sujeto pasivo [S][13] | Precios más bajos que en EE.UU.; mercado pyme muy atomizado [E] | GDPR + AI Act + representante UE [V][17] |
| **Reino Unido** | 5.690.265 empresas privadas; 1.417.730 con empleados (inicio de 2025) [V][21] | Inglés | +3/+4 h [E] | GBP vía Wise o Payoneer [E] | Alta, similar a EE.UU. [E] | UK GDPR (régimen propio) [E] |
| **México** | "Poco más de 7 millones" de establecimientos al cierre de 2024 (Censos Económicos, resultados oportunos); 95,3% micro [S][24] | Español | −3 h [E] | Tarjeta con MoR; transferencias en USD [E] | Precio bajo; el cliente pyme pide factura CFDI deducible [E, confirmar] | El IVA digital para extranjeros en B2C exige registro ante el SAT [E, NE en esta ronda] |
| **Brasil** | ≈ 24 M de pequeños negocios con CNPJ activo en el 4T 2025 (Sebrae sobre datos de la Receita) [S][23] | Portugués | 0 h | Pix y boleto dominan; un MoR resuelve la tarjeta [E] | Ecosistema SaaS local fuerte y barato [E] | Tributación alta sobre la importación de servicios (alícuotas NE) [NE] |
| **Chile, Colombia, Perú** | [NE] en esta ronda | Español | 0 a −2 h | Tarjeta con MoR [E] | Mercados chicos, ticket bajo [E] | Chile y Colombia gravan servicios digitales del exterior en B2C [E, NE] |

**Disposición a pagar software:** no se encontró en esta ronda una fuente primaria comparable entre países [NE]. Los precios de lista de herramientas de EE.UU. ya relevados en `INFORME.md` (AgencyAnalytics, Pipedrive, Gorgias) y las tarifas de agencias de IA (sección 7) sirven de referencia.

### 1.2 Orden recomendado y por qué [E]

1. **EE.UU., empezando por pymes hispanas y agencias que las atienden.** Es el mercado más grande y que mejor paga, y el cobro es el más simple (ACH o MoR). El español es una ventaja frente a la competencia de EE.UU. y el horario es compatible.
2. **España.** Mismo idioma y SEPA, B2B con inversión del sujeto pasivo. Pero el cumplimiento es mayor (GDPR, AI Act, representante en la UE), los precios son más bajos y hay 4–5 h de diferencia.
3. **México.** Idioma y huso razonables. El ticket es menor y la factura deducible (CFDI) complica la venta directa a pymes.
4. **Reino Unido.** Buen poder de compra pero competencia alta y sin ventaja de idioma. Sirve como segundo mercado en inglés.
5. **Chile, Colombia, Perú.** Útiles como pilotos baratos en el mismo huso, pero los tickets son bajos.
6. **Brasil, al final.** Portugués, competencia local fuerte, Pix y una carga tributaria alta para el cliente que importa servicios. Solo con un socio local.

---

## 2. Estructura: ¿monotributo exportador, LLC, e-Residency o SL?

### 2.1 Tabla comparativa

| Opción | Costo inicial | Costo anual | Cuándo conviene | Riesgos y obligaciones |
|---|---|---|---|---|
| **Monotributista exportador (Factura E)** | Ver 05-legal-fiscal | Cuota mensual del monotributo | **Desde el día 1**: servicios a clientes del exterior cobrados por Payoneer o Wise; SaaS vendido por Paddle (MoR) | Las facturas E suman al tope de la categoría (05-legal-fiscal). Sin Stripe directo. Algunos clientes de EE.UU. piden W-8BEN o proveedor de EE.UU. [E] |
| **LLC de EE.UU. (Stripe Atlas)** | USD 500 (incluye tasas estatales y el primer año de agente registrado) [V][8] | USD 100 de agente registrado [V][8] + **USD 400 de impuesto anual de Delaware** (vence el 1 de junio) [V][9] + preparación del 1120 pro forma y el 5472 (honorarios NE) | Clientes de EE.UU. que exigen proveedor de EE.UU. y W-9; necesidad de Stripe directo o Billing; marketplaces o seguros de EE.UU.; más de unos pocos miles de USD por mes [E] | **Form 5472 + 1120 pro forma** cada año, incluso sin ventas; los aportes y retiros del dueño se informan; **multa de USD 25.000** por no presentar [V][10]. BOI: las sociedades de EE.UU. están exentas (regla final del 11/08/2026, vigente desde el 14/08/2026) [V][11]. **Doble tributación:** no hay convenio AR–EE.UU. y Argentina grava la renta mundial [E, confirmar con contador] |
| **Doola / Firstbase** | [NE] precios 2026 no verificados | [NE] | Alternativas a Atlas con paquetes de contabilidad y 5472 | Comparar con Atlas: estado (Wyoming o Delaware), agente registrado, si incluyen el 5472 |
| **e-Residency de Estonia + OÜ** | Tasa estatal de €150 por la e-Residency [V][26] (más costo de la OÜ, NE) | Domicilio y contador en Estonia [NE] | Si se apunta a la UE y se quiere una entidad europea sin mudarse | La e-Residency **no da residencia fiscal**. Una OÜ dirigida desde Argentina puede tener riesgo de establecimiento permanente en AR [E]. Stripe Managed Payments sí admite Estonia (EE) [V][4] |
| **SL en España** | €200–600 de notaría y registro según la vía [S][27]; capital mínimo €1 (Ley Crea y Crece) [S][27] | Gestoría y obligaciones contables [NE] | Solo si Federico se muda a España o tiene socio residente | El administrador no residente de fuera de la UE necesita NIE [S][27]. La sede de dirección efectiva desde AR es un riesgo fiscal [E] |

### 2.2 Cómo funciona la single-member LLC de un no residente [E, confirmar con contador]
- La LLC de un solo socio es una **entidad transparente** (disregarded entity). Si el socio extranjero no tiene renta conectada con EE.UU. (sin oficina ni empleados allá), en general **no paga impuesto federal a la renta**. Igual tiene que presentar el **1120 pro forma + 5472** [V para la obligación de presentar][10].
- Del lado argentino, Federico declara la renta de la LLC como propia. Hay que revisar con un contador el tratamiento de entidades transparentes del exterior, los bienes personales y cómo ingresan los fondos (05-legal-fiscal: la persona física no está obligada a liquidar si los fondos entran a una cuenta USD propia).
- **Regla práctica:** abrir la LLC cuando **un cliente o un canal concreto la exija** (Stripe directo, un marketplace, un contrato, un seguro), no "por las dudas".

---

## 3. Cobro

| Herramienta | ¿Sirve desde AR? | Costo | Qué resuelve | Fuente |
|---|---|---|---|---|
| **Stripe directo** | **No**: Argentina no figura entre los países soportados (en LatAm, solo Brasil y México) | — | — | [V][1] |
| **Paddle (MoR)** | Su documentación muestra Argentina con `allow_sales: true` y pago en USD; retiro a banco o Payoneer [S][7] | **5% + USD 0,50** por transacción; "sin cargos mensuales" [V][2] | Es el vendedor legal: cobra, liquida y presenta IVA y sales tax, fraude y contracargos [V][2] | Confirmar el alta y que el producto sea software (no servicios) [E] |
| **Lemon Squeezy** | Página vigente: 5% + USD 0,50, más cargos extra fuera de EE.UU.; retiros a 200+ países [V][3] | 5% + USD 0,50 [V][3] | MoR | **En migración a Stripe Managed Payments** (blog del 28/01/2026) [V][5]. **No conviene empezar acá** [E] |
| **Stripe Managed Payments** | **No** para negocios argentinos (solo CA, US, 31 países de Europa, AU, HK, JP, SG) [V][4] | [NE]; un agregador menciona ≈ 3,5% adicional sin confirmar [S][6] | MoR en más de 80 países; **excluye servicios profesionales** y productos con intervención humana [V][4] | Opción si hay LLC de EE.UU. o OÜ estonia |
| **Payoneer / Wise** | Sí (ver 05-legal-fiscal) | Ver 05-legal-fiscal | Recibir ACH, SEPA o GBP por **servicios** facturados con Factura E | 05-legal-fiscal |

**Impuestos indirectos al vender afuera:**
- **UE, B2C:** quien no está establecido en la UE y vende servicios electrónicos a consumidores usa el **OSS no-Unión** en el país de la UE que elija, **sin umbral** (desde la primera venta). El umbral de €10.000 aplica solo a empresas de la UE [S][12][13]. **UE, B2B:** inversión del sujeto pasivo; validar el NIF-IVA del cliente en VIES [E].
- **EE.UU.:** después de *Wayfair*, cada estado fija su nexo económico. Lo típico es **USD 100.000** de ventas (algunos estados eliminan el criterio de 200 transacciones); California y Nueva York tienen umbrales mayores [S][14]. Un fabricante de software de tasas cuenta **25 jurisdicciones que gravan SaaS** [S][14]. Los vendedores extranjeros no están exentos [S][14].
- **Conclusión [E]:** para SaaS vendido con tarjeta a muchos clientes chicos, **un MoR (Paddle) evita registrarse en OSS y en estados de EE.UU.** El 5% es caro frente a Stripe (≈ 3%), pero reemplaza contador internacional y software de impuestos. Para servicios B2B facturados a pocas empresas, la factura directa con Payoneer o Wise es más barata y el IVA no suele recaer sobre el prestador extranjero en B2B [E].

---

## 4. Cumplimiento para vender afuera

### 4.1 GDPR (UE) — vigente
- **Transferencias:** la UE reconoce a Argentina como país adecuado; la decisión se ratificó en 2024 (05-legal-fiscal, fuente 41) [S]. Recibir datos de clientes europeos en Argentina **no requiere SCCs**. Los subencargados de EE.UU. (OpenAI, AWS) se cubren con el EU-US Data Privacy Framework o con SCCs del proveedor [E, verificar estado del DPF a 2026].
- **DPA (art. 28):** obligatorio cuando Federico es encargado del tratamiento. Conviene una plantilla propia con lista de subencargados [E].
- **Representante en la UE (art. 27):** lo exige el art. 27(1) a quien está fuera de la UE y entra en el art. 3(2). Hay excepción para tratamiento **ocasional**, que no incluya a gran escala categorías especiales y que sea poco probable que genere riesgo [V][17]. Un SaaS con clientes europeos recurrentes probablemente no califica como ocasional [E]. Hay servicios de representante desde unos cientos de euros por año [NE, no verificado].

### 4.2 EU AI Act — Reglamento (UE) 2024/1689, modificado por el Omnibus Reg. (UE) 2026/1744
- **Omnibus:** según fuentes secundarias, firmado el 08/07/2026 y **vigente desde el 27/07/2026** [S][16]. Gibson Dunn (27/05/2026) describía el acuerdo antes de su publicación [S][15].
- **Art. 50 (transparencia, riesgo limitado): se aplica desde el 02/08/2026 y el Omnibus no lo modificó** [S][15][16].
  - Un **chatbot o agente de voz** que interactúa con personas debe avisar que es una IA (proveedor).
  - Los **contenidos generados** deben llevar una marca legible por máquina (art. 50(2)). Los sistemas que ya estaban en el mercado antes del 02/08/2026 tienen hasta el **02/12/2026**; los nuevos deben cumplir desde el lanzamiento [S][15][16].
  - Los **deepfakes** deben declararse (deployer).
- **Alto riesgo (Anexo III), por ejemplo empleo o crédito:** pasó del 02/08/2026 al **02/12/2027**; los productos del Anexo I, al 02/08/2028 [S][15][16]. **No entrar en scoring de crédito ni en selección de personal para la UE** en esta etapa [E].
- **Alfabetización en IA (art. 4):** vigente desde el 02/02/2025. El Omnibus la suaviza a "apoyar" la alfabetización del personal [S][15].
- **Para Federico [E]:** voz o WhatsApp con IA para clientes europeos implica aviso explícito de IA (que ya se recomienda en Argentina), registro de qué modelo se usa y marca de contenido si genera imágenes, audio o video.

### 4.3 Leyes de privacidad estatales de EE.UU. — vigentes
- **20 estados** con ley integral (19 sin contar Florida) a agosto de 2026. Indiana, Kentucky y Rhode Island rigen desde el 01/01/2026 [S][25]. No hay ley federal [S][25].
- Los umbrales suelen ser altos: Rhode Island y Connecticut tienen el más bajo, 35.000 consumidores [S][25]. Una pyme cliente puede no estar alcanzada, pero **los contratos con "processors" son obligatorios cuando sí lo está**, y cada vez más pymes piden un DPA estándar [E].

### 4.4 SOC 2
- **Costo:** primer año con Vanta o Drata más auditor ≈ **USD 30.000–60.000** según un tercero; Drata lo estima entre USD 25.000 para una startup chica y más de USD 200.000 para una grande. Las plataformas cuestan ≈ USD 7.500–15.000 por año y el auditor ≈ USD 7.500–50.000 (Tipo 1) o USD 12.000–100.000+ (Tipo 2) [S][18]. Son cifras de proveedores con interés: pedir cotización.
- **Cuándo [E]:** las pymes casi nunca lo piden. Lo piden las empresas medianas, los clientes regulados (salud, finanzas) y los partners grandes. Mientras tanto alcanza con un *security overview* de 2 páginas, MFA, cifrado, retención cero en los proveedores de IA, DPA y lista de subencargados.

### 4.5 Seguros (E&O tecnológico y cyber)
- **EE.UU.:** Vouch informa medianas para startups de ≈ **USD 3.700/año** de E&O tecnológico (rango 1.300–12.400) y ≈ **USD 2.900/año** de cyber. Insureon da promedios más bajos (≈ USD 807–1.320/año de E&O) y TechInsurance ≈ USD 1.799/año de cyber para empresas de software [S][28].
- **Ojo [E]:** estas aseguradoras suelen exigir una entidad y operaciones en EE.UU. Desde un monotributo argentino puede ser difícil contratar. Es otra razón para la LLC cuando un cliente exija seguro en el contrato. Mientras tanto, **limitar la responsabilidad por contrato** (tope = lo cobrado en 12 meses).

---

## 5. Canales de distribución global

| Canal | Costo o condición (fuente) | Comentario [E] |
|---|---|---|
| **Shopify App Store** | Registro único de USD 19; **0% de comisión sobre el primer USD 1 M** de ingresos brutos acumulados (contados desde el 01/01/2025), 15% por encima; 2,9% de procesamiento aparte [V][29] | El canal pyme más eficiente si el producto es para ecommerce. Shopify factura al comerciante, así que resuelve el cobro desde AR |
| **HubSpot App Marketplace** | Requiere **3 instalaciones activas** de cuentas no afiliadas, OAuth, revisión manual de unos 10 días hábiles; la página de requisitos no menciona revenue share [V][30] | Bueno para apps de agencias y CRM; cobrás por tu cuenta (MoR) |
| **QuickBooks (Intuit App Partner Program)** | [NE]: la página no cargó; existe un programa con niveles y cobro por llamadas a la API (no verificado) | Claude for Small Business se centra en QuickBooks (INFORME): competencia directa |
| **Xero App Store** | [NE]: página con acceso restringido | — |
| **Zapier / Make / GoHighLevel** | [NE] tarifas de partner en esta ronda | GoHighLevel es relevante para agencias de EE.UU. que revenden; valida demanda hispana [E] |
| **AWS Marketplace** | SaaS de oferta pública **3%**; oferta privada 3% (<USD 1 M), 2%, 1,5%; renovaciones 1,5%; servicios profesionales 0,5% desde junio de 2026 [V][31] | No sirve para pymes; útil solo con clientes medianos o grandes que compran con su compromiso de AWS. Requiere entidad y cuenta en un país habilitado [E] |
| **Azure Marketplace** | [NE] en esta ronda | Ídem |
| **Upwork** | Comisión variable al freelancer **0–15%** (≈ 10% típico) desde mayo de 2025 [S][32] | Buen canal para **servicios productizados** (por ejemplo "agente de voz para clínicas, USD X") y para validar la demanda en EE.UU. con poco capital |
| **Fiverr / Contra** | [NE] tarifas 2026 | — |
| **Product Hunt** | Gratis [E] | Pico de tráfico de un día; poco efecto en pymes no técnicas |
| **Cold outbound internacional** | 3,4% de respuesta por correo frío y 7,2% en LinkedIn (benchmarks globales ya citados en `INFORME.md`, sección 6) | Hace falta un dominio aparte, calentamiento y listas propias. En EE.UU. rige CAN-SPAM (opt-out); en la UE, GDPR y ePrivacy son más estrictos para el correo frío [E] |
| **Partners y revendedores** | — | Agencias de marketing y contadores hispanos de EE.UU. que revendan con margen del 20–30% [E] |

### 5.1 CAC y conversión de referencia (pyme global)
- **Recuperación del CAC:** la mediana de High Alpha 2025 es de 20 meses para empresas de USD 20–50 M de ARR. Para SMB, según fuentes secundarias, 8–12 meses (KeyBanc 2025) o 12–15 meses (atribuido a OpenView 2025) [S][33]. OpenView cerró en 2024 [E], así que tomar con cautela las cifras "OpenView 2025".
- **CAC de SMB:** USD 200–700 según un agregador; USD 1.100–1.400 para ACV de USD 1.000–10.000 según otro [S][33]. Son muy dispersos: usar el CAC USD 300–500 de `INFORME.md` como supuesto propio.
- **Prueba gratuita a pago:** según cifras atribuidas a ChartMogul 2026, 3,1% sin tarjeta y 34% con tarjeta; asistida por ventas 15,5% contra 4% sin asistencia (Redpoint) [S][33]. No se pudo abrir el informe original de ChartMogul [NE].

---

## 6. Precios y ventaja de costo

### 6.1 Referencias
- **Agencias y servicios productizados de IA en EE.UU. (2026, autodeclarado por operadores) [S][34]:**
  - abono de pyme desde ≈ USD 500/mes;
  - paquetes productizados ≈ USD 1.800–4.500/mes;
  - solo monitoreo ≈ USD 300–1.500/mes;
  - implementación única ≈ USD 1.500–15.000;
  - auditoría o diagnóstico ≈ USD 250–1.000.
- **SaaS pyme:** los precios de lista de EE.UU. relevados en `INFORME.md` (Pipedrive USD 14, AgencyAnalytics USD 20 por cliente, voz Vapi USD 82–129 por 1.000 min) marcan el piso del software genérico.

### 6.2 Ventaja de costo de un equipo argentino [E]
- `INFORME.md` usa una hora propia de USD 20 y una delegada de USD 12. Frente a abonos de USD 500–4.500/mes en EE.UU., el margen por cliente es varias veces mayor que con pymes argentinas (USD 150–250).
  - **Ejemplo:** un servicio de USD 1.000/mes con 8 h de trabajo delegado (USD 96) y USD 50 de API deja ≈ USD 800 de contribución antes del CAC.
  - Es un cálculo ilustrativo, no un pronóstico.
- **No se encontraron en esta ronda salarios comparables AR vs. EE.UU.** [NE].
- **Riesgo:** competir por precio contra agencias de India, Filipinas o LatAm en Upwork. **Diferenciar** por idioma (pymes hispanas), vertical y resultado medido.
- **Cómo cobrar [E]:** setup fijo + abono mensual en USD, con consumo de API transferido al cliente o tope incluido. Facturar el servicio con Factura E y cobrar por ACH (Payoneer). Si hay componente SaaS de autoservicio, venderlo por Paddle.

---

## 7. Qué no se pudo confirmar [NE]
- Precios 2026 de Doola y Firstbase; costo y mantenimiento de una OÜ estonia; costos anuales de una SL.
- Tarifas de partner de QuickBooks/Intuit, Xero, Zapier, Make, GoHighLevel, Azure, Fiverr y Contra.
- Cantidad de pymes en Chile, Colombia y Perú; cifra definitiva de México por tamaño; desglose MEI/ME/EPP en Brasil.
- Tributación de la importación de servicios en Brasil y México (retenciones al cliente); registro de IVA digital para B2C en México, Chile y Colombia.
- Comisión de Stripe Managed Payments; si Paddle admite hoy vendedores personas físicas argentinas (solo hay evidencia indirecta en la API).
- Estado del EU-US Data Privacy Framework en 2026; costo de un representante art. 27.
- Benchmarks primarios de ChartMogul, High Alpha o Benchmarkit (solo vía terceros); salarios de desarrolladores AR vs. EE.UU.

---

## 8. Checklist para vender afuera

**Fase 0: sin abrir empresa (meses 0–6)**
- [ ] Mantener el monotributo exportador y la caja de ahorro en USD (ver checklist de 05-legal-fiscal). Sumar la proyección de **Factura E** al tope de la categoría.
- [ ] Elegir **un** mercado inicial: pymes hispanas de EE.UU. (o agencias que las atienden) en **una** vertical.
- [ ] **Servicios:** cobrar setup + abono por ACH a Payoneer o Wise; contrato en inglés o español con tope de responsabilidad, IP, confidencialidad y DPA.
- [ ] **SaaS de autoservicio:** pedir el alta como vendedor en **Paddle** y confirmar por escrito que acepta vendedor argentino y que el producto es "software" (no servicio). No empezar con Lemon Squeezy (en migración) ni con Stripe Managed Payments (no admite AR).
- [ ] Paquete de confianza: **security overview** de 2 páginas, lista de subencargados, retención cero o no entrenamiento activado en los proveedores de IA, MFA y cifrado.
- [ ] Si toca la UE: DPA art. 28, evaluar **representante art. 27**, **aviso de IA (art. 50 AI Act)** en chat y voz, y marca de contenido si genera media. No entrar en casos de alto riesgo (empleo, crédito).
- [ ] Probar canales baratos: Upwork (servicio productizado), app en Shopify o HubSpot si el producto encaja (Shopify cobra 0% hasta USD 1 M), outbound acotado (≈ 900 correos para 15 entrevistas).

**Fase 1: abrir LLC cuando haya un disparador concreto**
- [ ] Disparadores: un cliente exige proveedor de EE.UU. o W-9, hace falta Stripe Billing o Connect, un marketplace o un seguro lo exige, o el volumen en USD justifica el costo fijo.
- [ ] Presupuestar: Atlas USD 500 + USD 100/año de agente + **USD 400/año de impuesto de Delaware a la LLC** + contador para **1120 pro forma + 5472** (multa de USD 25.000 si no se presenta).
- [ ] Contador argentino: tratamiento de la LLC transparente en Ganancias y Bienes Personales y cómo ingresan los fondos.
- [ ] BOI: no aplica a sociedades de EE.UU. (regla final de FinCEN, 14/08/2026). Revisar si cambia.

**Fase 2: escala (más de 12 meses)**
- [ ] Sales tax: si se vende fuera del MoR, monitorear el nexo por estado (≈ USD 100.000) con Stripe Tax o Anrok.
- [ ] UE B2C fuera del MoR: registro en OSS no-Unión desde la primera venta.
- [ ] SOC 2 solo cuando un cliente lo pida por contrato (≈ USD 25.000–60.000 el primer año).
- [ ] Seguro E&O tecnológico + cyber (≈ USD 1.000–4.000/año cada uno en EE.UU.) cuando haya LLC y contratos medianos.
- [ ] Seguir el AI Act (Anexo III, 02/12/2027), las leyes estatales de EE.UU. de 2027 (Oklahoma, Alabama) y el proyecto argentino 3397-D-2026.

---

## 9. Fuentes (consultadas el 30/10/2026)

1. Stripe, "Global availability". https://stripe.com/global [V]
2. Paddle, Pricing. https://www.paddle.com/pricing [V]
3. Lemon Squeezy, Pricing (con el aviso "2026 Update: Lemon Squeezy + Stripe Managed Payments"). https://www.lemonsqueezy.com/pricing [V]
4. Stripe Docs, "Managed Payments eligibility" (ubicaciones admitidas, productos excluidos). https://docs.stripe.com/payments/managed-payments/eligibility ; "Managed Payments". https://docs.stripe.com/payments/managed-payments [V]
5. Lemon Squeezy, "2026 update", JR Farr, 28/01/2026. https://www.lemonsqueezy.com/blog/2026-update [V]
6. Fungies, "Lemon Squeezy Stripe acquisition, SaaS founders 2026". https://fungies.io/lemon-squeezy-stripe-acquisition-saas-founders-2026/ ; Dodo Payments, alternativas. https://dodopayments.com/blogs/lemonsqueezy-alternatives [S, proveedores competidores]
7. Paddle Developer, "Supported countries" y "Payout accounts". https://developer.paddle.com/concepts/sell/supported-countries-locales ; https://developer.paddle.com/partners/embed-billing/seller-go-live/payout-accounts [S, ejemplo de API; no es una política de alta de vendedores]
8. Stripe Atlas. https://stripe.com/atlas [V]
9. Delaware Division of Corporations, "Alternative entity tax instructions" (USD 400/año, vence el 1 de junio). https://corp.delaware.gov/alt-entitytaxinstructions/ [V]
10. IRS, Instructions for Form 5472 (Rev. 12/2024). https://www.irs.gov/instructions/i5472 [V]
11. FinCEN, Beneficial Ownership Information (regla final del 11/08/2026, vigente desde el 14/08/2026). https://www.fincen.gov/boi [V]
12. Your Europe (Comisión Europea), "EU VAT One Stop Shop". https://europa.eu/youreurope/business/taxation/vat/one-stop-shop/indexamp_hr.htm ; Guía OSS de la Comisión. https://vat-one-stop-shop.ec.europa.eu/system/files/2021-07/OSS_guidelines_en.pdf [V para el alcance; el umbral cero para no establecidos, vía S]
13. Hellotax, "Non-Union OSS for non-EU digital service providers". https://helpdesk.hellotax.com/hc/en-150/articles/49817186344209-Non-Union-OSS-for-Non-EU-Digital-Service-Providers ; Avalara, "Union vs non-Union OSS". https://www.avalara.com/blog/en/europe/2021/08/union-vs-non-union-oss-what-is-the-difference.html [S]
14. Numeral, "SaaS sales tax state-by-state 2026". https://numeral.com/blog/sales-tax-on-saas ; Anrok, "Sales tax statistics" (25 jurisdicciones). https://www.anrok.com/resources/sales-tax-statistics ; Creem, 03/06/2026. https://www.creem.io/blog/saas-sales-tax-usa [S, proveedores de software de impuestos]
15. Gibson Dunn, "EU AI Act Omnibus Agreement — Postponed High-Risk Deadlines…", 27/05/2026. https://www.gibsondunn.com/eu-ai-act-omnibus-agreement-postponed-high-risk-deadlines-and-other-key-changes/ [S]
16. Usercentrics, "EU AI Act Deal: Digital Omnibus Now in Force" (Reg. UE 2026/1744, vigente desde el 27/07/2026). https://usercentrics.com/knowledge-hub/eu-ai-act-high-risk-delay-article-50-transparency-consent/ ; Technology.org, 13/10/2026. https://www.technology.org/2026/10/13/eu-ai-act-deadlines-after-the-digital-omnibus-what-applies-from-december-2026-to-august-2028/ [S; no se verificó contra el Diario Oficial de la UE]
17. GDPR, art. 27 (texto). https://gdpr-info.eu/art-27-gdpr/ [V, texto de la norma]
18. Drata, "SOC 2 cost". https://drata.com/learn/soc-2/cost ; Agency, "SOC 2 audit cost for startups 2026". https://blog.getagency.com/articles/soc-2-audit-cost-for-startups ; Costbench, Drata vs Vanta. https://www.costbench.com/compare/drata-vs-vanta/ [S, proveedores con interés]
19. SBA Office of Advocacy, "New Advocacy Report Shows the Number of Small Businesses in the U.S. Exceeds 36 million", 30/06/2025. https://advocacy.sba.gov/2025/06/30/new-advocacy-report-shows-the-number-of-small-businesses-in-the-u-s-exceeds-36-million/ ; perfil de EE.UU. 2025. https://advocacy.sba.gov/wp-content/uploads/2025/06/United_States_2025-State-Profile.pdf [V]
20. U.S. Census Bureau, "Census Bureau Releases New Data About Characteristics of Employer and Nonemployer Business Owners", 20/11/2025 (ABS, datos de 2024). https://www.census.gov/newsroom/press-releases/2025/business-owner-characteristics.html [V]
21. GOV.UK, "Business population estimates for the UK and regions 2025: statistical release". https://www.gov.uk/government/statistics/business-population-estimates-2025/business-population-estimates-for-the-uk-and-regions-2025-statistical-release [V]
22. INE, nota de prensa DIRCE 2025, 11/12/2025. https://ine.es/dyngs/Prensa/DIRCE2025.htm ; Ipyme, "Retrato de la PYME DIRCE 2024". https://ipyme.org/Publicaciones/Retrato%20de%20la%20PYME/Retrato_Pyme_DIRCE_2024.pdf ; Tesify (54,4% sin asalariados). https://tesify.es/pymes-tfg-administracion-empresas-datos-ine-2026 [V para el total; S para el porcentaje]
23. SBT News, "Número de pequenos negócios ativos cresce no Brasil, segundo o Sebrae". https://sbtnews.sbt.com.br/noticia/brasil/numero-de-pequenos-negocios-ativos-cresce-no-brasil-segundo-o-sebrae ; Agência Sebrae. https://agenciasebrae.com.br/?p=38255 [S]
24. INEGI, Censos Económicos 2024, resultados oportunos. https://inegi.org.mx/contenidos/saladeprensa/boletines/2025/ce/CE_2024_RO_Nal.pdf ; México Cómo Vamos. https://mexicocomovamos.mx/wp-content/uploads/2025/07/20250729_PublicacionMCV_Censos_economicos_2024.pdf ; Publimetro, 23/01/2025. https://www.publimetro.com.mx/nacional/2025/01/23/ventas-por-internet-aumentaron-casi-al-doble-en-micronegocios-pymes-y-empresas-grandes-inegi/ [S; la cifra exacta no se leyó en el PDF oficial]
25. MultiState, "All of the comprehensive privacy laws that take effect in 2026". https://multistate.us/insider/2026/2/4/all-of-the-comprehensive-privacy-laws-that-take-effect-in-2026 ; Bloomberg Law. https://news.bgov.com/us-law-week/indiana-kentucky-and-rhode-island-enforce-new-privacy-laws ; Enzuzo, 2026 tracker. https://www.enzuzo.com/blog/us-state-privacy-laws ; IAPP tracker (actualizado el 08/09/2026, sin conteo). https://iapp.org/resources/article/us-state-privacy-legislation-tracker/ [S]
26. e-Residency de Estonia, "Become an e-resident" (tasa de €150). https://www.e-resident.gov.ee/become-an-e-resident/ [V]
27. Billeo, "Crear Sociedad Limitada 2026". https://www.billeo.es/crear-sociedad-limitada-espana-2026 ; Costa Luz Lawyers (2025). https://www.costaluzlawyers.com/business/guide-to-the-costs-of-setting-up-and-running-a-company-in-spain/ ; Freenance (no residentes). https://freenance.io/entrepreneurship/how-to-start-business-spain-2026-sl-vs-autonomo-foreigner-step-by-step-residency-guide/ [S]
28. Vouch, "Startup insurance costs". https://www.vouch.us/blog/startup-insurance-costs ; Insureon, IT business insurance cost. https://insureon.com/technology-business-insurance/cost ; TechInsurance, cyber cost. https://www.techinsurance.com/technology-business-insurance/cybersecurity/cost [S, corredores]
29. Shopify.dev, "Revenue share". https://shopify.dev/docs/apps/launch/distribution/revenue-share [V]
30. HubSpot Developers, "App Marketplace listing requirements". https://developers.hubspot.com/docs/apps/developer-platform/list-apps/listing-your-app/app-marketplace-listing-requirements [V]
31. AWS Marketplace, "Understanding listing fees". https://docs.aws.amazon.com/marketplace/latest/userguide/listing-fees.html ; AWS What's New, 06/2026 (servicios profesionales 0,5%). https://aws.amazon.com/about-aws/whats-new/2026/06/reduce-listing-fee-professional-services-aws-marketplace/ [V]
32. Snipework, "How do Upwork's dynamic fees (0–15%) work?". https://snipework.com/answers/upwork-dynamic-fees-explained ; goLance, 2026. https://golance.com/blogs/upwork-fees-explained-2026 [S; el centro de ayuda de Upwork devolvió 403]
33. ScaleXP, "2025 SaaS Benchmarks: CAC Payback". https://www.scalexp.com/blog/saas-benchmarks-cac-payback/ ; SaaS Hero (Maxio CAC benchmarks, 18/07/2026). https://www.saashero.net/strategy/maxio-cac-benchmarks-b2b-saas/ ; Foundry CRO, 2026. https://foundrycro.com/blog/saas-marketing-benchmarks-2026/ ; Stealth Agents. https://stealthagents.com/research/startup-cac-payback-period-benchmarks-2026 [S, agregadores]
34. Vantaige, "The 2026 AI Automation Rate Card". https://vantaige.io/blog/2026-ai-automation-rate-card-operators-charge ; Layer3 Labs (02/07/2026). https://www.layer3labs.io/guides/ai-agency-pricing ; Taskip. https://taskip.net/ai-automation-agency-pricing/ [S, autodeclarado]
