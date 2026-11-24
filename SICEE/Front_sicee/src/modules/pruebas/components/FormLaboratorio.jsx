import { useState } from "react";
import { Campo } from "./Campo";
import { crearLaboratorio } from "../../../api/Catalogos";

const VALORES_INICIALES = {
  institucion: "",
  direccion: "",
  descripcion: "",
};

export default function FormLaboratorio({ onGuardado, onCancelar }) {
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
      const nuevo = await crearLaboratorio({
        institucion: valores.institucion,
        direccion: valores.direccion,
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
      <Campo
        label="Institución"
        name="institucion"
        required
        value={valores.institucion}
        onChange={cambiar}
      />
      <Campo
        label="Dirección"
        name="direccion"
        value={valores.direccion}
        onChange={cambiar}
      />
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
            <span className="material-symbols-outlined" aria-hidden="true">water_voc</span>
          )}
          {guardando ? "Guardando…" : "Guardar"}
        </button>
      </div>
    </form>
  );
}
