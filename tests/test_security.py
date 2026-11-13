import os
import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
import test_comercial as fixtures
from main import app
from routers.comercial import Credentials, create_responsible
from fastapi import HTTPException


class SecurityTests(unittest.TestCase):
    def setUp(self):
        fixtures.ComercialTests.setUp(self)
        self.client.close()
        self.mode = patch.dict(os.environ, NATIVA_ENV='production')
        self.mode.start()
        self.client = TestClient(app, base_url='https://testserver')

    login = fixtures.ComercialTests.login
    create_product = fixtures.ComercialTests.create_product

    def tearDown(self):
        self.client.close()
        self.mode.stop()
        fixtures.ComercialTests.tearDown(self)

    def test_private_data_and_pages(self):
        for path in ('/api/estado', '/api/productos', '/api/gestion/productos', '/api/comercial/productos', '/media/missing.jpg'):
            self.assertEqual(self.client.get(path).status_code, 401, path)
        for path in ('/docs', '/openapi.json'):
            self.assertEqual(self.client.get(path, follow_redirects=False).status_code, 303)
        self.assertEqual(self.client.get('/', follow_redirects=False).status_code, 303)
        self.assertEqual(self.client.get('/login').status_code, 200)
        self.assertEqual(self.client.get('/healthz').json(), {'estado': 'ok'})

    def test_login_cookie_and_logout(self):
        response = self.login()
        cookie = response.headers['set-cookie']
        self.assertIn('Secure', cookie)
        self.assertIn('HttpOnly', cookie)
        self.assertIn('SameSite=strict', cookie)
        self.assertEqual(self.client.get('/api/gestion/productos').status_code, 200)
        self.assertEqual(self.client.get('/').headers['cache-control'], 'no-store')
        self.client.delete('/api/comercial/sesion')
        self.assertEqual(self.client.get('/api/gestion/productos').status_code, 401)

    def test_cross_origin_and_cashier_write(self):
        self.assertEqual(self.client.post('/api/comercial/sesion', json=self.owner, headers={'Origin':'https://otro.example'}).status_code, 403)
        self.login()
        self.assertEqual(self.client.post('/api/comercial/responsables', json={'nombre':'Caja','clave':'clave-caja-123','rol':'cajero'}).status_code, 201)
        self.login('Caja', 'clave-caja-123')
        self.assertEqual(self.client.post('/api/gestion/productos', json={}).status_code, 403)
        self.assertEqual(self.client.post('/api/facturacion/cualquier-cosa', json={}).status_code, 403)

    def test_bootstrap_cannot_be_taken_over(self):
        from routers.preparacion import database
        with database() as conn:
            conn.execute('DELETE FROM sesiones_comerciales')
            conn.execute('DELETE FROM responsables')
        self.assertEqual(self.client.post('/api/comercial/responsables', json=self.owner).status_code, 401)
        with self.assertRaises(HTTPException) as error:
            create_responsible(Credentials(**self.owner), cs_sesion=None)
        self.assertEqual(error.exception.status_code, 403)
