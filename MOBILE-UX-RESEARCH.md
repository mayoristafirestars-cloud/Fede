# UX Mobile Audit — Tienda de Bebidas

> Auditoría sobre `catalogo-bebidas.html` (commit `6bd810b`). Mobile-first, B2B mayorista, checkout via WhatsApp.

## 0. Resumen ejecutivo

El sitio ya hace bien lo difícil: single-file, sticky cart bar, drawer con qty stepper, WhatsApp link bien armado, fallback de imagen, cache de CSV en `sessionStorage`. Lo que más rinde para B2C-de-kiosquero (que es lo que es esta página, aunque vendas mayorista) es bajar la fricción card → carrito y mostrar siempre cuánto va el pedido. Hoy se agrega de a 1 pack y para subir cantidad hay que abrir el drawer — eso es el quick-win #1.

Se identificaron **6 acciones "do now"** (≤5h c/u, alto impacto), **5 "soon"** (1-3 días) y **3 "later"** (cambios estructurales).

---

## 1. Patrones probados — Mobile e-commerce argentino (B2C)

### 1.1 Mercado Libre app
- **Add-to-cart everywhere**: ML invirtió específicamente en que el botón "Agregar" esté disponible en la card, en search results, en home y en PDP, con UX consistente. Conclusión interna: bajaron fricción y subieron velocidad de compra.
- **Card pattern**: imagen cuadrada, título 2 líneas, precio destacado, badge de OFF. La card es 100% tappeable → abre PDP. Botón "+" pequeño superpuesto abajo a la derecha (FAB-style sobre la card) en algunas verticals.
- **Buscador**: full-screen modal al tappear, con historial + sugerencias.
- **Categorías**: chips horizontales scrollables con scroll-snap.

### 1.2 PedidosYa / Rappi (delivery)
- **Stepper inline en card** una vez que agregás: en lugar de "Agregar", la card muestra `[ − ] [ 2 ] [ + ]` en el mismo lugar, sin abrir drawer. Esto es el patrón crítico para pedidos de muchos productos × pocas unidades (que es exactamente tu caso).
- **Sticky bottom bar** "Ver carrito · 5 ítems · $4.300" (verde Rappi / rojo PedidosYa). Igual al tuyo, ya estás bien acá.
- **Categorías**: chips arriba pegajosos cuando hacés scroll dentro del comercio.

### 1.3 Tiendanube / Shopify themes
- Sticky add-to-cart en mobile: tests reportan **+8 a +25% conversión**.
- Cards en grilla de 2 columnas en mobile ≤ 480px (tu valor actual también, bien).

### 1.4 Carrefour / Vea / DIA app
- **Stepper inline** sobre la card. Fundamental: el peso del carrito de supermercado son 30-50 productos chicos.
- **Lazy load + skeleton** mientras carga; nunca hay pantalla en blanco.
- **Filtros** como bottom-sheet, no como drawer lateral (más natural en mobile, requiere menos viewport).

### 1.5 Performance baseline
- Ningún player serio carga >20 productos sin lazy/infinite scroll. Tu HTML hoy renderiza **todos** los productos del CSV en un solo paint — funciona con 50, se vuelve lento con 300.

---

## 2. Wholesale-specific patterns (B2B bebidas/almacén)

### 2.1 Maxiconsumo, distribuidoras (Ferraro, BigPlaneta, Distribuidora Pop)
- Login obligatorio (vos no lo necesitás → ventaja).
- **Cantidad por pack visible**: "x 12 unidades" debajo del precio. El kiosquero quiere saber qué le entra al pack antes de agregar.
- **Quick-order pad**: tabla con SKU + cantidad para clientes recurrentes.
- **Reorder de último pedido** (para ti: imposible sin login, pero podés simularlo con localStorage).

### 2.2 AKGO / TiendasB2B / MayoriStore (plataformas argentinas B2B)
- Catálogo + carrito + WhatsApp es el patrón dominante en Argentina chica. Tu modelo está validado.
- Diferencias clave vs B2C:
  - El cliente repite. **Persistir carrito** entre sesiones es crítico.
  - Pedido típico: 8-15 SKUs distintos × 1-3 packs c/u → minimizar taps/SKU es lo que más mueve la aguja.
  - Mostrar siempre **mínimo de pack y unidades por pack** (ej. "Pack x 6 botellas 1L").

---

## 3. WhatsApp-as-checkout — buenas prácticas

Mensaje actual generado:

```
¡Hola! 👋 Quiero hacer el siguiente pedido:

• Quilmes 1L — 3 packs — $5.550
…

*Total estimado: $12.500*
_Los precios son por pack mínimo de venta._

¿Tienen disponibilidad?
```

