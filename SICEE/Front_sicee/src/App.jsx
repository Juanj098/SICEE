import { useState } from "react";

// Datos de ejemplo. Luego se reemplazan por un fetch a tu API de Flask.
const PRUEBAS_INICIALES = [
  { id: 1, fecha: "2026-10-14", estufa: "Estufa A", combustible: "Pino", eficiencia: 31.2, co: 42, co2: 3.1 },
  { id: 2, fecha: "2026-10-15", estufa: "Estufa A", combustible: "Encino", eficiencia: 35.8, co: 36, co2: 3.4 },
  { id: 3, fecha: "2026-10-17", estufa: "Estufa B", combustible: "Pino", eficiencia: 27.5, co: 55, co2: 2.8 },
];

const FORM_VACIO = {
  fecha: "",
  estufa: "",
  combustible: "",
  eficiencia: "",
  co: "",
  co2: "",
};

function Tarjeta({ titulo, valor, unidad }) {
  return (
    <div className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
      <p className="text-sm text-slate-500">{titulo}</p>
      <p className="mt-1 text-3xl font-semibold text-slate-900">
        {valor}
        <span className="ml-1 text-base font-normal text-slate-400">{unidad}</span>
      </p>
    </div>
  );
}

function Campo({ label, ...props }) {
  return (
    <label className="block">
      <span className="mb-1 block text-sm font-medium text-slate-700">{label}</span>
      <input
        {...props}
        required
        className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm
                   focus:border-emerald-500 focus:outline-none focus:ring-2 focus:ring-emerald-200"
      />
    </label>
  );
}

export default function App() {
  const [pruebas, setPruebas] = useState(PRUEBAS_INICIALES);
  const [form, setForm] = useState(FORM_VACIO);

  const handleChange = (e) =>
    setForm({ ...form, [e.target.name]: e.target.value });

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
  };

  const promedio = (campo) =>
    pruebas.length
      ? (pruebas.reduce((acc, p) => acc + p[campo], 0) / pruebas.length).toFixed(1)
      : "0";

  return (
    <div className="min-h-screen bg-slate-50 text-slate-800">
      {/* Encabezado */}
      <header className="border-b border-slate-200 bg-white">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
          <div>
            <h1 className="text-xl font-bold text-emerald-700">SICEE</h1>
            <p className="text-xs text-slate-500">
              Sistema de Caracterización Energética y Emisiones
            </p>
          </div>
          <span className="rounded-full bg-emerald-100 px-3 py-1 text-xs font-medium text-emerald-700">
            CII · USAC
          </span>
        </div>
      </header>

      <main className="mx-auto max-w-6xl space-y-8 px-6 py-8">
        {/* Resumen */}
        <section className="grid gap-4 sm:grid-cols-3">
          <Tarjeta titulo="Pruebas registradas" valor={pruebas.length} />
          <Tarjeta titulo="Eficiencia térmica promedio" valor={promedio("eficiencia")} unidad="%" />
          <Tarjeta titulo="CO promedio" valor={promedio("co")} unidad="ppm" />
        </section>

        <div className="grid gap-8 lg:grid-cols-3">
          {/* Formulario */}
          <section className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm lg:col-span-1">
            <h2 className="mb-4 text-lg font-semibold">Nueva prueba</h2>
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
                className="w-full rounded-lg bg-emerald-600 px-4 py-2 text-sm font-medium text-white
                           transition hover:bg-emerald-700 active:scale-[0.98]"
              >
                Guardar prueba
              </button>
            </form>
          </section>

          {/* Tabla */}
          <section className="overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm lg:col-span-2">
            <h2 className="border-b border-slate-200 px-6 py-4 text-lg font-semibold">
              Historial de pruebas
            </h2>
            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm">
                <thead className="bg-slate-50 text-xs uppercase text-slate-500">
                  <tr>
                    {["Fecha", "Estufa", "Combustible", "Eficiencia", "CO", "CO₂"].map((h) => (
                      <th key={h} className="px-6 py-3 font-medium">{h}</th>
                    ))}
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {pruebas.map((p) => (
                    <tr key={p.id} className="hover:bg-slate-50">
                      <td className="px-6 py-3">{p.fecha}</td>
                      <td className="px-6 py-3">{p.estufa}</td>
                      <td className="px-6 py-3">{p.combustible}</td>
                      <td className="px-6 py-3 font-medium text-emerald-700">{p.eficiencia}%</td>
                      <td className="px-6 py-3">{p.co} ppm</td>
                      <td className="px-6 py-3">{p.co2}%</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>
        </div>
      </main>
    </div>
  );
}