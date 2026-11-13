"""End-to-end stock, payable accounts and claims, temporary data only."""
import os,subprocess,sys,tempfile,time,urllib.request
from pathlib import Path
from uuid import uuid4
from playwright.sync_api import sync_playwright,expect

root=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='verduleria-inventory-') as tmp:
    env={**os.environ,'CORONEL_DB_PATH':tmp+'/test.db','CORONEL_MEDIA_DIR':tmp+'/photos'}
    with open(tmp+'/server.log','w+') as log:
        process=subprocess.Popen([os.environ.get('APP_PYTHON',sys.executable),'-m','uvicorn','main:app','--app-dir','backend','--host','127.0.0.1','--port','8004'],cwd=root,env=env,stdout=log,stderr=log)
        try:
            for _ in range(60):
                try:
                    with urllib.request.urlopen('http://127.0.0.1:8004/api/estado',timeout=1):break
                except Exception:
                    if process.poll() is not None:log.seek(0);raise RuntimeError(log.read())
                    time.sleep(.1)
            else:raise RuntimeError('Server not ready')
            with sync_playwright() as p:
                browser=p.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH','/usr/bin/chromium'),headless=True,args=['--no-sandbox'])
                page=browser.new_page(viewport={'width':1440,'height':1100});page.set_default_timeout(10000)
                errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
                base='http://127.0.0.1:8004'
                def post(path,body):
                    response=page.request.post(base+path,data=body)
                    assert response.ok,(path,response.status,response.text())
                    return response.json()
                credentials={'nombre':'Responsable de prueba','clave':'solo-pruebas-123'}
                post('/api/comercial/responsables',credentials);post('/api/comercial/sesion',credentials)
                product=post('/api/gestion/productos',{'codigo':'TOM','descripcion':'Tomate perita'})
                supplier=post('/api/comercial/proveedores',{'nombre':'Quinta de prueba','dias_plazo':7})
                order=post('/api/comercial/pedidos',{'proveedor_id':supplier['id'],'clave_operacion':str(uuid4()),'lineas':[{'producto_id':product['id'],'cantidad':'20','precio':'1000'}]})
                post(f'/api/comercial/pedidos/{order["id"]}/recepciones',{'clave_operacion':str(uuid4()),'lineas':[{'linea_id':order['lineas'][0]['id'],'bruto_kg':'21','tara_kg':'1','precio':'1000'}],'flete':'2000'})
                page.goto(base+'/#inventario')
                expect(page.locator('.lot-card')).to_have_count(1)
                expect(page.locator('.inventory-product .stock-values')).to_contain_text('20 kg')
                page.get_by_role('button',name='Trasladar',exact=True).click()
                form=page.locator('#stock-action-form');form.locator('[name=destino_id]').select_option('2');form.locator('[name=cantidad]').fill('5');form.locator('[name=motivo]').fill('Guardar parte en depósito')
                form.locator('[type=submit]').click();expect(page.locator('#stock-action-dialog')).not_to_be_visible()
                expect(page.locator('.lot-positions')).to_contain_text('Depósito: 5 kg')
                page.get_by_role('button',name='Registrar salida',exact=True).click()
                form.locator('[name=cantidad]').fill('2');form.locator('[name=motivo]').fill('Deterioro detectado al revisar');form.locator('[type=submit]').click()
                expect(page.locator('#stock-action-dialog')).not_to_be_visible()
                expect(page.locator('.inventory-product .stock-values')).to_contain_text('18 kg')
                page.get_by_role('button',name='Maduración / revisión',exact=True).click()
                form.locator('[name=estado]').select_option('maduro');form.locator('[name=motivo]').fill('Priorizar venta por maduración');form.locator('[type=submit]').click()
                expect(page.locator('#stock-action-dialog')).not_to_be_visible();expect(page.locator('.lot-card .status-tag')).to_have_text('maduro')
                page.get_by_role('button',name='Contar',exact=True).click()
                form.locator('[name=cantidad]').fill('12');form.locator('[name=motivo]').fill('Pesaje físico del salón');form.locator('[type=submit]').click()
                expect(page.locator('#stock-action-dialog')).not_to_be_visible()
                expect(page.locator('.inventory-product .stock-values')).to_contain_text('18 kg')
                page.get_by_role('button',name='Aprobar conteo',exact=True).click();page.get_by_role('button',name='Aprobar ajuste',exact=True).click()
                expect(page.locator('#count-approve-dialog')).not_to_be_visible()
                expect(page.locator('.inventory-product .stock-values')).to_contain_text('17 kg')
                page.get_by_role('button',name='Devolver al proveedor',exact=True).click()
                form.locator('[name=cantidad]').fill('1');form.locator('[name=motivo]').fill('Devolución de calidad acordada');form.locator('[type=submit]').click()
                expect(page.locator('#stock-action-dialog')).not_to_be_visible()
                expect(page.locator('.inventory-product .stock-values')).to_contain_text('16 kg')
                page.evaluate('window.scrollTo(0,0)')
                page.screenshot(path='/tmp/verduleria-inventario.png',full_page=True)
                page.get_by_role('link',name='Proveedores y cuentas',exact=False).click()
                expect(page.locator('.account-card')).to_have_count(1)
                assert float(page.request.get(base+'/api/inventario/cuentas').json()[0]['saldo'])==20000
                page.get_by_role('button',name='+ Pago, crédito o reintegro',exact=True).click()
                accountForm=page.locator('#account-entry-form')
                accountForm.locator('[name=importe]').fill('5000');accountForm.locator('[name=referencia]').fill('REC-PAGO-001');accountForm.locator('[name=motivo]').fill('Pago parcial confirmado');accountForm.locator('[name=confirmado]').check();accountForm.locator('[type=submit]').click()
                expect(page.locator('#account-entry-dialog')).not_to_be_visible()
                expect(page.locator('.account-card .status-tag')).to_contain_text('15.000')
                page.get_by_role('button',name='+ Pago, crédito o reintegro',exact=True).click()
                accountForm.locator('[name=tipo]').select_option('credito');accountForm.locator('[name=importe]').fill('1000');accountForm.locator('[name=referencia]').fill('NC-PROV-001');accountForm.locator('[name=motivo]').fill('Crédito aceptado por devolución');accountForm.locator('[name=devolucion_id]').select_option('1');accountForm.locator('[name=confirmado]').check();accountForm.locator('[type=submit]').click()
                expect(page.locator('#account-entry-dialog')).not_to_be_visible();expect(page.locator('.account-card .status-tag')).to_contain_text('14.000')
                page.get_by_role('button',name='+ Reclamo',exact=True).click()
                claimForm=page.locator('#claim-form');claimForm.locator('[name=detalle]').fill('Consultar reposición de mercadería devuelta');claimForm.locator('[type=submit]').click()
                expect(page.locator('#claim-dialog')).not_to_be_visible();expect(page.locator('#supplier-claims .supplier-case')).to_have_count(1)
                page.get_by_role('button',name='Agregar seguimiento',exact=True).click();claimForm.locator('[name=estado]').select_option('en_gestion');claimForm.locator('[name=detalle]').fill('Proveedor avisado; esperando respuesta');claimForm.locator('[type=submit]').click()
                expect(page.locator('#claim-dialog')).not_to_be_visible();expect(page.locator('#supplier-claims .status-tag')).to_have_text('en gestion')
                entries=page.request.get(base+'/api/inventario/cuentas').json()[0]['movimientos'];payment=next(e for e in entries if e['tipo']=='pago')
                page.get_by_text('Ver movimientos de cuenta',exact=True).click();page.locator(f'[data-reverse="{payment["id"]}"]').click()
                page.locator('#account-reverse-form [name=motivo]').fill('El pago fue registrado por error');page.locator('#account-reverse-form [type=submit]').click()
                expect(page.locator('#account-reverse-dialog')).not_to_be_visible();expect(page.locator('.account-card .status-tag')).to_contain_text('19.000')
                page.reload();expect(page.locator('.account-card .status-tag')).to_contain_text('19.000')
                page.screenshot(path='/tmp/verduleria-cuentas.png',full_page=True)
                page.set_viewport_size({'width':390,'height':844})
                assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'),'Accounts mobile overflow'
                page.get_by_role('link',name='Inventario',exact=False).click()
                expect(page.locator('.lot-card')).to_have_count(1)
                assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'),'Stock mobile overflow'
                page.get_by_role('button',name='Contar',exact=True).click();expect(form.locator('[name=cantidad]')).to_be_visible()
                assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'),'Dialog mobile overflow'
                page.locator('#stock-action-dialog [data-inventory-close]').first.click()
                page.screenshot(path='/tmp/verduleria-inventario-movil.png',full_page=True)
                assert not errors,errors
                browser.close()
                print('PASS: inventory, transfer, merma, maturation, count approval, supplier return, partial payment, confirmed credit, claim followup, reversal, persistence, desktop/mobile; no JS errors.')
        finally:
            process.terminate();process.wait(timeout=10)
