import json,sqlite3,time,unittest
from decimal import Decimal
from datetime import timedelta
from uuid import uuid4
import test_comercial as fixtures
from db import database
import stock


def ean(body):return body+str((10-sum(int(c)*(1 if i%2==0 else 3) for i,c in enumerate(body))%10)%10)

class MostradorTests(unittest.TestCase):
    login=fixtures.ComercialTests.login
    create_product=fixtures.ComercialTests.create_product
    finance=fixtures.ComercialTests.finance
    adjust=fixtures.ComercialTests.adjust
    order=fixtures.ComercialTests.order
    receipt_body=fixtures.ComercialTests.receipt_body
    receive=fixtures.ComercialTests.receive
    tearDown=fixtures.ComercialTests.tearDown

    def setUp(self):
        fixtures.ComercialTests.setUp(self)
        self.o,_=self.order();self.receive(self.o,self.receipt_body(self.o));self.adjust('1500')

    def post(self,path,**body):return self.client.post('/api/mostrador'+path,json={'clave_operacion':str(uuid4()),**body})
    def cart(self,**extra):return {'lineas':[{'producto_id':self.p['id'],'bruto_kg':'1','tara_kg':'0'}],**extra}
    def quote(self,body=None):return self.client.post('/api/mostrador/cotizar',json=body or self.cart())
    def sale(self,body=None):
        quoted=self.quote(body);self.assertEqual(quoted.status_code,200,quoted.text)
        return self.post('/ventas',cotizacion_id=quoted.json()['id'])
    def correction(self,sale,qty=None,**extra):
        body={'tipo':'devolucion','motivo':'Devolución de prueba','lineas':[{'linea_id':sale['lineas'][0]['id'],'cantidad':qty or '0.5'}],**extra}
        if body['tipo']=='anulacion':body['lineas']=[]
        return self.post(f'/ventas/{sale["id"]}/correcciones',**body)
    def rule(self,prefix='21',kind='peso'):
        body={'nombre':'Formato de prueba','prefijo':prefix,'codigo_desde':3,'codigo_largo':5,'valor_desde':8,'valor_largo':5,'decimales':3 if kind=='peso' else 2,'tipo':kind,'unidad_peso':'kg'}
        response=self.client.post('/api/mostrador/etiquetas/reglas',json=body)
        self.assertEqual(response.status_code,201,response.text);return response.json()
    def numeric_product(self):
        self.client.put(f'/api/gestion/productos/{self.p["id"]}',json={'codigo':'123','descripcion':'Tomate','unidad_venta':'kg'})

    def test_weight_tare_decimal_total_and_payment_pending(self):
        self.adjust('1999')
        cart={'lineas':[{'producto_id':self.p['id'],'bruto_kg':'0.500','tara_kg':'0.125'}]}
        quote=self.quote(cart).json()
        self.assertEqual(quote['lineas'][0]['cantidad'],'0.375');self.assertEqual(quote['total'],'749.63')
        sale=self.post('/ventas',cotizacion_id=quote['id'])
        self.assertEqual(sale.status_code,201,sale.text)
        self.assertEqual(sale.json()['cobro'],'pendiente');self.assertEqual(sale.json()['total'],'749.63')
        self.assertEqual(Decimal(self.finance()['stock']),Decimal('19.625'))
        self.assertEqual(sale.json()['lineas'][0]['unidad'],'kg')

    def test_invalid_tare_quantity_origin_and_zero_net(self):
        for line in [{'bruto_kg':'1','tara_kg':'2'},{'bruto_kg':'1','tara_kg':'1'},{'cantidad':'1'},{'bruto_kg':'1','tara_kg':'0','cantidad':'1'}]:
            response=self.quote({'lineas':[{'producto_id':self.p['id'],**line}]})
            self.assertEqual(response.status_code,422,response.text)
        self.assertEqual(Decimal(self.finance()['stock']),20)

    def test_mixed_units_and_weights_in_one_sale(self):
        other=self.create_product('AT','Perejil','atado')
        order,_=self.order(extra={'producto_id':other['id'],'cantidad':'5','precio':'100'})
        receipt={'clave_operacion':str(uuid4()),'lineas':[{'linea_id':order['lineas'][1]['id'],'cantidad':'5','precio':'100'}]}
        self.assertEqual(self.receive(order,receipt).status_code,201)
        state=self.client.get('/api/comercial/productos').json();p=next(p for p in state if p['id']==other['id'])
        self.client.post(f'/api/comercial/productos/{other["id"]}/ajuste',json={'tipo':'precio','importe':'200','version':p['version_precio'],'motivo':'Precio inicial','clave_operacion':str(uuid4())})
        cart=self.cart();cart['lineas'].append({'producto_id':other['id'],'cantidad':'2'})
        sale=self.sale(cart)
        self.assertEqual(sale.status_code,201,sale.text);self.assertEqual(sale.json()['total'],'1900.00')
        self.assertEqual({l['unidad'] for l in sale.json()['lineas']},{'kg','atado'})
        cart['lineas'][1]['cantidad']='1.5';self.assertEqual(self.quote(cart).status_code,422)

    def test_discount_authorization_and_audit(self):
        response=self.sale(self.cart(descuento='10',motivo_descuento='Promoción autorizada'))
        sale=response.json();self.assertEqual(sale['total'],'1350.00');self.assertEqual(sale['descuento'],'150.00')
        self.assertEqual(sale['responsable'],self.owner['nombre']);self.assertEqual(sale['motivo_descuento'],'Promoción autorizada')
        self.assertEqual(self.quote(self.cart(descuento='10')).status_code,422)
        self.client.post('/api/comercial/responsables',json={'nombre':'Caja','clave':'clave-de-prueba','rol':'cajero'})
        self.client.delete('/api/comercial/sesion');self.login('Caja','clave-de-prueba')
        self.assertEqual(self.quote(self.cart(descuento='10',motivo_descuento='No autorizado')).status_code,403)
        self.assertEqual(self.sale().status_code,201)

    def test_registration_idempotent_and_quote_cannot_be_used_twice(self):
        quote=self.quote().json();body={'clave_operacion':str(uuid4()),'cotizacion_id':quote['id']}
        first=self.client.post('/api/mostrador/ventas',json=body)
        self.assertEqual(first.status_code,201)
        self.assertEqual(self.client.post('/api/mostrador/ventas',json=body).json(),first.json())
        self.assertEqual(self.post('/ventas',cotizacion_id=quote['id']).status_code,409)
        self.assertEqual(len(self.client.get('/api/mostrador/ventas').json()),1)
        self.assertEqual(Decimal(self.finance()['stock']),19)

    def test_changed_price_expired_quote_and_changed_operator(self):
        q=self.quote().json();self.adjust('1600')
        self.assertEqual(self.post('/ventas',cotizacion_id=q['id']).status_code,409)
        q=self.quote().json()
        with sqlite3.connect(database.DB_PATH) as conn:conn.execute('UPDATE cotizaciones_pos SET vence=0 WHERE id=?',(q['id'],))
        self.assertEqual(self.post('/ventas',cotizacion_id=q['id']).status_code,409)
        q=self.quote().json();self.client.post('/api/comercial/responsables',json={'nombre':'Encargada','clave':'clave-de-prueba','rol':'encargado'})
        self.client.delete('/api/comercial/sesion');self.login('Encargada','clave-de-prueba')
        self.assertEqual(self.post('/ventas',cotizacion_id=q['id']).status_code,409)
        self.assertEqual(Decimal(self.finance()['stock']),20)

    def test_stock_is_checked_atomically_across_duplicate_products(self):
        cart={'lineas':[{'producto_id':self.p['id'],'bruto_kg':'15','tara_kg':'0'},{'producto_id':self.p['id'],'bruto_kg':'10','tara_kg':'0'}]}
        self.assertEqual(self.sale(cart).status_code,409)
        self.assertEqual(Decimal(self.finance()['stock']),20)
        self.assertEqual(self.client.get('/api/mostrador/ventas').json(),[])

    def test_sale_prioritizes_mature_lot_and_records_inferred_source(self):
        order,_=self.order();self.receive(order,self.receipt_body(order))
        lots=self.client.get('/api/inventario/resumen').json()['lotes'];latest=lots[-1]
        self.client.post(f'/api/inventario/lotes/{latest["id"]}/revision',json={'estado':'maduro','notas':'Maduración verificada','clave_operacion':str(uuid4())})
        self.assertEqual(self.sale().status_code,201)
        with sqlite3.connect(database.DB_PATH) as conn:
            row=conn.execute("SELECT lote_id,asignacion FROM movimientos_stock WHERE tipo='venta_pos'").fetchone()
        self.assertEqual(row,(latest['id'],'inferida'))

    def test_partial_return_uses_original_discount_and_quarantine(self):
        sale=self.sale(self.cart(descuento='10',motivo_descuento='Descuento autorizado')).json()
        self.adjust('9999')
        response=self.correction(sale,'0.5')
        self.assertEqual(response.status_code,201,response.text)
        self.assertEqual(response.json()['importe_a_revisar'],'675.00')
        self.assertEqual(response.json()['venta']['estado'],'parcial_devuelta')
        inventory=self.client.get('/api/inventario/resumen').json()['productos'][0]
        self.assertEqual(Decimal(inventory['total']),Decimal('19.5'))
        self.assertEqual(Decimal(inventory['vendible']),19)
        self.assertEqual(self.correction(sale,'0.501').status_code,409)

    def test_partial_then_full_cancellation_conserves_original_total(self):
        sale=self.sale(self.cart(descuento='10',motivo_descuento='Promoción')).json()
        self.correction(sale,'0.3')
        corrected=self.correction(sale,tipo='anulacion')
        self.assertEqual(corrected.status_code,201,corrected.text)
        self.assertEqual(corrected.json()['venta']['estado'],'anulada')
        self.assertEqual(corrected.json()['venta']['importe_corregido'],sale['total'])
        self.assertEqual(Decimal(self.finance()['stock']),20)
        self.assertEqual(self.correction(sale,tipo='anulacion').status_code,409)

    def test_return_rounding_and_discard_do_not_create_sellable_stock(self):
        self.adjust('0.05');sale=self.sale().json();refunded=Decimal(0)
        for qty in ['0.333','0.333','0.334']:
            r=self.correction(sale,qty,destino='descarte');self.assertEqual(r.status_code,201,r.text);refunded+=Decimal(r.json()['importe_a_revisar'])
        self.assertEqual(refunded,Decimal('.05'))
        self.assertEqual(Decimal(self.finance()['stock']),19)
        self.assertEqual(self.client.get('/api/mostrador/ventas').json()[0]['estado'],'devuelta')

    def test_return_retries_and_cashier_cannot_correct(self):
        sale=self.sale().json();body={'clave_operacion':str(uuid4()),'tipo':'devolucion','motivo':'Corrección autorizada','lineas':[{'linea_id':sale['lineas'][0]['id'],'cantidad':'0.5'}]}
        path=f'/api/mostrador/ventas/{sale["id"]}/correcciones'
        first=self.client.post(path,json=body);self.assertEqual(first.status_code,201)
        self.assertEqual(self.client.post(path,json=body).json(),first.json())
        self.assertEqual(Decimal(self.finance()['stock']),Decimal('19.5'))
        self.client.post('/api/comercial/responsables',json={'nombre':'Caja','clave':'clave-de-prueba','rol':'cajero'})
        self.client.delete('/api/comercial/sesion');self.login('Caja','clave-de-prueba')
        self.assertEqual(self.correction(sale).status_code,403)

    def test_suspended_cart_has_no_stock_reservation_or_frozen_price(self):
        created=self.post('/suspendidos',nombre='Pedido a esperar',carrito=self.cart()).json()
        self.assertEqual(Decimal(self.finance()['stock']),20)
        self.adjust('2500')
        resumed=self.post(f'/suspendidos/{created["id"]}/recuperar').json()
        quote=self.quote(resumed['carrito']).json();self.assertEqual(quote['total'],'2500.00')
        self.assertEqual(self.post(f'/suspendidos/{created["id"]}/recuperar').status_code,409)
        self.assertEqual(self.client.get('/api/mostrador/suspendidos').json(),[])

    def test_favorites_are_per_operator(self):
        self.assertEqual(self.client.put(f'/api/mostrador/favoritos/{self.p["id"]}').status_code,200)
        self.assertTrue(self.client.get('/api/mostrador/catalogo').json()[0]['favorito'])
        self.client.post('/api/comercial/responsables',json={'nombre':'Caja','clave':'clave-de-prueba','rol':'cajero'})
        self.client.delete('/api/comercial/sesion');self.login('Caja','clave-de-prueba')
        self.assertFalse(self.client.get('/api/mostrador/catalogo').json()[0]['favorito'])

    def test_configurable_weight_label_and_checksum(self):
        self.numeric_product();self.rule();code=ean('21'+'00123'+'00750')
        response=self.client.post('/api/mostrador/resolver-codigo',json={'codigo':code})
        self.assertEqual(response.status_code,200,response.text);self.assertEqual(response.json()['cantidad'],'0.75')
        sale=self.sale({'lineas':[{'producto_id':self.p['id'],'etiqueta':code}]})
        self.assertEqual(sale.status_code,201,sale.text);self.assertEqual(sale.json()['total'],'1125.00')
        bad=code[:-1]+str((int(code[-1])+1)%10)
        self.assertEqual(self.client.post('/api/mostrador/resolver-codigo',json={'codigo':bad}).status_code,422)

    def test_amount_only_label_does_not_invent_weight(self):
        self.numeric_product();self.rule(kind='importe');code=ean('21'+'00123'+'01250')
        decoded=self.client.post('/api/mostrador/resolver-codigo',json={'codigo':code}).json()
        self.assertEqual(decoded['importe'],'12.5');self.assertTrue(decoded['requiere_peso'])
        self.assertEqual(self.quote({'lineas':[{'producto_id':self.p['id'],'etiqueta':code}]}).status_code,422)

    def test_overlapping_rules_and_edit_validation(self):
        rule=self.rule()
        body={k:v for k,v in rule.items() if k!='id'};body['prefijo']='2'
        self.assertEqual(self.client.post('/api/mostrador/etiquetas/reglas',json=body).status_code,409)
        body['prefijo']='22';body['valor_desde']=5
        self.assertEqual(self.client.post('/api/mostrador/etiquetas/reglas',json=body).status_code,422)
        body['valor_desde']=8;body['activo']=False
        self.assertEqual(self.client.put(f'/api/mostrador/etiquetas/reglas/{rule["id"]}',json=body).status_code,200)

    def test_scale_is_not_falsely_reported_connected(self):
        result=self.client.get('/api/mostrador/balanza').json()
        self.assertFalse(result['integrada']);self.assertEqual(result['modo'],'manual')

    def test_short_internal_code_is_not_mistaken_for_weight_prefix(self):
        self.rule()
        self.client.put(f'/api/gestion/productos/{self.p["id"]}',json={'codigo':'21','descripcion':'Tomate','unidad_venta':'kg'})
        response=self.client.post('/api/mostrador/resolver-codigo',json={'codigo':'21'})
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json()['tipo'],'producto')

    def test_weight_in_grams_and_zero_price_are_explicit(self):
        other=self.create_product('GRAM','Especia','g')
        order,_=self.order(extra={'producto_id':other['id'],'cantidad':'1000','precio':'0.1'})
        self.receive(order,{'clave_operacion':str(uuid4()),'lineas':[{'linea_id':order['lineas'][1]['id'],'bruto_kg':'1','tara_kg':'0','precio':'0.1'}]})
        self.client.post(f'/api/comercial/productos/{other["id"]}/ajuste',json={'tipo':'precio','importe':'0','version':0,'motivo':'Muestra sin cargo','clave_operacion':str(uuid4())})
        sale=self.sale({'lineas':[{'producto_id':other['id'],'bruto_kg':'0.5','tara_kg':'0.125'}]})
        self.assertEqual(sale.status_code,201,sale.text)
        self.assertEqual(Decimal(sale.json()['lineas'][0]['cantidad']),375)
        self.assertEqual(sale.json()['total'],'0.00')

    def test_purchase_suggestion_accounts_for_dates_and_rounding(self):
        self.client.put(f'/api/mostrador/reposicion/{self.p["id"]}',json={'venta_diaria':'12','dias_cobertura':2,'dias_entrega':0,'seguridad':'5'})
        response=self.client.get('/api/mostrador/plan').json();p=response['reposicion'][0]
        self.assertEqual(Decimal(p['sugerencia']),9)
        order,_=self.order(quantity='3');self.assertGreater(order['id'],0)
        self.assertEqual(Decimal(self.client.get('/api/mostrador/plan').json()['reposicion'][0]['sugerencia']),9)
        with sqlite3.connect(database.DB_PATH) as conn:conn.execute('UPDATE pedidos_compra SET fecha_entrega=? WHERE id=?',(str(stock.today()+timedelta(days=1)),order['id']))
        p=self.client.get('/api/mostrador/plan').json()['reposicion'][0]
        self.assertEqual(Decimal(p['sugerencia']),6);self.assertEqual(Decimal(p['entradas_previstas']),3)

    def test_forecast_does_not_treat_new_no_sales_as_evidence_of_no_demand(self):
        p=self.client.get('/api/mostrador/plan').json()['reposicion'][0]
        self.assertEqual(p['base'],'sin_historial_suficiente');self.assertIsNone(p['venta_diaria'])
        sale=self.sale().json()
        p=self.client.get('/api/mostrador/plan').json()['reposicion'][0]
        self.assertEqual(Decimal(p['vendido_periodo']),1)
        self.correction(sale,tipo='anulacion')
        p=self.client.get('/api/mostrador/plan').json()['reposicion'][0]
        self.assertEqual(Decimal(p['vendido_periodo']),0)

    def test_pos_activity_is_visible_in_inventory_alerts(self):
        self.sale()
        p=self.client.get('/api/inventario/resumen').json()['productos'][0]
        self.assertIsNotNone(p['ultima_venta']);self.assertFalse(p['baja_rotacion'])

    def test_returnable_containers_loss_and_deposit_are_separate(self):
        kind=self.client.post('/api/mostrador/envases/tipos',json={'nombre':'Cajón del proveedor'}).json()
        def event(type,qty=0,amount='0'):
            return self.post('/envases/movimientos',proveedor_id=self.s['id'],envase_id=kind['id'],tipo=type,cantidad=qty,importe=amount,referencia='Remito de prueba',motivo='Movimiento confirmado')
        self.assertEqual(event('saldo_inicial',10).status_code,201)
        self.assertEqual(event('perdida',2).status_code,201)
        state=self.client.get('/api/mostrador/envases').json()[0]
        self.assertEqual((state['en_local'],state['por_devolver'],state['perdidos_a_regularizar']),(8,10,2))
        self.assertEqual(event('devuelto',9).status_code,409)
        self.assertEqual(event('baja_acordada',2).status_code,201)
        self.assertEqual(event('deposito_pagado',amount='5000').status_code,201)
        self.assertEqual(event('deposito_reintegrado',amount='2000').status_code,201)
        state=self.client.get('/api/mostrador/envases').json()[0]
        self.assertEqual(Decimal(state['deposito_a_favor']),3000)
        self.assertEqual(event('deposito_reintegrado',amount='3001').status_code,409)
        self.assertEqual(event('saldo_inicial',1).status_code,409)

    def test_crates_do_not_change_food_stock_or_provider_food_debt(self):
        kind=self.client.post('/api/mostrador/envases/tipos',json={'nombre':'Cajón'}).json()
        body={'clave_operacion':str(uuid4()),'proveedor_id':self.s['id'],'envase_id':kind['id'],'tipo':'recibido','cantidad':3,'referencia':'Remito real','motivo':'Recepción de cajones'}
        first=self.client.post('/api/mostrador/envases/movimientos',json=body)
        self.assertEqual(first.status_code,201)
        self.assertEqual(self.client.post('/api/mostrador/envases/movimientos',json=body).json(),first.json())
        self.assertEqual(Decimal(self.finance()['stock']),20)
        self.assertEqual(Decimal(self.client.get('/api/inventario/cuentas').json()[0]['saldo']),20000)

    def test_unauthenticated_checkout_is_rejected(self):
        self.client.delete('/api/comercial/sesion')
        self.assertEqual(self.quote().status_code,401)
        self.assertEqual(self.client.get('/api/mostrador/catalogo').status_code,401)


if __name__=='__main__':unittest.main()
