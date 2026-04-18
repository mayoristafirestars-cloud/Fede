// Weather PWA — Open-Meteo (no API key required)
// Docs: https://open-meteo.com/en/docs

const API_FORECAST = "https://api.open-meteo.com/v1/forecast";
const API_GEOCODE  = "https://geocoding-api.open-meteo.com/v1/search";
const API_REVERSE  = "https://geocoding-api.open-meteo.com/v1/reverse";

const $ = (id) => document.getElementById(id);
const state = {
  place: null, // { name, country, lat, lon, tz }
};

// --- WMO weather code → icon + description (Spanish) ---
const WMO = {
  0:  { i: "☀️", t: "Despejado",                theme: "clear" },
  1:  { i: "🌤️", t: "Mayormente despejado",     theme: "clear" },
  2:  { i: "⛅",  t: "Parcialmente nublado",     theme: "cloud" },
  3:  { i: "☁️", t: "Nublado",                   theme: "cloud" },
  45: { i: "🌫️", t: "Niebla",                    theme: "cloud" },
  48: { i: "🌫️", t: "Niebla con escarcha",       theme: "cloud" },
  51: { i: "🌦️", t: "Llovizna ligera",          theme: "rain"  },
  53: { i: "🌦️", t: "Llovizna",                 theme: "rain"  },
  55: { i: "🌧️", t: "Llovizna intensa",         theme: "rain"  },
  56: { i: "🌧️", t: "Llovizna helada",          theme: "rain"  },
  57: { i: "🌧️", t: "Llovizna helada intensa",  theme: "rain"  },
  61: { i: "🌦️", t: "Lluvia ligera",            theme: "rain"  },
  63: { i: "🌧️", t: "Lluvia",                    theme: "rain"  },
  65: { i: "🌧️", t: "Lluvia intensa",           theme: "rain"  },
  66: { i: "🌧️", t: "Lluvia helada",            theme: "rain"  },
  67: { i: "🌧️", t: "Lluvia helada intensa",    theme: "rain"  },
  71: { i: "🌨️", t: "Nevada ligera",            theme: "snow"  },
  73: { i: "🌨️", t: "Nevada",                    theme: "snow"  },
  75: { i: "❄️", t: "Nevada intensa",           theme: "snow"  },
  77: { i: "❄️", t: "Granos de nieve",          theme: "snow"  },
  80: { i: "🌦️", t: "Chubascos ligeros",        theme: "rain"  },
  81: { i: "🌧️", t: "Chubascos",                 theme: "rain"  },
  82: { i: "⛈️", t: "Chubascos violentos",       theme: "storm" },
  85: { i: "🌨️", t: "Chubascos de nieve",       theme: "snow"  },
  86: { i: "❄️", t: "Chubascos fuertes de nieve", theme: "snow" },
  95: { i: "⛈️", t: "Tormenta eléctrica",        theme: "storm" },
  96: { i: "⛈️", t: "Tormenta con granizo",     theme: "storm" },
  99: { i: "⛈️", t: "Tormenta fuerte con granizo", theme: "storm" },
};
const wmo = (c) => WMO[c] || { i: "❓", t: "—", theme: "cloud" };

const fmtT = (v) => (v == null ? "--" : `${Math.round(v)}°`);
const fmtKmh = (v) => (v == null ? "--" : `${Math.round(v)} km/h`);
const fmtMm = (v) => (v == null ? "--" : `${v.toFixed(1)} mm`);
const fmtPct = (v) => (v == null ? "--" : `${Math.round(v)}%`);

function toast(msg, ms = 2500) {
  const el = $("toast");
  el.textContent = msg;
  el.hidden = false;
  clearTimeout(toast._t);
  toast._t = setTimeout(() => (el.hidden = true), ms);
}

