"""Roadmap 31–40: replenishment, returnable crates and retail counter."""
import json,time
from datetime import timedelta,datetime,timezone
from decimal import Decimal,ROUND_CEILING
from typing import Literal
from uuid import UUID,uuid4
from fastapi import APIRouter,Cookie,Depends,HTTPException,Query
from pydantic import Field,model_validator
from routers.preparacion import Model,database,clave
from routers.comercial import actor,authorized,fingerprint,Qty,PositiveQty,Money,allocate_expenses,require_quantity_unit,financial
import stock
from document_photos import safe_photo,effective_photo

router=APIRouter(prefix='/api/mostrador',tags=['Mostrador y reposición'])
D=stock.D
s=stock.s

def operator(cs_sesion:str|None=Cookie(default=None)):
    with database() as conn:return actor(conn,cs_sesion)

class Operation(Model):
    clave_operacion:UUID

def run(kind,data,person,action):
    with database() as conn:
        conn.execute('BEGIN IMMEDIATE')
        old=conn.execute('SELECT * FROM operaciones_mostrador WHERE clave=?',(str(data.clave_operacion),)).fetchone()
        if old:
            if old['tipo']!=kind or old['payload']!=fingerprint(data):raise HTTPException(409,'La operación ya fue registrada con otros datos')
            return json.loads(old['resultado'])
        result=action(conn,str(data.clave_operacion))
        conn.execute('INSERT INTO operaciones_mostrador(clave,tipo,payload,resultado) VALUES(?,?,?,?)',(str(data.clave_operacion),kind,fingerprint(data),json.dumps(result,ensure_ascii=False)))
        return result

def product(conn,ident):
    row=conn.execute('SELECT * FROM productos WHERE id=? AND activo=1',(ident,)).fetchone()
    if not row:raise HTTPException(422,'Producto inexistente o inactivo')
    return row

def available(conn,ident):
    stock.ensure_product(conn,ident)
    rows=conn.execute('SELECT e.cantidad,l.estado,u.vendible FROM existencias_lote e JOIN lotes_stock l ON l.id=e.lote_id JOIN ubicaciones_stock u ON u.id=e.ubicacion_id WHERE l.producto_id=?',(ident,)).fetchall()
    if any(D(r['cantidad'])<0 for r in rows):return Decimal(0)
    return max(Decimal(0),sum((D(r['cantidad']) for r in rows if r['vendible'] and r['estado']!='no_apto'),Decimal(0))-stock.reserved_web(conn,ident))

@router.get('/catalogo')
def catalog(buscar:str=Query(default='',max_length=160),person=Depends(operator)):
    with database() as conn:
        favorites={r[0] for r in conn.execute('SELECT producto_id FROM favoritos_pos WHERE responsable_id=?',(person['id'],))}
        items=[]
        for p in conn.execute('SELECT * FROM productos WHERE activo=1 ORDER BY descripcion,id').fetchall():
            aliases=[r[0] for r in conn.execute("SELECT valor FROM identificadores_producto WHERE producto_id=? AND tipo='alias'",(p['id'],))]
            description=' · '.join(filter(None,[p['descripcion'],p['variedad'],p['calidad'],p['presentacion']]))
            if clave(buscar.strip()) not in clave(' '.join([description,p['codigo'],*aliases])):continue
            f=financial(conn,p)
            items.append({'id':p['id'],'descripcion':description,'codigo':p['codigo'],'unidad':p['unidad_venta'],'foto':p['foto'],'precio':f['precio'],'vendible':s(available(conn,p['id'])),'favorito':p['id'] in favorites,'aliases':aliases})
        return items

@router.put('/favoritos/{ident}')
def favorite(ident:int,activo:bool=True,person=Depends(operator)):
    with database() as conn:
        product(conn,ident)
        if activo:conn.execute('INSERT OR IGNORE INTO favoritos_pos VALUES(?,?)',(person['id'],ident))
        else:conn.execute('DELETE FROM favoritos_pos WHERE responsable_id=? AND producto_id=?',(person['id'],ident))
    return {'ok':True}

@router.get('/balanza')
def scale_status():
    with database() as conn:row=conn.execute('SELECT datos FROM configuracion_negocio WHERE id=1').fetchone()
    devices=json.loads(row[0]).get('equipos',[]) if row else []
    scales=[e for e in devices if e['tipo']=='balanza']
    identified=next((e['marca_modelo'] for e in scales if e.get('marca_modelo')),'')
    return {'modo':'manual','integrada':False,'estado':f'{identified}: variante, conexión y protocolo por verificar' if identified else 'Pendiente de identificar modelo y probar protocolo','modelo_identificado':identified,'equipos':scales}

