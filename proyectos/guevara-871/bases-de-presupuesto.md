# Bases de presupuesto — A. Guevara 871

Convenciones fijas para cargar precios y armar el cómputo. **Toda planilla de este proyecto se
lee bajo estas reglas.**

---

## 1. Convenciones de carga

| Regla | Definición |
|---|---|
| **Precios NETOS** | Todas las listas de proveedores se cargan **sin IVA**. Es la convención del comitente |
| **Moneda** | Pesos argentinos, salvo que la lista indique lo contrario |
| **Fecha obligatoria** | Cada lista lleva la fecha de emisión. Un precio sin fecha no se carga |
| **Bonificación** | Se aclara si el precio es de lista o ya bonificado, y el % en su caso |
| **Unidad** | La del proveedor, con su conversión a la unidad de cómputo del rubro |

**Presentación de resultados:** todo total se muestra en **dos columnas — neto y final** — nunca
en una sola. El neto sirve para comparar proveedores; el final es lo que paga el comitente.

---

## 2. El punto a resolver antes de cerrar cualquier total

En Argentina, el IVA de una obra **no es una sola alícuota**:

| Concepto | Alícuota | Estado |
|---|---|---|
| **Materiales** | 21 % | Alícuota general |
| **Trabajos sobre inmueble ajeno destinados a vivienda** | **10,5 %** | Alícuota reducida — Ley de IVA, art. 28 · **⚠ verificar con contador** |

**Por qué importa acá:** si el presupuesto mezcla materiales y mano de obra en un solo total y
se le aplica 21 % a todo, el número final queda inflado. La diferencia en una obra de este
tamaño no es menor.

**Lo que hay que definir antes de emitir un presupuesto final:**

- [ ] Condición del comitente frente al IVA (responsable inscripto, monotributo, consumidor final)
- [ ] Si la obra se contrata **por administración** (materiales y gremios por separado) o **por
      ajuste alzado** (un contratista factura todo)
- [ ] Si corresponde la alícuota reducida del 10,5 % a los trabajos, y sobre qué ítems
- [ ] **Confirmar todo lo anterior con contador** — acá se registra el criterio, no se define

---

## 3. Vigencia

Los precios se desactualizan en semanas. Todo cuadro lleva **fecha del dato** y se actualiza por
los índices de referencia (CAC / INDEC ICC). **Sirve para decidir y para comparar proveedores;
para firmar contrato hay que repedir precio.**

---

## 4. Rubros de esta obra

Orden de ejecución, que es también el orden de compra:

| # | Rubro | Nota |
|---|---|---|
| 1 | Demolición y retiro de escombros | 47,68 m² de construcción precaria |
| 2 | **Aislaciones e impermeabilizaciones** | **Primero en obra** — hay humedad activa |
| 3 | Estructura: losa del hueco, encadenados, dinteles | |
| 4 | Mampostería | |
| 5 | Techos y cubierta | |
| 6 | Contrapisos y carpetas | |
| 7 | Revoques | |
| 8 | **SATE / aislación exterior** | EPS 100 mm muros · 120-140 mm losa |
| 9 | Solados y revestimientos | R10 interior · R11 semicubierto y exterior |
| 10 | Carpinterías | V1 4,00 DVH 3+3 lam. · P1 · P2 portón seccional · puerta al patio |
| 11 | Instalación sanitaria | |
| 12 | Instalación de gas | Matriculado 2ª categoría si supera 5 m³/h |
| 13 | Instalación eléctrica | |
| 14 | Pintura | |
| 15 | Mobiliario de cocina y lavadero | Incluye pileta de bañado |
| 16 | Ayuda de gremios y limpieza de obra | |

**Metodología de cómputo y análisis de precios:** `docs/02-proyecto/proyecto-ejecutivo.md` §5.

---

## 5. Listas cargadas

| Proveedor | Fecha de lista | Rubros que cubre | Neta / con IVA | Bonificación |
|---|---|---|---|---|
| *(pendiente)* | | | | |
