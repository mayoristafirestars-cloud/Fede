CREATE TABLE IF NOT EXISTS ubicaciones_stock(id INTEGER PRIMARY KEY,nombre TEXT NOT NULL UNIQUE,vendible INTEGER NOT NULL);
INSERT OR IGNORE INTO ubicaciones_stock VALUES(1,'Salón',1),(2,'Depósito',1),(3,'Cámara',1),(4,'Cuarentena',0);
CREATE TABLE IF NOT EXISTS inventario_productos(producto_id INTEGER PRIMARY KEY REFERENCES productos(id));
CREATE TABLE IF NOT EXISTS lotes_stock(
 id INTEGER PRIMARY KEY,producto_id INTEGER NOT NULL REFERENCES productos(id),origen TEXT NOT NULL,
 recepcion_id INTEGER REFERENCES recepciones_compra(id),linea_id INTEGER REFERENCES pedido_lineas(id),
 proveedor_id INTEGER REFERENCES proveedores(id),unidad TEXT NOT NULL,costo_unitario TEXT,
 estado TEXT NOT NULL DEFAULT 'listo',notas TEXT NOT NULL DEFAULT '',proxima_revision TEXT,
 ingreso TEXT NOT NULL DEFAULT(strftime('%Y-%m-%dT%H:%M:%fZ','now')),UNIQUE(recepcion_id,linea_id)
);
CREATE TABLE IF NOT EXISTS existencias_lote(
 lote_id INTEGER NOT NULL REFERENCES lotes_stock(id),ubicacion_id INTEGER NOT NULL REFERENCES ubicaciones_stock(id),
 cantidad TEXT NOT NULL DEFAULT '0',version INTEGER NOT NULL DEFAULT 0,PRIMARY KEY(lote_id,ubicacion_id)
);
CREATE TABLE IF NOT EXISTS movimientos_stock(
 id INTEGER PRIMARY KEY,lote_id INTEGER NOT NULL REFERENCES lotes_stock(id),ubicacion_id INTEGER NOT NULL REFERENCES ubicaciones_stock(id),
 producto_id INTEGER NOT NULL REFERENCES productos(id),tipo TEXT NOT NULL,cantidad TEXT NOT NULL,unidad TEXT NOT NULL,
 costo_unitario TEXT,costo_total TEXT,responsable TEXT NOT NULL,motivo TEXT NOT NULL,
 origen_clave TEXT NOT NULL UNIQUE,documento_id INTEGER,asignacion TEXT NOT NULL DEFAULT 'declarada',
 creado TEXT NOT NULL DEFAULT(strftime('%Y-%m-%dT%H:%M:%fZ','now'))
);
CREATE TABLE IF NOT EXISTS operaciones_inventario(
 id INTEGER PRIMARY KEY,clave TEXT NOT NULL UNIQUE,tipo TEXT NOT NULL,payload TEXT NOT NULL,resultado TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS revisiones_lote(
 id INTEGER PRIMARY KEY,lote_id INTEGER NOT NULL REFERENCES lotes_stock(id),anterior TEXT NOT NULL,estado TEXT NOT NULL,
 notas TEXT NOT NULL,proxima_revision TEXT,responsable TEXT NOT NULL,
 creado TEXT NOT NULL DEFAULT(strftime('%Y-%m-%dT%H:%M:%fZ','now'))
);
CREATE TABLE IF NOT EXISTS conteos_stock(
 id INTEGER PRIMARY KEY,lote_id INTEGER NOT NULL REFERENCES lotes_stock(id),ubicacion_id INTEGER NOT NULL REFERENCES ubicaciones_stock(id),
 esperado TEXT NOT NULL,contado TEXT NOT NULL,version INTEGER NOT NULL,motivo TEXT NOT NULL,
 responsable TEXT NOT NULL,estado TEXT NOT NULL DEFAULT 'pendiente',aprobador TEXT,
 creado TEXT NOT NULL DEFAULT(strftime('%Y-%m-%dT%H:%M:%fZ','now')),aprobado TEXT
);
CREATE TABLE IF NOT EXISTS politica_stock(producto_id INTEGER PRIMARY KEY REFERENCES productos(id),minimo TEXT NOT NULL DEFAULT '0',dias_sin_venta INTEGER NOT NULL DEFAULT 7);
CREATE TABLE IF NOT EXISTS devoluciones_proveedor(
 id INTEGER PRIMARY KEY,lote_id INTEGER NOT NULL REFERENCES lotes_stock(id),ubicacion_id INTEGER NOT NULL REFERENCES ubicaciones_stock(id),
 recepcion_id INTEGER NOT NULL REFERENCES recepciones_compra(id),proveedor_id INTEGER NOT NULL REFERENCES proveedores(id),
 cantidad TEXT NOT NULL,motivo TEXT NOT NULL,responsable TEXT NOT NULL,
 creado TEXT NOT NULL DEFAULT(strftime('%Y-%m-%dT%H:%M:%fZ','now'))
);
CREATE TABLE IF NOT EXISTS reclamos_proveedor(
 id INTEGER PRIMARY KEY,recepcion_id INTEGER NOT NULL REFERENCES recepciones_compra(id),proveedor_id INTEGER NOT NULL REFERENCES proveedores(id),
 tipo TEXT NOT NULL,detalle TEXT NOT NULL,estado TEXT NOT NULL DEFAULT 'abierto',responsable TEXT NOT NULL,
 creado TEXT NOT NULL DEFAULT(strftime('%Y-%m-%dT%H:%M:%fZ','now'))
);
CREATE TABLE IF NOT EXISTS eventos_reclamo(
 id INTEGER PRIMARY KEY,reclamo_id INTEGER NOT NULL REFERENCES reclamos_proveedor(id),estado TEXT NOT NULL,
 nota TEXT NOT NULL,responsable TEXT NOT NULL,creado TEXT NOT NULL DEFAULT(strftime('%Y-%m-%dT%H:%M:%fZ','now'))
);
CREATE TABLE IF NOT EXISTS cuenta_proveedor(
 id INTEGER PRIMARY KEY,proveedor_id INTEGER NOT NULL REFERENCES proveedores(id),recepcion_id INTEGER NOT NULL REFERENCES recepciones_compra(id),
 tipo TEXT NOT NULL,importe TEXT NOT NULL,referencia TEXT NOT NULL,motivo TEXT NOT NULL,responsable TEXT NOT NULL,
 fecha TEXT NOT NULL,vencimiento TEXT,medio TEXT,reversa_de INTEGER UNIQUE REFERENCES cuenta_proveedor(id),
 devolucion_id INTEGER REFERENCES devoluciones_proveedor(id),reclamo_id INTEGER REFERENCES reclamos_proveedor(id),
 origen_clave TEXT NOT NULL UNIQUE,creado TEXT NOT NULL DEFAULT(strftime('%Y-%m-%dT%H:%M:%fZ','now'))
);
CREATE INDEX IF NOT EXISTS idx_mov_stock_producto ON movimientos_stock(producto_id,id);
CREATE INDEX IF NOT EXISTS idx_cuenta_proveedor ON cuenta_proveedor(proveedor_id,recepcion_id);
