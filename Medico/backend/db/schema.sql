-- ============================================================
-- MÉDICO — Base de datos principal
-- ============================================================

-- PROFESIONALES (médicos y nutricionistas)
CREATE TABLE IF NOT EXISTS profesionales (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo            TEXT NOT NULL CHECK (tipo IN ('medico', 'nutricionista')),
    nombre          TEXT NOT NULL,
    apellido        TEXT NOT NULL,
    dni             TEXT,
    matricula       TEXT UNIQUE NOT NULL,
    especialidad    TEXT,
    telefono        TEXT,
    email           TEXT,
    direccion       TEXT,
    activo          INTEGER DEFAULT 1,
    creado_en       TEXT DEFAULT (datetime('now', 'localtime')),
    actualizado_en  TEXT DEFAULT (datetime('now', 'localtime'))
);

-- PACIENTES
CREATE TABLE IF NOT EXISTS pacientes (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre          TEXT NOT NULL,
    apellido        TEXT NOT NULL,
    dni             TEXT UNIQUE,
    fecha_nacimiento TEXT,
    telefono        TEXT,
    email           TEXT,
    obra_social     TEXT,
    creado_en       TEXT DEFAULT (datetime('now', 'localtime'))
);

-- CONSULTAS / TURNOS
CREATE TABLE IF NOT EXISTS consultas (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    profesional_id  INTEGER NOT NULL REFERENCES profesionales(id),
    paciente_id     INTEGER REFERENCES pacientes(id),
    fecha           TEXT NOT NULL,
    motivo          TEXT,
    diagnostico     TEXT,
    indicaciones    TEXT,
    estado          TEXT DEFAULT 'programada', -- programada | realizada | cancelada
    creado_en       TEXT DEFAULT (datetime('now', 'localtime'))
);

CREATE INDEX IF NOT EXISTS idx_prof_tipo       ON profesionales(tipo);
CREATE INDEX IF NOT EXISTS idx_prof_matricula  ON profesionales(matricula);
CREATE INDEX IF NOT EXISTS idx_pac_dni         ON pacientes(dni);
CREATE INDEX IF NOT EXISTS idx_consultas_fecha ON consultas(fecha);
CREATE INDEX IF NOT EXISTS idx_consultas_prof  ON consultas(profesional_id);
