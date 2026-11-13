"""Transactional inventory helpers, shared by purchases and the legacy sales module."""
import json
import time
from datetime import datetime,timedelta,timezone
from decimal import Decimal,ROUND_HALF_UP
from zoneinfo import ZoneInfo
from fastapi import HTTPException

D=lambda value: Decimal(str(value))
def s(value): return format(value,'f') if value is not None else None
def money(value): return value.quantize(Decimal('.01'),rounding=ROUND_HALF_UP)
def unitcost(value): return value.quantize(Decimal('.0001'),rounding=ROUND_HALF_UP)
def today(): return datetime.now(ZoneInfo('America/Argentina/Cordoba')).date()

def lot(conn,ident):
    row=conn.execute('SELECT * FROM lotes_stock WHERE id=?',(ident,)).fetchone()
    if not row: raise HTTPException(404,'Lote no encontrado')
    return row

def location(conn,ident):
    row=conn.execute('SELECT * FROM ubicaciones_stock WHERE id=?',(ident,)).fetchone()
    if not row: raise HTTPException(422,'Ubicación no encontrada')
    return row

def balance(conn,lote_id,ubicacion_id):
    row=conn.execute('SELECT * FROM existencias_lote WHERE lote_id=? AND ubicacion_id=?',(lote_id,ubicacion_id)).fetchone()
    return dict(row) if row else {'lote_id':lote_id,'ubicacion_id':ubicacion_id,'cantidad':'0','version':0}

def move(conn,lote_id,ubicacion_id,delta,tipo,origin,actor,reason,document=None,inferred=False,allow_negative=False):
    batch=lot(conn,lote_id);location(conn,ubicacion_id)
    if conn.execute('SELECT 1 FROM movimientos_stock WHERE origen_clave=?',(origin,)).fetchone():
        raise HTTPException(409,'El movimiento ya fue registrado')
    previous=balance(conn,lote_id,ubicacion_id)
    new=D(previous['cantidad'])+delta
    if new<0 and not allow_negative: raise HTTPException(409,'La cantidad supera la existencia del lote en esa ubicación')
    if abs(new)>D('99999999999'): raise HTTPException(422,'La existencia supera el límite admitido')
    cost=D(batch['costo_unitario']) if batch['costo_unitario'] is not None else None
    conn.execute('INSERT INTO existencias_lote(lote_id,ubicacion_id,cantidad,version) VALUES(?,?,?,1) ON CONFLICT(lote_id,ubicacion_id) DO UPDATE SET cantidad=excluded.cantidad,version=existencias_lote.version+1',(lote_id,ubicacion_id,s(new)))
    return conn.execute('INSERT INTO movimientos_stock(lote_id,ubicacion_id,producto_id,tipo,cantidad,unidad,costo_unitario,costo_total,responsable,motivo,origen_clave,documento_id,asignacion) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)',(lote_id,ubicacion_id,batch['producto_id'],tipo,s(delta),batch['unidad'],s(cost),s(money(abs(delta)*cost)) if cost is not None else None,actor,reason,origin,document,'inferida' if inferred else 'declarada')).lastrowid

def ensure_product(conn,product_id):
    if conn.execute('SELECT 1 FROM inventario_productos WHERE producto_id=?',(product_id,)).fetchone(): return
    p=conn.execute('SELECT * FROM productos WHERE id=?',(product_id,)).fetchone()
    if not p: raise HTTPException(404,'Producto no encontrado')
    conn.execute('INSERT INTO inventario_productos VALUES(?)',(product_id,))
    if D(p['stock'])!=0:
        cost=p['promedio_exacto'] if p['promedio_exacto'] is not None else str(p['precio_costo']) if p['precio_costo'] else None
        ident=conn.execute("INSERT INTO lotes_stock(producto_id,origen,unidad,costo_unitario,estado,notas) VALUES(?,'saldo_anterior',?,?,'revisar','Saldo anterior sin asignación de recepción. Revisar origen físico')",(product_id,p['unidad_venta'],cost)).lastrowid
        move(conn,ident,1,D(p['stock']),'apertura',f'apertura:{product_id}','Migración','Saldo previo; no se infiere proveedor ni recepción',allow_negative=True)

def physical(conn,product_id):
    return sum((D(r[0]) for r in conn.execute('SELECT e.cantidad FROM existencias_lote e JOIN lotes_stock l ON l.id=e.lote_id WHERE l.producto_id=?',(product_id,))),Decimal(0))

