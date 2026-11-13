"""Pruebas de migraciones versionadas, respaldo y restauración."""

import os
import sqlite3

import pytest


@pytest.fixture
def respaldos_tmp(tmp_path, monkeypatch):
    carpeta = tmp_path / "respaldos"
    monkeypatch.setenv("BACKUP_DIR", str(carpeta))
    return carpeta


def _tablas(ruta):
    conn = sqlite3.connect(ruta)
    nombres = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    conn.close()
    return nombres


def test_base_nueva_aplica_todo_sin_respaldo(db_temporal, respaldos_tmp):
    from db.migrador import aplicar_migraciones, listar_migraciones
    hechas = aplicar_migraciones()
    assert hechas == [v for v, _, _ in listar_migraciones()]
    assert {"productos", "clientes", "comprobantes", "schema_migraciones"} <= _tablas(db_temporal)
    respaldos_db = list(respaldos_tmp.glob("*.db")) if respaldos_tmp.exists() else []
    assert respaldos_db == []                  # base nueva: no hay nada que respaldar


def test_aplicar_dos_veces_no_hace_nada(db_temporal, respaldos_tmp):
    from db.migrador import aplicar_migraciones
    aplicar_migraciones()
    assert aplicar_migraciones() == []


def test_base_existente_se_respalda_y_conserva_datos(db_temporal, respaldos_tmp):
    """Simula la base de producción: creada con el schema.sql viejo, sin control de migraciones."""
    from db.migrador import aplicar_migraciones, DIR_MIGRACIONES
    conn = sqlite3.connect(db_temporal)
    conn.executescript(open(os.path.join(DIR_MIGRACIONES, "0001_esquema_inicial.sql"), encoding="utf-8").read())
    conn.execute("INSERT INTO productos (codigo, descripcion, stock) VALUES ('X1', 'Producto viejo', 3)")
    conn.commit()
    conn.close()

    aplicar_migraciones()

    archivos = [a for a in os.listdir(respaldos_tmp) if a.endswith(".db")]
    assert len(archivos) == 1 and "pre_migracion_0001" in archivos[0]
    conn = sqlite3.connect(db_temporal)
    assert conn.execute("SELECT descripcion FROM productos WHERE codigo='X1'").fetchone()[0] == "Producto viejo"
    assert conn.execute("SELECT COUNT(*) FROM schema_migraciones WHERE version = 1").fetchone()[0] == 1
    conn.close()


def test_migracion_con_error_no_deja_cambios(db_temporal, respaldos_tmp, tmp_path):
    from db.migrador import aplicar_migraciones
    carpeta = tmp_path / "migs"
    carpeta.mkdir()
    (carpeta / "0001_ok.sql").write_text("CREATE TABLE a (id INTEGER);")
    (carpeta / "0002_rota.sql").write_text("CREATE TABLE b (id INTEGER);\nINSERT INTO tabla_que_no_existe VALUES (1);")
    with pytest.raises(sqlite3.OperationalError):
        aplicar_migraciones(directorio=str(carpeta))
    tablas = _tablas(db_temporal)
    assert "a" in tablas and "b" not in tablas            # 0002 se deshizo completa
    conn = sqlite3.connect(db_temporal)
    assert [r[0] for r in conn.execute("SELECT version FROM schema_migraciones")] == [1]
    conn.close()


def test_sentencias_respeta_triggers():
    from db.migrador import _sentencias
    sql = """
    -- comentario
    CREATE TABLE t (id INTEGER);
    CREATE TRIGGER t_no_borrar BEFORE DELETE ON t
    BEGIN
        SELECT RAISE(ABORT, 'no; se borra');
    END;
    """
    partes = _sentencias(sql)
    assert len(partes) == 2
    assert partes[1].startswith("CREATE TRIGGER") and partes[1].endswith("END;")


def test_respaldar_y_restaurar_devuelve_los_mismos_datos(db_temporal, respaldos_tmp):
    from db.migrador import aplicar_migraciones
    from db import respaldos
    aplicar_migraciones()
    conn = sqlite3.connect(db_temporal)
    conn.execute("INSERT INTO productos (codigo, descripcion, stock) VALUES ('A', 'Antes', 5)")
    conn.commit()
    conn.close()

    copia = respaldos.respaldar(motivo="prueba")
    assert respaldos.verificar_integridad(copia)

    conn = sqlite3.connect(db_temporal)
    conn.execute("UPDATE productos SET descripcion = 'Después', stock = 0")
    conn.execute("INSERT INTO productos (codigo, descripcion) VALUES ('B', 'Nuevo')")
    conn.commit()
    conn.close()

    previo = respaldos.restaurar(copia)

    conn = sqlite3.connect(db_temporal)
    filas = conn.execute("SELECT codigo, descripcion, stock FROM productos ORDER BY codigo").fetchall()
    conn.close()
    assert filas == [("A", "Antes", 5)]
    # el estado anterior a restaurar quedó guardado
    conn = sqlite3.connect(previo)
    assert conn.execute("SELECT COUNT(*) FROM productos").fetchone()[0] == 2
    conn.close()


def test_restaurar_archivo_invalido_falla_sin_tocar_la_base(db_temporal, respaldos_tmp, tmp_path):
    from db.migrador import aplicar_migraciones
    from db import respaldos
    aplicar_migraciones()
    basura = tmp_path / "no_es_base.db"
    basura.write_text("esto no es sqlite")
    with pytest.raises(ValueError):
        respaldos.restaurar(str(basura))
    assert "productos" in _tablas(db_temporal)
