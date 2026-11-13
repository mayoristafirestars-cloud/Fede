"""Supplier corrections, payable accounts and physical inventory (21–30)."""
import json
from datetime import date,datetime,timezone
from decimal import Decimal
from typing import Literal
from uuid import UUID
from fastapi import APIRouter,Depends,HTTPException,Query
from pydantic import Field,model_validator
from routers.preparacion import Model,database
from routers.comercial import authorized,fingerprint,Qty,PositiveQty,Money,require_quantity_unit
import stock

router=APIRouter(prefix='/api/inventario',tags=['Inventario y proveedores'])
D=stock.D
s=stock.s

class Operation(Model):
    clave_operacion: UUID

def run(kind,data,person,action):
    with database() as conn:
        conn.execute('BEGIN IMMEDIATE')
        key=str(data.clave_operacion)
        previous=conn.execute('SELECT * FROM operaciones_inventario WHERE clave=?',(key,)).fetchone()
        if previous:
            if previous['tipo']!=kind or previous['payload']!=fingerprint(data):
                raise HTTPException(409,'Esta operación ya fue registrada con otros datos. Actualizá la pantalla antes de continuar')
            return json.loads(previous['resultado'])
        result=action(conn,key,person['nombre'])
        conn.execute('INSERT INTO operaciones_inventario(clave,tipo,payload,resultado) VALUES(?,?,?,?)',(key,kind,fingerprint(data),json.dumps(result,ensure_ascii=False)))
        return result

def receipt(conn,ident):
    row=conn.execute('SELECT r.*,p.proveedor_id FROM recepciones_compra r JOIN pedidos_compra p ON p.id=r.pedido_id WHERE r.id=?',(ident,)).fetchone()
    if not row: raise HTTPException(404,'Recepción no encontrada')
    return row

def valid_lot_quantity(conn,ident,quantity):
    batch=stock.lot(conn,ident)
    require_quantity_unit(quantity,batch['unidad'])
    return batch

def account_balance(conn,receipt_id):
    return sum((D(r[0]) for r in conn.execute('SELECT importe FROM cuenta_proveedor WHERE recepcion_id=?',(receipt_id,))),Decimal(0))

@router.get('/ubicaciones')
def locations():
    with database() as conn:return [dict(r) for r in conn.execute('SELECT * FROM ubicaciones_stock ORDER BY id')]