def require_consistent(conn,product_id):
    ensure_product(conn,product_id)
    projected=D(conn.execute('SELECT stock FROM productos WHERE id=?',(product_id,)).fetchone()[0])
    if abs(projected-physical(conn,product_id))>D('.000001'):
        raise HTTPException(409,'El stock fue modificado fuera del inventario. Revisá y conciliá un conteo físico antes de continuar')
    if any(D(r[0])<0 for r in conn.execute('SELECT e.cantidad FROM existencias_lote e JOIN lotes_stock l ON l.id=e.lote_id WHERE l.producto_id=?',(product_id,))):
        raise HTTPException(409,'Hay un saldo negativo heredado. Corregí ese lote mediante un conteo físico antes de continuar')

def sync_product(conn,product_id):
    rows=conn.execute('SELECT e.cantidad,l.costo_unitario FROM existencias_lote e JOIN lotes_stock l ON l.id=e.lote_id WHERE l.producto_id=?',(product_id,)).fetchall()
    total=sum((D(r['cantidad']) for r in rows),Decimal(0))
    known=total>0 and all(D(r['cantidad'])>=0 and r['costo_unitario'] is not None for r in rows if D(r['cantidad'])!=0)
    average=unitcost(sum((D(r['cantidad'])*D(r['costo_unitario']) for r in rows if D(r['cantidad'])!=0),Decimal(0))/total) if known else None
    conn.execute("UPDATE productos SET stock=?,promedio_exacto=?,precio_costo=?,actualizado_en=datetime('now') WHERE id=?",(float(total),s(average),float(average) if average is not None else 0,product_id))

def receipt_charge(conn,rid):
    row=conn.execute('SELECT r.*,p.proveedor_id,p.dias_plazo FROM recepciones_compra r JOIN pedidos_compra p ON p.id=r.pedido_id WHERE r.id=?',(rid,)).fetchone()
    data=json.loads(row['datos'])
    timestamp=datetime.fromisoformat(row['creado'].replace('Z','+00:00')).astimezone(ZoneInfo('America/Argentina/Cordoba')).date()
    owed=data.get('importe_proveedor',s(sum((D(i['subtotal']) for i in data.get('lineas',[])),Decimal(0))))
    conn.execute('INSERT OR IGNORE INTO cuenta_proveedor(proveedor_id,recepcion_id,tipo,importe,referencia,motivo,responsable,fecha,vencimiento,origen_clave) VALUES(?,?,?,?,?,?,?,?,?,?)',(row['proveedor_id'],rid,'cargo',owed,data.get('referencia') or f'Recepción {rid}','Mercadería y gastos expresamente cobrados por este proveedor; pagos a registrar por separado',data['responsable'],str(timestamp),str(timestamp+timedelta(days=row['dias_plazo'])),f'cargo_recepcion:{rid}'))

def record_receipt(conn,rid,item,person,ubicacion):
    location(conn,ubicacion)
    supplier=conn.execute('SELECT p.proveedor_id FROM recepciones_compra r JOIN pedidos_compra p ON p.id=r.pedido_id WHERE r.id=?',(rid,)).fetchone()[0]
    ident=conn.execute('INSERT INTO lotes_stock(producto_id,origen,recepcion_id,linea_id,proveedor_id,unidad,costo_unitario,estado,notas) VALUES(?,?,?,?,?,?,?,?,?)',(item['producto_id'],'recepcion',rid,item['linea_id'],supplier,item['unidad'],item['costo_unitario'],'listo' if item['calidad']=='buena' else 'revisar',item['observaciones'])).lastrowid
    move(conn,ident,ubicacion,D(item['aceptado']),'recepcion',f'recepcion:{rid}:{item["linea_id"]}',person,'Ingreso de mercadería aceptada',rid)

def initialize(conn):
    for row in conn.execute('SELECT id FROM productos').fetchall(): ensure_product(conn,row[0])
    # Historical receipts retain provenance but do not invent what remains of each lot.
    for row in conn.execute('SELECT r.id,r.datos,r.creado,p.proveedor_id FROM recepciones_compra r JOIN pedidos_compra p ON p.id=r.pedido_id').fetchall():
        data=json.loads(row['datos'])
        for item in data.get('lineas',[]):
            if D(item['aceptado'])>0:
                conn.execute("INSERT OR IGNORE INTO lotes_stock(producto_id,origen,recepcion_id,linea_id,proveedor_id,unidad,costo_unitario,estado,notas,ingreso) VALUES(?,'recepcion_historica',?,?,?,?,?,'revisar','Recepción anterior: existencia actual no atribuida automáticamente',?)",(item['producto_id'],row['id'],item['linea_id'],row['proveedor_id'],item['unidad'],item['costo_unitario'],row['creado']))
        receipt_charge(conn,row['id'])

