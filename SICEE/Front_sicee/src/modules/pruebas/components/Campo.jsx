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

export function Selector({ label, opciones, onNuevo, ...props }) {
  return (
    <div>
      <label htmlFor={props.name} className="mb-1.5 block text-sm text-[#5d6862]">
        {label}
      </label>
      <div className="flex gap-2">
        <select id={props.name} {...props} className={`min-w-0 flex-1 ${ESTILO}`}>
          <option value="">Seleccionar…</option>
          {opciones.map((o) => (
            <option key={o.id} value={o.id}>{o.texto}</option>
          ))}
        </select>
        {onNuevo && (
          <button
            type="button"
            onClick={onNuevo}
            className="shrink-0 rounded-md bg-[#0f6b4f] px-3 text-sm font-medium text-white transition
                       hover:bg-[#0b5a42] focus-visible:outline-none focus-visible:ring-2
                       focus-visible:ring-[#0f6b4f] focus-visible:ring-offset-2"
          >
            + Nuevo
          </button>
        )}
      </div>
    </div>
  );
}