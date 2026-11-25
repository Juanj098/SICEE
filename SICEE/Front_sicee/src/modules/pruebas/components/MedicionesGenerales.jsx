import { useEffect, useState } from "react";
import Seccion from "./Seccion";
import Subseccion from "./Subseccion";
import { Campo, Selector } from "./Campo";
import Modal from "./Modal";
import FormCombustible from "./FormCombustible";
import FichaCombustible from "./FichaCombustible";
import { listarCombustibles } from "../../../api/Catalogos";

export default function MedicionesGenerales({
  datos,
  onCambiarCondiciones,
  onCambiarPrueba,
  onCambiarMuestra,
  onCambiarOlla,
  onAgregarOlla,
  onQuitarOlla,
}) {
  const { condiciones = {}, prueba = {}, muestras = [], ollas = [] } = datos;

  // Promedio sólo para mostrar: el cálculo oficial lo hace el backend al
  // guardar las 9 mediciones de muestra_humedad.
  const valoresHumedad = muestras
    .map((m) => m.humedad_pct)
    .filter((v) => v !== "" && v !== null && v !== undefined)
    .map(Number)
    .filter((v) => Number.isFinite(v) && v >= 0 && v <= 100);

  const promedioHumedad = valoresHumedad.length
    ? (valoresHumedad.reduce((a, b) => a + b, 0) / valoresHumedad.length).toFixed(2)
    : "—";

  const [combustibles, setCombustibles] = useState([]);
  const [modal, setModal] = useState(false);
  const [errorLista, setErrorLista] = useState("");

  useEffect(() => {
    let activo = true;
    listarCombustibles()
      .then((lista) => {
        if (!activo) return;
        // Se guardan los datos completos: el selector usa `texto` y la ficha
        // muestra el resto de campos de la especie elegida.
        setCombustibles(lista.map((c) => ({ ...c, texto: c.tipo })));
        setErrorLista("");
      })
      .catch((err) => {
        if (activo) setErrorLista(err.message);
      });
    return () => {
      activo = false;
    };
  }, []);

  const seleccionado = combustibles.find(
    (c) => String(c.id) === String(prueba.combustible_id)
  );

  const manejarCondiciones = (e) =>
    onCambiarCondiciones(e.target.name, e.target.value);

  const manejarPrueba = (e) => onCambiarPrueba(e.target.name, e.target.value);

  const alCrearCombustible = (nuevo) => {
    setCombustibles((lista) => [...lista, { ...nuevo, texto: nuevo.tipo }]);
    onCambiarPrueba("combustible_id", String(nuevo.id));
    setModal(false);
  };

  return (
    <Seccion
      titulo="Mediciones generales"
      descripcion="Condiciones ambientales y combustible de la prueba"
    >
      <Subseccion titulo="Condiciones ambientales">
        <Campo
          label="Temperatura (°C)"
          name="temperatura_c"
          type="number"
          step="0.01"
          value={condiciones.temperatura_c}
          onChange={manejarCondiciones}
        />
        <Campo
          label="Humedad relativa (%)"
          name="humedad_relativa_pct"
          type="number"
          min="0"
          max="100"
          step="0.01"
          value={condiciones.humedad_relativa_pct}
          onChange={manejarCondiciones}
        />
        <Campo
          label="Altitud (m)"
          name="altitud_m"
          type="number"
          min="0"
          step="0.01"
          value={condiciones.altitud_m}
          onChange={manejarCondiciones}
        />
        <Campo
          label="Presión atmosférica (kPa)"
          name="presion_atmosferica_kpa"
          type="number"
          min="0"
          step="0.001"
          value={condiciones.presion_atmosferica_kpa}
          onChange={manejarCondiciones}
        />
        <Campo
          label="Viento (m/s)"
          name="viento_ms"
          type="number"
          min="0"
          step="0.01"
          value={condiciones.viento_ms}
          onChange={manejarCondiciones}
        />
        <Campo
          label="Condición del viento"
          name="condicion_viento"
          placeholder="Ej. Viento leve"
          value={condiciones.condicion_viento}
          onChange={manejarCondiciones}
        />
        <Campo
          label="Punto de ebullición (°C)"
          name="punto_ebullicion_c"
          type="number"
          step="0.01"
          value={condiciones.punto_ebullicion_c}
          onChange={manejarCondiciones}
        />
      </Subseccion>

      <div className="mt-6 border-t border-[#e9f0ec] pt-5">
        <Subseccion titulo="Combustible">
          <Selector
            label="Combustible"
            name="combustible_id"
            opciones={combustibles}
            value={prueba.combustible_id}
            onChange={manejarPrueba}
            onNuevo={() => setModal(true)}
          />
        </Subseccion>
        <FichaCombustible combustible={seleccionado} />
        {errorLista && <p className="mt-2 text-sm text-[#c94f4f]">{errorLista}</p>}

        <div className="mt-5">
          <h4 className="text-sm font-semibold text-[#141a17]">
            Humedad del combustible
          </h4>
          <p className="mt-1 text-xs text-[#5d6862]">
            3 leños × 3 mediciones. Se mide en cada prueba y su promedio entra
            en el cálculo.
          </p>

          <div className="mt-3 grid gap-4 sm:grid-cols-3">
            {[1, 2, 3].map((lenio) => (
              <div key={lenio}>
                <p className="mb-2 text-sm text-[#5d6862]">Leño {lenio}</p>
                <div className="space-y-2">
                  {[1, 2, 3].map((medicion) => {
                    const indice = (lenio - 1) * 3 + (medicion - 1);
                    return (
                      <Campo
                        key={medicion}
                        label={`Medición ${medicion}`}
                        name={`humedad_${lenio}_${medicion}`}
                        type="number"
                        min="0"
                        max="100"
                        step="0.01"
                        value={muestras[indice]?.humedad_pct ?? ""}
                        onChange={(e) => onCambiarMuestra(indice, e.target.value)}
                      />
                    );
                  })}
                </div>
              </div>
            ))}
          </div>

          <p className="mt-3 text-sm text-[#5d6862]">
            Promedio:{" "}
            <span className="font-medium text-[#0f6b4f]">{promedioHumedad} %</span>
            {" · "}
            {valoresHumedad.length} de {muestras.length || 9} mediciones
          </p>
        </div>
      </div>

      <div className="mt-6 border-t border-[#e9f0ec] pt-5">
        <div className="flex flex-wrap items-start justify-between gap-3">
          <div>
            <h4 className="text-sm font-semibold text-[#141a17]">Ollas</h4>
            <p className="mt-1 text-xs text-[#5d6862]">
              Peso de la olla vacía y capacidad. Se usan en todas las fases para
              calcular el agua.
            </p>
          </div>
          <button
            type="button"
            onClick={onAgregarOlla}
            disabled={ollas.length >= 4}
            title={ollas.length >= 4 ? "Máximo 4 ollas" : undefined}
            className="shrink-0 rounded-md bg-[#0f6b4f] px-3 py-1.5 text-sm font-medium text-white
                       transition hover:bg-[#0b5a42] focus-visible:outline-none focus-visible:ring-2
                       focus-visible:ring-[#0f6b4f] focus-visible:ring-offset-2
                       disabled:cursor-not-allowed disabled:opacity-50"
          >
            + Agregar olla
          </button>
        </div>

        <div className="mt-3 grid gap-4 sm:grid-cols-2">
          {ollas.map((olla, indice) => (
            <div
              key={olla.numero_olla}
              className="rounded-md border border-[#e9f0ec] p-4"
            >
              <div className="mb-3 flex items-center justify-between gap-2">
                <p className="text-sm font-medium text-[#0f6b4f]">
                  Olla {olla.numero_olla}
                </p>
                {ollas.length > 1 && (
                  <button
                    type="button"
                    onClick={() => onQuitarOlla(indice)}
                    title={`Quitar olla ${olla.numero_olla}`}
                    aria-label={`Quitar olla ${olla.numero_olla}`}
                    className="rounded p-1 text-[#c94f4f] transition hover:bg-[#fdf1ef]
                               focus-visible:outline-none focus-visible:ring-2
                               focus-visible:ring-[#c94f4f] focus-visible:ring-offset-2"
                  >
                    <span
                      className="material-symbols-outlined text-[18px]"
                      aria-hidden="true"
                    >
                      delete
                    </span>
                  </button>
                )}
              </div>
              <div className="grid gap-4 sm:grid-cols-2">
                <Campo
                  label="Peso seco (kg)"
                  name={`peso_seco_${olla.numero_olla}`}
                  type="number"
                  min="0"
                  step="0.0001"
                  value={olla.peso_seco_kg}
                  onChange={(e) =>
                    onCambiarOlla(indice, "peso_seco_kg", e.target.value)
                  }
                />
                <Campo
                  label="Capacidad (L)"
                  name={`capacidad_${olla.numero_olla}`}
                  type="number"
                  min="0"
                  step="0.01"
                  value={olla.capacidad_l}
                  onChange={(e) =>
                    onCambiarOlla(indice, "capacidad_l", e.target.value)
                  }
                />
              </div>
            </div>
          ))}
        </div>
      </div>

      <Modal
        titulo="Nuevo Combustible"
        abierto={modal}
        onCerrar={() => setModal(false)}
      >
        <FormCombustible
          onGuardado={alCrearCombustible}
          onCancelar={() => setModal(false)}
        />
      </Modal>
    </Seccion>
  );
}
