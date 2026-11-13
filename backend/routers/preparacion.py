"""Business discovery and product catalog, roadmap points 1–10."""
import io
import json
import os
import sqlite3
import unicodedata
import uuid
from contextlib import contextmanager
from pathlib import Path
from typing import Literal

from fastapi import APIRouter, File, HTTPException, Query, UploadFile
from PIL import Image, UnidentifiedImageError
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from db.database import conectar

router = APIRouter(prefix="/api/gestion", tags=["Negocio y catálogo"])
MEDIA_DIR = os.environ.get("CORONEL_MEDIA_DIR", str(Path(__file__).resolve().parents[1] / "uploads"))
UNIDADES = [
    {"codigo": "kg", "nombre": "Kilogramo", "fraccionable": True},
    {"codigo": "g", "nombre": "Gramo", "fraccionable": True},
    {"codigo": "unidad", "nombre": "Unidad", "fraccionable": False},
    {"codigo": "atado", "nombre": "Atado", "fraccionable": False},
    {"codigo": "bolsa", "nombre": "Bolsa", "fraccionable": False},
    {"codigo": "bandeja", "nombre": "Bandeja", "fraccionable": False},
    {"codigo": "cajon", "nombre": "Cajón", "fraccionable": False},
]
Unit = Literal["kg", "g", "unidad", "atado", "bolsa", "bandeja", "cajon"]
Pay = Literal["efectivo", "transferencia", "qr", "debito", "credito"]

@contextmanager
def database():
    conn = conectar()
    try:
        with conn:
            yield conn
    finally:
        conn.close()

