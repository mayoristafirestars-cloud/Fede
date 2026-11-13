CREATE TABLE IF NOT EXISTS operaciones_mostrador(id INTEGER PRIMARY KEY,clave TEXT UNIQUE NOT NULL,tipo TEXT NOT NULL,payload TEXT NOT NULL,resultado TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS cotizaciones_pos(id TEXT PRIMARY KEY,datos TEXT NOT NULL,responsable_id INTEGER NOT NULL,vence REAL NOT NULL);
CREATE TABLE IF NOT EXISTS ventas_pos(
 id INTEGER PRIMARY KEY,cotizacion_id TEXT UNIQUE NOT NULL,responsable TEXT NOT NULL,
 subtotal TEXT NOT NULL,descuento TEXT NOT NULL,total TEXT NOT NULL,porcentaje TEXT NOT NULL,motivo_descuento TEXT NOT NULL,
 estado TEXT NOT NULL DEFAULT 'registrada',cobro TEXT NOT NULL DEFAULT 'pendiente',
 creado TEXT NOT NULL DEFAULT(strftime('%Y-%m-%dT%H:%M:%fZ','now'))
);
CREATE TABLE IF NOT EXISTS lineas_pos(
 id INTEGER PRIMARY KEY,venta_id INTEGER NOT NULL REFERENCES ventas_pos(id),producto_id INTEGER NOT NULL REFERENCES productos(id),
 descripcion TEXT NOT NULL,unidad TEXT NOT NULL,cantidad TEXT NOT NULL,precio TEXT NOT NULL,
 bruto TEXT NOT NULL,descuento TEXT NOT NULL,neto TEXT NOT NULL,devuelto TEXT NOT NULL DEFAULT '0',reintegro TEXT NOT NULL DEFAULT '0',datos TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS correcciones_pos(
 id INTEGER PRIMARY KEY,venta_id INTEGER NOT NULL REFERENCES ventas_pos(id),tipo TEXT NOT NULL,motivo TEXT NOT NULL,
 destino TEXT NOT NULL,importe TEXT NOT NULL,responsable TEXT NOT NULL,
 creado TEXT NOT NULL DEFAULT(strftime('%Y-%m-%dT%H:%M:%fZ','now'))
);
CREATE TABLE IF NOT EXISTS correccion_lineas_pos(correccion_id INTEGER NOT NULL REFERENCES correcciones_pos(id),linea_id INTEGER NOT NULL REFERENCES lineas_pos(id),cantidad TEXT NOT NULL,importe TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS carritos_suspendidos(
 id INTEGER PRIMARY KEY,nombre TEXT NOT NULL,datos TEXT NOT NULL,responsable_id INTEGER NOT NULL,responsable TEXT NOT NULL,
 estado TEXT NOT NULL DEFAULT 'disponible',recuperado_por TEXT,
 creado TEXT NOT NULL DEFAULT(strftime('%Y-%m-%dT%H:%M:%fZ','now'))
);
CREATE TABLE IF NOT EXISTS favoritos_pos(responsable_id INTEGER NOT NULL,producto_id INTEGER NOT NULL REFERENCES productos(id),PRIMARY KEY(responsable_id,producto_id));
CREATE TABLE IF NOT EXISTS reglas_peso(
 id INTEGER PRIMARY KEY,nombre TEXT NOT NULL,prefijo TEXT NOT NULL UNIQUE,codigo_desde INTEGER NOT NULL,codigo_largo INTEGER NOT NULL,
 valor_desde INTEGER NOT NULL,valor_largo INTEGER NOT NULL,decimales INTEGER NOT NULL,tipo TEXT NOT NULL,unidad_peso TEXT NOT NULL,activo INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS politica_reposicion(
 producto_id INTEGER PRIMARY KEY REFERENCES productos(id),venta_diaria TEXT,dias_cobertura INTEGER NOT NULL DEFAULT 2,
 dias_entrega INTEGER NOT NULL DEFAULT 0,seguridad TEXT NOT NULL DEFAULT '0'
);
CREATE TABLE IF NOT EXISTS tipos_envase(id INTEGER PRIMARY KEY,nombre TEXT NOT NULL UNIQUE);
CREATE TABLE IF NOT EXISTS movimientos_envase(
 id INTEGER PRIMARY KEY,proveedor_id INTEGER NOT NULL REFERENCES proveedores(id),envase_id INTEGER NOT NULL REFERENCES tipos_envase(id),
 tipo TEXT NOT NULL,cantidad INTEGER NOT NULL,importe TEXT NOT NULL DEFAULT '0',referencia TEXT NOT NULL,motivo TEXT NOT NULL,responsable TEXT NOT NULL,
 creado TEXT NOT NULL DEFAULT(strftime('%Y-%m-%dT%H:%M:%fZ','now'))
);
