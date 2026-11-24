import DatosPrueba from "./components/DatosPrueba";
import MedicionesGenerales from "./components/MedicionesGenerales";
import FasesPrueba from "./components/FasesPrueba";
import { FASES } from "./fases";
import { useState } from "react";

const MAX_OLLAS = 4;

const FORM_INICIAL = {
    prueba: {
        fecha: '',
        numero_repeticion: '',
        investigador_id: '',
        laboratorio_id: '',
        conjunto_pruebas_id: '',
        condiciones_ambientales_id: '',
        combustible_id: '',
        peso_recipiente_carbon_kg: ''
    },
    condiciones: {
        temperatura_c: '',
        humedad_relativa_pct: '',
        altitud_m: '',
        presion_atmosferica_kpa: '',
        viento_ms: '',
        condicion_viento: '',
        punto_ebullicion_c: ''
    },
    combustible: {
        tipo: '',
        tipo_alimentacion: '',
        longitud_combustible_cm: '',
        ancho_combustible_cm: '',
        poder_calorifico_neto_mj_kg: '',
        poder_calorifico_bruto_mj_kg: '',
        poder_calorifico_carbon_mj_kg: '',
        contenido_carbono_pct: '',
        contenido_carbono_carbon_pct: '',
        descripcion: ''
    },
    // Ollas de la prueba: peso seco y capacidad se usan en todas las fases.
    ollas: [1, 2].map((numero) => ({
        numero_olla: numero,
        peso_seco_kg: '',
        capacidad_l: ''
    })),
    // Humedad medida en cada prueba: 3 leños × 3 mediciones.
    muestras: Array.from({ length: 9 }, (_, i) => ({
        numero_lenio: Math.floor(i / 3) + 1,
        numero_medicion: (i % 3) + 1,
        humedad_pct: ''
    })),
    // Datos por fase; `ollas` se llena al capturar el agua de cada olla.
    fases: FASES.map((fase) => ({
        tipo_fase: fase.tipo,
        t_inicial: '',
        t_final: '',
        peso_combustible_inicial_kg: '',
        peso_combustible_final_kg: '',
        peso_carbon_con_recipiente_kg: '',
        peso_cenizas_kg: '',
        observaciones: '',
        ollas: []
    }))
}

export default function PruebaWBT(){

    const [form, setForm] = useState(FORM_INICIAL)

    const actualizar = (seccion, campo, valor) =>
        setForm((f)=>({...f, [seccion]:{...f[seccion], [campo]:valor}}))

    const cambiarPrueba = (campo, valor) => actualizar('prueba', campo, valor)

    const cambiarMuestra = (indice, valor) =>
        setForm((f) => ({
            ...f,
            muestras: f.muestras.map((m, i) =>
                i === indice ? { ...m, humedad_pct: valor } : m
            )
        }))

    const cambiarOlla = (indice, campo, valor) =>
        setForm((f) => ({
            ...f,
            ollas: f.ollas.map((o, i) =>
                i === indice ? { ...o, [campo]: valor } : o
            )
        }))

    const agregarOlla = () =>
        setForm((f) =>
            f.ollas.length >= MAX_OLLAS
                ? f
                : {
                      ...f,
                      ollas: [
                          ...f.ollas,
                          {
                              numero_olla: f.ollas.length + 1,
                              peso_seco_kg: '',
                              capacidad_l: ''
                          }
                      ]
                  }
        )

    // Se renumeran para que las ollas queden siempre 1..n.
    const quitarOlla = (indice) =>
        setForm((f) =>
            f.ollas.length <= 1
                ? f
                : {
                      ...f,
                      ollas: f.ollas
                          .filter((_, i) => i !== indice)
                          .map((o, i) => ({ ...o, numero_olla: i + 1 }))
                  }
        )

    const [pantalla, setPantalla] = useState('general')

    const cambiarFase = (indice, campo, valor) =>
        setForm((f) => ({
            ...f,
            fases: f.fases.map((fase, i) =>
                i === indice ? { ...fase, [campo]: valor } : fase
            )
        }))

    const cambiarOllaFase = (indiceFase, numeroOlla, campo, valor) =>
        setForm((f) => ({
            ...f,
            fases: f.fases.map((fase, i) => {
                if (i !== indiceFase) return fase
                const existe = fase.ollas.some(
                    (o) => o.numero_olla === numeroOlla
                )
                return {
                    ...fase,
                    ollas: existe
                        ? fase.ollas.map((o) =>
                              o.numero_olla === numeroOlla
                                  ? { ...o, [campo]: valor }
                                  : o
                          )
                        : [
                              ...fase.ollas,
                              { numero_olla: numeroOlla, [campo]: valor }
                          ]
                }
            })
        }))

    if (pantalla === 'fases') {
        return (
            <FasesPrueba
                datos={form}
                onVolver={() => setPantalla('general')}
                onCambiarFase={cambiarFase}
                onCambiarOllaFase={cambiarOllaFase}
            />
        )
    }

    return(
        <div className="space-y-6">
            <DatosPrueba datos={form} onChange={cambiarPrueba}/>
            <MedicionesGenerales
                datos={form}
                onCambiarCondiciones={(campo, valor) => actualizar('condiciones', campo, valor)}
                onCambiarPrueba={cambiarPrueba}
                onCambiarMuestra={cambiarMuestra}
                onCambiarOlla={cambiarOlla}
                onAgregarOlla={agregarOlla}
                onQuitarOlla={quitarOlla}
            />

            <div className="flex justify-end">
                <button
                    type="button"
                    onClick={() => setPantalla('fases')}
                    className="inline-flex items-center gap-2 rounded-md bg-[#0f6b4f] px-6 py-3
                               text-base font-medium text-white transition hover:bg-[#0b5a42]
                               focus-visible:outline-none focus-visible:ring-2
                               focus-visible:ring-[#0f6b4f] focus-visible:ring-offset-2"
                >
                    <span className="material-symbols-outlined" aria-hidden="true">
                        save
                    </span>
                    Guardar datos
                </button>
            </div>
        </div>
    )
}
