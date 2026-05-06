/* Service Worker — Tienda de Bebidas
 * Estrategias:
 *  - CSV de Google Sheets:  network-first   (precios siempre frescos, fallback a cache si no hay red)
 *  - HTML / navegación:     stale-while-revalidate (carga instantánea de cache, refresca en background)
 *  - Imágenes / fonts / CSS: cache-first    (no cambian seguido, ahorra mucha red)
 *  - Todo lo demás:         pasa al fetch real
 */

const VERSION = "v3";
const CACHE_RUNTIME = `tienda-bebidas-runtime-${VERSION}`;
const CACHE_HTML    = `tienda-bebidas-html-${VERSION}`;
const CACHE_ASSETS  = `tienda-bebidas-assets-${VERSION}`;

const PRECACHE = ["./", "./index.html", "./catalogo-bebidas.html", "./manifest.json"];

// Install: precachear el HTML al instalar
self.addEventListener("install", event => {
  event.waitUntil(
    caches.open(CACHE_HTML)
      .then(cache => cache.addAll(PRECACHE).catch(() => {/* tolerar URLs ausentes */}))
      .then(() => self.skipWaiting())
  );
});

// Activate: limpiar caches viejos
self.addEventListener("activate", event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => !k.endsWith(VERSION)).map(k => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

// Helper: ¿es un asset estático (img/font/css/js)?
function isAsset(url) {
  if (/\.(png|jpe?g|webp|svg|gif|ico|woff2?|css|js)(\?|$)/.test(url.pathname)) return true;
  if (url.hostname === "fonts.gstatic.com") return true;
  if (url.hostname === "fonts.googleapis.com") return true;
  if (url.hostname === "images.weserv.nl") return true;
  if (url.hostname === "i.ibb.co") return true;
  if (url.hostname === "ibb.co") return true;
  return false;
}

// Helper: ¿es el CSV del Sheet (vía proxies)?
function isSheetCSV(url) {
  if (url.hostname === "docs.google.com") return true;
  if (url.hostname === "api.allorigins.win") return true;
  if (url.hostname === "corsproxy.io") return true;
  if (url.hostname === "api.codetabs.com") return true;
  return false;
}

// Estrategias
async function cacheFirst(request, cacheName) {
  const cache = await caches.open(cacheName);
  const cached = await cache.match(request);
  if (cached) return cached;
  try {
    const response = await fetch(request);
    if (response && response.status === 200 && response.type !== "opaqueredirect") {
      cache.put(request, response.clone()).catch(() => {});
    }
    return response;
  } catch (e) {
    return cached || new Response("", { status: 503 });
  }
}

async function networkFirst(request, cacheName, timeoutMs = 6000) {
  const cache = await caches.open(cacheName);
  try {
    const ctrl = new AbortController();
    const timer = setTimeout(() => ctrl.abort(), timeoutMs);
    const response = await fetch(request, { signal: ctrl.signal });
    clearTimeout(timer);
    if (response && response.status === 200) {
      cache.put(request, response.clone()).catch(() => {});
    }
    return response;
  } catch (e) {
    const cached = await cache.match(request);
    return cached || new Response("", { status: 503 });
  }
}

async function staleWhileRevalidate(request, cacheName) {
  const cache = await caches.open(cacheName);
  const cached = await cache.match(request);
  const networkPromise = fetch(request).then(response => {
    if (response && response.status === 200) {
      cache.put(request, response.clone()).catch(() => {});
    }
    return response;
  }).catch(() => cached);
  return cached || networkPromise;
}

// Router de fetch
self.addEventListener("fetch", event => {
  const { request } = event;
  if (request.method !== "GET") return;
  let url;
  try { url = new URL(request.url); } catch { return; }
  // Evitar interceptar Chrome extensions / about:
  if (!url.protocol.startsWith("http")) return;

  // CSV del sheet → siempre intentar fresco, con fallback a cache si offline
  if (isSheetCSV(url)) {
    event.respondWith(networkFirst(request, CACHE_RUNTIME, 8000));
    return;
  }

  // Assets estáticos → cache-first
  if (isAsset(url)) {
    event.respondWith(cacheFirst(request, CACHE_ASSETS));
    return;
  }

  // HTML / navegación → stale-while-revalidate
  if (request.mode === "navigate" || (url.origin === self.location.origin && url.pathname.endsWith("/")) ||
      (url.origin === self.location.origin && /\.html?$/.test(url.pathname)) ||
      url.pathname === "/" || url.pathname === "") {
    event.respondWith(staleWhileRevalidate(request, CACHE_HTML));
    return;
  }
});

// Permitir que la página fuerce un update del SW
self.addEventListener("message", event => {
  if (event.data === "skipWaiting") self.skipWaiting();
});