class BarcodeRule(Model):
    nombre:str=Field(min_length=1,max_length=100)
    prefijo:str=Field(min_length=1,max_length=4,pattern=r'^[0-9]+$')
    codigo_desde:int=Field(ge=1,le=12)
    codigo_largo:int=Field(ge=1,le=10)
    valor_desde:int=Field(ge=1,le=12)
    valor_largo:int=Field(ge=1,le=10)
    decimales:int=Field(ge=0,le=3)
    tipo:Literal['peso','importe']='peso'
    unidad_peso:Literal['kg','g']='kg'
    activo:bool=True
    @model_validator(mode='after')
    def segments(self):
        code=set(range(self.codigo_desde,self.codigo_desde+self.codigo_largo));value=set(range(self.valor_desde,self.valor_desde+self.valor_largo))
        if max(code|value)>12 or min(code|value)<=len(self.prefijo) or code&value:raise ValueError('Los campos no deben superponerse, tocar el prefijo ni el dígito verificador (posición 13)')
        if self.tipo=='importe' and self.decimales>2:raise ValueError('El importe admite hasta dos decimales')
        return self

@router.get('/etiquetas/reglas')
def rules():
    with database() as conn:return [dict(r) for r in conn.execute('SELECT * FROM reglas_peso ORDER BY id')]

@router.post('/etiquetas/reglas',status_code=201)
def create_rule(data:BarcodeRule,person=Depends(authorized)):
    with database() as conn:
        conn.execute('BEGIN IMMEDIATE')
        for r in conn.execute('SELECT prefijo FROM reglas_peso'):
            if r[0].startswith(data.prefijo) or data.prefijo.startswith(r[0]):raise HTTPException(409,'El prefijo se superpone con una regla existente')
        fields=data.model_dump()
        ident=conn.execute(f"INSERT INTO reglas_peso({','.join(fields)}) VALUES({','.join('?' for _ in fields)})",tuple(fields.values())).lastrowid
    return {'id':ident,**fields}

@router.put('/etiquetas/reglas/{ident}')
def edit_rule(ident:int,data:BarcodeRule,person=Depends(authorized)):
    with database() as conn:
        conn.execute('BEGIN IMMEDIATE')
        if not conn.execute('SELECT 1 FROM reglas_peso WHERE id=?',(ident,)).fetchone():raise HTTPException(404,'Regla no encontrada')
        for row in conn.execute('SELECT id,prefijo FROM reglas_peso WHERE id!=?',(ident,)):
            if row['prefijo'].startswith(data.prefijo) or data.prefijo.startswith(row['prefijo']):raise HTTPException(409,'El prefijo se superpone con otra regla')
        fields=data.model_dump()
        conn.execute(f"UPDATE reglas_peso SET {','.join(f'{k}=?' for k in fields)} WHERE id=?",(*fields.values(),ident))
    return {'id':ident,**fields}

def decode(conn,code):
    rule=next((r for r in conn.execute('SELECT * FROM reglas_peso WHERE activo=1') if len(code)==13 and code.startswith(r['prefijo'])),None)
    if rule:
        if len(code)!=13 or not code.isascii() or not code.isdigit():raise HTTPException(422,'La etiqueta configurada debe tener 13 dígitos')
        expected=(10-sum(int(c)*(1 if i%2==0 else 3) for i,c in enumerate(code[:12]))%10)%10
        if expected!=int(code[-1]):raise HTTPException(422,'El dígito verificador de la etiqueta no es válido')
        plu=code[rule['codigo_desde']-1:rule['codigo_desde']-1+rule['codigo_largo']]
        candidates=[plu,plu.lstrip('0') or '0']
        p=None
        for candidate in candidates:
            p=conn.execute('SELECT p.* FROM productos p LEFT JOIN identificadores_producto i ON i.producto_id=p.id WHERE p.activo=1 AND (lower(p.codigo)=? OR i.clave=?) LIMIT 1',(candidate,clave(candidate))).fetchone()
            if p:break
        if not p:raise HTTPException(422,'El PLU de la etiqueta no identifica un producto activo')
        value=D(code[rule['valor_desde']-1:rule['valor_desde']-1+rule['valor_largo']])/(10**rule['decimales'])
        if value<=0:raise HTTPException(422,'La etiqueta tiene un peso o importe cero')
        if rule['tipo']=='importe':return {'tipo':'importe','producto_id':p['id'],'importe':s(value),'requiere_peso':True,'mensaje':'La etiqueta solo contiene importe. Falta el peso real; no se inventa una cantidad para descontar stock.'}
        if p['unidad_venta'] not in ('kg','g'):raise HTTPException(422,'La etiqueta de peso corresponde a un producto que no se vende por peso')
        qty=value*(1000 if rule['unidad_peso']=='kg' and p['unidad_venta']=='g' else D('.001') if rule['unidad_peso']=='g' and p['unidad_venta']=='kg' else 1)
        if qty!=qty.quantize(D('.001')):raise HTTPException(422,'El peso de la etiqueta excede la precisión de la unidad del catálogo')
        return {'tipo':'peso','producto_id':p['id'],'cantidad':s(qty),'regla_id':rule['id'],'unidad':p['unidad_venta'],'configuracion':dict(rule)}
    p=conn.execute('SELECT p.id FROM productos p LEFT JOIN identificadores_producto i ON i.producto_id=p.id WHERE p.activo=1 AND (lower(p.codigo)=? OR i.clave=?) LIMIT 1',(code.lower(),clave(code))).fetchone()
    if not p:raise HTTPException(404,'Código no encontrado; configurá el formato real si es una etiqueta de peso')
    return {'tipo':'producto','producto_id':p['id']}

