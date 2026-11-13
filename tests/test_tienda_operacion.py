import json
import sqlite3
import time
import unittest
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime,timedelta,timezone
from unittest.mock import patch
from uuid import uuid4
from decimal import Decimal
from fastapi import HTTPException
from fastapi.testclient import TestClient
from db import database
import stock
import test_tienda as fixtures
from main import app


class OperacionTests(unittest.TestCase):
    setUp=fixtures.TiendaTests.setUp
    tearDown=fixtures.TiendaTests.tearDown
    create_product=fixtures.TiendaTests.create_product
    publish=fixtures.TiendaTests.publish
    body=fixtures.TiendaTests.body
    create=fixtures.TiendaTests.create
    prepare=fixtures.TiendaTests.prepare
    read=fixtures.TiendaTests.read

    def slot(self,cupo=3):
        start=datetime.now(timezone.utc)+timedelta(hours=1)
        r=self.owner.post('/api/gestion/tienda/franjas',json={'inicio':start.isoformat(),'fin':(start+timedelta(hours=1)).isoformat(),'cupo':cupo})
        self.assertEqual(r.status_code,201,r.text);return r.json()

    def book(self,cupo=3,**extra):
        slot=self.slot(cupo);self.publish()
        body=self.body(franja_id=slot['id'],**extra)
        r=self.customer.post('/api/tienda/pedidos',json=body)
        self.assertEqual(r.status_code,201,r.text);return r.json(),slot,body

    def cancel(self,order):
        return self.customer.post('/api/tienda/pedidos/'+order['id']+'/cancelacion',json={'version':order['version'],'clave_operacion':str(uuid4())},headers={'X-Pedido-Acceso':self.access})

    def approve(self,order):
        r=self.customer.post('/api/tienda/pedidos/'+order['id']+'/aprobacion',json={'version':order['version'],'clave_operacion':str(uuid4()),'aceptar':True},headers={'X-Pedido-Acceso':self.access})
        self.assertEqual(r.status_code,200,r.text);return r.json()

    def deliver(self,order,**extra):
        data={'version':order['version'],'clave_operacion':str(uuid4()),'medio':'efectivo','importe':order['final'],'referencia':'Contado en caja','cobro_verificado':True,**extra}
        return self.owner.post('/api/gestion/tienda/pedidos/'+order['id']+'/entrega',json=data)

    def test_budget_guards_estimate_and_final(self):
        self.publish()
        self.assertEqual(self.customer.post('/api/tienda/pedidos',json=self.body(presupuesto='1999')).status_code,422)
        order=self.create(self.body(presupuesto='2100'))
        self.assertEqual(self.prepare(order).status_code,422)
        r=self.prepare(order,gross='1',tare='0');self.assertEqual(r.status_code,200,r.text)
        self.assertEqual(r.json()['final'],'2000.00')

    def test_replacements_restricted_and_final_approval_required(self):
        replacement=self.create_product('ALT','Tomate redondo',price='1500');self.publish(replacement)
        body=self.body();body['lineas'][0]['reemplazo']='no_reemplazar';order=self.create(body)
        lines=[{'producto_id':self.product['id'],'reemplazo_id':replacement['id'],'bruto':'1'}]
        self.assertEqual(self.prepare(order,lineas=lines).status_code,422)
        order=self.create();r=self.prepare(order,lineas=lines);self.assertEqual(r.status_code,200,r.text)
        result=r.json();self.assertEqual(result['estado'],'por_aprobar');self.assertEqual(result['final'],'1500.00')
        self.assertEqual(result['preparacion'][0]['nombre'],'Tomate redondo')
        self.assertNotIn('costo',str(result['preparacion']))
        self.assertEqual(result['preparacion'][0]['solicitado_id'],self.product['id'])
        self.approve(result)

    def test_multiple_replacements_for_same_product_share_reservation(self):
        other=self.create_product('OTR','Otra verdura');self.publish(other)
        replacement=self.create_product('ALT','Alternativa',price='2000');self.publish(replacement)
        slot=self.slot();self.publish();body=self.body(franja_id=slot['id']);body['lineas'].append({'producto_id':other['id'],'cantidad':'1','precio_esperado':'2000','unidad':'kg'})
        order=self.customer.post('/api/tienda/pedidos',json=body).json()
        prepared=self.prepare(order,lineas=[{'producto_id':ident,'reemplazo_id':replacement['id'],'bruto':'1'} for ident in [self.product['id'],other['id']]])
        self.assertEqual(prepared.status_code,200,prepared.text)
        with database.conectar() as conn:
            self.assertEqual(stock.reserved_web(conn,replacement['id']),Decimal(2))
            self.assertEqual(stock.reserved_web(conn,self.product['id']),Decimal(0))

    def test_cannot_omit_all_items(self):
        order=self.create()
        self.assertEqual(self.prepare(order,lineas=[{'producto_id':self.product['id'],'omitir':True}]).status_code,422)

    def test_atomic_capacity_and_cancel_releases_slot(self):
        order,slot,body=self.book(cupo=1)
        self.assertTrue(order['reserva'])
        self.assertEqual(self.customer.post('/api/tienda/pedidos',json=self.body(franja_id=slot['id'])).status_code,409)
        self.assertEqual(self.customer.post('/api/tienda/pedidos',json=body).json()['id'],order['id'])
        self.assertEqual(self.cancel(order).status_code,200)
        self.assertEqual(self.customer.post('/api/tienda/pedidos',json=self.body(franja_id=slot['id'])).status_code,201)

    def test_expiration_releases_stock_and_capacity_without_background_job(self):
        order,slot,body=self.book(cupo=1)
        with sqlite3.connect(database.DB_PATH) as conn:
            conn.execute('UPDATE pedidos_web SET vence_reserva=? WHERE id=?',(time.time()-1,order['id']))
            conn.execute('UPDATE reservas_web SET vence=? WHERE pedido_id=?',(time.time()-1,order['id']))
        result=self.read(order).json();self.assertEqual(result['estado'],'vencido');self.assertFalse(result['reserva'])
        self.assertEqual(self.customer.post('/api/tienda/pedidos',json=self.body(franja_id=slot['id'])).status_code,201)
        self.assertEqual(self.prepare(result).status_code,409)

    def test_pos_and_legacy_cannot_consume_reserved_stock(self):
        order,slot,body=self.book()
        with database.conectar() as conn:
            self.assertEqual(stock.free_web(conn,self.product['id']),Decimal(14))
            with self.assertRaises(HTTPException):
                stock.consume_sale(conn,self.product['id'],Decimal(15),999,999)
            conn.rollback()
        self.cancel(order)
        with database.conectar() as conn:self.assertEqual(stock.free_web(conn,self.product['id']),Decimal(15))

    def test_preparation_reserves_real_weight_and_excludes_itself(self):
        order,slot,body=self.book()
        result=self.prepare(order,gross='1.5',tare='0').json()
        with database.conectar() as conn:self.assertEqual(stock.reserved_web(conn,self.product['id']),Decimal('1.5'))
        updated=self.prepare(result,gross='1.4',tare='0');self.assertEqual(updated.status_code,200,updated.text)
        with database.conectar() as conn:self.assertEqual(stock.reserved_web(conn,self.product['id']),Decimal('1.4'))

    def test_stock_contention_rolls_back_order_and_slot(self):
        slot=self.slot();self.publish()
        first=self.body(franja_id=slot['id']);first['lineas'][0]['cantidad']='14'
        self.assertEqual(self.customer.post('/api/tienda/pedidos',json=first).status_code,201)
        second=self.body(franja_id=slot['id']);second['lineas'][0]['cantidad']='2'
        self.assertEqual(self.customer.post('/api/tienda/pedidos',json=second).status_code,409)
        with sqlite3.connect(database.DB_PATH) as conn:self.assertEqual(conn.execute('SELECT COUNT(*) FROM pedidos_web').fetchone()[0],1)

    def test_two_clients_compete_for_last_slot(self):
        slot=self.slot(cupo=1);self.publish()
        bodies=[self.body(franja_id=slot['id']),self.body(franja_id=slot['id'])]
        def submit(body):
            client=TestClient(app,base_url='https://www.nativa.ar')
            try:return client.post('/api/tienda/pedidos',json=body).status_code
            finally:client.close()
        with ThreadPoolExecutor(max_workers=2) as pool:statuses=list(pool.map(submit,bodies))
        self.assertEqual(sorted(statuses),[201,409])

    def test_pause_required_slot_and_invalid_slot(self):
        self.publish()
        config={'abierta':False,'requiere_franja':True,'reserva_minutos':60,'contacto':'Consultar al local'}
        self.owner.put('/api/gestion/tienda/configuracion',json=config)
        self.assertEqual(self.customer.post('/api/tienda/pedidos',json=self.body()).status_code,409)
        config['abierta']=True;self.owner.put('/api/gestion/tienda/configuracion',json=config)
        self.assertEqual(self.customer.post('/api/tienda/pedidos',json=self.body()).status_code,422)
        self.assertEqual(self.customer.post('/api/tienda/pedidos',json=self.body(franja_id=999)).status_code,409)

    def test_reorder_updates_prices_and_does_not_create_or_pay(self):
        order=self.create()
        with sqlite3.connect(database.DB_PATH) as conn:conn.execute('UPDATE productos SET venta_exacta=? WHERE id=?',('2500',self.product['id']))
        result=self.customer.get('/api/tienda/pedidos/'+order['id']+'/repetir',headers={'X-Pedido-Acceso':self.access})
        self.assertEqual(result.status_code,200,result.text);self.assertEqual(result.json()['lineas'][0]['precio'],'2500')
        self.assertTrue(result.json()['cambios'])
        self.publish(visible=False)
        self.assertEqual(self.customer.get('/api/tienda/pedidos/'+order['id']+'/repetir',headers={'X-Pedido-Acceso':self.access}).json()['lineas'],[])
        with sqlite3.connect(database.DB_PATH) as conn:self.assertEqual(conn.execute('SELECT COUNT(*) FROM pedidos_web').fetchone()[0],1)

    def test_complaint_token_idempotency_and_reply(self):
        order=self.create();base='/api/tienda/pedidos/'+order['id']+'/reclamos';headers={'X-Pedido-Acceso':self.access}
        body={'clave_operacion':str(uuid4()),'producto_id':self.product['id'],'tipo':'calidad','detalle':'Necesito consultar por el producto'}
        self.assertEqual(self.customer.post(base,json=body).status_code,404)
        first=self.customer.post(base,json=body,headers=headers);self.assertEqual(first.status_code,201,first.text)
        retry=self.customer.post(base,json=body,headers=headers);self.assertEqual(first.json()['id'],retry.json()['id'])
        claim=first.json();data={'version':claim['version'],'clave_operacion':str(uuid4()),'estado':'resuelto','texto':'Coordinamos la revisión del producto con vos.'}
        endpoint='/api/gestion/tienda/pedidos/'+order['id']+'/reclamos/'+claim['id']
        self.assertEqual(self.owner.post(endpoint,json=data).status_code,200)
        self.assertEqual(self.owner.post(endpoint,json=data).status_code,200)
        reply=self.customer.get(base,headers=headers).json()[0]
        self.assertEqual(reply['estado'],'resuelto');self.assertEqual(len(reply['respuestas']),1)
        self.assertNotIn('responsable',str(reply))

    def test_delivery_consumes_once_and_manual_payment_must_match(self):
        order,slot,body=self.book();prepared=self.prepare(order,gross='1',tare='0').json();approved=self.approve(prepared)
        self.assertEqual(self.deliver(approved,importe='1').status_code,422)
        key=str(uuid4());delivered=self.deliver(approved,clave_operacion=key)
        self.assertEqual(delivered.status_code,200,delivered.text);self.assertEqual(delivered.json()['estado'],'entregado')
        self.assertEqual(self.deliver(approved,clave_operacion=key).status_code,200)
        with database.conectar() as conn:
            self.assertEqual(stock.physical(conn,self.product['id']),Decimal(14));self.assertEqual(stock.reserved_web(conn,self.product['id']),Decimal(0))
            self.assertEqual(conn.execute("SELECT COUNT(*) FROM movimientos_stock WHERE tipo='venta_web'").fetchone()[0],1)
        self.assertEqual(self.cancel(delivered.json()).status_code,409)

    def test_profit_unknown_costs_not_zero_and_no_public_exposure(self):
        order=self.create();prepared=self.prepare(order,gross='1',tare='0').json()
        endpoint='/api/gestion/tienda/pedidos/'+order['id']
        before=self.owner.get(endpoint+'/rentabilidad').json();self.assertIsNone(before['contribucion'])
        expenses={'version':prepared['version'],'clave_operacion':str(uuid4()),'empaque':'100','comision':'50','minutos':'10','valor_hora':'600','reparto':'0','incidencias':'0'}
        result=self.owner.post(endpoint+'/costos',json=expenses);self.assertEqual(result.status_code,200,result.text)
        report=self.owner.get(endpoint+'/rentabilidad').json();self.assertEqual(report['gastos_variables'],'250.00');self.assertEqual(report['contribucion'],'1627.00')
        self.assertEqual(self.customer.get(endpoint+'/rentabilidad').status_code,404)
        public=self.read(order).text
        self.assertNotIn('costos_base',public);self.assertNotIn('contribucion',public);self.assertNotIn('precio_costo',public)

    def test_missing_cost_keeps_contribution_unknown(self):
        with sqlite3.connect(database.DB_PATH) as conn:conn.execute('UPDATE productos SET promedio_exacto=NULL,precio_costo=NULL WHERE id=?',(self.product['id'],))
        order=self.create();prepared=self.prepare(order,gross='1',tare='0').json()
        self.owner.post('/api/gestion/tienda/pedidos/'+order['id']+'/costos',json={'version':prepared['version'],'clave_operacion':str(uuid4()),'empaque':'0','comision':'0','minutos':'0','valor_hora':'0','reparto':'0','incidencias':'0'})
        result=self.owner.get('/api/gestion/tienda/pedidos/'+order['id']+'/rentabilidad').json()
        self.assertIsNone(result['mercaderia']);self.assertIsNone(result['contribucion']);self.assertFalse(result['completo'])

    def test_slot_rejects_timezone_missing_overlap_and_closure(self):
        slot=self.slot()
        overlap={'inicio':slot['inicio'],'fin':slot['fin'],'cupo':1}
        self.assertEqual(self.owner.post('/api/gestion/tienda/franjas',json=overlap).status_code,409)
        overlap['inicio']=overlap['inicio'][:19]
        self.assertEqual(self.owner.post('/api/gestion/tienda/franjas',json=overlap).status_code,422)
        self.owner.delete('/api/gestion/tienda/franjas/'+str(slot['id']));self.publish()
        self.assertEqual(self.customer.post('/api/tienda/pedidos',json=self.body(franja_id=slot['id'])).status_code,409)

    def test_approval_holds_reservation_until_slot_end(self):
        order,slot,body=self.book()
        approved=self.approve(self.prepare(order,gross='1',tare='0').json())
        self.assertEqual(approved['vence_reserva'],datetime.fromisoformat(slot['fin']).timestamp())
        with database.conectar() as conn:
            self.assertEqual(conn.execute('SELECT vence FROM reservas_web WHERE pedido_id=?',(order['id'],)).fetchone()[0],approved['vence_reserva'])

    def test_cancel_retry_does_not_release_someone_elses_reservation(self):
        order,slot,body=self.book();payload={'version':order['version'],'clave_operacion':str(uuid4())}
        path='/api/tienda/pedidos/'+order['id']+'/cancelacion';headers={'X-Pedido-Acceso':self.access}
        self.assertEqual(self.customer.post(path,json=payload,headers=headers).status_code,200)
        second=self.customer.post('/api/tienda/pedidos',json=self.body(franja_id=slot['id'])).json()
        self.assertEqual(self.customer.post(path,json=payload,headers=headers).status_code,200)
        with database.conectar() as conn:
            self.assertEqual(stock.reserved_web(conn,self.product['id']),Decimal(1))
            self.assertEqual(conn.execute('SELECT pedido_id FROM reservas_web').fetchone()[0],second['id'])

    def test_replacement_respects_target_unit_and_missing_line_releases_only_that_stock(self):
        other=self.create_product('AT','Perejil','atado');self.publish(other)
        order,slot,body=self.book()
        r=self.prepare(order,lineas=[{'producto_id':self.product['id'],'reemplazo_id':other['id'],'cantidad':'0.5'}])
        self.assertEqual(r.status_code,422)
        r=self.prepare(order,lineas=[{'producto_id':self.product['id'],'reemplazo_id':other['id'],'cantidad':'2'}])
        self.assertEqual(r.status_code,200,r.text)
        self.assertEqual(r.json()['preparacion'][0]['unidad'],'atado')
        with database.conectar() as conn:
            self.assertEqual(stock.reserved_web(conn,self.product['id']),Decimal(0))
            self.assertEqual(stock.reserved_web(conn,other['id']),Decimal(2))

    def test_last_stock_concurrent_orders_do_not_oversell(self):
        slot=self.slot(cupo=2);self.publish();bodies=[]
        for _ in range(2):
            body=self.body(franja_id=slot['id']);body['lineas'][0]['cantidad']='10';bodies.append(body)
        def submit(body):
            client=TestClient(app,base_url='https://www.nativa.ar')
            try:return client.post('/api/tienda/pedidos',json=body).status_code
            finally:client.close()
        with ThreadPoolExecutor(max_workers=2) as pool:statuses=list(pool.map(submit,bodies))
        self.assertEqual(sorted(statuses),[201,409])
        with database.conectar() as conn:
            self.assertEqual(stock.reserved_web(conn,self.product['id']),Decimal(10))
            self.assertEqual(conn.execute('SELECT COUNT(*) FROM pedidos_web').fetchone()[0],1)

    def test_legacy_request_retry_after_new_optional_fields(self):
        import hashlib
        body=self.body();order=self.create(body)
        legacy={k:v for k,v in body.items() if k not in ('presupuesto','franja_id')}
        for line in legacy['lineas']:line.pop('reemplazo',None)
        digest=hashlib.sha256(json.dumps(legacy,sort_keys=True,separators=(',',':')).encode()).hexdigest()
        with sqlite3.connect(database.DB_PATH) as conn:conn.execute('UPDATE pedidos_web SET payload=? WHERE id=?',(digest,order['id']))
        retry=self.customer.post('/api/tienda/pedidos',json=body)
        self.assertEqual(retry.status_code,201,retry.text);self.assertEqual(retry.json()['id'],order['id'])

    def test_inventory_and_planning_include_web_reservations_and_deliveries(self):
        order,slot,body=self.book()
        summary=self.owner.get('/api/inventario/resumen')
        self.assertEqual(summary.status_code,200,summary.text)
        item=next(p for p in summary.json()['productos'] if p['id']==self.product['id'])
        self.assertEqual(item['reservado_web'],'1');self.assertEqual(Decimal(item['libre_para_venta']),Decimal(14))
        approved=self.approve(self.prepare(order,gross='1',tare='0').json());self.assertEqual(self.deliver(approved).status_code,200)
        plan=self.owner.get('/api/mostrador/plan').json()
        self.assertEqual(Decimal(next(p for p in plan['reposicion'] if p['id']==self.product['id'])['vendido_periodo']),Decimal(1))

    def test_specific_alternative_is_bounded_to_chosen_product(self):
        allowed=self.create_product('ALT','Alternativa elegida');self.publish(allowed)
        other=self.create_product('OTR','Otra alternativa');self.publish(other)
        body=self.body();body['lineas'][0].update(reemplazo='alternativa',alternativa_id=allowed['id'])
        order=self.create(body)
        wrong=self.prepare(order,lineas=[{'producto_id':self.product['id'],'reemplazo_id':other['id'],'bruto':'1'}])
        self.assertEqual(wrong.status_code,422)
        right=self.prepare(order,lineas=[{'producto_id':self.product['id'],'reemplazo_id':allowed['id'],'bruto':'1'}])
        self.assertEqual(right.status_code,200,right.text)
        self.assertEqual(right.json()['estado'],'por_aprobar')

    def test_deterioration_after_reservation_warns_staff_and_blocks_approval(self):
        order,slot,body=self.book();prepared=self.prepare(order,gross='1',tare='0').json()
        with sqlite3.connect(database.DB_PATH) as conn:conn.execute("UPDATE lotes_stock SET estado='no_apto' WHERE producto_id=?",(self.product['id'],))
        listing=self.owner.get('/api/gestion/tienda/pedidos').json()
        self.assertTrue(next(p for p in listing if p['id']==order['id'])['alerta_reserva'])
        result=self.customer.post('/api/tienda/pedidos/'+order['id']+'/aprobacion',json={'version':prepared['version'],'clave_operacion':str(uuid4()),'aceptar':True},headers={'X-Pedido-Acceso':self.access})
        self.assertEqual(result.status_code,409)
        self.assertEqual(self.read(order).json()['estado'],'por_aprobar')

    def test_closed_slot_with_existing_commitments_cannot_be_duplicated(self):
        order,slot,body=self.book()
        self.owner.delete('/api/gestion/tienda/franjas/'+str(slot['id']))
        duplicate={'inicio':slot['inicio'],'fin':slot['fin'],'cupo':3}
        self.assertEqual(self.owner.post('/api/gestion/tienda/franjas',json=duplicate).status_code,409)
        self.cancel(order)
        self.assertEqual(self.owner.post('/api/gestion/tienda/franjas',json=duplicate).status_code,201)
