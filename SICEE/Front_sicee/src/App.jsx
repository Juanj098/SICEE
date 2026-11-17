import { useState } from "react";
import Sidebar, { GRUPOS } from "./layouts/sidebar";

// Datos de ejemplo. Luego se reemplazan por un fetch a tu API de Flask.
const PRUEBAS_INICIALES = [
  { id: 1, fecha: "2026-10-14", estufa: "Estufa A", combustible: "Pino", eficiencia: 31.2, co: 42, co2: 3.1 },
  { id: 2, fecha: "2026-10-15", estufa: "Estufa A", combustible: "Encino", eficiencia: 35.8, co: 36, co2: 3.4 },
  { id: 3, fecha: "2026-10-17", estufa: "Estufa B", combustible: "Pino", eficiencia: 27.5, co: 55, co2: 2.8 },
];

const FORM_VACIO = { fecha: "", estufa: "", combustible: "", eficiencia: "", co: "", co2: "" };

// Un color por combustible. Los que no estén en la lista usan un gris neutro.
const COLORES_COMBUSTIBLE = {
  pino: "#2f9e6e",
  encino: "#d9822b",
  ocote: "#c94f4f",
  eucalipto: "#3b82a6",
  bambú: "#8a6bc4",
  bambu: "#8a6bc4",
};
const colorCombustible = (nombre) =>
  COLORES_COMBUSTIBLE[nombre.trim().toLowerCase()] || "#9aa5a0";

const TITULOS = {
  resumen: "Resumen",
  wbt: "Nueva prueba WBT",
  historial: "Historial de pruebas",
  estufas: "Estufas",
  combustibles: "Combustibles",
  laboratorios: "Laboratorios",
};

function Cifra({ titulo, valor, unidad, tono }) {
  return (
    <div className={`rounded-xl p-6 ${tono}`}>
      <p className="text-sm opacity-80">{titulo}</p>
      <p className="mt-8 text-4xl font-semibold leading-none tracking-tight tabular-nums sm:text-5xl">
        {valor}
        {unidad && (
          <span className="ml-1.5 text-lg font-normal tracking-normal opacity-70">{unidad}</span>
        )}
      </p>
    </div>
  );
}