@router.get('/resumen')
def summary():
    with database() as conn:
        products=[];batches=[]
        for p in conn.execute('SELECT * FROM productos ORDER BY descripcion,id').fetchall():
            stock.ensure_product(conn,p['id'])
            lots=[];available=Decimal(0);total=Decimal(0);places={};negative=False
            for row in conn.execute('SELECT l.*,pr.nombre proveedor FROM lotes_stock l LEFT JOIN proveedores pr ON pr.id=l.proveedor_id WHERE l.producto_id=? ORDER BY l.id',(p['id'],)).fetchall():
                batch=dict(row);batch['descripcion']=p['descripcion'];batch['codigo']=p['codigo']
                batch['existencias']=[dict(r) for r in conn.execute('SELECT e.*,u.nombre ubicacion,u.vendible FROM existencias_lote e JOIN ubicaciones_stock u ON u.id=e.ubicacion_id WHERE e.lote_id=? ORDER BY e.ubicacion_id',(row['id'],))]
                for e in batch['existencias']:
                    value=D(e['cantidad']);negative=negative or value<0;total+=value;places[e['ubicacion']]=places.get(e['ubicacion'],Decimal(0))+value
                    if e['vendible'] and row['estado']!='no_apto':available+=max(value,Decimal(0))
                batch['total']=s(sum((D(e['cantidad']) for e in batch['existencias']),Decimal(0)))
                batches.append(batch);lots.append(batch)
            if negative:available=Decimal(0)
            policy=conn.execute('SELECT * FROM politica_stock WHERE producto_id=?',(p['id'],)).fetchone()
            minimum=D(policy['minimo']) if policy else Decimal(0);days=policy['dias_sin_venta'] if policy else 7
            last=conn.execute("SELECT MAX(m.creado) FROM movimientos_stock m JOIN comprobantes c ON c.id=m.documento_id WHERE m.producto_id=? AND m.tipo='venta' AND c.estado!='anulado'",(p['id'],)).fetchone()[0]
            last_pos=conn.execute("SELECT MAX(v.creado) FROM ventas_pos v JOIN lineas_pos l ON l.venta_id=v.id WHERE l.producto_id=? AND v.estado NOT IN ('anulada','devuelta') AND CAST(l.cantidad AS REAL)>CAST(l.devuelto AS REAL)",(p['id'],)).fetchone()[0]
            last_web=conn.execute("SELECT MAX(m.creado) FROM movimientos_stock m JOIN pedidos_web w ON w.id=m.documento_id WHERE m.producto_id=? AND m.tipo='venta_web' AND w.estado='entregado'",(p['id'],)).fetchone()[0]
            last=max([d for d in (last,last_pos,last_web) if d],default=None)
            reserved=stock.reserved_web(conn,p['id'])
            free=max(Decimal(0),available-reserved)
            since=last or conn.execute("SELECT MIN(creado) FROM movimientos_stock WHERE producto_id=? AND tipo IN ('recepcion','apertura','ajuste_sobrante') AND CAST(cantidad AS REAL)>0",(p['id'],)).fetchone()[0]
            observed=max(0,(datetime.now(timezone.utc)-datetime.fromisoformat(since.replace('Z','+00:00'))).days) if since else 0
            products.append({'id':p['id'],'descripcion':p['descripcion'],'codigo':p['codigo'],'unidad':p['unidad_venta'],'activo':bool(p['activo']),'total':s(total),'vendible':s(available),'reservado_web':s(reserved),'libre_para_venta':s(free),'ubicaciones':{k:s(v) for k,v in places.items()},'minimo':s(minimum),'dias_sin_venta':days,'faltante':free<=minimum,'baja_rotacion':available>0 and since is not None and observed>=days,'dias_observados':observed,'ultima_venta':last,'negativo':negative,'descuadre':abs(total-D(p['stock']))>D('.000001')})
        return {'productos':products,'lotes':batches,'ubicaciones':[dict(r) for r in conn.execute('SELECT * FROM ubicaciones_stock ORDER BY id')]}

@router.get('/movimientos')
def movements(producto_id:int|None=None,offset:int=Query(default=0,ge=0),limit:int=Query(default=100,ge=1,le=500)):
    with database() as conn:
        where=' WHERE m.producto_id=?' if producto_id else ''
        args=[producto_id] if producto_id else []
        total=conn.execute('SELECT count(*) FROM movimientos_stock m'+where,args).fetchone()[0]
        rows=conn.execute('SELECT m.*,p.descripcion,u.nombre ubicacion FROM movimientos_stock m JOIN productos p ON p.id=m.producto_id JOIN ubicaciones_stock u ON u.id=m.ubicacion_id'+where+' ORDER BY m.id DESC LIMIT ? OFFSET ?',(*args,limit,offset)).fetchall()
        return {'total':total,'items':[dict(r) for r in rows]}

class Transfer(Operation):
    lote_id:int=Field(gt=0)
    origen_id:int=Field(gt=0)
    destino_id:int=Field(gt=0)
    cantidad:PositiveQty
    motivo:str=Field(min_length=3,max_length=500)

@router.post('/traslados',status_code=201)
def transfer(data:Transfer,person=Depends(authorized)):
    def action(conn,key,name):
        batch=valid_lot_quantity(conn,data.lote_id,data.cantidad);stock.require_consistent(conn,batch['producto_id'])
        if data.origen_id==data.destino_id:raise HTTPException(422,'Elegí dos ubicaciones distintas')
        stock.location(conn,data.destino_id)
        stock.move(conn,data.lote_id,data.origen_id,-data.cantidad,'traslado_salida','traslado:'+key+':s',name,data.motivo)
        stock.move(conn,data.lote_id,data.destino_id,data.cantidad,'traslado_entrada','traslado:'+key+':e',name,data.motivo)
        return {'ok':True,'lote_id':data.lote_id,'cantidad':s(data.cantidad)}
    return run('traslado',data,person,action)

