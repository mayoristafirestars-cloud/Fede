"""End-to-end checks for roadmap 11–20; temporary data only."""
import os
import subprocess
import sys
import tempfile
import time
import urllib.request
from pathlib import Path
from uuid import uuid4

from playwright.sync_api import expect, sync_playwright

root=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='verduleria-commercial-') as tmp:
    env={**os.environ,'CORONEL_DB_PATH':tmp+'/test.db','CORONEL_MEDIA_DIR':tmp+'/photos'}
    with open(tmp+'/server.log','w+') as log:
        process=subprocess.Popen([os.environ.get('APP_PYTHON',sys.executable),'-m','uvicorn','main:app','--app-dir','backend','--host','127.0.0.1','--port','8003'],cwd=root,env=env,stdout=log,stderr=log)
        try:
            for _ in range(60):
                try:
                    with urllib.request.urlopen('http://127.0.0.1:8003/api/estado',timeout=1):break
                except Exception:
                    if process.poll() is not None:
                        log.seek(0);raise RuntimeError(log.read())
                    time.sleep(.1)
            else:raise RuntimeError('Server did not start')
            with sync_playwright() as p:
                browser=p.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH','/usr/bin/chromium'),headless=True,args=['--no-sandbox'])
                page=browser.new_page(viewport={'width':1440,'height':1000})
                page.set_default_timeout(10000)
                errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
                base='http://127.0.0.1:8003'
                response=page.request.post(base+'/api/gestion/productos',data={'codigo':'TOM-01','descripcion':'Tomate perita'})
                assert response.status==201
                product_id=response.json()['id']
                page.goto(base+'/#precios')
                page.locator('#precios-page .auth-open').click()
                page.locator('#auth-form [name=nombre]').fill('Responsable de prueba')
                page.locator('#auth-form [name=clave]').fill('solo-pruebas-123')
                page.locator('#auth-form [type=submit]').click()
                expect(page.locator('#auth-dialog')).not_to_be_visible()
                expect(page.locator('#precios-page .change-cost')).to_be_enabled()
                for selector,value,reason in [('.change-cost','1000','Costo del proveedor'),('.change-price','1500','Precio inicial')]:
                    page.locator(selector).click()
                    page.locator('#adjust-form [name=importe]').fill(value)
                    page.locator('#adjust-form [name=motivo]').fill(reason)
                    page.get_by_role('button',name='Guardar cambio',exact=True).click()
                    expect(page.locator('#adjust-dialog')).not_to_be_visible()
                expect(page.locator('.price-stats')).to_contain_text('33,33%')
                expect(page.locator('.price-stats')).to_contain_text('50%')
                page.get_by_role('button',name='Ver historial',exact=True).click()
                expect(page.locator('#history-content tbody tr')).to_have_count(2)
                expect(page.locator('#history-content')).to_contain_text('Precio inicial')
                page.locator('#history-dialog [data-close]').click()
                page.screenshot(path='/tmp/verduleria-precios.png',full_page=True)
                page.get_by_role('link',name='Compras',exact=False).click()
                page.get_by_role('button',name='+ Agregar proveedor',exact=True).click()
                form=page.locator('#supplier-form')
                form.locator('[name=nombre]').fill('Quinta de prueba')
                form.locator('[name=condiciones]').fill('Transferencia a siete días')
                form.locator('[name=dias_plazo]').fill('7')
                page.get_by_role('button',name='Guardar proveedor',exact=True).click()
                expect(page.locator('#supplier-dialog')).not_to_be_visible()
                expect(page.locator('#supplier-list')).to_contain_text('Quinta de prueba')
                page.get_by_role('button',name='+ Nuevo pedido',exact=True).click()
                page.locator('#order-lines [data-field=cantidad]').fill('20')
                page.locator('#order-lines [data-field=precio]').fill('1000')
                page.get_by_role('button',name='Guardar pedido',exact=True).click()
                expect(page.locator('#order-dialog')).not_to_be_visible()
                expect(page.locator('#order-list .order-card')).to_have_count(1)
                finance=page.request.get(base+'/api/comercial/productos').json()[0]
                assert float(finance['stock'])==0
                page.get_by_role('button',name='Recibir mercadería',exact=True).click()
                for key,value in [('bruto_kg','13'),('tara_kg','1'),('bultos','1'),('rechazado','2'),('observaciones','Golpes al recibir')]:
                    page.locator(f'#receipt-lines [data-field={key}]').fill(value)
                page.locator('#receipt-lines [data-field=calidad]').select_option('regular')
                page.locator('#receipt-lines .receipt-pricing-mode').select_option('total')
                page.locator('#receipt-lines [data-field=importe_mercaderia]').fill('10000')
                page.locator('#receipt-form [name=flete]').fill('1000')
                page.get_by_role('button',name='Confirmar recepción',exact=True).click()
                expect(page.locator('#receipt-dialog')).not_to_be_visible()
                expect(page.locator('#order-list .status-tag')).to_have_text('parcial')
                page.get_by_role('button',name='Ver pedido',exact=True).click()
                expect(page.locator('#order-detail-content')).to_contain_text('rechazado 2 kg')
                expect(page.locator('#order-detail-content')).to_contain_text('Golpes al recibir')
                page.locator('#order-detail-dialog [data-close]').click()
                page.get_by_role('button',name='Recibir mercadería',exact=True).click()
                for key,value in [('bruto_kg','11'),('tara_kg','1'),('precio','2000')]:
                    page.locator(f'#receipt-lines [data-field={key}]').fill(value)
                page.get_by_role('button',name='Confirmar recepción',exact=True).click()
                expect(page.locator('#receipt-dialog')).not_to_be_visible()
                expect(page.locator('#order-list .status-tag')).to_have_text('recibido')
                expect(page.get_by_role('button',name='Recibir mercadería',exact=True)).to_be_disabled()
                state=page.request.get(base+'/api/comercial/productos').json()[0]
                assert float(state['stock'])==20 and state['promedio']=='1550.0000' and state['reposicion']=='2000.0000',state
                page.reload()
                expect(page.locator('#order-list .status-tag')).to_have_text('recibido')
                page.screenshot(path='/tmp/verduleria-compras.png',full_page=True)
                page.set_viewport_size({'width':390,'height':844})
                assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'),'Mobile overflow'
                page.get_by_role('button',name='Ver pedido',exact=True).click()
                expect(page.locator('#order-detail-dialog')).to_be_visible()
                assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'),'Dialog mobile overflow'
                page.screenshot(path='/tmp/verduleria-compra-movil.png',full_page=True)
                page.locator('#order-detail-dialog [data-close]').click()
                page.get_by_role('link',name='Precios y costos',exact=False).click()
                page.locator('#precios-page .auth-logout').click()
                expect(page.locator('#precios-page .change-price')).to_be_disabled()
                response=page.request.post(base+f'/api/comercial/productos/{product_id}/ajuste',data={'tipo':'precio','importe':'1','version':0,'motivo':'No autorizado','clave_operacion':str(uuid4())})
                assert response.status==401
                assert not errors,errors
                browser.close()
                print('PASS: authorization, price/cost/history, supplier, purchase order, partial rejection, final receipt, weighted cost, reload, logout enforcement, desktop/mobile; no JS errors.')
        finally:
            process.terminate();process.wait(timeout=10)
