import json
import os
import sqlite3
import sys
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path
from uuid import uuid4

from fastapi.testclient import TestClient

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'backend'))
from db import database
from main import app


class ComercialTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.previous=database.DB_PATH
        database.DB_PATH=os.path.join(self.temp.name,'commercial.db')
        self.context=TestClient(app)
        self.client=self.context.__enter__()
        self.owner={'nombre':'Dueño de prueba','clave':'prueba-segura-123','rol':'dueno'}
        self.assertEqual(self.client.post('/api/comercial/responsables',json=self.owner).status_code,201)
        self.login()
        self.p=self.create_product('TOM','Tomate')
        self.s=self.client.post('/api/comercial/proveedores',json={'nombre':'Proveedor de prueba','condiciones':'A 7 días','dias_plazo':7}).json()

    def tearDown(self):
        self.context.__exit__(None,None,None)
        database.DB_PATH=self.previous
        self.temp.cleanup()

    def login(self, name=None, password=None):
        return self.client.post('/api/comercial/sesion',json={'nombre':name or self.owner['nombre'],'clave':password or self.owner['clave']})

    def create_product(self,code,name,unit='kg'):
        response=self.client.post('/api/gestion/productos',json={'codigo':code,'descripcion':name,'unidad_venta':unit})
        self.assertEqual(response.status_code,201)
        return response.json()

    def finance(self,ident=None):
        return next(p for p in self.client.get('/api/comercial/productos').json() if p['id']==(ident or self.p['id']))

    def adjust(self,amount,kind='precio',version=None,**kwargs):
        body={'tipo':kind,'importe':amount,'version':self.finance()['version_precio' if kind=='precio' else 'version_costo'] if version is None else version,'motivo':'Prueba de cambio','clave_operacion':str(uuid4()),**kwargs}
        return self.client.post(f'/api/comercial/productos/{self.p["id"]}/ajuste',json=body)

    def order(self,quantity='20',price='1000',extra=None):
        body={'proveedor_id':self.s['id'],'lineas':[{'producto_id':self.p['id'],'cantidad':quantity,'precio':price}], 'clave_operacion':str(uuid4())}
        if extra:body['lineas'].append(extra)
        response=self.client.post('/api/comercial/pedidos',json=body)
        self.assertEqual(response.status_code,201,response.text)
        return response.json(),body

    def receipt_body(self,order,**overrides):
        line={'linea_id':order['lineas'][0]['id'],'bruto_kg':'21','tara_kg':'1','precio':'1000','bultos':1,**overrides}
        return {'clave_operacion':str(uuid4()),'lineas':[line],'flete':'2000','otros_gastos':'0'}

    def receive(self,order,body):
        return self.client.post(f'/api/comercial/pedidos/{order["id"]}/recepciones',json=body)

    def test_authorization_required_and_cashier_cannot_change(self):
        self.client.delete('/api/comercial/sesion')
        self.assertEqual(self.adjust('1500').status_code,401)
        self.assertEqual(self.client.post('/api/comercial/proveedores',json={'nombre':'X'}).status_code,401)
        self.assertEqual(self.client.post('/api/comercial/responsables',json={'nombre':'Intruso','clave':'prueba-clave','rol':'dueno'}).status_code,401)
        self.login()
        self.client.post('/api/comercial/responsables',json={'nombre':'Caja','clave':'prueba-clave','rol':'cajero'})
        self.client.delete('/api/comercial/sesion');self.login('Caja','prueba-clave')
        self.assertEqual(self.adjust('1500').status_code,403)
        self.assertEqual(self.client.post('/api/comercial/responsables',json={'nombre':'Otro','clave':'prueba-clave'}).status_code,403)

    def test_encargado_can_change_but_not_create_responsibles(self):
        self.client.post('/api/comercial/responsables',json={'nombre':'Encargada','clave':'prueba-clave','rol':'encargado'})
        self.client.delete('/api/comercial/sesion');self.login('Encargada','prueba-clave')
        self.assertEqual(self.adjust('1500').status_code,200)
        self.assertEqual(self.client.post('/api/comercial/responsables',json={'nombre':'Otro','clave':'prueba-clave'}).status_code,403)

    def test_password_not_stored_in_plaintext_and_login_throttled(self):
        self.client.delete('/api/comercial/sesion')
        for _ in range(5):
            self.assertEqual(self.login(password='equivocada').status_code,401)
        self.assertEqual(self.login().status_code,429)
        with sqlite3.connect(database.DB_PATH) as conn:
            self.assertNotEqual(conn.execute('SELECT clave_hash FROM responsables').fetchone()[0],self.owner['clave'])
            conn.execute('UPDATE responsables SET bloqueado_hasta=0')
        response=self.login()
        self.assertEqual(response.status_code,200)
        self.assertIn('HttpOnly',response.headers['set-cookie'])
        self.assertIn('SameSite=strict',response.headers['set-cookie'])
        with sqlite3.connect(database.DB_PATH) as conn:
            conn.execute('UPDATE sesiones_comerciales SET vence=0')
        self.assertEqual(self.adjust('1500').status_code,401)

    def test_decimal_margins_and_append_only_history(self):
        self.adjust('1000','reposicion')
        response=self.adjust('1500')
        value=response.json()
        self.assertEqual(value['margen'],'33.33')
        self.assertEqual(value['recargo'],'50.00')
        first=value['historial'][0]
        self.adjust('1750.1234')
        value=self.finance()
        self.assertEqual(len(value['historial']),3)
        self.assertEqual(value['historial'][1],first)
        self.assertEqual(value['historial'][0]['anterior'],'1500')
        self.assertEqual(value['historial'][0]['responsable'],self.owner['nombre'])
        self.assertEqual(value['precio'],'1750.1234')

    def test_zero_missing_negative_and_invalid_prices(self):
        self.assertIsNone(self.finance()['margen'])
        self.adjust('0','reposicion');self.adjust('0')
        self.assertIsNone(self.finance()['margen']);self.assertIsNone(self.finance()['recargo'])
        self.adjust('100','reposicion');self.adjust('50')
        self.assertEqual(self.finance()['margen'],'-100.00')
        for amount in ['-1','NaN','Infinity','1.00001']:
            self.assertEqual(self.adjust(amount).status_code,422)
        self.assertEqual(self.adjust('100',motivo=' ').status_code,422)

    def test_price_version_and_operation_retry(self):
        body={'tipo':'precio','importe':'123.45','motivo':'Cambio de prueba','version':0,'clave_operacion':str(uuid4())}
        url=f'/api/comercial/productos/{self.p["id"]}/ajuste'
        self.assertEqual(self.client.post(url,json=body).status_code,200)
        self.assertEqual(self.client.post(url,json={**body,'importe':'123.4500'}).status_code,200)
        self.assertEqual(self.client.post(url,json=body).status_code,200)
        self.assertEqual(len(self.finance()['historial']),1)
        self.assertEqual(self.client.post(url,json={**body,'importe':'200'}).status_code,409)
        self.assertEqual(self.adjust('300',version=0).status_code,409)

    def test_new_prices_do_not_change_existing_comprobantes(self):
        with sqlite3.connect(database.DB_PATH) as conn:
            conn.execute("INSERT INTO comprobantes(tipo,numero,fecha,total) VALUES('presupuesto','P-OLD','01-01-2026',123)")
        self.adjust('500')
        with sqlite3.connect(database.DB_PATH) as conn:
            self.assertEqual(conn.execute("SELECT total FROM comprobantes WHERE numero='P-OLD'").fetchone()[0],123)

    def test_order_does_not_change_stock_and_retries_do_not_duplicate(self):
        order,body=self.order()
        self.assertEqual(order['estado'],'pendiente')
        self.assertEqual(Decimal(self.finance()['stock']),0)
        retry=self.client.post('/api/comercial/pedidos',json=body)
        self.assertEqual(retry.json()['id'],order['id'])
        self.assertEqual(len(self.client.get('/api/comercial/pedidos').json()),1)
        body['notas']='Cambió'
        self.assertEqual(self.client.post('/api/comercial/pedidos',json=body).status_code,409)

    def test_supplier_edit_keeps_order_snapshot(self):
        order,_=self.order()
        result=self.client.put(f'/api/comercial/proveedores/{self.s["id"]}',json={'nombre':'Nuevo nombre','dias_plazo':30})
        self.assertEqual(result.status_code,200)
        saved=self.client.get('/api/comercial/pedidos').json()[0]
        self.assertEqual(saved['proveedor_nombre'],'Proveedor de prueba')
        self.assertEqual(saved['dias_plazo'],7)
        self.assertEqual(self.client.put('/api/comercial/proveedores/999',json={'nombre':'X'}).status_code,404)

    def test_invalid_supplier_units_and_duplicate_order_lines(self):
        unit=self.create_product('AT','Perejil','atado')
        base={'proveedor_id':self.s['id'],'clave_operacion':str(uuid4()),'lineas':[{'producto_id':unit['id'],'cantidad':'1.5','precio':'10'}]}
        self.assertEqual(self.client.post('/api/comercial/pedidos',json=base).status_code,422)
        base['lineas']=[{'producto_id':self.p['id'],'cantidad':'1','precio':'10'}]*2
        self.assertEqual(self.client.post('/api/comercial/pedidos',json=base).status_code,422)
        base['lineas']=base['lineas'][:1];base['proveedor_id']=999
        self.assertEqual(self.client.post('/api/comercial/pedidos',json=base).status_code,422)

    def test_reception_weight_tare_freight_cost_and_history(self):
        order,_=self.order()
        body=self.receipt_body(order)
        response=self.receive(order,body)
        self.assertEqual(response.status_code,201,response.text)
        receipt=response.json()
        self.assertEqual(receipt['total'],'22000.00')
        self.assertEqual(receipt['lineas'][0]['aceptado'],'20')
        self.assertEqual(receipt['lineas'][0]['costo_unitario'],'1100.0000')
        state=self.finance()
        self.assertEqual(Decimal(state['stock']),20)
        self.assertEqual(state['promedio'],'1100.0000')
        self.assertEqual(state['historial'][0]['origen_id'],receipt['id'])
        self.assertEqual(self.client.get('/api/comercial/pedidos').json()[0]['estado'],'recibido')
        self.assertEqual(self.receive(order,body).json(),receipt)
        self.assertEqual(Decimal(self.finance()['stock']),20)
        with sqlite3.connect(database.DB_PATH) as conn:
            self.assertEqual(conn.execute('SELECT COUNT(*) FROM movimientos_compra').fetchone()[0],1)

    def test_partial_rejection_and_second_delivery(self):
        order,_=self.order()
        body=self.receipt_body(order,bruto_kg='13',tara_kg='1',rechazado='2',observaciones='Golpes')
        body['flete']='1000'
        response=self.receive(order,body)
        self.assertEqual(response.status_code,201,response.text)
        saved=self.client.get('/api/comercial/pedidos').json()[0]
        self.assertEqual(saved['estado'],'parcial')
        self.assertEqual(saved['lineas'][0]['pendiente'],'10')
        self.assertEqual(saved['recepciones'][0]['lineas'][0]['rechazado'],'2')
        body=self.receipt_body(order,bruto_kg='11',tara_kg='1',precio='2000');body['flete']='0'
        self.assertEqual(self.receive(order,body).status_code,201)
        self.assertEqual(self.finance()['promedio'],'1550.0000')
        self.assertEqual(self.finance()['reposicion'],'2000.0000')

    def test_invalid_reception_does_not_change_anything(self):
        order,_=self.order()
        invalid=[{'tara_kg':'22'},{'rechazado':'21','observaciones':'Mal estado'},{'rechazado':'1'},{'bruto_kg':'22'},{'cantidad':'20'},{'linea_id':999}]
        for overrides in invalid:
            body=self.receipt_body(order,**overrides)
            self.assertIn(self.receive(order,body).status_code,(409,422))
            self.assertEqual(Decimal(self.finance()['stock']),0)
        self.assertEqual(self.client.get('/api/comercial/pedidos').json()[0]['recepciones'],[])

    def test_all_rejected_does_not_increase_stock_or_cost(self):
        order,_=self.order()
        body=self.receipt_body(order,rechazado='20',observaciones='Rechazo total');body['flete']='0'
        self.assertEqual(self.receive(order,body).status_code,201)
        self.assertEqual(Decimal(self.finance()['stock']),0)
        self.assertIsNone(self.finance()['reposicion'])
        body=self.receipt_body(order,rechazado='20',observaciones='Rechazo total')
        self.assertEqual(self.receive(order,body).status_code,422)

    def test_expense_cent_allocation_is_exact(self):
        other=self.create_product('LEC','Lechuga')
        order,_=self.order(quantity='1',price='1',extra={'producto_id':other['id'],'cantidad':'1','precio':'1'})
        body={'clave_operacion':str(uuid4()),'flete':'0.01','lineas':[{'linea_id':line['id'],'bruto_kg':'1','tara_kg':'0','precio':'1'} for line in order['lineas']]}
        result=self.receive(order,body).json()
        self.assertEqual(sum(Decimal(i['gastos_asignados']) for i in result['lineas']),Decimal('.01'))
        self.assertEqual(sum(Decimal(i['costo_total']) for i in result['lineas']),Decimal('2.01'))

    def test_units_and_grams_and_no_implicit_box_weight(self):
        other=self.create_product('AT','Perejil','atado')
        order,_=self.order(quantity='1',price='1',extra={'producto_id':other['id'],'cantidad':'3','precio':'100'})
        body={'clave_operacion':str(uuid4()),'lineas':[{'linea_id':order['lineas'][1]['id'],'cantidad':'3','precio':'100'}]}
        self.assertEqual(self.receive(order,body).status_code,201)
        self.assertEqual(Decimal(self.finance(other['id'])['stock']),3)
        grams=self.create_product('GRAM','Especia','g')
        order,_=self.order(quantity='1',price='1',extra={'producto_id':grams['id'],'cantidad':'1000','precio':'1'})
        body={'clave_operacion':str(uuid4()),'lineas':[{'linea_id':order['lineas'][1]['id'],'bruto_kg':'1.2','tara_kg':'.2','precio':'1'}]}
        self.assertEqual(self.receive(order,body).status_code,201)
        self.assertEqual(Decimal(self.finance(grams['id'])['stock']),1000)

    def test_cost_update_does_not_rewrite_purchase_or_average(self):
        order,_=self.order();self.receive(order,self.receipt_body(order))
        before=self.client.get('/api/comercial/pedidos').json()
        self.adjust('2000','reposicion')
        self.assertEqual(self.finance()['promedio'],'1100.0000')
        self.assertEqual(self.client.get('/api/comercial/pedidos').json(),before)

    def test_used_product_unit_is_locked(self):
        self.order()
        response=self.client.put(f'/api/gestion/productos/{self.p["id"]}',json={'codigo':'TOM','descripcion':'Tomate','unidad_venta':'unidad'})
        self.assertEqual(response.status_code,409)

    def test_receipt_payload_conflict_and_multiple_lines_atomic_rollback(self):
        other=self.create_product('BAD','Negativo')
        with sqlite3.connect(database.DB_PATH) as conn:
            conn.execute('UPDATE productos SET stock=-1 WHERE id=?',(other['id'],))
        order,_=self.order(quantity='1',price='1',extra={'producto_id':other['id'],'cantidad':'1','precio':'1'})
        body={'clave_operacion':str(uuid4()),'lineas':[{'linea_id':line['id'],'bruto_kg':'1','tara_kg':'0','precio':'1'} for line in order['lineas']]}
        self.assertEqual(self.receive(order,body).status_code,409)
        self.assertEqual(Decimal(self.finance()['stock']),0)
        self.assertEqual(self.client.get('/api/comercial/pedidos').json()[0]['recepciones'],[])
        with sqlite3.connect(database.DB_PATH) as conn:
            conn.execute('UPDATE productos SET stock=0 WHERE id=?',(other['id'],))
        self.assertEqual(self.receive(order,body).status_code,201)
        body['referencia']='Distinta'
        self.assertEqual(self.receive(order,body).status_code,409)

    def test_migration_repeatable_and_no_duplicate_events(self):
        self.adjust('1.2345')
        database.inicializar_db();database.inicializar_db()
        self.assertEqual(self.finance()['precio'],'1.2345')
        self.assertEqual(len(self.finance()['historial']),1)

    def test_unknown_legacy_stock_cost_is_not_invented(self):
        with sqlite3.connect(database.DB_PATH) as conn:
            conn.execute('UPDATE productos SET stock=10,precio_costo=0 WHERE id=?',(self.p['id'],))
        order,_=self.order()
        self.assertEqual(self.receive(order,self.receipt_body(order)).status_code,201)
        self.assertIsNone(self.finance()['promedio'])
        self.assertEqual(self.finance()['reposicion'],'1100.0000')
        self.assertEqual(Decimal(self.finance()['stock']),30)

    def test_extreme_unit_cost_rejected_without_side_effect(self):
        order,_=self.order(quantity='0.001',price='1')
        body=self.receipt_body(order,bruto_kg='0.001',tara_kg='0',precio='1')
        body['flete']='999999999999.99'
        self.assertEqual(self.receive(order,body).status_code,422)
        self.assertEqual(Decimal(self.finance()['stock']),0)

    def test_variable_box_total_determines_real_cost_per_kg(self):
        order,_=self.order()
        body=self.receipt_body(order,bruto_kg='19',tara_kg='1')
        body['lineas'][0].pop('precio')
        body['lineas'][0]['importe_mercaderia']='20000'
        response=self.receive(order,body)
        self.assertEqual(response.status_code,201,response.text)
        line=response.json()['lineas'][0]
        self.assertEqual(line['aceptado'],'18')
        self.assertEqual(line['subtotal'],'20000')
        self.assertEqual(line['costo_unitario'],'1222.2222')
        self.assertEqual(response.json()['total'],'22000')

    def test_reception_requires_one_unambiguous_pricing_basis(self):
        order,_=self.order()
        body=self.receipt_body(order)
        body['lineas'][0]['importe_mercaderia']='100'
        self.assertEqual(self.receive(order,body).status_code,422)
        body['lineas'][0].pop('precio');body['lineas'][0].pop('importe_mercaderia')
        self.assertEqual(self.receive(order,body).status_code,422)


if __name__=='__main__':
    unittest.main()
