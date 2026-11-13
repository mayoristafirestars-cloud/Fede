-- 0002: empresa. Todas las tablas nuevas llevan empresa_id.
-- Por ahora hay una sola empresa: Coronel Sur (id 1).
CREATE TABLE IF NOT EXISTS empresa (
    id            INTEGER PRIMARY KEY,
    razon_social  TEXT NOT NULL,
    cuit          TEXT,
    moneda_base   TEXT NOT NULL DEFAULT 'ARS',
    activa        INTEGER NOT NULL DEFAULT 1,
    creado_en     TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
);

INSERT OR IGNORE INTO empresa (id, razon_social) VALUES (1, 'Coronel Sur');
