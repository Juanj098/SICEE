from decimal import Decimal

from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy import select, text

from app.extensions import db
from app.modules.pruebas.models import (
    ConjuntoPruebas,
    FasePrueba,
    OllaFase,
    PruebaWBT,
)
from .models import resultado_fase
from app.modules.calculos.formulas import calcular_resultado_fase


def _num(valor):
    return float(valor) if valor is not None else None


def _fecha(valor):
    return valor.isoformat() if valor is not None else None


def _redondear(resultado, decimales=2):
    return {
        k: round(v, decimales) if isinstance(v, float) else v
        for k, v in resultado.items()
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
        "humedad_pct": _num(combustible.humedad_pct),
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
        )
        .where(PruebaWBT.id == id_prueba)
    )
    data =  db.session.execute(stmt).scalar_one_or_none()
    return data


def get_data(id):
    data = get_data_db(id)
    if data is None:
        return None
    return {
        'fases':_fase_dict(data),
        'condiciones_ambientales':_condiciones_a_dict(data.cond_ambientales),
        'combustible':_combustible_a_dict(data.combustible),
        'prueba': _prueba_a_dict(data)
    }


def calculo_fases(id):
    dict_prueba = get_data(id)
    if dict_prueba is None:
        return None

    combustible = dict_prueba['combustible']
    cond_ambientales = dict_prueba['condiciones_ambientales']
    peso_recipiente_carbon_kg = dict_prueba['prueba']['peso_recipiente_carbon_kg']

    resp = {}
    dc_frio = None
    
    for fase in dict_prueba['fases']:
        tipo = fase['tipo_fase']  

        resultado = calcular_resultado_fase(
            fase,
            fase['ollas'],
            combustible,
            cond_ambientales,
            peso_recipiente_carbon_kg,
            cambio_carbon_frio_kg=dc_frio
        )

        if tipo == 'inicio_frio':
            dc_frio = resultado['cambio_carbon_kg']


        resp[tipo]=_redondear(resultado)
    return resp