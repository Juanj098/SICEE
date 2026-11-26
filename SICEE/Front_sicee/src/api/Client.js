const API = (import.meta.env.VITE_API_URL ?? "/api").replace(/\/$/, "");

async function pedir(ruta, opts = []) {
  const res = await fetch(`${API}${ruta}`,{
    headers:{"Content-Type":"application/json"},
    ...opts
  });
  const datos = await res.json().catch(()=>null);
  if (!res.ok) throw new Error(datos?.error?? `Error ${res.status}`);
  return datos
  
}

export const get =(ruta)=> pedir(ruta)
export const post = (ruta, datos) => pedir(ruta, {method:"POST", body: JSON.stringify(datos)})
export const patch = (ruta, datos) => pedir(ruta, {method: "PATCH", body: JSON.stringify(datos)})