**Lo que está bien**: usás `\n` codificado (`%0A` via `encodeURIComponent`), bullets, bold con `*…*`, italic con `_…_`. Saludo + pregunta abierta al final.

**Lo que falta** (ver Sección 4):
- No incluís **dirección/zona del cliente** ni nombre. El distribuidor va a tener que pedirlo.
- No hay **referencia de pedido** (ID corto generado client-side) para que el dueño pueda matchear el chat con el carrito si llegan 5 chats juntos.
- Falta **link de vuelta al catálogo** — si el cliente pierde el chat o reabre días después, no tiene cómo volver.
- Si el mensaje crece a 30 ítems, supera 1024 chars (límite seguro de wa.me en algunos clientes Android viejos). Riesgo bajo en tu caso, pero hay que tenerlo en cuenta.

---

## 4. Quick-wins — DO NOW (≤5h c/u, alto impacto)

### 4.1 Stepper inline en la card  ★★★
**Problema**: hoy el botón pasa a `✓ 3 packs · EDITAR` que abre drawer. Para sumar el cuarto pack: tap card → tap botón → drawer abierto → tap `+` → tap cerrar drawer → seguir comprando. Son **5 taps** para algo que en Rappi es 1.
**Solución**: cuando `cant > 0`, reemplazar el botón por `[ − ] [ 3 ] [ + ]` inline en la card, mismo alto que el botón actual (48px). El drawer queda solo para revisar/finalizar.
- Impacto: **alto** — es el paso que más se repite en la sesión.
- Esfuerzo: **3-5h**.
- Prioridad: **do now**.

### 4.2 Lazy-load + tamaño explícito en `<img>` para evitar CLS  ★★★
**Problema**: usás `loading="lazy"` (bien) pero las `<img>` no tienen `width`/`height` ni `aspect-ratio` declarado en CSS — `min-height: 220px` está en el contenedor, pero la imagen sigue causando layout shift cuando carga.
**Solución**: agregar `aspect-ratio: 1/1` a `.b-card-img img` y `width="200" height="200"` en el tag.
- Impacto: **medio-alto** (LCP / CLS, sensación de calidad).
- Esfuerzo: **30 min**.
- Prioridad: **do now**.

### 4.3 Persistir carrito en `localStorage`  ★★★
**Problema**: el kiosquero arranca el carrito a las 10:30, lo deja, vuelve a las 14:00 desde el mismo cel — perdió todo. En B2B esto es un orden de magnitud más doloroso que en B2C.
**Solución**: `localStorage.setItem('carrito', JSON.stringify(carrito))` después de cada `agregar/quitar/setQty`, y `JSON.parse(localStorage.getItem('carrito') || '{}')` al `init()`. TTL 7 días.
- Impacto: **alto** para retención y completar pedidos.
- Esfuerzo: **2h**.
- Prioridad: **do now**.

### 4.4 Skeleton mientras carga el CSV  ★★
**Problema**: con un CSV de 200+ filas + 3 proxies CORS en cascada, hay 1-3s de pantalla con `b-loading` (texto). Mobiles con red lenta sienten "el sitio está roto".
**Solución**: 6 cards de skeleton (gris animado) en cada sección durante el fetch.
- Impacto: **medio** (perceived performance).
- Esfuerzo: **2h**.
- Prioridad: **do now**.

### 4.5 Mostrar el carrito SIEMPRE accesible — botón cart visible en mobile  ★★★
**Problema**: en `@media (max-width: 800px)` escondés `.b-cart` (`display: none`). Sólo queda la sticky bar abajo, que aparece sólo cuando hay items. Si el cliente cierra el sticky por accidente o no entiende que se llega ahí, no tiene cómo abrir el drawer desde la card.
**Solución**: dejar el ícono carrito visible en el header sticky en mobile.
- Impacto: **alto** (es un atasco de navegación real).
- Esfuerzo: **15 min**.
- Prioridad: **do now**.

### 4.6 Touch targets en el drawer + hit area en steppers  ★★
**Problema**: confirmar que steppers tengan **mínimo 44×44px** (Apple HIG, WCAG 2.5.5 AA).
- Impacto: **medio** (accesibilidad + usuarios con dedos grandes / camión).
- Esfuerzo: **30 min**.
- Prioridad: **do now**.

---

## 5. SOON (1-3 días, impacto medio-alto)

### 5.1 Buscador full-screen en mobile  ★★
Hoy `.b-search` se oculta a ≤800px y solo queda el burger. El kiosquero que viene a buscar "Quilmes 1L" no tiene buscador. Patrón ML: ícono lupa en header → modal full-screen con input grande + lista de resultados live.
- Esfuerzo: **1 día**. Prioridad: **soon**.

