import { useState } from "react";
import { Campo } from "./Campo";
import { FASES } from "../fases";

const valor = (dato) =>
  dato === "" || dato === null || dato === undefined ? "—" : dato;

function Stepper({ paso, onIr }) {
  return (
    <div className="flex items-center px-1 py-5 sm:px-5">
      {FASES.map((fase, indice) => {
        const completo = indice < paso;
        const activo = indice === paso;

        return (
          <div
            key={fase.tipo}
            className={`flex items-center ${indice === FASES.length - 1 ? "" : "flex-1"}`}
          >
            <button
              type="button"
              onClick={() => onIr(indice)}
              className="flex flex-col items-center gap-2"
            >
              <span
                className={`flex h-10 w-10 items-center justify-center rounded-full text-sm font-semibold transition
                  ${
                    completo || activo
                      ? "bg-[#0f6b4f] text-white"
                      : "bg-[#e9f0ec] text-[#5d6862]"
                  }
                  ${activo ? "ring-4 ring-[#d8e8e0]" : ""}`}
              >
                {completo ? (
                  <span
                    className="material-symbols-outlined text-[18px]"
                    aria-hidden="true"
                  >
                    check
                  </span>
                ) : (
                  indice + 1
                )}
              </span>
              <span
                className={`whitespace-nowrap text-sm ${
                  activo
                    ? "font-semibold text-[#0f6b4f]"
                    : "text-[#5d6862]"
                }`}
              >
                {fase.titulo}
              </span>
            </button>

            {indice !== FASES.length - 1 && (
              <span
                className={`mx-2 h-[2px] flex-1 sm:mx-4 ${
                  completo ? "bg-[#0f6b4f]" : "bg-[#e9f0ec]"
                }`}
              />
            )}
          </div>
        );
      })}
    </div>
  );
}

