# Cómo deployar — Tienda de Bebidas (PWA)

A partir de ahora son **3 archivos** que tienen que vivir juntos en la misma carpeta:

```
/
├── index.html          (renombrado desde catalogo-bebidas.html)
├── manifest.json
└── service-worker.js
```

## Opción A — Netlify drag & drop (más simple)

1. Bajá los 3 archivos del repo:
   - https://raw.githubusercontent.com/mayoristafirestars-cloud/Fede/claude/beverage-catalog-whatsapp-1P40L/catalogo-bebidas.html
   - https://raw.githubusercontent.com/mayoristafirestars-cloud/Fede/claude/beverage-catalog-whatsapp-1P40L/manifest.json
   - https://raw.githubusercontent.com/mayoristafirestars-cloud/Fede/claude/beverage-catalog-whatsapp-1P40L/service-worker.js
2. Creá una carpeta nueva, por ejemplo `tienda-bebidas/`.
3. Pegá los 3 archivos adentro. **Renombrá `catalogo-bebidas.html` a `index.html`**.
4. En Netlify → tu site → **Deploys** → arrastrá la **carpeta entera** (no los archivos sueltos).
5. En 30 segundos está online.

## Opción B — Conectar el repo (auto-deploy en cada push)

1. Netlify → **Site settings** → **Build & deploy** → **Link repository**.
2. Elegí `mayoristafirestars-cloud/Fede`, branch `claude/beverage-catalog-whatsapp-1P40L`.
3. Build command: dejar **vacío**. Publish directory: `.`.
4. Cada vez que hago push, se redeploya solo.

## Cómo se prueba la PWA

1. Abrí la URL desde el celular.
2. **Android (Chrome):** banner abajo "Instalar app" o menú ⋮ → "Agregar a pantalla de inicio".
3. **iOS (Safari):** botón compartir → "Agregar a pantalla de inicio".
4. Abrí la app desde el ícono que quedó en el escritorio.
5. Probá ponerlo en modo avión y reabrir — el catálogo cargado en la última visita sigue funcionando.

## Forzar update cuando hay versión nueva

El service worker actualiza solo. Si querés forzar:
- Cerrar la app, esperá 5 segundos, reabrila.
- O: configuración del navegador → Borrar datos del sitio.

## Troubleshooting

- **No aparece el botón "Instalar"**: puede tardar 1-2 minutos en propagar tras el primer deploy. Recargá con `Ctrl+Shift+R`.
- **Imágenes lentas la primera vez**: es normal. La 2da visita usa la cache del SW.
- **Precios viejos**: el CSV se busca con network-first; si hay red, siempre trae lo último. Si no hay red, sirve la última versión cacheada.
