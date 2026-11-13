"""Guest store and weight consent; fixture data only, never the business database."""
import io
import os
import subprocess
import sys
import tempfile
import time
import urllib.request
from pathlib import Path
from uuid import uuid4
from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright, expect

root=Path(__file__).resolve().parents[1]

def fixture_image(kind):
    im=Image.new('RGB',(600,460),'#f0eee3');d=ImageDraw.Draw(im)
    if kind=='tomate':
        for x,y in [(215,230),(355,230)]:
            d.ellipse((x-95,y-85,x+95,y+85),fill='#d95632');d.polygon([(x,y-80),(x-50,y-105),(x-18,y-77),(x+12,y-122),(x+23,y-77),(x+60,y-90)],fill='#416c38')
    elif kind=='banana':
        for off in [0,45,90]:
            d.arc((145+off,80,365+off,370),35,170,fill='#dcad36',width=48)
    elif kind=='perejil':
        for x,y in [(230,180),(290,150),(350,185),(250,240),(335,240)]:d.ellipse((x-55,y-45,x+55,y+45),fill='#568345')
        for x in [250,280,310,335]:d.line((x,220,290,350),fill='#67944b',width=12)
    elif kind=='zanahoria':
        for off in [-80,50]:
            d.polygon([(250+off,160),(340+off,160),(295+off,370)],fill='#db893d');d.line((280+off,160,245+off,80),fill='#567e36',width=17);d.line((300+off,160,335+off,65),fill='#567e36',width=17)
    else:
        color='#e69b37' if kind=='naranja' else '#c7a478'
        for x,y in [(215,210),(345,230),(280,310)]:
            d.ellipse((x-75,y-60,x+75,y+60),fill=color)
            if kind=='papa':d.ellipse((x-25,y-15,x-15,y-7),fill='#9f805b')
    stream=io.BytesIO();im.save(stream,'PNG');return stream.getvalue()

