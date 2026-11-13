"""Guest storefront, explicit publication, bounded replacements and price consent.
Slotted requests reserve stock; delivery consumes it. No automatic payment or fiscal emission.
"""
import hashlib
import hmac
import json
import time
from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from typing import Annotated, Literal
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, Header, HTTPException, Request
from fastapi.responses import FileResponse
from pydantic import Field, field_validator, model_validator
from routers import preparacion
from routers.preparacion import Model, database, clave
from routers.comercial import authorized
from document_photos import available_photo

router = APIRouter(tags=['Tienda de Nativa'])
Qty = Annotated[Decimal, Field(gt=0, le=9999, max_digits=10, decimal_places=3, allow_inf_nan=False)]
Price = Annotated[Decimal, Field(gt=0, max_digits=14, decimal_places=4, allow_inf_nan=False)]
Secret = Annotated[str, Field(pattern=r'^[A-Za-z0-9_-]{43}$')]
WEIGHED = {'kg', 'g'}


def money(value):
    return format(value.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP), 'f')


def fingerprint(data):
    return json.dumps(data.model_dump(mode='json'), sort_keys=True, separators=(',', ':'))


def secret_hash(value):
    return hashlib.sha256(value.encode()).hexdigest()


def offer(conn, ident, require_visible=True):
    row = conn.execute('SELECT p.*,coalesce(w.visible,0) visible FROM productos p LEFT JOIN publicaciones_web w ON w.producto_id=p.id WHERE p.id=?', (ident,)).fetchone()
    if not row:
        raise HTTPException(404, 'Producto no encontrado')
    row = dict(row)
    price = Decimal(str(row['venta_exacta'] if row['venta_exacta'] is not None else row['precio_venta'] or 0))
    photo = available_photo(row['foto'])
    eligible = bool(row['activo'] and price.is_finite() and price > 0 and photo)
    if require_visible and not (row['visible'] and eligible):
        raise HTTPException(409, 'Este producto ya no está disponible en la tienda. Revisá tu carrito.')
    from routers.tienda_promociones import effective_promotion
    promotion=effective_promotion(conn,row) if eligible else None
    row['promocion_publica']=promotion
    if promotion:price=Decimal(promotion['precio'])
    return row, price, photo, eligible


def public_product(row, price):
    return {'id': row['id'], 'nombre': row['descripcion'], 'categoria': row['rubro'],
            'variedad': row['variedad'], 'presentacion': row['presentacion'],
            'unidad': row['unidad_venta'], 'precio': format(price, 'f'),
            'foto': f'/api/tienda/productos/{row["id"]}/foto',
            'disponibilidad': 'a_confirmar', 'promocion':row.get('promocion_publica')}


@router.get('/api/tienda/catalogo')
def catalog():
    from routers.tienda_operacion import expire, settings, slot_view
    import stock
    with database() as conn:
        expire(conn)
        policy = settings(conn)
        slots = [slot_view(conn,r) for r in conn.execute('SELECT * FROM franjas_web WHERE activa=1 ORDER BY inicio') if datetime.fromisoformat(r['inicio']).timestamp()>time.time()]
        config = conn.execute('SELECT datos FROM configuracion_negocio WHERE id=1').fetchone()
        business = json.loads(config[0]) if config else {}
        products = []
        for entry in conn.execute('SELECT producto_id FROM publicaciones_web WHERE visible=1 ORDER BY producto_id').fetchall():
            row, price, photo, eligible = offer(conn, entry[0], False)
            if eligible:
                item = public_product(row, price)
                tracked = conn.execute('SELECT 1 FROM inventario_productos WHERE producto_id=?',(row['id'],)).fetchone()
                if tracked and abs(stock.physical(conn,row['id'])-Decimal(str(row['stock'])))<Decimal('.000001'):
                    item['disponibilidad'] = 'disponible' if stock.free_web(conn,row['id'])>0 else 'agotado'
                products.append(item)
    products.sort(key=lambda p: clave(p['nombre']))
    return {'negocio': {'nombre': business.get('nombre') or 'Nativa', 'localidad': business.get('localidad') or ''},
            'productos': products, 'moneda': 'ARS', 'franjas': slots, 'tienda': policy.model_dump(),
            'mensaje': 'Confirmamos peso e importe antes de cobrar. Con franja elegida, la mercadería se reserva temporalmente; sin franja es una solicitud a coordinar.'}


