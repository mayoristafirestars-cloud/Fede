-- ============================================================
-- CORONEL SUR — Base de datos principal
-- ============================================================

-- PRODUCTOS / INVENTARIO
CREATE TABLE IF NOT EXISTS productos (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo          TEXT UNIQUE NOT NULL,
    descripcion     TEXT NOT NULL,
    rubro           TEXT,
    proveedor       TEXT,
    stock           REAL DEFAULT 0,
    precio_venta    REAL DEFAULT 0,
    precio_costo    REAL DEFAULT 0,
    fecha_ingreso   TEXT,   -- Fecha Modificado del CSV (ingreso real de stock)
    activo          INTEGER DEFAULT 1,
    creado_en       TEXT DEFAULT (datetime('now', 'localtime')),
    actualizado_en  TEXT DEFAULT (datetime('now', 'localtime'))
);

-- CLIENTES (base CS Más — 4180 clientes)
CREATE TABLE IF NOT EXISTS clientes (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre          TEXT NOT NULL,
    telefono        TEXT,
    email           TEXT,
    dni             TEXT,
    direccion       TEXT,
    tipo            TEXT DEFAULT 'minorista',  -- minorista | mayorista | institucional
    notas           TEXT,
    creado_en       TEXT DEFAULT (datetime('now', 'localtime')),
    actualizado_en  TEXT DEFAULT (datetime('now', 'localtime'))
);

-- FACTURAS / PRESUPUESTOS (cabecera)
CREATE TABLE IF NOT EXISTS comprobantes (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo            TEXT NOT NULL,  -- factura | presupuesto | nota_credito
    numero          TEXT,
    cliente_id      INTEGER REFERENCES clientes(id),
    cliente_nombre  TEXT,           -- para casos sin cliente registrado
    fecha           TEXT NOT NULL,
    subtotal        REAL DEFAULT 0,
    descuento       REAL DEFAULT 0,
    total           REAL DEFAULT 0,
    estado          TEXT DEFAULT 'activo',  -- activo | anulado | cobrado
    origen          TEXT DEFAULT 'sistema', -- sistema | importado
    creado_en       TEXT DEFAULT (datetime('now', 'localtime'))
);

-- DETALLE DE COMPROBANTES (ítems)
CREATE TABLE IF NOT EXISTS comprobante_items (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    comprobante_id  INTEGER NOT NULL REFERENCES comprobantes(id),
    producto_id     INTEGER REFERENCES productos(id),
    producto_desc   TEXT NOT NULL,
    cantidad        REAL NOT NULL,
    precio_unitario REAL NOT NULL,
    precio_costo    REAL DEFAULT 0,
    subtotal        REAL NOT NULL
);

-- VENTAS HISTÓRICAS (importadas de FactuPyme — solo lectura)
CREATE TABLE IF NOT EXISTS ventas_historicas (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha           TEXT,
    producto        TEXT,
    rubro           TEXT,
    costo_unit      REAL,
    cantidad        REAL,
    subtotal        REAL,
    ganancia        REAL,
    cliente         TEXT,
    origen          TEXT DEFAULT 'factura',  -- factura | presupuesto
    importado_en    TEXT DEFAULT (datetime('now', 'localtime'))
);

-- ÍNDICES para consultas frecuentes
CREATE INDEX IF NOT EXISTS idx_productos_rubro       ON productos(rubro);
CREATE INDEX IF NOT EXISTS idx_productos_codigo      ON productos(codigo);
CREATE INDEX IF NOT EXISTS idx_ventas_fecha          ON ventas_historicas(fecha);
CREATE INDEX IF NOT EXISTS idx_ventas_producto       ON ventas_historicas(producto);
CREATE INDEX IF NOT EXISTS idx_ventas_rubro          ON ventas_historicas(rubro);
CREATE INDEX IF NOT EXISTS idx_comprobantes_fecha    ON comprobantes(fecha);
CREATE INDEX IF NOT EXISTS idx_comprobantes_cliente  ON comprobantes(cliente_id);

-- CONVERSACIONES DE EVA (log de lo que habla con los clientes)
CREATE TABLE IF NOT EXISTS conversaciones_eva (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    session         TEXT,
    telefono        TEXT,
    mensaje         TEXT,           -- lo que dijo el cliente
    respuesta       TEXT,           -- lo que respondió Eva
    es_audio        INTEGER DEFAULT 0,
    creado_en       TEXT DEFAULT (datetime('now', 'localtime'))
);

-- ÍNDICES (rendimiento con miles de clientes y ventas)
CREATE INDEX IF NOT EXISTS idx_vh_cliente  ON ventas_historicas(cliente);
CREATE INDEX IF NOT EXISTS idx_vh_producto ON ventas_historicas(producto);
CREATE INDEX IF NOT EXISTS idx_comp_cli    ON comprobantes(cliente_id);
CREATE INDEX IF NOT EXISTS idx_comp_origen ON comprobantes(origen);
CREATE INDEX IF NOT EXISTS idx_items_comp  ON comprobante_items(comprobante_id);
CREATE INDEX IF NOT EXISTS idx_cli_tel     ON clientes(telefono);
CREATE INDEX IF NOT EXISTS idx_conv_tel    ON conversaciones_eva(telefono);
