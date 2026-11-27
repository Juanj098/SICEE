import {get, post, patch} from './Client'

const API = (import.meta.env.VITE_API_URL ?? "/api").replace(/\/$/, "");

async function enviar(ruta, datos, mensajeError) {
  const res = await fetch(`${API}${ruta}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(datos),
  });

  const cuerpo = await res.json().catch(() => null);

  if (!res.ok || cuerpo?.error) {
    throw new Error(cuerpo?.error ?? `${mensajeError} (HTTP ${res.status})`);
  }

  return cuerpo;
}


export const listActivos = () => get('/investigadores/list_activos')
export const listLabs = () => get('/catalogos/labs')
export const listEstufas = () => get('/catalogos/estufas')
export const listConjuntos = () => get('/pruebas/conjunto_pruebas')
export const listCombusiblesA = () => get('/catalogos/combustible/activos')
export const listEspeciesActivas = () => get('/catalogos/especies/activos')
export const crearInvestigador = (datos) => post('/investigadores/', datos)
export const crearLaboratorio = (datos) => post('/catalogos/labs', datos)
export const crearEstufa = (datos) => post('/catalogos/estufas', datos)
export const crearCombustible = (datos) => post('/catalogos/combustible', datos)
export const eliminatInvestigador = (id) => patch(`/investigadores/${id}`, {activo:false})
export const eliminarLaboratorio = (id) => patch(`/catalogos/labs/${id}`, {activo:false})
export const eliminarEstufa = (id) => patch(`/catalogos/estufas/${id}`, {activo:false})
export const eliminarCombustible = (id) => patch(`/catalogos/combustible/${id}`, {activo:false})



// Crea un conjunto de pruebas para una estufa.
// El backend responde { id, estufa_id, descripcion }.
export async function crearConjuntoPruebas(datos) {
  return enviar(
    "/pruebas/conjunto_pruebas",
    datos,
    "No se pudo crear el conjunto de pruebas"
  );
}



// Crea las condiciones ambientales de una prueba.
export async function crearCondicionesAmbientales(datos) {
  return enviar(
    "/pruebas/condiciones_ambientales",
    datos,
    "No se pudieron crear las condiciones ambientales"
  );
}
