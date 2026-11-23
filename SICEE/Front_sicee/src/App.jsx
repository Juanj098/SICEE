import { useState } from "react";
import Sidebar from "./layouts/sidebar";
import PruebaWBT from "./modules/pruebas/pruebaWbt";

// Datos de ejemplo. Luego se reemplazan por un fetch a tu API de Flask.
const PRUEBAS = [
  { id: 1, fecha: "2026-10-14", estufa: "Estufa A", combustible: "Pino", eficiencia: 31.2, co: 42, co2: 3.1 },
  { id: 2, fecha: "2026-10-15", estufa: "Estufa A", combustible: "Encino", eficiencia: 35.8, co: 36, co2: 3.4 },
  { id: 3, fecha: "2026-10-17", estufa: "Estufa B", combustible: "Pino", eficiencia: 27.5, co: 55, co2: 2.8 },
];

const TITULOS = {
  wbt: "Prueba WBT",
  historial: "Historial",
};

function TablaPruebas({ pruebas }) {
  return (
    <div className="overflow-x-auto rounded-xl bg-white p-4 sm:p-6">
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
              <td className="px-2 py-3.5">{p.combustible}</td>
              <td className="px-2 py-3.5 font-medium text-[#0f6b4f]">{p.eficiencia}%</td>
              <td className="px-2 py-3.5">{p.co} ppm</td>
              <td className="rounded-r-md px-2 py-3.5">{p.co2}%</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div> 
  );
}

export default function App() {
  const [vista, setVista] = useState("wbt");
  const [menuAbierto, setMenuAbierto] = useState(false);

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
        <div className="mx-auto max-w-7xl">
          <h1 className="text-2xl font-semibold tracking-tight sm:text-3xl">{TITULOS[vista]}</h1>

          {vista === "wbt" && (
            <div className="mt-8">
              <PruebaWBT/>
            </div>
          )}

          {vista === "historial" && (
            <div className="mt-8">
              <TablaPruebas pruebas={PRUEBAS} />
            </div>
          )}
        </div>
      </main>
    </div>
  );
}