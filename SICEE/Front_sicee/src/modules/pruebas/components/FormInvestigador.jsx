import { useState } from "react";
import { Campo } from "./Campo";
import { crearInvestigador } from "../../../api/Catalogos";

export default function FormInvestigador({ onGuardado, onCancelar }) {
  const [nombre, setNombre] = useState("");
  const [error, setError] = useState("");
  const [guardando, setGuardando] = useState(false);

  const enviar = async (e) => {
    e.preventDefault();
    setGuardando(true);
    setError("");
    try {
      const nuevo = await crearInvestigador({ nombre });
      onGuardado(nuevo);
    } catch (err) {
      setError(err.message);
    } finally {
      setGuardando(false);
    }
  };

  return (
    <form onSubmit={enviar} className="space-y-4">
      <Campo label="Nombre del investigador" name="nombre_investigador" required
             value={nombre} onChange={(e) => setNombre(e.target.value)} />
      {error && <p className="text-sm text-[#c94f4f]">{error}</p>}
      <div className="flex justify-end gap-2">
        <button type="button" onClick={onCancelar}
                className="rounded-md px-4 py-2 text-sm text-[#5d6862] hover:bg-[#e9f0ec]">
          Cancelar
        </button>
        <button type="submit" disabled={guardando}
                className="inline-flex items-center gap-2 rounded-md bg-[#0f6b4f] px-4 py-2
                           text-sm font-medium text-white hover:bg-[#0b5a42] disabled:opacity-60">
          {!guardando && (
            <span className="material-symbols-outlined" aria-hidden="true">person</span>
          )}
          {guardando ? "Guardando…" : "Guardar"}
        </button>
      </div>
    </form>
  );
}