with tempfile.TemporaryDirectory(prefix='nativa-store-') as tmp:
    env={**os.environ,'NATIVA_ENV':'development','CORONEL_DB_PATH':tmp+'/test.db','CORONEL_MEDIA_DIR':tmp+'/photos'}
    with open(tmp+'/server.log','w+') as log:
        process=subprocess.Popen([os.environ.get('APP_PYTHON',sys.executable),'-m','uvicorn','main:app','--app-dir','backend','--host','127.0.0.1','--port','8007'],cwd=root,env=env,stdout=log,stderr=log)
        try:
            base='http://127.0.0.1:8007'
            for _ in range(80):
                try:
                    urllib.request.urlopen(base+'/healthz',timeout=1).close();break
                except Exception:
                    if process.poll() is not None:log.seek(0);raise RuntimeError(log.read())
                    time.sleep(.1)
            else:raise RuntimeError('Servidor no disponible')
            with sync_playwright() as p:
                browser=p.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH','/usr/bin/chromium'),headless=True,args=['--no-sandbox'])
                staff=browser.new_context();admin=staff.new_page();admin.set_default_timeout(10000)
                def post(path,body):
                    r=staff.request.post(base+path,data=body);assert r.ok,(path,r.status,r.text());return r.json()
                credentials={'nombre':'Juliana de prueba','clave':'solo-pruebas-123'}
                post('/api/comercial/responsables',credentials);post('/api/comercial/sesion',credentials)
                staff.request.put(base+'/api/gestion/negocio',data={'nombre':'Nativa','localidad':'Villa Carlos Paz, Córdoba'})
                specs=[('TOM','Tomate perita','kg','2000','tomate','Verduras'),('BAN','Banana','kg','2400','banana','Frutas'),('PER','Perejil','atado','800','perejil','Hierbas'),('PAP','Papa','kg','1200','papa','Verduras'),('NAR','Naranja','kg','1600','naranja','Frutas'),('ZAN','Zanahoria','kg','1800','zanahoria','Verduras')]
                for code,name,unit,price,kind,category in specs:
                    product=post('/api/gestion/productos',{'codigo':code,'descripcion':name,'unidad_venta':unit,'rubro':category})
                    post('/api/comercial/productos/'+str(product['id'])+'/ajuste',{'tipo':'precio','importe':price,'version':0,'motivo':'Precio de prueba aislada','clave_operacion':str(uuid4())})
                    r=staff.request.post(base+f'/api/gestion/productos/{product["id"]}/foto',multipart={'archivo':{'name':'prueba.png','mimeType':'image/png','buffer':fixture_image(kind)}});assert r.ok,r.text()
                    r=staff.request.put(base+f'/api/gestion/tienda/productos/{product["id"]}',data={'visible':True});assert r.ok,r.text()
                guests=browser.new_context(viewport={'width':1440,'height':1080});page=guests.new_page();page.set_default_timeout(10000)
                errors=[];page.on('pageerror',lambda e:errors.append(str(e)));admin.on('pageerror',lambda e:errors.append(str(e)))
                page.goto(base+'/tienda');expect(page.locator('.product-card')).to_have_count(6)
                page.screenshot(path='/workspace/nativa-tienda-escritorio.png',full_page=True)
                page.get_by_role('button',name='Frutas',exact=True).click();expect(page.locator('.product-card')).to_have_count(2)
                page.get_by_role('button',name='Todo',exact=True).click()
                page.locator('#store-search').fill('tomáte');expect(page.locator('.product-card')).to_have_count(1);page.locator('#store-search').fill('')
                page.get_by_role('button',name='Elegir cantidad de Tomate perita',exact=True).click()
                page.get_by_role('button',name='½ kg',exact=True).click();expect(page.locator('#quantity-estimate')).to_contain_text('1.000,00')
                page.get_by_role('button',name='Agregar a mi compra',exact=True).click()
                page.get_by_role('button',name='Elegir cantidad de Perejil',exact=True).click();page.locator('#product-quantity').fill('1.5');page.get_by_role('button',name='Agregar a mi compra',exact=True).click();expect(page.locator('#quantity-form .form-error')).to_be_visible()
                page.locator('#product-quantity').fill('2');page.get_by_role('button',name='Agregar a mi compra',exact=True).click()
                page.reload();expect(page.locator('#cart-count')).to_have_text('2')
                page.set_viewport_size({'width':390,'height':844});assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
                page.screenshot(path='/workspace/nativa-tienda-movil.png',full_page=True)
                page.locator('#open-cart').click();expect(page.locator('#cart-total')).to_contain_text('2.600,00')
                page.screenshot(path='/workspace/nativa-carrito-movil.png',full_page=True)
                page.locator('#checkout').click();page.locator('#guest-form [name=nombre]').fill('Vecina de prueba');page.locator('#guest-form [name=telefono]').fill('3541 123456');page.locator('#guest-form [name=entendido]').check()
                def lose_response(route):
                    route.fetch();route.abort()
                page.route('**/api/tienda/pedidos',lose_response,times=1)
                page.get_by_role('button',name='Enviar mi solicitud',exact=True).click();expect(page.locator('#guest-form .form-error')).to_be_visible()
                page.get_by_role('button',name='Enviar mi solicitud',exact=True).click();page.wait_for_url('**/tienda/pedido#*');expect(page.locator('.status-pill')).to_have_text('Solicitud recibida')
                orders=staff.request.get(base+'/api/gestion/tienda/pedidos').json();assert len(orders)==1
                admin.goto(base+'/#tiendaweb');expect(admin.locator('#web-orders .prepare-form')).to_have_count(1)
                form=admin.locator('#web-orders .prepare-form');form.locator('[name=bruto]').fill('0.550');form.locator('[name=tara]').fill('0.010');form.get_by_role('button',name='Enviar peso e importe al cliente',exact=True).click()
                expect(admin.locator('#web-status')).to_contain_text('Propuesta guardada')
                page.get_by_role('button',name='Actualizar estado',exact=True).click();expect(page.locator('.status-pill')).to_have_text('El total está listo para revisar');expect(page.locator('#tracking-content')).to_contain_text('2.680,00')
                page.screenshot(path='/workspace/nativa-total-pesado-movil.png',full_page=True)
                page.get_by_role('button',name='Aprobar importe final',exact=True).click();expect(page.locator('.status-pill')).to_have_text('Aprobaste el importe final')
                assert not errors,errors
                print('PASS: catálogo público, fotos, categorías/búsqueda, kg/atado, carrito persistente, móvil sin desborde, invitado, respuesta perdida sin duplicado, pesaje administrativo y aprobación del importe; sin errores JS. Datos y dibujos sólo de prueba.')
                browser.close()
        finally:
            process.terminate();process.wait(timeout=10)
