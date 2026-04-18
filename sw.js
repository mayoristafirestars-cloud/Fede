// Service Worker — caché de la app (no de los datos del clima)
const CACHE = "clima-v1";
const ASSETS = [
  "./",
  "./index.html",
  "./styles.css",
  "./app.js",
  "./manifest.webmanifest",
  "./icons/icon.svg",
];

self.addEventListener("install", (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(ASSETS)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", (e) => {
  e.waitUntil(
    caches.keys().then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (e) => {
  const url = new URL(e.request.url);
  // Nunca cachear los datos del pronóstico (deben ser frescos)
  if (url.hostname.includes("open-meteo.com")) {
    e.respondWith(fetch(e.request).catch(() => new Response(JSON.stringify({ error: "offline" }), { headers: { "Content-Type": "application/json" } })));
    return;
  }
  // Cache-first para assets de la app
  if (e.request.method === "GET" && url.origin === location.origin) {
    e.respondWith(
      caches.match(e.request).then((cached) =>
        cached || fetch(e.request).then((resp) => {
          const copy = resp.clone();
          caches.open(CACHE).then((c) => c.put(e.request, copy));
          return resp;
        }).catch(() => cached)
      )
    );
  }
});
