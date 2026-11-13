"""Store operations: capacity, reservations, help and private contribution reports."""
import json
import time
from collections import defaultdict
from datetime import datetime, timezone
from decimal import Decimal
from typing import Literal
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import Field, model_validator
from routers.preparacion import Model, database
from routers.comercial import authorized
from routers.tienda import customer_order, get_order, order_view, offer, public_product, money, fingerprint, prior_action, save_action
import stock

router=APIRouter(tags=['Operación de tienda'])
D=lambda v: Decimal(str(v))
TERMINAL={'cancelado','vencido','entregado'}

class Settings(Model):
    abierta: bool=True
    requiere_franja: bool=False
    reserva_minutos: int=Field(default=120,ge=15,le=1440)
    contacto: str=Field(default='',max_length=200)


def settings(conn):
    row=conn.execute('SELECT datos FROM configuracion_web WHERE id=1').fetchone()
    return Settings.model_validate_json(row[0]) if row else Settings()


def expire(conn):
    now=time.time()
    conn.execute("UPDATE pedidos_web SET estado='vencido',version=version+1 WHERE vence_reserva IS NOT NULL AND vence_reserva<=? AND estado NOT IN ('entregado','cancelado','vencido')",(now,))
    conn.execute('DELETE FROM reservas_web WHERE vence<=? OR pedido_id IN (SELECT id FROM pedidos_web WHERE estado IN (\'entregado\',\'cancelado\',\'vencido\'))',(now,))


def slot_view(conn,row):
    used=conn.execute("SELECT COUNT(*) FROM pedidos_web WHERE franja_id=? AND estado NOT IN ('cancelado','vencido')",(row['id'],)).fetchone()[0]
    return {**dict(row),'libres':max(0,row['cupo']-used)}


def check_slot(conn,ident):
    row=conn.execute('SELECT * FROM franjas_web WHERE id=?',(ident,)).fetchone()
    if not row or not row['activa'] or datetime.fromisoformat(row['inicio']).timestamp()<=time.time():
        raise HTTPException(409,'La franja ya cerró. Elegí otro horario.')
    if slot_view(conn,row)['libres']<=0:
        raise HTTPException(409,'La franja está completa. Elegí otro horario.')
    return row


def reserve(conn,row,lines):
    if row['franja_id'] is None:return
    deadline=row['vence_reserva']
    if not deadline or deadline<=time.time():raise HTTPException(409,'La reserva venció; no se puede renovar automáticamente.')
    totals=defaultdict(Decimal)
    for line in lines:
        if not line.get('omitido'):totals[line['producto_id']]+=D(line['cantidad'])
    for ident,qty in totals.items():
        stock.require_consistent(conn,ident)
        if stock.free_web(conn,ident,row['id'])<qty:
            raise HTTPException(409,'No alcanza el stock libre de un producto. Revisá cantidad o reemplazo.')
    conn.execute('DELETE FROM reservas_web WHERE pedido_id=?',(row['id'],))
    for ident,qty in totals.items():
        conn.execute('INSERT INTO reservas_web VALUES(?,?,?,?)',(row['id'],ident,str(qty),deadline))


def reservation_risk(conn,row):
    if row['estado'] in TERMINAL:return False
    return any(D(r['cantidad'])>stock.free_web(conn,r['producto_id'],row['id']) for r in conn.execute('SELECT producto_id,cantidad FROM reservas_web WHERE pedido_id=? AND vence>?',(row['id'],time.time())))


@router.get('/api/gestion/tienda/configuracion')
def read_settings(person=Depends(authorized)):
    with database() as conn:return settings(conn).model_dump()


@router.put('/api/gestion/tienda/configuracion')
def write_settings(data:Settings,person=Depends(authorized)):
    with database() as conn:conn.execute('INSERT INTO configuracion_web VALUES(1,?) ON CONFLICT(id) DO UPDATE SET datos=excluded.datos',(data.model_dump_json(),))
    return data.model_dump()


class Slot(Model):
    inicio:datetime
    fin:datetime
    cupo:int=Field(ge=1,le=100)
    activa:bool=True
    @model_validator(mode='after')
    def dates(self):
        if self.inicio.tzinfo is None or self.fin.tzinfo is None:raise ValueError('Los horarios necesitan zona horaria')
        if self.fin<=self.inicio or (self.fin-self.inicio).total_seconds()>8*3600:raise ValueError('La franja debe durar entre 1 segundo y 8 horas')
        if self.inicio.timestamp()<=time.time() or self.inicio.timestamp()>time.time()+7*86400:raise ValueError('Elegí una franja futura dentro de los próximos siete días')
        return self


@router.get('/api/gestion/tienda/franjas')
def staff_slots(person=Depends(authorized)):
    with database() as conn:
        expire(conn)
        return [slot_view(conn,r) for r in conn.execute('SELECT * FROM franjas_web ORDER BY inicio DESC LIMIT 100')]


