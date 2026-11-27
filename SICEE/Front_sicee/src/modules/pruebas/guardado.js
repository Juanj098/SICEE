import { FASES } from "./fases";

const CAMPOS_OLLA_FASE = [
  "temperatura_inicial_agua_c",
  "temperatura_final_agua_c",
  "peso_con_agua_inicial_kg",
  "peso_con_agua_final_kg",
];

const vacio = (valor) =>
  valor === "" || valor === null || valor === undefined;

const numero = (valor) => (vacio(valor) ? null : Number(valor));

const texto = (valor) => (vacio(valor) ? null : String(valor).trim());

const tituloFase = (tipo) =>
  FASES.find((fase) => fase.tipo === tipo)?.titulo ?? tipo;

// Un inicio caliente parcialmente capturado sí debe validarse.
function faseRegistrada({ tipo_fase, ollas, ...campos }) {
  return tipo_fase !== "inicio_caliente" ||
    Object.values(campos).some((v) => !vacio(v)) ||
    ollas.some((olla) => CAMPOS_OLLA_FASE.some((campo) => !vacio(olla[campo])));
}

// Combina la fecha de la prueba (YYYY-MM-DD) con la hora de la fase (HH:MM).
const horaISO = (fecha, hora) => {
  if (vacio(hora)) return null;
  const completa = String(hora).length === 5 ? `${hora}:00` : String(hora);
  return `${fecha}T${completa}`;
};

export function errorMedicionFase(fase, { prueba, condiciones }) {
  if (!faseRegistrada(fase)) return null;
  const { t_inicial, t_final } = fase;
  if (!t_inicial || !t_final) return "Completa las horas de inicio y finalización.";
  if (t_final <= t_inicial) return "La hora de finalización debe ser posterior al inicio.";
  const inicial = numero(fase.peso_combustible_inicial_kg);
  const final = numero(fase.peso_combustible_final_kg);
  if (inicial === null || final === null) return "Completa los pesos inicial y final del combustible.";
  if (!Number.isFinite(inicial) || !Number.isFinite(final)) return "Los pesos del combustible deben ser números válidos.";
  if (inicial < 0 || final < 0 || final > inicial) {
    return "Los pesos del combustible no pueden ser negativos ni el peso final superar al inicial.";
  }
  const carbon = numero(fase.peso_carbon_con_recipiente_kg);
  const tara = numero(prueba.peso_recipiente_carbon_kg);
  if (carbon !== null && tara === null) return "Indica el peso del recipiente vacío en Datos de la prueba.";
  if (carbon !== null && (!Number.isFinite(carbon) || !Number.isFinite(tara) || tara < 0 || carbon < tara)) return "El peso del carbón con recipiente no puede ser menor que la tara; verifica ambos pesos.";
  if (vacio(condiciones.temperatura_c) || vacio(condiciones.punto_ebullicion_c)) {
    return "Completa la temperatura ambiente y el punto de ebullición en Mediciones generales.";
  }
  for (const olla of fase.ollas) {
    if (fase.tipo_fase !== "baja_potencia" && !vacio(olla.temperatura_inicial_agua_c) &&
        Number(olla.temperatura_inicial_agua_c) >= Number(condiciones.punto_ebullicion_c)) {
      return `Olla ${olla.numero_olla}: la temperatura inicial debe ser menor que el punto de ebullición local.`;
    }
  }
  return null;
}

