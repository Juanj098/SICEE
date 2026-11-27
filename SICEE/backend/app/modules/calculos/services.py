from decimal import Decimal

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy import select, text

from app.extensions import db
from app.modules.pruebas.models import (
    ConjuntoPruebas,
    FasePrueba,
    OllaFase,
    PruebaWBT,
)
from .models import resultado_fase, resultado_prueba
from app.modules.calculos.formulas import calcular_resultado_fase, poder_calorifico_neto_mj_kg


def _num(valor):
    return float(valor) if valor is not None else None


def _fecha(valor):
    return valor.isoformat() if valor is not None else None


def _redondear(resultado, decimales=2):
    return {
        k: round(v, decimales) if isinstance(v, float) else v
        for k, v in resultado.items()
    }


CAMPOS_RESULTADO_FASE = (
    "tiempo_fase_min",
    "masa_agua_inicial_kg",
    "masa_agua_final_kg",
    "masa_agua_evaporada_kg",
    "masa_agua_efectiva_kg",
    "combustible_consumido_kg",
    "tiempo_ebullicion_min",
    "tiempo_ebullicion_corregido_min",
    "energia_util_kj",
    "energia_combustible_kj",
    "eficiencia_termica_pct",
    "consumo_especifico_g_l",
    "velocidad_combustion_g_min",
    "potencia_fase_kw",
    "energia_especifica_corregida_kj_l",
    "combustible_seco_equivalente_kg",
    "cambio_carbon_kg",
    "consumo_especifico_corregido_g_l",
)


def _valores_resultado(resultado):
    """Extrae de un resultado_fase solo las 18 columnas calculadas."""
    return {campo: _num(getattr(resultado, campo)) for campo in CAMPOS_RESULTADO_FASE}


CAMPOS_RESULTADO_PRUEBA = (
    "eficiencia_alta_pct",
    "consumo_especifico_baja_mj_min_l",
    "relacion_reduccion",
    "combustible_ref_5l_g",
    "energia_ref_5l_kj",
    "co_alta_g_mj",
    "pm_alta_mg_mj",
    "co_baja_g_min_l",
    "pm_baja_mg_min_l",
    "co_interior_g_min",
    "pm_interior_mg_min",
    "co_ref_5l_g",
    "pm_ref_5l_g",
)


def _resultado_prueba_a_dict(resultado):
    if resultado is None:
        return None
    return {
        "id": resultado.id,
        "prueba_wbt_id": resultado.prueba_wbt_id,
        **{
            campo: _num(getattr(resultado, campo))
            for campo in CAMPOS_RESULTADO_PRUEBA
        },
    }

# ------------------------------------------------------------
# Serialización de resultados calculados
# ------------------------------------------------------------
def _resultado_a_dict(resultado):
    if resultado is None:
        return None
    return {
        "id": resultado.id,
        "fase_id": resultado.fase_id,
        "tiempo_fase_min": _num(resultado.tiempo_fase_min),
        "masa_agua_inicial_kg": _num(resultado.masa_agua_inicial_kg),
        "masa_agua_final_kg": _num(resultado.masa_agua_final_kg),
        "masa_agua_evaporada_kg": _num(resultado.masa_agua_evaporada_kg),
        "masa_agua_efectiva_kg": _num(resultado.masa_agua_efectiva_kg),
        "combustible_consumido_kg": _num(resultado.combustible_consumido_kg),
        "tiempo_ebullicion_min": _num(resultado.tiempo_ebullicion_min),
        "tiempo_ebullicion_corregido_min": _num(resultado.tiempo_ebullicion_corregido_min),
        "energia_util_kj": _num(resultado.energia_util_kj),
        "energia_combustible_kj": _num(resultado.energia_combustible_kj),
        "eficiencia_termica_pct": _num(resultado.eficiencia_termica_pct),
        "consumo_especifico_g_l": _num(resultado.consumo_especifico_g_l),
        "velocidad_combustion_g_min": _num(resultado.velocidad_combustion_g_min),
        "potencia_fase_kw": _num(resultado.potencia_fase_kw),
        "energia_especifica_corregida_kj_l": _num(resultado.energia_especifica_corregida_kj_l),
        "combustible_seco_equivalente_kg": _num(resultado.combustible_seco_equivalente_kg),
        "cambio_carbon_kg": _num(resultado.cambio_carbon_kg),
        "consumo_especifico_corregido_g_l": _num(resultado.consumo_especifico_corregido_g_l),
    }


