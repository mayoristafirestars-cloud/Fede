'use strict';
const $ = (selector, root = document) => root.querySelector(selector);
const $$ = (selector, root = document) => [...root.querySelectorAll(selector)];
const escapeHTML = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const stable = value => JSON.stringify(value, (key, item) => Array.isArray(item) && ['medios_pago','funciones_previstas','canales_venta'].includes(key) ? [...item].sort() : item && !Array.isArray(item) && typeof item === 'object' ? Object.fromEntries(Object.keys(item).sort().map(name => [name,item[name]])) : item);
const businessForm = $('#business-form');
const productForm = $('#product-form');
const dialog = $('#product-dialog');
let savedBusiness = null;
let productItems = [];
let unitItems = [];
let noticeTimer;
let requestNumber = 0;
let loading = true;

function notify(message, error = false) {
  clearTimeout(noticeTimer);
  const el = $('#notice'); el.textContent = message; el.hidden = false; el.classList.toggle('error', error);
  noticeTimer = setTimeout(() => { el.hidden = true; }, error ? 12000 : 5000);
}
async function api(path, options = {}) {
  const response = await fetch('/api/gestion' + path, options);
  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    const detail = data.detail;
    throw new Error(Array.isArray(detail) ? detail.map(e => `${e.loc.slice(1).join('.')}: ${e.msg}`).join(' · ') : detail || 'No se pudo completar la operación. Intentá nuevamente.');
  }
  return data;
}
const jsonOptions = (method, body) => ({method, headers: {'Content-Type': 'application/json'}, body: JSON.stringify(body)});
const options = (items, selected) => items.map(([value, label]) => `<option value="${value}"${value === selected ? ' selected' : ''}>${label}</option>`).join('');

function personRow(person = {nombre: '', rol: 'cajero'}) {
  const row = document.createElement('div'); row.className = 'dynamic-row';
  row.innerHTML = `<label>Nombre<input data-field="nombre" maxlength="100" required value="${escapeHTML(person.nombre)}" placeholder="Nombre de la persona"></label><label>Función<select data-field="rol">${options([['dueno','Dueño/a'],['encargado','Encargado/a'],['cajero','Cajero/a']],person.rol)}</select></label><button type="button" class="icon-button" aria-label="Quitar persona">×</button>`;
  $('button', row).addEventListener('click', () => { row.remove(); markDirty(); });
  $('#people-list').append(row);
}
function equipmentRow(equipment = {tipo:'balanza',marca_modelo:'',conexion:'pendiente',estado:'pendiente'}) {
  const row = document.createElement('div'); row.className = 'equipment-row';
  row.innerHTML = `<div class="equipment-top"><label class="sr-only">Tipo de equipo</label><select data-field="tipo" aria-label="Tipo de equipo">${options([['computadora','Computadora'],['tablet','Tablet'],['balanza','Balanza'],['lector','Lector'],['impresora','Impresora']],equipment.tipo)}</select><button type="button" class="icon-button" aria-label="Quitar equipo">×</button></div><label>Marca y modelo<input data-field="marca_modelo" maxlength="150" placeholder="Pendiente de relevar" value="${escapeHTML(equipment.marca_modelo)}"></label><div class="two"><label>Conexión<select data-field="conexion">${options([['pendiente','Pendiente'],['usb','USB'],['serie','Serie'],['red','Red'],['bluetooth','Bluetooth'],['otra','Otra']],equipment.conexion)}</select></label><label>Disponibilidad<select data-field="estado">${options([['pendiente','Pendiente'],['disponible','Disponible'],['por_comprar','Por comprar']],equipment.estado)}</select></label></div><label>Observaciones del equipo<input data-field="notas" maxlength="300" value="${escapeHTML(equipment.notas||'')}"></label>`;
  $('button', row).addEventListener('click', () => { row.remove(); markDirty(); });
  $('#equipment-list').append(row);
}
function readRows(selector) {
  return $$(selector).map(row => Object.fromEntries($$('[data-field]',row).map(input => [input.dataset.field,input.value.trim()])));
}
const businessFields = ['nombre','localidad','atencion','pesaje','cobro','entrega','contador','situacion_fiscal','comprobantes','internet','contingencia','tiene_contador','notas_local'];
function readBusiness() {
  const value = Object.fromEntries(businessFields.map(name => [name,businessForm.elements[name].value.trim()]));
  value.personas = readRows('#people-list .dynamic-row');
  value.equipos = readRows('#equipment-list .equipment-row');
  value.funciones_previstas = $$('[name=funcion_prevista]:checked').map(i=>i.value);
  value.canales_venta = $$('[name=canal_venta]:checked').map(i=>i.value);
  value.medios_pago = $$('[name=pago]:checked').map(input => input.value);
  value.fiscal_revisado = businessForm.elements.fiscal_revisado.checked;
  return value;
}
function updateBrand(name){$('#business-brand').textContent=name||'Mi verdulería';document.title=(name||'Mi verdulería')+' · Gestión del local';}
function fillBusiness(data) {
  updateBrand(data.nombre);
  $$('[name=funcion_prevista]').forEach(i=>{i.checked=(data.funciones_previstas||[]).includes(i.value);});
  $$('[name=canal_venta]').forEach(i=>{i.checked=(data.canales_venta||[]).includes(i.value);});
  businessFields.forEach(name => { businessForm.elements[name].value = data[name]; });
  businessForm.elements.fiscal_revisado.checked = data.fiscal_revisado;
  $$('[name=pago]').forEach(input => { input.checked = data.medios_pago.includes(input.value); });
  $('#people-list').replaceChildren(); data.personas.forEach(personRow);
  $('#equipment-list').replaceChildren(); data.equipos.forEach(equipmentRow);
  updateProgress(data);
}
function updateProgress(data) {
  const complete = [
    !!data.nombre && !!data.localidad && ['atencion','pesaje','cobro','entrega'].every(key => data[key] !== 'pendiente'),
    data.personas.length > 0,
    ['computadora','balanza','lector','impresora'].every(tipo => data.equipos.some(e => e.tipo === tipo && e.estado !== 'pendiente' && e.marca_modelo)),
    data.medios_pago.length > 0,
    data.fiscal_revisado,
    data.internet !== 'pendiente' && !!data.contingencia
  ];
  const count = complete.filter(Boolean).length;
  $('#progress-label').textContent = `${count} de 6 puntos relevados`;
  $('#progress-dots').innerHTML = complete.map((done,i) => `<span class="dot${done?' done':''}" title="Punto ${i+1}: ${done?'relevado':'pendiente'}">${String(i+1).padStart(2,'0')}</span>`).join('');
}
function markDirty() {
  if (loading) return;
  $('#save-state').textContent = stable(readBusiness()) === stable(savedBusiness) ? 'Sin cambios pendientes' : 'Cambios sin guardar';
}
businessForm.addEventListener('input',markDirty);
businessForm.addEventListener('change',markDirty);
$$('[form=business-form]').forEach(el=>el.addEventListener('input',markDirty));
$('#add-person').addEventListener('click',() => { personRow(); markDirty(); });
$('#add-equipment').addEventListener('click',() => { equipmentRow(); markDirty(); });
businessForm.addEventListener('submit',async event => {
  event.preventDefault();
  if (loading) return;
  const buttons = $$('button[type=submit][form=business-form], #business-form button[type=submit]');
  buttons.forEach(b => { b.disabled = true; });
  try {
    savedBusiness = await api('/negocio',jsonOptions('PUT',readBusiness()));
    updateBrand(savedBusiness.nombre); updateProgress(savedBusiness); markDirty(); notify('Configuración guardada. Podés completar los pendientes cuando quieras.');
  } catch (error) { notify(error.message,true); }
  finally { buttons.forEach(b => { b.disabled = false; }); }
});

