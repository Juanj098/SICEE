import { FASES } from "../fases";
import { codigoConjunto } from "../conjuntos";
import { useEffect, useState } from "react";
import { get } from "../../../api/Client";

const ENERGIA_IWA = [
  ["eficiencia_alta_pct", "Eficiencia a alta potencia (%)"],
  ["consumo_especifico_baja_mj_min_l", "Consumo específico a baja potencia (MJ/(min·L))"],
];

const METRICAS = [
  ["tiempo_fase_min", "Tiempo de fase", "min"],
  ["masa_agua_inicial_kg", "Masa de agua inicial", "kg"],
  ["masa_agua_final_kg", "Masa de agua final", "kg"],
  ["masa_agua_evaporada_kg", "Agua evaporada", "kg"],
  ["masa_agua_efectiva_kg", "Agua efectiva", "kg"],
  ["combustible_consumido_kg", "Combustible consumido", "kg"],
  ["tiempo_ebullicion_min", "Tiempo de ebullición", "min"],
  ["tiempo_ebullicion_corregido_min", "Tiempo de ebullición corregido", "min"],
  ["energia_util_kj", "Energía útil", "kJ"],
  ["energia_combustible_kj", "Energía del combustible", "kJ"],
  ["eficiencia_termica_pct", "Eficiencia térmica", "%"],
  ["consumo_especifico_g_l", "Consumo específico", "g/L"],
  ["velocidad_combustion_g_min", "Velocidad de combustión", "g/min"],
  ["potencia_fase_kw", "Potencia de fase", "kW"],
  ["energia_especifica_corregida_kj_l", "Energía específica corregida", "kJ/L"],
  ["combustible_seco_equivalente_kg", "Combustible seco equivalente", "kg"],
  ["cambio_carbon_kg", "Cambio de carbón", "kg"],
  ["consumo_especifico_corregido_g_l", "Consumo específico corregido", "g/L"],
];

const numero = (valor) => {
  if (valor === null || valor === undefined || valor === "") return "—";
  const n = Number(valor);
  return Number.isFinite(n) ? n.toFixed(2) : "—";
};

