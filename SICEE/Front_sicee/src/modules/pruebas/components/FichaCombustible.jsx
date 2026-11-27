const SIN_DATO = "—";

// El backend guarda 0.00 cuando un número no se envía; en estos campos un 0 no
// tiene sentido físico, así que se muestra como "sin dato".
const numero = (valor, unidad, mostrarCero = false) => {
  if (valor === null || valor === undefined || valor === "") return SIN_DATO;
  const n = Number(valor);
  if (!Number.isFinite(n) || (n === 0 && !mostrarCero)) return SIN_DATO;
  return unidad ? `${n} ${unidad}` : String(n);
};

const texto = (valor) =>
  valor === null || valor === undefined || valor === "" ? SIN_DATO : String(valor);

export default function FichaCombustible({ combustible }) {
  if (!combustible) return null;

  const conReferencia = combustible.especie_id != null;
  const filas = [
    ["Especie", texto(combustible.especie)],
    ["Fuente", texto(combustible.fuente)],
    ["Poder calorífico neto", numero(combustible.poder_calorifico_neto_mj_kg, "MJ/kg", conReferencia)],
    ["Poder calorífico bruto", numero(combustible.poder_calorifico_bruto_mj_kg, "MJ/kg", conReferencia)],
    ["Poder calorífico del carbón", numero(combustible.poder_calorifico_carbon_mj_kg, "MJ/kg", conReferencia)],
    ["Carbono de la madera", numero(combustible.contenido_carbono_pct, "%", conReferencia)],
    ["Carbono del carbón", numero(combustible.contenido_carbono_carbon_pct, "%")],
    ["Largo del combustible", numero(combustible.longitud_combustible_cm, "cm")],
    ["Ancho del combustible", numero(combustible.ancho_combustible_cm, "cm")],
    ["Tipo de alimentación", texto(combustible.tipo_alimentacion)],
  ];

  return (
    <div className="mt-3 rounded-md border border-[#e9f0ec] bg-[#f7faf8] p-4">
      <div className="flex flex-wrap items-baseline justify-between gap-2">
        <h4 className="text-sm font-semibold text-[#141a17]">
          Datos del combustible
        </h4>
        <span className="text-xs text-[#5d6862]">{combustible.tipo}</span>
      </div>

      <dl className="mt-3 grid gap-x-6 gap-y-2 sm:grid-cols-2 lg:grid-cols-4">
        {filas.map(([etiqueta, valor]) => (
          <div key={etiqueta}>
            <dt className="text-xs text-[#5d6862]">{etiqueta}</dt>
            <dd className="text-sm text-[#141a17]">{valor}</dd>
          </div>
        ))}
        <div className="sm:col-span-2 lg:col-span-4">
          <dt className="text-xs text-[#5d6862]">Descripción</dt>
          <dd className="text-sm text-[#141a17]">{texto(combustible.descripcion)}</dd>
        </div>
      </dl>

      <p className="mt-3 text-xs text-[#5d6862]">
        El poder calorífico neto y el del carbón entran al cálculo; el carbono y
        las dimensiones son informativos.
      </p>
    </div>
  );
}
