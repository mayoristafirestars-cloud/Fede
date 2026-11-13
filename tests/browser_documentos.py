"""Photo binding, historical snapshots, printable documents and PDF checks."""
import io,os,subprocess,sys,tempfile,time,urllib.request
from pathlib import Path
from uuid import uuid4
from PIL import Image
from playwright.sync_api import sync_playwright,expect

root=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='nativa-photo-doc-') as tmp:
    env={**os.environ,'CORONEL_DB_PATH':tmp+'/test.db','CORONEL_MEDIA_DIR':tmp+'/photos'}
    with open(tmp+'/server.log','w+') as log:
        process=subprocess.Popen([os.environ.get('APP_PYTHON',sys.executable),'-m','uvicorn','main:app','--app-dir','backend','--host','127.0.0.1','--port','8006'],cwd=root,env=env,stdout=log,stderr=log)
        try:
            for _ in range(60):
                try:
                    with urllib.request.urlopen('http://127.0.0.1:8006/api/estado',timeout=1):break
                except Exception:
                    if process.poll() is not None:log.seek(0);raise RuntimeError(log.read())
                    time.sleep(.1)
            else:raise RuntimeError('Server not ready')
            with sync_playwright() as p:
                browser=p.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH','/usr/bin/chromium'),headless=True,args=['--no-sandbox'])
                page=browser.new_page(viewport={'width':1300,'height':1000});page.set_default_timeout(10000)
                errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
                base='http://127.0.0.1:8006'
                def post(path,body):
                    response=page.request.post(base+path,data=body);assert response.ok,(path,response.status,response.text());return response.json()
                def photo(product,color):
                    image=io.BytesIO();Image.new('RGB',(120,80),color).save(image,'PNG')
                    response=page.request.post(base+f'/api/gestion/productos/{product["id"]}/foto',multipart={'archivo':{'name':'foto-de-prueba.png','mimeType':'image/png','buffer':image.getvalue()}})
                    assert response.ok,response.text();return response.json()['foto']
                credentials={'nombre':'Responsable de prueba','clave':'solo-pruebas-123'}
                post('/api/comercial/responsables',credentials);post('/api/comercial/sesion',credentials)
                page.request.put(base+'/api/gestion/negocio',data={'nombre':'Nativa · documentos de prueba','localidad':'Villa Carlos Paz, Córdoba'})
                red=post('/api/gestion/productos',{'codigo':'ROJO','descripcion':'Producto de prueba rojo'})
                green=post('/api/gestion/productos',{'codigo':'VERDE','descripcion':'Producto de prueba verde'})
                red_image=photo(red,'red');green_image=photo(green,'green')
                supplier=post('/api/comercial/proveedores',{'nombre':'Proveedor de prueba'})
                order=post('/api/comercial/pedidos',{'proveedor_id':supplier['id'],'clave_operacion':str(uuid4()),'lineas':[{'producto_id':red['id'],'cantidad':'5','precio':'100'},{'producto_id':green['id'],'cantidad':'5','precio':'100'}]})
                post(f'/api/comercial/pedidos/{order["id"]}/recepciones',{'clave_operacion':str(uuid4()),'lineas':[{'linea_id':line['id'],'bruto_kg':'5','tara_kg':'0','precio':'100'} for line in order['lineas']]})
                for product in [red,green]:post(f'/api/comercial/productos/{product["id"]}/ajuste',{'clave_operacion':str(uuid4()),'tipo':'precio','importe':'200','version':0,'motivo':'Precio de prueba'})
                quote=post('/api/mostrador/cotizar',{'lineas':[{'producto_id':red['id'],'bruto_kg':'1','tara_kg':'0'},{'producto_id':green['id'],'bruto_kg':'0.5','tara_kg':'0'}]})
                sale=post('/api/mostrador/ventas',{'clave_operacion':str(uuid4()),'cotizacion_id':quote['id']})
                photo(red,'blue')
                page.goto(base+'/#caja')
                expect(page.locator('.counter-sale')).to_have_count(1)
                with page.context.expect_page() as new:page.get_by_role('button',name='Ver comprobante con fotos',exact=True).click()
                document=new.value;document.on('pageerror',lambda e:errors.append(str(e)));document.wait_for_load_state()
                expect(document.locator('.product-photo')).to_have_count(2)
                expect(document.locator('.product-photo').nth(0)).to_have_attribute('src',red_image)
                expect(document.locator('.product-photo').nth(1)).to_have_attribute('src',green_image)
                expect(document.locator('#print-document')).to_be_enabled()
                assert document.locator('.product-photo').evaluate_all('(images)=>images.every(i=>i.complete&&i.naturalWidth>0)')
                document.emulate_media(media='print');expect(document.locator('.product-photo').nth(0)).to_be_visible();expect(document.locator('.document-toolbar')).not_to_be_visible()
                pdf=document.pdf(format='A4',print_background=True);assert pdf.startswith(b'%PDF-') and len(pdf)>1000 and pdf.count(b'/Subtype /Image')>=2
                Path('/tmp/nativa-comprobante-fotos-prueba.pdf').write_bytes(pdf)
                document.emulate_media(media='screen');document.screenshot(path='/tmp/nativa-comprobante-fotos-prueba.png',full_page=True)
                with page.context.expect_page() as new:page.get_by_role('button',name='Ver remito con fotos',exact=True).click()
                delivery=new.value;delivery.wait_for_load_state();expect(delivery.locator('.product-photo')).to_have_count(2)
                expect(delivery.get_by_role('heading',name='Remito interno',exact=True)).to_be_visible()
                expect(delivery.locator('thead')).not_to_contain_text('Precio unitario')
                # A product without a photo remains unprintable until an audited attachment.
                page.request.put(base+f'/api/gestion/productos/{red["id"]}',data={'codigo':'ROJO','descripcion':'Producto de prueba rojo'})
                import sqlite3
                with sqlite3.connect(tmp+'/test.db') as conn:conn.execute("UPDATE productos SET foto='' WHERE id=?",(red['id'],))
                quote=post('/api/mostrador/cotizar',{'lineas':[{'producto_id':red['id'],'bruto_kg':'0.5','tara_kg':'0'}]})
                missing=post('/api/mostrador/ventas',{'clave_operacion':str(uuid4()),'cotizacion_id':quote['id']})
                document.goto(base+f'/api/documentos/pos/{missing["id"]}')
                expect(document.locator('#print-document')).to_be_disabled();expect(document.locator('.photo-missing')).to_have_count(1)
                document.emulate_media(media='print');expect(document.locator('.print-guard')).to_be_visible();expect(document.locator('.document-content')).not_to_be_visible();document.emulate_media(media='screen')
                photo(red,'red');document.locator('#complete-photos').click()
                expect(document.locator('#print-document')).to_be_enabled();expect(document.locator('.product-photo')).to_have_count(1)
                # Legacy draft and registered documents carry the same product-bound image.
                page.goto(base+'/ventas')
                current=page.request.get(base+'/api/productos').json();product=next(p for p in current if p['id']==red['id'])
                page.evaluate('(p)=>{agregarItemDirect(p);verPreview();}',product)
                expect(page.locator('#preview-content .document-product-photo')).to_have_count(1)
                legacy=post('/api/facturacion/nuevo',{'tipo':'presupuesto','items':[{'producto_id':red['id'],'producto_desc':'Producto de prueba rojo','cantidad':1,'precio_unitario':200}]})
                document.goto(base+f'/api/documentos/legado/{legacy["comprobante_id"]}')
                expect(document.locator('.product-photo')).to_have_count(1)
                document.set_viewport_size({'width':390,'height':844})
                assert document.evaluate('document.documentElement.scrollWidth<=innerWidth'),'Document mobile overflow'
                assert not errors,errors
                browser.close();print('PASS: per-product images, immutable photo snapshot, remito and receipt, printable PDF, missing-photo print guard, audited completion, legacy preview, mobile; no JS errors.')
        finally:process.terminate();process.wait(timeout=10)
