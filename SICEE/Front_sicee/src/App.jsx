import { useState } from "react";

// Datos de ejemplo. Luego se reemplazan por un fetch a tu API de Flask.
const PRUEBAS_INICIALES = [
  { id: 1, fecha: "2026-10-14", estufa: "Estufa A", combustible: "Pino", eficiencia: 31.2, co: 42, co2: 3.1 },
  { id: 2, fecha: "2026-10-15", estufa: "Estufa A", combustible: "Encino", eficiencia: 35.8, co: 36, co2: 3.4 },
  { id: 3, fecha: "2026-10-17", estufa: "Estufa B", combustible: "Pino", eficiencia: 27.5, co: 55, co2: 2.8 },
];

const FORM_VACIO = { fecha: "", estufa: "", combustible: "", eficiencia: "", co: "", co2: "" };

/*
  Sistema visual (un solo acento, una sola tipografía, sin líneas ni sombras):
  - suelo:   #e9f0ec   (fondo de la página)
  - panel:   #ffffff   (superficies; se separan del suelo por tono)
  - campo:   #e9f0ec   (inputs; mismo tono que el suelo)
  - tinta:   #141a17   (texto principal)
  - apagado: #6b7570   (texto secundario)
  - acento:  #0f6b4f   (botón, cifra de eficiencia, foco)
*/

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

function Cifra({ titulo, valor, unidad, tono }) {
  return (
    <div className={`rounded-2xl p-6 sm:p-7 ${tono}`}>
      <p className="text-sm opacity-80">{titulo}</p>
      <p className="mt-10 text-5xl font-semibold leading-none tracking-tight tabular-nums sm:text-6xl">
        {valor}
        {unidad && (
          <span className="ml-1.5 text-xl font-normal tracking-normal opacity-70">{unidad}</span>
        )}
      </p>
    </div>
  );
}

function Campo({ label, ...props }) {
  return (
    <label className="block">
      <span className="mb-1.5 block text-sm text-[#6b7570]">{label}</span>
      <input
        {...props}
        required
        className="w-full rounded-md bg-[#e9f0ec] px-3 py-2.5 text-sm text-[#141a17]
                   placeholder:text-[#a3aaa6] outline-none transition
                   focus:bg-white focus:ring-2 focus:ring-[#0f6b4f]"
      />
    </label>
  );
}

export default function App() {
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
  };

  const promedio = (campo) =>
    pruebas.length
      ? (pruebas.reduce((acc, p) => acc + p[campo], 0) / pruebas.length).toFixed(1)
      : "0";

  return (
    <div className="min-h-screen bg-[#e9f0ec] font-sans text-[#141a17] antialiased">
      {/* Encabezado */}
      <header>
        <div className="mx-auto flex max-w-6xl items-baseline justify-between px-6 pb-2 pt-8">
          <div className="flex items-baseline gap-4">
            <h1 className="text-lg font-semibold tracking-tight text-[#0f6b4f]">SICEE</h1>
            <p className="hidden text-sm text-[#6b7570] sm:block">
              Sistema de Caracterización Energética y Emisiones
            </p>
          </div>
          <span className="text-sm text-[#6b7570]">CII · USAC</span>
        </div>
      </header>

      <main className="mx-auto max-w-6xl px-6 pb-16 pt-12">
        {/* Resumen: cifras grandes sobre el suelo, sin tarjetas */}
        <section aria-label="Resumen" className="grid gap-4 sm:grid-cols-3">
          <Cifra tono="bg-[#0f6b4f] text-white" titulo="Pruebas registradas" valor={pruebas.length} />
          <Cifra tono="bg-[#bfe5d0] text-[#0a3d2d]" titulo="Eficiencia térmica promedio" valor={promedio("eficiencia")} unidad="%" />
          <Cifra tono="bg-[#cfe3f2] text-[#12384f]" titulo="CO promedio" valor={promedio("co")} unidad="ppm" />
        </section>

        <div className="mt-16 grid gap-6 lg:grid-cols-12">
          {/* Formulario */}
          <section className="rounded-xl bg-white p-7 lg:col-span-4 lg:self-start">
            <h2 className="text-base font-semibold">Nueva prueba</h2>
            <form onSubmit={handleSubmit} className="mt-6 space-y-4">
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
          </section>

          {/* Historial */}
          <section className="rounded-xl bg-white p-7 lg:col-span-8">
            <h2 className="text-base font-semibold">Historial de pruebas</h2>

            {pruebas.length === 0 ? (
              <p className="py-16 text-center text-sm text-[#6b7570]">
                Aún no hay pruebas. Registra la primera con el formulario.
              </p>
            ) : (
              <div className="-mx-2 mt-4 overflow-x-auto">
                <table className="w-full min-w-[620px] text-left text-sm">
                  <thead>
                    <tr className="text-[#6b7570]">
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
            )}
          </section>
        </div>
      </main>
    </div>
  );
}