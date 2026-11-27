import { useEffect, useRef, useState } from "react";

const ESTILO =
  "w-full rounded-md bg-[#e9f0ec] px-3 py-2.5 text-sm text-[#141a17] outline-none transition " +
  "focus:bg-white focus:ring-2 focus:ring-[#0f6b4f]";

export function Campo({ label, ...props }) {
  return (
    <label className="block">
      <span className="mb-1.5 block text-sm text-[#5d6862]">{label}</span>
      <input {...props} className={ESTILO} />
    </label>
  );
}

export function Selector({ label, opciones, onNuevo, textoNuevo = "+ Nuevo", onEliminar, ...props }) {
  const [abierto, setAbierto] = useState(false);
  const contenedor = useRef(null);

  useEffect(() => {
    if (!abierto) return undefined;

    const alSenalarFuera = (evento) => {
      if (contenedor.current && !contenedor.current.contains(evento.target)) {
        setAbierto(false);
      }
    };
    const alTeclear = (evento) => {
      if (evento.key === "Escape") setAbierto(false);
    };

    document.addEventListener("pointerdown", alSenalarFuera);
    document.addEventListener("keydown", alTeclear);
    return () => {
      document.removeEventListener("pointerdown", alSenalarFuera);
      document.removeEventListener("keydown", alTeclear);
    };
  }, [abierto]);

  const elegido = opciones.find((o) => String(o.id) === String(props.value));

  const elegir = (id) => {
    props.onChange({ target: { name: props.name, value: String(id) } });
    setAbierto(false);
  };

  // Los <option> nativos no admiten el icono de borrar por opción, así que el
  // desplegable se dibuja a mano. Se usa en todos los selectores para que
  // todos tengan el mismo aspecto.
  return (
    <div>
      <label htmlFor={props.name} className="mb-1.5 block text-sm text-[#5d6862]">
        {label}
      </label>

      <div className="flex gap-2">
        <div ref={contenedor} className="relative min-w-0 flex-1">
          <button
            type="button"
            id={props.name}
            aria-haspopup="listbox"
            aria-expanded={abierto}
            onClick={() => setAbierto((previo) => !previo)}
            className={`flex items-center justify-between gap-2 text-left ${ESTILO}`}
          >
            <span className={`truncate ${elegido ? "" : "text-[#5d6862]"}`}>
              {elegido ? elegido.texto : "Seleccionar…"}
            </span>
            <span
              className={`material-symbols-outlined shrink-0 text-[18px] text-[#5d6862] transition-transform
                ${abierto ? "-rotate-90" : "rotate-90"}`}
              aria-hidden="true"
            >
              arrow_forward
            </span>
          </button>

          {abierto && (
            <ul
              role="listbox"
              aria-label={label}
              className="absolute left-0 right-0 top-full z-20 mt-1 max-h-64 overflow-auto
                         rounded-md border border-[#d8e0dc] bg-white py-1 shadow-lg"
            >
              {opciones.length === 0 && (
                <li className="px-3 py-2 text-sm text-[#5d6862]">
                  Sin registros
                </li>
              )}

              {opciones.map((o) => {
                const activo = String(o.id) === String(props.value);

                return (
                  <li
                    key={o.id}
                    className={`flex items-center gap-1 pr-1 ${
                      activo ? "bg-[#f1f7f4]" : ""
                    }`}
                  >
                    <button
                      type="button"
                      role="option"
                      aria-selected={activo}
                      onClick={() => elegir(o.id)}
                      className={`min-w-0 flex-1 truncate px-3 py-2 text-left text-sm
                        transition hover:bg-[#f1f7f4] focus-visible:outline-none
                        focus-visible:ring-2 focus-visible:ring-[#0f6b4f]
                        ${
                          activo
                            ? "font-medium text-[#0f6b4f]"
                            : "text-[#141a17]"
                        }`}
                    >
                      {o.texto}
                    </button>

                    {onEliminar && (
                      <button
                        type="button"
                        onClick={() => onEliminar(o.id)}
                        title={`Eliminar ${o.texto}`}
                        aria-label={`Eliminar ${o.texto}`}
                        className="shrink-0 rounded p-1.5 text-[#b3352c] transition
                                   hover:bg-[#fdf1ef] focus-visible:outline-none
                                   focus-visible:ring-2 focus-visible:ring-[#b3352c]"
                      >
                        <span
                          className="material-symbols-outlined text-[18px]"
                          aria-hidden="true"
                        >
                          delete
                        </span>
                      </button>
                    )}
                  </li>
                );
              })}
            </ul>
          )}
        </div>

        {onNuevo && (
          <button
            type="button"
            onClick={onNuevo}
            className="shrink-0 rounded-md bg-[#0f6b4f] px-3 text-sm font-medium text-white transition
                       hover:bg-[#0b5a42] focus-visible:outline-none focus-visible:ring-2
                       focus-visible:ring-[#0f6b4f] focus-visible:ring-offset-2"
          >
            {textoNuevo}
          </button>
        )}
      </div>
    </div>
  );
}
