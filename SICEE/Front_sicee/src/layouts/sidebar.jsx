// Sidebar de SICEE. No depende de React Router: recibe qué vista está activa
// y avisa con onNavegar(id). Para agregar una opción, añade un item a GRUPOS
// (y su ícono en ICONOS) y crea su vista en App.jsx.

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
  wbt: "M9 3h6M10 3v6l-5 9a2 2 0 0 0 1.8 3h10.4a2 2 0 0 0 1.8-3l-5-9V3",
  historial: "M12 7v5l3 2M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0z",
};

export const GRUPOS = [
  {
    items: [
      { id: "wbt", etiqueta: "Prueba WBT" },
      { id: "historial", etiqueta: "Historial" },
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
            <ul key={i} className="space-y-0.5">
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
          ))}
        </nav>

        <div className="px-6 py-5 text-sm text-white/55">Protocolo WBT 4.2.3</div>
      </aside>
    </>
  );
}