"""Prices, accountable changes and purchase reception (roadmap 11–20)."""
import hashlib
import hmac
import json
import os
import secrets
import time
from datetime import date
from decimal import Decimal, ROUND_FLOOR, ROUND_HALF_UP
from typing import Annotated, Literal
from uuid import UUID

from fastapi import APIRouter, Cookie, Depends, HTTPException, Response
from pydantic import Field, SecretStr, field_validator, model_validator
from routers.preparacion import Model, database
import stock

router = APIRouter(prefix='/api/comercial', tags=['Precios y compras'])
Amount = Annotated[Decimal, Field(ge=0, max_digits=14, decimal_places=4, allow_inf_nan=False)]
Money = Annotated[Decimal, Field(ge=0, max_digits=14, decimal_places=2, allow_inf_nan=False)]
Qty = Annotated[Decimal, Field(ge=0, max_digits=14, decimal_places=3, allow_inf_nan=False)]
PositiveQty = Annotated[Decimal, Field(gt=0, max_digits=14, decimal_places=3, allow_inf_nan=False)]

def dec(value):
    return Decimal(str(value))

def rounded(value, places='0.01'):
    return value.quantize(Decimal(places), rounding=ROUND_HALF_UP)

def text(value):
    return format(value, 'f') if value is not None else None

def fingerprint(data):
    def encode(value):
        if isinstance(value,Decimal):
            return format(value.normalize(),'f')
        return str(value)
    return json.dumps(data.model_dump(), default=encode, sort_keys=True, separators=(',',':'))

def product(conn, ident):
    row = conn.execute('SELECT * FROM productos WHERE id=?', (ident,)).fetchone()
    if not row:
        raise HTTPException(404, 'Producto no encontrado')
    return row

def actor(conn, token):
    if not token:
        raise HTTPException(401, 'Ingresá con la clave de un responsable')
    row = conn.execute('SELECT r.id,r.nombre,r.rol FROM sesiones_comerciales s JOIN responsables r ON r.id=s.responsable_id WHERE s.token_hash=? AND s.vence>?', (hashlib.sha256(token.encode()).hexdigest(), time.time())).fetchone()
    if not row:
        raise HTTPException(401, 'La autorización venció. Volvé a ingresar')
    return dict(row)

def authorized(cs_sesion: str | None = Cookie(default=None)):
    with database() as conn:
        person = actor(conn, cs_sesion)
    if person['rol'] not in ('dueno', 'encargado'):
        raise HTTPException(403, 'Solo dueño o encargado pueden modificar precios, costos y compras')
    return person

class Credentials(Model):
    nombre: str = Field(min_length=1, max_length=100)
    clave: SecretStr
    rol: Literal['dueno', 'encargado', 'cajero'] = 'dueno'

    @field_validator('clave')
    @classmethod
    def password_length(cls, value):
        if not 8 <= len(value.get_secret_value()) <= 128 or not value.get_secret_value().strip():
            raise ValueError('La clave debe tener entre 8 y 128 caracteres')
        return value

def password_hash(password, salt):
    return hashlib.scrypt(password.encode(), salt=bytes.fromhex(salt), n=16384, r=8, p=1).hex()

@router.get('/autorizacion')
def authorization_status(cs_sesion: str | None = Cookie(default=None)):
    with database() as conn:
        configured = conn.execute('SELECT COUNT(*) FROM responsables').fetchone()[0] > 0
        try:
            person = actor(conn, cs_sesion)
        except HTTPException:
            person = None
    return {'configurado': configured, 'responsable': person}

@router.post('/responsables', status_code=201)
def create_responsible(data: Credentials, cs_sesion: str | None = Cookie(default=None)):
    with database() as conn:
        conn.execute('BEGIN IMMEDIATE')
        if conn.execute('SELECT COUNT(*) FROM responsables').fetchone()[0]:
            if actor(conn, cs_sesion)['rol'] != 'dueno':
                raise HTTPException(403, 'Solo el dueño puede agregar responsables')
        elif os.environ.get('NATIVA_ENV') == 'production':
            raise HTTPException(403, 'El primer dueño se crea desde la consola del servidor')
        elif data.rol != 'dueno':
            raise HTTPException(422, 'El primer responsable debe ser el dueño')
        if conn.execute('SELECT 1 FROM responsables WHERE lower(nombre)=lower(?)', (data.nombre,)).fetchone():
            raise HTTPException(409, 'Ya existe un responsable con ese nombre')
        salt = secrets.token_hex(16)
        ident = conn.execute('INSERT INTO responsables(nombre,rol,sal,clave_hash) VALUES(?,?,?,?)', (data.nombre, data.rol, salt, password_hash(data.clave.get_secret_value(), salt))).lastrowid
    return {'id': ident, 'nombre': data.nombre, 'rol': data.rol}

