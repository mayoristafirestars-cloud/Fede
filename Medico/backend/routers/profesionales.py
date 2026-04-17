from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
import sys, os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db.database import conectar

router = APIRouter(prefix="/api/profesionales", tags=["profesionales"])


class ProfesionalIn(BaseModel):
    tipo: str = Field(pattern="^(medico|nutricionista)$")
    nombre: str
    apellido: str
    matricula: str
    dni: Optional[str] = None
    especialidad: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[str] = None
    direccion: Optional[str] = None


@router.get("")
def listar(tipo: Optional[str] = None, buscar: Optional[str] = None, limit: int = 100):
    conn = conectar()
    try:
        query  = "SELECT * FROM profesionales WHERE activo = 1"
        params = []
        if tipo:
            query += " AND tipo = ?"; params.append(tipo)
        if buscar:
            query += " AND (nombre LIKE ? OR apellido LIKE ? OR matricula LIKE ?)"
            params += [f"%{buscar}%", f"%{buscar}%", f"%{buscar}%"]
        query += " ORDER BY apellido, nombre LIMIT ?"
        params.append(limit)
        return [dict(f) for f in conn.execute(query, params).fetchall()]
    finally:
        conn.close()


@router.get("/{prof_id}")
def obtener(prof_id: int):
    conn = conectar()
    try:
        row = conn.execute("SELECT * FROM profesionales WHERE id = ?", (prof_id,)).fetchone()
        if not row:
            raise HTTPException(404, "No encontrado")
        return dict(row)
    finally:
        conn.close()


@router.post("", status_code=201)
def crear(p: ProfesionalIn):
    conn = conectar()
    try:
        cur = conn.execute(
            """INSERT INTO profesionales
               (tipo, nombre, apellido, dni, matricula, especialidad, telefono, email, direccion)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (p.tipo, p.nombre, p.apellido, p.dni, p.matricula,
             p.especialidad, p.telefono, p.email, p.direccion),
        )
        conn.commit()
        return {"id": cur.lastrowid, **p.model_dump()}
    except Exception as e:
        if "UNIQUE" in str(e):
            raise HTTPException(409, "Matrícula ya registrada")
        raise HTTPException(400, str(e))
    finally:
        conn.close()


@router.put("/{prof_id}")
def actualizar(prof_id: int, p: ProfesionalIn):
    conn = conectar()
    try:
        cur = conn.execute(
            """UPDATE profesionales SET
               tipo=?, nombre=?, apellido=?, dni=?, matricula=?,
               especialidad=?, telefono=?, email=?, direccion=?,
               actualizado_en=datetime('now','localtime')
               WHERE id = ?""",
            (p.tipo, p.nombre, p.apellido, p.dni, p.matricula,
             p.especialidad, p.telefono, p.email, p.direccion, prof_id),
        )
        conn.commit()
        if cur.rowcount == 0:
            raise HTTPException(404, "No encontrado")
        return {"id": prof_id, **p.model_dump()}
    finally:
        conn.close()


@router.delete("/{prof_id}")
def eliminar(prof_id: int):
    conn = conectar()
    try:
        cur = conn.execute("UPDATE profesionales SET activo = 0 WHERE id = ?", (prof_id,))
        conn.commit()
        if cur.rowcount == 0:
            raise HTTPException(404, "No encontrado")
        return {"ok": True}
    finally:
        conn.close()