class Departure(Operation):
    lote_id:int=Field(gt=0)
    ubicacion_id:int=Field(gt=0)
    cantidad:PositiveQty
    tipo:Literal['merma','regalo','consumo','donacion']
    causa:Literal['deterioro','deshidratacion','rotura','otro']='otro'
    motivo:str=Field(min_length=3,max_length=500)

@router.post('/salidas',status_code=201)
def departure(data:Departure,person=Depends(authorized)):
    def action(conn,key,name):
        batch=valid_lot_quantity(conn,data.lote_id,data.cantidad);stock.require_consistent(conn,batch['producto_id'])
        ident=stock.move(conn,data.lote_id,data.ubicacion_id,-data.cantidad,data.tipo,'salida:'+key,name,f'{data.causa}: {data.motivo}')
        stock.sync_product(conn,batch['producto_id'])
        return dict(conn.execute('SELECT * FROM movimientos_stock WHERE id=?',(ident,)).fetchone())
    return run('salida',data,person,action)

class Review(Operation):
    estado:Literal['verde','listo','maduro','revisar','no_apto']
    notas:str=Field(min_length=3,max_length=500)
    proxima_revision:date|None=None

@router.post('/lotes/{ident}/revision')
def review(ident:int,data:Review,person=Depends(authorized)):
    def action(conn,key,name):
        batch=stock.lot(conn,ident)
        conn.execute('INSERT INTO revisiones_lote(lote_id,anterior,estado,notas,proxima_revision,responsable) VALUES(?,?,?,?,?,?)',(ident,batch['estado'],data.estado,data.notas,str(data.proxima_revision) if data.proxima_revision else None,name))
        conn.execute('UPDATE lotes_stock SET estado=?,notas=?,proxima_revision=? WHERE id=?',(data.estado,data.notas,str(data.proxima_revision) if data.proxima_revision else None,ident))
        return dict(stock.lot(conn,ident))
    return run(f'revision:{ident}',data,person,action)

@router.get('/lotes/{ident}/revisiones')
def reviews(ident:int):
    with database() as conn:
        stock.lot(conn,ident)
        return [dict(r) for r in conn.execute('SELECT * FROM revisiones_lote WHERE lote_id=? ORDER BY id DESC',(ident,))]

class Count(Operation):
    lote_id:int|None=Field(default=None,gt=0)
    producto_id:int|None=Field(default=None,gt=0)
    ubicacion_id:int=Field(gt=0)
    cantidad:Qty
    version:int=Field(default=0,ge=0)
    motivo:str=Field(min_length=3,max_length=500)
    @model_validator(mode='after')
    def target(self):
        if (self.lote_id is None)==(self.producto_id is None):raise ValueError('Elegí un lote existente o un producto sin origen identificado')
        return self

@router.get('/conteos')
def counts():
    with database() as conn:return [dict(r) for r in conn.execute('SELECT c.*,p.descripcion,l.unidad,u.nombre ubicacion FROM conteos_stock c JOIN lotes_stock l ON l.id=c.lote_id JOIN productos p ON p.id=l.producto_id JOIN ubicaciones_stock u ON u.id=c.ubicacion_id ORDER BY c.id DESC')]

@router.post('/conteos',status_code=201)
def count(data:Count,person=Depends(authorized)):
    def action(conn,key,name):
        stock.location(conn,data.ubicacion_id)
        ident=data.lote_id
        if ident is None:
            stock.ensure_product(conn,data.producto_id)
            p=conn.execute('SELECT * FROM productos WHERE id=?',(data.producto_id,)).fetchone()
            ident=conn.execute("INSERT INTO lotes_stock(producto_id,origen,unidad,estado,notas) VALUES(?,'conteo_sin_origen',?,'revisar','Mercadería encontrada sin origen de compra confirmado')",(p['id'],p['unidad_venta'])).lastrowid
        batch=valid_lot_quantity(conn,ident,data.cantidad)
        current=stock.balance(conn,ident,data.ubicacion_id)
        if current['version']!=data.version:raise HTTPException(409,'El stock cambió desde que abriste el conteo. Actualizá y volvé a contar')
        row=conn.execute('INSERT INTO conteos_stock(lote_id,ubicacion_id,esperado,contado,version,motivo,responsable) VALUES(?,?,?,?,?,?,?)',(ident,data.ubicacion_id,current['cantidad'],s(data.cantidad),current['version'],data.motivo,name)).lastrowid
        return dict(conn.execute('SELECT * FROM conteos_stock WHERE id=?',(row,)).fetchone())
    return run('conteo',data,person,action)