export function validarPrueba(form) {
  const { prueba, muestras, ollas, fases } = form;

  if (prueba.es_valida === false && !texto(prueba.motivo_invalidez)) {
    return "Escribe el motivo para guardar esta repetición como inválida.";
  }
  if (vacio(prueba.fecha)) return "Falta la fecha de la prueba.";
  if (vacio(prueba.investigador_id)) return "Selecciona un investigador.";
  if (vacio(prueba.laboratorio_id)) return "Selecciona un laboratorio.";
  if (vacio(prueba.conjunto_pruebas_id)) return "Selecciona una estufa y su conjunto de pruebas.";
  if (vacio(prueba.combustible_id)) return "Selecciona un combustible.";

  if (!vacio(prueba.numero_repeticion)) {
    const repeticion = Number(prueba.numero_repeticion);
    if (!Number.isInteger(repeticion) || repeticion < 1) {
      return "El número de repetición debe ser un entero mayor o igual a 1.";
    }
  }

  const humedadesValidas = muestras.every((muestra) => {
    if (vacio(muestra.humedad_pct)) return false;
    const valor = Number(muestra.humedad_pct);
    return Number.isFinite(valor) && valor >= 0 && valor <= 100;
  });
  if (!humedadesValidas) {
    return "Completa las 9 mediciones de humedad con valores entre 0 y 100.";
  }

  if (!ollas.length) return "Registra al menos una olla.";
  for (const olla of ollas) {
    if (vacio(olla.peso_seco_kg) || vacio(olla.capacidad_l)) {
      return `Completa el peso seco y la capacidad de la olla ${olla.numero_olla}.`;
    }
  }

  for (const fase of fases.filter(faseRegistrada)) {
    const titulo = tituloFase(fase.tipo_fase);

    if (prueba.es_valida === false) continue;
    const error = errorMedicionFase(fase, form);
    if (error) return `${titulo}: ${error}`;

    const olla1 = fase.ollas.find((olla) => olla.numero_olla === 1);
    if (!olla1 || CAMPOS_OLLA_FASE.some((campo) => vacio(olla1[campo]))) {
      return `Completa los datos de agua de la olla 1 en la fase ${titulo}.`;
    }

    for (const olla of fase.ollas) {
      const ollaBase = ollas.find((item) => Number(item.numero_olla) === Number(olla.numero_olla));
      for (const campo of ["peso_con_agua_inicial_kg", "peso_con_agua_final_kg"]) {
        if (!vacio(olla[campo]) && Number(olla[campo]) < Number(ollaBase?.peso_seco_kg)) {
          return `Olla ${olla.numero_olla}: ${campo.replaceAll("_", " ")} no puede ser menor que el peso seco.`;
        }
      }
      if (Number(olla.peso_con_agua_final_kg) > Number(olla.peso_con_agua_inicial_kg)) {
        return `Olla ${olla.numero_olla}: el peso final con agua no puede superar el inicial.`;
      }
      if (fase.tipo_fase !== "baja_potencia" &&
          Number(olla.temperatura_final_agua_c) < Number(olla.temperatura_inicial_agua_c)) {
        return `Olla ${olla.numero_olla}: en alta potencia la temperatura final debe ser mayor o igual a la inicial.`;
      }
      if (olla.numero_olla === 1) continue;
      const llenos = CAMPOS_OLLA_FASE.filter(
        (campo) => !vacio(olla[campo])
      ).length;
      if (llenos > 0 && llenos < CAMPOS_OLLA_FASE.length) {
        return `Completa los datos de agua de la olla ${olla.numero_olla} en la fase ${titulo}.`;
      }
    }
  }

  return null;
}

export function construirPayload(form) {
  const { prueba, condiciones, muestras, ollas, fases } = form;
  const numerosOlla = new Set(ollas.map((olla) => Number(olla.numero_olla)));

  return {
    prueba: {
      fecha: prueba.fecha,
      es_valida: prueba.es_valida ?? true,
      motivo_invalidez: prueba.es_valida === false ? texto(prueba.motivo_invalidez) : null,
      investigador_id: Number(prueba.investigador_id),
      laboratorio_id: Number(prueba.laboratorio_id),
      combustible_id: Number(prueba.combustible_id),
      conjunto_pruebas_id: Number(prueba.conjunto_pruebas_id),
      numero_repeticion: vacio(prueba.numero_repeticion)
        ? null
        : Number(prueba.numero_repeticion),
      peso_recipiente_carbon_kg: numero(prueba.peso_recipiente_carbon_kg),
    },
    condiciones: {
      temperatura_c: numero(condiciones.temperatura_c),
      humedad_relativa_pct: numero(condiciones.humedad_relativa_pct),
      altitud_m: numero(condiciones.altitud_m),
      presion_atmosferica_kpa: numero(condiciones.presion_atmosferica_kpa),
      viento_ms: numero(condiciones.viento_ms),
      condicion_viento: texto(condiciones.condicion_viento),
      punto_ebullicion_c: numero(condiciones.punto_ebullicion_c),
    },
    muestras: muestras.map((muestra) => ({
      numero_lenio: Number(muestra.numero_lenio),
      numero_medicion: Number(muestra.numero_medicion),
      humedad_pct: Number(muestra.humedad_pct),
    })),
    ollas: ollas.map((olla) => ({
      numero_olla: Number(olla.numero_olla),
      peso_seco_kg: numero(olla.peso_seco_kg),
      capacidad_l: numero(olla.capacidad_l),
    })),
    fases: fases.filter(faseRegistrada).map((fase) => ({
      tipo_fase: fase.tipo_fase,
      t_inicial: horaISO(prueba.fecha, fase.t_inicial),
      t_final: horaISO(prueba.fecha, fase.t_final),
      peso_combustible_inicial_kg: numero(fase.peso_combustible_inicial_kg),
      peso_combustible_final_kg: numero(fase.peso_combustible_final_kg),
      peso_carbon_con_recipiente_kg: numero(
        fase.peso_carbon_con_recipiente_kg
      ),
      peso_cenizas_kg: numero(fase.peso_cenizas_kg),
      observaciones: texto(fase.observaciones),
      ollas: fase.ollas
        .filter(
          (olla) =>
            numerosOlla.has(Number(olla.numero_olla)) &&
            CAMPOS_OLLA_FASE.some((campo) => !vacio(olla[campo]))
        )
        .map((olla) => ({
          numero_olla: Number(olla.numero_olla),
          ...Object.fromEntries(
            CAMPOS_OLLA_FASE.map((campo) => [campo, numero(olla[campo])])
          ),
        })),
    })),
  };
}