@router.post('/api/gestion/tienda/franjas',status_code=201)
def add_slot(data:Slot,person=Depends(authorized)):
    with database() as conn:
        conn.execute('BEGIN IMMEDIATE')
        expire(conn)
        if conn.execute("SELECT 1 FROM franjas_web f WHERE (activa=1 OR EXISTS(SELECT 1 FROM pedidos_web p WHERE p.franja_id=f.id AND p.estado NOT IN ('cancelado','vencido'))) AND inicio<? AND fin>?",(data.fin.astimezone(timezone.utc).isoformat(),data.inicio.astimezone(timezone.utc).isoformat())).fetchone():
            raise HTTPException(409,'La franja se superpone con otra activa')
        ident=conn.execute('INSERT INTO franjas_web(inicio,fin,cupo,activa) VALUES(?,?,?,?)',(data.inicio.astimezone(timezone.utc).isoformat(),data.fin.astimezone(timezone.utc).isoformat(),data.cupo,data.activa)).lastrowid
        return slot_view(conn,conn.execute('SELECT * FROM franjas_web WHERE id=?',(ident,)).fetchone())


@router.delete('/api/gestion/tienda/franjas/{ident}')
def close_slot(ident:int,person=Depends(authorized)):
    with database() as conn:
        if not conn.execute('SELECT 1 FROM franjas_web WHERE id=?',(ident,)).fetchone():raise HTTPException(404,'Franja no encontrada')
        conn.execute('UPDATE franjas_web SET activa=0 WHERE id=?',(ident,))
    return {'cerrada':True,'nota':'Los compromisos existentes se conservan.'}


class Action(Model):
    version:int=Field(ge=1)
    clave_operacion:UUID


def cancel(conn,row,data,kind):
    payload=fingerprint(data)
    previous=prior_action(conn,row['id'],data.clave_operacion,kind,payload)
    if previous:return previous
    if row['version']!=data.version or row['estado'] in TERMINAL:raise HTTPException(409,'El pedido cambió o ya terminó. Actualizá el estado.')
    conn.execute('DELETE FROM reservas_web WHERE pedido_id=?',(row['id'],))
    conn.execute("UPDATE pedidos_web SET estado='cancelado',version=version+1 WHERE id=?",(row['id'],))
    return save_action(conn,row['id'],data.clave_operacion,kind,payload)


@router.post('/api/tienda/pedidos/{ident}/cancelacion')
def customer_cancel(ident:UUID,data:Action,x_pedido_acceso:str|None=Header(default=None,max_length=100)):
    with database() as conn:
        conn.execute('BEGIN IMMEDIATE');expire(conn)
        return cancel(conn,customer_order(conn,ident,x_pedido_acceso),data,'cancelacion_cliente')


@router.post('/api/gestion/tienda/pedidos/{ident}/cancelacion')
def staff_cancel(ident:UUID,data:Action,person=Depends(authorized)):
    with database() as conn:
        conn.execute('BEGIN IMMEDIATE');expire(conn)
        return cancel(conn,get_order(conn,ident),data,'cancelacion_personal')


@router.get('/api/tienda/pedidos/{ident}/repetir')
def reorder(ident:UUID,x_pedido_acceso:str|None=Header(default=None,max_length=100)):
    with database() as conn:
        row=customer_order(conn,ident,x_pedido_acceso);items=[];changes=[]
        for old in json.loads(row['lineas']):
            try:p,price,photo,eligible=offer(conn,old['producto_id'])
            except HTTPException:
                changes.append(old['nombre']+': ya no está publicado');continue
            if p['unidad_venta']!=old['unidad']:
                changes.append(old['nombre']+': cambió la unidad; elegí la cantidad de nuevo');continue
            if price!=D(old['precio']):changes.append(old['nombre']+': precio actualizado')
            alternate=(old.get('alternativa') or {}).get('id')
            if alternate is not None:
                try:offer(conn,alternate)
                except HTTPException:
                    alternate=None
                    changes.append(old['nombre']+': su alternativa ya no está publicada; elegí otra o cambiá la preferencia')
            items.append({**public_product(p,price),'cantidad':old['cantidad'],'reemplazo':old.get('reemplazo','consultar'),'alternativa_id':alternate})
        return {'lineas':items,'cambios':changes,'mensaje':'Lista para revisar con precios actuales. No crea un pedido ni realiza cobros.'}


class Complaint(Model):
    clave_operacion:UUID
    producto_id:int|None=Field(default=None,gt=0)
    tipo:Literal['faltante','calidad','cantidad','reemplazo','cobro','entrega','consulta']
    detalle:str=Field(min_length=5,max_length=1500)


