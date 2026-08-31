"""Catálogo de aeropuertos: coordenadas, nombres y vecinos por carretera.

El catálogo no pretende ser exhaustivo: cubre Argentina completa (que es de
donde sale el usuario) y los destinos internacionales que se vuelan desde
acá. Un código desconocido no rompe nada, sólo pierde las funciones que
dependen de coordenadas.
"""
from __future__ import annotations

import math
import unicodedata
from dataclasses import dataclass


@dataclass(frozen=True)
class Aeropuerto:
    iata: str
    nombre: str
    ciudad: str
    pais: str
    lat: float
    lon: float


def _a(iata, nombre, ciudad, pais, lat, lon) -> tuple[str, Aeropuerto]:
    return iata, Aeropuerto(iata, nombre, ciudad, pais, lat, lon)


AEROPUERTOS: dict[str, Aeropuerto] = dict([
    # --- Argentina ---
    _a("AEP", "Aeroparque Jorge Newbery", "Buenos Aires", "AR", -34.5592, -58.4156),
    _a("EZE", "Ministro Pistarini", "Buenos Aires", "AR", -34.8222, -58.5358),
    _a("COR", "Ingeniero Taravella", "Córdoba", "AR", -31.3236, -64.2080),
    _a("MDZ", "El Plumerillo", "Mendoza", "AR", -32.8317, -68.7929),
    _a("ROS", "Islas Malvinas", "Rosario", "AR", -32.9036, -60.7850),
    _a("BRC", "Teniente Candelaria", "San Carlos de Bariloche", "AR", -41.1512, -71.1575),
    _a("SLA", "Martín Miguel de Güemes", "Salta", "AR", -24.8560, -65.4862),
    _a("TUC", "Teniente Benjamín Matienzo", "San Miguel de Tucumán", "AR", -26.8409, -65.1049),
    _a("IGR", "Cataratas del Iguazú", "Puerto Iguazú", "AR", -25.7373, -54.4734),
    _a("USH", "Malvinas Argentinas", "Ushuaia", "AR", -54.8433, -68.2958),
    _a("FTE", "Comandante Armando Tola", "El Calafate", "AR", -50.2803, -72.0531),
    _a("NQN", "Presidente Perón", "Neuquén", "AR", -38.9490, -68.1557),
    _a("BHI", "Comandante Espora", "Bahía Blanca", "AR", -38.7250, -62.1693),
    _a("MDQ", "Astor Piazzolla", "Mar del Plata", "AR", -37.9342, -57.5733),
    _a("RSA", "Santa Rosa", "Santa Rosa (La Pampa)", "AR", -36.5883, -64.2757),
    _a("CRD", "General Mosconi", "Comodoro Rivadavia", "AR", -45.7853, -67.4655),
    _a("REL", "Almirante Zar", "Trelew", "AR", -43.2105, -65.2703),
    _a("PMY", "El Tehuelche", "Puerto Madryn", "AR", -42.7592, -65.1027),
    _a("RGL", "Piloto Civil N. Fernández", "Río Gallegos", "AR", -51.6089, -69.3126),
    _a("RGA", "Hermes Quijada", "Río Grande", "AR", -53.7777, -67.7494),
    _a("POS", "Libertador Gral. San Martín", "Posadas", "AR", -27.3858, -55.9707),
    _a("CNQ", "Doctor Fernando Piragine", "Corrientes", "AR", -27.4455, -58.7619),
    _a("RES", "Resistencia", "Resistencia", "AR", -27.4500, -59.0561),
    _a("SDE", "Vicecomodoro Á. de la Paz", "Santiago del Estero", "AR", -27.7656, -64.3100),
    _a("JUJ", "Gobernador Horacio Guzmán", "San Salvador de Jujuy", "AR", -24.3928, -65.0978),
    _a("CTC", "Coronel Felipe Varela", "San Fernando del Valle", "AR", -28.5656, -65.7517),
    _a("IRJ", "Capitán Vicente Almandos", "La Rioja", "AR", -29.3816, -66.7958),
    _a("UAQ", "Domingo Faustino Sarmiento", "San Juan", "AR", -31.5715, -68.4182),
    _a("LUQ", "Brigadier Mayor C. Krause", "San Luis", "AR", -33.2732, -66.3564),
    _a("SFN", "Sauce Viejo", "Santa Fe", "AR", -31.7117, -60.8117),
    _a("PRA", "General Justo J. de Urquiza", "Paraná", "AR", -31.7948, -60.4804),
    _a("VDM", "Gobernador Castello", "Viedma", "AR", -40.8692, -63.0004),
    _a("ESQ", "Esquel", "Esquel", "AR", -42.9080, -71.1394),
    _a("CRV", "Caleta Olivia", "Caleta Olivia", "AR", -46.4363, -67.4611),
    _a("RCQ", "Reconquista", "Reconquista", "AR", -29.2103, -59.6800),
    _a("TDL", "Héroes de Malvinas", "Tandil", "AR", -37.2374, -59.2279),
    _a("OYA", "Goya", "Goya", "AR", -29.1058, -59.2189),
    _a("SIS", "San Rafael", "San Rafael", "AR", -34.5883, -68.4039),
    _a("AFA", "Suboficial Ay. Santiago Germano", "San Rafael", "AR", -34.5883, -68.4039),
    _a("RHD", "Termas de Río Hondo", "Termas de Río Hondo", "AR", -27.4966, -64.9360),

    # --- Sudamérica ---
    _a("MVD", "Carrasco", "Montevideo", "UY", -34.8384, -56.0308),
    _a("PDP", "Capitán Curbelo", "Punta del Este", "UY", -34.8551, -55.0943),
    _a("SCL", "Arturo Merino Benítez", "Santiago de Chile", "CL", -33.3930, -70.7858),
    _a("GRU", "Guarulhos", "São Paulo", "BR", -23.4356, -46.4731),
    _a("CGH", "Congonhas", "São Paulo", "BR", -23.6261, -46.6564),
    _a("GIG", "Galeão", "Río de Janeiro", "BR", -22.8100, -43.2506),
    _a("FLN", "Hercílio Luz", "Florianópolis", "BR", -27.6705, -48.5477),
    _a("SSA", "Deputado L. Magalhães", "Salvador", "BR", -12.9086, -38.3225),
    _a("REC", "Guararapes", "Recife", "BR", -8.1264, -34.9236),
    _a("FOR", "Pinto Martins", "Fortaleza", "BR", -3.7763, -38.5326),
    _a("LIM", "Jorge Chávez", "Lima", "PE", -12.0219, -77.1143),
    _a("CUZ", "Alejandro Velasco Astete", "Cusco", "PE", -13.5357, -71.9388),
    _a("BOG", "El Dorado", "Bogotá", "CO", 4.7016, -74.1469),
    _a("CTG", "Rafael Núñez", "Cartagena", "CO", 10.4424, -75.5130),
    _a("PTY", "Tocumen", "Ciudad de Panamá", "PA", 9.0714, -79.3835),
    _a("ASU", "Silvio Pettirossi", "Asunción", "PY", -25.2400, -57.5200),
    _a("VVI", "Viru Viru", "Santa Cruz", "BO", -17.6448, -63.1354),
    _a("UIO", "Mariscal Sucre", "Quito", "EC", -0.1292, -78.3575),

    # --- Norteamérica y Caribe ---
    _a("MIA", "Miami International", "Miami", "US", 25.7959, -80.2870),
    _a("MCO", "Orlando International", "Orlando", "US", 28.4312, -81.3081),
    _a("JFK", "John F. Kennedy", "Nueva York", "US", 40.6413, -73.7781),
    _a("EWR", "Newark Liberty", "Nueva York", "US", 40.6895, -74.1745),
    _a("LAX", "Los Angeles International", "Los Ángeles", "US", 33.9416, -118.4085),
    _a("IAH", "George Bush", "Houston", "US", 29.9902, -95.3368),
    _a("ATL", "Hartsfield-Jackson", "Atlanta", "US", 33.6407, -84.4277),
    _a("DFW", "Dallas/Fort Worth", "Dallas", "US", 32.8998, -97.0403),
    _a("MEX", "Benito Juárez", "Ciudad de México", "MX", 19.4361, -99.0719),
    _a("CUN", "Cancún", "Cancún", "MX", 21.0365, -86.8771),
    _a("PUJ", "Punta Cana", "Punta Cana", "DO", 18.5674, -68.3634),
    _a("HAV", "José Martí", "La Habana", "CU", 22.9892, -82.4091),
    _a("YYZ", "Pearson", "Toronto", "CA", 43.6777, -79.6248),

    # --- Europa ---
    _a("MAD", "Adolfo Suárez Barajas", "Madrid", "ES", 40.4936, -3.5668),
    _a("BCN", "El Prat", "Barcelona", "ES", 41.2974, 2.0833),
    _a("CDG", "Charles de Gaulle", "París", "FR", 49.0097, 2.5479),
    _a("ORY", "Orly", "París", "FR", 48.7233, 2.3794),
    _a("FCO", "Fiumicino", "Roma", "IT", 41.8003, 12.2389),
    _a("MXP", "Malpensa", "Milán", "IT", 45.6306, 8.7281),
    _a("LHR", "Heathrow", "Londres", "GB", 51.4700, -0.4543),
    _a("LGW", "Gatwick", "Londres", "GB", 51.1537, -0.1821),
    _a("FRA", "Frankfurt am Main", "Fráncfort", "DE", 50.0379, 8.5622),
    _a("MUC", "Franz Josef Strauss", "Múnich", "DE", 48.3538, 11.7861),
    _a("AMS", "Schiphol", "Ámsterdam", "NL", 52.3105, 4.7683),
    _a("LIS", "Humberto Delgado", "Lisboa", "PT", 38.7742, -9.1342),
    _a("OPO", "Francisco Sá Carneiro", "Oporto", "PT", 41.2481, -8.6814),
    _a("IST", "Istanbul Airport", "Estambul", "TR", 41.2753, 28.7519),
    _a("ZRH", "Zúrich", "Zúrich", "CH", 47.4647, 8.5492),
    _a("VIE", "Viena", "Viena", "AT", 48.1103, 16.5697),
    _a("ATH", "Eleftherios Venizelos", "Atenas", "GR", 37.9364, 23.9445),

    # --- Resto del mundo ---
    _a("DOH", "Hamad International", "Doha", "QA", 25.2731, 51.6080),
    _a("DXB", "Dubái", "Dubái", "AE", 25.2532, 55.3657),
    _a("JNB", "O. R. Tambo", "Johannesburgo", "ZA", -26.1392, 28.2460),
    _a("CPT", "Ciudad del Cabo", "Ciudad del Cabo", "ZA", -33.9715, 18.6021),
    _a("SYD", "Kingsford Smith", "Sídney", "AU", -33.9399, 151.1753),
    _a("AKL", "Auckland", "Auckland", "NZ", -37.0082, 174.7850),
    _a("NRT", "Narita", "Tokio", "JP", 35.7720, 140.3929),
    _a("HND", "Haneda", "Tokio", "JP", 35.5494, 139.7798),
    _a("BKK", "Suvarnabhumi", "Bangkok", "TH", 13.6900, 100.7501),
    _a("SIN", "Changi", "Singapur", "SG", 1.3644, 103.9915),
    _a("TLV", "Ben Gurión", "Tel Aviv", "IL", 32.0114, 34.8867),
])