def reserved_web(conn, product_id, exclude=None):
    if not conn.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='reservas_web'").fetchone():
        return Decimal(0)
    return sum((D(r[0]) for r in conn.execute('SELECT cantidad FROM reservas_web WHERE producto_id=? AND vence>? AND pedido_id!=?', (product_id,time.time(),str(exclude or '')))), Decimal(0))

def free_web(conn, product_id, exclude=None):
    rows=conn.execute("SELECT e.cantidad FROM existencias_lote e JOIN lotes_stock l ON l.id=e.lote_id JOIN ubicaciones_stock u ON u.id=e.ubicacion_id WHERE l.producto_id=? AND u.vendible=1 AND l.estado!='no_apto'", (product_id,))
    return max(Decimal(0),sum((max(D(r[0]),Decimal(0)) for r in rows),Decimal(0))-reserved_web(conn,product_id,exclude))

def consume_sale(conn,product_id,qty,sale_id,item_id,kind='venta',responsible='Módulo de ventas anterior',prioritize=False,reservation_id=None):
    require_consistent(conn,product_id)
    p=conn.execute('SELECT unidad_venta FROM productos WHERE id=?',(product_id,)).fetchone()
    if qty<=0 or qty.as_tuple().exponent < -3 or (p[0] not in ('kg','g') and qty!=qty.to_integral_value()):
        raise HTTPException(422,'Cantidad de venta incompatible con la unidad o precisión del producto')
    ordering="CASE l.estado WHEN 'maduro' THEN 0 WHEN 'listo' THEN 1 WHEN 'verde' THEN 2 ELSE 3 END," if prioritize else ''
    rows=conn.execute("SELECT e.*,l.ingreso FROM existencias_lote e JOIN lotes_stock l ON l.id=e.lote_id JOIN ubicaciones_stock u ON u.id=e.ubicacion_id WHERE l.producto_id=? AND u.vendible=1 AND l.estado!='no_apto' ORDER BY "+ordering+"l.ingreso,l.id,u.id",(product_id,)).fetchall()
    if sum((max(D(r['cantidad']),Decimal(0)) for r in rows),Decimal(0))-reserved_web(conn,product_id,reservation_id)<qty:
        raise HTTPException(409,'No hay suficiente stock libre; revisá lotes y reservas de la tienda')
    remaining=qty
    for row in rows:
        take=min(remaining,max(D(row['cantidad']),Decimal(0)))
        if take:
            move(conn,row['lote_id'],row['ubicacion_id'],-take,kind,f'{kind}:{item_id}:{row["lote_id"]}:{row["ubicacion_id"]}',responsible,'Lote asignado automáticamente; origen físico no confirmado',sale_id,True)
            remaining-=take
        if not remaining: break
    sync_product(conn,product_id)

def reverse_sale(conn,sale_id,items):
    rows=conn.execute("SELECT * FROM movimientos_stock WHERE tipo='venta' AND documento_id=?",(sale_id,)).fetchall()
    touched=set()
    if rows:
        for row in rows:
            require_consistent(conn,row['producto_id'])
            move(conn,row['lote_id'],row['ubicacion_id'],-D(row['cantidad']),'anulacion_venta',f'anulacion_venta:{row["id"]}','Módulo de ventas anterior','Anulación del comprobante; verificar condición de la mercadería',sale_id,True)
            touched.add(row['producto_id'])
            sync_product(conn,row['producto_id'])
    else:
        for item in items:
            if not item['producto_id']: continue
            pid=item['producto_id'];require_consistent(conn,pid)
            p=conn.execute('SELECT unidad_venta FROM productos WHERE id=?',(pid,)).fetchone()
            ident=conn.execute("INSERT INTO lotes_stock(producto_id,origen,unidad,costo_unitario,estado,notas) VALUES(?,'anulacion_heredada',?,?,'revisar','Origen físico pendiente de verificar')",(pid,p[0],str(item['precio_costo']) if item['precio_costo'] else None)).lastrowid
            move(conn,ident,1,D(item['cantidad']),'anulacion_venta',f'anulacion_heredada:{sale_id}:{item["id"]}','Módulo de ventas anterior','Anulación anterior al libro de inventario: no se infiere recepción',sale_id,True)
            sync_product(conn,pid)
