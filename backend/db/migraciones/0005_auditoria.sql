-- 0005: auditoría. Sólo se agregan filas: los triggers impiden modificar o borrar.
CREATE TABLE IF NOT EXISTS evento_auditoria (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    empresa_id        INTEGER REFERENCES empresa(id),   -- NULL en eventos del sistema (migraciones)
    actor_usuario_id  INTEGER REFERENCES usuario(id),
    actor_texto       TEXT,                             -- usuario, 'sistema' o 'consola'
    accion            TEXT NOT NULL,
    entidad           TEXT,
    entidad_id        TEXT,
    antes             TEXT,                             -- JSON
    despues           TEXT,                             -- JSON
    ip                TEXT,
    momento           TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
);

CREATE INDEX IF NOT EXISTS idx_auditoria_empresa_momento ON evento_auditoria(empresa_id, momento);
CREATE INDEX IF NOT EXISTS idx_auditoria_accion ON evento_auditoria(accion);

CREATE TRIGGER IF NOT EXISTS evento_auditoria_sin_modificar
BEFORE UPDATE ON evento_auditoria
BEGIN
    SELECT RAISE(ABORT, 'La auditoría no se puede modificar');
END;

CREATE TRIGGER IF NOT EXISTS evento_auditoria_sin_borrar
BEFORE DELETE ON evento_auditoria
BEGIN
    SELECT RAISE(ABORT, 'La auditoría no se puede borrar');
END;