@router.post('/conteos/{ident}/aprobar')
def approve_count(ident:int,data:Operation,person=Depends(authorized)):
    def action(conn,key,name):
        row=conn.execute('SELECT * FROM conteos_stock WHERE id=?',(ident,)).fetchone()
        if not row:raise HTTPException(404,'Conteo no encontrado')
        if row['estado']!='pendiente':raise HTTPException(409,'El conteo ya fue aprobado')
        current=stock.balance(conn,row['lote_id'],row['ubicacion_id'])
        if current['version']!=row['version']:raise HTTPException(409,'Hubo movimientos después del conteo. Hacé un nuevo conteo; no se sobrescribe el stock actual')
        delta=D(row['contado'])-D(row['esperado'])
        if delta:
            stock.move(conn,row['lote_id'],row['ubicacion_id'],delta,'ajuste_sobrante' if delta>0 else 'ajuste_faltante','conteo:'+str(ident),name,row['motivo'],ident)
        stock.sync_product(conn,stock.lot(conn,row['lote_id'])['producto_id'])
        conn.execute("UPDATE conteos_stock SET estado='aprobado',aprobador=?,aprobado=strftime('%Y-%m-%dT%H:%M:%fZ','now') WHERE id=?",(name,ident))
        return {'id':ident,'estado':'aprobado','diferencia':s(delta)}
    return run(f'aprobar:{ident}',data,person,action)

class Policy(Model):
    minimo:Qty=Decimal(0)
    dias_sin_venta:int=Field(default=7,ge=1,le=365)

@router.put('/productos/{ident}/alertas')
def policy(ident:int,data:Policy,person=Depends(authorized)):
    with database() as conn:
        p=conn.execute('SELECT unidad_venta FROM productos WHERE id=?',(ident,)).fetchone()
        if not p:raise HTTPException(404,'Producto no encontrado')
        require_quantity_unit(data.minimo,p[0])
        conn.execute('INSERT INTO politica_stock VALUES(?,?,?) ON CONFLICT(producto_id) DO UPDATE SET minimo=excluded.minimo,dias_sin_venta=excluded.dias_sin_venta',(ident,s(data.minimo),data.dias_sin_venta))
    return data.model_dump(mode='json')

class Return(Operation):
    lote_id:int=Field(gt=0)
    ubicacion_id:int=Field(gt=0)
    cantidad:PositiveQty
    motivo:str=Field(min_length=3,max_length=500)

@router.post('/devoluciones',status_code=201)
def supplier_return(data:Return,person=Depends(authorized)):
    def action(conn,key,name):
        batch=valid_lot_quantity(conn,data.lote_id,data.cantidad);stock.require_consistent(conn,batch['producto_id'])
        if not batch['recepcion_id']:raise HTTPException(422,'Este lote no tiene una recepción de proveedor identificada. Confirmá su origen antes de devolverlo')
        source=json.loads(receipt(conn,batch['recepcion_id'])['datos'])
        accepted=next(D(i['aceptado']) for i in source['lineas'] if i['linea_id']==batch['linea_id'])
        returned=sum((D(r[0]) for r in conn.execute('SELECT cantidad FROM devoluciones_proveedor WHERE lote_id=?',(batch['id'],))),Decimal(0))
        if data.cantidad+returned>accepted:raise HTTPException(409,'La devolución supera lo aceptado originalmente de ese lote')
        ident=conn.execute('INSERT INTO devoluciones_proveedor(lote_id,ubicacion_id,recepcion_id,proveedor_id,cantidad,motivo,responsable) VALUES(?,?,?,?,?,?,?)',(batch['id'],data.ubicacion_id,batch['recepcion_id'],batch['proveedor_id'],s(data.cantidad),data.motivo,name)).lastrowid
        stock.move(conn,batch['id'],data.ubicacion_id,-data.cantidad,'devolucion_proveedor','devolucion:'+str(ident),name,data.motivo,ident)
        stock.sync_product(conn,batch['producto_id'])
        return {'id':ident,'recepcion_id':batch['recepcion_id'],'cantidad':s(data.cantidad),'credito_registrado':False}
    return run('devolucion',data,person,action)