function Campo({ label, ...props }) {
  return (
    <label className="block">
      <span className="mb-1.5 block text-sm text-[#5d6862]">{label}</span>
      <input
        {...props}
        required
        className="w-full rounded-md bg-[#e9f0ec] px-3 py-2.5 text-sm text-[#141a17]
                   placeholder:text-[#8b948f] outline-none transition
                   focus:bg-white focus:ring-2 focus:ring-[#0f6b4f]"
      />
    </label>
  );
}

function TablaPruebas({ pruebas }) {
  if (pruebas.length === 0) {
    return (
      <p className="py-16 text-center text-sm text-[#5d6862]">
        Aún no hay pruebas. Registra la primera en «Prueba WBT».
      </p>
    );
  }
  return (
    <div className="-mx-2 overflow-x-auto">
      <table className="w-full min-w-[620px] text-left text-sm">
        <thead>
          <tr className="text-[#5d6862]">
            {["Fecha", "Estufa", "Combustible", "Eficiencia", "CO", "CO₂"].map((h) => (
              <th key={h} className="px-2 py-3 font-normal">{h}</th>
            ))}
          </tr>
        </thead>
        <tbody className="tabular-nums">
          {pruebas.map((p) => (
            <tr key={p.id} className="transition hover:bg-[#e9f0ec]">
              <td className="rounded-l-md px-2 py-3.5">{p.fecha}</td>
              <td className="px-2 py-3.5">{p.estufa}</td>
              <td className="px-2 py-3.5">
                <span className="inline-flex items-center gap-2">
                  <span
                    className="h-2 w-2 rounded-full"
                    style={{ backgroundColor: colorCombustible(p.combustible) }}
                  />
                  {p.combustible}
                </span>
              </td>
              <td className="px-2 py-3.5">
                <div className="flex items-center gap-3">
                  <span className="w-12 font-medium text-[#0f6b4f]">{p.eficiencia}%</span>
                  <span className="hidden h-1 w-20 rounded-full bg-[#e6e9e7] sm:block">
                    <span
                      className="block h-1 rounded-full bg-[#0f6b4f]"
                      style={{ width: `${Math.min(p.eficiencia, 100)}%` }}
                    />
                  </span>
                </div>
              </td>
              <td className="px-2 py-3.5">{p.co} ppm</td>
              <td className="rounded-r-md px-2 py-3.5">{p.co2}%</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function Panel({ titulo, accion, children, className = "" }) {
  return (
    <section className={`rounded-xl bg-white p-6 sm:p-7 ${className}`}>
      <div className="flex items-baseline justify-between gap-4">
        <h2 className="text-base font-semibold">{titulo}</h2>
        {accion}
      </div>
      <div className="mt-4">{children}</div>
    </section>
  );
}

export default function App() {
  const [vista, setVista] = useState("resumen");
  const [menuAbierto, setMenuAbierto] = useState(false);
  const [pruebas, setPruebas] = useState(PRUEBAS_INICIALES);
  const [form, setForm] = useState(FORM_VACIO);

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = (e) => {
    e.preventDefault();
    const nueva = {
      id: Date.now(),
      ...form,
      eficiencia: parseFloat(form.eficiencia),
      co: parseFloat(form.co),
      co2: parseFloat(form.co2),
    };
    setPruebas([nueva, ...pruebas]);
    setForm(FORM_VACIO);
    setVista("historial"); // al guardar, lleva al historial para ver la prueba nueva
  };

  const promedio = (campo) =>
    pruebas.length
      ? (pruebas.reduce((acc, p) => acc + p[campo], 0) / pruebas.length).toFixed(1)
      : "0";

  const esCatalogo = GRUPOS.some(
    (g) => g.titulo === "Catálogos" && g.items.some((i) => i.id === vista)
  );

  return (
    <div className="min-h-screen bg-[#e9f0ec] font-sans text-[#141a17] antialiased">
      <Sidebar
        activa={vista}
        onNavegar={setVista}
        abierta={menuAbierto}
        onCerrar={() => setMenuAbierto(false)}
      />

      {/* Barra superior: solo en móvil, para abrir el menú */}
      <div className="sticky top-0 z-20 flex items-center gap-3 bg-[#0a3d2d] px-4 py-3 text-white lg:hidden">
        <button
          type="button"
          onClick={() => setMenuAbierto(true)}
          aria-label="Abrir menú"
          className="rounded-md p-1.5 hover:bg-white/10 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-white/70"
        >
          <svg viewBox="0 0 24 24" className="h-6 w-6" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" aria-hidden="true">
            <path d="M4 7h16M4 12h16M4 17h16" />
          </svg>
        </button>
        <span className="text-base font-semibold tracking-tight">SICEE</span>
      </div>

      <main className="px-5 pb-16 pt-8 sm:px-8 lg:pl-72 lg:pr-10 lg:pt-10">
        <div className="mx-auto max-w-6xl">
          <h1 className="text-2xl font-semibold tracking-tight sm:text-3xl">{TITULOS[vista]}</h1>

          {vista === "resumen" && (
            <div className="mt-8 space-y-6">
              <div className="grid gap-4 sm:grid-cols-3">
                <Cifra tono="bg-[#0f6b4f] text-white" titulo="Pruebas registradas" valor={pruebas.length} />
                <Cifra tono="bg-[#bfe5d0] text-[#0a3d2d]" titulo="Eficiencia térmica promedio" valor={promedio("eficiencia")} unidad="%" />
                <Cifra tono="bg-[#cfe3f2] text-[#12384f]" titulo="CO promedio" valor={promedio("co")} unidad="ppm" />
              </div>
              <Panel
                titulo="Últimas pruebas"
                accion={
                  <button
                    type="button"
                    onClick={() => setVista("historial")}
                    className="text-sm font-medium text-[#0f6b4f] hover:underline focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#0f6b4f]"
                  >
                    Ver historial completo
                  </button>
                }
              >
                <TablaPruebas pruebas={pruebas.slice(0, 3)} />
              </Panel>
            </div>
          )}

          {vista === "wbt" && (
            <Panel titulo="Datos de la prueba" className="mt-8 max-w-xl">
              <form onSubmit={handleSubmit} className="space-y-4">
                <Campo label="Fecha" type="date" name="fecha" value={form.fecha} onChange={handleChange} />
                <Campo label="Estufa" name="estufa" value={form.estufa} onChange={handleChange} placeholder="Estufa A" />
                <Campo label="Combustible" name="combustible" value={form.combustible} onChange={handleChange} placeholder="Pino" />
                <Campo label="Eficiencia (%)" type="number" step="0.1" name="eficiencia" value={form.eficiencia} onChange={handleChange} />
                <div className="grid grid-cols-2 gap-3">
                  <Campo label="CO (ppm)" type="number" step="0.1" name="co" value={form.co} onChange={handleChange} />
                  <Campo label="CO₂ (%)" type="number" step="0.1" name="co2" value={form.co2} onChange={handleChange} />
                </div>
                <button
                  type="submit"
                  className="mt-2 w-full rounded-md bg-[#0f6b4f] px-4 py-2.5 text-sm font-medium text-white
                             transition hover:bg-[#0b5a42] active:scale-[0.99]
                             focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#0f6b4f] focus-visible:ring-offset-2"
                >
                  Guardar prueba
                </button>
              </form>
            </Panel>
          )}

          {vista === "historial" && (
            <Panel titulo={`${pruebas.length} pruebas registradas`} className="mt-8">
              <TablaPruebas pruebas={pruebas} />
            </Panel>
          )}

          {esCatalogo && (
            <Panel titulo="Sección en construcción" className="mt-8 max-w-xl">
              <p className="text-sm text-[#5d6862]">
                Aquí se administrará el catálogo de {TITULOS[vista].toLowerCase()}.
              </p>
            </Panel>
          )}
        </div>
      </main>
    </div>
  );
}