function navigate() {
  const requested = location.hash.slice(1);
  const tab = ['productos','precios','compras','inventario','cuentas','caja','plan','envases','tiendaweb'].includes(requested) ? requested : 'negocio';
  ['negocio','productos','precios','compras','inventario','cuentas','caja','plan','envases','tiendaweb'].forEach(name => { $(`#${name}-page`).hidden = tab !== name; });
  $$('[data-tab]').forEach(a => a.classList.toggle('active',a.dataset.tab === tab));
  if (tab === 'productos') loadProducts();
  window.dispatchEvent(new CustomEvent('gestion:navigate', {detail:tab}));
}
window.addEventListener('hashchange',navigate);

async function loadProducts() {
  const current = ++requestNumber;
  const params = new URLSearchParams({buscar:$('#product-search').value,incluir_inactivos:$('#show-inactive').checked});
  try {
    const items = await api('/productos?' + params);
    if (current !== requestNumber) return;
    productItems = items;
    $('#product-count').textContent = `${items.length} producto${items.length === 1 ? '' : 's'}`;
    renderProducts();
  } catch(error) {
    if (current !== requestNumber) return;
    $('#product-grid').innerHTML = '<div class="empty"><h2>No pudimos cargar el catálogo</h2><p>Revisá la conexión y volvé a intentarlo.</p><button class="secondary" id="retry-products">Reintentar</button></div>';
    $('#retry-products').addEventListener('click',loadProducts); notify(error.message,true);
  }
}
function renderProducts() {
  const grid = $('#product-grid'); grid.replaceChildren();
  if (!productItems.length) {
    const filtered = $('#product-search').value.trim();
    grid.innerHTML = `<div class="empty"><div class="empty-icon">✳</div><h2>${filtered?'No encontramos coincidencias':'Tu catálogo empieza acá'}</h2><p>${filtered?'Probá con otro nombre, código o alias.':'Agregá el primer producto con su unidad, variedad y código. No cargamos mercadería ni stock ficticios.'}</p>${filtered?'':'<button class="primary" id="first-product">+ Crear primer producto</button>'}</div>`;
    $('#first-product')?.addEventListener('click',() => openProduct());
    return;
  }
  productItems.forEach(p => {
    const card = document.createElement('article'); card.className = 'product-card';
    const unit = unitItems.find(u => u.codigo === p.unidad_venta)?.nombre || p.unidad_venta;
    card.innerHTML = `<div class="product-photo">${p.foto?.startsWith('/media/')?`<img src="${escapeHTML(p.foto)}" alt="${escapeHTML(p.descripcion)}" loading="lazy">`:'✳'}</div><div class="product-content"><h2>${escapeHTML(p.descripcion)}${p.activo?'':' · Inactivo'}</h2><p>${escapeHTML([p.variedad,p.calidad,p.presentacion].filter(Boolean).join(' · ') || p.rubro)}</p><div class="product-meta"><span class="product-code">${escapeHTML(p.codigo)}</span><span class="unit-tag">${escapeHTML(unit)}</span></div><p class="hint">${p.aliases.length?'También: '+escapeHTML(p.aliases.join(', ')):'Sin nombres alternativos'}</p><button class="secondary">Editar producto</button></div>`;
    $('button',card).addEventListener('click',() => openProduct(p)); grid.append(card);
  });
}
function openProduct(product = null) {
  productForm.reset(); $('#product-error').hidden = true;
  $('#product-title').textContent = product ? 'Editar producto' : 'Nuevo producto';
  productForm.elements.id.value = product?.id || '';
  ['codigo','descripcion','rubro','unidad_venta','variedad','calidad','presentacion'].forEach(key => { productForm.elements[key].value = product?.[key] ?? ({rubro:'Verduras',unidad_venta:'kg'}[key] || ''); });
  productForm.elements.aliases.value = product?.aliases.join(', ') || '';
  productForm.elements.activo.checked = product ? !!product.activo : true;
  $('#photo-preview').hidden = !product?.foto;
  if (product?.foto?.startsWith('/media/')) $('#photo-preview').src = product.foto;
  else $('#photo-preview').removeAttribute('src');
  dialog.showModal(); productForm.elements.descripcion.focus();
}
$('#new-product').addEventListener('click',() => openProduct());
$('#close-product').addEventListener('click',() => dialog.close());
$('#cancel-product').addEventListener('click',() => dialog.close());
let searchTimer;
$('#product-search').addEventListener('input',() => { clearTimeout(searchTimer); searchTimer = setTimeout(loadProducts,180); });
$('#show-inactive').addEventListener('change',loadProducts);
productForm.addEventListener('submit',async event => {
  event.preventDefault(); $('#product-error').hidden = true;
  const photo = productForm.elements.foto.files[0];
  if (photo && photo.size > 5*1024*1024) { $('#product-error').textContent = 'La foto debe pesar hasta 5 MB.'; $('#product-error').hidden = false; return; }
  $('#save-product').disabled = true;
  let productSaved = false;
  try {
    const fields = ['codigo','descripcion','rubro','unidad_venta','variedad','calidad','presentacion'];
    const data = Object.fromEntries(fields.map(key => [key,productForm.elements[key].value.trim()]));
    data.aliases = productForm.elements.aliases.value.split(',').map(s => s.trim()).filter(Boolean);
    data.activo = productForm.elements.activo.checked;
    const id = productForm.elements.id.value;
    const saved = await api('/productos' + (id ? '/'+id : ''),jsonOptions(id?'PUT':'POST',data));
    productSaved = true;
    // Keep the ID if image upload fails: retry must edit, never create twice.
    productForm.elements.id.value = saved.id;
    $('#product-title').textContent = 'Editar producto';
    if (photo) {
      const form = new FormData(); form.append('archivo',photo);
      await api(`/productos/${saved.id}/foto`,{method:'POST',body:form});
    }
    dialog.close(); await loadProducts(); notify('Producto guardado correctamente.');
  } catch(error) {
    $('#product-error').textContent = (productSaved?'El producto quedó guardado; no se pudo completar la foto. ':'') + error.message;
    $('#product-error').hidden = false;
    if (productSaved) loadProducts();
  } finally { $('#save-product').disabled = false; }
});
window.addEventListener('beforeunload',event => {
  if (savedBusiness && stable(readBusiness()) !== stable(savedBusiness)) { event.preventDefault(); event.returnValue = ''; }
});
async function init() {
  $('#save-business').disabled = true;
  $('#new-product').disabled = true;
  try {
    const [data, units] = await Promise.all([api('/negocio'),api('/unidades')]);
    savedBusiness = data; unitItems = units;
    $('#unit-options').innerHTML = units.map(u => `<option value="${escapeHTML(u.codigo)}">${escapeHTML(u.nombre)}${u.fraccionable?' · admite fracciones':''}</option>`).join('');
    fillBusiness(data); loading = false;
    $('#save-business').disabled = false; $('#new-product').disabled = false;
    navigate();
  } catch(error) {
    $('#progress-label').textContent = 'No se pudo cargar la configuración'; notify(error.message,true);
    // Prevent accidental replacement of stored settings after a failed load.
    $$('input,select,textarea,button',businessForm).forEach(el => { el.disabled = true; });
  }
}
init();