def complaints(conn,ident):
    rows=[]
    for r in conn.execute('SELECT * FROM reclamos_web WHERE pedido_id=? ORDER BY creado',(str(ident),)):
        rows.append({k:r[k] for k in ('id','producto_id','tipo','detalle','estado','version','creado')})
        rows[-1]['respuestas']=[{'texto':m['texto'],'creado':m['creado'],'autor':'Nativa'} for m in conn.execute('SELECT * FROM respuestas_web WHERE reclamo_id=? ORDER BY id',(r['id'],))]
    return rows


@router.get('/api/tienda/pedidos/{ident}/reclamos')
def customer_complaints(ident:UUID,x_pedido_acceso:str|None=Header(default=None,max_length=100)):
    with database() as conn:
        customer_order(conn,ident,x_pedido_acceso)
        return complaints(conn,ident)


@router.post('/api/tienda/pedidos/{ident}/reclamos',status_code=201)
def create_complaint(ident:UUID,data:Complaint,x_pedido_acceso:str|None=Header(default=None,max_length=100)):
    payload=fingerprint(data)
    with database() as conn:
        conn.execute('BEGIN IMMEDIATE');row=customer_order(conn,ident,x_pedido_acceso)
        previous=conn.execute('SELECT * FROM reclamos_web WHERE clave=?',(str(data.clave_operacion),)).fetchone()
        if previous:
            if previous['pedido_id']!=str(ident) or previous['payload']!=payload:raise HTTPException(409,'La clave ya se usó con otro reclamo')
            return next(r for r in complaints(conn,ident) if r['id']==previous['id'])
        ids={l['producto_id'] for l in json.loads(row['lineas'])}|{l['producto_id'] for l in json.loads(row['preparacion'] or '[]')}
        if data.producto_id and data.producto_id not in ids:raise HTTPException(422,'El producto no pertenece a este pedido')
        if conn.execute("SELECT COUNT(*) FROM reclamos_web WHERE pedido_id=? AND estado!='resuelto'",(str(ident),)).fetchone()[0]>=5:raise HTTPException(429,'Ya hay cinco consultas abiertas. Revisá las respuestas o contactá al local.')
        key=str(uuid4())
        conn.execute('INSERT INTO reclamos_web(id,pedido_id,clave,payload,producto_id,tipo,detalle) VALUES(?,?,?,?,?,?,?)',(key,str(ident),str(data.clave_operacion),payload,data.producto_id,data.tipo,data.detalle))
        return next(r for r in complaints(conn,ident) if r['id']==key)


class Reply(Action):
    estado:Literal['abierto','en_revision','resuelto']
    texto:str=Field(min_length=3,max_length=1500)


@router.post('/api/gestion/tienda/pedidos/{ident}/reclamos/{claim_id}')
def reply(ident:UUID,claim_id:UUID,data:Reply,person=Depends(authorized)):
    payload=fingerprint(data)
    with database() as conn:
        conn.execute('BEGIN IMMEDIATE')
        previous=prior_action(conn,ident,data.clave_operacion,'respuesta:'+str(claim_id),payload)
        if previous:return previous
        claim=conn.execute('SELECT * FROM reclamos_web WHERE id=? AND pedido_id=?',(str(claim_id),str(ident))).fetchone()
        if not claim:raise HTTPException(404,'Consulta no encontrada')
        if claim['version']!=data.version:raise HTTPException(409,'La consulta cambió. Actualizá antes de responder.')
        conn.execute('INSERT INTO respuestas_web(reclamo_id,texto,responsable) VALUES(?,?,?)',(str(claim_id),data.texto,person['nombre']))
        conn.execute('UPDATE reclamos_web SET estado=?,version=version+1 WHERE id=?',(data.estado,str(claim_id)))
        return save_action(conn,ident,data.clave_operacion,'respuesta:'+str(claim_id),payload)


class Expenses(Action):
    empaque:Decimal=Field(ge=0,max_digits=14,decimal_places=2,allow_inf_nan=False)
    comision:Decimal=Field(ge=0,max_digits=14,decimal_places=2,allow_inf_nan=False)
    minutos:Decimal=Field(ge=0,le=1440,max_digits=8,decimal_places=2,allow_inf_nan=False)
    valor_hora:Decimal=Field(ge=0,max_digits=14,decimal_places=2,allow_inf_nan=False)
    reparto:Decimal=Field(ge=0,max_digits=14,decimal_places=2,allow_inf_nan=False)
    incidencias:Decimal=Field(ge=0,max_digits=14,decimal_places=2,allow_inf_nan=False)