class Login(Model):
    nombre: str = Field(min_length=1, max_length=100)
    clave: SecretStr

@router.post('/sesion')
def login(data: Login, response: Response):
    error = None
    with database() as conn:
        conn.execute('BEGIN IMMEDIATE')
        row = conn.execute('SELECT * FROM responsables WHERE lower(nombre)=lower(?)', (data.nombre,)).fetchone()
        if row and row['bloqueado_hasta'] > time.time():
            error = (429, 'Demasiados intentos. Esperá 15 minutos antes de volver a ingresar')
        elif not row or len(data.clave.get_secret_value()) > 128 or not hmac.compare_digest(password_hash(data.clave.get_secret_value(), row['sal']), row['clave_hash']):
            if row:
                attempts = row['intentos'] + 1
                conn.execute('UPDATE responsables SET intentos=?,bloqueado_hasta=? WHERE id=?', (attempts if attempts < 5 else 0, time.time() + 900 if attempts >= 5 else 0, row['id']))
            error = (401, 'Nombre o clave incorrectos')
        else:
            conn.execute('UPDATE responsables SET intentos=0,bloqueado_hasta=0 WHERE id=?', (row['id'],))
            conn.execute('DELETE FROM sesiones_comerciales WHERE vence<=?', (time.time(),))
            token = secrets.token_urlsafe(32)
            conn.execute('INSERT INTO sesiones_comerciales VALUES(?,?,?)', (hashlib.sha256(token.encode()).hexdigest(), row['id'], time.time() + 1800))
    if error:
        raise HTTPException(*error)
    response.set_cookie('cs_sesion', token, max_age=1800, httponly=True, samesite='strict', secure=os.environ.get('CORONEL_SECURE_COOKIE') == '1' or os.environ.get('NATIVA_ENV') == 'production')
    return {'id': row['id'], 'nombre': row['nombre'], 'rol': row['rol']}

@router.delete('/sesion')
def logout(response: Response, cs_sesion: str | None = Cookie(default=None)):
    with database() as conn:
        if cs_sesion:
            conn.execute('DELETE FROM sesiones_comerciales WHERE token_hash=?', (hashlib.sha256(cs_sesion.encode()).hexdigest(),))
    response.delete_cookie('cs_sesion')
    return {'ok': True}

def financial(conn, p):
    sale = dec(p['venta_exacta']) if p['venta_exacta'] is not None else dec(p['precio_venta']) if p['precio_venta'] else None
    replacement = dec(p['reposicion_exacta']) if p['reposicion_exacta'] is not None else dec(p['precio_costo']) if p['precio_costo'] else None
    average = dec(p['promedio_exacto']) if p['promedio_exacto'] is not None else dec(p['precio_costo']) if p['precio_costo'] else None
    histories = [dict(r) for r in conn.execute('SELECT id,tipo,importe,anterior,unidad,responsable,motivo,origen_id,creado FROM historial_comercial WHERE producto_id=? ORDER BY id DESC', (p['id'],))]
    margin = rounded((sale-replacement)/sale*100) if sale is not None and sale > 0 and replacement is not None else None
    markup = rounded((sale-replacement)/replacement*100) if sale is not None and replacement is not None and replacement > 0 else None
    return {'id': p['id'], 'codigo': p['codigo'], 'descripcion': p['descripcion'], 'unidad': p['unidad_venta'], 'precio': text(sale), 'reposicion': text(replacement), 'promedio': text(average), 'stock': str(p['stock']), 'margen': text(margin), 'recargo': text(markup), 'historial': histories,
            'version_precio': next((h['id'] for h in histories if h['tipo']=='precio'),0), 'version_costo': next((h['id'] for h in histories if h['tipo']!='precio'),0)}