function hourLabel(iso, tz) {
  const d = new Date(iso);
  return new Intl.DateTimeFormat("es-AR", { hour: "2-digit", minute: "2-digit", hour12: false, timeZone: tz }).format(d);
}
function dayLabel(iso, tz, idx) {
  if (idx === 0) return "Hoy";
  if (idx === 1) return "Mañana";
  const d = new Date(iso);
  const s = new Intl.DateTimeFormat("es-AR", { weekday: "short", day: "2-digit", month: "short", timeZone: tz }).format(d);
  return s.charAt(0).toUpperCase() + s.slice(1).replace(".", "");
}
function timeLabel(iso, tz) {
  const d = new Date(iso);
  return new Intl.DateTimeFormat("es-AR", { hour: "2-digit", minute: "2-digit", hour12: false, timeZone: tz }).format(d);
}

// --- Search & geolocation ---
async function geocode(q) {
  const url = `${API_GEOCODE}?name=${encodeURIComponent(q)}&count=8&language=es&format=json`;
  const r = await fetch(url);
  if (!r.ok) throw new Error("geocode");
  const j = await r.json();
  return j.results || [];
}

async function reverseGeocode(lat, lon) {
  try {
    const url = `${API_REVERSE}?latitude=${lat}&longitude=${lon}&language=es&count=1&format=json`;
    const r = await fetch(url);
    if (!r.ok) return null;
    const j = await r.json();
    return (j.results && j.results[0]) || null;
  } catch { return null; }
}

function renderSuggest(items) {
  const box = $("suggest");
  if (!items.length) { box.hidden = true; box.innerHTML = ""; return; }
  box.innerHTML = items.map((it, idx) => {
    const name = [it.name, it.admin1, it.country].filter(Boolean).join(", ");
    return `<button data-idx="${idx}">${name}</button>`;
  }).join("");
  box.hidden = false;
  box.querySelectorAll("button").forEach((b) => {
    b.addEventListener("click", () => {
      const it = items[+b.dataset.idx];
      selectPlace({
        name: it.name,
        country: it.country || "",
        admin1: it.admin1 || "",
        lat: it.latitude,
        lon: it.longitude,
        tz: it.timezone || "auto",
      });
      box.hidden = true;
      $("q").value = "";
    });
  });
}

async function selectPlace(p) {
  state.place = p;
  localStorage.setItem("place", JSON.stringify(p));
  await loadWeather();
}

function getSavedPlace() {
  try {
    const s = localStorage.getItem("place");
    return s ? JSON.parse(s) : null;
  } catch { return null; }
}