# ------------------------------------------------------------
# Serialización de ollas y agua por fase
# ------------------------------------------------------------
def _olla_fase_a_dict(olla_fase):
    olla = olla_fase.olla
    peso_seco = olla.peso_seco_kg if olla is not None else None

    return {
        "olla_id": olla_fase.olla_id,
        "numero_olla": olla.numero_olla if olla is not None else None,
        "capacidad_l": _num(olla.capacidad_l) if olla is not None else None,
        "peso_seco_kg": _num(peso_seco),
        "temperatura_inicial_agua_c": _num(olla_fase.temperatura_inicial_agua_c),
        "temperatura_final_agua_c": _num(olla_fase.temperatura_final_agua_c),
        "peso_con_agua_inicial_kg": _num(olla_fase.peso_con_agua_inicial_kg),
        "peso_con_agua_final_kg": _num(olla_fase.peso_con_agua_final_kg),
    }


# ------------------------------------------------------------
# Serialización de la fase completa
# ------------------------------------------------------------
def _medicion_a_dict(medicion):
    if medicion is None:
        return None
    return {
        "id": medicion.id,
        "fase_id": medicion.fase_id,
        "temperatura_ducto_c": _num(medicion.temperatura_ducto_c),
        "co_ppm": _num(medicion.co_ppm),
        "pm_ug_m3": _num(medicion.pm_ug_m3),
        "co2_ppm": _num(medicion.co2_ppm),
        "co2_fondo_ppm": _num(medicion.co2_fondo_ppm),
        "co_fondo_ppm": _num(medicion.co_fondo_ppm),
        "pm_fondo_ug_m3": _num(medicion.pm_fondo_ug_m3),
        "co2_total_g": _num(medicion.co2_total_g),
        "co_total_g": _num(medicion.co_total_g),
        "pm_total_g": _num(medicion.pm_total_g),
    }


def _fase_a_dict(fase):

    if fase is None:
        return None
    return {
        "tipo_fase": fase.tipo_fase,
        "t_inicial": _fecha(fase.t_inicial),
        "t_final": _fecha(fase.t_final),
        "peso_combustible_inicial_kg": _num(fase.peso_combustible_inicial_kg),
        "peso_combustible_final_kg": _num(fase.peso_combustible_final_kg),
        "peso_carbon_con_recipiente_kg": _num(fase.peso_carbon_con_recipiente_kg),
        "peso_cenizas_kg": _num(fase.peso_cenizas_kg),
        "observaciones": fase.observaciones,
        "mediciones_opcionales": _medicion_a_dict(fase.medicion),
    }


# ------------------------------------------------------------
# Serialización de la prueba y sus catálogos
# ------------------------------------------------------------
def _promedio_humedad(muestras):
    """Promedio de las mediciones de humedad de la prueba (3 leños × 3)."""
    valores = [float(m.humedad_pct) for m in muestras if m.humedad_pct is not None]
    if not valores:
        return None
    return round(sum(valores) / len(valores), 2)


