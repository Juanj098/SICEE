// Base de la API. En desarrollo se usa el proxy de Vite (/api -> localhost:5000).
const API = (import.meta.env.VITE_API_URL ?? "/api").replace(/\/$/, "");

// Envía un POST y traduce la respuesta del backend a un objeto o a un Error.
// El backend a veces responde 200 con { error } (p. ej. POST /catalogos/labs),
// por eso también se revisa el cuerpo.
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

// Crea un investigador. El backend responde { id, nombre }.
export async function crearInvestigador(datos) {
  return enviar("/investigadores/", datos, "No se pudo crear el investigador");
}

// Crea un laboratorio. El backend responde { id, institucion, direccion, descripcion }.
export async function crearLaboratorio(datos) {
  return enviar("/catalogos/labs", datos, "No se pudo crear el laboratorio");
}

// Crea una estufa. El backend responde { id, marca, fabricante, ... }.
export async function crearEstufa(datos) {
  return enviar("/catalogos/estufas", datos, "No se pudo crear la estufa");
}

// Crea un conjunto de pruebas para una estufa.
// El backend responde { id, estufa_id, descripcion }.
export async function crearConjuntoPruebas(datos) {
  return enviar(
    "/pruebas/conjunto_pruebas",
    datos,
    "No se pudo crear el conjunto de pruebas"
  );
}