export default function FasesPrueba({
  datos,
  onVolver,
  onCambiarFase,
  onCambiarOllaFase,
}) {
  const [paso, setPaso] = useState(0);

  const fase = datos.fases?.[paso] ?? {};
  const info = FASES[paso];
  const ollas = datos.ollas ?? [];

  // Sólo para mostrar: el promedio oficial lo calcula el backend.
  const valoresHumedad = (datos.muestras ?? [])
    .map((m) => m.humedad_pct)
    .filter((v) => v !== "" && v !== null && v !== undefined)
    .map(Number)
    .filter((v) => Number.isFinite(v) && v >= 0 && v <= 100);

  const promedioHumedad = valoresHumedad.length
    ? (
        valoresHumedad.reduce((a, b) => a + b, 0) / valoresHumedad.length
      ).toFixed(2)
    : "—";

  return (
    <div className="space-y-6">
      <div>
        <button
          type="button"
          onClick={onVolver}
          className="mb-3 inline-flex items-center gap-1.5 text-sm text-[#5d6862]
                     transition hover:text-[#0f6b4f]"
        >
          <span className="material-symbols-outlined text-[18px]" aria-hidden="true">
            arrow_back
          </span>
          Volver a datos generales
        </button>

        <div className="flex flex-wrap items-center gap-3">
          <h1 className="text-2xl font-semibold text-[#141a17]">
            Datos de las fases
          </h1>
          <span className="rounded-full bg-[#e9f0ec] px-3 py-1 text-xs font-medium text-[#0f6b4f]">
            En proceso
          </span>
        </div>

        <p className="mt-1 text-sm text-[#5d6862]">
          Registra los datos de cada fase de la prueba.
        </p>

        <div className="mt-4 flex flex-wrap gap-x-10 gap-y-3 rounded-xl bg-white px-5 py-4 text-sm">
          <div>
            <span className="text-[#5d6862]">Fecha</span>
            <p className="font-medium text-[#141a17]">
              {valor(datos.prueba?.fecha)}
            </p>
          </div>
          <div>
            <span className="text-[#5d6862]">Repetición</span>
            <p className="font-medium text-[#141a17]">
              {valor(datos.prueba?.numero_repeticion)}
            </p>
          </div>
          <div>
            <span className="text-[#5d6862]">Recipiente del carbón</span>
            <p className="font-medium text-[#141a17]">
              {datos.prueba?.peso_recipiente_carbon_kg
                ? `${datos.prueba.peso_recipiente_carbon_kg} kg`
                : "—"}
            </p>
          </div>
        </div>
      </div>

      <div className="rounded-xl bg-white">
        <Stepper paso={paso} onIr={setPaso} />
      </div>

      <div className="grid gap-6 lg:grid-cols-[1fr_320px]">
        <div className="rounded-xl bg-white p-6">
          <div className="flex items-start gap-3 border-b border-[#e9f0ec] pb-4">
            <div
              className={`rounded-xl p-2 ${
                info.tipo === "baja_potencia"
                  ? "bg-[#e9f0ec] text-[#0f6b4f]"
                  : "bg-[#fdf0e3] text-[#c9741f]"
              }`}
            >
              <span className="material-symbols-outlined text-[22px]" aria-hidden="true">
                {info.icono}
              </span>
            </div>

            <div>
              <h2 className="text-lg font-semibold text-[#141a17]">
                {info.titulo}
              </h2>
              <p className="text-sm text-[#5d6862]">{info.descripcion}</p>
            </div>
          </div>

          <div className="mt-5 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            <Campo
              label="Hora de inicio"
              name="t_inicial"
              type="time"
              value={fase.t_inicial}
              onChange={(e) => onCambiarFase(paso, "t_inicial", e.target.value)}
            />
            <Campo
              label="Hora de finalización"
              name="t_final"
              type="time"
              value={fase.t_final}
              onChange={(e) => onCambiarFase(paso, "t_final", e.target.value)}
            />
            <Campo
              label="Peso del combustible inicial (kg)"
              name="peso_combustible_inicial_kg"
              type="number"
              min="0"
              step="0.0001"
              value={fase.peso_combustible_inicial_kg}
              onChange={(e) =>
                onCambiarFase(paso, "peso_combustible_inicial_kg", e.target.value)
              }
            />
            <Campo
              label="Peso del combustible final (kg)"
              name="peso_combustible_final_kg"
              type="number"
              min="0"
              step="0.0001"
              value={fase.peso_combustible_final_kg}
              onChange={(e) =>
                onCambiarFase(paso, "peso_combustible_final_kg", e.target.value)
              }
            />
            <Campo
              label="Carbón con recipiente (kg)"
              name="peso_carbon_con_recipiente_kg"
              type="number"
              min="0"
              step="0.0001"
              value={fase.peso_carbon_con_recipiente_kg}
              onChange={(e) =>
                onCambiarFase(paso, "peso_carbon_con_recipiente_kg", e.target.value)
              }
            />
            <Campo
              label="Cenizas (kg)"
              name="peso_cenizas_kg"
              type="number"
              min="0"
              step="0.0001"
              value={fase.peso_cenizas_kg}
              onChange={(e) =>
                onCambiarFase(paso, "peso_cenizas_kg", e.target.value)
              }
            />
          </div>

          <div className="mt-4">
            <label className="block">
              <span className="mb-1.5 block text-sm text-[#5d6862]">
                Observaciones
              </span>
              <textarea
                name="observaciones"
                rows="3"
                value={fase.observaciones}
                onChange={(e) =>
                  onCambiarFase(paso, "observaciones", e.target.value)
                }
                className="w-full rounded-md bg-[#e9f0ec] px-3 py-2.5 text-sm text-[#141a17]
                           outline-none transition focus:bg-white focus:ring-2 focus:ring-[#0f6b4f]"
              />
            </label>
          </div>

          <div className="mt-6">
            <h3 className="text-sm font-semibold text-[#141a17]">
              Agua por olla
            </h3>
            <p className="mt-1 text-xs text-[#5d6862]">
              Temperaturas y pesos de cada olla en esta fase.
            </p>

            <div className="mt-3 space-y-4">
              {ollas.map((olla) => {
                const datosOlla =
                  fase.ollas?.find(
                    (o) => o.numero_olla === olla.numero_olla
                  ) ?? {};

                return (
                  <div
                    key={olla.numero_olla}
                    className="rounded-md border border-[#e9f0ec] p-4"
                  >
                    <div className="mb-3 flex flex-wrap items-baseline justify-between gap-2">
                      <p className="text-sm font-medium text-[#0f6b4f]">
                        Olla {olla.numero_olla}
                      </p>
                      <span className="text-xs text-[#5d6862]">
                        {olla.peso_seco_kg
                          ? `${olla.peso_seco_kg} kg en vacío`
                          : "Sin peso seco registrado"}
                      </span>
                    </div>

                    <div className="grid gap-4 sm:grid-cols-2">
                      <Campo
                        label="Temperatura inicial del agua (°C)"
                        name={`t_inicial_olla_${olla.numero_olla}`}
                        type="number"
                        step="0.01"
                        value={datosOlla.temperatura_inicial_agua_c}
                        onChange={(e) =>
                          onCambiarOllaFase(
                            paso,
                            olla.numero_olla,
                            "temperatura_inicial_agua_c",
                            e.target.value
                          )
                        }
                      />
                      <Campo
                        label="Temperatura final del agua (°C)"
                        name={`t_final_olla_${olla.numero_olla}`}
                        type="number"
                        step="0.01"
                        value={datosOlla.temperatura_final_agua_c}
                        onChange={(e) =>
                          onCambiarOllaFase(
                            paso,
                            olla.numero_olla,
                            "temperatura_final_agua_c",
                            e.target.value
                          )
                        }
                      />
                      <Campo
                        label="Peso con agua inicial (kg)"
                        name={`peso_inicial_olla_${olla.numero_olla}`}
                        type="number"
                        min="0"
                        step="0.0001"
                        value={datosOlla.peso_con_agua_inicial_kg}
                        onChange={(e) =>
                          onCambiarOllaFase(
                            paso,
                            olla.numero_olla,
                            "peso_con_agua_inicial_kg",
                            e.target.value
                          )
                        }
                      />
                      <Campo
                        label="Peso con agua final (kg)"
                        name={`peso_final_olla_${olla.numero_olla}`}
                        type="number"
                        min="0"
                        step="0.0001"
                        value={datosOlla.peso_con_agua_final_kg}
                        onChange={(e) =>
                          onCambiarOllaFase(
                            paso,
                            olla.numero_olla,
                            "peso_con_agua_final_kg",
                            e.target.value
                          )
                        }
                      />
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          <div className="mt-6 flex flex-wrap items-center justify-between gap-3 border-t border-[#e9f0ec] pt-5">
            <button
              type="button"
              onClick={() => (paso > 0 ? setPaso(paso - 1) : onVolver())}
              className="inline-flex items-center gap-2 rounded-md border border-[#d8e0dc]
                         px-4 py-2.5 text-sm font-medium text-[#5d6862] transition
                         hover:bg-[#f7faf8] focus-visible:outline-none focus-visible:ring-2
                         focus-visible:ring-[#0f6b4f] focus-visible:ring-offset-2"
            >
              <span className="material-symbols-outlined text-[18px]" aria-hidden="true">
                arrow_back
              </span>
              Anterior
            </button>

            <div className="flex flex-wrap gap-3">
              <button
                type="button"
                className="inline-flex items-center gap-2 rounded-md border border-[#cfe0d8]
                           px-4 py-2.5 text-sm font-medium text-[#0f6b4f] transition
                           hover:bg-[#f1f7f4] focus-visible:outline-none focus-visible:ring-2
                           focus-visible:ring-[#0f6b4f] focus-visible:ring-offset-2"
              >
                <span className="material-symbols-outlined text-[18px]" aria-hidden="true">
                  save
                </span>
                Guardar borrador
              </button>

              <button
                type="button"
                onClick={() =>
                  paso < FASES.length - 1 && setPaso(paso + 1)
                }
                className="inline-flex items-center gap-2 rounded-md bg-[#0f6b4f] px-4 py-2.5
                           text-sm font-medium text-white transition hover:bg-[#0b5a42]
                           focus-visible:outline-none focus-visible:ring-2
                           focus-visible:ring-[#0f6b4f] focus-visible:ring-offset-2"
              >
                {paso === FASES.length - 1 ? "Finalizar" : "Siguiente"}
                <span className="material-symbols-outlined text-[18px]" aria-hidden="true">
                  {paso === FASES.length - 1 ? "check" : "arrow_forward"}
                </span>
              </button>
            </div>
          </div>
        </div>

        <aside className="h-fit rounded-xl bg-white p-5">
          <div className="flex items-center gap-2">
            <span className="material-symbols-outlined text-[20px] text-[#0f6b4f]" aria-hidden="true">
              description
            </span>
            <h2 className="font-semibold text-[#141a17]">Resumen de la prueba</h2>
          </div>

          <div className="mt-5">
            <p className="text-xs font-semibold uppercase tracking-wide text-[#5d6862]">
              Fases
            </p>
            <ul className="mt-2 space-y-2">
              {FASES.map((f, indice) => (
                <li key={f.tipo} className="flex items-center gap-2 text-sm">
                  <span
                    className={`h-2.5 w-2.5 rounded-full ${
                      indice < paso
                        ? "bg-[#0f6b4f]"
                        : indice === paso
                          ? "bg-[#c9741f]"
                          : "bg-[#d8e0dc]"
                    }`}
                  />
                  <span
                    className={
                      indice === paso
                        ? "font-medium text-[#141a17]"
                        : "text-[#5d6862]"
                    }
                  >
                    {f.titulo}
                  </span>
                </li>
              ))}
            </ul>
          </div>

          <hr className="my-4 border-[#e9f0ec]" />

          <div>
            <p className="text-xs font-semibold uppercase tracking-wide text-[#5d6862]">
              Humedad promedio
            </p>
            <p className="mt-1 text-2xl font-semibold text-[#141a17]">
              {promedioHumedad} %
            </p>
            <p className="text-xs text-[#5d6862]">
              {valoresHumedad.length} de {datos.muestras?.length || 9} muestras
            </p>
          </div>

          <div className="mt-4 rounded-md bg-[#f7faf8] p-3 text-xs text-[#5d6862]">
            Los datos se guardan por fase. Puedes volver a modificarlos antes de
            cerrar la prueba.
          </div>
        </aside>
      </div>
    </div>
  );
}
