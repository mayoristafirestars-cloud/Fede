-- 0003: numeración de comprobantes con secuencia (reemplaza COUNT(*)).
-- Arranca desde el número más alto que ya existe para cada tipo.
CREATE TABLE IF NOT EXISTS secuencias (
    empresa_id  INTEGER NOT NULL REFERENCES empresa(id),
    tipo        TEXT    NOT NULL,
    ultimo      INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (empresa_id, tipo)
);

INSERT OR IGNORE INTO secuencias (empresa_id, tipo, ultimo)
SELECT 1, 'factura', COALESCE(MAX(CAST(substr(numero, 3) AS INTEGER)), 0)
FROM comprobantes WHERE tipo = 'factura' AND numero LIKE 'F-%';

INSERT OR IGNORE INTO secuencias (empresa_id, tipo, ultimo)
SELECT 1, 'presupuesto', COALESCE(MAX(CAST(substr(numero, 3) AS INTEGER)), 0)
FROM comprobantes WHERE tipo = 'presupuesto' AND numero LIKE 'P-%';
