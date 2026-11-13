import sqlite3
import unittest
from datetime import datetime,timedelta,timezone
from decimal import Decimal
from unittest.mock import patch
from uuid import uuid4
from fastapi.testclient import TestClient
from db import database
from main import app
import test_tienda as fixtures


class PromocionesTests(unittest.TestCase):
    setUp=fixtures.TiendaTests.setUp
    tearDown=fixtures.TiendaTests.tearDown
    create_product=fixtures.TiendaTests.create_product
    publish=fixtures.TiendaTests.publish
    body=fixtures.TiendaTests.body
    create=fixtures.TiendaTests.create
    prepare=fixtures.TiendaTests.prepare

    def promotion(self,product=None,**extra):
        current=datetime.now(timezone.utc)
        return {'producto_id':(product or self.product)['id'],'titulo':'Oferta de temporada','precio':'1500',
                'desde':(current-timedelta(minutes=1)).isoformat(),'hasta':(current+timedelta(hours=2)).isoformat(),
                'motivo':'Promoción controlada de prueba','clave_operacion':str(uuid4()),**extra}

    def submit(self,body=None):return self.owner.post('/api/gestion/tienda/promociones',json=body or self.promotion())

    def catalog(self):return self.customer.get('/api/tienda/catalogo').json()['productos']

    def test_active_promotion_public_fields_and_regular_price_preserved(self):
        self.publish();result=self.submit();self.assertEqual(result.status_code,201,result.text)
        item=self.catalog()[0];self.assertEqual(item['precio'],'1500');self.assertEqual(item['promocion']['precio_anterior'],'2000')
        self.assertEqual(set(item['promocion']),{'id','titulo','precio_anterior','desde','hasta','precio'})
        for field in ('responsable','motivo','costo_referencia','payload'):self.assertNotIn(field,str(item))
        with sqlite3.connect(database.DB_PATH) as conn:self.assertEqual(conn.execute('SELECT venta_exacta FROM productos').fetchone()[0],'2000')

    def test_future_and_expired_promotion_change_only_current_catalog(self):
        self.publish();current=datetime.now(timezone.utc)
        data=self.promotion(desde=(current+timedelta(hours=1)).isoformat(),hasta=(current+timedelta(hours=2)).isoformat())
        self.assertEqual(self.submit(data).status_code,201)
        self.assertEqual(self.catalog()[0]['precio'],'2000')
        with patch('routers.tienda_promociones.now',return_value=current.timestamp()+4000):
            self.assertEqual(self.catalog()[0]['precio'],'1500')
        with patch('routers.tienda_promociones.now',return_value=current.timestamp()+8000):
            self.assertEqual(self.catalog()[0]['precio'],'2000');self.assertIsNone(self.catalog()[0]['promocion'])

    def test_retries_overlap_and_explicit_cancellation(self):
        self.publish();body=self.promotion();first=self.submit(body);retry=self.submit(body)
        self.assertEqual(first.status_code,201);self.assertEqual(retry.json()['id'],first.json()['id'])
        body['precio']='1400';self.assertEqual(self.submit(body).status_code,409)
        self.assertEqual(self.submit().status_code,409)
        path='/api/gestion/tienda/promociones/'+str(first.json()['id'])
        canceled=self.owner.delete(path);self.assertEqual(canceled.json()['estado'],'cancelada')
        self.assertEqual(self.owner.delete(path).json()['cancelada_en'],canceled.json()['cancelada_en'])
        self.assertEqual(self.catalog()[0]['precio'],'2000')
        self.assertEqual(self.submit().status_code,201)

    def test_price_and_unit_reference_change_suspends_offer(self):
        self.publish();self.submit()
        with sqlite3.connect(database.DB_PATH) as conn:conn.execute('UPDATE productos SET venta_exacta=? WHERE id=?',('2200',self.product['id']))
        self.assertEqual(self.catalog()[0]['precio'],'2200');self.assertIsNone(self.catalog()[0]['promocion'])
        listing=self.owner.get('/api/gestion/tienda/promociones').json()
        self.assertEqual(listing[0]['estado'],'suspendida_por_cambio')

    def test_order_keeps_agreed_discount_after_offer_ends(self):
        self.publish();promo=self.submit().json();body=self.body();body['lineas'][0]['precio_esperado']='1500'
        order=self.create(body);self.assertEqual(order['estimado'],'1500.00');self.assertEqual(order['lineas'][0]['promocion']['id'],promo['id'])
        self.owner.delete('/api/gestion/tienda/promociones/'+str(promo['id']))
        prepared=self.prepare(order,gross='1',tare='0');self.assertEqual(prepared.status_code,200,prepared.text)
        self.assertEqual(prepared.json()['final'],'1500.00')
        self.assertEqual(self.customer.post('/api/tienda/pedidos',json={**body,'clave_operacion':str(uuid4())}).status_code,409)

    def test_replacement_uses_its_current_offer_and_not_original_promotion(self):
        other=self.create_product('ALT','Otra variedad',price='1800');self.publish(other)
        self.assertEqual(self.submit(self.promotion(other,precio='1200')).status_code,201)
        order=self.create();result=self.prepare(order,lineas=[{'producto_id':self.product['id'],'reemplazo_id':other['id'],'bruto':'1'}])
        self.assertEqual(result.status_code,200,result.text);self.assertEqual(result.json()['final'],'1200.00')
        self.assertIsNotNone(result.json()['preparacion'][0]['promocion'])

    def test_below_cost_needs_explicit_owner_approval(self):
        self.assertEqual(self.submit(self.promotion(precio='100')).status_code,422)
        approved=self.submit(self.promotion(precio='100',permitir_bajo_costo=True));self.assertEqual(approved.status_code,201,approved.text)
        self.assertEqual(approved.json()['costo_referencia'],'123.0')

    def test_manager_cannot_override_below_cost_or_public_admin_access(self):
        credentials={'nombre':'Encargada prueba','clave':'clave-prueba-123','rol':'encargado'}
        self.owner.post('/api/comercial/responsables',json=credentials);self.owner.post('/api/comercial/sesion',json={'nombre':credentials['nombre'],'clave':credentials['clave']})
        self.assertEqual(self.submit(self.promotion(precio='100',permitir_bajo_costo=True)).status_code,422)
        self.assertEqual(self.customer.get('/api/gestion/tienda/promociones').status_code,404)
        self.assertEqual(self.customer.post('/api/gestion/tienda/promociones',json=self.promotion()).status_code,404)
        guest=TestClient(app,base_url='https://sistema.nativa.ar')
        self.assertEqual(guest.get('/api/gestion/tienda/promociones').status_code,401);guest.close()

    def test_decimal_gram_offer_is_not_rounded_before_quantity(self):
        product=self.create_product('GR','A granel','g',price='0.1250');self.publish(product)
        with sqlite3.connect(database.DB_PATH) as conn:conn.execute('UPDATE productos SET promedio_exacto=?,precio_costo=? WHERE id=?',('0.08',0.08,product['id']))
        result=self.submit(self.promotion(product,precio='0.1000'));self.assertEqual(result.status_code,201,result.text)
        body=self.body(product);body['lineas'][0].update(cantidad='250',precio_esperado='0.1000')
        result=self.customer.post('/api/tienda/pedidos',json=body);self.assertEqual(result.status_code,201,result.text)
        self.assertEqual(result.json()['estimado'],'25.00')

    def test_hidden_products_dates_and_non_discount_are_rejected_or_private(self):
        for data in [self.promotion(precio='2000'),self.promotion(precio='2200'),self.promotion(desde='2026-01-01T00:00:00'),self.promotion(hasta=(datetime.now(timezone.utc)-timedelta(days=1)).isoformat())]:
            self.assertEqual(self.submit(data).status_code,422)
        self.assertEqual(self.submit().status_code,201)
        self.assertEqual(self.catalog(),[])