// --- Alerts generator (Open-Meteo has no global alert feed; derive from data) ---
function buildAlerts(w) {
  const out = [];
  const h = w.hourly;
  if (!h) return out;

  const now = new Date();
  const upcoming = h.time.map((iso, i) => ({ i, t: new Date(iso) }))
    .filter((x) => x.t >= now && x.t - now <= 24 * 3600 * 1000);

  const max = (arr, idxs) => idxs.reduce((m, i) => Math.max(m, arr[i] ?? -Infinity), -Infinity);
  const sum = (arr, idxs) => idxs.reduce((s, i) => s + (arr[i] ?? 0), 0);
  const any = (arr, idxs, pred) => idxs.some((i) => pred(arr[i]));

  const idxs = upcoming.map((x) => x.i);

  // Thunderstorm in next 24h
  if (any(h.weathercode, idxs, (c) => c >= 95 && c <= 99)) {
    const when = upcoming.find((x) => h.weathercode[x.i] >= 95);
    out.push({
      level: "alert",
      ico: "⛈️",
      title: "Tormenta eléctrica prevista",
      msg: `Se esperan tormentas hacia las ${timeLabel(h.time[when.i], w.timezone)}. Evitá zonas abiertas y desconectá electrónicos sensibles.`,
    });
  }

  // Heavy rain (≥ 20 mm en 24h o ≥ 10 mm en 1h)
  const rain24 = sum(h.precipitation, idxs);
  const rain1h = max(h.precipitation, idxs);
  if (rain1h >= 10) {
    out.push({ level: "alert", ico: "🌧️", title: "Lluvia intensa", msg: `Pico de ${rain1h.toFixed(1)} mm/h en las próximas horas. Posibles anegamientos.` });
  } else if (rain24 >= 20) {
    out.push({ level: "warn", ico: "🌧️", title: "Lluvias acumuladas", msg: `~${rain24.toFixed(0)} mm en 24 h. Precaución al conducir.` });
  }

  // Strong wind (ráfagas ≥ 60 km/h) o viento sostenido ≥ 40
  const gust = max(h.windgusts_10m || [], idxs);
  const wind = max(h.windspeed_10m || [], idxs);
  if (gust >= 75) {
    out.push({ level: "alert", ico: "💨", title: "Viento fuerte", msg: `Ráfagas de hasta ${Math.round(gust)} km/h. Asegurá objetos sueltos.` });
  } else if (gust >= 60 || wind >= 40) {
    out.push({ level: "warn", ico: "💨", title: "Viento moderado a fuerte", msg: `Ráfagas ~${Math.round(gust)} km/h, sostenido ~${Math.round(wind)} km/h.` });
  }

  // Extreme temperature
  const tmax = max(h.temperature_2m, idxs);
  const tmin = Math.min(...idxs.map((i) => h.temperature_2m[i]));
  if (tmax >= 35) out.push({ level: "alert", ico: "🥵", title: "Calor extremo", msg: `Se esperan ${Math.round(tmax)} °C. Hidratate y evitá el sol entre 11 y 16 h.` });
  else if (tmax >= 32) out.push({ level: "warn", ico: "☀️", title: "Calor intenso", msg: `Máxima cerca de ${Math.round(tmax)} °C.` });
  if (tmin <= 0) out.push({ level: "alert", ico: "🥶", title: "Heladas", msg: `Temperatura mínima ${Math.round(tmin)} °C. Cuidá plantas y cañerías.` });

  // Snow
  if (any(h.weathercode, idxs, (c) => c >= 71 && c <= 86)) {
    out.push({ level: "warn", ico: "❄️", title: "Nevadas", msg: "Se esperan nevadas en las próximas horas." });
  }

  // Fog
  if (any(h.weathercode, idxs.slice(0, 6), (c) => c === 45 || c === 48)) {
    out.push({ level: "warn", ico: "🌫️", title: "Niebla", msg: "Visibilidad reducida en las próximas horas. Precaución al conducir." });
  }

  // UV extreme
  if (w.daily && w.daily.uv_index_max && w.daily.uv_index_max[0] != null && w.daily.uv_index_max[0] >= 8) {
    out.push({ level: "warn", ico: "☀️", title: "Índice UV muy alto", msg: `UV máximo ${w.daily.uv_index_max[0].toFixed(0)}. Usá protector solar y sombrero.` });
  }

  return out;
}

function renderAlerts(list) {
  const box = $("alerts");
  if (!list.length) { box.hidden = true; box.innerHTML = ""; return; }
  box.hidden = false;
  box.innerHTML = list.map((a) => `
    <div class="alert ${a.level === "warn" ? "warn" : ""}">
      <div class="ico">${a.ico}</div>
      <div class="body">
        <p class="title">${a.title}</p>
        <p class="msg">${a.msg}</p>
      </div>
    </div>`).join("");
}

// --- Fetch weather ---
async function fetchWeather(lat, lon, tz) {
  const params = new URLSearchParams({
    latitude: lat,
    longitude: lon,
    timezone: tz || "auto",
    current: [
      "temperature_2m", "apparent_temperature", "relative_humidity_2m",
      "precipitation", "weather_code", "wind_speed_10m", "wind_gusts_10m",
      "wind_direction_10m", "is_day",
    ].join(","),
    hourly: [
      "temperature_2m", "apparent_temperature", "precipitation_probability",
      "precipitation", "weather_code", "wind_speed_10m", "wind_gusts_10m",
      "relative_humidity_2m",
    ].join(","),
    daily: [
      "weather_code", "temperature_2m_max", "temperature_2m_min",
      "precipitation_sum", "precipitation_probability_max",
      "wind_speed_10m_max", "wind_gusts_10m_max", "uv_index_max",
      "sunrise", "sunset",
    ].join(","),
    wind_speed_unit: "kmh",
    forecast_days: 7,
  });
  const r = await fetch(`${API_FORECAST}?${params}`);
  if (!r.ok) throw new Error("forecast");
  const j = await r.json();
  // Normalize keys (API returns snake_case; some older docs used camelCase)
  j.hourly.windspeed_10m = j.hourly.wind_speed_10m;
  j.hourly.windgusts_10m = j.hourly.wind_gusts_10m;
  j.hourly.weathercode   = j.hourly.weather_code;
  j.daily.weathercode    = j.daily.weather_code;
  return j;
}