class Model(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

class Persona(Model):
    nombre: str = Field(min_length=1, max_length=100)
    rol: Literal["dueno", "encargado", "cajero"]

class Equipo(Model):
    tipo: Literal["computadora", "tablet", "balanza", "lector", "impresora"]
    marca_modelo: str = Field(default="", max_length=150)
    conexion: Literal["pendiente", "usb", "serie", "red", "bluetooth", "otra"] = "pendiente"
    estado: Literal["pendiente", "disponible", "por_comprar"] = "pendiente"
    notas: str = Field(default="",max_length=300)

class Negocio(Model):
    nombre: str = Field(default="", max_length=120)
    localidad: str = Field(default="", max_length=120)
    atencion: Literal["pendiente", "mostrador", "autoservicio", "mixta"] = "pendiente"
    pesaje: Literal["pendiente", "antes_de_caja", "en_caja"] = "pendiente"
    cobro: Literal["pendiente", "misma_persona", "caja_separada"] = "pendiente"
    entrega: Literal["pendiente", "en_local", "retiro_y_reparto"] = "pendiente"
    personas: list[Persona] = Field(default_factory=list, max_length=30)
    funciones_previstas: list[Literal['dueno','encargado','cajero']] = Field(default_factory=list,max_length=3)
    canales_venta: list[Literal['local','whatsapp','retiro','reparto']] = Field(default_factory=list,max_length=4)
    equipos: list[Equipo] = Field(default_factory=list, max_length=30)
    medios_pago: list[Literal['efectivo','transferencia','qr','debito','credito','mercado_pago']] = Field(default_factory=list, max_length=6)
    tiene_contador: Literal['pendiente','si','no'] = 'pendiente'
    contador: str = Field(default="", max_length=150)
    situacion_fiscal: str = Field(default="", max_length=200)
    comprobantes: str = Field(default="", max_length=300)
    fiscal_revisado: bool = False
    internet: Literal["pendiente", "disponible", "estable", "intermitente", "sin_internet"] = "pendiente"
    contingencia: str = Field(default="", max_length=1000)
    notas_local: str = Field(default="",max_length=2000)

    @model_validator(mode="after")
    def unique_and_fiscal(self):
        if len(set(self.medios_pago)) != len(self.medios_pago):
            raise ValueError("No repetir medios de pago")
        for values in (self.funciones_previstas,self.canales_venta):
            if len(set(values))!=len(values):
                raise ValueError('No repetir funciones o canales de venta')
        if self.fiscal_revisado and not all([self.contador, self.situacion_fiscal, self.comprobantes]):
            raise ValueError("Completar contador, situación fiscal y comprobantes antes de marcar revisado")
        return self

def clave(value):
    return "".join(c for c in unicodedata.normalize("NFKD", value.casefold()) if not unicodedata.combining(c))

class Producto(Model):
    codigo: str = Field(min_length=1, max_length=40, pattern=r"^[A-Za-z0-9_-]+$")
    descripcion: str = Field(min_length=1, max_length=160)
    rubro: str = Field(default="Verduras", min_length=1, max_length=80)
    unidad_venta: Unit = "kg"
    variedad: str = Field(default="", max_length=80)
    calidad: str = Field(default="", max_length=80)
    presentacion: str = Field(default="", max_length=80)
    aliases: list[str] = Field(default_factory=list, max_length=15)
    activo: bool = True

    @field_validator("aliases")
    @classmethod
    def valid_aliases(cls, values):
        values = [v.strip() for v in values]
        if any(not v or len(v) > 80 for v in values):
            raise ValueError("Cada nombre alternativo debe tener entre 1 y 80 caracteres")
        keys = [clave(v) for v in values]
        if len(set(keys)) != len(keys):
            raise ValueError("No repetir nombres alternativos")
        return values

    @model_validator(mode="after")
    def distinct_code(self):
        if clave(self.codigo) in [clave(a) for a in self.aliases]:
            raise ValueError("El código y los nombres alternativos deben ser diferentes")
        return self

@router.get("/unidades")
def unidades():
    return UNIDADES

@router.get("/negocio")
def negocio():
    with database() as conn:
        row = conn.execute("SELECT datos FROM configuracion_negocio WHERE id=1").fetchone()
    return Negocio.model_validate(json.loads(row[0])).model_dump() if row else Negocio().model_dump()

@router.put("/negocio")
def guardar_negocio(data: Negocio):
    with database() as conn:
        conn.execute("INSERT INTO configuracion_negocio(id,datos) VALUES(1,?) ON CONFLICT(id) DO UPDATE SET datos=excluded.datos", (data.model_dump_json(),))
    return data.model_dump()

def product_dict(conn, row):
    result = dict(row)
    result["aliases"] = [r[0] for r in conn.execute("SELECT valor FROM identificadores_producto WHERE producto_id=? AND tipo='alias' ORDER BY clave", (row["id"],))]
    return result

@router.get("/productos")
def productos(buscar: str = Query(default="", max_length=160), incluir_inactivos: bool = False):
    # Normalize in Python to search accents consistently across SQLite installations.
    with database() as conn:
        rows = conn.execute("SELECT * FROM productos" + ("" if incluir_inactivos else " WHERE activo=1") + " ORDER BY descripcion,id").fetchall()
        items = [product_dict(conn, row) for row in rows]
    q = clave(buscar.strip())
    return [p for p in items if not q or q in clave(" ".join([p["codigo"], p["descripcion"], p["rubro"] or "", p["variedad"], p["calidad"], p["presentacion"], *p["aliases"]]))]

def save_product(data, product_id=None):
    with database() as conn:
        # Serialize writers before checking identifiers, including pre-migration codes.
        conn.execute("BEGIN IMMEDIATE")
        if product_id is not None:
            previous = conn.execute("SELECT * FROM productos WHERE id=?", (product_id,)).fetchone()
            if not previous:
                raise HTTPException(404, "Producto no encontrado")
            if previous['unidad_venta'] != data.unidad_venta:
                used = previous['stock'] != 0 or previous['precio_venta'] != 0 or previous['precio_costo'] != 0 or conn.execute('SELECT 1 FROM historial_comercial WHERE producto_id=? UNION SELECT 1 FROM pedido_lineas WHERE producto_id=? UNION SELECT 1 FROM lotes_stock WHERE producto_id=?', (product_id,product_id,product_id)).fetchone()
                if used:
                    raise HTTPException(409, "No se puede cambiar la unidad de un producto con stock, precios o compras. Creá otra presentación")
        identifiers = [(clave(data.codigo), "codigo", data.codigo)] + [(clave(a), "alias", a) for a in data.aliases]
        other_codes = {clave(r["codigo"]) for r in conn.execute("SELECT id,codigo FROM productos") if r["id"] != product_id}
        for key, _, _ in identifiers:
            existing = conn.execute("SELECT producto_id FROM identificadores_producto WHERE clave=?", (key,)).fetchone()
            if key in other_codes or (existing and existing[0] != product_id):
                raise HTTPException(409, "El código o un nombre alternativo ya pertenece a otro producto")
        fields = data.model_dump(exclude={"aliases"})
        try:
            if product_id is None:
                cur = conn.execute(f"INSERT INTO productos ({','.join(fields)}) VALUES ({','.join('?' for _ in fields)})", tuple(fields.values()))
                product_id = cur.lastrowid
            else:
                conn.execute(f"UPDATE productos SET {','.join(f'{k}=?' for k in fields)},actualizado_en=datetime('now') WHERE id=?", (*fields.values(), product_id))
                conn.execute("DELETE FROM identificadores_producto WHERE producto_id=?", (product_id,))
            conn.executemany("INSERT INTO identificadores_producto(clave,producto_id,tipo,valor) VALUES(?,?,?,?)", [(key, product_id, kind, value) for key, kind, value in identifiers])
        except sqlite3.IntegrityError:
            raise HTTPException(409, "El código o un nombre alternativo está en uso")
        result = product_dict(conn, conn.execute("SELECT * FROM productos WHERE id=?", (product_id,)).fetchone())
    return result

@router.post("/productos", status_code=201)
def crear_producto(data: Producto):
    return save_product(data)

@router.put("/productos/{product_id}")
def editar_producto(product_id: int, data: Producto):
    return save_product(data, product_id)

@router.post("/productos/{product_id}/foto")
async def foto_producto(product_id: int, archivo: UploadFile = File(...)):
    with database() as conn:
        if not conn.execute("SELECT 1 FROM productos WHERE id=?", (product_id,)).fetchone():
            raise HTTPException(404, "Producto no encontrado")
    raw = await archivo.read(5 * 1024 * 1024 + 1)
    if len(raw) > 5 * 1024 * 1024:
        raise HTTPException(413, "La foto debe pesar hasta 5 MB")
    try:
        with Image.open(io.BytesIO(raw)) as image:
            if image.format not in {"JPEG", "PNG", "WEBP"} or image.width * image.height > 20_000_000:
                raise ValueError()
            image.load()
            image.thumbnail((1000, 1000))
            image = image.convert("RGB")
            out = io.BytesIO()
            image.save(out, format="JPEG", quality=85)
    except (UnidentifiedImageError, OSError, ValueError, Image.DecompressionBombError):
        raise HTTPException(422, "Usar una imagen JPG, PNG o WebP válida de hasta 20 megapíxeles")
    name = f"{uuid.uuid4().hex}.jpg"
    Path(MEDIA_DIR).mkdir(parents=True, exist_ok=True)
    path = Path(MEDIA_DIR) / name
    path.write_bytes(out.getvalue())
    try:
        with database() as conn:
            conn.execute("UPDATE productos SET foto=?,actualizado_en=datetime('now') WHERE id=?", (f"/media/{name}", product_id))
    except Exception:
        path.unlink(missing_ok=True)
        raise
    return {"foto": f"/media/{name}"}