class Barcode(Model):
    codigo:str=Field(min_length=1,max_length=80)

@router.post('/resolver-codigo')
def resolve_code(data:Barcode,person=Depends(operator)):
    with database() as conn:return decode(conn,data.codigo)

class SaleLine(Model):
    producto_id:int=Field(gt=0)
    cantidad:PositiveQty|None=None
    bruto_kg:Qty|None=None
    tara_kg:Qty|None=None
    etiqueta:str|None=Field(default=None,min_length=1,max_length=80)

class Cart(Model):
    lineas:list[SaleLine]=Field(min_length=1,max_length=100)
    descuento:Decimal=Field(default=0,ge=0,le=100,max_digits=5,decimal_places=2,allow_inf_nan=False)
    motivo_descuento:str=Field(default='',max_length=300)

def sale_line(conn,line):
    p=product(conn,line.producto_id)
    label=None
    if line.etiqueta:
        if any(v is not None for v in [line.cantidad,line.bruto_kg,line.tara_kg]):raise HTTPException(422,'Usá una etiqueta o ingreso manual, sin mezclar cantidades')
        label=decode(conn,line.etiqueta)
        if label['tipo']!='peso' or label['producto_id']!=p['id']:raise HTTPException(422,'La etiqueta no contiene el peso de este producto; cargá la pesada real por separado')
        qty=D(label['cantidad']);origin='etiqueta'
    elif p['unidad_venta'] in ('kg','g'):
        if line.cantidad is not None or line.bruto_kg is None or line.tara_kg is None:raise HTTPException(422,'Ingresá peso bruto y tara en kg para este producto')
        qty=(line.bruto_kg-line.tara_kg)*(1000 if p['unidad_venta']=='g' else 1);origin='pesaje_manual'
    else:
        if line.cantidad is None or line.bruto_kg is not None or line.tara_kg is not None:raise HTTPException(422,'Ingresá cantidad de unidades, sin datos de pesaje')
        qty=line.cantidad;origin='cantidad_manual'
    require_quantity_unit(qty,p['unidad_venta'])
    if qty<=0 or qty>D('99999999999') or qty!=qty.quantize(D('.001')):raise HTTPException(422,'La cantidad neta debe ser positiva y tener hasta tres decimales')
    f=financial(conn,p)
    if f['precio'] is None:raise HTTPException(422,'Falta registrar el precio de venta de '+p['descripcion'])
    return {'producto_id':p['id'],'descripcion':' · '.join(filter(None,[p['descripcion'],p['variedad'],p['calidad'],p['presentacion']])),'unidad':p['unidad_venta'],'cantidad':s(qty),'precio':f['precio'],'version_precio':f['version_precio'],'bruto':s(stock.money(qty*D(f['precio']))),'origen':origin,'entrada':line.model_dump(mode='json'),'lectura_etiqueta':label}

@router.post('/pesaje')
def weigh(data:SaleLine,person=Depends(operator)):
    with database() as conn:return sale_line(conn,data)

