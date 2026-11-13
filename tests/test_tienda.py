import io
import json
import os
import secrets
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from uuid import uuid4
from fastapi.testclient import TestClient
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'backend'))
from db import database
from main import app
from routers import preparacion


class TiendaTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.old_db, self.old_media = database.DB_PATH, preparacion.MEDIA_DIR
        database.DB_PATH = self.temp.name + '/tienda.db'
        preparacion.MEDIA_DIR = self.temp.name + '/photos'
        self.context = TestClient(app, base_url='https://testserver')
        self.owner = self.context.__enter__()
        credentials = {'nombre': 'Juliana de prueba', 'clave': 'solo-pruebas-123'}
        self.owner.post('/api/comercial/responsables', json=credentials)
        self.owner.post('/api/comercial/sesion', json=credentials)
        self.product = self.create_product('TOM', 'Tomate perita')
        self.mode = patch.dict(os.environ, NATIVA_ENV='production', NATIVA_PUBLIC_HOSTS='www.nativa.ar,nativa.ar')
        self.mode.start()
        self.customer = TestClient(app, base_url='https://www.nativa.ar')
        self.access = secrets.token_urlsafe(32)

    def tearDown(self):
        self.customer.close()
        self.mode.stop()
        self.context.__exit__(None, None, None)
        database.DB_PATH, preparacion.MEDIA_DIR = self.old_db, self.old_media
        self.temp.cleanup()

    def create_product(self, code, name, unit='kg', price='2000', with_photo=True):
        response = self.owner.post('/api/gestion/productos', json={'codigo': code, 'descripcion': name, 'unidad_venta': unit})
        self.assertEqual(response.status_code, 201, response.text)
        product = response.json()
        with sqlite3.connect(database.DB_PATH) as conn:
            conn.execute('UPDATE productos SET venta_exacta=?,precio_venta=?,precio_costo=123,stock=15 WHERE id=?', (price, price, product['id']))
        if with_photo:
            stream = io.BytesIO();Image.new('RGB', (70, 70), '#db7044').save(stream, 'PNG')
            photo = self.owner.post(f'/api/gestion/productos/{product["id"]}/foto', files={'archivo': ('producto.png', stream.getvalue(), 'image/png')})
            self.assertEqual(photo.status_code, 200, photo.text)
        return product

    def publish(self, product=None, visible=True):
        product = product or self.product
        return self.owner.put(f'/api/gestion/tienda/productos/{product["id"]}', json={'visible': visible})

    def body(self, product=None, **extra):
        product = product or self.product
        return {'clave_operacion': str(uuid4()), 'acceso': self.access, 'nombre': 'Vecina de prueba', 'telefono': '3541 123456',
                'lineas': [{'producto_id': product['id'], 'cantidad': '1', 'precio_esperado': '2000', 'unidad': product['unidad_venta']}], **extra}

    def create(self, body=None):
        self.publish()
        response = self.customer.post('/api/tienda/pedidos', json=body or self.body())
        self.assertEqual(response.status_code, 201, response.text)
        return response.json()

    def prepare(self, order, gross='1.100', tare='0.020', **extra):
        data = {'version': order['version'], 'clave_operacion': str(uuid4()), 'lineas': [{'producto_id': self.product['id'], 'bruto': gross, 'tara': tare}], **extra}
        return self.owner.post('/api/gestion/tienda/pedidos/'+order['id']+'/pesaje', json=data)

    def read(self, order, token=None):
        return self.customer.get('/api/tienda/pedidos/'+order['id'], headers={'X-Pedido-Acceso': token or self.access})

    def test_explicit_publication_and_no_private_fields(self):
        self.assertEqual(self.customer.get('/api/tienda/catalogo').json()['productos'], [])
        self.assertEqual(self.publish().status_code, 200)
        catalog = self.customer.get('/api/tienda/catalogo')
        product = catalog.json()['productos'][0]
        self.assertEqual(product['nombre'], 'Tomate perita')
        self.assertEqual(product['precio'], '2000')
        self.assertEqual(set(product), {'id','nombre','categoria','variedad','presentacion','unidad','precio','foto','disponibilidad','promocion'})
        for private in ('precio_costo', 'stock', 'sal', 'clave_hash', 'medios_pago'):
            self.assertNotIn('"'+private+'":', catalog.text)
        self.assertEqual(self.customer.get(product['foto']).headers['content-type'], 'image/jpeg')

    def test_cannot_publish_without_photo_price_or_active(self):
        missing = self.create_product('SIN', 'Sin foto', with_photo=False)
        self.assertEqual(self.publish(missing).status_code, 422)
        for values in [('0', 1), ('2000', 0)]:
            with sqlite3.connect(database.DB_PATH) as conn:
                conn.execute('UPDATE productos SET venta_exacta=?,activo=? WHERE id=?', (*values, self.product['id']))
            self.assertEqual(self.publish().status_code, 422)

    def test_hidden_and_missing_photos_are_not_public(self):
        self.publish()
        self.publish(visible=False)
        self.assertEqual(self.customer.get(f'/api/tienda/productos/{self.product["id"]}/foto').status_code, 404)
        self.assertEqual(self.customer.get('/media/arbitrary.jpg').status_code, 404)
        self.publish()
        for path in Path(preparacion.MEDIA_DIR).glob('*.jpg'): path.unlink()
        self.assertEqual(self.customer.get('/api/tienda/catalogo').json()['productos'], [])

    def test_public_host_does_not_serve_administration_even_with_staff_session(self):
        self.assertIn('Lo fresco del barrio', self.customer.get('/').text)
        self.assertEqual(self.customer.get('/tienda').status_code, 200)
        self.assertEqual(self.customer.get('/static/tienda.js').status_code, 200)
        self.customer.cookies.update(self.owner.cookies)
        for path in ('/api/gestion/productos', '/api/comercial/productos', '/ventas', '/login', '/docs', '/api/gestion/tienda/pedidos'):
            self.assertEqual(self.customer.get(path).status_code, 404, path)
        guest = TestClient(app, base_url='https://sistema.nativa.ar')
        self.assertEqual(guest.get('/api/gestion/tienda/productos').status_code, 401)
        guest.close()

    def test_guest_request_is_estimated_and_does_not_consume_stock_or_charge(self):
        order = self.create()
        self.assertEqual(order['estado'], 'recibido')
        self.assertEqual(order['estimado'], '2000.00')
        self.assertIsNone(order['final'])
        self.assertFalse(order['reserva'])
        self.assertEqual(order['pago'], 'no_cobrado')
        with sqlite3.connect(database.DB_PATH) as conn:
            self.assertEqual(conn.execute('SELECT stock FROM productos WHERE id=?', (self.product['id'],)).fetchone()[0], 15)
            self.assertEqual(conn.execute('SELECT COUNT(*) FROM ventas_pos').fetchone()[0], 0)
            self.assertNotIn(self.access, str(conn.execute('SELECT * FROM pedidos_web').fetchall()))

    def test_guest_retry_and_conflicting_idempotency(self):
        self.publish();body=self.body()
        first=self.customer.post('/api/tienda/pedidos',json=body)
        retry=self.customer.post('/api/tienda/pedidos',json=body)
        self.assertEqual(first.json()['id'],retry.json()['id'])
        body['nombre']='Otra persona'
        self.assertEqual(self.customer.post('/api/tienda/pedidos',json=body).status_code,409)
        with sqlite3.connect(database.DB_PATH) as conn:
            self.assertEqual(conn.execute('SELECT COUNT(*) FROM pedidos_web').fetchone()[0],1)

    def test_tampered_price_unit_hidden_product_and_invalid_amount(self):
        self.publish()
        for change in [{'precio_esperado':'1'},{'unidad':'unidad'},{'cantidad':'0'},{'cantidad':'NaN'},{'cantidad':'0.0001'}]:
            body=self.body();body['lineas'][0].update(change)
            self.assertIn(self.customer.post('/api/tienda/pedidos',json=body).status_code,(409,422))
        self.publish(visible=False)
        self.assertEqual(self.customer.post('/api/tienda/pedidos',json=self.body()).status_code,409)

    def test_secret_access_is_required_and_not_in_response(self):
        order=self.create()
        self.assertEqual(self.customer.get('/api/tienda/pedidos/'+order['id']).status_code,404)
        self.assertEqual(self.read(order,'incorrecto').status_code,404)
        result=self.read(order)
        self.assertEqual(result.status_code,200)
        self.assertNotIn('telefono',result.json())
        self.assertNotIn(self.access,result.text)
        self.assertNotIn('acceso_hash',result.text)

    def test_prepare_real_net_and_customer_approval_no_payment(self):
        order=self.create();prepared=self.prepare(order)
        self.assertEqual(prepared.status_code,200,prepared.text)
        prepared=prepared.json();self.assertEqual(prepared['final'],'2160.00')
        self.assertEqual(prepared['preparacion'][0]['cantidad'],'1.080')
        self.assertEqual(prepared['lineas'][0]['cantidad'],'1')
        self.assertEqual(prepared['estado'],'por_aprobar')
        data={'version':prepared['version'],'clave_operacion':str(uuid4()),'aceptar':True}
        endpoint='/api/tienda/pedidos/'+order['id']+'/aprobacion'
        self.assertEqual(self.customer.post(endpoint,json=data).status_code,404)
        response=self.customer.post(endpoint,json=data,headers={'X-Pedido-Acceso':self.access})
        self.assertEqual(response.status_code,200,response.text)
        self.assertEqual(response.json()['estado'],'confirmado')
        self.assertEqual(response.json()['pago'],'no_cobrado')
        self.assertEqual(self.customer.post(endpoint,json=data,headers={'X-Pedido-Acceso':self.access}).json(),response.json())
        self.assertEqual(self.prepare(response.json()).status_code,409)

    def test_stale_approval_and_repreparation(self):
        order=self.create();first=self.prepare(order).json();second=self.prepare(first,gross='0.900').json()
        body={'version':first['version'],'clave_operacion':str(uuid4()),'aceptar':True}
        endpoint='/api/tienda/pedidos/'+order['id']+'/aprobacion'
        self.assertEqual(self.customer.post(endpoint,json=body,headers={'X-Pedido-Acceso':self.access}).status_code,409)
        body.update(version=second['version'],clave_operacion=str(uuid4()),aceptar=False)
        rejected=self.customer.post(endpoint,json=body,headers={'X-Pedido-Acceso':self.access}).json()
        self.assertEqual(rejected['estado'],'revisar')
        self.assertEqual(self.prepare(rejected).status_code,200)

    def test_preparation_is_idempotent_and_preserves_requested_price(self):
        order=self.create()
        with sqlite3.connect(database.DB_PATH) as conn:
            conn.execute('UPDATE productos SET venta_exacta=? WHERE id=?',('9999',self.product['id']))
        key=str(uuid4())
        response=self.prepare(order,clave_operacion=key)
        self.assertEqual(response.json()['final'],'2160.00')
        self.assertEqual(self.prepare(order,clave_operacion=key).json(),response.json())
        self.assertEqual(self.prepare(order,gross='2',clave_operacion=key).status_code,409)

    def test_invalid_tare_extra_products_and_integer_presentations(self):
        order=self.create()
        for gross,tare in [('1','2'),('1','1')]:
            self.assertEqual(self.prepare(order,gross,tare).status_code,422)
        self.assertEqual(self.prepare(order,lineas=[]).status_code,422)
        self.assertEqual(self.prepare(order,lineas=[{'producto_id':999,'bruto':'1'}]).status_code,422)
        other=self.create_product('PER','Perejil','atado');self.publish(other)
        body=self.body(other);body['lineas'][0]['cantidad']='0.5'
        self.assertEqual(self.customer.post('/api/tienda/pedidos',json=body).status_code,422)
        body['lineas'][0]['cantidad']='2'
        other_order=self.customer.post('/api/tienda/pedidos',json=body).json()
        response=self.owner.post('/api/gestion/tienda/pedidos/'+other_order['id']+'/pesaje',json={'version':1,'clave_operacion':str(uuid4()),'lineas':[{'producto_id':other['id'],'cantidad':'2'}]})
        self.assertEqual(response.json()['final'],'4000.00')

    def test_rate_limit_and_retry_do_not_create_extra_orders(self):
        self.publish();first=self.body()
        for i in range(10):
            response=self.customer.post('/api/tienda/pedidos',json=first if i==0 else self.body())
            self.assertEqual(response.status_code,201)
        self.assertEqual(self.customer.post('/api/tienda/pedidos',json=self.body()).status_code,429)
        self.assertEqual(self.customer.post('/api/tienda/pedidos',json=first).status_code,201)

    def test_cross_origin_customer_submission_is_rejected(self):
        self.publish()
        self.assertEqual(self.customer.post('/api/tienda/pedidos',json=self.body(),headers={'Origin':'https://otro.example'}).status_code,403)

    def test_private_link_expires_and_cannot_approve_after_expiry(self):
        order = self.create()
        with sqlite3.connect(database.DB_PATH) as conn:
            conn.execute("UPDATE pedidos_web SET creado='2020-01-01T00:00:00.000Z' WHERE id=?", (order['id'],))
        self.assertEqual(self.read(order).status_code, 410)
        self.assertEqual(self.read(order, 'wrong-token').status_code, 404)
        response = self.customer.post('/api/tienda/pedidos/'+order['id']+'/aprobacion',
            json={'version': 1, 'clave_operacion': str(uuid4()), 'aceptar': True}, headers={'X-Pedido-Acceso': self.access})
        self.assertEqual(response.status_code, 410)

    def test_unknown_legacy_records_not_auto_published_on_restart(self):
        database.inicializar_db()
        self.assertEqual(self.customer.get('/api/tienda/catalogo').json()['productos'],[])