@router.get('/productos')
def financial_products():
    with database() as conn:
        return [financial(conn, p) for p in conn.execute('SELECT * FROM productos WHERE activo=1 ORDER BY descripcion,id').fetchall()]

class Change(Model):
    tipo: Literal['precio', 'reposicion']
    importe: Amount
    motivo: str = Field(min_length=3, max_length=300)
    version: int = Field(ge=0)
    clave_operacion: UUID

@router.post('/productos/{product_id}/ajuste')
def change(product_id: int, data: Change, person=Depends(authorized)):
    with database() as conn:
        conn.execute('BEGIN IMMEDIATE')
        previous = conn.execute('SELECT * FROM historial_comercial WHERE clave_operacion=?', (str(data.clave_operacion),)).fetchone()
        if previous:
            if previous['producto_id'] != product_id or previous['payload'] != fingerprint(data):
                raise HTTPException(409, 'La clave de operación ya se usó con otros datos')
            return financial(conn, product(conn, product_id))
        p = product(conn, product_id)
        state = financial(conn, p)
        key = 'precio' if data.tipo == 'precio' else 'costo'
        if data.version != state['version_'+key]:
            raise HTTPException(409, 'El valor cambió en otra operación. Recargá antes de guardar')
        before = state['precio' if data.tipo == 'precio' else 'reposicion']
        conn.execute('INSERT INTO historial_comercial(producto_id,tipo,importe,anterior,unidad,responsable,motivo,clave_operacion,payload) VALUES(?,?,?,?,?,?,?,?,?)', (product_id,data.tipo,text(data.importe),before,p['unidad_venta'],person['nombre'],data.motivo,str(data.clave_operacion),fingerprint(data)))
        if data.tipo == 'precio':
            conn.execute("UPDATE productos SET venta_exacta=?,precio_venta=?,actualizado_en=datetime('now') WHERE id=?", (text(data.importe),float(data.importe),product_id))
        else:
            conn.execute("UPDATE productos SET reposicion_exacta=?,actualizado_en=datetime('now') WHERE id=?", (text(data.importe),product_id))
        return financial(conn, product(conn, product_id))

class Supplier(Model):
    nombre: str = Field(min_length=1, max_length=150)
    contacto: str = Field(default='', max_length=120)
    telefono: str = Field(default='', max_length=60)
    documento: str = Field(default='', max_length=40)
    condiciones: str = Field(default='', max_length=300)
    dias_plazo: int = Field(default=0, ge=0, le=365)
    activo: bool = True

@router.get('/proveedores')
def suppliers():
    with database() as conn:
        return [dict(r) for r in conn.execute('SELECT * FROM proveedores ORDER BY nombre,id')]

@router.post('/proveedores', status_code=201)
def create_supplier(data: Supplier, person=Depends(authorized)):
    fields = data.model_dump()
    with database() as conn:
        ident = conn.execute(f"INSERT INTO proveedores({','.join(fields)}) VALUES({','.join('?' for _ in fields)})", tuple(fields.values())).lastrowid
    return {'id':ident, **fields}

@router.put('/proveedores/{ident}')
def edit_supplier(ident: int, data: Supplier, person=Depends(authorized)):
    fields = data.model_dump()
    with database() as conn:
        cur = conn.execute(f"UPDATE proveedores SET {','.join(f'{k}=?' for k in fields)} WHERE id=?", (*fields.values(),ident))
        if not cur.rowcount:
            raise HTTPException(404,'Proveedor no encontrado')
    return {'id':ident, **fields}

class OrderLine(Model):
    producto_id: int = Field(gt=0)
    cantidad: PositiveQty
    precio: Amount

class Order(Model):
    proveedor_id: int = Field(gt=0)
    fecha_entrega: date | None = None
    notas: str = Field(default='', max_length=1000)
    lineas: list[OrderLine] = Field(min_length=1, max_length=100)
    clave_operacion: UUID

    @model_validator(mode='after')
    def distinct(self):
        if len({x.producto_id for x in self.lineas}) != len(self.lineas):
            raise ValueError('Agrupá cada producto en una sola línea')
        return self

def require_quantity_unit(quantity, unit):
    if unit not in ('kg','g') and quantity != quantity.to_integral_value():
        raise HTTPException(422, 'La cantidad de unidades, atados, bolsas, bandejas o cajones debe ser entera')