function applyTheme(code, isDay) {
  const t = wmo(code).theme;
  const cls = (!isDay && (t === "clear" || t === "cloud")) ? "theme-night" : `theme-${t}`;
  document.body.className = cls;
}

function renderNow(w, place) {
  const c = w.current;
  $("place").textContent = [place.name, place.admin1, place.country].filter(Boolean).join(", ");
  $("desc").textContent = wmo(c.weather_code).t;
  $("icon").textContent = wmo(c.weather_code).i;
  $("temp").textContent = fmtT(c.temperature_2m);
  $("feels").textContent = `Sensación ${fmtT(c.apparent_temperature)}`;
  $("updated").textContent = `Actualizado ${timeLabel(c.time, w.timezone)}`;

  $("n-rain").textContent = fmtMm(c.precipitation);
  $("n-wind").textContent = fmtKmh(c.wind_speed_10m);
  $("n-gust").textContent = fmtKmh(c.wind_gusts_10m);
  $("n-hum").textContent  = fmtPct(c.relative_humidity_2m);
  $("n-uv").textContent   = (w.daily.uv_index_max?.[0] ?? "--").toString().replace(/^(\d+(?:\.\d)?).*/, "$1");
  const rise = w.daily.sunrise?.[0], set = w.daily.sunset?.[0];
  $("n-sun").textContent  = rise && set ? `${timeLabel(rise, w.timezone)} / ${timeLabel(set, w.timezone)}` : "--";

  applyTheme(c.weather_code, c.is_day);
}

function renderHourly(w) {
  const h = w.hourly;
  const now = new Date();
  const startIdx = h.time.findIndex((iso) => new Date(iso) >= now);
  const s = Math.max(0, startIdx === -1 ? 0 : startIdx - 0);
  const end = Math.min(s + 24, h.time.length);
  const frag = [];
  for (let i = s; i < end; i++) {
    const meta = wmo(h.weathercode[i]);
    const isNow = i === s;
    frag.push(`
      <div class="h-item ${isNow ? "now-item" : ""}" role="listitem">
        <div class="h-time">${isNow ? "Ahora" : hourLabel(h.time[i], w.timezone)}</div>
        <div class="h-ico" title="${meta.t}">${meta.i}</div>
        <div class="h-t">${fmtT(h.temperature_2m[i])}</div>
        <div class="h-rain">💧 ${fmtPct(h.precipitation_probability?.[i])}</div>
        <div class="h-wind">💨 ${Math.round(h.windspeed_10m[i] ?? 0)}</div>
      </div>`);
  }
  $("hourly").innerHTML = frag.join("");
}

function renderDaily(w) {
  const d = w.daily;
  const rows = d.time.map((iso, idx) => {
    const meta = wmo(d.weathercode[idx]);
    return `
      <div class="d-row">
        <div class="d-day">${dayLabel(iso, w.timezone, idx)}</div>
        <div class="d-ico" title="${meta.t}">${meta.i}</div>
        <div class="d-rain">💧 ${fmtPct(d.precipitation_probability_max?.[idx])} · 💨 ${Math.round(d.wind_gusts_10m_max?.[idx] ?? 0)} km/h</div>
        <div class="d-tmp"><span class="hi">${fmtT(d.temperature_2m_max[idx])}</span> / <span class="lo">${fmtT(d.temperature_2m_min[idx])}</span></div>
      </div>`;
  }).join("");
  $("daily").innerHTML = rows;
}