@router.post('/cotizar')
def quote(data:Cart,person=Depends(operator)):
    if data.descuento and person['rol'] not in ('dueno','encargado'):raise HTTPException(403,'El descuento requiere autorización de dueño o encargada')
    if data.descuento and len(data.motivo_descuento)<3:raise HTTPException(422,'Indicá el motivo del descuento')
    with database() as conn:
        lines=[sale_line(conn,line) for line in data.lineas]
        subtotal=sum((D(l['bruto']) for l in lines),Decimal(0));discount=stock.money(subtotal*data.descuento/100)
        allocated=allocate_expenses(discount,[D(l['bruto']) for l in lines])
        for line,amount in zip(lines,allocated):line.update(descuento=s(amount),neto=s(D(line['bruto'])-amount))
        result={'id':str(uuid4()),'lineas':lines,'subtotal':s(subtotal),'descuento':s(discount),'total':s(subtotal-discount),'porcentaje':s(data.descuento),'motivo_descuento':data.motivo_descuento}
        conn.execute('DELETE FROM cotizaciones_pos WHERE vence<? AND id NOT IN (SELECT cotizacion_id FROM ventas_pos)',(time.time(),))
        conn.execute('INSERT INTO cotizaciones_pos VALUES(?,?,?,?)',(result['id'],json.dumps(result,ensure_ascii=False),person['id'],time.time()+300))
        return result

def sale_detail(conn,ident):
    row=conn.execute('SELECT * FROM ventas_pos WHERE id=?',(ident,)).fetchone()
    if not row:raise HTTPException(404,'Venta no encontrada')
    result=dict(row);result['numero']=f'V-{ident:06}'
    result['lineas']=[dict(r) for r in conn.execute('SELECT * FROM lineas_pos WHERE venta_id=? ORDER BY id',(ident,))]
    for line in result['lineas']:line['foto']=effective_photo(conn,'pos',line['id'],line['foto'])
    result['correcciones']=[dict(r) for r in conn.execute('SELECT * FROM correcciones_pos WHERE venta_id=? ORDER BY id',(ident,))]
    result['importe_corregido']=s(sum((D(r['importe']) for r in result['correcciones']),Decimal(0)))
    return result

class Confirm(Operation):
    cotizacion_id:UUID

@router.post('/ventas',status_code=201)
def confirm(data:Confirm,person=Depends(operator)):
    def action(conn,key):
        row=conn.execute('SELECT * FROM cotizaciones_pos WHERE id=?',(str(data.cotizacion_id),)).fetchone()
        if not row or row['vence']<time.time():raise HTTPException(409,'La cotización venció. Volvé a calcular antes de registrar')
        if row['responsable_id']!=person['id']:raise HTTPException(409,'La autorización cambió. Volvé a cotizar con el responsable actual')
        if conn.execute('SELECT 1 FROM ventas_pos WHERE cotizacion_id=?',(str(data.cotizacion_id),)).fetchone():raise HTTPException(409,'Esta cotización ya fue registrada como venta')
        quoted=json.loads(row['datos'])
        if D(quoted['porcentaje']) and person['rol'] not in ('dueno','encargado'):raise HTTPException(403,'Descuento sin autorización')
        for line in quoted['lineas']:
            now=financial(conn,product(conn,line['producto_id']))
            if now['version_precio']!=line['version_precio'] or now['precio'] is None or D(now['precio'])!=D(line['precio']):raise HTTPException(409,'Cambió un precio. Volvé a cotizar para revisar el total')
        ident=conn.execute('INSERT INTO ventas_pos(cotizacion_id,responsable,subtotal,descuento,total,porcentaje,motivo_descuento) VALUES(?,?,?,?,?,?,?)',(str(data.cotizacion_id),person['nombre'],quoted['subtotal'],quoted['descuento'],quoted['total'],quoted['porcentaje'],quoted['motivo_descuento'])).lastrowid
        for line in quoted['lineas']:
            lid=conn.execute('INSERT INTO lineas_pos(venta_id,producto_id,descripcion,unidad,cantidad,precio,bruto,descuento,neto,datos) VALUES(?,?,?,?,?,?,?,?,?,?)',(ident,line['producto_id'],line['descripcion'],line['unidad'],line['cantidad'],line['precio'],line['bruto'],line['descuento'],line['neto'],json.dumps(line,ensure_ascii=False))).lastrowid
            image=conn.execute('SELECT foto FROM productos WHERE id=?',(line['producto_id'],)).fetchone()[0]
            conn.execute('UPDATE lineas_pos SET foto=? WHERE id=?',(safe_photo(image),lid))
            stock.consume_sale(conn,line['producto_id'],D(line['cantidad']),ident,lid,'venta_pos',person['nombre'],True)
        return sale_detail(conn,ident)
    return run('venta',data,person,action)