### 5.2 Chips de categoría sticky debajo del header en mobile  ★★
El megamenú existe pero no es sticky en mobile. Cuando scrolleás 2 secciones perdés contexto. Hacer sticky el `.b-nav` con scroll-snap chips activos.
- Esfuerzo: **4-6h**. Prioridad: **soon**.

### 5.3 Mensaje de WhatsApp con metadatos del cliente  ★★★
Antes de abrir wa.me, modal corto pidiendo **Nombre comercio + Localidad** (opcional, recordado en localStorage). Generar un **ID de pedido** (`#TB-A4F2`) y prependear al mensaje.

```
Pedido #TB-A4F2
Comercio: Kiosco La Esquina — General Pico
———
• Quilmes 1L — 3 packs — $5.550
…
*Total: $12.500*
```

Esto le ahorra 3 minutos al distribuidor por pedido y le permite organizarse cuando llegan varios juntos.
- Impacto: **alto** (fricción operativa del lado vendedor).
- Esfuerzo: **1 día**. Prioridad: **soon**.

### 5.4 Botón "Repetir último pedido"  ★★
En el drawer vacío, mostrar "Tu último pedido (15/04): 8 productos — repetir". Re-poblar carrito desde localStorage histórico.
- Esfuerzo: **1 día**. Prioridad: **soon**.

### 5.5 Filtros tipo bottom-sheet  ★
Por marca, por rubro, por rango de precio. Bottom-sheet es el patrón mobile correcto. Sólo justifica si llegás a 100+ SKUs.
- Esfuerzo: **2 días**. Prioridad: **soon** (cuando crezca el CSV).

---

## 6. Mediano plazo — LATER (estructural)

### 6.1 Enriquecer el Sheet
Sumar columnas:
- `unidades_pack` (ej. 6, 12, 24) → mostrar "Pack x 12 · $1.850 ($154/u)". **Subí mucho la confianza del kiosquero**.
- `marca` → filtrable.
- `stock` (S/N o número) → mostrar agotado en gris, no agregable.
- `foto_2`, `foto_3` → carrusel en lightbox.
- `tags` (FRIO, RETORNABLE, SIN_TACC) → badges chicos.
- Esfuerzo: **2-3 días**. Prioridad: **later**, pero el más alto ROI del bloque.

### 6.2 PWA instalable
`manifest.json` + service worker mínimo (cache del CSV + assets). Promo banner "Instalá Tienda de Bebidas" a la 2da visita. El kiosquero va a abrir esto literal cada semana.
- Esfuerzo: **2-3 días**. Prioridad: **later** pero alto fit con el caso de uso.

### 6.3 Variantes de producto (mismo nombre, distintos tamaños)
Hoy "Quilmes 1L" y "Quilmes 473ml" son 2 cards distintas. UX correcta es 1 card con toggle de tamaño (chips). Requiere refactor del modelo de datos del CSV: columna `producto_grupo`.
- Esfuerzo: **1 semana**. Prioridad: **later**.

### 6.4 Modo cliente recurrente (sin login)
Cookie + localStorage que recuerda nombre/localidad/lista de favoritos. No es login, es "este celular ya conozco".
- Esfuerzo: **3-5 días**. Prioridad: **later**.

---

## 7. Patrones a EVITAR para este caso

| Anti-patrón | Por qué no |
|---|---|
| **Login obligatorio** | Mata la conversión cold; tu valor es justo que sea instantáneo |
| **Pop-up de email/newsletter al entrar** | Estás en mobile + B2B; rompe el flujo |
| **Carrusel hero auto-rotativo agresivo** | A 5s no llegás a leer. Subir a **7-8s** o detener al primer swipe |
| **Modal de confirmación "¿seguro querés agregar?"** | Es B2B, el cliente sabe lo que hace |
| **Infinite scroll sin footer accesible** | El footer tiene info crítica; usar paginación o load-more |
| **Iconos sin label en mobile** | Pop tu "buscar" con lupa sin texto va a ser visto como decorativo |
| **Sticky cart bar tapando contenido** | Verificar padding-bottom igual al alto del bar |
| **Imágenes >150KB cada una** | Asumir red 3G; pasar por CDN tipo `images.weserv.nl` con `w=400` |
| **Color `--muted: #8a8a8a` sobre `--paper: #f6f4ef`** | Contraste **3.4:1** — falla WCAG AA. Usar `#6e6e6e` (4.6:1) |

---

## 8. Issues técnicos detectados en el código