@router.get('/api/tienda/productos/{ident}/foto')
def photo(ident: int):
    with database() as conn:
        try:
            row, price, filename, eligible = offer(conn, ident)
        except HTTPException:
            raise HTTPException(404, 'Foto no disponible')
    return FileResponse(Path(preparacion.MEDIA_DIR) / filename.rsplit('/', 1)[1], media_type='image/jpeg', headers={'Cache-Control': 'no-store'})


@router.get('/api/gestion/tienda/productos')
def publications(person=Depends(authorized)):
    with database() as conn:
        result = []
        for item in conn.execute('SELECT id FROM productos ORDER BY descripcion,id').fetchall():
            row, price, photo_path, eligible = offer(conn, item[0], False)
            missing = []
            if not row['activo']: missing.append('producto inactivo')
            if not price.is_finite() or price <= 0: missing.append('precio de venta')
            if not photo_path: missing.append('foto del producto')
            result.append({**public_product(row, price), 'foto': photo_path, 'visible': bool(row['visible']),
                           'publicable': eligible, 'pendientes': missing})
        return result


class Publication(Model):
    visible: bool


@router.put('/api/gestion/tienda/productos/{ident}')
def publish(ident: int, data: Publication, person=Depends(authorized)):
    with database() as conn:
        conn.execute('BEGIN IMMEDIATE')
        row, price, photo_path, eligible = offer(conn, ident, False)
        if data.visible and not eligible:
            raise HTTPException(422, 'Para publicar: producto activo, precio de venta mayor a cero y foto correspondiente cargada.')
        conn.execute('INSERT INTO publicaciones_web VALUES(?,?) ON CONFLICT(producto_id) DO UPDATE SET visible=excluded.visible', (ident, data.visible))
    return {'id': ident, 'visible': data.visible}


class RequestedLine(Model):
    producto_id: int = Field(gt=0)
    cantidad: Qty
    precio_esperado: Price
    unidad: preparacion.Unit
    reemplazo: Literal['no_reemplazar','consultar','alternativa'] = 'consultar'
    alternativa_id: int | None = Field(default=None,gt=0)


class GuestOrder(Model):
    clave_operacion: UUID
    acceso: Secret
    nombre: str = Field(min_length=2, max_length=100)
    telefono: str = Field(min_length=8, max_length=30, pattern=r'^[+0-9 ()-]+$')
    presupuesto: Decimal | None = Field(default=None,gt=0,max_digits=14,decimal_places=2,allow_inf_nan=False)
    franja_id: int | None = Field(default=None,gt=0)
    lineas: list[RequestedLine] = Field(min_length=1, max_length=40)

    @field_validator('telefono')
    @classmethod
    def valid_phone(cls, value):
        if not 8 <= sum(c.isdigit() for c in value) <= 15:
            raise ValueError('Ingresá un teléfono válido, con código de área')
        return value

    @model_validator(mode='after')
    def unique_products(self):
        if len({line.producto_id for line in self.lineas}) != len(self.lineas):
            raise ValueError('Unificá las cantidades de cada producto')
        for line in self.lineas:
            if line.reemplazo=='alternativa' and (not line.alternativa_id or line.alternativa_id==line.producto_id):
                raise ValueError('Elegí un producto alternativo distinto')
            if line.reemplazo!='alternativa' and line.alternativa_id is not None:
                raise ValueError('La alternativa sólo se guarda cuando se elige esa preferencia')
            if line.unidad not in WEIGHED and line.cantidad != line.cantidad.to_integral():
                raise ValueError('Las unidades, atados y presentaciones se piden en números enteros')
        return self


def get_order(conn, ident):
    row = conn.execute('SELECT p.*,f.inicio AS franja_inicio,f.fin AS franja_fin FROM pedidos_web p LEFT JOIN franjas_web f ON f.id=p.franja_id WHERE p.id=?', (str(ident),)).fetchone()
    if not row:
        raise HTTPException(404, 'Solicitud no encontrada')
    return row


def order_view(row, staff=False):
    result = {'id': row['id'], 'nombre': row['nombre'], 'estado': row['estado'], 'version': row['version'],
              'lineas': json.loads(row['lineas']), 'estimado': row['estimado'], 'final': row['final'],
              'preparacion': json.loads(row['preparacion']) if row['preparacion'] else None,
              'creado': row['creado'], 'aprobado_en': row['aprobado_en'],
              'pago': 'verificado_manualmente' if row['cobro'] else 'no_cobrado',
              'presupuesto': row['presupuesto'], 'franja_id': row['franja_id'], 'vence_reserva': row['vence_reserva'],
              'franja': {'inicio':row['franja_inicio'],'fin':row['franja_fin']} if 'franja_inicio' in row.keys() and row['franja_inicio'] else None,
              'reserva': bool(row['vence_reserva'] and row['vence_reserva']>time.time() and row['estado'] not in ('cancelado','vencido','entregado'))}
    if staff:
        result.update(telefono=row['telefono'], responsable=row['responsable'])
    return result


