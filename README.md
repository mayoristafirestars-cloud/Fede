# Clima • Pronóstico y Alertas (PWA)

App web para celular que muestra el pronóstico **por hora** (temperatura, lluvia, viento, humedad) y resalta **alertas** (tormenta, lluvia intensa, viento fuerte, calor extremo, heladas, niebla, UV alto).

- Sin clave de API: usa **Open-Meteo** (gratis).
- Geolocalización + búsqueda de ciudad en español.
- Instalable como app (PWA) y funciona con conexión intermitente.

## Cómo usarla

1. Abrí `index.html` desde un servidor local (los PWA no andan desde `file://`).
2. Permití la geolocalización o buscá tu ciudad.
3. En Android/Chrome: menú ⋮ → "Agregar a pantalla de inicio".
   En iPhone/Safari: Compartir → "Agregar a pantalla de inicio".

## Servir localmente

Cualquier servidor estático sirve. Ejemplos:

```bash
# Python 3
python3 -m http.server 8080

# Node
npx serve .
```

Luego entrá desde el celular a `http://TU-IP:8080`.

## Publicar gratis

Subí los archivos a GitHub Pages, Netlify, Vercel o Cloudflare Pages. Es HTML/CSS/JS puro — sin build.

## Estructura

```
index.html            UI
styles.css            estilos mobile-first
app.js                lógica (fetch, render, alertas)
manifest.webmanifest  PWA
sw.js                 service worker (cache offline)
icons/icon.svg        ícono
```

## Alertas (cómo se generan)

Open-Meteo no publica un feed oficial global de alertas. La app **deriva** alertas del pronóstico de las próximas 24 h:

- ⛈️ Tormenta eléctrica (códigos WMO 95–99)
- 🌧️ Lluvia intensa (pico ≥ 10 mm/h) o acumulada (≥ 20 mm/24 h)
- 💨 Viento fuerte (ráfagas ≥ 60–75 km/h)
- 🥵 Calor extremo (≥ 32/35 °C) · 🥶 Heladas (≤ 0 °C)
- ❄️ Nevadas · 🌫️ Niebla · ☀️ UV ≥ 8

Para decisiones críticas, consultá siempre al **servicio meteorológico oficial** de tu país.