def order_detail(conn, ident):
    row = conn.execute('SELECT * FROM pedidos_compra WHERE id=?', (ident,)).fetchone()
    if not row:
        raise HTTPException(404, 'Pedido no encontrado')
    result = {k:row[k] for k in row.keys() if k not in ('payload','clave_operacion')}
    lines = []
    for line in conn.execute('SELECT * FROM pedido_lineas WHERE pedido_id=? ORDER BY id', (ident,)):
        item = dict(line)
        item['pendiente'] = text(dec(line['cantidad'])-dec(line['recibido']))
        lines.append(item)
    result['lineas'] = lines
    result['estado'] = 'recibido' if all(dec(x['pendiente'])==0 for x in lines) else 'parcial' if any(dec(x['recibido'])>0 for x in lines) else 'pendiente'
    result['total_estimado'] = text(sum((rounded(dec(x['cantidad'])*dec(x['precio'])) for x in lines),Decimal(0)))
    result['recepciones'] = [json.loads(r['datos']) for r in conn.execute('SELECT datos FROM recepciones_compra WHERE pedido_id=? ORDER BY id', (ident,))]
    return result

@router.get('/pedidos')
def orders():
    with database() as conn:
        return [order_detail(conn,r[0]) for r in conn.execute('SELECT id FROM pedidos_compra ORDER BY id DESC').fetchall()]

@router.post('/pedidos', status_code=201)
def create_order(data: Order, person=Depends(authorized)):
    with database() as conn:
        conn.execute('BEGIN IMMEDIATE')
        previous = conn.execute('SELECT id,payload FROM pedidos_compra WHERE clave_operacion=?', (str(data.clave_operacion),)).fetchone()
        if previous:
            if previous['payload'] != fingerprint(data):
                raise HTTPException(409,'La clave del pedido ya se usó con otros datos')
            return order_detail(conn,previous['id'])
        supplier = conn.execute('SELECT * FROM proveedores WHERE id=? AND activo=1',(data.proveedor_id,)).fetchone()
        if not supplier:
            raise HTTPException(422,'Seleccioná un proveedor activo')
        snapshots = []
        for line in data.lineas:
            p = product(conn,line.producto_id)
            if not p['activo']:
                raise HTTPException(422,'El pedido contiene un producto inactivo')
            require_quantity_unit(line.cantidad,p['unidad_venta'])
            snapshots.append((line,p))
        ident = conn.execute('INSERT INTO pedidos_compra(proveedor_id,proveedor_nombre,condiciones,dias_plazo,fecha_entrega,notas,responsable,clave_operacion,payload) VALUES(?,?,?,?,?,?,?,?,?)', (supplier['id'],supplier['nombre'],supplier['condiciones'],supplier['dias_plazo'],str(data.fecha_entrega) if data.fecha_entrega else None,data.notas,person['nombre'],str(data.clave_operacion),fingerprint(data))).lastrowid
        for line,p in snapshots:
            description = ' · '.join(filter(None,[p['descripcion'],p['variedad'],p['calidad'],p['presentacion']]))
            conn.execute('INSERT INTO pedido_lineas(pedido_id,producto_id,descripcion,unidad,cantidad,precio) VALUES(?,?,?,?,?,?)', (ident,p['id'],description,p['unidad_venta'],text(line.cantidad),text(line.precio)))
        return order_detail(conn,ident)

class ReceivedLine(Model):
    linea_id: int = Field(gt=0)
    bultos: int = Field(default=0, ge=0, le=1000000)
    bruto_kg: Qty | None = None
    tara_kg: Qty | None = None
    cantidad: PositiveQty | None = None
    rechazado: Qty = Decimal(0)
    precio: Amount | None = None
    importe_mercaderia: Money | None = None
    calidad: Literal['buena','regular','mala'] = 'buena'
    observaciones: str = Field(default='', max_length=500)

    @model_validator(mode='after')
    def pricing_basis(self):
        if (self.precio is None) == (self.importe_mercaderia is None):
            raise ValueError('Indicá precio por unidad o importe total de mercadería, no ambos')
        return self

