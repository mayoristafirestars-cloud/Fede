import json
import sqlite3
import re
import unittest
from datetime import timedelta
from decimal import Decimal
from uuid import uuid4
from pathlib import Path
import test_comercial as fixtures
from db import database
import stock


class InventarioTests(unittest.TestCase):
    login=fixtures.ComercialTests.login
    create_product=fixtures.ComercialTests.create_product
    finance=fixtures.ComercialTests.finance
    adjust=fixtures.ComercialTests.adjust
    order=fixtures.ComercialTests.order
    receipt_body=fixtures.ComercialTests.receipt_body
    receive=fixtures.ComercialTests.receive
    tearDown=fixtures.ComercialTests.tearDown

    def setUp(self):
        fixtures.ComercialTests.setUp(self)
        self.o,_=self.order()
        response=self.receive(self.o,self.receipt_body(self.o))
        self.assertEqual(response.status_code,201,response.text)
        self.r=response.json()
        self.lot=self.summary()['lotes'][0]

    def summary(self):return self.client.get('/api/inventario/resumen').json()
    def post(self,path,**body):return self.client.post('/api/inventario'+path,json={'clave_operacion':str(uuid4()),**body})
    def account(self):return self.client.get('/api/inventario/cuentas').json()[0]
    def payment(self,amount='5000',kind='pago',**extra):
        return self.post('/cuentas/movimientos',recepcion_id=self.r['id'],tipo=kind,importe=amount,referencia='Documento de prueba',motivo='Registro confirmado',confirmado=True,**extra)
    def leave(self,quantity='1',kind='merma',**extra):
        return self.post('/salidas',lote_id=self.lot['id'],ubicacion_id=1,cantidad=quantity,tipo=kind,motivo='Movimiento de prueba',**extra)
    def return_goods(self,quantity='3'):
        return self.post('/devoluciones',lote_id=self.lot['id'],ubicacion_id=1,cantidad=quantity,motivo='Calidad rechazada después de recibir')
    def count(self,amount='18'):
        current=self.summary()['lotes'][0]['existencias'][0]
        return self.post('/conteos',lote_id=self.lot['id'],ubicacion_id=1,cantidad=amount,version=current['version'],motivo='Recuento físico del lote')
    def sale(self,quantity=2):
        return self.client.post('/api/facturacion/nuevo',json={'items':[{'producto_id':self.p['id'],'producto_desc':'Tomate','cantidad':quantity,'precio_unitario':1500}]})

    def test_receipt_trace_and_expenses_owed_to_correct_party(self):
        p=self.summary()['productos'][0]
        self.assertEqual(Decimal(p['total']),20)
        self.assertEqual(Decimal(p['vendible']),20)
        self.assertEqual(self.lot['proveedor_id'],self.s['id'])
        self.assertEqual(self.lot['recepcion_id'],self.r['id'])
        self.assertEqual(self.lot['costo_unitario'],'1100.0000')
        self.assertEqual(Decimal(self.account()['saldo']),20000)
        order,_=self.order();body=self.receipt_body(order);body['gastos_a_proveedor']=True
        self.assertEqual(self.receive(order,body).status_code,201)
        self.assertEqual(Decimal(self.account()['saldo']),42000)

    def test_receiving_at_deposit(self):
        order,_=self.order();body=self.receipt_body(order);body['ubicacion_id']=2
        self.assertEqual(self.receive(order,body).status_code,201)
        p=self.summary()['productos'][0]
        self.assertEqual(Decimal(p['ubicaciones']['Depósito']),20)
        self.assertEqual(Decimal(p['ubicaciones']['Salón']),20)

    def test_transfer_conserves_physical_and_moves_available_out_of_quarantine(self):
        response=self.post('/traslados',lote_id=self.lot['id'],origen_id=1,destino_id=4,cantidad='5',motivo='Separar para inspección')
        self.assertEqual(response.status_code,201,response.text)
        p=self.summary()['productos'][0]
        self.assertEqual((Decimal(p['total']),Decimal(p['vendible'])),(20,15))
        movements=self.client.get('/api/inventario/movimientos').json()['items']
        self.assertEqual({m['tipo'] for m in movements},{'recepcion','traslado_salida','traslado_entrada'})
        self.assertEqual(sum(Decimal(m['cantidad']) for m in movements),20)

    def test_transfer_invalid_destination_or_quantity_rolls_back(self):
        for destination,qty in [(999,'1'),(1,'1'),(2,'21')]:
            self.assertIn(self.post('/traslados',lote_id=self.lot['id'],origen_id=1,destino_id=destination,cantidad=qty,motivo='Traslado de prueba').status_code,(409,422))
        self.assertEqual(Decimal(self.finance()['stock']),20)
        self.assertEqual(len(self.summary()['lotes'][0]['existencias']),1)

    def test_merma_gifts_consumption_and_donation_are_distinct(self):
        for kind in ['merma','regalo','consumo','donacion']:
            response=self.leave(kind=kind)
            self.assertEqual(response.status_code,201,response.text)
            self.assertEqual(response.json()['costo_total'],'1100.00')
        self.assertEqual(Decimal(self.finance()['stock']),16)
        self.assertEqual(Decimal(self.account()['saldo']),20000)
        types={m['tipo'] for m in self.client.get('/api/inventario/movimientos').json()['items']}
        self.assertTrue({'merma','regalo','consumo','donacion'}.issubset(types))
        self.assertEqual(self.leave('17').status_code,409)

    def test_return_does_not_silently_credit_debt_and_retry_is_safe(self):
        body={'clave_operacion':str(uuid4()),'lote_id':self.lot['id'],'ubicacion_id':1,'cantidad':'3','motivo':'Mercadería devuelta'}
        first=self.client.post('/api/inventario/devoluciones',json=body)
        self.assertEqual(first.status_code,201,first.text)
        self.assertEqual(self.client.post('/api/inventario/devoluciones',json=body).json(),first.json())
        self.assertEqual(Decimal(self.finance()['stock']),17)
        self.assertEqual(Decimal(self.account()['saldo']),20000)
        self.assertEqual(self.payment('3000','credito',devolucion_id=first.json()['id']).status_code,201)
        self.assertEqual(Decimal(self.account()['saldo']),17000)
        self.assertEqual(self.return_goods('18').status_code,409)

    def test_partial_payment_credit_and_supplier_refund(self):
        self.assertEqual(self.payment('5000').status_code,201)
        self.assertEqual(Decimal(self.account()['saldo']),15000)
        self.assertEqual(self.payment('15000').status_code,201)
        self.assertEqual(Decimal(self.account()['saldo']),0)
        self.assertEqual(self.payment('3000','credito').status_code,201)
        self.assertEqual(Decimal(self.account()['saldo']),-3000)
        self.assertEqual(self.payment('3001','reintegro').status_code,409)
        self.assertEqual(self.payment('3000','reintegro').status_code,201)
        self.assertEqual(Decimal(self.account()['saldo']),0)

    def test_payment_validation_and_idempotency(self):
        self.assertEqual(self.payment('20001').status_code,409)
        self.assertEqual(self.payment('1','reintegro').status_code,409)
        self.assertEqual(self.payment('20001','credito').status_code,409)
        self.assertEqual(self.payment('-1').status_code,422)
        self.assertEqual(self.payment('1',fecha=str(stock.today()+timedelta(days=1))).status_code,422)
        body={'clave_operacion':str(uuid4()),'recepcion_id':self.r['id'],'tipo':'pago','importe':'5000','referencia':'Recibo 123','motivo':'Pago confirmado','confirmado':True}
        first=self.client.post('/api/inventario/cuentas/movimientos',json=body)
        self.assertEqual(first.status_code,201)
        self.assertEqual(self.client.post('/api/inventario/cuentas/movimientos',json=body).json(),first.json())
        self.assertEqual(self.client.post('/api/inventario/cuentas/movimientos',json={**body,'importe':'6000'}).status_code,409)
        self.assertEqual(Decimal(self.account()['saldo']),15000)

    def test_payment_reversal_preserves_original_and_only_runs_once(self):
        payment=self.payment().json();body={'clave_operacion':str(uuid4()),'motivo':'Error en el recibo registrado'}
        url=f'/api/inventario/cuentas/movimientos/{payment["id"]}/revertir'
        response=self.client.post(url,json=body)
        self.assertEqual(response.status_code,200,response.text)
        self.assertEqual(self.client.post(url,json=body).json(),response.json())
        self.assertEqual(Decimal(self.account()['saldo']),20000)
        self.assertEqual(self.post(f'/cuentas/movimientos/{payment["id"]}/revertir',motivo='Otro intento').status_code,409)
        rows=self.account()['movimientos'];self.assertEqual(len(rows),3)
        self.assertTrue(next(m for m in rows if m['id']==payment['id'])['revertido'])

    def test_claims_and_followup_do_not_modify_stock_or_money(self):
        created=self.post('/reclamos',recepcion_id=self.r['id'],tipo='calidad',detalle='Calidad diferente a la acordada')
        self.assertEqual(created.status_code,201)
        ident=created.json()['id']
        for status in ['en_gestion','resuelto']:
            self.assertEqual(self.post(f'/reclamos/{ident}/eventos',estado=status,nota='Proveedor contactado por teléfono').status_code,200)
        claim=self.client.get('/api/inventario/reclamos').json()[0]
        self.assertEqual(claim['estado'],'resuelto');self.assertEqual(len(claim['eventos']),2)
        self.assertEqual(Decimal(self.finance()['stock']),20)
        self.assertEqual(Decimal(self.account()['saldo']),20000)

    def test_credit_cannot_link_another_reception_claim(self):
        claim=self.post('/reclamos',recepcion_id=self.r['id'],tipo='precio',detalle='Precio no acordado').json()
        order,_=self.order();other=self.receive(order,self.receipt_body(order)).json()
        response=self.post('/cuentas/movimientos',recepcion_id=other['id'],tipo='credito',importe='10',referencia='NC prueba',motivo='Diferencia de precio',confirmado=True,reclamo_id=claim['id'])
        self.assertEqual(response.status_code,422)
        self.assertEqual(Decimal(self.account()['saldo']),40000)

    def test_revision_and_non_sellable_lot(self):
        response=self.post(f'/lotes/{self.lot["id"]}/revision',estado='no_apto',notas='Separar por inspección',proxima_revision=str(stock.today()))
        self.assertEqual(response.status_code,200,response.text)
        p=self.summary()['productos'][0];self.assertEqual(Decimal(p['total']),20);self.assertEqual(Decimal(p['vendible']),0)
        self.assertEqual(self.sale().status_code,409)
        rows=self.client.get(f'/api/inventario/lotes/{self.lot["id"]}/revisiones').json()
        self.assertEqual(rows[0]['anterior'],'listo');self.assertEqual(rows[0]['estado'],'no_apto')

    def test_count_draft_and_approved_difference_are_not_merma(self):
        count=self.count().json();self.assertEqual(Decimal(self.finance()['stock']),20)
        body={'clave_operacion':str(uuid4())}
        url=f'/api/inventario/conteos/{count["id"]}/aprobar'
        response=self.client.post(url,json=body);self.assertEqual(response.status_code,200,response.text)
        self.assertEqual(response.json()['diferencia'],'-2')
        self.assertEqual(self.client.post(url,json=body).json(),response.json())
        self.assertEqual(self.post(f'/conteos/{count["id"]}/aprobar').status_code,409)
        self.assertEqual(Decimal(self.finance()['stock']),18)
        self.assertEqual(self.client.get('/api/inventario/movimientos').json()['items'][0]['tipo'],'ajuste_faltante')

    def test_stale_count_cannot_overwrite_new_movements(self):
        count=self.count().json();self.leave()
        response=self.post(f'/conteos/{count["id"]}/aprobar')
        self.assertEqual(response.status_code,409)
        self.assertEqual(Decimal(self.finance()['stock']),19)
        response=self.post('/conteos',lote_id=self.lot['id'],ubicacion_id=1,cantidad='18',version=1,motivo='Conteo con versión vieja')
        self.assertEqual(response.status_code,409)

    def test_found_stock_has_unknown_origin_and_cost_until_identified(self):
        created=self.post('/conteos',producto_id=self.p['id'],ubicacion_id=2,cantidad='4',motivo='Existencia adicional encontrada sin lote',version=0)
        self.assertEqual(created.status_code,201,created.text)
        self.assertEqual(Decimal(self.finance()['stock']),20)
        self.assertEqual(self.post(f'/conteos/{created.json()["id"]}/aprobar').status_code,200)
        self.assertEqual(Decimal(self.finance()['stock']),24)
        self.assertIsNone(self.finance()['promedio'])
        found=next(l for l in self.summary()['lotes'] if l['origen']=='conteo_sin_origen')
        self.assertIsNone(found['recepcion_id'])
        self.assertEqual(self.post('/devoluciones',lote_id=found['id'],ubicacion_id=2,cantidad='1',motivo='Sin origen confirmado').status_code,422)

    def test_sale_and_annulment_are_in_the_same_ledger(self):
        response=self.sale(2);self.assertEqual(response.status_code,200,response.text)
        ident=response.json()['comprobante_id']
        self.assertEqual(Decimal(self.finance()['stock']),18)
        sale=next(m for m in self.client.get('/api/inventario/movimientos').json()['items'] if m['tipo']=='venta')
        self.assertEqual(sale['asignacion'],'inferida')
        self.assertEqual(self.client.post(f'/api/facturacion/{ident}/anular').status_code,200)
        self.assertEqual(Decimal(self.finance()['stock']),20)
        self.assertEqual(self.client.post(f'/api/facturacion/{ident}/anular').status_code,400)
        self.assertEqual(Decimal(self.finance()['stock']),20)

    def test_quarantined_stock_not_available_for_sale(self):
        self.post('/traslados',lote_id=self.lot['id'],origen_id=1,destino_id=4,cantidad='19',motivo='Separado por inspección')
        self.assertEqual(self.sale(2).status_code,409)
        self.assertEqual(self.sale(1).status_code,200)
        self.assertEqual(Decimal(self.finance()['stock']),19)

    def test_shortage_and_low_rotation_have_defined_time_window(self):
        self.assertFalse(self.summary()['productos'][0]['baja_rotacion'])
        self.assertEqual(self.client.put(f'/api/inventario/productos/{self.p["id"]}/alertas',json={'minimo':'25','dias_sin_venta':7}).status_code,200)
        with sqlite3.connect(database.DB_PATH) as conn:
            conn.execute("UPDATE movimientos_stock SET creado=strftime('%Y-%m-%dT%H:%M:%fZ','now','-10 days') WHERE tipo='recepcion'")
        p=self.summary()['productos'][0];self.assertTrue(p['faltante']);self.assertTrue(p['baja_rotacion'])
        self.sale(1)
        self.assertFalse(self.summary()['productos'][0]['baja_rotacion'])

    def test_external_stock_changes_are_visible_and_block_writes(self):
        with sqlite3.connect(database.DB_PATH) as conn:conn.execute('UPDATE productos SET stock=9 WHERE id=?',(self.p['id'],))
        self.assertTrue(self.summary()['productos'][0]['descuadre'])
        self.assertEqual(self.leave().status_code,409)
        count=self.count('19').json()
        self.assertEqual(self.post(f'/conteos/{count["id"]}/aprobar').status_code,200)
        self.assertFalse(self.summary()['productos'][0]['descuadre'])
        self.assertEqual(Decimal(self.finance()['stock']),19)

    def test_migration_repeat_does_not_duplicate_lots_charges_or_movements(self):
        self.payment('1000')
        before=(self.summary(),self.account(),self.client.get('/api/inventario/movimientos').json())
        database.inicializar_db();database.inicializar_db()
        self.assertEqual((self.summary(),self.account(),self.client.get('/api/inventario/movimientos').json()),before)

    def test_history_pagination(self):
        self.leave();self.leave()
        a=self.client.get('/api/inventario/movimientos?limit=1&offset=0').json()
        b=self.client.get('/api/inventario/movimientos?limit=1&offset=1').json()
        self.assertEqual(a['total'],3);self.assertNotEqual(a['items'][0]['id'],b['items'][0]['id'])

    def test_due_date_and_overdue_balance(self):
        doc=self.account()['documentos'][0]
        self.assertEqual(doc['vencimiento'],str(stock.today()+timedelta(days=7)))
        with sqlite3.connect(database.DB_PATH) as conn:conn.execute("UPDATE cuenta_proveedor SET vencimiento=? WHERE tipo='cargo'",(str(stock.today()-timedelta(days=1)),))
        self.assertTrue(self.account()['documentos'][0]['vencido'])

    def test_unauthorized_and_cashier_cannot_change_inventory_or_pay(self):
        self.client.delete('/api/comercial/sesion');self.assertEqual(self.leave().status_code,401)
        self.login();self.client.post('/api/comercial/responsables',json={'nombre':'Caja','clave':'clave-de-prueba','rol':'cajero'})
        self.client.delete('/api/comercial/sesion');self.login('Caja','clave-de-prueba')
        self.assertEqual(self.leave().status_code,403);self.assertEqual(self.payment().status_code,403)

    def test_upgrade_keeps_only_actual_stock_and_does_not_invent_remaining_lots(self):
        legacy=self.temp.name+'/legacy.db'
        with sqlite3.connect(database.DB_PATH) as source,sqlite3.connect(legacy) as dest:source.backup(dest)
        conn=sqlite3.connect(legacy)
        conn.execute('PRAGMA foreign_keys=OFF')
        tables=re.findall(r'CREATE TABLE IF NOT EXISTS (\w+)',Path(database.SCHEMA).with_name('inventario.sql').read_text())
        for name in reversed(tables):conn.execute('DROP TABLE '+name)
        conn.execute('UPDATE productos SET stock=5 WHERE id=?',(self.p['id'],))
        row=conn.execute('SELECT datos,payload FROM recepciones_compra WHERE id=?',(self.r['id'],)).fetchone()
        data=json.loads(row[0]);payload=json.loads(row[1])
        for name in ['ubicacion_id','gastos_a_proveedor','importe_proveedor']:
            data.pop(name,None);payload.pop(name,None)
        conn.execute('UPDATE recepciones_compra SET datos=?,payload=? WHERE id=?',(json.dumps(data),json.dumps(payload),self.r['id']))
        conn.commit();conn.close()
        database.DB_PATH=legacy
        database.inicializar_db()
        summary=self.summary()
        opening=next(l for l in summary['lotes'] if l['origen']=='saldo_anterior')
        historic=next(l for l in summary['lotes'] if l['origen']=='recepcion_historica')
        self.assertEqual(Decimal(opening['total']),5);self.assertIsNone(opening['recepcion_id'])
        self.assertEqual(Decimal(historic['total']),0)
        self.assertEqual(Decimal(summary['productos'][0]['total']),5)
        self.assertEqual(Decimal(self.account()['saldo']),20000)
        database.inicializar_db()
        self.assertEqual(len(self.summary()['lotes']),2)
        retried=self.receive(self.o,payload)
        self.assertEqual(retried.status_code,201,retried.text)
        self.assertEqual(Decimal(self.summary()['productos'][0]['total']),5)

    def test_confirmed_and_cross_kind_retry_checks(self):
        response=self.post('/cuentas/movimientos',recepcion_id=self.r['id'],tipo='pago',importe='10',referencia='Recibo prueba',motivo='Pago por confirmar',confirmado=False)
        self.assertEqual(response.status_code,422)
        operation=str(uuid4())
        self.assertEqual(self.leave(clave_operacion=operation).status_code,201)
        response=self.post('/reclamos',clave_operacion=operation,recepcion_id=self.r['id'],tipo='calidad',detalle='No reutilizar otra operación')
        self.assertEqual(response.status_code,409)

    def test_negative_legacy_position_must_be_counted_before_selling(self):
        p=self.create_product('HER','Producto heredado')
        with sqlite3.connect(database.DB_PATH) as conn:conn.execute('UPDATE productos SET stock=-2 WHERE id=?',(p['id'],))
        negative=next(l for l in self.summary()['lotes'] if l['producto_id']==p['id'])
        found=self.post('/conteos',producto_id=p['id'],ubicacion_id=2,cantidad='4',motivo='Mercadería adicional encontrada').json()
        self.assertEqual(self.post(f'/conteos/{found["id"]}/aprobar').status_code,200)
        summary=next(x for x in self.summary()['productos'] if x['id']==p['id'])
        self.assertEqual(Decimal(summary['total']),2);self.assertEqual(Decimal(summary['vendible']),0)
        sale={'items':[{'producto_id':p['id'],'producto_desc':p['descripcion'],'cantidad':1,'precio_unitario':10}]}
        self.assertEqual(self.client.post('/api/facturacion/nuevo',json=sale).status_code,409)
        current=negative['existencias'][0]
        count=self.post('/conteos',lote_id=negative['id'],ubicacion_id=1,cantidad='0',version=current['version'],motivo='Corrección de saldo negativo').json()
        self.assertEqual(self.post(f'/conteos/{count["id"]}/aprobar').status_code,200)
        self.assertEqual(self.client.post('/api/facturacion/nuevo',json=sale).status_code,200)


if __name__=='__main__':unittest.main()