@router.get('/devoluciones')
def returns():
    with database() as conn:return [dict(r) for r in conn.execute('SELECT d.*,p.descripcion,l.unidad,pr.nombre proveedor FROM devoluciones_proveedor d JOIN lotes_stock l ON l.id=d.lote_id JOIN productos p ON p.id=l.producto_id JOIN proveedores pr ON pr.id=d.proveedor_id ORDER BY d.id DESC')]

class Claim(Operation):
    recepcion_id:int=Field(gt=0)
    tipo:Literal['calidad','faltante','precio','otro']
    detalle:str=Field(min_length=3,max_length=1000)

@router.post('/reclamos',status_code=201)
def create_claim(data:Claim,person=Depends(authorized)):
    def action(conn,key,name):
        row=receipt(conn,data.recepcion_id)
        ident=conn.execute('INSERT INTO reclamos_proveedor(recepcion_id,proveedor_id,tipo,detalle,responsable) VALUES(?,?,?,?,?)',(data.recepcion_id,row['proveedor_id'],data.tipo,data.detalle,name)).lastrowid
        return {'id':ident,'estado':'abierto'}
    return run('reclamo',data,person,action)

class ClaimEvent(Operation):
    estado:Literal['abierto','en_gestion','resuelto','rechazado']
    nota:str=Field(min_length=3,max_length=1000)

@router.post('/reclamos/{ident}/eventos')
def claim_event(ident:int,data:ClaimEvent,person=Depends(authorized)):
    def action(conn,key,name):
        if not conn.execute('SELECT 1 FROM reclamos_proveedor WHERE id=?',(ident,)).fetchone():raise HTTPException(404,'Reclamo no encontrado')
        conn.execute('INSERT INTO eventos_reclamo(reclamo_id,estado,nota,responsable) VALUES(?,?,?,?)',(ident,data.estado,data.nota,name))
        conn.execute('UPDATE reclamos_proveedor SET estado=? WHERE id=?',(data.estado,ident))
        return {'id':ident,'estado':data.estado}
    return run(f'reclamo_evento:{ident}',data,person,action)

@router.get('/reclamos')
def claims():
    with database() as conn:
        rows=[dict(r) for r in conn.execute('SELECT r.*,p.nombre proveedor FROM reclamos_proveedor r JOIN proveedores p ON p.id=r.proveedor_id ORDER BY r.id DESC')]
        for row in rows:row['eventos']=[dict(r) for r in conn.execute('SELECT * FROM eventos_reclamo WHERE reclamo_id=? ORDER BY id',(row['id'],))]
        return rows

@router.get('/cuentas')
def accounts():
    with database() as conn:
        result=[]
        for supplier in conn.execute('SELECT id,nombre FROM proveedores ORDER BY nombre').fetchall():
            entries=[dict(r) for r in conn.execute('SELECT c.*,EXISTS(SELECT 1 FROM cuenta_proveedor x WHERE x.reversa_de=c.id) revertido FROM cuenta_proveedor c WHERE proveedor_id=? ORDER BY id DESC',(supplier['id'],))]
            docs=[]
            for entry in entries:
                if entry['tipo']=='cargo':
                    amount=account_balance(conn,entry['recepcion_id'])
                    docs.append({'recepcion_id':entry['recepcion_id'],'referencia':entry['referencia'],'cargo':entry['importe'],'saldo':s(amount),'vencimiento':entry['vencimiento'],'vencido':bool(amount>0 and entry['vencimiento']<str(stock.today()))})
            result.append({**dict(supplier),'saldo':s(sum((D(e['importe']) for e in entries),Decimal(0))),'documentos':docs,'movimientos':entries})
        return result

class AccountEntry(Operation):
    recepcion_id:int=Field(gt=0)
    tipo:Literal['pago','credito','reintegro']
    importe:Money=Field(gt=0)
    referencia:str=Field(min_length=3,max_length=200)
    motivo:str=Field(min_length=3,max_length=500)
    fecha:date|None=None
    medio:Literal['efectivo','transferencia','cheque','otro']='transferencia'
    confirmado:Literal[True]
    devolucion_id:int|None=Field(default=None,gt=0)
    reclamo_id:int|None=Field(default=None,gt=0)

