import json
from decimal import Decimal
from datetime import datetime
from zoneinfo import ZoneInfo
from html import escape
from pathlib import Path
from string import Template
from typing import Literal
from fastapi import APIRouter,Cookie,Depends,HTTPException
from fastapi.responses import HTMLResponse
from routers.preparacion import database
from routers.comercial import authorized,actor
from document_photos import available_photo,effective_photo

router=APIRouter(prefix='/api/documentos',tags=['Documentos con fotos'])
Origin=Literal['pos','legado']
Kind=Literal['comprobante','remito']
TEMPLATE=Path(__file__).resolve().parents[2]/'frontend/templates/documento.html'

def amount(value,places=2):
    value=Decimal(str(value or 0))
    result=format(value,f',.{places}f')
    return result.replace(',','X').replace('.',',').replace('X','.')

def document(conn,origin,ident,token=None):
    if origin=='pos':
        actor(conn,token)
        sale=conn.execute('SELECT * FROM ventas_pos WHERE id=?',(ident,)).fetchone()
        if not sale:raise HTTPException(404,'Venta no encontrada')
        items=[dict(r) for r in conn.execute('SELECT * FROM lineas_pos WHERE venta_id=? ORDER BY id',(ident,))]
        rows=[{'id':l['id'],'producto_id':l['producto_id'],'descripcion':l['descripcion'],'unidad':l['unidad'],'cantidad':l['cantidad'],'precio':l['precio'],'subtotal':l['neto'],'foto':l['foto'],'devuelto':l['devuelto']} for l in items]
        head={'numero':f'V-{ident:06}','fecha':sale['creado'],'estado':sale['estado'],'subtotal':sale['subtotal'],'descuento':sale['descuento'],'total':sale['total'],'cliente':'','cobro':sale['cobro']}
    else:
        sale=conn.execute('SELECT * FROM comprobantes WHERE id=?',(ident,)).fetchone()
        if not sale:raise HTTPException(404,'Comprobante no encontrado')
        items=[dict(r) for r in conn.execute('SELECT * FROM comprobante_items WHERE comprobante_id=? ORDER BY id',(ident,))]
        rows=[]
        for l in items:
            rows.append({'id':l['id'],'producto_id':l['producto_id'],'descripcion':l['producto_desc'],'unidad':'','cantidad':l['cantidad'],'precio':l['precio_unitario'],'subtotal':l['subtotal'],'foto':l['foto'],'devuelto':'0'})
        subtotal=Decimal(str(sale['subtotal'] or 0))
        head={'numero':sale['numero'],'fecha':sale['fecha'],'estado':sale['estado'],'subtotal':str(subtotal),'descuento':str(subtotal-Decimal(str(sale['total'] or 0))),'total':str(sale['total']),'cliente':sale['cliente_nombre'] or '','cobro':'sin verificar'}
    missing=[]
    for row in rows:
        row['foto']=effective_photo(conn,origin,row['id'],row['foto'])
        row['foto_disponible']=bool(available_photo(row['foto']))
        if not row['foto_disponible']:missing.append({'item_id':row['id'],'producto_id':row['producto_id'],'descripcion':row['descripcion']})
    config=conn.execute('SELECT datos FROM configuracion_negocio WHERE id=1').fetchone()
    business=json.loads(config[0]) if config else {}
    return {**head,'origen':origin,'id':ident,'negocio':business.get('nombre') or 'Mi negocio','localidad':business.get('localidad') or '','items':rows,'fotos_faltantes':missing}

@router.get('/{origin}/{ident}/datos')
def document_data(origin:Origin,ident:int,cs_sesion:str|None=Cookie(default=None)):
    with database() as conn:return document(conn,origin,ident,cs_sesion)

@router.post('/{origin}/{ident}/completar-fotos')
def complete_photos(origin:Origin,ident:int,person=Depends(authorized),cs_sesion:str|None=Cookie(default=None)):
    with database() as conn:
        conn.execute('BEGIN IMMEDIATE')
        current=document(conn,origin,ident,cs_sesion)
        completed=0
        for row in current['items']:
            if row['foto_disponible'] or not row['producto_id']:continue
            p=conn.execute('SELECT foto FROM productos WHERE id=?',(row['producto_id'],)).fetchone()
            image=available_photo(p[0]) if p else ''
            if not image:continue
            conn.execute('INSERT INTO fotos_documento(origen,item_id,foto,responsable,motivo) VALUES(?,?,?,?,?)',(origin,row['id'],image,person['nombre'],'Foto del catálogo incorporada después del registro; importes y cantidades conservados'))
            completed+=1
        return {'completadas':completed,'faltantes':document(conn,origin,ident,cs_sesion)['fotos_faltantes']}

@router.get('/{origin}/{ident}',response_class=HTMLResponse)
def render_document(origin:Origin,ident:int,tipo:Kind='comprobante',cs_sesion:str|None=Cookie(default=None)):
    with database() as conn:data=document(conn,origin,ident,cs_sesion)
    delivery=tipo=='remito';title='Remito interno' if delivery else 'Comprobante de venta interno'
    rows=[]
    for index,row in enumerate(data['items'],1):
        photo=f'<img class="product-photo" src="{escape(row["foto"],quote=True)}" alt="{escape(row["descripcion"],quote=True)}" loading="eager">' if row['foto_disponible'] else '<span class="photo-missing">Foto pendiente</span>'
        prices='' if delivery else f'<td class="number">$ {amount(row["precio"],4)}</td><td class="number">$ {amount(row["subtotal"])}</td>'
        returned=f'<small>Devuelto: {amount(row["devuelto"],3)}</small>' if Decimal(str(row['devuelto'])) else ''
        rows.append(f'<tr><td>{index}</td><td class="photo-cell">{photo}</td><td>{escape(row["descripcion"])}{returned}</td><td class="number">{amount(row["cantidad"],3)} {escape(row["unidad"])}</td>{prices}</tr>')
    missing=data['fotos_faltantes']
    notice='<strong>Faltan fotos de productos.</strong> Cargalas en el catálogo y completá las imágenes de este documento antes de imprimir.<ul>'+''.join('<li>'+escape(r['descripcion'])+'</li>' for r in missing)+'</ul>' if missing else 'Cada renglón conserva la imagen asociada a este documento.'
    totals='' if delivery else f'<div class="totals"><p>Subtotal <b>$ {amount(data["subtotal"])}</b></p><p>Descuento <b>−$ {amount(data["descuento"])}</b></p><p class="total">Total original <b>$ {amount(data["total"])}</b></p></div>'
    date_text=datetime.fromisoformat(data['fecha'].replace('Z','+00:00')).astimezone(ZoneInfo('America/Argentina/Cordoba')).strftime('%d/%m/%Y %H:%M') if origin=='pos' else data['fecha']
    values={'title':escape(title),'business':escape(data['negocio']),'locality':escape(data['localidad']),'number':escape(data['numero'] or str(ident)),'date':escape(date_text),'status':escape(data['estado']),'payment':escape(data['cobro']),'client':escape(data['cliente'] or 'Sin identificación de cliente'),'notice':notice,'rows':''.join(rows),'price_columns':'' if delivery else '<th class="number">Precio unitario</th><th class="number">Importe</th>','totals':totals,'missing':'1' if missing else '0','complete_url':f'/api/documentos/{origin}/{ident}/completar-fotos','disabled':'disabled' if missing else '','complete_disabled':'' if missing else 'disabled'}
    return Template(TEMPLATE.read_text(encoding='utf-8')).substitute(values)
