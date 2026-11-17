// Sidebar de SICEE. No depende de React Router: recibe qué vista está activa
// y avisa con onNavegar(id). Si luego usas rutas, cambia cada <button> por <NavLink>.

const Icono = ({ d }) => (
  <svg
    viewBox="0 0 24 24"
    className="h-[18px] w-[18px] shrink-0"
    fill="none"
    stroke="currentColor"
    strokeWidth="1.7"
    strokeLinecap="round"
    strokeLinejoin="round"
    aria-hidden="true"
  >
    <path d={d} />
  </svg>
);

const ICONOS = {
  resumen: "M4 4h6v6H4zM14 4h6v6h-6zM4 14h6v6H4zM14 14h6v6h-6z",
  wbt: "M9 3h6M10 3v6l-5 9a2 2 0 0 0 1.8 3h10.4a2 2 0 0 0 1.8-3l-5-9V3",
  historial: "M12 7v5l3 2M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0z",
  estufas: "M12 3c1 3 5 5 5 10a5 5 0 0 1-10 0c0-2 1-3 2-4 0 2 1 3 2 3 0-3-1-5 1-9z",
  combustibles: "M4 7l8-4 8 4-8 4zM4 12l8 4 8-4M4 17l8 4 8-4",
  laboratorios: "M4 21V8l8-5 8 5v13M9 21v-6h6v6",
};

// Para agregar una opción: añade un item aquí y su vista en App.jsx.
export const GRUPOS = [
  {
    items: [
      { id: "resumen", etiqueta: "Resumen" },
      { id: "wbt", etiqueta: "Prueba WBT" },
      { id: "historial", etiqueta: "Historial" },
    ],
  },
  {
    titulo: "Catálogos",
    items: [
      { id: "estufas", etiqueta: "Estufas" },
      { id: "combustibles", etiqueta: "Combustibles" },
      { id: "laboratorios", etiqueta: "Laboratorios" },
    ],
  },
];

export default function Sidebar({ activa, onNavegar, abierta = false, onCerrar }) {
  const ir = (id) => {
    onNavegar(id);
    onCerrar?.();
  };

  return (
    <>
      {/* Fondo oscuro solo en móvil, cuando el menú está abierto */}
      {abierta && (
        <div
          className="fixed inset-0 z-30 bg-black/40 lg:hidden"
          onClick={onCerrar}
          aria-hidden="true"
        />
      )}

      <aside
        aria-label="Navegación principal"
        className={`fixed inset-y-0 left-0 z-40 flex w-64 flex-col bg-[#0a3d2d] text-white
                    transition-transform duration-200 ease-out lg:translate-x-0
                    ${abierta ? "translate-x-0" : "-translate-x-full"}`}
      >
        <div className="px-6 pb-8 pt-8">
          <p className="text-xl font-semibold tracking-tight">SICEE</p>
          <p className="mt-1 text-sm text-white/65">Centro de Investigación · USAC</p>
        </div>

        <nav className="flex-1 space-y-6 overflow-y-auto px-3 pb-6">
          {GRUPOS.map((grupo, i) => (
            <div key={grupo.titulo ?? i}>
              {grupo.titulo && (
                <p className="px-3 pb-2 text-sm text-white/55">{grupo.titulo}</p>
              )}
              <ul className="space-y-0.5">
                {grupo.items.map((item) => {
                  const activo = item.id === activa;
                  return (
                    <li key={item.id}>
                      <button
                        type="button"
                        onClick={() => ir(item.id)}
                        aria-current={activo ? "page" : undefined}
                        className={`flex w-full items-center gap-3 rounded-md px-3 py-2.5 text-left text-[15px]
                                    transition-colors focus-visible:outline-none focus-visible:ring-2
                                    focus-visible:ring-white/70
                                    ${activo
                                      ? "bg-white/[0.14] font-medium text-white"
                                      : "text-white/80 hover:bg-white/[0.07] hover:text-white"}`}
                      >
                        <Icono d={ICONOS[item.id]} />
                        {item.etiqueta}
                      </button>
                    </li>
                  );
                })}
              </ul>
            </div>
          ))}
        </nav>

        <div className="px-6 py-5 text-sm text-white/55">Protocolo WBT 4.2.3</div>
      </aside>
    </>
  );
}