#: Ciudades con más de un aeropuerto: buscar en una implica mirar las otras.
CIUDADES_MULTIAEROPUERTO: dict[str, list[str]] = {
    "Buenos Aires": ["AEP", "EZE"],
    "São Paulo": ["GRU", "CGH"],
    "París": ["CDG", "ORY"],
    "Londres": ["LHR", "LGW"],
    "Nueva York": ["JFK", "EWR"],
    "Tokio": ["NRT", "HND"],
}

#: Aeropuertos alcanzables por tierra desde una ciudad sin aeropuerto propio
#: o con oferta muy limitada. Clave: IATA base. Valor: (IATA alterno, km por ruta).
#: Los km son por carretera, no en línea recta: es lo que efectivamente maneja
#: el pasajero, y es lo que hay que descontar del ahorro.
VECINOS_TERRESTRES: dict[str, list[tuple[str, int]]] = {
    # Santa Rosa (La Pampa) tiene aeropuerto propio pero con poquísimas
    # frecuencias: casi siempre conviene manejar a alguna de estas.
    "RSA": [("BHI", 320), ("NQN", 520), ("AEP", 615), ("EZE", 640), ("MDQ", 620), ("COR", 700)],
    "BHI": [("RSA", 320), ("NQN", 540), ("AEP", 680), ("MDQ", 480)],
    "NQN": [("RSA", 520), ("BRC", 425), ("BHI", 540)],
    "AEP": [("EZE", 45), ("ROS", 300), ("MDQ", 400)],
    "EZE": [("AEP", 45), ("ROS", 320), ("MDQ", 385)],
    "ROS": [("AEP", 300), ("EZE", 320), ("COR", 400), ("SFN", 170)],
    "MDQ": [("AEP", 400), ("EZE", 385), ("TDL", 175), ("BHI", 480)],
    "COR": [("ROS", 400), ("SDE", 420), ("TUC", 570)],
    "MDZ": [("UAQ", 170), ("SIS", 235)],
    "BRC": [("NQN", 425), ("ESQ", 290)],
}


