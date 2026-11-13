"""Scheduled offers and local favorites, with isolated fixtures and no business data."""
import io,os,subprocess,sys,tempfile,time,urllib.request
from datetime import datetime,timedelta
from pathlib import Path
from zoneinfo import ZoneInfo
from uuid import uuid4
from PIL import Image,ImageDraw
from playwright.sync_api import sync_playwright,expect

root=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='nativa-offers-browser-') as tmp:
    env={**os.environ,'NATIVA_ENV':'development','CORONEL_DB_PATH':tmp+'/test.db','CORONEL_MEDIA_DIR':tmp+'/photos'}
    with open(tmp+'/server.log','w+') as log:
        process=subprocess.Popen([os.environ.get('APP_PYTHON',sys.executable),'-m','uvicorn','main:app','--app-dir','backend','--host','127.0.0.1','--port','8009'],cwd=root,env=env,stdout=log,stderr=log)
        try:
            base='http://127.0.0.1:8009'
            for _ in range(80):
                try:urllib.request.urlopen(base+'/healthz',timeout=1).close();break
                except Exception:
                    if process.poll() is not None:log.seek(0);raise RuntimeError(log.read())
                    time.sleep(.1)
            else:raise RuntimeError('Servidor no disponible')
            with sync_playwright() as p:
                browser=p.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH','/usr/bin/chromium'),headless=True,args=['--no-sandbox'])
                staff=browser.new_context(viewport={'width':1440,'height':1080},timezone_id='America/Argentina/Cordoba');admin=staff.new_page();admin.set_default_timeout(10000)
                def post(path,body):
                    response=staff.request.post(base+path,data=body);assert response.ok,(path,response.status,response.text());return response.json()
                credentials={'nombre':'Juliana prueba','clave':'solo-pruebas-123'};post('/api/comercial/responsables',credentials);post('/api/comercial/sesion',credentials)
                staff.request.put(base+'/api/gestion/negocio',data={'nombre':'Nativa','localidad':'Villa Carlos Paz, Córdoba'})
                products=[]
                for code,name,unit,price in [('TOM','Tomate perita','kg','2000'),('PER','Perejil','atado','800')]:
                    product=post('/api/gestion/productos',{'codigo':code,'descripcion':name,'unidad_venta':unit});products.append(product)
                    post('/api/comercial/productos/'+str(product['id'])+'/ajuste',{'tipo':'precio','importe':price,'version':0,'motivo':'Precio inicial aislado','clave_operacion':str(uuid4())})
                    im=Image.new('RGB',(500,360),'#eeede3');draw=ImageDraw.Draw(im)
                    for x,y in [(190,190),(310,190)]:
                        draw.ellipse((x-85,y-70,x+85,y+70),fill='#d85b38' if code=='TOM' else '#608549')
                        if code=='TOM':draw.polygon([(x,y-70),(x-40,y-90),(x-15,y-70),(x,y-110),(x+15,y-70),(x+40,y-90)],fill='#3f713b')
                    stream=io.BytesIO();im.save(stream,'PNG')
                    response=staff.request.post(base+f'/api/gestion/productos/{product["id"]}/foto',multipart={'archivo':{'name':'fixture.png','mimeType':'image/png','buffer':stream.getvalue()}});assert response.ok
                    assert staff.request.put(base+f'/api/gestion/tienda/productos/{product["id"]}',data={'visible':True}).ok
                errors=[];admin.on('pageerror',lambda e:errors.append(str(e)))
                admin.goto(base+'/#tiendaweb');expect(admin.locator('#web-publications article')).to_have_count(2)
                form=admin.locator('#web-promotion-form');form.locator('[name=producto_id]').select_option(str(products[0]['id']));form.locator('[name=titulo]').fill('Oferta de la semana');form.locator('[name=precio]').fill('1500')
                local=datetime.now(ZoneInfo('America/Argentina/Cordoba'))
                form.locator('[name=desde]').fill((local-timedelta(minutes=1)).strftime('%Y-%m-%dT%H:%M'));form.locator('[name=hasta]').fill((local+timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M'));form.locator('[name=motivo]').fill('Promoción de prueba sin datos reales');form.get_by_role('button',name='Programar oferta',exact=True).click();expect(admin.locator('#web-status')).to_contain_text('Oferta programada')
                guests=browser.new_context(viewport={'width':390,'height':844},timezone_id='America/Argentina/Cordoba');page=guests.new_page();page.set_default_timeout(10000);page.on('pageerror',lambda e:errors.append(str(e)))
                page.goto(base+'/tienda');expect(page.locator('.product-card')).to_have_count(2);expect(page.locator('.offer-badge')).to_have_text('Oferta de la semana');expect(page.locator('.regular-price')).to_contain_text('2.000,00')
                page.get_by_role('button',name='Guardar Tomate perita en favoritos',exact=True).click();page.get_by_role('button',name='♡ Mis favoritos',exact=True).click();expect(page.locator('.product-card')).to_have_count(1)
                page.reload();expect(page.get_by_role('button',name='Quitar Tomate perita de favoritos',exact=True)).to_have_attribute('aria-pressed','true')
                page.get_by_role('button',name='Ofertas',exact=True).click();expect(page.locator('.product-card')).to_have_count(1);assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
                page.screenshot(path='/workspace/nativa-ofertas-favoritos-movil.png',full_page=True)
                page.get_by_role('button',name='Elegir cantidad de Tomate perita',exact=True).click();expect(page.locator('#product-detail')).to_contain_text('Oferta hasta');page.get_by_role('button',name='Agregar a mi compra',exact=True).click();page.locator('#open-cart').click();expect(page.locator('#cart-total')).to_contain_text('1.500,00')
                page.locator('#checkout').click();guest=page.locator('#guest-form');guest.locator('[name=nombre]').fill('Vecina de prueba');guest.locator('[name=telefono]').fill('3541 123456');guest.locator('[name=presupuesto]').fill('1500');guest.locator('[name=entendido]').check();guest.get_by_role('button',name='Enviar mi solicitud',exact=True).click();page.wait_for_url('**/tienda/pedido#*')
                admin.locator('#web-promotions').get_by_role('button',name='Cancelar oferta',exact=True).click();expect(admin.locator('#web-promotions')).to_contain_text('Cancelada')
                prepare=admin.locator('#web-orders .prepare-form');expect(prepare).to_have_count(1);prepare.locator('[name=bruto]').fill('1');prepare.locator('[name=tara]').fill('0');prepare.get_by_role('button',name='Enviar peso e importe al cliente',exact=True).click();expect(admin.locator('#web-status')).to_contain_text('Propuesta guardada')
                page.get_by_role('button',name='Actualizar estado',exact=True).click();expect(page.locator('#tracking-content')).to_contain_text('1.500,00');expect(page.locator('#tracking-content')).to_contain_text('Oferta acordada: Oferta de la semana')
                page.get_by_role('button',name='Volver a pedir',exact=True).click();page.wait_for_url('**/tienda');page.locator('#open-cart').click();expect(page.locator('#cart-total')).to_contain_text('2.000,00');page.get_by_role('button',name='Cerrar mi compra',exact=True).click();page.get_by_role('button',name='Ofertas',exact=True).click();expect(page.locator('.empty')).to_contain_text('Sin ofertas para mostrar')
                assert len(staff.request.get(base+'/api/gestion/tienda/pedidos').json())==1
                assert not errors,errors
                print('PASS: promoción programada desde gestión, precio habitual/oferta, filtros, favoritos persistentes, detalle/vigencia, carrito y presupuesto a precio de oferta, cancelación sin cambiar pedido previo y recompra a precio actual; móvil sin desborde y sin errores JS. Sólo datos de prueba.')
                browser.close()
        finally:process.terminate();process.wait(timeout=10)
