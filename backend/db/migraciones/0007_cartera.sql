-- 0007: cartera de cuentas corrientes (Hito 1).
-- Importes en centavos enteros. "Vencido" y "parcialmente cancelado" no se guardan: se calculan.

-- Clientes: datos para cuenta corriente.
ALTER TABLE clientes ADD COLUMN empresa_id INTEGER NOT NULL DEFAULT 1;   -- (SQLite no admite REFERENCES con DEFAULT en ALTER)
ALTER TABLE clientes ADD COLUMN cuit TEXT;
ALTER TABLE clientes ADD COLUMN cuenta_corriente INTEGER NOT NULL DEFAULT 0;
ALTER TABLE clientes ADD COLUMN condicion_pago_dias INTEGER;          -- NULL = la condición por defecto
ALTER TABLE clientes ADD COLUMN limite_informativo_centavos INTEGER;  -- sólo informativo, no bloquea
ALTER TABLE clientes ADD COLUMN cliente_origen_id TEXT;               -- identificador en el sistema de origen

CREATE UNIQUE INDEX IF NOT EXISTS ux_clientes_empresa_cuit ON clientes(empresa_id, cuit) WHERE cuit IS NOT NULL;

-- Contactos: sin consentimiento registrado no se usan para mensajes.
CREATE TABLE IF NOT EXISTS contacto_autorizado (
    id                     INTEGER PRIMARY KEY,
    empresa_id             INTEGER NOT NULL REFERENCES empresa(id),
    cliente_id             INTEGER NOT NULL REFERENCES clientes(id),
    nombre                 TEXT,
    telefono_e164          TEXT,
    email                  TEXT,
    canal                  TEXT NOT NULL DEFAULT 'whatsapp',
    consentimiento_fecha   TEXT,
    consentimiento_fuente  TEXT,
    baja_fecha             TEXT,
    creado_en              TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
    UNIQUE (empresa_id, cliente_id, telefono_e164)
);

-- Lotes de importación: vista previa → confirmado → (revertido).
CREATE TABLE IF NOT EXISTS lote_importacion (
    id                     INTEGER PRIMARY KEY,
    empresa_id             INTEGER NOT NULL REFERENCES empresa(id),
    formato                TEXT NOT NULL,              -- saldo_inicial | arca_emitidos
    archivo                TEXT NOT NULL,
    hash_sha256            TEXT NOT NULL,
    filas_totales          INTEGER NOT NULL DEFAULT 0,
    filas_ok               INTEGER NOT NULL DEFAULT 0,
    filas_error            INTEGER NOT NULL DEFAULT 0,
    filas_omitidas         INTEGER NOT NULL DEFAULT 0,
    errores                TEXT,                        -- JSON
    filas                  TEXT,                        -- JSON de filas válidas (para confirmar)
    total_archivo_centavos INTEGER,
    total_informado_centavos INTEGER,
    excepciones            TEXT,                        -- JSON: diferencias aceptadas y motivo
    fecha_corte            TEXT,                        -- saldo inicial: fecha del saldo
    estado                 TEXT NOT NULL DEFAULT 'vista_previa',
    importado_por          INTEGER REFERENCES usuario(id),
    creado_en              TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
    confirmado_en          TEXT,
    confirmado_por         INTEGER REFERENCES usuario(id),
    revertido_en           TEXT,
    revertido_por          INTEGER REFERENCES usuario(id)
);

-- Documentos comerciales: FC factura, ND nota de débito, NC nota de crédito, SI saldo inicial.
CREATE TABLE IF NOT EXISTS documento_comercial (
    id                 INTEGER PRIMARY KEY,
    empresa_id         INTEGER NOT NULL REFERENCES empresa(id),
    cliente_id         INTEGER NOT NULL REFERENCES clientes(id),
    tipo               TEXT NOT NULL CHECK (tipo IN ('FC', 'ND', 'NC', 'SI')),
    letra              TEXT,
    punto_venta        INTEGER,
    numero             INTEGER,
    fecha_emision      TEXT NOT NULL,
    fecha_vencimiento  TEXT NOT NULL,
    importe_centavos   INTEGER NOT NULL CHECK (importe_centavos > 0),
    moneda             TEXT NOT NULL DEFAULT 'ARS',
    estado             TEXT NOT NULL DEFAULT 'emitido' CHECK (estado IN ('emitido', 'anulado')),
    fuente             TEXT NOT NULL,
    id_externo         TEXT NOT NULL,
    lote_id            INTEGER REFERENCES lote_importacion(id),
    creado_en          TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
    UNIQUE (empresa_id, fuente, id_externo)
);

CREATE INDEX IF NOT EXISTS idx_documento_cliente ON documento_comercial(empresa_id, cliente_id);

-- Ajustes: corrección manual con motivo. Nunca se borran: se revierten con otro ajuste.
CREATE TABLE IF NOT EXISTS ajuste (
    id                 INTEGER PRIMARY KEY,
    empresa_id         INTEGER NOT NULL REFERENCES empresa(id),
    cliente_id         INTEGER NOT NULL REFERENCES clientes(id),
    documento_id       INTEGER REFERENCES documento_comercial(id),   -- si cancela parte de un documento
    sentido            TEXT NOT NULL CHECK (sentido IN ('debito', 'credito')),
    importe_centavos   INTEGER NOT NULL CHECK (importe_centavos > 0),
    motivo             TEXT NOT NULL,
    evidencia          TEXT,
    aprobado_por       INTEGER NOT NULL REFERENCES usuario(id),
    revierte_a         INTEGER REFERENCES ajuste(id),
    creado_en          TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
);

CREATE UNIQUE INDEX IF NOT EXISTS ux_ajuste_revierte ON ajuste(revierte_a) WHERE revierte_a IS NOT NULL;

-- Aplicaciones: un crédito (NC o ajuste crédito) que cancela parte de un documento deudor.
CREATE TABLE IF NOT EXISTS aplicacion (
    id                 INTEGER PRIMARY KEY,
    empresa_id         INTEGER NOT NULL REFERENCES empresa(id),
    documento_id       INTEGER NOT NULL REFERENCES documento_comercial(id),   -- FC, ND o SI
    origen_tipo        TEXT NOT NULL CHECK (origen_tipo IN ('nota_credito', 'ajuste')),
    origen_id          INTEGER NOT NULL,
    importe_centavos   INTEGER NOT NULL CHECK (importe_centavos <> 0),       -- negativo = reverso
    fecha              TEXT NOT NULL,
    aprobado_por       INTEGER NOT NULL REFERENCES usuario(id),
    revierte_a         INTEGER REFERENCES aplicacion(id),
    creado_en          TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
);

CREATE INDEX IF NOT EXISTS idx_aplicacion_documento ON aplicacion(documento_id);
