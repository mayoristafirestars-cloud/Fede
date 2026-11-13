document.querySelector('#login').addEventListener('submit',async event=>{
  event.preventDefault();const form=event.target,button=form.querySelector('button');button.disabled=true;
  try{
    const response=await fetch('/api/comercial/sesion',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(Object.fromEntries(new FormData(form)))});
    if(!response.ok){const data=await response.json();throw new Error(typeof data.detail==='string'?data.detail:'Revisá el nombre y la clave');}
    location.assign('/');
  }catch(error){document.querySelector('#error').textContent=error.message;}finally{button.disabled=false;}
});
