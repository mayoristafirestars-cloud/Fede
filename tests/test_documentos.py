import io,json,sqlite3,unittest
from pathlib import Path
from PIL import Image
import test_mostrador as fixtures
from db import database
from routers import preparacion


class DocumentoTests(unittest.TestCase):
    login=fixtures.MostradorTests.login
    create_product=fixtures.MostradorTests.create_product
    finance=fixtures.MostradorTests.finance
    adjust=fixtures.MostradorTests.adjust
    order=fixtures.MostradorTests.order
    receipt_body=fixtures.MostradorTests.receipt_body
    receive=fixtures.MostradorTests.receive
    post=fixtures.MostradorTests.post
    cart=fixtures.MostradorTests.cart
    quote=fixtures.MostradorTests.quote
    sale=fixtures.MostradorTests.sale

    def setUp(self):
        fixtures.MostradorTests.setUp(self)
        self.old_media=preparacion.MEDIA_DIR
        preparacion.MEDIA_DIR=str(Path(self.temp.name)/'photos')

    def tearDown(self):
        preparacion.MEDIA_DIR=self.old_media
        fixtures.MostradorTests.tearDown(self)

    def photo(self,color,product=None):
        image=io.BytesIO();Image.new('RGB',(40,30),color).save(image,'PNG')
        response=self.client.post(f'/api/gestion/productos/{product or self.p["id"]}/foto',files={'archivo':('producto.png',image.getvalue(),'image/png')})
        self.assertEqual(response.status_code,200,response.text)
        return response.json()['foto']

    def data(self,sale,origin='pos'):
        return self.client.get(f'/api/documentos/{origin}/{sale["id"]}/datos')

    def legacy(self):
        response=self.client.post('/api/facturacion/nuevo',json={'tipo':'presupuesto','items':[{'producto_id':self.p['id'],'producto_desc':'Tomate','cantidad':1,'precio_unitario':1500}]})
        self.assertEqual(response.status_code,200,response.text)
        return {'id':response.json()['comprobante_id']}

    def test_photo_is_snapshotted_for_pos_and_preserved_after_catalog_change(self):
        first=self.photo('red');sale=self.sale().json()
        self.assertEqual(sale['lineas'][0]['foto'],first)
        second=self.photo('green');self.assertNotEqual(first,second)
        data=self.data(sale).json()
        self.assertEqual(data['items'][0]['foto'],first)
        self.assertEqual(data['fotos_faltantes'],[])
        html=self.client.get(f'/api/documentos/pos/{sale["id"]}').text
        self.assertIn('src="'+first+'"',html);self.assertNotIn('src="'+second+'"',html)
        self.assertIn('No válido como factura fiscal',html)

    def test_legacy_photo_snapshot_and_history_detail(self):
        first=self.photo('red');legacy=self.legacy();self.photo('blue')
        data=self.data(legacy,'legado').json()
        self.assertEqual(data['items'][0]['foto'],first)
        detail=self.client.get(f'/api/facturacion/{legacy["id"]}').json()
        self.assertEqual(detail['items'][0]['foto'],first)
        search=self.client.get('/api/facturacion/buscar-producto?q=Tom').json()
        self.assertIn('foto',search[0])

    def test_missing_photo_blocks_print_and_can_be_attached_with_audit(self):
        sale=self.sale().json()
        data=self.data(sale).json();self.assertEqual(len(data['fotos_faltantes']),1)
        html=self.client.get(f'/api/documentos/pos/{sale["id"]}').text
        self.assertIn('data-missing="1"',html);self.assertIn('id="print-document" disabled',html)
        before_stock=self.finance()['stock'];photo=self.photo('red')
        response=self.client.post(f'/api/documentos/pos/{sale["id"]}/completar-fotos')
        self.assertEqual(response.status_code,200);self.assertEqual(response.json()['completadas'],1)
        self.assertEqual(self.client.post(f'/api/documentos/pos/{sale["id"]}/completar-fotos').json()['completadas'],0)
        self.assertEqual(self.finance()['stock'],before_stock)
        self.assertEqual(self.data(sale).json()['items'][0]['foto'],photo)
        with sqlite3.connect(database.DB_PATH) as conn:
            row=conn.execute('SELECT responsable FROM fotos_documento').fetchone();self.assertEqual(row[0],self.owner['nombre'])
            self.assertEqual(conn.execute('SELECT foto FROM lineas_pos WHERE venta_id=?',(sale['id'],)).fetchone()[0],'')
            self.assertEqual(conn.execute('SELECT total FROM ventas_pos WHERE id=?',(sale['id'],)).fetchone()[0],sale['total'])
        self.photo('green');self.client.post(f'/api/documentos/pos/{sale["id"]}/completar-fotos')
        self.assertEqual(self.data(sale).json()['items'][0]['foto'],photo)

    def test_different_origins_do_not_share_line_photo_attachments(self):
        sale=self.sale().json();legacy=self.legacy()
        first=self.photo('red');self.client.post(f'/api/documentos/pos/{sale["id"]}/completar-fotos')
        second=self.photo('green');self.client.post(f'/api/documentos/legado/{legacy["id"]}/completar-fotos')
        self.assertEqual(self.data(sale).json()['items'][0]['foto'],first)
        self.assertEqual(self.data(legacy,'legado').json()['items'][0]['foto'],second)

    def test_legacy_unknown_photos_are_not_silently_filled_on_read(self):
        legacy=self.legacy()
        with sqlite3.connect(database.DB_PATH) as conn:conn.execute('UPDATE comprobante_items SET foto=NULL WHERE comprobante_id=?',(legacy['id'],))
        self.photo('red')
        data=self.data(legacy,'legado').json();self.assertEqual(data['items'][0]['foto'],'')
        self.assertEqual(len(data['fotos_faltantes']),1)
        self.assertEqual(self.client.post(f'/api/documentos/legado/{legacy["id"]}/completar-fotos').json()['completadas'],1)

    def test_missing_file_and_remote_photo_are_not_trusted(self):
        image=self.photo('red');sale=self.sale().json()
        (Path(preparacion.MEDIA_DIR)/image.rsplit('/',1)[1]).unlink()
        self.assertFalse(self.data(sale).json()['items'][0]['foto_disponible'])
        with sqlite3.connect(database.DB_PATH) as conn:conn.execute("UPDATE productos SET foto='https://example.com/wrong.jpg' WHERE id=?",(self.p['id'],))
        other=self.sale().json();self.assertEqual(other['lineas'][0]['foto'],'')
        self.assertNotIn('https://example.com',self.client.get(f'/api/documentos/pos/{other["id"]}').text)

    def test_remito_has_photo_and_quantity_but_no_prices(self):
        image=self.photo('red');sale=self.sale().json()
        html=self.client.get(f'/api/documentos/pos/{sale["id"]}?tipo=remito').text
        self.assertIn('Remito interno',html);self.assertIn('src="'+image+'"',html)
        self.assertNotIn('Precio unitario',html);self.assertNotIn('Total original',html)

    def test_html_escapes_product_and_customer_names(self):
        self.client.put(f'/api/gestion/productos/{self.p["id"]}',json={'codigo':'TOM','descripcion':'<script>alert(1)</script>','unidad_venta':'kg'})
        self.photo('red');sale=self.sale().json()
        html=self.client.get(f'/api/documentos/pos/{sale["id"]}').text
        self.assertNotIn('<script>alert(1)</script>',html);self.assertIn('&lt;script&gt;alert(1)&lt;/script&gt;',html)

    def test_permissions_and_unknown_documents(self):
        sale=self.sale().json();self.client.delete('/api/comercial/sesion')
        self.assertEqual(self.data(sale).status_code,401)
        self.assertEqual(self.client.post(f'/api/documentos/pos/{sale["id"]}/completar-fotos').status_code,401)
        self.login();self.client.post('/api/comercial/responsables',json={'nombre':'Caja','clave':'clave-de-prueba','rol':'cajero'})
        self.client.delete('/api/comercial/sesion');self.login('Caja','clave-de-prueba')
        self.assertEqual(self.client.post(f'/api/documentos/pos/{sale["id"]}/completar-fotos').status_code,403)
        self.assertEqual(self.client.get('/api/documentos/pos/999').status_code,404)


if __name__=='__main__':unittest.main()
