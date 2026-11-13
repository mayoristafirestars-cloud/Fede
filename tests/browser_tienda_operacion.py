"""End-to-end points 4–10, isolated database and synthetic image fixtures."""
import io,os,subprocess,sys,tempfile,time,urllib.request
from datetime import datetime,timedelta,timezone
from pathlib import Path
from uuid import uuid4
from PIL import Image
from playwright.sync_api import sync_playwright,expect

root=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='nativa-ops-browser-') as tmp:
    env={**os.environ,'NATIVA_ENV':'development','CORONEL_DB_PATH':tmp+'/test.db','CORONEL_MEDIA_DIR':tmp+'/photos'}
    with open(tmp+'/server.log','w+') as log:
        process=subprocess.Popen([os.environ.get('APP_PYTHON',sys.executable),'-m','uvicorn','main:app','--app-dir','backend','--host','127.0.0.1','--port','8008'],cwd=root,env=env,stdout=log,stderr=log)
        try:
            base='http://127.0.0.1:8008'
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
                    r=staff.request.post(base+path,data=body);assert r.ok,(path,r.status,r.text());return r.json()
                credentials={'nombre':'Juliana de prueba','clave':'solo-pruebas-123'};post('/api/comercial/responsables',credentials);post('/api/comercial/sesion',credentials)
                staff.request.put(base+'/api/gestion/negocio',data={'nombre':'Nativa','localidad':'Villa Carlos Paz, Córdoba'})
                products=[]
                for code,name,unit,price,cost in [('TOM','Tomate perita','kg','2000','1000'),('ALT','Tomate redondo','kg','1800','700'),('PER','Perejil','atado','800','200')]:
                    product=post('/api/gestion/productos',{'codigo':code,'descripcion':name,'unidad_venta':unit});products.append(product)
                    post('/api/comercial/productos/'+str(product['id'])+'/ajuste',{'tipo':'precio','importe':price,'version':0,'motivo':'Precio de prueba aislada','clave_operacion':str(uuid4())})
                    buffer=io.BytesIO();Image.new('RGB',(300,220),'#d9623d' if code!='PER' else '#668f46').save(buffer,'PNG')
                    r=staff.request.post(base+f'/api/gestion/productos/{product["id"]}/foto',multipart={'archivo':{'name':'fixture.png','mimeType':'image/png','buffer':buffer.getvalue()}});assert r.ok
                    r=staff.request.put(base+f'/api/gestion/tienda/productos/{product["id"]}',data={'visible':True});assert r.ok
                supplier=post('/api/comercial/proveedores',{'nombre':'Quinta de prueba'})
                purchase=post('/api/comercial/pedidos',{'proveedor_id':supplier['id'],'clave_operacion':str(uuid4()),'lineas':[{'producto_id':prod['id'],'cantidad':'10' if prod['unidad_venta']=='atado' else '20','precio':cost} for prod,cost in zip(products,['1000','700','200'])]})
                received=[]
                for line,prod,cost in zip(purchase['lineas'],products,['1000','700','200']):
                    received.append({'linea_id':line['id'],'precio':cost,**({'cantidad':'10'} if prod['unidad_venta']=='atado' else {'bruto_kg':'20','tara_kg':'0'})})
                post('/api/comercial/pedidos/'+str(purchase['id'])+'/recepciones',{'clave_operacion':str(uuid4()),'lineas':received})
                r=staff.request.put(base+'/api/gestion/tienda/configuracion',data={'abierta':True,'requiere_franja':True,'reserva_minutos':120,'contacto':'Consultas desde el pedido o en el local'});assert r.ok
                start=datetime.now(timezone.utc)+timedelta(hours=1)
                slot=post('/api/gestion/tienda/franjas',{'inicio':start.isoformat(),'fin':(start+timedelta(hours=1)).isoformat(),'cupo':2})
                guests=browser.new_context(viewport={'width':390,'height':844},timezone_id='America/Argentina/Cordoba');page=guests.new_page();page.set_default_timeout(10000);errors=[]
                page.on('pageerror',lambda e:errors.append(str(e)));admin.on('pageerror',lambda e:errors.append(str(e)))
                page.goto(base+'/tienda');expect(page.locator('.product-card')).to_have_count(3)
                page.get_by_role('button',name='Elegir cantidad de Tomate perita',exact=True).click();page.get_by_role('button',name='Agregar a mi compra',exact=True).click()
                page.get_by_role('button',name='Elegir cantidad de Perejil',exact=True).click();page.locator('#product-quantity').fill('2');page.get_by_role('button',name='Agregar a mi compra',exact=True).click()
                page.locator('#open-cart').click();page.locator('[data-replacement="'+str(products[2]['id'])+'"]').select_option('no_reemplazar')
                page.locator('#checkout').click();f=page.locator('#guest-form');f.locator('[name=nombre]').fill('Vecina de prueba');f.locator('[name=telefono]').fill('3541 123456');f.locator('[name=presupuesto]').fill('3500');f.locator('[name=franja_id]').select_option(str(slot['id']));f.locator('[name=entendido]').check();f.get_by_role('button',name='Enviar mi solicitud',exact=True).click();expect(f.locator('.form-error')).to_contain_text('presupuesto')
                f.locator('[name=presupuesto]').fill('4000');page.screenshot(path='/workspace/nativa-presupuesto-franja-movil.png',full_page=True)
                f.get_by_role('button',name='Enviar mi solicitud',exact=True).click();page.wait_for_url('**/tienda/pedido#*');expect(page.locator('.reservation-note')).to_contain_text('Reserva temporal')
                assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
                admin.goto(base+'/#tiendaweb');expect(admin.locator('#web-orders .prepare-form')).to_have_count(1)
                form=admin.locator('#web-orders .prepare-form');field=form.locator('fieldset').first;field.locator('[name=reemplazo_id]').select_option(str(products[1]['id']));field.locator('[name=bruto]').fill('1.100');field.locator('[name=tara]').fill('0.020');form.get_by_role('button',name='Enviar peso e importe al cliente',exact=True).click();expect(admin.locator('#web-status')).to_contain_text('Propuesta guardada')
                page.get_by_role('button',name='Actualizar estado',exact=True).click();expect(page.locator('#tracking-content')).to_contain_text('Reemplazo propuesto: Tomate redondo');expect(page.locator('#tracking-content')).to_contain_text('3.544,00')
                page.screenshot(path='/workspace/nativa-reemplazo-presupuesto-movil.png',full_page=True)
                claim=page.locator('#claim-form');claim.locator('[name=detalle]').fill('¿Podemos coordinar la selección para consumir mañana?');claim.get_by_role('button',name='Enviar consulta a Nativa',exact=True).click();expect(page.locator('#claim-list')).to_contain_text('consumir mañana')
                admin.locator('#web-refresh').click();expect(admin.locator('.web-claims form')).to_have_count(1)
                reply=admin.locator('.web-claims form');reply.locator('[name=texto]').fill('Sí, revisamos el estado de la fruta al preparar.');reply.locator('[name=estado]').select_option('resuelto');reply.get_by_role('button',name='Responder consulta',exact=True).click()
                expect(admin.locator('.web-claims')).to_contain_text('resuelto')
                admin.locator('.web-profit summary').click();costform=admin.locator('.web-cost-form')
                for name,value in {'empaque':'100','comision':'70','minutos':'10','valor_hora':'600','reparto':'0','incidencias':'0'}.items():costform.locator('[name='+name+']').fill(value)
                costform.get_by_role('button',name='Guardar costos del pedido',exact=True).click();expect(admin.locator('.web-profit')).to_contain_text('2.118,00')
                page.get_by_role('button',name='Actualizar estado',exact=True).click();expect(page.locator('#claim-list')).to_contain_text('revisamos el estado');page.get_by_role('button',name='Aprobar importe final',exact=True).click();expect(page.locator('.status-pill')).to_have_text('Aprobaste el importe final')
                admin.locator('#web-refresh').click();expect(admin.get_by_role('button',name='Registrar entrega y cobro verificado',exact=True)).to_be_visible()
                deliver=admin.locator('.web-fulfill form');deliver.locator('[name=referencia]').fill('Cobro en efectivo contado');deliver.locator('[name=verificado]').check();deliver.get_by_role('button',name='Registrar entrega y cobro verificado',exact=True).click();expect(admin.locator('#web-orders h3')).to_contain_text('Entregado')
                page.get_by_role('button',name='Actualizar estado',exact=True).click();expect(page.locator('.status-pill')).to_have_text('Pedido entregado');expect(page.locator('#tracking-content')).to_contain_text('verificación manual del cobro')
                finance=staff.request.get(base+'/api/comercial/productos').json();tom=next(p for p in finance if p['id']==products[0]['id'])
                post('/api/comercial/productos/'+str(tom['id'])+'/ajuste',{'tipo':'precio','importe':'2300','version':tom['version_precio'],'motivo':'Cambio de precio de prueba','clave_operacion':str(uuid4())})
                page.get_by_role('button',name='Volver a pedir',exact=True).click();page.wait_for_url('**/tienda');expect(page.locator('#cart-count')).to_have_text('2');expect(page.locator('#store-notice')).to_contain_text('precio actualizado');page.locator('#open-cart').click();expect(page.locator('#cart-total')).to_contain_text('3.900,00')
                page.locator('[data-replacement="'+str(products[0]['id'])+'"]').select_option('alternativa');page.locator('[data-alternative="'+str(products[0]['id'])+'"]').select_option(str(products[1]['id']));assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
                page.screenshot(path='/workspace/nativa-recompra-movil.png',full_page=True)
                assert len(staff.request.get(base+'/api/gestion/tienda/pedidos').json())==1
                finance=staff.request.get(base+'/api/comercial/productos').json();assert next(p for p in finance if p['id']==products[1]['id'])['stock']=='18.92'
                assert not errors,errors
                print('PASS: presupuesto bloqueante, preferencias de reemplazo, franja/cupo/reserva, pesaje con alternativa, consulta y respuesta, costos/contribución, aprobación, entrega/cobro manual con stock y recompra a precios actuales; móvil sin desborde y sin errores JS. Sólo datos aislados.')
                browser.close()
        finally:process.terminate();process.wait(timeout=10)
