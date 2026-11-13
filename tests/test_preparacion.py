import io
import os
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path

from fastapi.testclient import TestClient
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))
from db import database
from routers import preparacion
from main import app


class PreparacionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.previous_db = database.DB_PATH
        self.previous_media = preparacion.MEDIA_DIR
        database.DB_PATH = os.path.join(self.temp.name, "test.db")
        preparacion.MEDIA_DIR = os.path.join(self.temp.name, "photos")
        self.context = TestClient(app)
        self.client = self.context.__enter__()

    def tearDown(self):
        self.context.__exit__(None, None, None)
        database.DB_PATH = self.previous_db
        preparacion.MEDIA_DIR = self.previous_media
        self.temp.cleanup()

    def create(self, **overrides):
        body = {"codigo": "TOM-01", "descripcion": "Tomate", "aliases": ["jitomate"], **overrides}
        return self.client.post("/api/gestion/productos", json=body)

    def test_unknown_business_data_is_pending_and_persists(self):
        initial = self.client.get("/api/gestion/negocio").json()
        self.assertEqual(initial["nombre"], "")
        self.assertEqual(initial["atencion"], "pendiente")
        self.assertFalse(initial["fiscal_revisado"])
        initial.update(nombre="La Huerta", personas=[{"nombre": "Ana", "rol": "dueno"}], medios_pago=["efectivo", "qr"])
        self.assertEqual(self.client.put("/api/gestion/negocio", json=initial).status_code, 200)
        self.assertEqual(self.client.get("/api/gestion/negocio").json(), initial)

    def test_fiscal_review_requires_information_and_does_not_destroy_previous(self):
        data = self.client.get("/api/gestion/negocio").json()
        data["fiscal_revisado"] = True
        self.assertEqual(self.client.put("/api/gestion/negocio", json=data).status_code, 422)
        self.assertFalse(self.client.get("/api/gestion/negocio").json()["fiscal_revisado"])

    def test_partial_real_business_configuration_does_not_invent_unknown_details(self):
        body={'nombre':'Nativa','localidad':'Villa Carlos Paz, Córdoba','funciones_previstas':['dueno','encargado'],'canales_venta':['local','whatsapp','retiro','reparto'],'medios_pago':['efectivo','mercado_pago','transferencia'],'tiene_contador':'si','situacion_fiscal':'Monotributo','internet':'disponible','equipos':[{'tipo':'tablet','estado':'por_comprar','notas':'Modelo pendiente'},{'tipo':'balanza','estado':'disponible'},{'tipo':'impresora','estado':'disponible','notas':'Integrada en la balanza'}]}
        response=self.client.put('/api/gestion/negocio',json=body)
        self.assertEqual(response.status_code,200)
        saved=self.client.get('/api/gestion/negocio').json()
        self.assertEqual(saved['funciones_previstas'],['dueno','encargado'])
        self.assertEqual(saved['personas'],[])
        self.assertFalse(saved['fiscal_revisado'])
        self.assertEqual(saved['comprobantes'],'')
        self.assertEqual(saved['equipos'][1]['marca_modelo'],'')

    def test_old_saved_configuration_gets_new_defaults(self):
        import json
        with sqlite3.connect(database.DB_PATH) as conn:
            conn.execute('INSERT INTO configuracion_negocio(id,datos) VALUES(1,?)',(json.dumps({'nombre':'Local anterior'}),))
        saved=self.client.get('/api/gestion/negocio').json()
        self.assertEqual(saved['nombre'],'Local anterior')
        self.assertEqual(saved['canales_venta'],[])
        self.assertEqual(saved['tiene_contador'],'pendiente')

    def test_roles_payments_and_unknown_fields_are_validated(self):
        for body in [{"personas": [{"nombre":" ","rol":"cajero"}]}, {"medios_pago":["efectivo","efectivo"]}, {"personas":[{"nombre":"Ana","rol":"superadmin"}]}, {"api_key":"not-supported"}]:
            with self.subTest(body=body):
                self.assertEqual(self.client.put("/api/gestion/negocio",json=body).status_code,422)

    def test_create_search_edit_without_touching_prices_or_stock(self):
        response = self.create(variedad="Perita", calidad="Primera", presentacion="Suelto")
        self.assertEqual(response.status_code, 201)
        product = response.json()
        for term in ["jitómate", "tom-01", "perita", "primera"]:
            found = self.client.get("/api/gestion/productos",params={"buscar":term}).json()
            self.assertEqual([p["id"] for p in found],[product["id"]])
        conn = sqlite3.connect(database.DB_PATH)
        conn.execute("UPDATE productos SET stock=12.5,precio_venta=1234,precio_costo=456 WHERE id=?",(product["id"],))
        conn.commit(); conn.close()
        updated = self.client.put(f'/api/gestion/productos/{product["id"]}',json={"codigo":"TOM-02","descripcion":"Tomate perita","aliases":["tomatito"],"unidad_venta":"kg"})
        self.assertEqual(updated.status_code,200)
        value = updated.json()
        self.assertEqual((value["stock"],value["precio_venta"],value["precio_costo"]),(12.5,1234,456))
        self.assertEqual(self.client.get("/api/gestion/productos",params={"buscar":"jitomate"}).json(),[])

    def test_identifiers_unique_across_codes_aliases_and_inactive_products(self):
        self.assertEqual(self.create(activo=False).status_code,201)
        for body in [{"codigo":"tom-01","aliases":[]},{"codigo":"OTRO","aliases":["JITÓMATE"]},{"codigo":"JITOMATE","aliases":[]}]:
            with self.subTest(body=body):
                self.assertEqual(self.create(**body).status_code,409)

    def test_invalid_unit_and_repeated_aliases_are_rejected(self):
        for body in [{"unidad_venta":"litro"},{"aliases":["palta","PÁLTA"]},{"aliases":[" "]},{"codigo":"../test"},{"descripcion":" "}]:
            with self.subTest(body=body):
                self.assertEqual(self.create(**body).status_code,422)
        units = self.client.get("/api/gestion/unidades").json()
        self.assertEqual(len(units),7)
        self.assertFalse(next(u for u in units if u["codigo"]=="cajon")["fraccionable"])

    def test_inactive_is_retained_and_edit_of_missing_returns_404(self):
        self.create(activo=False)
        self.assertEqual(self.client.get("/api/gestion/productos").json(),[])
        self.assertEqual(len(self.client.get("/api/gestion/productos?incluir_inactivos=true").json()),1)
        self.assertEqual(self.client.put("/api/gestion/productos/999",json={"codigo":"X","descripcion":"X"}).status_code,404)

    def test_valid_photo_is_recoded_and_malicious_file_rejected(self):
        product = self.create().json()
        image = io.BytesIO(); Image.new("RGB",(24,24),"green").save(image,"PNG")
        path = f'/api/gestion/productos/{product["id"]}/foto'
        response = self.client.post(path,files={"archivo":("../bad.png",image.getvalue(),"image/png")})
        self.assertEqual(response.status_code,200)
        name = response.json()["foto"].split("/")[-1]
        with Image.open(Path(preparacion.MEDIA_DIR)/name) as uploaded:
            self.assertEqual(uploaded.format,"JPEG")
        self.assertEqual(self.client.post(path,files={"archivo":("fake.jpg",b"<script>alert(1)</script>","image/jpeg")}).status_code,422)
        self.assertEqual(self.client.post(path,files={"archivo":("huge.jpg",b"x"*(5*1024*1024+1),"image/jpeg")}).status_code,413)
        self.assertEqual(self.client.post("/api/gestion/productos/999/foto",files={"archivo":("x.jpg",b"x","image/jpeg")}).status_code,404)

    def test_migration_repeatable_and_keeps_existing_catalog(self):
        self.create()
        database.inicializar_db(); database.inicializar_db()
        self.assertEqual(len(self.client.get("/api/gestion/productos").json()),1)
        legacy = os.path.join(self.temp.name,"legacy.db")
        conn = sqlite3.connect(legacy)
        conn.executescript(Path(database.SCHEMA).read_text())
        conn.execute("INSERT INTO productos(codigo,descripcion,stock,precio_venta) VALUES('LEG-1','Legado',7,100)")
        conn.commit(); conn.close()
        database.DB_PATH = legacy
        database.inicializar_db()
        result = self.client.get("/api/gestion/productos").json()[0]
        self.assertEqual((result["codigo"],result["stock"],result["precio_venta"],result["unidad_venta"]),("LEG-1",7,100,"kg"))
        self.assertEqual(self.create(codigo="leg-1",aliases=[]).status_code,409)

    def test_existing_pages_and_endpoints_survive(self):
        for path in ["/","/ventas","/api/estado","/api/productos","/api/facturacion/historial"]:
            with self.subTest(path=path):
                self.assertEqual(self.client.get(path).status_code,200)


if __name__ == "__main__":
    unittest.main()