@router.get('/ventas')
def sales(limit:int=Query(default=50,ge=1,le=200),offset:int=Query(default=0,ge=0),person=Depends(operator)):
    with database() as conn:return [sale_detail(conn,r[0]) for r in conn.execute('SELECT id FROM ventas_pos ORDER BY id DESC LIMIT ? OFFSET ?',(limit,offset)).fetchall()]

class ReturnLine(Model):
    linea_id:int=Field(gt=0)
    cantidad:PositiveQty

class Correction(Operation):
    tipo:Literal['devolucion','anulacion']
    motivo:str=Field(min_length=3,max_length=500)
    destino:Literal['cuarentena','descarte']='cuarentena'
    lineas:list[ReturnLine]=Field(default_factory=list,max_length=100)
    @model_validator(mode='after')
    def valid_lines(self):
        if len({l.linea_id for l in self.lineas})!=len(self.lineas):raise ValueError('No repetir líneas de devolución')
        if self.tipo=='devolucion' and not self.lineas:raise ValueError('Seleccioná al menos una línea a devolver')
        if self.tipo=='anulacion' and self.lineas:raise ValueError('La anulación toma todas las cantidades pendientes')
        return self

@router.post('/ventas/{ident}/correcciones',status_code=201)
def correct_sale(ident:int,data:Correction,person=Depends(authorized)):
    def action(conn,key):
        sale=sale_detail(conn,ident)
        if sale['estado'] in ('anulada','devuelta'):raise HTTPException(409,'La venta ya fue corregida completamente')
        lines={l['id']:l for l in sale['lineas']}
        desired=[ReturnLine(linea_id=l['id'],cantidad=D(l['cantidad'])-D(l['devuelto'])) for l in lines.values() if D(l['cantidad'])>D(l['devuelto'])] if data.tipo=='anulacion' else data.lineas
        correction=conn.execute('INSERT INTO correcciones_pos(venta_id,tipo,motivo,destino,importe,responsable) VALUES(?,?,?,?,?,?)',(ident,data.tipo,data.motivo,data.destino,'0',person['nombre'])).lastrowid
        refund=Decimal(0)
        for request in desired:
            line=lines.get(request.linea_id)
            if not line:raise HTTPException(422,'La línea no pertenece a esta venta')
            require_quantity_unit(request.cantidad,line['unidad'])
            total_returned=D(line['devuelto'])+request.cantidad
            if total_returned>D(line['cantidad']):raise HTTPException(409,'La devolución supera la cantidad pendiente de esa línea')
            amount=stock.money(D(line['neto'])*total_returned/D(line['cantidad']))-D(line['reintegro']);refund+=amount
            # Replay source allocation in sale order; original lot cost stays attached.
            allocations=conn.execute("SELECT * FROM movimientos_stock WHERE tipo='venta_pos' AND origen_clave LIKE ? ORDER BY id",(f'venta_pos:{line["id"]}:%',)).fetchall()
            skip=D(line['devuelto']);remaining=request.cantidad
            for origin in allocations:
                allocated=-D(origin['cantidad'])
                if skip>=allocated:skip-=allocated;continue
                take=min(remaining,allocated-skip);skip=Decimal(0)
                stock.require_consistent(conn,line['producto_id'])
                stem=f'cliente:{correction}:{line["id"]}:{origin["id"]}'
                stock.move(conn,origin['lote_id'],4,take,'devolucion_cliente',stem+':e',person['nombre'],data.motivo,correction,True)
                if data.destino=='descarte':stock.move(conn,origin['lote_id'],4,-take,'merma_devolucion',stem+':s',person['nombre'],data.motivo,correction,True)
                stock.sync_product(conn,line['producto_id']);remaining-=take
                if remaining==0:break
            if remaining:raise HTTPException(409,'No se pudo reconstruir el origen de stock de la venta')
            conn.execute('UPDATE lineas_pos SET devuelto=?,reintegro=? WHERE id=?',(s(total_returned),s(D(line['reintegro'])+amount),line['id']))
            conn.execute('INSERT INTO correccion_lineas_pos VALUES(?,?,?,?)',(correction,line['id'],s(request.cantidad),s(amount)))
        conn.execute('UPDATE correcciones_pos SET importe=? WHERE id=?',(s(refund),correction))
        fully=all(D(r['cantidad'])==D(r['devuelto']) for r in conn.execute('SELECT cantidad,devuelto FROM lineas_pos WHERE venta_id=?',(ident,)))
        status='anulada' if data.tipo=='anulacion' else 'devuelta' if fully else 'parcial_devuelta'
        conn.execute('UPDATE ventas_pos SET estado=? WHERE id=?',(status,ident))
        return {'correccion_id':correction,'importe_a_revisar':s(refund),'venta':sale_detail(conn,ident),'mensaje':'Se registró la corrección comercial. No se ejecutó ningún reintegro de dinero.'}
    return run(f'correccion:{ident}',data,person,action)

