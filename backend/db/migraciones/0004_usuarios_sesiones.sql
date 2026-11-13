-- 0004: usuarios, roles y sesiones.
CREATE TABLE IF NOT EXISTS rol (
    id           INTEGER PRIMARY KEY,
    codigo       TEXT NOT NULL UNIQUE,
    descripcion  TEXT NOT NULL
);

INSERT OR IGNORE INTO rol (codigo, descripcion) VALUES
    ('admin', 'Administrador'),
    ('responsable_cobranza', 'Responsable de cobranza'),
    ('cobrador', 'Cobrador'),
    ('consulta', 'Solo consulta');

CREATE TABLE IF NOT EXISTS usuario (
    id                 INTEGER PRIMARY KEY,
    empresa_id         INTEGER NOT NULL REFERENCES empresa(id),
    usuario            TEXT    NOT NULL UNIQUE,
    nombre             TEXT    NOT NULL,
    hash_contrasena    TEXT    NOT NULL,
    activo             INTEGER NOT NULL DEFAULT 1,
    intentos_fallidos  INTEGER NOT NULL DEFAULT 0,
    bloqueado_hasta    TEXT,
    ultimo_acceso      TEXT,
    creado_en          TEXT    NOT NULL DEFAULT (datetime('now', 'localtime')),
    actualizado_en     TEXT
);

CREATE TABLE IF NOT EXISTS usuario_rol (
    usuario_id  INTEGER NOT NULL REFERENCES usuario(id),
    rol_id      INTEGER NOT NULL REFERENCES rol(id),
    PRIMARY KEY (usuario_id, rol_id)
);

-- El token de sesión no se guarda: sólo su HMAC con SECRET_KEY.
CREATE TABLE IF NOT EXISTS sesion (
    token_hmac  TEXT    PRIMARY KEY,
    usuario_id  INTEGER NOT NULL REFERENCES usuario(id),
    empresa_id  INTEGER NOT NULL REFERENCES empresa(id),
    csrf        TEXT    NOT NULL,
    creada_en   TEXT    NOT NULL,
    expira_en   TEXT    NOT NULL,
    ip          TEXT,
    revocada    INTEGER NOT NULL DEFAULT 0
);

CREATE INDEX IF NOT EXISTS idx_sesion_usuario ON sesion(usuario_id);