def _prueba_a_dict(prueba):
    conjunto = prueba.conjunto_pruebas
    estufa_id = conjunto.estufa_id if conjunto is not None else None

    return {
        "id": prueba.id,
        "uuid": str(prueba.uuid),
        "fecha": _fecha(prueba.fecha),
        "investigador_id": prueba.investigador_id,
        "laboratorio_id": prueba.laboratorio_id,
        "combustible_id": prueba.combustible_id,
        "condiciones_ambientales_id": prueba.condiciones_ambientales_id,
        "conjunto_pruebas_id": prueba.conjunto_pruebas_id,
        "estufa_id": estufa_id,
        "peso_recipiente_carbon_kg": _num(prueba.peso_recipiente_carbon_kg),
        "numero_repeticion": prueba.numero_repeticion,
        "humedad_promedio_pct": _promedio_humedad(prueba.muestra_humedad),
        "es_valida": prueba.es_valida,
        "motivo_invalidez": prueba.motivo_invalidez,
        "version_protocolo": prueba.version_protocolo,
        "observaciones": prueba.observaciones,
        "created_at": _fecha(prueba.created_at),
        "updated_at": _fecha(prueba.updated_at),
    }


def _estufa_a_dict(estufa):
    if estufa is None:
        return None
    return {
        "id": estufa.id,
        "marca": estufa.marca,
        "fabricante": estufa.fabricante,
        "area_camara_cm2": _num(estufa.area_camara_cm2),
        "altura_cm": _num(estufa.altura_cm),
        "numero_hornillas": estufa.numero_hornillas,
        "material": estufa.material,
        "descripcion": estufa.descripcion,
    }


def _conjunto_a_dict(conjunto):
    if conjunto is None:
        return None
    return {
        "id": conjunto.id,
        "estufa_id": conjunto.estufa_id,
        "descripcion": conjunto.descripcion,
    }


def _combustible_a_dict(combustible):
    if combustible is None:
        return None
    return {
        "id": combustible.id,
        "tipo": combustible.tipo,
        "longitud_combustible_cm": _num(combustible.longitud_combustible_cm),
        "ancho_combustible_cm": _num(combustible.ancho_combustible_cm),
        "poder_calorifico_neto_mj_kg": _num(combustible.poder_calorifico_neto_mj_kg),
        "poder_calorifico_bruto_mj_kg": _num(combustible.poder_calorifico_bruto_mj_kg),
        "poder_calorifico_carbon_mj_kg": _num(combustible.poder_calorifico_carbon_mj_kg),
        "contenido_carbono_carbon_pct": _num(combustible.contenido_carbono_carbon_pct),
        "tipo_alimentacion": combustible.tipo_alimentacion,
        "contenido_carbono_pct": _num(combustible.contenido_carbono_pct),
        "descripcion": combustible.descripcion,
    }


def _condiciones_a_dict(condiciones):
    if condiciones is None:
        return None
    return {
        "id": condiciones.id,
        "temperatura_c": _num(condiciones.temperatura_c),
        "humedad_relativa_pct": _num(condiciones.humedad_relativa_pct),
        "altitud_m": _num(condiciones.altitud_m),
        "presion_atmosferica_kpa": _num(condiciones.presion_atmosferica_kpa),
        "viento_ms": _num(condiciones.viento_ms),
        "condicion_viento": condiciones.condicion_viento,
        "punto_ebullicion_c": _num(condiciones.punto_ebullicion_c),
    }


ORDEN_FASES = {"inicio_frio": 0, "inicio_caliente": 1, "baja_potencia": 2}

def _fase_dict(prueba):
    fases = []
    for fase in sorted(prueba.fase_prueba, key=lambda f: ORDEN_FASES.get(f.tipo_fase, 99)):
        ollas = sorted(
            fase.olla_fase,
            key=lambda of: of.olla.numero_olla if of.olla is not None else 0,
        )
        fases.append({
            "id": fase.id,
            "tipo_fase": fase.tipo_fase,
            "t_inicial": fase.t_inicial,
            "t_final": fase.t_final,
            "peso_combustible_inicial_kg": _num(fase.peso_combustible_inicial_kg),
            "peso_combustible_final_kg": _num(fase.peso_combustible_final_kg),
            "peso_carbon_con_recipiente_kg": _num(fase.peso_carbon_con_recipiente_kg),
            "peso_cenizas_kg": _num(fase.peso_cenizas_kg),
            "ollas": [_olla_fase_a_dict(of) for of in ollas],
        })
    return fases