class Suspend(Operation):
    nombre:str=Field(min_length=1,max_length=100)
    carrito:Cart

@router.post('/suspendidos',status_code=201)
def suspend(data:Suspend,person=Depends(operator)):
    def action(conn,key):
        for line in data.carrito.lineas:sale_line(conn,line)
        ident=conn.execute('INSERT INTO carritos_suspendidos(nombre,datos,responsable_id,responsable) VALUES(?,?,?,?)',(data.nombre,data.carrito.model_dump_json(),person['id'],person['nombre'])).lastrowid
        return {'id':ident,'nombre':data.nombre}
    return run('suspender',data,person,action)

@router.get('/suspendidos')
def suspended(person=Depends(operator)):
    with database() as conn:
        rows=conn.execute("SELECT id,nombre,responsable,responsable_id,creado FROM carritos_suspendidos WHERE estado='disponible' ORDER BY id DESC").fetchall()
        return [dict(r) for r in rows if person['rol'] in ('dueno','encargado') or r['responsable_id']==person['id']]

@router.post('/suspendidos/{ident}/recuperar')
def resume(ident:int,data:Operation,person=Depends(operator)):
    def action(conn,key):
        row=conn.execute('SELECT * FROM carritos_suspendidos WHERE id=?',(ident,)).fetchone()
        if not row:raise HTTPException(404,'Venta suspendida no encontrada')
        if row['responsable_id']!=person['id'] and person['rol'] not in ('dueno','encargado'):raise HTTPException(403,'Solo podés recuperar tus ventas suspendidas')
        if row['estado']!='disponible':raise HTTPException(409,'Esta venta suspendida ya fue recuperada')
        conn.execute("UPDATE carritos_suspendidos SET estado='recuperado',recuperado_por=? WHERE id=?",(person['nombre'],ident))
        return {'id':ident,'carrito':json.loads(row['datos']),'mensaje':'Revisá precios y stock actuales antes de registrar'}
    return run(f'recuperar:{ident}',data,person,action)

class Replenishment(Model):
    venta_diaria:Qty|None=None
    dias_cobertura:int=Field(default=2,ge=1,le=14)
    dias_entrega:int=Field(default=0,ge=0,le=14)
    seguridad:Qty=Decimal(0)

@router.put('/reposicion/{ident}')
def set_replenishment(ident:int,data:Replenishment,person=Depends(authorized)):
    with database() as conn:
        p=product(conn,ident);require_quantity_unit(data.seguridad,p['unidad_venta'])
        conn.execute('INSERT INTO politica_reposicion VALUES(?,?,?,?,?) ON CONFLICT(producto_id) DO UPDATE SET venta_diaria=excluded.venta_diaria,dias_cobertura=excluded.dias_cobertura,dias_entrega=excluded.dias_entrega,seguridad=excluded.seguridad',(ident,s(data.venta_diaria),data.dias_cobertura,data.dias_entrega,s(data.seguridad)))
    return data.model_dump(mode='json')

