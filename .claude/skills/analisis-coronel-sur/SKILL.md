---
name: analisis-coronel-sur
description: Skill para el proyecto de análisis de Distribuidora Coronel Sur. Prioriza lo correcto sobre lo rápido, verifica errores, busca múltiples puntos de vista y genera preguntas clave antes de actuar. Activar cuando se trabaje sobre datos, reportes, decisiones o cualquier análisis vinculado a Coronel Sur (ventas, stock, clientes, rutas, finanzas, operaciones, etc.).
---

# Análisis Coronel Sur — Protocolo de Excelencia

Objetivo: en todo análisis o acción relacionada al proyecto **Distribuidora Coronel Sur**, garantizar **lo correcto por sobre lo rápido**, verificando errores, contrastando perspectivas y buscando la excelencia.

## Principios rectores

1. **Correcto > rápido.** Nunca entregar un resultado sin validar. Si falta información, preguntar antes de asumir.
2. **Verificar siempre.** Todo dato, número, fórmula o conclusión se revisa al menos una vez antes de reportarse.
3. **Múltiples puntos de vista.** Analizar cada problema desde al menos 2–3 ángulos distintos (comercial, operativo, financiero, cliente, riesgo).
4. **Detectar y corregir.** Si aparece un error, inconsistencia o dato sospechoso → detener, investigar la causa raíz y corregir. No parchar.
5. **Excelencia.** El estándar es "lo mejor posible con la información disponible", no "lo mínimo que funciona".

## Flujo de trabajo obligatorio

### Paso 1 — Entender antes de actuar
Antes de producir cualquier análisis o cambio, responder:
- ¿Cuál es el objetivo real del pedido? ¿Qué decisión se va a tomar con esto?
- ¿Qué datos tengo, cuáles faltan, y cuáles son sospechosos?
- ¿Qué supuestos estoy haciendo? ¿Están validados?
- ¿Quién es el destinatario y qué nivel de detalle necesita?

Si alguna respuesta no es clara → **preguntar al usuario** usando las preguntas guía de abajo.

### Paso 2 — Generar preguntas clave
Antes de concluir, formular y responder preguntas como:
- ¿Qué pasa si los datos de entrada están mal? ¿Cómo lo detectaría?
- ¿Hay una interpretación alternativa de estos números?
- ¿Qué diría alguien del área comercial vs. alguien de finanzas vs. operaciones?
- ¿Qué me estaría perdiendo si solo miro el promedio / el total / el último mes?
- ¿Hay estacionalidad, outliers, duplicados, faltantes?
- ¿El resultado es consistente con lo que ya sabemos del negocio?

### Paso 3 — Verificación cruzada
- Recalcular totales por al menos 2 métodos cuando sea posible.
- Chequear sumas, rangos de fechas, unidades (pesos vs. unidades, kg vs. unidades, IVA incluido/no).
- Comparar contra un período o benchmark conocido.
- Señalar explícitamente cualquier dato que parezca inconsistente.

### Paso 4 — Múltiples perspectivas
Cuando se emita una conclusión o recomendación, incluir:
- **Visión principal** (lo que los datos indican).
- **Contraargumento** (qué podría estar mal, qué riesgo hay).
- **Perspectiva alternativa** (cómo lo vería otro rol del negocio).

### Paso 5 — Entrega
Formato de salida recomendado:
1. **Resumen** (1–3 frases, qué encontré y qué recomiendo).
2. **Hallazgos** con evidencia (números, archivos, rangos).
3. **Supuestos y limitaciones** explícitos.
4. **Riesgos / puntos débiles del análisis.**
5. **Próximos pasos o preguntas abiertas.**

## Preguntas guía (usar cuando falte contexto)

Comerciales / ventas:
- ¿Qué período cubre el análisis y con qué se compara?
- ¿Se consideran ventas netas o brutas? ¿Con/sin IVA? ¿Con/sin devoluciones?
- ¿Por cliente, canal, zona, vendedor, producto o familia?

Stock / logística:
- ¿Stock físico, contable o disponible para venta?
- ¿Incluye mercadería en tránsito / reservada?
- ¿Cuál es el criterio de "faltante" o "sobrestock"?

Clientes / rutas:
- ¿Qué define cliente activo/inactivo?
- ¿Cómo se agrupan las rutas? ¿Hay cambios recientes?

Finanzas:
- ¿Moneda, tipo de cambio, fecha de corte?
- ¿Margen bruto, neto, o contribución?
- ¿Costos incluyen flete, comisiones, impuestos?

Datos:
- ¿Cuál es la fuente de verdad?
- ¿Hay más de una fuente? ¿Cuál prima si hay conflicto?
- ¿Fecha de última actualización?

## Señales de alerta — detener y revisar

- Números redondos sospechosos (todo termina en 000).
- Saltos bruscos sin explicación.
- Totales que no cierran entre vistas.
- Duplicados de clientes, productos, facturas.
- Fechas fuera de rango.
- Unidades mezcladas.
- Cambios recientes en la estructura de datos.

Ante cualquiera de estas → **no continuar hasta entender la causa**.

## Qué NO hacer

- No entregar un número sin decir de dónde sale.
- No asumir que el último archivo/dato es el correcto sin verificarlo.
- No borrar ni sobrescribir datos originales.
- No tomar el atajo "me da parecido, debe estar bien".
- No ocultar incertidumbre — si hay dudas, decirlas.

## Registro

Al terminar cada análisis o acción, dejar constancia breve de:
- Qué se hizo.
- Qué se verificó.
- Qué quedó pendiente o sin resolver.

Esto alimenta el contexto de sesiones futuras.
