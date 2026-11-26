import { useState, useEffect } from "react";
import Seccion from "./Seccion";
import { Campo, Selector } from "./Campo";
import Modal from "./Modal";
import FormInvestigador from "./FormInvestigador";
import FormLaboratorio from "./FormLaboratorio";
import FormEstufa from "./FormEstufa";
import { listActivos, crearConjuntoPruebas, eliminatInvestigador } from "../../../api/Catalogos";

const LABORATORIOS = [{ id: 1, texto: "CII - Centro de Investigación e Innovación" }];
const ESTUFAS = [{ id: 1, texto: "Rocket A1" }];

export default function DatosPrueba({datos, onChange}){

    
    const manejar = (e) => onChange(e.target.name, e.target.value)

    const [modal, setModal] = useState(null)
    const [investigador, setInvestigador] = useState([])
    const [laboratorios, setLaboratorios] = useState(LABORATORIOS)
    const [estufas, setEstufas] = useState(ESTUFAS)
    const [error, setError] = useState('')

    const alCrearInvestigador = (nuevo) => {
        setInvestigador((lista) => [...lista, {id: nuevo.id, texto: nuevo.nombre}])
        onChange('investigador_id', String(nuevo.id))
        setModal(null)
    }

    const alEliminarInvestigador = async (id) => {
        if (!id) return
        try {
            await eliminatInvestigador(id)
            setInvestigador((lista) => lista.filter((i) => String(i.id) !== String(id)))
            if (String(datos.prueba.investigador_id) === String(id)) {
                onChange('investigador_id', '')
            }
        } catch (error) {
            setError(error.message)
        }
    }

    const alCrearLaboratorio = (nuevo) => {
        setLaboratorios((lista) => [...lista, {id: nuevo.id, texto: nuevo.institucion}])
        onChange('laboratorio_id', String(nuevo.id))
        setModal(null)
    }

    const alCrearEstufa = async (nueva) => {
        const conjunto = await crearConjuntoPruebas({
            estufa_id: nueva.id,
            descripcion: `Conjunto de pruebas ${nueva.marca}`,
        })
        setEstufas((lista) => [...lista, {id: conjunto.id, texto: nueva.marca}])
        onChange('conjunto_pruebas_id', String(conjunto.id))
        setModal(null)
    }

    useEffect(()=>{
        listActivos()
        .then((lista)=> setInvestigador(lista.map((i)=>({id: i.id, texto: i.nombre})))
        )
        .catch((e)=>setError(e.message))
    },[])

    return(
        <Seccion
            titulo='Datos de la prueba'
            descripcion='Informacion general de la prueba WBT'
        >
            <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
                <Campo label='Fecha' type='date' name='fecha' value = {datos.prueba.fecha} onChange={manejar}/>
                <Selector
                    label='Investigador'
                    name='investigador_id'
                    opciones={investigador}
                    value={datos.prueba.investigador_id}
                    onChange={manejar}
                    onNuevo={()=>setModal('investigador')}
                    onEliminar={alEliminarInvestigador}
                />
                <Selector
                    label='Laboratorio'
                    name='laboratorio_id'
                    opciones={laboratorios}
                    value={datos.prueba.laboratorio_id}
                    onChange={manejar}
                    onNuevo={()=>setModal('laboratorio')}
                />
                <Selector
                    label='Estufa'
                    name='conjunto_pruebas_id'
                    opciones={estufas}
                    value={datos.prueba.conjunto_pruebas_id}
                    onChange={manejar}
                    onNuevo={()=>setModal('estufa')}
                />
                <Campo label='Número Repeticion' type='number' name='numero_repeticion' value = {datos.prueba.numero_repeticion} onChange={manejar}/>
                <Campo label='Peso del recipiente del carbón (kg)' type='number' min='0' step='0.0001' name='peso_recipiente_carbon_kg' value={datos.prueba.peso_recipiente_carbon_kg} onChange={manejar}/>
            </div>

            {error && <p className="mt-2 text-sm text-[#c94f4f]">{error}</p>}

            <Modal titulo='Nuevo Investigador' abierto={modal==='investigador'} onCerrar={() => setModal(null)}>
                <FormInvestigador onGuardado={alCrearInvestigador} onCancelar={()=>setModal(null)}/>
            </Modal>

            <Modal titulo='Nuevo Laboratorio' abierto={modal==='laboratorio'} onCerrar={() => setModal(null)}>
                <FormLaboratorio onGuardado={alCrearLaboratorio} onCancelar={()=>setModal(null)}/>
            </Modal>

            <Modal titulo='Nueva Estufa' abierto={modal==='estufa'} onCerrar={() => setModal(null)}>
                <FormEstufa onGuardado={alCrearEstufa} onCancelar={()=>setModal(null)}/>
            </Modal>
        </Seccion>
    )
}