def profitability(conn,row):
    prepared=json.loads(row['preparacion'] or '[]')
    cost_data=json.loads(row['costos_base'] or '{}')
    costs=[cost_data.get(str(l['solicitado_id'] if 'solicitado_id' in l else l['producto_id'])) for l in prepared if not l.get('omitido')]
    merchandise=sum((D(v) for v in costs if v is not None),D(0)) if costs and all(v is not None for v in costs) else None
    if row['estado']=='entregado':
        movements=conn.execute("SELECT costo_total FROM movimientos_stock WHERE tipo='venta_web' AND documento_id=?",(row['id'],)).fetchall()
        merchandise=sum((D(m[0]) for m in movements if m[0] is not None),D(0)) if movements and all(m[0] is not None for m in movements) else None
    latest=conn.execute('SELECT datos FROM costos_web WHERE pedido_id=? ORDER BY id DESC LIMIT 1',(row['id'],)).fetchone()
    expenses=json.loads(latest[0]) if latest else None
    revenue=D(row['final']) if row['final'] is not None else D(row['estimado'])
    variable=None;contribution=None
    if expenses:
        variable=sum((D(expenses[k]) for k in ('empaque','comision','reparto','incidencias')),D(0))+D(expenses['minutos'])*D(expenses['valor_hora'])/60
        variable=D(money(variable))
        if merchandise is not None:contribution=revenue-merchandise-variable
    return {'pedido_id':row['id'],'base':'realizada_con_costos_declarados' if row['estado']=='entregado' else 'estimada',
            'ingreso':money(revenue),'mercaderia':money(merchandise) if merchandise is not None else None,
            'gastos_variables':money(variable) if variable is not None else None,'contribucion':money(contribution) if contribution is not None else None,
            'margen_porcentaje':money(contribution/revenue*100) if contribution is not None and revenue else None,
            'gastos':expenses,'completo':contribution is not None,'nota':'Antes de costos fijos e impuestos. Gastos declarados; cobro electrónico no integrado.'}


@router.get('/api/gestion/tienda/pedidos/{ident}/rentabilidad')
def read_profit(ident:UUID,person=Depends(authorized)):
    with database() as conn:return profitability(conn,get_order(conn,ident))


@router.post('/api/gestion/tienda/pedidos/{ident}/costos')
def save_expenses(ident:UUID,data:Expenses,person=Depends(authorized)):
    payload=fingerprint(data)
    with database() as conn:
        conn.execute('BEGIN IMMEDIATE');row=get_order(conn,ident)
        previous=prior_action(conn,ident,data.clave_operacion,'costos',payload)
        if previous:return previous
        if row['version']!=data.version:raise HTTPException(409,'El pedido cambió. Actualizá antes de registrar costos.')
        conn.execute('INSERT INTO costos_web(pedido_id,datos,responsable) VALUES(?,?,?)',(str(ident),json.dumps(data.model_dump(mode='json',exclude={'version','clave_operacion'})),person['nombre']))
        conn.execute('UPDATE pedidos_web SET version=version+1 WHERE id=?',(str(ident),))
        return save_action(conn,ident,data.clave_operacion,'costos',payload)


class Fulfill(Action):
    medio:Literal['efectivo','transferencia','mercado_pago']
    importe:Decimal=Field(ge=0,max_digits=14,decimal_places=2,allow_inf_nan=False)
    referencia:str=Field(min_length=3,max_length=150)
    cobro_verificado:Literal[True]


@router.post('/api/gestion/tienda/pedidos/{ident}/entrega')
def fulfill(ident:UUID,data:Fulfill,person=Depends(authorized)):
    payload=fingerprint(data)
    with database() as conn:
        conn.execute('BEGIN IMMEDIATE');expire(conn)
        previous=prior_action(conn,ident,data.clave_operacion,'entrega',payload)
        if previous:return previous
        row=get_order(conn,ident)
        if row['version']!=data.version or row['estado']!='confirmado':raise HTTPException(409,'La entrega requiere el importe vigente aprobado por el cliente.')
        if D(row['final'])!=data.importe:raise HTTPException(422,'El cobro verificado debe coincidir con el importe aprobado')
        for index,line in enumerate(json.loads(row['preparacion']),1):
            if not line.get('omitido'):
                stock.consume_sale(conn,line['producto_id'],D(line['cantidad']),str(ident),str(ident)+':'+str(index),'venta_web',person['nombre'],True,reservation_id=str(ident))
        conn.execute('DELETE FROM reservas_web WHERE pedido_id=?',(str(ident),))
        conn.execute("UPDATE pedidos_web SET estado='entregado',version=version+1,cobro=?,entregado_en=strftime('%Y-%m-%dT%H:%M:%fZ','now') WHERE id=?",(json.dumps({'medio':data.medio,'importe':money(data.importe),'referencia':data.referencia,'verificado_por':person['nombre']}),str(ident)))
        return save_action(conn,ident,data.clave_operacion,'entrega',payload)
