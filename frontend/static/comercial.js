(() => {
  'use strict';
  const el = (s,r=document) => r.querySelector(s);
  const all = (s,r=document) => [...r.querySelectorAll(s)];
  const esc = v => String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const cash = n => n===null||n===undefined ? 'Sin registrar' : new Intl.NumberFormat('es-AR',{style:'currency',currency:'ARS',maximumFractionDigits:4}).format(Number(n));
  const quantity = n => new Intl.NumberFormat('es-AR',{maximumFractionDigits:3}).format(Number(n));
  const when = s => new Date(s).toLocaleString('es-AR',{timeZone:'America/Argentina/Cordoba'});
  const newKey = () => crypto.randomUUID();
  let products=[], suppliers=[], orders=[], locations=[], auth={configurado:false,responsable:null}, currentTab='', refreshVersion=0;
  let authMode='login', supplierId=null, orderKey='', receiptOrder=null, receiptKey='', adjustment=null;
  const canEdit = () => ['dueno','encargado'].includes(auth.responsable?.rol);
  const writeOptions = (method,body) => ({method,headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});
  async function request(path, options={}) {
    const response=await fetch('/api/comercial'+path,options);
    const data=await response.json().catch(()=>({}));
    if(!response.ok) {
      if(response.status===401) {auth.responsable=null;renderAuth();}
      throw new Error(Array.isArray(data.detail)?data.detail.map(x=>`${x.loc.slice(1).join('.')}: ${x.msg}`).join(' · '):data.detail||'No se pudo completar la operación. Intentá nuevamente.');
    }
    return data;
  }
  function showError(form,error) {const p=el('.form-error',form);p.textContent=error.message;p.hidden=false;}
  function clearError(form) {el('.form-error',form).hidden=true;}
  function bindForm(id,handler) {
    const form=el(id);
    form.addEventListener('submit',async event=>{
      event.preventDefault();clearError(form);
      const button=el('[type=submit]',form);button.disabled=true;
      try {await handler(form);}catch(error){showError(form,error);}finally{button.disabled=false;}
    });
  }
  all('[data-close]').forEach(button=>button.addEventListener('click',()=>button.closest('dialog').close()));
  async function refresh() {
    const version=++refreshVersion;
    try {
      const [a,p,s,o,l]=await Promise.all([request('/autorizacion'),request('/productos'),request('/proveedores'),request('/pedidos'),request('/ubicaciones')]);
      if(version!==refreshVersion)return;
      auth=a;products=p;suppliers=s;orders=o;locations=l;window.dispatchEvent(new CustomEvent('gestion:autorizacion',{detail:a}));
      renderAuth();renderPrices();renderSuppliers();renderOrders();
    }catch(error){notify(error.message,true);}
  }
  window.addEventListener('gestion:navigate',event=>{
    currentTab=event.detail;
    if(['precios','compras'].includes(currentTab)) refresh();
  });
  window.addEventListener('gestion:autorizar',event=>openAuth(event.detail||'login'));
  all('.refresh-commercial').forEach(button=>button.addEventListener('click',refresh));
  function renderAuth() {
    all('.commercial-auth').forEach(container=>{
      container.innerHTML=`<div class="auth-copy"><strong>${auth.responsable?esc(auth.responsable.nombre)+' · '+esc(auth.responsable.rol):'Cambios con responsable'}</strong><p>${auth.responsable?'La autorización dura 30 minutos. Cada ajuste conserva nombre, fecha y motivo.':auth.configurado?'Ingresá para modificar precios, costos, proveedores y compras.':'Creá el primer responsable con una clave propia para habilitar cambios.'}</p></div>${auth.responsable?'<button class="secondary auth-logout">Cerrar autorización</button>':'<button class="primary auth-open">'+(auth.configurado?'Ingresar':'Crear responsable')+'</button>'}${auth.responsable?.rol==='dueno'?'<button class="secondary auth-add">+ Responsable</button>':''}`;
      el('.auth-open',container)?.addEventListener('click',()=>openAuth(auth.configurado?'login':'setup'));
      el('.auth-add',container)?.addEventListener('click',()=>openAuth('add'));
      el('.auth-logout',container)?.addEventListener('click',async()=>{try{await request('/sesion',{method:'DELETE'});await refresh();}catch(e){notify(e.message,true);}});
    });
    el('#new-supplier').disabled=!canEdit();el('#new-order').disabled=!canEdit();
    all('.requires-commercial').forEach(button=>{button.disabled=!canEdit();});
  }
  function openAuth(mode) {
    authMode=mode;const form=el('#auth-form');form.reset();clearError(form);
    el('#auth-title').textContent=mode==='login'?'Ingresar como responsable':mode==='setup'?'Crear primer responsable':'Agregar responsable';
    el('#auth-help').textContent=mode==='login'?'Usá el nombre y la clave registrados.':'Elegí una clave de al menos 8 caracteres. No hay claves predeterminadas. El primer responsable debe ser el dueño.';
    el('#auth-role-label').hidden=mode!=='add';
    form.elements.clave.autocomplete=mode==='login'?'current-password':'new-password';
    form.elements.clave.minLength=mode==='login'?1:8;
    el('#auth-dialog').showModal();
  }
  bindForm('#auth-form',async form=>{
    const body={nombre:form.elements.nombre.value.trim(),clave:form.elements.clave.value};
    if(authMode!=='login')await request('/responsables',writeOptions('POST',{...body,rol:authMode==='setup'?'dueno':form.elements.rol.value}));
    if(authMode!=='add')await request('/sesion',writeOptions('POST',body));
    form.elements.clave.value='';el('#auth-dialog').close();await refresh();notify('Responsable registrado o autorizado correctamente.');
  });
  function renderPrices() {
    const query=el('#price-search').value.trim().toLocaleLowerCase();
    const items=products.filter(p=>`${p.codigo} ${p.descripcion}`.toLocaleLowerCase().includes(query));
    const container=el('#price-list');container.replaceChildren();
    if(!items.length){container.innerHTML='<div class="empty"><h2>No hay productos para mostrar</h2><p>Cargá productos en el catálogo o probá otra búsqueda.</p><a class="secondary" href="#productos">Ir a productos</a></div>';return;}
    items.forEach(p=>{
      const card=document.createElement('article');card.className='price-card';
      card.innerHTML=`<div class="price-heading"><div><h2>${esc(p.descripcion)}</h2><small>${esc(p.codigo)} · importes por ${esc(p.unidad)}</small></div><span class="status-tag">${quantity(p.stock)} ${esc(p.unidad)} en stock</span></div><div class="price-stats"><div><span>PRECIO DE VENTA</span><strong>${cash(p.precio)}</strong></div><div><span>COSTO DE REPOSICIÓN</span><strong>${cash(p.reposicion)}</strong></div><div><span>COSTO PROMEDIO DE STOCK</span><strong>${cash(p.promedio)}</strong></div><div><span>MARGEN SOBRE VENTA</span><strong class="${Number(p.margen)<0?'negative':''}">${p.margen===null?'—':quantity(p.margen)+'%'}</strong></div><div><span>RECARGO SOBRE COSTO</span><strong>${p.recargo===null?'—':quantity(p.recargo)+'%'}</strong></div></div><div class="price-actions"><button class="primary requires-commercial change-price" ${canEdit()?'':'disabled'}>Cambiar precio</button><button class="secondary requires-commercial change-cost" ${canEdit()?'':'disabled'}>Costo de reposición</button><button class="secondary price-history">Ver historial</button></div>`;
      el('.change-price',card).addEventListener('click',()=>openAdjustment(p,'precio'));
      el('.change-cost',card).addEventListener('click',()=>openAdjustment(p,'reposicion'));
      el('.price-history',card).addEventListener('click',()=>openHistory(p));container.append(card);
    });
  }
  el('#price-search').addEventListener('input',renderPrices);
  function openAdjustment(p,type) {
    adjustment={product:p,tipo:type,key:newKey()};const form=el('#adjust-form');form.reset();clearError(form);
    el('#adjust-title').textContent=type==='precio'?'Cambiar precio de venta':'Actualizar costo de reposición';
    el('#adjust-product').textContent=`${p.descripcion} · ${p.codigo} · por ${p.unidad}`;
    form.elements.importe.value=p[type==='precio'?'precio':'reposicion']??'';
    el('#adjust-hint').textContent=type==='precio'?'El cambio rige desde ahora y no modifica los comprobantes anteriores.':'Este valor ayuda a decidir precios. No modifica costos históricos, stock ni pedidos ya registrados.';
    el('#adjust-dialog').showModal();
  }
  bindForm('#adjust-form',async form=>{
    const p=adjustment.product;
    await request(`/productos/${p.id}/ajuste`,writeOptions('POST',{tipo:adjustment.tipo,importe:form.elements.importe.value,motivo:form.elements.motivo.value.trim(),version:p[adjustment.tipo==='precio'?'version_precio':'version_costo'],clave_operacion:adjustment.key}));
    el('#adjust-dialog').close();await refresh();notify('Cambio guardado con su responsable y motivo.');
  });
  function openHistory(p) {
    const labels={precio:'Precio de venta',reposicion:'Costo de reposición',compra:'Costo de recepción'};
    el('#history-content').innerHTML=`<p>${esc(p.descripcion)} · ${esc(p.codigo)}</p><p class="hint">Fechas en hora de Argentina. Los costos de recepción incluyen los gastos distribuidos.</p>${p.historial.length?`<div class="table-wrap"><table class="data-table"><thead><tr><th>Fecha / responsable</th><th>Tipo</th><th>Anterior → nuevo</th><th>Motivo</th></tr></thead><tbody>${p.historial.map(h=>`<tr><td>${when(h.creado)}<small>${esc(h.responsable)}</small></td><td>${labels[h.tipo]}</td><td>${cash(h.anterior)} → ${cash(h.importe)}<small>Por ${esc(h.unidad)}</small></td><td>${esc(h.motivo)}</td></tr>`).join('')}</tbody></table></div>`:'<div class="empty"><p>Todavía no hay cambios registrados. Los valores heredados se conservan como referencia.</p></div>'}`;
    el('#history-dialog').showModal();
  }
  function renderSuppliers() {
    const container=el('#supplier-list');container.replaceChildren();
    if(!suppliers.length){container.innerHTML='<p class="hint">Todavía no hay proveedores. Agregá el primero para registrar una compra.</p>';return;}
    suppliers.forEach(s=>{
      const card=document.createElement('article');card.className='supplier-card';
      card.innerHTML=`<h3>${esc(s.nombre)}${s.activo?'':' · Inactivo'}</h3><p>${esc([s.contacto,s.telefono].filter(Boolean).join(' · '))||'Sin contacto registrado'}</p><p>${esc(s.condiciones)||'Condiciones pendientes'} · ${s.dias_plazo} días</p><button class="secondary requires-commercial" ${canEdit()?'':'disabled'}>Editar proveedor</button>`;
      el('button',card).addEventListener('click',()=>openSupplier(s));container.append(card);
    });
  }
  function openSupplier(s=null) {
    supplierId=s?.id??null;const form=el('#supplier-form');form.reset();clearError(form);
    ['nombre','contacto','telefono','documento','condiciones','dias_plazo'].forEach(k=>{form.elements[k].value=s?.[k]??(k==='dias_plazo'?0:'');});
    form.elements.activo.checked=s?!!s.activo:true;el('#supplier-dialog').showModal();
  }
  el('#new-supplier').addEventListener('click',()=>openSupplier());
  bindForm('#supplier-form',async form=>{
    const body=Object.fromEntries(['nombre','contacto','telefono','documento','condiciones'].map(k=>[k,form.elements[k].value.trim()]));
    body.dias_plazo=Number(form.elements.dias_plazo.value);body.activo=form.elements.activo.checked;
    const saved=await request('/proveedores'+(supplierId?'/'+supplierId:''),writeOptions(supplierId?'PUT':'POST',body));
    supplierId=saved.id;el('#supplier-dialog').close();await refresh();notify('Proveedor guardado.');
  });
  function renderOrders() {
    const container=el('#order-list');container.replaceChildren();
    if(!orders.length){container.innerHTML='<div class="empty"><h2>La próxima compra, organizada.</h2><p>Registrá un pedido. Al llegar la mercadería, confirmá cantidades, calidad y costos reales.</p></div>';return;}
    orders.forEach(order=>{
      const card=document.createElement('article');card.className='order-card';
      card.innerHTML=`<div class="order-heading"><div><h2>Pedido #${order.id} · ${esc(order.proveedor_nombre)}</h2><p>${when(order.creado)} · ${esc(order.responsable)}</p></div><span class="status-tag ${order.estado}">${order.estado}</span></div><div class="order-totals"><span><small>Estimado sin gastos</small><strong>${cash(order.total_estimado)}</strong></span><span><small>Productos</small><strong>${order.lineas.length}</strong></span><span><small>Recepciones</small><strong>${order.recepciones.length}</strong></span></div><div class="price-actions"><button class="secondary order-detail">Ver pedido</button><button class="primary requires-commercial receive-order" ${canEdit()&&order.estado!=='recibido'?'':'disabled'}>Recibir mercadería</button></div>`;
      el('.order-detail',card).addEventListener('click',()=>openOrderDetail(order));
      el('.receive-order',card).addEventListener('click',()=>openReceipt(order));container.append(card);
    });
  }
  function openOrder() {
    if(!suppliers.some(s=>s.activo)||!products.length){notify('Primero cargá al menos un proveedor activo y un producto.',true);return;}
    const form=el('#order-form');form.reset();clearError(form);orderKey=newKey();
    form.elements.proveedor_id.innerHTML=suppliers.filter(s=>s.activo).map(s=>`<option value="${s.id}">${esc(s.nombre)}</option>`).join('');
    el('#order-lines').replaceChildren();orderLine();el('#order-dialog').showModal();
  }
  function orderLine() {
    const row=document.createElement('div');row.className='purchase-line';
    row.innerHTML=`<div class="line-head"><select data-field="producto_id" aria-label="Producto del pedido">${products.map(p=>`<option value="${p.id}">${esc(p.descripcion)} · ${esc(p.codigo)}</option>`).join('')}</select><button type="button" class="icon-button" aria-label="Quitar línea">×</button></div><div class="two"><label>Cantidad solicitada<input data-field="cantidad" type="number" required min="0.001" max="99999999999" step="0.001"></label><label>Precio de compra por <span class="line-unit"></span> ($)<input data-field="precio" type="number" required min="0" max="9999999999" step="0.0001"></label></div>`;
    function update(){const p=products.find(p=>p.id===Number(el('[data-field=producto_id]',row).value));el('.line-unit',row).textContent=p.unidad;el('[data-field=precio]',row).value=p.reposicion??'';const input=el('[data-field=cantidad]',row);input.step=['kg','g'].includes(p.unidad)?'0.001':'1';input.min=['kg','g'].includes(p.unidad)?'0.001':'1';}
    el('select',row).addEventListener('change',update);el('button',row).addEventListener('click',()=>row.remove());update();el('#order-lines').append(row);
  }
  el('#new-order').addEventListener('click',openOrder);el('#add-order-line').addEventListener('click',orderLine);
  bindForm('#order-form',async form=>{
    const lineas=all('#order-lines .purchase-line').map(row=>({producto_id:Number(el('[data-field=producto_id]',row).value),cantidad:el('[data-field=cantidad]',row).value,precio:el('[data-field=precio]',row).value}));
    await request('/pedidos',writeOptions('POST',{proveedor_id:Number(form.elements.proveedor_id.value),fecha_entrega:form.elements.fecha_entrega.value||null,notas:form.elements.notas.value.trim(),lineas,clave_operacion:orderKey}));
    el('#order-dialog').close();await refresh();notify('Pedido registrado. El stock se actualiza al recibir.');
  });
  function openOrderDetail(order) {
    el('#order-detail-title').textContent=`Pedido #${order.id} · ${order.proveedor_nombre}`;
    el('#order-detail-content').innerHTML=`<p>${esc(order.condiciones)||'Sin condiciones registradas'} · plazo ${order.dias_plazo} días</p><p>${esc(order.notas)}</p><div class="table-wrap"><table class="data-table"><thead><tr><th>Producto</th><th>Pedido</th><th>Aceptado</th><th>Pendiente</th><th>Precio estimado</th></tr></thead><tbody>${order.lineas.map(l=>`<tr><td>${esc(l.descripcion)}<small>${esc(l.unidad)}</small></td><td>${quantity(l.cantidad)}</td><td>${quantity(l.recibido)}</td><td>${quantity(l.pendiente)}</td><td>${cash(l.precio)}</td></tr>`).join('')}</tbody></table></div><h3>Recepciones</h3>${order.recepciones.length?order.recepciones.map(r=>`<article class="receipt-summary"><h3>Recepción #${r.id} · ${cash(r.total)}</h3><p>${when(r.creado)} · ${esc(r.responsable)} · ${esc(r.referencia)||'Sin referencia'}</p><p>Flete ${cash(r.flete)} · otros gastos ${cash(r.otros_gastos)}</p>${r.lineas.map(l=>`<p><b>${esc(l.descripcion)}</b>: aceptado ${quantity(l.aceptado)} ${esc(l.unidad)}, rechazado ${quantity(l.rechazado)} ${esc(l.unidad)} · ${esc(l.calidad)}. Costo puesto: ${cash(l.costo_unitario)} / ${esc(l.unidad)}.</p><p class="hint">${l.bruto_kg!==null?'Bruto '+quantity(l.bruto_kg)+' kg − tara '+quantity(l.tara_kg)+' kg · ':''}${l.bultos} bultos · ${l.importe_mercaderia!==null&&l.importe_mercaderia!==undefined?'mercadería por importe '+cash(l.importe_mercaderia):'precio '+cash(l.precio)} · gastos asignados ${cash(l.gastos_asignados)}. ${esc(l.observaciones)}</p>`).join('')}</article>`).join(''):'<p class="hint">Todavía no se recibió mercadería.</p>'}`;
    el('#order-detail-dialog').showModal();
  }
  function openReceipt(order) {
    receiptOrder=order;receiptKey=newKey();const form=el('#receipt-form');form.reset();clearError(form);
    form.elements.ubicacion_id.innerHTML=locations.map(l=>`<option value="${l.id}">${esc(l.nombre)}</option>`).join('');
    el('#receipt-title').textContent=`Recibir pedido #${order.id}`;const container=el('#receipt-lines');container.replaceChildren();
    order.lineas.filter(l=>Number(l.pendiente)>0).forEach(line=>{
      const weighted=['kg','g'].includes(line.unidad);const row=document.createElement('div');row.className='purchase-line';row.dataset.lineId=line.id;
      row.innerHTML=`<div class="line-head"><h3>${esc(line.descripcion)}</h3><label class="check"><input type="checkbox" class="include-line" checked>Recibir</label></div><p>Pendiente: ${quantity(line.pendiente)} ${esc(line.unidad)}</p><div class="three"><label>Bultos / envases<input data-field="bultos" type="number" min="0" max="1000000" step="1" value="0" required></label>${weighted?'<label>Peso bruto (kg)<input data-field="bruto_kg" type="number" min="0.001" max="99999999999" step="0.001" required></label><label>Tara total (kg)<input data-field="tara_kg" type="number" min="0" max="99999999999" step="0.001" value="0" required></label>':`<label>Cantidad entregada (${esc(line.unidad)})<input data-field="cantidad" type="number" min="1" max="99999999999" step="1" required></label>`}</div><div class="three"><label>Rechazado (${esc(line.unidad)})<input data-field="rechazado" type="number" min="0" max="99999999999" step="${weighted?'0.001':'1'}" value="0" required></label><label class="receipt-unit-price">Precio por ${esc(line.unidad)} ($)<input data-field="precio" type="number" min="0" max="9999999999" step="0.0001" value="${esc(line.precio)}" required></label><label class="receipt-total-price" hidden>Importe de mercadería aceptada ($)<input data-field="importe_mercaderia" type="number" min="0" max="999999999999" step="0.01" required disabled></label><label>Calidad<select data-field="calidad"><option value="buena">Buena</option><option value="regular">Regular</option><option value="mala">Mala</option></select></label></div><label>Cómo se cobra esta entrega<select class="receipt-pricing-mode"><option value="unidad">Precio por unidad de venta</option><option value="total">Importe total (ej.: compra por cajón de peso variable)</option></select></label><label>Observaciones / motivo de rechazo<textarea data-field="observaciones" maxlength="500" rows="2"></textarea></label><p class="receipt-info">Completá los datos reales de la entrega.</p>`;
      function preview(){const field=name=>Number(el(`[data-field=${name}]`,row)?.value||0);const net=weighted?(field('bruto_kg')-field('tara_kg'))*(line.unidad==='g'?1000:1):field('cantidad');el('.receipt-info',row).textContent=`Neto recibido: ${quantity(net)} ${line.unidad} · aceptado: ${quantity(net-field('rechazado'))} ${line.unidad}.`;}
      row.addEventListener('input',preview);
      function pricingMode(){
        const included=el('.include-line',row).checked;
        const total=el('.receipt-pricing-mode',row).value==='total';
        all('[data-field]',row).forEach(input=>{input.disabled=!included;});
        el('[data-field=precio]',row).disabled=!included||total;
        el('[data-field=importe_mercaderia]',row).disabled=!included||!total;
        el('.receipt-unit-price',row).hidden=total;
        el('.receipt-total-price',row).hidden=!total;
        row.classList.toggle('disabled',!included);
      }
      el('.include-line',row).addEventListener('change',pricingMode);
      el('.receipt-pricing-mode',row).addEventListener('change',pricingMode);
      container.append(row);
    });
    el('#receipt-dialog').showModal();
  }
  bindForm('#receipt-form',async form=>{
    const lineas=all('#receipt-lines .purchase-line').filter(row=>el('.include-line',row).checked).map(row=>{
      const data=Object.fromEntries(all('[data-field]:not(:disabled)',row).map(input=>[input.dataset.field,input.value.trim()]));
      data.linea_id=Number(row.dataset.lineId);data.bultos=Number(data.bultos);return data;
    });
    const receipt=await request(`/pedidos/${receiptOrder.id}/recepciones`,writeOptions('POST',{clave_operacion:receiptKey,ubicacion_id:Number(form.elements.ubicacion_id.value),gastos_a_proveedor:form.elements.gastos_a_proveedor.checked,referencia:form.elements.referencia.value.trim(),flete:form.elements.flete.value,otros_gastos:form.elements.otros_gastos.value,lineas}));
    el('#receipt-dialog').close();await refresh();notify(`Recepción #${receipt.id} registrada: ${cash(receipt.total)}. Stock y costos actualizados.`);
  });
})();