export default function ResultadosPrueba({
  resumen,
  resultados,
  errorCalculo,
  onNuevaPrueba,
}) {
  const [iwa, setIwa] = useState(null);
  const [errorIwa, setErrorIwa] = useState("");
  useEffect(() => {
    let vigente = true;
    get(`/calculos/conjuntos/${resumen.conjunto_pruebas_id}/iwa`)
      .then((datos) => { if (vigente) setIwa(datos); })
      .catch((err) => { if (vigente) setErrorIwa(err.message); });
    return () => { vigente = false; };
  }, [resumen.conjunto_pruebas_id]);
  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <h1 className="text-2xl font-semibold text-[#141a17]">
            Resultados de la prueba
          </h1>
          <p className="mt-1 text-sm text-[#5d6862]">
            Prueba #{resumen.id} · Repetición {resumen.numero_repeticion} · Humedad promedio{" "}
            <span className="font-medium text-[#0f6b4f]">
              {resumen.promedio_humedad_pct} %
            </span>{" "}
            · {resumen.muestras} muestras · {resumen.ollas} ollas ·{" "}
            {resumen.fases} fases
          </p>
        </div>

        <button
          type="button"
          onClick={onNuevaPrueba}
          className="inline-flex items-center gap-2 rounded-md bg-[#0f6b4f] px-4 py-2.5
                     text-sm font-medium text-white transition hover:bg-[#0b5a42]
                     focus-visible:outline-none focus-visible:ring-2
                     focus-visible:ring-[#0f6b4f] focus-visible:ring-offset-2"
        >
          <span className="material-symbols-outlined text-[18px]" aria-hidden="true">
            arrow_back
          </span>
          Nueva prueba
        </button>
      </div>

      {errorCalculo && (
        <div className="rounded-md border border-[#f0c9c2] bg-[#fdf1ef] p-4 text-sm text-[#b3352c]">
          La prueba se guardó, pero no se pudieron calcular los resultados:{" "}
          {errorCalculo}
        </div>
      )}

      <section className="space-y-3 rounded-xl bg-white p-6">
        <h2 className="text-lg font-semibold">Mediciones IWA · {codigoConjunto(resumen.conjunto_pruebas_id)}</h2>
        {!resumen.es_valida && <p role="status">Esta repetición se guardó como inválida y no participa en el promedio. Motivo: {resumen.motivo_invalidez || "—"}</p>}
        {iwa && <p>Repeticiones válidas: {iwa.pruebas_validas} · Versión de umbrales: {iwa.version_umbrales}</p>}
        {errorIwa && <p role="alert">No se pudo consultar el conjunto: {errorIwa}</p>}
        {!iwa && !errorIwa && <p>Consultando el conjunto…</p>}
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead><tr>{["Métrica", "Esta repetición", "Promedio", "Repeticiones con dato", "Nivel del conjunto"].map(
              (columna) => <th key={columna} className="p-2">{columna}</th>
            )}</tr></thead>
            <tbody>{ENERGIA_IWA.map(([clave, etiqueta]) => {
              const grupo = iwa?.metricas[clave];
              return <tr key={clave} className="border-t border-[#e9f0ec]">
                <th className="p-2 font-normal">{etiqueta}</th>
                <td className="p-2">{resumen.resultado_prueba?.[clave] ?? "—"}</td>
                <td className="p-2">{grupo?.promedio?.toLocaleString("es-GT", {maximumFractionDigits: 8}) ?? "—"}</td>
                <td className="p-2">{grupo?.n ?? "—"}</td>
                <td className="p-2">{grupo?.tier ?? "—"}</td>
              </tr>;
            })}</tbody>
          </table>
        </div>
        <p className="text-xs text-[#5d6862]">NA: menos de tres repeticiones válidas con valor positivo para esa métrica. CO y PM pendientes del módulo de emisiones.</p>
      </section>

      {resultados &&
        FASES.map((fase) => {
          const datos = resultados[fase.tipo];
          if (!datos) return null;

          return (
            <section key={fase.tipo} className="rounded-xl bg-white p-6">
              <div className="flex items-center gap-3 border-b border-[#e9f0ec] pb-4">
                <div
                  className={`rounded-xl p-2 ${
                    fase.tipo === "baja_potencia"
                      ? "bg-[#e9f0ec] text-[#0f6b4f]"
                      : "bg-[#fdf0e3] text-[#c9741f]"
                  }`}
                >
                  <span
                    className="material-symbols-outlined text-[22px]"
                    aria-hidden="true"
                  >
                    {fase.icono}
                  </span>
                </div>
                <div>
                  <h2 className="text-lg font-semibold text-[#141a17]">
                    {fase.titulo}
                  </h2>
                  <p className="text-sm text-[#5d6862]">{fase.descripcion}</p>
                </div>
              </div>

              <dl className="mt-5 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
                {METRICAS.map(([clave, etiqueta, unidad]) => (
                  <div key={clave}>
                    <dt className="text-xs text-[#5d6862]">{etiqueta}</dt>
                    <dd className="text-sm font-medium text-[#141a17]">
                      {numero(datos[clave])}
                      {unidad && (
                        <span className="ml-1 font-normal text-[#5d6862]">
                          {unidad}
                        </span>
                      )}
                    </dd>
                  </div>
                ))}
              </dl>
            </section>
          );
        })}

      {resultados && !FASES.some((fase) => resultados[fase.tipo]) && (
        <p className="rounded-md bg-[#f7faf8] p-4 text-sm text-[#5d6862]">
          El backend no devolvió resultados para las fases de esta prueba.
        </p>
      )}
    </div>
  );
}