def normalizar(texto: str) -> str:
    """Minúsculas sin acentos, para buscar 'cordoba' y encontrar 'Córdoba'."""
    limpio = unicodedata.normalize("NFKD", texto.strip().lower())
    return "".join(c for c in limpio if not unicodedata.combining(c))


def buscar_aeropuerto(texto: str) -> list[Aeropuerto]:
    """Resuelve un código IATA o un nombre de ciudad a aeropuertos.

    Devuelve la lista ordenada por calidad de coincidencia: exacta primero.
    """
    t = normalizar(texto)
    if len(t) == 3 and t.upper() in AEROPUERTOS:
        return [AEROPUERTOS[t.upper()]]

    exactos, parciales = [], []
    for ap in AEROPUERTOS.values():
        ciudad = normalizar(ap.ciudad)
        if ciudad == t:
            exactos.append(ap)
        elif t in ciudad or t in normalizar(ap.nombre):
            parciales.append(ap)
    return exactos + parciales


def distancia_km(iata_a: str, iata_b: str) -> float | None:
    """Distancia ortodrómica entre dos aeropuertos. None si falta alguno."""
    a, b = AEROPUERTOS.get(iata_a.upper()), AEROPUERTOS.get(iata_b.upper())
    if not a or not b:
        return None
    radio = 6371.0
    dlat = math.radians(b.lat - a.lat)
    dlon = math.radians(b.lon - a.lon)
    h = (math.sin(dlat / 2) ** 2
         + math.cos(math.radians(a.lat)) * math.cos(math.radians(b.lat)) * math.sin(dlon / 2) ** 2)
    return 2 * radio * math.asin(math.sqrt(h))


def alternativos(iata: str, radio_km: int = 400) -> list[tuple[str, int]]:
    """Aeropuertos alternativos alcanzables por tierra, ordenados por cercanía.

    Combina la tabla de rutas conocidas con un barrido por distancia para los
    códigos que no están en la tabla.
    """
    iata = iata.upper()
    conocidos = {c: km for c, km in VECINOS_TERRESTRES.get(iata, []) if km <= radio_km}

    for ciudad, codigos in CIUDADES_MULTIAEROPUERTO.items():
        if iata in codigos:
            for otro in codigos:
                if otro != iata:
                    conocidos.setdefault(otro, 50)

    if not conocidos and iata in AEROPUERTOS:
        for codigo in AEROPUERTOS:
            if codigo == iata:
                continue
            d = distancia_km(iata, codigo)
            # 1.25 aproxima el rodeo de la ruta sobre la línea recta.
            if d is not None and d * 1.25 <= radio_km:
                conocidos[codigo] = int(d * 1.25)

    return sorted(conocidos.items(), key=lambda kv: kv[1])


def nombre(iata: str) -> str:
    ap = AEROPUERTOS.get(iata.upper())
    return f"{ap.ciudad} ({iata.upper()})" if ap else iata.upper()