class Receipt(Model):
    ubicacion_id: int = Field(default=1,gt=0)
    gastos_a_proveedor: bool = False
    clave_operacion: UUID
    referencia: str = Field(default='', max_length=100)
    flete: Money = Decimal(0)
    otros_gastos: Money = Decimal(0)
    lineas: list[ReceivedLine] = Field(min_length=1, max_length=100)

    @model_validator(mode='after')
    def distinct(self):
        if len({x.linea_id for x in self.lineas}) != len(self.lineas):
            raise ValueError('No repetir líneas de recepción')
        return self

def allocate_expenses(total, weights):
    if not weights:
        if total:
            raise HTTPException(422,'No se pueden distribuir gastos sin mercadería aceptada')
        return []
    if not sum(weights):
        weights = [Decimal(1)] * len(weights)
    raw = [total * w / sum(weights) for w in weights]
    allocations = [r.quantize(Decimal('.01'),rounding=ROUND_FLOOR) for r in raw]
    cents = int((total-sum(allocations))*100)
    for index in sorted(range(len(raw)),key=lambda i: raw[i]-allocations[i],reverse=True)[:cents]:
        allocations[index] += Decimal('.01')
    return allocations

@router.post('/pedidos/{ident}/recepciones', status_code=201)
def receive(ident: int, data: Receipt, person=Depends(authorized)):
    with database() as conn:
        conn.execute('BEGIN IMMEDIATE')
        prior = conn.execute('SELECT * FROM recepciones_compra WHERE clave_operacion=?',(str(data.clave_operacion),)).fetchone()
        if prior:
            old_payload=json.loads(prior['payload'])
            old_payload.setdefault('ubicacion_id',1)
            old_payload.setdefault('gastos_a_proveedor',False)
            if prior['pedido_id'] != ident or old_payload != json.loads(fingerprint(data)):
                raise HTTPException(409,'La clave de recepción ya se usó con otros datos')
            return json.loads(prior['datos'])
        order_detail(conn,ident)
        stock.location(conn,data.ubicacion_id)
        items = []
        for incoming in data.lineas:
            line = conn.execute('SELECT * FROM pedido_lineas WHERE id=? AND pedido_id=?',(incoming.linea_id,ident)).fetchone()
            if not line:
                raise HTTPException(422,'Una línea no pertenece a este pedido')
            p = product(conn,line['producto_id'])
            if p['unidad_venta'] != line['unidad']:
                raise HTTPException(409,'La unidad del producto cambió desde el pedido')
            if line['unidad'] in ('kg','g'):
                if incoming.bruto_kg is None or incoming.tara_kg is None or incoming.cantidad is not None:
                    raise HTTPException(422,'Para productos por peso registrá bruto y tara en kg, sin cantidad manual')
                net_kg = incoming.bruto_kg-incoming.tara_kg
                total = net_kg * (1000 if line['unidad']=='g' else 1)
                if total <= 0:
                    raise HTTPException(422,'El peso neto debe ser positivo y la tara menor al bruto')
            else:
                if incoming.cantidad is None or incoming.bruto_kg is not None or incoming.tara_kg is not None:
                    raise HTTPException(422,'Para este producto registrá cantidad, sin peso bruto ni tara')
                total = incoming.cantidad
            require_quantity_unit(total,line['unidad'])
            require_quantity_unit(incoming.rechazado,line['unidad'])
            accepted = total-incoming.rechazado
            if accepted < 0:
                raise HTTPException(422,'La cantidad rechazada supera la recibida')
            if incoming.rechazado and not incoming.observaciones:
                raise HTTPException(422,'Indicá el motivo del rechazo')
            if accepted > dec(line['cantidad'])-dec(line['recibido']):
                raise HTTPException(409,'La cantidad aceptada supera el pendiente del pedido')
            subtotal = incoming.importe_mercaderia if incoming.importe_mercaderia is not None else rounded(accepted*incoming.precio)
            if accepted == 0 and subtotal > 0:
                raise HTTPException(422,'No se puede asignar un importe de mercadería a una línea totalmente rechazada')
            items.append({'linea_id':line['id'],'producto_id':p['id'],'descripcion':line['descripcion'],'unidad':line['unidad'],**incoming.model_dump(mode='json',exclude={'linea_id'}),'total_recibido':text(total),'aceptado':text(accepted),'subtotal':text(subtotal)})
        accepted_items = [i for i in items if dec(i['aceptado'])>0]
        expenses = data.flete+data.otros_gastos
        allocated = allocate_expenses(expenses,[dec(i['subtotal']) for i in accepted_items])
        for item,assigned in zip(accepted_items,allocated):
            item['gastos_asignados'] = text(assigned)
            item['costo_total'] = text(dec(item['subtotal'])+assigned)
            item['costo_unitario'] = text(rounded(dec(item['costo_total'])/dec(item['aceptado']),'0.0001'))
            if dec(item['costo_unitario']) > Decimal('9999999999.9999'):
                raise HTTPException(422,'El costo por unidad supera el límite admitido. Revisá pesos, precio y gastos')
        for item in items:
            if dec(item['aceptado'])==0:
                item.update(gastos_asignados='0.00',costo_total='0.00',costo_unitario=None)
        result = {'pedido_id':ident,'referencia':data.referencia,'responsable':person['nombre'],'flete':text(data.flete),'otros_gastos':text(data.otros_gastos),'total':text(sum((dec(i['subtotal']) for i in items),Decimal(0))+expenses),'lineas':items}
        rid = conn.execute('INSERT INTO recepciones_compra(pedido_id,clave_operacion,payload,datos) VALUES(?,?,?,?)',(ident,str(data.clave_operacion),fingerprint(data),'{}')).lastrowid
        result['id'] = rid
        result['creado'] = conn.execute('SELECT creado FROM recepciones_compra WHERE id=?',(rid,)).fetchone()[0]
        for item in accepted_items:
            stock.require_consistent(conn,item['producto_id'])
            p = product(conn,item['producto_id'])
            current = financial(conn,p)
            old_stock = dec(p['stock'])
            qty = dec(item['aceptado'])
            if old_stock < 0:
                raise HTTPException(409,'Corregí el stock negativo antes de calcular el costo de recepción')
            average = rounded((old_stock*dec(current['promedio'])+dec(item['costo_total']))/(old_stock+qty),'0.0001') if current['promedio'] is not None else dec(item['costo_unitario']) if old_stock==0 else None
            new_stock = old_stock+qty
            if new_stock > Decimal('99999999999'):
                raise HTTPException(422,'La existencia resultante supera el límite admitido')
            conn.execute("UPDATE productos SET stock=?,reposicion_exacta=?,promedio_exacto=?,precio_costo=?,actualizado_en=datetime('now') WHERE id=?", (float(new_stock),item['costo_unitario'],text(average),float(average) if average is not None else p['precio_costo'],p['id']))
            conn.execute('INSERT INTO historial_comercial(producto_id,tipo,importe,anterior,unidad,responsable,motivo,origen_id) VALUES(?,?,?,?,?,?,?,?)',(p['id'],'compra',item['costo_unitario'],current['reposicion'],p['unidad_venta'],person['nombre'],f'Recepción {rid}',rid))
            conn.execute('UPDATE pedido_lineas SET recibido=? WHERE id=?',(text(dec(conn.execute('SELECT recibido FROM pedido_lineas WHERE id=?',(item['linea_id'],)).fetchone()[0])+qty),item['linea_id']))
            conn.execute('INSERT INTO movimientos_compra(recepcion_id,linea_id,producto_id,cantidad,unidad,costo_total) VALUES(?,?,?,?,?,?)',(rid,item['linea_id'],p['id'],text(qty),p['unidad_venta'],item['costo_total']))
            stock.record_receipt(conn,rid,item,person['nombre'],data.ubicacion_id)
        result['ubicacion_id']=data.ubicacion_id
        result['importe_proveedor']=text(sum((dec(i['subtotal']) for i in items),Decimal(0))+(expenses if data.gastos_a_proveedor else 0))
        result['gastos_a_proveedor']=data.gastos_a_proveedor
        conn.execute('UPDATE recepciones_compra SET datos=? WHERE id=?',(json.dumps(result,ensure_ascii=False),rid))
        stock.receipt_charge(conn,rid)
        return result

@router.get('/ubicaciones')
def stock_locations():
    with database() as conn:
        return [dict(r) for r in conn.execute('SELECT * FROM ubicaciones_stock ORDER BY id')]
