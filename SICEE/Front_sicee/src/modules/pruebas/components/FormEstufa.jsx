import { useState } from "react";
import { Campo } from "./Campo";
import { crearEstufa } from "../../../api/Catalogos";

const VALORES_INICIALES = {
  marca: "",
  fabricante: "",
  area_camara_cm2: "",
  altura_cm: "",
  numero_hornillas: "",
  material: "",
  descripcion: "",
};

// El backend guarda 0.00 cuando el número no se envía; se manda null en ese caso.
const numero = (valor) => (valor === "" ? null : Number(valor));

export default function FormEstufa({ onGuardado, onCancelar }) {
  const [valores, setValores] = useState(VALORES_INICIALES);
  const [error, setError] = useState("");
  const [guardando, setGuardando] = useState(false);

  const cambiar = (e) =>
    setValores((v) => ({ ...v, [e.target.name]: e.target.value }));

  const enviar = async (e) => {
    e.preventDefault();
    setGuardando(true);
    setError("");
    try {
      const nueva = await crearEstufa({
        marca: valores.marca,
        fabricante: valores.fabricante,
        area_camara_cm2: numero(valores.area_camara_cm2),
        altura_cm: numero(valores.altura_cm),
        numero_hornillas: numero(valores.numero_hornillas),
        material: valores.material,
        descripcion: valores.descripcion,
      });
      await onGuardado(nueva);
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
          label="Marca"
          name="marca"
          required
          value={valores.marca}
          onChange={cambiar}
        />
        <Campo
          label="Fabricante"
          name="fabricante"
          required
          value={valores.fabricante}
          onChange={cambiar}
        />
        <Campo
          label="Área de cámara (cm²)"
          name="area_camara_cm2"
          type="number"
          min="0"
          step="0.01"
          value={valores.area_camara_cm2}
          onChange={cambiar}
        />
        <Campo
          label="Altura (cm)"
          name="altura_cm"
          type="number"
          min="0"
          step="0.01"
          value={valores.altura_cm}
          onChange={cambiar}
        />
        <Campo
          label="Número de hornillas"
          name="numero_hornillas"
          type="number"
          min="1"
          step="1"
          value={valores.numero_hornillas}
          onChange={cambiar}
        />
        <Campo
          label="Material"
          name="material"
          value={valores.material}
          onChange={cambiar}
        />
      </div>
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
          className="inline-flex items-center gap-2 rounded-md bg-[#0f6b4f] px-4 py-2 text-sm font-medium text-white
                     hover:bg-[#0b5a42] disabled:opacity-60"
        >
          {!guardando && (
            <span className="material-symbols-outlined" aria-hidden="true">cooking</span>
          )}
          {guardando ? "Guardando…" : "Guardar"}
        </button>
      </div>
    </form>
  );
}