# ------------------------------------------------------------
# Consulta principal
# ------------------------------------------------------------

def exist_prueba_wbt():
    result = db.session.execute(
        text("SELECT to_regclass('public.prueba_wbt')")
    ).scalar()
    return result is not None


def get_data_db(id_prueba):
    stmt = (
        select(PruebaWBT)
        .options(
            selectinload(PruebaWBT.fase_prueba).selectinload(FasePrueba.medicion),
            selectinload(PruebaWBT.fase_prueba).selectinload(FasePrueba.olla_fase).selectinload(OllaFase.olla),
            selectinload(PruebaWBT.fase_prueba).selectinload(FasePrueba.resultados),
            selectinload(PruebaWBT.cond_ambientales),
            selectinload(PruebaWBT.combustible),
            selectinload(PruebaWBT.muestra_humedad),
        )
        .where(PruebaWBT.id == id_prueba)
    )
    data =  db.session.execute(stmt).scalar_one_or_none()
    return data


def _data_dict(data):
    # La humedad no vive en el catálogo de combustible: se mide en cada prueba
    # (3 leños × 3 mediciones) y su promedio alimenta la ecuación (11).
    combustible = _combustible_a_dict(data.combustible)
    if combustible is not None:
        combustible['humedad_pct'] = _promedio_humedad(data.muestra_humedad)

    return {
        'fases':_fase_dict(data),
        'condiciones_ambientales':_condiciones_a_dict(data.cond_ambientales),
        'combustible':combustible,
        'prueba': _prueba_a_dict(data)
    }


def get_data(id):
    data = get_data_db(id)
    if data is None:
        return None
    return _data_dict(data)


def _resultados_guardados(data):
    """Devuelve los resultados persistidos, o None si falta alguna fase."""
    if not data.fase_prueba:
        return None

    resultados = {}
    for fase in data.fase_prueba:
        if not fase.resultados:
            return None
        resultados[fase.tipo_fase] = _redondear(_valores_resultado(fase.resultados[0]))
    return resultados


def _calcular_resultados(dict_prueba):
    """Calcula las fases y devuelve [(fase_id, tipo_fase, resultado)]."""
    combustible = dict_prueba['combustible']
    cond_ambientales = dict_prueba['condiciones_ambientales']
    peso_recipiente_carbon_kg = dict_prueba['prueba']['peso_recipiente_carbon_kg']

    if combustible is None:
        raise ValueError('La prueba no tiene combustible asociado')
    if combustible.get('humedad_pct') is None:
        raise ValueError(
            'La prueba no tiene mediciones de humedad del combustible (muestra_humedad)'
        )

    calculados = []
    dc_frio = None

    for fase in dict_prueba['fases']:
        resultado = calcular_resultado_fase(
            fase,
            fase['ollas'],
            combustible,
            cond_ambientales,
            peso_recipiente_carbon_kg,
            cambio_carbon_frio_kg=dc_frio
        )

        if fase['tipo_fase'] == 'inicio_frio':
            dc_frio = resultado['cambio_carbon_kg']

        calculados.append((fase['id'], fase['tipo_fase'], resultado))

    return calculados


def calculo_fases(id):
    data = get_data_db(id)
    if data is None:
        return None

    guardados = _resultados_guardados(data)
    if guardados is not None:
        return guardados

    return {
        tipo: _redondear(resultado)
        for _, tipo, resultado in _calcular_resultados(_data_dict(data))
    }