async function loadWeather() {
  if (!state.place) return;
  toast("Cargando pronóstico…", 1500);
  try {
    const w = await fetchWeather(state.place.lat, state.place.lon, state.place.tz);
    renderNow(w, state.place);
    renderHourly(w);
    renderDaily(w);
    renderAlerts(buildAlerts(w));
  } catch (e) {
    console.error(e);
    toast("No se pudo obtener el pronóstico. Revisá tu conexión.", 4000);
  }
}

// --- Wiring ---
function wire() {
  const q = $("q");
  let deb;
  q.addEventListener("input", () => {
    clearTimeout(deb);
    const v = q.value.trim();
    if (v.length < 2) { renderSuggest([]); return; }
    deb = setTimeout(async () => {
      try { renderSuggest(await geocode(v)); }
      catch { /* silencio */ }
    }, 250);
  });
  q.addEventListener("keydown", async (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      const v = q.value.trim();
      if (!v) return;
      const res = await geocode(v);
      if (res[0]) {
        selectPlace({
          name: res[0].name, country: res[0].country || "",
          admin1: res[0].admin1 || "",
          lat: res[0].latitude, lon: res[0].longitude,
          tz: res[0].timezone || "auto",
        });
        q.value = "";
        $("suggest").hidden = true;
      } else {
        toast("Ciudad no encontrada");
      }
    }
  });

  $("btn-search").addEventListener("click", () => {
    q.focus();
  });

  $("btn-geo").addEventListener("click", () => {
    if (!navigator.geolocation) return toast("Geolocalización no disponible");
    toast("Obteniendo ubicación…", 1500);
    navigator.geolocation.getCurrentPosition(async (pos) => {
      const { latitude, longitude } = pos.coords;
      const g = await reverseGeocode(latitude, longitude);
      selectPlace({
        name: g?.name || "Mi ubicación",
        country: g?.country || "",
        admin1: g?.admin1 || "",
        lat: latitude, lon: longitude,
        tz: g?.timezone || "auto",
      });
    }, (err) => {
      console.warn(err);
      toast("No se pudo obtener tu ubicación");
    }, { enableHighAccuracy: false, timeout: 10000, maximumAge: 5 * 60 * 1000 });
  });

  document.addEventListener("click", (e) => {
    if (!e.target.closest(".search") && !e.target.closest(".suggest")) {
      $("suggest").hidden = true;
    }
  });
}

async function init() {
  wire();
  const saved = getSavedPlace();
  if (saved) { state.place = saved; await loadWeather(); }
  else {
    // Arranque: intenta geolocalización silenciosa; si falla, usa Buenos Aires.
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(async (pos) => {
        const g = await reverseGeocode(pos.coords.latitude, pos.coords.longitude);
        selectPlace({
          name: g?.name || "Mi ubicación",
          country: g?.country || "", admin1: g?.admin1 || "",
          lat: pos.coords.latitude, lon: pos.coords.longitude,
          tz: g?.timezone || "auto",
        });
      }, () => {
        selectPlace({ name: "Buenos Aires", country: "Argentina", admin1: "CABA", lat: -34.6037, lon: -58.3816, tz: "America/Argentina/Buenos_Aires" });
      }, { timeout: 6000 });
    } else {
      selectPlace({ name: "Buenos Aires", country: "Argentina", admin1: "CABA", lat: -34.6037, lon: -58.3816, tz: "America/Argentina/Buenos_Aires" });
    }
  }

  // Auto-refresh every 10 min
  setInterval(() => state.place && loadWeather(), 10 * 60 * 1000);

  if ("serviceWorker" in navigator) {
    try { await navigator.serviceWorker.register("sw.js"); } catch (e) { /* noop */ }
  }
}

document.addEventListener("DOMContentLoaded", init);
