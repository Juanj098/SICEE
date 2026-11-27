import { useState, useEffect } from "react";
import Seccion from "./Seccion";
import { Campo, Selector } from "./Campo";
import Modal from "./Modal";
import FormInvestigador from "./FormInvestigador";
import FormLaboratorio from "./FormLaboratorio";
import FormEstufa from "./FormEstufa";
import { codigoConjunto } from "../conjuntos";
import { 
    listActivos, 
    crearConjuntoPruebas, 
    eliminatInvestigador,
    listLabs,
    listEstufas,
    listConjuntos,
    eliminarLaboratorio,
    eliminarEstufa
} from "../../../api/Catalogos";

export default function DatosPrueba({datos, onChange}){

    
    const manejar = (e) => onChange(e.target.name, e.target.value)

    const [modal, setModal] = useState(null)
    const [investigador, setInvestigador] = useState([])
    const [laboratorios, setLaboratorios] = useState([])
    const [estufas, setEstufas] = useState([])
    const [conjuntos, setConjuntos] = useState([])
    const [descripcion, setDescripcion] = useState('')
    const [creandoConjunto, setCreandoConjunto] = useState(false)
    const [errorConjunto, setErrorConjunto] = useState('')
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

    const alEliminarLaboratorio = async (id) => {
        if (!id) return
        try {
            await eliminarLaboratorio(id)
            setLaboratorios((lista) => lista.filter((l) => String(l.id) !== String(id)))
            if (String(datos.prueba.laboratorio_id) === String(id)) {
                onChange('laboratorio_id', '')
            }
        } catch (error) {
            setError(error.message)
        }
    }

    const elegirConjunto = (id) => {
        onChange('conjunto_pruebas_id', id)
        onChange('numero_repeticion', '')
    }

    const elegirEstufa = (id) => {
        if (id === datos.prueba.estufa_id) return
        onChange('estufa_id', id)
        elegirConjunto('')
    }

    const alCrearEstufa = (nueva) => {
        setEstufas((lista) => [...lista, nueva])
        elegirEstufa(String(nueva.id))
        setModal(null)
    }

    const crearConjunto = async (evento) => {
        evento.preventDefault()
        if (creandoConjunto || !descripcion.trim()) return
        setCreandoConjunto(true)
        setErrorConjunto('')
        try {
            const nuevo = await crearConjuntoPruebas({
                estufa_id: Number(datos.prueba.estufa_id),
                descripcion: descripcion.trim(),
            })
            setConjuntos((lista) => [...lista, nuevo])
            elegirConjunto(String(nuevo.id))
            setModal(null)
        } catch (err) {
            setErrorConjunto(err.message)
        } finally {
            setCreandoConjunto(false)
        }
    }

    const alEliminarEstufa = async (id) => {
        try {
            await eliminarEstufa(id)
            setEstufas((lista) => lista.filter((e) => e.id !== id))
            if (String(id) === datos.prueba.estufa_id) elegirEstufa('')
        } catch (error) {
            setError(error.message)
        }
    }

    useEffect(()=>{
        listActivos()
        .then((lista)=> setInvestigador(lista.map((i)=>({id: i.id, texto: i.nombre}))))
        .catch((e)=>setError(e.message))
    },[])

    useEffect(()=>{
        listLabs()
        .then((lista)=>setLaboratorios(lista.map((i)=>({id: i.id, texto:i.institucion}))))
        .catch((e)=>setError(e.message))
    },[])

    useEffect(()=>{
        Promise.all([listEstufas(), listConjuntos()])
        .then(([listaEstufas, conjuntos]) => {
            setEstufas(listaEstufas)
            setConjuntos(conjuntos)
        })
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
                    onEliminar={alEliminarLaboratorio}
                />
                <Selector
                    label='Estufa'
                    name='estufa_id'
                    opciones={estufas.map((e) => ({id: e.id, texto: e.marca}))}
                    value={datos.prueba.estufa_id}
                    onChange={(e) => elegirEstufa(e.target.value)}
                    onNuevo={()=>setModal('estufa')}
                    onEliminar={alEliminarEstufa}
                />
                {datos.prueba.estufa_id && <Selector
                    label='Conjunto de pruebas'
                    name='conjunto_pruebas_id'
                    opciones={conjuntos.filter((c) => String(c.estufa_id) === datos.prueba.estufa_id)
                        .map((c) => ({ id: c.id, texto: `${codigoConjunto(c.id)} · ${c.descripcion || 'Sin descripción'}` }))}
                    value={datos.prueba.conjunto_pruebas_id}
                    onChange={(e) => elegirConjunto(e.target.value)}
                    textoNuevo="Nuevo conjunto"
                    onNuevo={() => { setDescripcion(''); setErrorConjunto(''); setModal('conjunto') }}
                />}
                <Campo label='Número de repetición' type='number' min='1' name='numero_repeticion'
                    placeholder="Automático al guardar" value={datos.prueba.numero_repeticion} onChange={manejar}/>
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
            <Modal titulo="Nuevo conjunto" abierto={modal === 'conjunto'} onCerrar={() => !creandoConjunto && setModal(null)}>
                <form onSubmit={crearConjunto} className="space-y-4">
                    <Campo label="Descripción del conjunto" placeholder="Ej. Ensayo base" required maxLength={500}
                        value={descripcion} onChange={(e) => setDescripcion(e.target.value)} />
                    <p className="text-sm text-[#5d6862]">El código se asigna al crear el conjunto.</p>
                    {errorConjunto && <p role="alert">{errorConjunto}</p>}
                    <div className="flex justify-end gap-3">
                        <button type="button" disabled={creandoConjunto} onClick={() => setModal(null)}>Cancelar</button>
                        <button type="submit" disabled={creandoConjunto || !descripcion.trim()}
                            className="rounded-md bg-[#0f6b4f] px-4 py-2 text-white disabled:opacity-60">
                            {creandoConjunto ? "Creando…" : "Crear conjunto"}
                        </button>
                    </div>
                </form>
            </Modal>
        </Seccion>
    )
}