@router.get('/plan')
def plan(dias:int=Query(default=7,ge=1,le=90),person=Depends(operator)):
    cutoff=(datetime.now(timezone.utc)-timedelta(days=dias)).isoformat().replace('+00:00','Z')
    with database() as conn:
        purchases=[];rotation=[]
        for p in conn.execute('SELECT * FROM productos WHERE activo=1 ORDER BY descripcion,id').fetchall():
            current=available(conn,p['id'])
            first=conn.execute("SELECT MIN(creado) FROM movimientos_stock WHERE producto_id=? AND tipo IN ('apertura','recepcion','ajuste_sobrante') AND CAST(cantidad AS REAL)>0",(p['id'],)).fetchone()[0]
            observed=min(dias,max(1,(datetime.now(timezone.utc)-datetime.fromisoformat(first.replace('Z','+00:00'))).days+1)) if first else 0
            sold=sum((-D(r[0]) for r in conn.execute("SELECT m.cantidad FROM movimientos_stock m JOIN comprobantes c ON c.id=m.documento_id WHERE m.producto_id=? AND m.tipo='venta' AND m.creado>=? AND c.estado!='anulado'",(p['id'],cutoff))),Decimal(0))
            sold+=sum((D(r['cantidad'])-D(r['devuelto']) for r in conn.execute("SELECT l.cantidad,l.devuelto FROM lineas_pos l JOIN ventas_pos v ON v.id=l.venta_id WHERE l.producto_id=? AND v.creado>=? AND v.estado!='anulada'",(p['id'],cutoff))),Decimal(0))
            sold+=sum((-D(r[0]) for r in conn.execute("SELECT m.cantidad FROM movimientos_stock m JOIN pedidos_web w ON w.id=m.documento_id WHERE m.producto_id=? AND m.tipo='venta_web' AND m.creado>=? AND w.estado='entregado'",(p['id'],cutoff))),Decimal(0))
            setting=conn.execute('SELECT * FROM politica_reposicion WHERE producto_id=?',(p['id'],)).fetchone()
            setting=dict(setting) if setting else {'venta_diaria':None,'dias_cobertura':2,'dias_entrega':0,'seguridad':'0'}
            manual=setting['venta_diaria'] is not None
            daily=D(setting['venta_diaria']) if manual else sold/observed if observed and sold else None
            horizon=setting['dias_cobertura']+setting['dias_entrega']
            due=stock.today()+timedelta(days=horizon)
            incoming=unknown=late=Decimal(0)
            for row in conn.execute('SELECT l.cantidad,l.recibido,p.fecha_entrega FROM pedido_lineas l JOIN pedidos_compra p ON p.id=l.pedido_id WHERE l.producto_id=?',(p['id'],)):
                pending=D(row['cantidad'])-D(row['recibido'])
                if not row['fecha_entrega']:unknown+=pending
                elif row['fecha_entrega']<str(stock.today()):late+=pending
                elif row['fecha_entrega']<=str(due):incoming+=pending
            minimum=conn.execute('SELECT minimo FROM politica_stock WHERE producto_id=?',(p['id'],)).fetchone()
            target=max(D(minimum[0]) if minimum else Decimal(0),(daily or Decimal(0))*horizon+D(setting['seguridad']))
            suggestion=max(Decimal(0),target-current-incoming)
            suggestion=suggestion.quantize(D('.001') if p['unidad_venta'] in ('kg','g') else Decimal(1),rounding=ROUND_CEILING)
            purchases.append({'id':p['id'],'descripcion':p['descripcion'],'codigo':p['codigo'],'unidad':p['unidad_venta'],'vendible':s(current),'venta_diaria':s(daily.quantize(D('.001'))) if daily is not None else None,'base':'estimacion_manual' if manual else 'ventas_observadas' if daily is not None else 'sin_historial_suficiente','dias_observados':observed,'vendido_periodo':s(sold),'entradas_previstas':s(incoming),'pedidos_sin_fecha':s(unknown),'pedidos_atrasados':s(late),'sugerencia':s(suggestion),'politica':setting})
            for l in conn.execute('SELECT * FROM lotes_stock WHERE producto_id=? ORDER BY ingreso,id',(p['id'],)):
                qty=sum((max(D(r[0]),Decimal(0)) for r in conn.execute('SELECT cantidad FROM existencias_lote WHERE lote_id=?',(l['id'],))),Decimal(0))
                if qty:rotation.append({'lote_id':l['id'],'producto_id':p['id'],'descripcion':p['descripcion'],'unidad':p['unidad_venta'],'cantidad':s(qty),'estado':l['estado'],'ingreso':l['ingreso'],'revision':l['proxima_revision'],'accion':'Separar; no vender' if l['estado']=='no_apto' else 'Revisar condición' if l['estado']=='revisar' else 'Revisar y priorizar si está apto' if l['estado']=='maduro' else 'Rotación habitual'})
        priority={'no_apto':0,'revisar':1,'maduro':2,'listo':3,'verde':4}
        rotation.sort(key=lambda l:(priority[l['estado']],l['ingreso'],l['lote_id']))
        return {'dias':dias,'reposicion':purchases,'rotacion':rotation,'nota':'Sugerencias para revisión humana. No se crean pedidos ni se garantiza demanda a partir de ventas con faltantes.'}

class ContainerType(Model):
    nombre:str=Field(min_length=1,max_length=100)

@router.get('/envases/tipos')
def container_types():
    with database() as conn:return [dict(r) for r in conn.execute('SELECT * FROM tipos_envase ORDER BY nombre')]

@router.post('/envases/tipos',status_code=201)
def create_container(data:ContainerType,person=Depends(authorized)):
    with database() as conn:
        conn.execute('BEGIN IMMEDIATE')
        if conn.execute('SELECT 1 FROM tipos_envase WHERE lower(nombre)=lower(?)',(data.nombre,)).fetchone():raise HTTPException(409,'Ya existe ese tipo de envase')
        ident=conn.execute('INSERT INTO tipos_envase(nombre) VALUES(?)',(data.nombre,)).lastrowid
    return {'id':ident,'nombre':data.nombre}