@router.post('/cuentas/movimientos',status_code=201)
def account_entry(data:AccountEntry,person=Depends(authorized)):
    def action(conn,key,name):
        row=receipt(conn,data.recepcion_id);balance=account_balance(conn,data.recepcion_id)
        effective=data.fecha or stock.today()
        if effective>stock.today():raise HTTPException(422,'La fecha de una operación confirmada no puede ser futura')
        if data.tipo=='pago' and data.importe>balance:raise HTTPException(409,'El pago supera la deuda pendiente de esa recepción')
        if data.tipo=='reintegro' and data.importe>max(-balance,Decimal(0)):raise HTTPException(409,'El reintegro supera el saldo a favor de esa recepción')
        if data.tipo=='credito':
            charge=sum((D(r[0]) for r in conn.execute("SELECT importe FROM cuenta_proveedor WHERE recepcion_id=? AND tipo='cargo'",(data.recepcion_id,))),Decimal(0))
            credited=sum((-D(r[0]) for r in conn.execute("SELECT c.importe FROM cuenta_proveedor c WHERE c.recepcion_id=? AND c.tipo='credito' AND NOT EXISTS(SELECT 1 FROM cuenta_proveedor x WHERE x.reversa_de=c.id)",(data.recepcion_id,))),Decimal(0))
            if data.importe+credited>charge:raise HTTPException(409,'Los créditos superan el cargo original. Revisá los documentos del proveedor')
        for ident,table in [(data.devolucion_id,'devoluciones_proveedor'),(data.reclamo_id,'reclamos_proveedor')]:
            if ident:
                linked=conn.execute(f'SELECT recepcion_id FROM {table} WHERE id=?',(ident,)).fetchone()
                if not linked or linked[0]!=data.recepcion_id:raise HTTPException(422,'La devolución o reclamo no pertenece a esta recepción')
        signed=data.importe if data.tipo=='reintegro' else -data.importe
        ident=conn.execute('INSERT INTO cuenta_proveedor(proveedor_id,recepcion_id,tipo,importe,referencia,motivo,responsable,fecha,medio,devolucion_id,reclamo_id,origen_clave) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)',(row['proveedor_id'],data.recepcion_id,data.tipo,s(signed),data.referencia,data.motivo,name,str(effective),data.medio,data.devolucion_id,data.reclamo_id,'cuenta:'+key)).lastrowid
        return {'id':ident,'saldo_recepcion':s(account_balance(conn,data.recepcion_id))}
    return run('cuenta',data,person,action)

class Reversal(Operation):
    motivo:str=Field(min_length=3,max_length=500)

@router.post('/cuentas/movimientos/{ident}/revertir')
def reverse_entry(ident:int,data:Reversal,person=Depends(authorized)):
    def action(conn,key,name):
        row=conn.execute('SELECT * FROM cuenta_proveedor WHERE id=?',(ident,)).fetchone()
        if not row:raise HTTPException(404,'Movimiento de cuenta no encontrado')
        if row['tipo'] not in ('pago','credito','reintegro'):raise HTTPException(422,'Solo se pueden revertir pagos, créditos y reintegros')
        if conn.execute('SELECT 1 FROM cuenta_proveedor WHERE reversa_de=?',(ident,)).fetchone():raise HTTPException(409,'El movimiento ya fue revertido')
        new=conn.execute("INSERT INTO cuenta_proveedor(proveedor_id,recepcion_id,tipo,importe,referencia,motivo,responsable,fecha,reversa_de,origen_clave) VALUES(?,?,'reversion',?,?,?,?,?,?,?)",(row['proveedor_id'],row['recepcion_id'],s(-D(row['importe'])),f'Reversión #{ident}',data.motivo,name,str(stock.today()),ident,'reversion:'+key)).lastrowid
        return {'id':new,'saldo_recepcion':s(account_balance(conn,row['recepcion_id']))}
    return run(f'reversion:{ident}',data,person,action)
