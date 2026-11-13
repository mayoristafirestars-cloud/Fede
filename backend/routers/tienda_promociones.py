"""Scheduled public prices, frozen order prices and explicit below-cost approval."""
import json
import time
from datetime import datetime,timezone
from decimal import Decimal
from uuid import UUID
from fastapi import APIRouter,Depends,HTTPException
from pydantic import Field,model_validator
from routers.preparacion import Model,database
from routers.comercial import authorized

router=APIRouter(tags=['Ofertas de Nativa'])
D=lambda value:Decimal(str(value))

def now():return time.time()

def regular_price(product):
    return D(product['venta_exacta'] if product['venta_exacta'] is not None else product['precio_venta'] or 0)

def reference_cost(product):
    for key in ('reposicion_exacta','promedio_exacto','precio_costo'):
        value=product[key]
        if value is not None and (key!='precio_costo' or D(value)>0):return D(value)
    return None

def effective_promotion(conn,product):
    base=regular_price(product)
    row=conn.execute('SELECT * FROM promociones_web WHERE producto_id=? AND activa=1 AND desde<=? AND hasta>? ORDER BY id DESC LIMIT 1',(product['id'],now(),now())).fetchone()
    if not row or row['unidad']!=product['unidad_venta'] or D(row['precio_referencia'])!=base or D(row['precio'])>=base:return None
    return {'id':row['id'],'titulo':row['titulo'],'precio_anterior':row['precio_referencia'],
            'desde':datetime.fromtimestamp(row['desde'],timezone.utc).isoformat(),
            'hasta':datetime.fromtimestamp(row['hasta'],timezone.utc).isoformat(),'precio':row['precio']}

class Promotion(Model):
    producto_id:int=Field(gt=0)
    titulo:str=Field(min_length=3,max_length=80)
    precio:Decimal=Field(gt=0,max_digits=14,decimal_places=4,allow_inf_nan=False)
    desde:datetime
    hasta:datetime
    motivo:str=Field(min_length=5,max_length=250)
    permitir_bajo_costo:bool=False
    clave_operacion:UUID
    @model_validator(mode='after')
    def valid_dates(self):
        if self.desde.tzinfo is None or self.hasta.tzinfo is None:raise ValueError('Las fechas requieren zona horaria')
        if self.hasta<=self.desde or (self.hasta-self.desde).total_seconds()>30*86400:raise ValueError('La promoción debe durar hasta 30 días y terminar después de iniciar')
        if self.hasta.timestamp()<=now():raise ValueError('La promoción debe terminar en el futuro')
        if self.desde.timestamp()<now()-300 or self.desde.timestamp()>now()+90*86400:raise ValueError('Elegí inicio actual o dentro de los próximos 90 días')
        return self

def view(conn,row):
    product=conn.execute('SELECT * FROM productos WHERE id=?',(row['producto_id'],)).fetchone()
    status='cancelada' if not row['activa'] else 'vencida' if row['hasta']<=now() else 'programada' if row['desde']>now() else 'vigente'
    if status in ('programada','vigente') and (not product['activo'] or product['unidad_venta']!=row['unidad'] or regular_price(product)!=D(row['precio_referencia'])):status='suspendida_por_cambio'
    return {'id':row['id'],'producto_id':row['producto_id'],'producto':product['descripcion'],'unidad':row['unidad'],
            'titulo':row['titulo'],'precio':row['precio'],'precio_referencia':row['precio_referencia'],
            'desde':datetime.fromtimestamp(row['desde'],timezone.utc).isoformat(),
            'hasta':datetime.fromtimestamp(row['hasta'],timezone.utc).isoformat(),'estado':status,
            'responsable':row['responsable'],'motivo':row['motivo'],'costo_referencia':row['costo_referencia'],
            'cancelada_por':row['cancelada_por'],'cancelada_en':row['cancelada_en']}

@router.get('/api/gestion/tienda/promociones')
def list_promotions(person=Depends(authorized)):
    with database() as conn:return [view(conn,row) for row in conn.execute('SELECT * FROM promociones_web ORDER BY id DESC LIMIT 200')]

@router.post('/api/gestion/tienda/promociones',status_code=201)
def create_promotion(data:Promotion,person=Depends(authorized)):
    from routers.tienda import offer
    payload=json.dumps(data.model_dump(mode='json'),sort_keys=True,separators=(',',':'))
    with database() as conn:
        conn.execute('BEGIN IMMEDIATE')
        previous=conn.execute('SELECT * FROM promociones_web WHERE clave=?',(str(data.clave_operacion),)).fetchone()
        if previous:
            if previous['payload']!=payload:raise HTTPException(409,'La clave ya fue usada para otra promoción')
            return view(conn,previous)
        product,_,photo,eligible=offer(conn,data.producto_id,False)
        if not eligible:raise HTTPException(422,'La oferta necesita un producto activo con foto y precio de venta')
        regular=regular_price(product)
        if data.precio>=regular:raise HTTPException(422,'La oferta debe ser menor al precio habitual actual')
        cost=reference_cost(product)
        if cost is not None and data.precio<cost and not(data.permitir_bajo_costo and person['rol']=='dueno'):
            raise HTTPException(422,'Precio por debajo del costo de referencia: requiere autorización expresa del dueño')
        if conn.execute('SELECT 1 FROM promociones_web WHERE producto_id=? AND activa=1 AND desde<? AND hasta>?',(data.producto_id,data.hasta.timestamp(),data.desde.timestamp())).fetchone():
            raise HTTPException(409,'Hay otra promoción que se superpone para este producto. Cancelala o elegí otras fechas.')
        ident=conn.execute('INSERT INTO promociones_web(producto_id,titulo,precio,precio_referencia,unidad,desde,hasta,responsable,motivo,costo_referencia,clave,payload) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)',
            (data.producto_id,data.titulo,str(data.precio),str(regular),product['unidad_venta'],data.desde.timestamp(),data.hasta.timestamp(),person['nombre'],data.motivo,str(cost) if cost is not None else None,str(data.clave_operacion),payload)).lastrowid
        return view(conn,conn.execute('SELECT * FROM promociones_web WHERE id=?',(ident,)).fetchone())

@router.delete('/api/gestion/tienda/promociones/{ident}')
def cancel_promotion(ident:int,person=Depends(authorized)):
    with database() as conn:
        conn.execute('BEGIN IMMEDIATE')
        row=conn.execute('SELECT * FROM promociones_web WHERE id=?',(ident,)).fetchone()
        if not row:raise HTTPException(404,'Promoción no encontrada')
        if row['activa']:conn.execute('UPDATE promociones_web SET activa=0,cancelada_por=?,cancelada_en=? WHERE id=?',(person['nombre'],now(),ident))
        return view(conn,conn.execute('SELECT * FROM promociones_web WHERE id=?',(ident,)).fetchone())
