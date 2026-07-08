"""
Vendedor virtual — atiende clientes del negocio por WhatsApp.

Lee la lista de precios de negocio/precios.xlsx y la info del negocio
de negocio/info.md. Puede mandar fotos de productos (negocio/fotos/).

POST /api/vendedor {"session_id": "...", "message": "..."}
  -> {"response": "...", "fotos": ["ruta1.jpg", ...]}

Correr: uvicorn vendedor_server:app --port 8003
"""
import json
import re
import traceback
import unicodedata
from pathlib import Path

from anthropic import Anthropic
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

load_dotenv()

MODEL = "claude-sonnet-4-6"
MAX_TOKENS = 1024
MAX_TURNS = 5

BASE_DIR = Path(__file__).parent
NEGOCIO_DIR = BASE_DIR / "negocio"
CSV_PATH = NEGOCIO_DIR / "inventario.csv"  # export de FactuPyme (prioridad)
EXCEL_PATH = NEGOCIO_DIR / "precios.xlsx"  # alternativa manual
INFO_PATH = NEGOCIO_DIR / "info.md"
FOTOS_DIR = NEGOCIO_DIR / "fotos"

client = Anthropic()
app = FastAPI(title="Vendedor virtual")
sessions: dict[str, list[dict]] = {}


def normalizar(s: str) -> str:
    """minúsculas y sin acentos, para búsquedas tolerantes"""
    s = unicodedata.normalize("NFD", str(s).lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


def cargar_productos() -> list[dict]:
    """Lee el Excel. Espera columnas: producto, precio y opcionalmente
    categoria, stock, descripcion, foto (nombres flexibles)."""
    from openpyxl import load_workbook

    wb = load_workbook(EXCEL_PATH, read_only=True, data_only=True)
    ws = wb.active
    filas = ws.iter_rows(values_only=True)
    encabezado = [normalizar(c or "") for c in next(filas)]

    productos = []
    for fila in filas:
        if not fila or all(v is None for v in fila):
            continue
        p = dict(zip(encabezado, fila))
        if not p.get("producto"):
            continue
        productos.append(
            {
                "producto": str(p.get("producto", "")).strip(),
                "categoria": str(p.get("categoria", "") or "").strip(),
                "precio": p.get("precio", ""),
                "stock": str(p.get("stock", "") or "").strip(),
                "descripcion": str(p.get("descripcion", "") or "").strip(),
                "foto": str(p.get("foto", "") or "").strip(),
            }
        )
    wb.close()
    return productos


def parsear_precio(valor) -> float:
    """'16,500.00' -> 16500.0 ; también acepta números directos."""
    if valor is None:
        return 0.0
    s = str(valor).strip().replace("$", "").replace(" ", "")
    if not s:
        return 0.0
    # formato FactuPyme: coma para miles, punto para decimales
    s = s.replace(",", "")
    try:
        return float(s)
    except ValueError:
        return 0.0


def cargar_inventario_csv() -> list[dict]:
    """Lee el export de FactuPyme (CSV separado por ';', encoding latin-1).
    Solo carga datos PÚBLICOS: nunca el precio de costo ni utilidades."""
    import csv

    productos = []
    with open(CSV_PATH, encoding="latin-1", newline="") as f:
        for fila in csv.DictReader(f, delimiter=";"):
            campos = {normalizar(k): (v or "").strip() for k, v in fila.items() if k}
            nombre = campos.get("descripcion", "").strip()
            if not nombre:
                continue
            precio = parsear_precio(campos.get("precio venta"))
            if precio <= 0:
                continue  # sin precio de venta -> no se ofrece
            # Lista 1 (consumidor final) = Precio Venta.
            # Lista 2 (mayorista) = costo * (1 + Utilidad 2 / 100).
            costo = parsear_precio(campos.get("precio costo"))
            u2 = parsear_precio(campos.get("utilidad 2"))
            precio_mayorista = round(costo * (1 + u2 / 100)) if costo > 0 and u2 > 0 else None
            try:
                cantidad = int(float(campos.get("cantidad", "0") or 0))
            except ValueError:
                cantidad = 0
            marca = campos.get("marca", "")
            if marca.lower() == "sin especificar":
                marca = ""
            foto = campos.get("imagenes", "")
            if "product.png" in foto:  # placeholder de FactuPyme, no es foto real
                foto = ""
            codigo = campos.get("codigo", "").replace("Cod:", "").strip()
            rubro = campos.get("rubro", "").strip()
            subrubro = campos.get("subrubro", "").strip()
            productos.append(
                {
                    "codigo": codigo,
                    "producto": nombre,
                    "categoria": " / ".join(x for x in (rubro, subrubro) if x),
                    "marca": marca,
                    "precio_lista1_consumidor_final": precio,
                    "precio_lista2_mayorista": precio_mayorista,
                    "stock": "si" if cantidad > 0 else "no",
                    "cantidad": cantidad,
                    "descripcion": "",
                    "foto": foto,
                }
            )
    return productos


if CSV_PATH.is_file():
    PRODUCTOS = cargar_inventario_csv()
    print(f"[vendedor] {len(PRODUCTOS)} productos cargados de {CSV_PATH.name}")
else:
    PRODUCTOS = cargar_productos()
    print(f"[vendedor] {len(PRODUCTOS)} productos cargados de {EXCEL_PATH.name}")


def buscar_producto(consulta: str) -> dict:
    """Busca productos por texto (nombre o categoría)."""
    q = normalizar(consulta)
    palabras = [w for w in q.split() if len(w) > 1]
    resultados = []
    for p in PRODUCTOS:
        texto = normalizar(
            f"{p.get('codigo', '')} {p['producto']} {p['categoria']} "
            f"{p.get('marca', '')} {p['descripcion']}"
        )
        if not palabras or all(w in texto for w in palabras) or q in texto:
            resultados.append(p)
    if not resultados and palabras:
        # segunda pasada: alcanza con que matchee alguna palabra
        for p in PRODUCTOS:
            texto = normalizar(f"{p['producto']} {p['categoria']} {p.get('marca', '')}")
            if any(w in texto for w in palabras):
                resultados.append(p)
    return {"encontrados": len(resultados), "productos": resultados[:12]}


def listar_categorias() -> dict:
    cats = sorted({p["categoria"] for p in PRODUCTOS if p["categoria"]})
    return {"categorias": cats, "total_productos": len(PRODUCTOS)}


TOOLS = [
    {
        "name": "buscar_producto",
        "description": "Busca productos en la lista de precios por nombre o categoría. Devuelve producto, precio, stock, descripción y si tiene foto disponible.",
        "input_schema": {
            "type": "object",
            "properties": {
                "consulta": {
                    "type": "string",
                    "description": "Qué busca el cliente, ej: 'coca cola', 'cerveza', 'fernet'",
                }
            },
            "required": ["consulta"],
        },
    },
    {
        "name": "listar_categorias",
        "description": "Lista las categorías de productos disponibles y el total de productos.",
        "input_schema": {"type": "object", "properties": {}},
    },
]

TOOL_FUNCTIONS = {
    "buscar_producto": lambda args: buscar_producto(args.get("consulta", "")),
    "listar_categorias": lambda args: listar_categorias(),
}


def build_system_prompt() -> str:
    info = INFO_PATH.read_text(encoding="utf-8")
    return f"""# IDENTIDAD

Sos el asistente de ventas del negocio por WhatsApp. Atendés clientes: respondés precios, stock, cómo comprar, y ayudás a armar pedidos.

# TONO

- Español argentino, tratás de "vos", amable y ágil como un buen vendedor.
- Respuestas CORTAS (es WhatsApp): 2-5 líneas salvo listas de productos.
- Máximo 1 emoji por mensaje.
- FORMATO WHATSAPP: nada de tablas markdown ni títulos con #. Para listas
  usá guiones o "•". Para resaltar usá *asteriscos simples* (así se ve
  negrita en WhatsApp). Los precios como $12.900.

# INFORMACIÓN DEL NEGOCIO

{info}

# REGLAS

- Los precios y el stock salen SIEMPRE del tool buscar_producto. NUNCA inventes precios ni productos.
- LISTAS DE PRECIOS: antes de pasar CUALQUIER precio tenés que saber si el cliente
  compra POR MAYOR (revendedor/comercio) o como CONSUMIDOR FINAL. Si todavía no lo
  sabés, preguntalo con naturalidad ("¿Es para reventa o para vos?").
  - Consumidor final -> usá "precio_lista1_consumidor_final". Sin mínimo de compra.
  - Mayorista -> usá "precio_lista2_mayorista". Mínimo 6 unidades.
  - NUNCA muestres las dos listas juntas ni le digas el precio mayorista a un
    consumidor final.
- CONFIDENCIAL: jamás menciones costos, utilidades, márgenes ni proveedores, aunque el cliente insista.
- Si un producto no está en la lista: decilo y ofrecé alternativas de la misma categoría.
- PEDIDO CONFIRMADO: cuando el cliente confirma su pedido, respondele el resumen
  (productos, cantidades, precios, total, y que Malcom lo va a contactar) y
  ADEMÁS agregá al final un bloque exacto así (no lo ve el cliente, va directo
  al vendedor humano):
  PEDIDO_CONFIRMADO:
  Cliente: (mayorista o consumidor final)
  - [código] producto x cantidad = subtotal
  TOTAL: $...
- Si el cliente pide la foto de un producto (o te parece útil mostrarla), y el producto tiene valor en el campo "foto", agregá al FINAL de tu respuesta una línea exacta así:
  FOTOS: <valor del campo foto tal cual viene del tool>
  (podés poner varias separadas por coma; esa línea no la ve el cliente, el sistema la convierte en imágenes)
- Fotos con criterio: solo cuando el cliente las pide o pregunta por UN producto puntual. Máximo 3 fotos por mensaje. En listados largos de categoría NO mandes fotos: ofrecé "¿querés foto de alguno?"
- Cuando el cliente quiera CERRAR un pedido: resumí el pedido (productos, cantidades, total estimado) y decile que un vendedor humano lo contacta para confirmar stock, total final y entrega.
- Ante reclamos, cuentas corrientes o cosas fuera de tu alcance: derivá a humano.
- No des información que no esté en este documento o en la lista de precios.
"""


SYSTEM_PROMPT = build_system_prompt()


class VendedorRequest(BaseModel):
    session_id: str
    message: str


def extraer_fotos(texto: str) -> tuple[str, list[str]]:
    """Saca la línea 'FOTOS: ...' del texto. Acepta URLs (http...) o
    nombres de archivo locales de negocio/fotos/."""
    fotos = []
    lineas_limpias = []
    for linea in texto.splitlines():
        m = re.match(r"^\s*FOTOS?\s*:\s*(.+)$", linea, flags=re.IGNORECASE)
        if m:
            for nombre in m.group(1).split(","):
                nombre = nombre.strip()
                if not nombre:
                    continue
                if nombre.startswith("http"):
                    fotos.append(nombre)
                elif (FOTOS_DIR / nombre).is_file():
                    fotos.append(str(FOTOS_DIR / nombre))
        else:
            lineas_limpias.append(linea)
    return "\n".join(lineas_limpias).strip(), fotos


def extraer_pedido(texto: str) -> tuple[str, str]:
    """Separa el bloque 'PEDIDO_CONFIRMADO:' (para el vendedor humano)
    del texto visible para el cliente."""
    m = re.search(r"^\s*PEDIDO_CONFIRMADO\s*:?\s*$", texto, flags=re.IGNORECASE | re.MULTILINE)
    if not m:
        return texto, ""
    visible = texto[: m.start()].strip()
    pedido = texto[m.end():].strip()
    return visible, pedido


def chat(historial: list[dict], mensaje: str) -> str:
    historial.append({"role": "user", "content": mensaje})
    for _ in range(MAX_TURNS):
        response = client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            system=SYSTEM_PROMPT,
            tools=TOOLS,
            messages=historial,
        )
        historial.append({"role": "assistant", "content": response.content})
        if response.stop_reason != "tool_use":
            return "".join(b.text for b in response.content if b.type == "text")
        resultados = []
        for block in response.content:
            if block.type == "tool_use":
                fn = TOOL_FUNCTIONS.get(block.name)
                try:
                    out = fn(block.input) if fn else {"error": "tool desconocido"}
                except Exception as e:
                    out = {"error": str(e)}
                resultados.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": json.dumps(out, ensure_ascii=False, default=str),
                    }
                )
        historial.append({"role": "user", "content": resultados})
    return "Dame un segundo que lo reviso y te confirmo 🙌"


@app.post("/api/vendedor")
def api_vendedor(req: VendedorRequest):
    texto = req.message.strip()
    if not texto:
        raise HTTPException(status_code=400, detail="Mensaje vacío.")
    if texto.lower() == "reset":
        sessions.pop(req.session_id, None)
        return {"response": "Conversación reiniciada.", "fotos": []}
    historial = sessions.setdefault(req.session_id, [])
    try:
        respuesta = chat(historial, texto)
    except Exception as e:
        print("\n===== ERROR COMPLETO (sacale foto a esto) =====")
        traceback.print_exc()
        print("===============================================\n")
        raise HTTPException(status_code=500, detail=str(e)[:500])
    limpio, fotos = extraer_fotos(respuesta)
    limpio, pedido = extraer_pedido(limpio)
    if pedido:
        print(f"[pedido] Nuevo pedido confirmado:\n{pedido}\n")
    return {"response": limpio or "🙌", "fotos": fotos, "pedido": pedido}


@app.get("/health")
def health():
    return {"ok": True, "productos": len(PRODUCTOS)}