@router.post('/api/tienda/pedidos', status_code=201)
def create_order(data: GuestOrder, request: Request):
    from routers.tienda_operacion import settings, check_slot, reserve, expire
    payload = fingerprint(data)
    digest = hashlib.sha256(payload.encode()).hexdigest()
    with database() as conn:
        conn.execute('BEGIN IMMEDIATE')
        expire(conn)
        previous = conn.execute('SELECT * FROM pedidos_web WHERE clave_operacion=?', (str(data.clave_operacion),)).fetchone()
        if previous:
            compatible = False
            if data.presupuesto is None and data.franja_id is None and all(l.reemplazo=='consultar' for l in data.lineas):
                legacy = data.model_dump(mode='json',exclude={'presupuesto','franja_id'})
                for line in legacy['lineas']:
                    line.pop('reemplazo',None)
                    line.pop('alternativa_id',None)
                compatible = previous['payload']==hashlib.sha256(json.dumps(legacy,sort_keys=True,separators=(',',':')).encode()).hexdigest()
            if previous['payload'] != digest and not compatible:
                raise HTTPException(409, 'La clave de solicitud ya fue usada con otros datos')
            return order_view(get_order(conn,previous['id']))
        policy = settings(conn)
        if not policy.abierta: raise HTTPException(409,'La tienda pausó las solicitudes. Volvé más tarde.')
        if policy.requiere_franja and data.franja_id is None: raise HTTPException(422,'Elegí una franja de retiro disponible')
        slot = check_slot(conn,data.franja_id) if data.franja_id is not None else None
        minute = int(time.time() // 60)
        bucket = secret_hash((request.client.host if request.client else 'unknown') + ':' + str(minute))
        count = conn.execute('SELECT cantidad FROM limites_web WHERE clave=?', (bucket,)).fetchone()
        if count and count[0] >= 10:
            raise HTTPException(429, 'Demasiadas solicitudes. Esperá un minuto antes de volver a intentar.')
        lines = []
        for line in data.lineas:
            row, price, photo_path, eligible = offer(conn, line.producto_id)
            if price != line.precio_esperado or row['unidad_venta'] != line.unidad:
                raise HTTPException(409, 'Cambió un precio o una unidad. Actualizá el catálogo y revisá tu carrito.')
            alternative = None
            if line.alternativa_id is not None:
                alt,alt_price,alt_photo,alt_eligible = offer(conn,line.alternativa_id)
                alternative = {'id':alt['id'],'nombre':alt['descripcion']}
            lines.append({'producto_id': row['id'], 'nombre': row['descripcion'], 'unidad': row['unidad_venta'],
                          'cantidad': format(line.cantidad, 'f'), 'precio': format(price, 'f'),
                          'estimado': money(price * line.cantidad), 'reemplazo': line.reemplazo, 'alternativa': alternative, 'promocion':row.get('promocion_publica')})
        ident = str(uuid4())
        total = money(sum((Decimal(l['estimado']) for l in lines), Decimal(0)))
        if data.presupuesto is not None and Decimal(total)>data.presupuesto:
            raise HTTPException(422,'El estimado supera tu presupuesto máximo. Ajustá las cantidades.')
        deadline = min(time.time()+policy.reserva_minutos*60,datetime.fromisoformat(slot['fin']).timestamp()) if slot else None
        conn.execute('INSERT INTO pedidos_web(id,clave_operacion,acceso_hash,payload,nombre,telefono,lineas,estimado,presupuesto,franja_id,vence_reserva) VALUES(?,?,?,?,?,?,?,?,?,?,?)',
                     (ident, str(data.clave_operacion), secret_hash(data.acceso), digest, data.nombre, data.telefono, json.dumps(lines), total, str(data.presupuesto) if data.presupuesto is not None else None, data.franja_id, deadline))
        reserve(conn,get_order(conn,ident),lines)
        conn.execute('INSERT INTO limites_web VALUES(?,1,?) ON CONFLICT(clave) DO UPDATE SET cantidad=cantidad+1', (bucket, minute))
        conn.execute('DELETE FROM limites_web WHERE minuto<?', (minute - 60,))
        return order_view(get_order(conn, ident))


def customer_order(conn, ident, token):
    from routers.tienda_operacion import expire
    expire(conn)
    row = get_order(conn, ident)
    if not token or not hmac.compare_digest(row['acceso_hash'], secret_hash(token)):
        raise HTTPException(404, 'Solicitud no encontrada o enlace de acceso incorrecto')
    created = datetime.fromisoformat(row['creado'].replace('Z', '+00:00'))
    if (datetime.now(timezone.utc) - created).total_seconds() > 30 * 86400:
        raise HTTPException(410, 'El enlace de esta solicitud venció. Contactá a Nativa para continuar.')
    return row


@router.get('/api/tienda/pedidos/{ident}')
def read_order(ident: UUID, x_pedido_acceso: str | None = Header(default=None, max_length=100)):
    with database() as conn:
        return order_view(customer_order(conn, ident, x_pedido_acceso))


@router.get('/api/gestion/tienda/pedidos')
def order_list(person=Depends(authorized)):
    from routers.tienda_operacion import expire, complaints, profitability, reservation_risk
    with database() as conn:
        expire(conn)
        return [{**order_view(row, True),'reclamos':complaints(conn,row['id']),'rentabilidad':profitability(conn,row),'alerta_reserva':reservation_risk(conn,row)} for row in conn.execute('SELECT p.*,f.inicio AS franja_inicio,f.fin AS franja_fin FROM pedidos_web p LEFT JOIN franjas_web f ON f.id=p.franja_id ORDER BY p.creado DESC LIMIT 200')]


class PreparedLine(Model):
    producto_id: int = Field(gt=0)
    bruto: Qty | None = None
    tara: Decimal = Field(default=Decimal(0), ge=0, le=9999, max_digits=10, decimal_places=3, allow_inf_nan=False)
    cantidad: Qty | None = None
    reemplazo_id: int | None = Field(default=None,gt=0)
    omitir: bool = False


class Preparation(Model):
    version: int = Field(ge=1)
    clave_operacion: UUID
    lineas: list[PreparedLine] = Field(min_length=1, max_length=40)


def prior_action(conn, ident, key, kind, payload):
    previous = conn.execute('SELECT * FROM acciones_web WHERE clave=?', (str(key),)).fetchone()
    if previous:
        if previous['pedido_id'] != str(ident) or previous['tipo'] != kind or previous['payload'] != payload:
            raise HTTPException(409, 'La clave de operación ya se usó con otros datos')
        return json.loads(previous['resultado'])


def save_action(conn, ident, key, kind, payload):
    result = order_view(get_order(conn, ident))
    conn.execute('INSERT INTO acciones_web VALUES(?,?,?,?,?)', (str(key), str(ident), kind, payload, json.dumps(result)))
    return result


@router.post('/api/gestion/tienda/pedidos/{ident}/pesaje')
def prepare(ident: UUID, data: Preparation, person=Depends(authorized)):
    from routers.tienda_operacion import reserve, expire
    import stock
    payload = fingerprint(data)
    with database() as conn:
        conn.execute('BEGIN IMMEDIATE')
        expire(conn)
        previous = prior_action(conn, ident, data.clave_operacion, 'pesaje', payload)
        if previous: return previous
        row = get_order(conn, ident)
        if row['version'] != data.version:
            raise HTTPException(409, 'La solicitud cambió. Actualizá antes de guardar el pesaje.')
        if row['estado'] in ('confirmado','cancelado','vencido','entregado'):
            raise HTTPException(409, 'El total ya fue aprobado. No se puede cambiar desde este pesaje.')
        requested = json.loads(row['lineas'])
        by_id = {l.producto_id: l for l in data.lineas}
        if len(by_id) != len(data.lineas) or set(by_id) != {l['producto_id'] for l in requested}:
            raise HTTPException(422, 'Ingresá un renglón por cada producto solicitado, incluso los omitidos o reemplazados.')
        prepared = []
        costs = {}
        for original in requested:
            line = by_id[original['producto_id']]
            target = dict(original)
            target['solicitado_id'] = original['producto_id']
            if line.omitir:
                if line.reemplazo_id is not None or line.bruto is not None or line.cantidad is not None or line.tara!=0:
                    raise HTTPException(422,'Un renglón omitido no lleva peso ni reemplazo')
                prepared.append({**target,'cantidad':'0','bruto':None,'tara':'0','importe':'0.00','omitido':True})
                continue
            if line.reemplazo_id is not None and line.reemplazo_id!=original['producto_id']:
                if original.get('reemplazo','consultar')=='no_reemplazar':raise HTTPException(422,'El cliente no permite reemplazar ese producto')
                if original.get('reemplazo')=='alternativa' and line.reemplazo_id!=(original.get('alternativa') or {}).get('id'):
                    raise HTTPException(422,'Sólo se permite la alternativa elegida por el cliente')
                replacement,price,photo,eligible = offer(conn,line.reemplazo_id)
                target.update(producto_id=replacement['id'],nombre=replacement['descripcion'],unidad=replacement['unidad_venta'],precio=format(price,'f'),sustitucion=True,promocion=replacement.get('promocion_publica'))
            if target['unidad'] in WEIGHED:
                if line.bruto is None or line.cantidad is not None or line.tara >= line.bruto:
                    raise HTTPException(422, 'Para productos por peso: bruto mayor a tara y sin cantidad por unidad.')
                quantity = line.bruto - line.tara
            else:
                if line.bruto is not None or line.tara != 0 or line.cantidad is None or line.cantidad != line.cantidad.to_integral():
                    raise HTTPException(422, 'Para unidades o atados: cantidad entera, sin bruto ni tara.')
                quantity = line.cantidad
            current = conn.execute('SELECT promedio_exacto,precio_costo FROM productos WHERE id=?',(target['producto_id'],)).fetchone()
            unit_cost = current['promedio_exacto'] if current['promedio_exacto'] is not None else current['precio_costo'] if current['precio_costo'] is not None and current['precio_costo']>0 else None
            costs[str(original['producto_id'])] = money(Decimal(str(unit_cost))*quantity) if unit_cost is not None else None
            prepared.append({**target, 'cantidad': format(quantity, 'f'),
                             'bruto': format(line.bruto, 'f') if line.bruto is not None else None,
                             'tara': format(line.tara, 'f'), 'importe': money(Decimal(target['precio']) * quantity)})
        total = money(sum((Decimal(l['importe']) for l in prepared), Decimal(0)))
        if not any(not l.get('omitido') for l in prepared): raise HTTPException(422,'No hay productos para preparar; cancelá la solicitud o proponé un reemplazo permitido.')
        if row['presupuesto'] is not None and Decimal(total)>Decimal(row['presupuesto']): raise HTTPException(422,'El importe final supera el presupuesto máximo autorizado. Ajustá cantidades o reemplazos.')
        reserve(conn,row,prepared)
        conn.execute("UPDATE pedidos_web SET estado='por_aprobar',version=version+1,preparacion=?,final=?,responsable=?,costos_base=?,aprobado_en=NULL WHERE id=?",
                     (json.dumps(prepared), total, person['nombre'], json.dumps(costs), str(ident)))
        return save_action(conn, ident, data.clave_operacion, 'pesaje', payload)


class Approval(Model):
    version: int = Field(ge=1)
    clave_operacion: UUID
    aceptar: bool


@router.post('/api/tienda/pedidos/{ident}/aprobacion')
def approve(ident: UUID, data: Approval, x_pedido_acceso: str | None = Header(default=None, max_length=100)):
    payload = fingerprint(data)
    with database() as conn:
        conn.execute('BEGIN IMMEDIATE')
        row = customer_order(conn, ident, x_pedido_acceso)
        previous = prior_action(conn, ident, data.clave_operacion, 'aprobacion', payload)
        if previous: return previous
        if row['version'] != data.version or row['estado'] != 'por_aprobar':
            raise HTTPException(409, 'El total cambió o ya fue respondido. Revisá el detalle actualizado.')
        if data.aceptar and row['franja_id'] is not None:
            from routers.tienda_operacion import reserve
            reserve(conn,row,json.loads(row['preparacion']))
        conn.execute("UPDATE pedidos_web SET estado=?,version=version+1,aprobado_en=strftime('%Y-%m-%dT%H:%M:%fZ','now') WHERE id=?",
                     ('confirmado' if data.aceptar else 'revisar', str(ident)))
        if data.aceptar and row['franja_id'] is not None:
            slot = conn.execute('SELECT fin FROM franjas_web WHERE id=?',(row['franja_id'],)).fetchone()
            deadline = datetime.fromisoformat(slot['fin']).timestamp()
            conn.execute('UPDATE pedidos_web SET vence_reserva=? WHERE id=?',(deadline,str(ident)))
            conn.execute('UPDATE reservas_web SET vence=? WHERE pedido_id=?',(deadline,str(ident)))
        return save_action(conn, ident, data.clave_operacion, 'aprobacion', payload)
