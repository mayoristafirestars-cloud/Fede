(() => {
  const print=document.querySelector('#print-document'),complete=document.querySelector('#complete-photos'),message=document.querySelector('#document-message');
  const missingAtRegistration=document.body.dataset.missing==='1';
  function block(text){document.body.dataset.missing='1';print.disabled=true;message.textContent=text;}
  async function ready(){const images=[...document.querySelectorAll('.product-photo')];try{await Promise.all(images.map(img=>img.decode()));if(images.some(img=>!img.naturalWidth))throw Error();}catch{block('No se pudo cargar alguna foto. Revisá los archivos y la conexión antes de imprimir.');return false;}if(!missingAtRegistration){document.body.dataset.missing='0';print.disabled=false;}return !missingAtRegistration;}
  ready();
  print.addEventListener('click',async()=>{if(await ready())window.print();});
  window.addEventListener('beforeprint',()=>{if([...document.querySelectorAll('.product-photo')].some(img=>!img.complete||!img.naturalWidth))block('Esperá a que se carguen todas las imágenes.');});
  complete.addEventListener('click',async()=>{complete.disabled=true;try{const r=await fetch(document.body.dataset.completeUrl,{method:'POST'});const data=await r.json();if(!r.ok)throw Error(r.status===401||r.status===403?'Ingresá en el sistema como dueño o encargada para completar las fotos.':data.detail||'No se pudieron completar las fotos.');if(data.completadas)location.reload();else message.textContent='Primero cargá las fotos faltantes en las fichas de los productos. No se modificaron importes ni cantidades.';}catch(e){message.textContent=e.message;}finally{complete.disabled=false;}});
})();