def guardar_resultados(id):
    """Calcula y persiste un resultado_fase por fase.

    Reemplaza los resultados previos de la prueba. Se ejecuta después de
    guardar la prueba completa, en su propia transacción: si el cálculo falla,
    la prueba ya guardada se conserva.
    """
    data = get_data_db(id)
    if data is None:
        return None

    calculados = _calcular_resultados(_data_dict(data))
    ids_fases = [fase_id for fase_id, _, _ in calculados]

    try:
        # Reemplaza los resultados previos: la relación es 1:1 por fase.
        db.session.query(resultado_fase).filter(
            resultado_fase.fase_id.in_(ids_fases)
        ).delete(synchronize_session='fetch')

        db.session.add_all(
            resultado_fase(fase_id=fase_id, **resultado)
            for fase_id, _, resultado in calculados
        )
        db.session.commit()
    except IntegrityError as exc:
        db.session.rollback()
        raise ValueError(
            f'No se pudieron guardar los resultados: {exc.orig}'
        ) from exc

    return {tipo: _redondear(resultado) for _, tipo, resultado in calculados}


# ------------------------------------------------------------
# Resultado de la prueba (métricas IWA y valores de referencia)
# ------------------------------------------------------------
def _fases_resultado(data):
    """Devuelve {tipo_fase: valores de resultado_fase} para la prueba."""
    fases = {}
    for fase in data.fase_prueba:
        if fase.resultados:
            fases[fase.tipo_fase] = _valores_resultado(fase.resultados[0])
        else:
            fases[fase.tipo_fase] = None
    return fases


def _promedio(valores):
    valores = [v for v in valores if v is not None]
    if not valores:
        return None
    return sum(valores) / len(valores)


def _calcular_resultado_prueba(data):
    """Compone los campos de resultado_prueba desde resultado_fase.

    Las métricas de emisiones quedan en None hasta que exista su módulo.
    """
    fases = _fases_resultado(data)
    frio = fases.get('inicio_frio')
    caliente = fases.get('inicio_caliente')
    baja = fases.get('baja_potencia')

    lhv = None
    combustible = data.combustible
    if combustible and (combustible.poder_calorifico_neto_mj_kg is not None
                        or combustible.poder_calorifico_bruto_mj_kg is not None):
        lhv = poder_calorifico_neto_mj_kg(combustible.poder_calorifico_neto_mj_kg,
                                          combustible.poder_calorifico_bruto_mj_kg)

    # η_alta = (η_c + η_h) / 2; si no hay inicio caliente, solo η_c.
    eficiencia_alta = None
    altas = [frio, caliente] if 'inicio_caliente' in fases else [frio]
    if all(fase and fase['eficiencia_termica_pct'] is not None for fase in altas):
        eficiencia_alta = _promedio([fase['eficiencia_termica_pct'] for fase in altas])

    # SC_baja = f_d,s × LHV / (m_rest × Δt_s × 1000), en MJ/(min·L).
    # consumo_especifico_g_l = f_d,s[g] / m_rest[L], así que:
    # SC_baja = consumo_especifico_g_l × LHV / (1000 × Δt_s).
    sc_baja = None
    if (
        baja is not None
        and lhv is not None
        and baja['consumo_especifico_g_l'] is not None
        and baja['tiempo_fase_min']
    ):
        sc_baja = (
            baja['consumo_especifico_g_l'] * lhv
            / (1000 * baja['tiempo_fase_min'])
        )

    # TDR = FP_c / FP_s
    relacion = None
    if (
        frio is not None
        and baja is not None
        and frio['potencia_fase_kw'] is not None
        and baja['potencia_fase_kw']
    ):
        relacion = frio['potencia_fase_kw'] / baja['potencia_fase_kw']

    # BF = 5 × (promedio(SC_corr,c; SC_corr,h) + SC_s)
    promedio_corr = _promedio([
        fase['consumo_especifico_corregido_g_l']
        for fase in (frio, caliente)
        if fase is not None
    ])
    sc_s = baja['consumo_especifico_g_l'] if baja is not None else None

    combustible_ref = None
    energia_ref = None
    if promedio_corr is not None and sc_s is not None:
        combustible_ref = 5 * (promedio_corr + sc_s)
        if lhv is not None:
            # g -> kg, MJ/kg -> kJ
            energia_ref = (combustible_ref / 1000) * lhv * 1000

    return {
        'eficiencia_alta_pct': eficiencia_alta,
        'consumo_especifico_baja_mj_min_l': sc_baja,
        'relacion_reduccion': relacion,
        'combustible_ref_5l_g': combustible_ref,
        'energia_ref_5l_kj': energia_ref,
        'co_alta_g_mj': None,
        'pm_alta_mg_mj': None,
        'co_baja_g_min_l': None,
        'pm_baja_mg_min_l': None,
        'co_interior_g_min': None,
        'pm_interior_mg_min': None,
        'co_ref_5l_g': None,
        'pm_ref_5l_g': None,
    }


