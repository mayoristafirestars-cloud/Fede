"""Retail flow, response-loss recovery, planning and crates; isolated data."""
import os,sys,subprocess,tempfile,time,urllib.request
from pathlib import Path
from uuid import uuid4
from playwright.sync_api import sync_playwright,expect

root=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='nativa-counter-') as tmp:
    env={**os.environ,'CORONEL_DB_PATH':tmp+'/test.db','CORONEL_MEDIA_DIR':tmp+'/photos'}
    with open(tmp+'/server.log','w+') as log:
        process=subprocess.Popen([os.environ.get('APP_PYTHON',sys.executable),'-m','uvicorn','main:app','--app-dir','backend','--host','127.0.0.1','--port','8005'],cwd=root,env=env,stdout=log,stderr=log)
        try:
            for _ in range(60):
                try:
                    with urllib.request.urlopen('http://127.0.0.1:8005/api/estado',timeout=1):break
                except Exception:
                    if process.poll() is not None:log.seek(0);raise RuntimeError(log.read())
                    time.sleep(.1)
            else:raise RuntimeError('Server not ready')
            with sync_playwright() as p:
                browser=p.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH','/usr/bin/chromium'),headless=True,args=['--no-sandbox'])
                page=browser.new_page(viewport={'width':1440,'height':1050});page.set_default_timeout(10000)
                errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
                base='http://127.0.0.1:8005'
                def post(path,body):
                    response=page.request.post(base+path,data=body);assert response.ok,(path,response.status,response.text());return response.json()
                credentials={'nombre':'Responsable de prueba','clave':'solo-pruebas-123'}
                post('/api/comercial/responsables',credentials);post('/api/comercial/sesion',credentials)
                page.request.put(base+'/api/gestion/negocio',data={'nombre':'Nativa'})
                tomato=post('/api/gestion/productos',{'codigo':'123','descripcion':'Tomate perita'})
                parsley=post('/api/gestion/productos',{'codigo':'200','descripcion':'Perejil','unidad_venta':'atado'})
                supplier=post('/api/comercial/proveedores',{'nombre':'Quinta de prueba'})
                order=post('/api/comercial/pedidos',{'proveedor_id':supplier['id'],'clave_operacion':str(uuid4()),'lineas':[{'producto_id':tomato['id'],'cantidad':'20','precio':'1000'},{'producto_id':parsley['id'],'cantidad':'5','precio':'100'}]})
                post(f'/api/comercial/pedidos/{order["id"]}/recepciones',{'clave_operacion':str(uuid4()),'lineas':[{'linea_id':order['lineas'][0]['id'],'bruto_kg':'21','tara_kg':'1','precio':'1000'},{'linea_id':order['lineas'][1]['id'],'cantidad':'5','precio':'100'}]})
                for product,price in [(tomato,'1999'),(parsley,'500')]:post(f'/api/comercial/productos/{product["id"]}/ajuste',{'tipo':'precio','importe':price,'version':0,'motivo':'Precio inicial de prueba','clave_operacion':str(uuid4())})
                page.goto(base+'/#caja')
                expect(page.locator('.counter-tile')).to_have_count(2)
                page.get_by_role('button',name='Marcar favorito Tomate perita',exact=True).click();page.locator('#counter-favorites').check();expect(page.locator('.counter-tile')).to_have_count(1);page.locator('#counter-favorites').uncheck()
                page.locator('.counter-tile').filter(has_text='Tomate perita').locator('.tile-main').click()
                form=page.locator('#weigh-form');form.locator('[name=bruto_kg]').fill('0.500');form.locator('[name=tara_kg]').fill('0.125');form.locator('[type=submit]').click()
                expect(page.locator('#weigh-dialog')).not_to_be_visible()
                page.locator('.counter-tile').filter(has_text='Perejil').locator('.tile-main').click();form.locator('[name=cantidad]').fill('2');form.locator('[type=submit]').click()
                expect(page.locator('#weigh-dialog')).not_to_be_visible();expect(page.locator('#counter-items .counter-item')).to_have_count(2)
                page.locator('#counter-discount').fill('10');page.locator('#counter-discount-reason').fill('Promoción autorizada')
                expect(page.locator('#counter-totals .final')).to_contain_text('1.574,67')
                page.get_by_role('button',name='Suspender',exact=True).click();page.locator('#suspend-form [name=nombre]').fill('Pedido en espera');page.locator('#suspend-form [type=submit]').click()
                expect(page.locator('#suspend-dialog')).not_to_be_visible();expect(page.locator('#counter-items .counter-item')).to_have_count(0)
                page.get_by_role('button',name='Recuperar',exact=True).click();expect(page.locator('#counter-totals .final')).to_contain_text('1.574,67')
                page.evaluate('window.scrollTo(0,0)');page.screenshot(path='/tmp/nativa-mostrador.png',full_page=True)
                def lost_response(route):
                    route.fetch();route.abort()
                page.route('**/api/mostrador/ventas',lost_response)
                page.get_by_role('button',name='Registrar venta · cobro pendiente',exact=True).click()
                expect(page.get_by_role('button',name='Reintentar registro pendiente',exact=True)).to_be_enabled()
                page.unroute('**/api/mostrador/ventas',lost_response)
                page.reload();expect(page.get_by_role('button',name='Reintentar registro pendiente',exact=True)).to_be_enabled()
                page.get_by_role('button',name='Reintentar registro pendiente',exact=True).click()
                expect(page.locator('.counter-sale')).to_have_count(1);expect(page.locator('#counter-items .counter-item')).to_have_count(0)
                registered=page.request.get(base+'/api/mostrador/ventas').json()
                assert len(registered)==1 and registered[0]['total']=='1574.67' and registered[0]['cobro']=='pendiente'
                page.get_by_role('button',name='Devolver productos',exact=True).click()
                page.locator('.sale-return-line').filter(has_text='Tomate perita').locator('input').fill('0.125')
                page.locator('#sale-correction-form [name=motivo]').fill('Cliente devuelve parte de la compra');page.locator('#sale-correction-form [type=submit]').click()
                expect(page.locator('#sale-correction-dialog')).not_to_be_visible();expect(page.locator('.counter-sale .status-tag')).to_have_text('parcial devuelta')
                page.get_by_role('button',name='Anular venta',exact=True).click();page.locator('#sale-correction-form [name=motivo]').fill('Corrección del resto de la venta');page.locator('#sale-correction-form [type=submit]').click()
                expect(page.locator('#sale-correction-dialog')).not_to_be_visible();expect(page.locator('.counter-sale .status-tag')).to_have_text('anulada')
                registered=page.request.get(base+'/api/mostrador/ventas').json()[0];assert registered['importe_corregido']=='1574.67'
                page.get_by_text('Configurar etiquetas de la balanza',exact=True).click()
                page.get_by_role('button',name='+ Agregar formato',exact=True).click()
                form=page.locator('#label-rule-form')
                for name,value in [('nombre','Formato de prueba'),('prefijo','21'),('codigo_desde','3'),('codigo_largo','5'),('valor_desde','8'),('valor_largo','5'),('decimales','3')]:form.locator(f'[name={name}]').fill(value)
                form.locator('[type=submit]').click();expect(page.locator('#label-rule-dialog')).not_to_be_visible()
                body='210012300750';code=body+str((10-sum(int(c)*(1 if i%2==0 else 3) for i,c in enumerate(body))%10)%10)
                page.locator('#scan-form [name=codigo]').fill(code);page.locator('#scan-form [type=submit]').click()
                expect(page.locator('#counter-totals .final')).to_contain_text('1.499,25')
                page.once('dialog',lambda dialog:dialog.accept());page.get_by_role('button',name='Vaciar',exact=True).click();expect(page.locator('#counter-items .counter-item')).to_have_count(0)
                page.get_by_role('link',name='Rotación y compra',exact=False).click()
                expect(page.locator('#replenishment-list .plan-card')).to_have_count(2)
                page.locator('#replenishment-list .plan-card').filter(has_text='Tomate perita').get_by_role('button',name='Ajustar previsión').click()
                form=page.locator('#replenishment-form');form.locator('[name=venta_diaria]').fill('12');form.locator('[name=seguridad]').fill('5');form.locator('[type=submit]').click()
                expect(page.locator('#replenishment-dialog')).not_to_be_visible();expect(page.locator('#replenishment-list .plan-card').filter(has_text='Tomate perita')).to_contain_text('estimacion manual')
                page.evaluate('window.scrollTo(0,0)');page.screenshot(path='/tmp/nativa-reposicion.png',full_page=True)
                page.get_by_role('link',name='Envases retornables',exact=False).click();page.get_by_role('button',name='+ Tipo de envase',exact=True).click();page.locator('#container-type-form [name=nombre]').fill('Cajón retornable de prueba');page.locator('#container-type-form [type=submit]').click()
                expect(page.locator('#container-type-dialog')).not_to_be_visible()
                for kind,qty,amount in [('recibido','10','0'),('perdida','2','0'),('deposito_pagado','0','5000')]:
                    page.get_by_role('button',name='+ Movimiento de envases',exact=True).click();form=page.locator('#container-move-form');form.locator('[name=tipo]').select_option(kind);form.locator('[name=cantidad]').fill(qty);form.locator('[name=importe]').fill(amount);form.locator('[name=referencia]').fill('REM-PRUEBA-001');form.locator('[name=motivo]').fill('Movimiento confirmado de prueba');form.locator('[type=submit]').click();expect(page.locator('#container-move-dialog')).not_to_be_visible()
                state=page.request.get(base+'/api/mostrador/envases').json()[0];assert state['en_local']==8 and state['por_devolver']==10 and state['perdidos_a_regularizar']==2
                page.evaluate('window.scrollTo(0,0)');page.screenshot(path='/tmp/nativa-envases.png',full_page=True)
                page.set_viewport_size({'width':390,'height':844});assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'),'Crates mobile overflow'
                page.get_by_role('link',name='Mostrador',exact=False).click();expect(page.locator('.counter-tile')).to_have_count(2)
                assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'),'Counter mobile overflow'
                page.locator('.counter-tile').filter(has_text='Tomate perita').locator('.tile-main').click();expect(page.locator('#weigh-form [name=bruto_kg]')).to_be_visible();page.locator('#weigh-dialog [data-counter-close]').first.click()
                page.evaluate('window.scrollTo(0,0)');page.screenshot(path='/tmp/nativa-mostrador-movil.png',full_page=True)
                assert not errors,errors
                browser.close();print('PASS: favorites, mixed weighted/unit sale, tara, authorized discount, suspend/recover, lost-response/reload retry, returns/cancellation, planning, crates/deposits, desktop/mobile; no JS errors.')
        finally:process.terminate();process.wait(timeout=10)
