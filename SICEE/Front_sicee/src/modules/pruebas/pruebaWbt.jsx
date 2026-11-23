import MedicionesFase from "./components/MedicionesFase";
import DatosPrueba from "./components/DatosPrueba";
import MedicionesGenerales from "./components/MedicionesGenerales";
import { useState } from "react";

const FORM_INICIAL = {
    prueba: {
        fecha: '',
        numero_repeticion: '',
        investigador_id: '',
        laboratorio_id: '',
        conjunto_pruebas_id: ''
    },
}

export default function PruebaWBT(){

    const [form, setForm] = useState(FORM_INICIAL)
    const cambiarPrueba = (campo, valor) => setForm((f)=>({...f,prueba:{...f.prueba, [campo]:valor}}))

    return(
        <div className="space-y-6">
            <DatosPrueba datos={form} onChange={cambiarPrueba}/>
            <MedicionesGenerales/>
            <MedicionesFase/>
        </div>
    )
}