def guardar_resultado_prueba(id):
    """Calcula y persiste resultado_prueba. Reemplaza el resultado previo."""
    data = get_data_db(id)
    if data is None:
        return None

    valores = _calcular_resultado_prueba(data)

    try:
        db.session.query(resultado_prueba).filter_by(
            prueba_wbt_id=id
        ).delete(synchronize_session='fetch')
        db.session.add(resultado_prueba(prueba_wbt_id=id, **valores))
        db.session.commit()
    except IntegrityError as exc:
        db.session.rollback()
        raise ValueError(
            f'No se pudo guardar el resultado de la prueba: {exc.orig}'
        ) from exc

    return _resultado_prueba_a_dict(
        resultado_prueba.query.filter_by(prueba_wbt_id=id).one()
    )


def resultado_prueba_de(id):
    """Devuelve el resultado persistido o lo compone sin guardarlo."""
    data = get_data_db(id)
    if data is None:
        return None

    if data.resultado is not None:
        return _resultado_prueba_a_dict(data.resultado)

    return {
        'id': None,
        'prueba_wbt_id': id,
        **_calcular_resultado_prueba(data),
    }


def iwa_conjunto(conjunto_id):
    if db.session.get(ConjuntoPruebas, conjunto_id) is None:
        return None

    umbrales = db.session.execute(text("""
        SELECT * FROM iwa_umbral
        WHERE version = (SELECT max(version) FROM iwa_umbral)
    """)).mappings().all()
    pruebas = PruebaWBT.query.filter_by(conjunto_pruebas_id=conjunto_id, es_valida=True).options(
        joinedload(PruebaWBT.resultado), joinedload(PruebaWBT.combustible),
        selectinload(PruebaWBT.fase_prueba).selectinload(FasePrueba.resultados),
    ).all()
    # Las pruebas anteriores a resultado_prueba pueden tener resultados de fase.
    resultados = [
        _resultado_prueba_a_dict(p.resultado) if p.resultado else _calcular_resultado_prueba(p)
        for p in pruebas
    ]
    metricas = {}
    for umbral in umbrales:
        campo = umbral['metrica']
        valores = [Decimal(str(r[campo])) for r in resultados if r.get(campo) and r[campo] > 0]
        promedio = sum(valores) / len(valores) if valores else None
        tier = 'NA'
        if len(valores) >= 3:
            tier = 'T0'
            for nivel in range(1, 5):
                limite = umbral[f't{nivel}']
                cumple = promedio >= limite if umbral['mayor_es_mejor'] else promedio <= limite
                if cumple:
                    tier = f'T{nivel}'
        metricas[campo] = {'promedio': _num(promedio), 'n': len(valores), 'tier': tier}
    return {
        'conjunto_pruebas_id': conjunto_id,
        'version_umbrales': umbrales[0]['version'] if umbrales else None,
        'pruebas_validas': len(pruebas),
        'metricas': metricas,
    }