def container_balance(conn,supplier,kind):
    local=debt=0;deposit=Decimal(0)
    for row in conn.execute('SELECT * FROM movimientos_envase WHERE proveedor_id=? AND envase_id=?',(supplier,kind)):
        if row['tipo'] in ('recibido','saldo_inicial'):local+=row['cantidad'];debt+=row['cantidad']
        elif row['tipo']=='devuelto':local-=row['cantidad'];debt-=row['cantidad']
        elif row['tipo']=='perdida':local-=row['cantidad']
        elif row['tipo']=='baja_acordada':debt-=row['cantidad']
        elif row['tipo']=='deposito_pagado':deposit+=D(row['importe'])
        else:deposit-=D(row['importe'])
    return {'en_local':local,'por_devolver':debt,'perdidos_a_regularizar':debt-local,'deposito_a_favor':s(deposit)}

@router.get('/envases')
def containers(person=Depends(operator)):
    with database() as conn:
        result=[]
        pairs=conn.execute('SELECT DISTINCT m.proveedor_id,m.envase_id,p.nombre proveedor,t.nombre envase FROM movimientos_envase m JOIN proveedores p ON p.id=m.proveedor_id JOIN tipos_envase t ON t.id=m.envase_id').fetchall()
        for pair in pairs:
            result.append({**dict(pair),**container_balance(conn,pair['proveedor_id'],pair['envase_id']),'historial':[dict(r) for r in conn.execute('SELECT * FROM movimientos_envase WHERE proveedor_id=? AND envase_id=? ORDER BY id DESC',(pair['proveedor_id'],pair['envase_id']))]})
        return result

class ContainerMove(Operation):
    proveedor_id:int=Field(gt=0)
    envase_id:int=Field(gt=0)
    tipo:Literal['recibido','devuelto','perdida','baja_acordada','saldo_inicial','deposito_pagado','deposito_reintegrado','deposito_aplicado']
    cantidad:int=Field(default=0,ge=0,le=1000000)
    importe:Money=Decimal(0)
    referencia:str=Field(min_length=3,max_length=200)
    motivo:str=Field(min_length=3,max_length=500)
    @model_validator(mode='after')
    def dimensions(self):
        financial=self.tipo.startswith('deposito_')
        if financial and (self.cantidad!=0 or self.importe<=0):raise ValueError('El depósito requiere importe positivo y cantidad cero')
        if not financial and (self.cantidad<=0 or self.importe!=0):raise ValueError('El movimiento de envases requiere cantidad entera positiva e importe cero')
        return self

@router.post('/envases/movimientos',status_code=201)
def container_move(data:ContainerMove,person=Depends(authorized)):
    def action(conn,key):
        if not conn.execute('SELECT 1 FROM proveedores WHERE id=?',(data.proveedor_id,)).fetchone() or not conn.execute('SELECT 1 FROM tipos_envase WHERE id=?',(data.envase_id,)).fetchone():raise HTTPException(422,'Proveedor o tipo de envase inexistente')
        before=container_balance(conn,data.proveedor_id,data.envase_id)
        if data.tipo in ('devuelto','perdida') and data.cantidad>before['en_local']:raise HTTPException(409,'La cantidad supera los envases disponibles en el local')
        if data.tipo=='baja_acordada' and data.cantidad>before['perdidos_a_regularizar']:raise HTTPException(409,'Solo se puede regularizar una pérdida ya registrada')
        if data.tipo in ('deposito_reintegrado','deposito_aplicado') and data.importe>D(before['deposito_a_favor']):raise HTTPException(409,'El importe supera el depósito a favor registrado')
        if data.tipo=='saldo_inicial' and conn.execute('SELECT 1 FROM movimientos_envase WHERE proveedor_id=? AND envase_id=?',(data.proveedor_id,data.envase_id)).fetchone():raise HTTPException(409,'El saldo inicial se registra antes de los demás movimientos')
        ident=conn.execute('INSERT INTO movimientos_envase(proveedor_id,envase_id,tipo,cantidad,importe,referencia,motivo,responsable) VALUES(?,?,?,?,?,?,?,?)',(data.proveedor_id,data.envase_id,data.tipo,data.cantidad,s(data.importe),data.referencia,data.motivo,person['nombre'])).lastrowid
        return {'id':ident,**container_balance(conn,data.proveedor_id,data.envase_id)}
    return run('envases',data,person,action)