1. **`.b-cart { display: none; }` en mobile** esconde el carrito del header.
2. **`.b-search input font-size: 14px`** — Safari iOS hace zoom auto cuando el input es <16px. Subir a **16px**.
3. **3 proxies CORS encadenados** con `Promise.any` — frágil. Considerar Netlify Function como proxy propio (gratis hasta 125k req/mes).
4. **`loading="lazy"`** está, pero falta `decoding="async"` y `fetchpriority` en LCP.
5. **`window.open` en iOS Safari** a veces es bloqueado como popup si no nace de un click directo síncrono.
6. **No hay `<meta name="theme-color">`** — la barra de Chrome Android queda gris. Sumar `<meta name="theme-color" content="#1a1a1a">`.
7. **No hay `<link rel="manifest">`** — pre-requisito para PWA.
8. **Hero a `380px` en mobile** ocupa **>50% del viewport del iPhone SE**. Bajar a **280px** y achicar `h1` a `clamp(28px, 6vw, 48px)`.

---

## 9. Priorización final (matriz impacto/esfuerzo)

| # | Acción | Impacto | Esfuerzo | Prioridad |
|---|---|---|---|---|
| 4.5 | Mostrar ícono carrito en header mobile | Alto | 15 min | **DO NOW** |
| 4.2 | `aspect-ratio` en imgs (CLS) | Alto | 30 min | **DO NOW** |
| 4.1 | Stepper inline en la card | Alto | 3-5h | **DO NOW** |
| 4.3 | Persistir carrito en localStorage | Alto | 2h | **DO NOW** |
| 4.4 | Skeleton loading | Medio | 2h | **DO NOW** |
| 4.6 | Touch targets 44px + contraste muted | Medio | 1h | **DO NOW** |
| 8.2 | Search input 16px (anti-zoom iOS) | Medio | 5 min | **DO NOW** |
| 8.7 | `meta theme-color` | Bajo | 2 min | **DO NOW** |
| 8.9 | Hero más bajo en mobile | Medio | 30 min | **DO NOW** |
| 5.3 | Pedido con Nombre + ID + Localidad | Alto | 1 día | **SOON** |
| 5.1 | Buscador full-screen mobile | Medio-Alto | 1 día | **SOON** |
| 5.4 | Repetir último pedido | Medio | 1 día | **SOON** |
| 5.2 | Chips categoría sticky | Medio | 4-6h | **SOON** |
| 5.5 | Filtros bottom-sheet | Bajo (hoy) | 2 días | **SOON** (al crecer SKUs) |
| 6.1 | Sheet enriquecido (unidades/pack, stock, marca) | Alto | 2-3 días | **LATER** |
| 6.2 | PWA + service worker | Medio-Alto | 2-3 días | **LATER** |
| 6.3 | Variantes de producto | Medio | 1 semana | **LATER** |
| 6.4 | Modo cliente recurrente | Medio | 3-5 días | **LATER** |

---

## 10. Recomendación de orden de ejecución

**Sprint 1 (1 día calendario)**: 8.7, 8.2, 4.5, 4.2, 4.6, 8.9 → wins instantáneos.
**Sprint 2 (3 días)**: 4.1 stepper inline + 4.3 persistencia + 4.4 skeleton. Ahí ya tenés el "sitio que parece app".
**Sprint 3 (1 semana)**: 5.3 metadatos del cliente + 5.1 search modal + 5.4 repetir pedido. Ahí dejás de ser "catálogo" y sos "canal de pedido recurrente".
**Sprint 4 (cuando se justifique por volumen)**: 6.1 sheet enriquecido + 6.2 PWA.

---

### Sources
- [Add to cart everywhere — Mercado Libre Tech](https://medium.com/mercadolibre-tech/add-to-cart-everywhere-taking-the-add-to-cart-button-to-every-corner-of-mercado-libre-139d439982be)
- [Sticky Add to Cart best practices — EasyApps](https://easyappsecom.com/guides/sticky-add-to-cart-best-practices)
- [Sticky Add-to-Cart A/B test results — GrowthRock](https://growthrock.co/sticky-add-to-cart-button-example/)
- [B2B product page UX — SparkLayer](https://www.sparklayer.io/blog/2024/11/06/b2b-product-pages-ui/)
- [WhatsApp character limits — PickyAssist](https://help.pickyassist.com/general-guidelines/character-limits-whatsapp)
- [wa.me URL format — WhatsApp FAQ](https://faq.whatsapp.com/5913398998672934)
- [Mobile Commerce Optimization Guide — DigitalApplied](https://www.digitalapplied.com/blog/mobile-commerce-optimization-ux-conversion-guide)
- [WCAG 2.2 Target Size — W3C](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html)
- [TiendasB2B](https://tiendasb2b.com/)
- [AKGO Argentina](https://akgo-argentina.com/)
