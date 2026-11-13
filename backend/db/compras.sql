CREATE TABLE IF NOT EXISTS responsables (
 id INTEGER PRIMARY KEY, nombre TEXT NOT NULL, rol TEXT NOT NULL,
 sal TEXT NOT NULL, clave_hash TEXT NOT NULL, intentos INTEGER NOT NULL DEFAULT 0,
 bloqueado_hasta REAL NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS sesiones_comerciales (
 token_hash TEXT PRIMARY KEY, responsable_id INTEGER NOT NULL REFERENCES responsables(id), vence REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS historial_comercial (
 id INTEGER PRIMARY KEY, producto_id INTEGER NOT NULL REFERENCES productos(id),
 tipo TEXT NOT NULL, importe TEXT NOT NULL, anterior TEXT, unidad TEXT NOT NULL,
 responsable TEXT NOT NULL, motivo TEXT NOT NULL, origen_id INTEGER,
 clave_operacion TEXT UNIQUE, payload TEXT,
 creado TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))
);
CREATE INDEX IF NOT EXISTS idx_historial_producto ON historial_comercial(producto_id,id);
CREATE TABLE IF NOT EXISTS proveedores (
 id INTEGER PRIMARY KEY, nombre TEXT NOT NULL, contacto TEXT NOT NULL DEFAULT '',
 telefono TEXT NOT NULL DEFAULT '', documento TEXT NOT NULL DEFAULT '',
 condiciones TEXT NOT NULL DEFAULT '', dias_plazo INTEGER NOT NULL DEFAULT 0,
 activo INTEGER NOT NULL DEFAULT 1
);
CREATE TABLE IF NOT EXISTS pedidos_compra (
 id INTEGER PRIMARY KEY, proveedor_id INTEGER NOT NULL REFERENCES proveedores(id),
 proveedor_nombre TEXT NOT NULL, condiciones TEXT NOT NULL, dias_plazo INTEGER NOT NULL,
 fecha_entrega TEXT, notas TEXT NOT NULL, responsable TEXT NOT NULL,
 clave_operacion TEXT NOT NULL UNIQUE, payload TEXT NOT NULL,
 creado TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))
);
CREATE TABLE IF NOT EXISTS pedido_lineas (
 id INTEGER PRIMARY KEY, pedido_id INTEGER NOT NULL REFERENCES pedidos_compra(id),
 producto_id INTEGER NOT NULL REFERENCES productos(id), descripcion TEXT NOT NULL,
 unidad TEXT NOT NULL, cantidad TEXT NOT NULL, recibido TEXT NOT NULL DEFAULT '0',
 precio TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS recepciones_compra (
 id INTEGER PRIMARY KEY, pedido_id INTEGER NOT NULL REFERENCES pedidos_compra(id),
 clave_operacion TEXT NOT NULL UNIQUE, payload TEXT NOT NULL, datos TEXT NOT NULL,
 creado TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))
);
CREATE TABLE IF NOT EXISTS movimientos_compra (
 id INTEGER PRIMARY KEY, recepcion_id INTEGER NOT NULL REFERENCES recepciones_compra(id),
 linea_id INTEGER NOT NULL REFERENCES pedido_lineas(id), producto_id INTEGER NOT NULL REFERENCES productos(id),
 cantidad TEXT NOT NULL, unidad TEXT NOT NULL, costo_total TEXT NOT NULL,
 UNIQUE(recepcion_id,linea_id)
);
