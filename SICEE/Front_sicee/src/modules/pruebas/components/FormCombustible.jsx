import { useState } from "react";
import { Campo } from "./Campo";
import { crearCombustible } from "../../../api/Catalogos";

const VALORES_INICIALES = {
  tipo: "",
  tipo_alimentacion: "",
  longitud_combustible_cm: "",
  ancho_combustible_cm: "",
  poder_calorifico_neto_mj_kg: "",
  poder_calorifico_bruto_mj_kg: "",
  poder_calorifico_carbon_mj_kg: "",
  contenido_carbono_pct: "",
  contenido_carbono_carbon_pct: "",
  descripcion: "",
};

// El backend guarda 0.00 cuando el número no se envía; se manda null en ese caso.
const numero = (valor) => (valor === "" ? null : Number(valor));

export default function FormCombustible({ onGuardado, onCancelar }) {
  const [valores, setValores] = useState(VALORES_INICIALES);
  const [error, setError] = useState("");
  const [guardando, setGuardando] = useState(false);

  const cambiar = (e) =>
    setValores((v) => ({ ...v, [e.target.name]: e.target.value }));

  const enviar = async (e) => {
    e.preventDefault();
    setError("");

    const neto = numero(valores.poder_calorifico_neto_mj_kg);
    const bruto = numero(valores.poder_calorifico_bruto_mj_kg);

    if (neto === null && bruto === null) {
      setError("Indica el poder calorífico neto o el bruto");
      return;
    }

    // Misma ecuación (2) del backend, que no puede estimarlo si recibe 0.00.
    const netoFinal = neto ?? Math.max(bruto - 1.32, 0);

    setGuardando(true);
    try {
      const nuevo = await crearCombustible({
        tipo: valores.tipo,
        tipo_alimentacion: valores.tipo_alimentacion,
        longitud_combustible_cm: numero(valores.longitud_combustible_cm),
        ancho_combustible_cm: numero(valores.ancho_combustible_cm),
        poder_calorifico_neto_mj_kg: netoFinal,
        poder_calorifico_bruto_mj_kg: bruto,
        poder_calorifico_carbon_mj_kg: numero(valores.poder_calorifico_carbon_mj_kg),
        contenido_carbono_pct: numero(valores.contenido_carbono_pct),
        contenido_carbono_carbon_pct: numero(valores.contenido_carbono_carbon_pct),
        descripcion: valores.descripcion,
      });
      await onGuardado(nuevo);
    } catch (err) {
      setError(err.message);
    } finally {
      setGuardando(false);
    }
  };

  return (
    <form onSubmit={enviar} className="space-y-4">
      <div className="grid gap-4 sm:grid-cols-2">
        <Campo
          label="Tipo de combustible"
          name="tipo"
          required
          placeholder="Ej. Leña de eucalipto"
          value={valores.tipo}
          onChange={cambiar}
        />
        <Campo
          label="Tipo de alimentación"
          name="tipo_alimentacion"
          placeholder="Ej. Manual"
          value={valores.tipo_alimentacion}
          onChange={cambiar}
        />
        <Campo
          label="Longitud de la leña (cm)"
          name="longitud_combustible_cm"
          type="number"
          min="0"
          step="0.01"
          value={valores.longitud_combustible_cm}
          onChange={cambiar}
        />
        <Campo
          label="Ancho de la leña (cm)"
          name="ancho_combustible_cm"
          type="number"
          min="0"
          step="0.01"
          value={valores.ancho_combustible_cm}
          onChange={cambiar}
        />
        <Campo
          label="Poder calorífico neto (MJ/kg)"
          name="poder_calorifico_neto_mj_kg"
          type="number"
          min="0"
          step="0.001"
          value={valores.poder_calorifico_neto_mj_kg}
          onChange={cambiar}
        />
        <Campo
          label="Poder calorífico bruto (MJ/kg)"
          name="poder_calorifico_bruto_mj_kg"
          type="number"
          min="0"
          step="0.001"
          value={valores.poder_calorifico_bruto_mj_kg}
          onChange={cambiar}
        />
        <Campo
          label="Poder calorífico del carbón (MJ/kg)"
          name="poder_calorifico_carbon_mj_kg"
          type="number"
          min="0"
          step="0.001"
          value={valores.poder_calorifico_carbon_mj_kg}
          onChange={cambiar}
        />
        <Campo
          label="Carbono de la madera (%)"
          name="contenido_carbono_pct"
          type="number"
          min="0"
          max="100"
          step="0.01"
          value={valores.contenido_carbono_pct}
          onChange={cambiar}
        />
        <Campo
          label="Carbono del carbón (%)"
          name="contenido_carbono_carbon_pct"
          type="number"
          min="0"
          max="100"
          step="0.01"
          value={valores.contenido_carbono_carbon_pct}
          onChange={cambiar}
        />
      </div>

      <p className="text-xs text-[#5d6862]">
        Si dejas vacío el poder calorífico neto, se estima como bruto − 1.32 MJ/kg.
      </p>

      <Campo
        label="Descripción"
        name="descripcion"
        value={valores.descripcion}
        onChange={cambiar}
      />

      {error && <p className="text-sm text-[#c94f4f]">{error}</p>}

      <div className="flex justify-end gap-2">
        <button
          type="button"
          onClick={onCancelar}
          className="rounded-md px-4 py-2 text-sm text-[#5d6862] hover:bg-[#e9f0ec]"
        >
          Cancelar
        </button>
        <button
          type="submit"
          disabled={guardando}
          className="inline-flex items-center gap-2 rounded-md bg-[#0f6b4f] px-4 py-2
                     text-sm font-medium text-white hover:bg-[#0b5a42] disabled:opacity-60"
        >
          {!guardando && (
            <span className="material-symbols-outlined" aria-hidden="true">fireplace</span>
          )}
          {guardando ? "Guardando…" : "Guardar"}
        </button>
      </div>
    </form>
  );
}
