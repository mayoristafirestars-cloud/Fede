CREATE TABLE IF NOT EXISTS publicaciones_web (
 producto_id INTEGER PRIMARY KEY REFERENCES productos(id),
 visible INTEGER NOT NULL DEFAULT 0 CHECK(visible IN (0,1))
);
CREATE TABLE IF NOT EXISTS pedidos_web (
 id TEXT PRIMARY KEY, clave_operacion TEXT NOT NULL UNIQUE, acceso_hash TEXT NOT NULL,
 payload TEXT NOT NULL, nombre TEXT NOT NULL, telefono TEXT NOT NULL,
 estado TEXT NOT NULL DEFAULT 'recibido', version INTEGER NOT NULL DEFAULT 1,
 lineas TEXT NOT NULL, estimado TEXT NOT NULL, preparacion TEXT,
 final TEXT, responsable TEXT, aprobado_en TEXT,
 creado TEXT NOT NULL DEFAULT(strftime('%Y-%m-%dT%H:%M:%fZ','now'))
);
CREATE TABLE IF NOT EXISTS acciones_web (
 clave TEXT PRIMARY KEY, pedido_id TEXT NOT NULL REFERENCES pedidos_web(id),
 tipo TEXT NOT NULL, payload TEXT NOT NULL, resultado TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS limites_web (clave TEXT PRIMARY KEY, cantidad INTEGER NOT NULL, minuto INTEGER NOT NULL);
CREATE TABLE IF NOT EXISTS configuracion_web(id INTEGER PRIMARY KEY CHECK(id=1),datos TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS franjas_web(id INTEGER PRIMARY KEY,inicio TEXT NOT NULL,fin TEXT NOT NULL,cupo INTEGER NOT NULL,activa INTEGER NOT NULL DEFAULT 1);
CREATE TABLE IF NOT EXISTS reservas_web(pedido_id TEXT NOT NULL REFERENCES pedidos_web(id),producto_id INTEGER NOT NULL REFERENCES productos(id),cantidad TEXT NOT NULL,vence REAL NOT NULL,PRIMARY KEY(pedido_id,producto_id));
CREATE INDEX IF NOT EXISTS idx_reservas_web_producto ON reservas_web(producto_id,vence);
CREATE TABLE IF NOT EXISTS reclamos_web(id TEXT PRIMARY KEY,pedido_id TEXT NOT NULL REFERENCES pedidos_web(id),clave TEXT NOT NULL UNIQUE,payload TEXT NOT NULL,producto_id INTEGER,tipo TEXT NOT NULL,detalle TEXT NOT NULL,estado TEXT NOT NULL DEFAULT 'abierto',version INTEGER NOT NULL DEFAULT 1,creado TEXT NOT NULL DEFAULT(strftime('%Y-%m-%dT%H:%M:%fZ','now')));
CREATE TABLE IF NOT EXISTS respuestas_web(id INTEGER PRIMARY KEY,reclamo_id TEXT NOT NULL REFERENCES reclamos_web(id),texto TEXT NOT NULL,responsable TEXT NOT NULL,creado TEXT NOT NULL DEFAULT(strftime('%Y-%m-%dT%H:%M:%fZ','now')));
CREATE TABLE IF NOT EXISTS costos_web(id INTEGER PRIMARY KEY,pedido_id TEXT NOT NULL REFERENCES pedidos_web(id),datos TEXT NOT NULL,responsable TEXT NOT NULL,creado TEXT NOT NULL DEFAULT(strftime('%Y-%m-%dT%H:%M:%fZ','now')));
CREATE TABLE IF NOT EXISTS promociones_web(
 id INTEGER PRIMARY KEY,producto_id INTEGER NOT NULL REFERENCES productos(id),titulo TEXT NOT NULL,
 precio TEXT NOT NULL,precio_referencia TEXT NOT NULL,unidad TEXT NOT NULL,
 desde REAL NOT NULL,hasta REAL NOT NULL,activa INTEGER NOT NULL DEFAULT 1,
 responsable TEXT NOT NULL,motivo TEXT NOT NULL,costo_referencia TEXT,
 clave TEXT NOT NULL UNIQUE,payload TEXT NOT NULL,
 cancelada_por TEXT,cancelada_en REAL,
 creado TEXT NOT NULL DEFAULT(strftime('%Y-%m-%dT%H:%M:%fZ','now'))
);
CREATE INDEX IF NOT EXISTS idx_promociones_web_producto ON promociones_web(producto_id,desde,hasta);
