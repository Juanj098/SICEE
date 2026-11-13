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


def _num(valor):
    """Convierte Decimal a float para que el JSON sea numérico."""
    return float(valor) if valor is not None else None


def _fecha(valor):
    return valor.isoformat() if valor is not None else None


def _masa_agua(peso_con_agua_kg, peso_seco_kg):
    """Masa de agua de una olla: peso con agua menos peso seco."""
    if peso_con_agua_kg is None or peso_seco_kg is None:
        return None
    return peso_con_agua_kg - peso_seco_kg


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
        "id": olla_fase.id,
        "olla_id": olla_fase.olla_id,
        "numero_olla": olla.numero_olla if olla is not None else None,
        "capacidad_l": _num(olla.capacidad_l) if olla is not None else None,
        "peso_seco_kg": _num(peso_seco),
        "temperatura_inicial_agua_c": _num(olla_fase.temperatura_inicial_agua_c),
        "temperatura_final_agua_c": _num(olla_fase.temperatura_final_agua_c),
        "peso_con_agua_inicial_kg": _num(olla_fase.peso_con_agua_inicial_kg),
        "peso_con_agua_final_kg": _num(olla_fase.peso_con_agua_final_kg),
        "masa_agua_inicial_kg": _num(_masa_agua(olla_fase.peso_con_agua_inicial_kg, peso_seco)),
        "masa_agua_final_kg": _num( _masa_agua(olla_fase.peso_con_agua_final_kg, peso_seco)),
    }


def _agua_fase(fase):
    """Suma las masas de agua de todas las ollas de una fase."""
    iniciales = []
    finales = []

    for olla_fase in fase.olla_fase:
        olla = olla_fase.olla
        if olla is None or olla.peso_seco_kg is None:
            return None, None, None

        masa_inicial = _masa_agua(olla_fase.peso_con_agua_inicial_kg, olla.peso_seco_kg)
        if masa_inicial is None:
            return None, None, None
        iniciales.append(masa_inicial)

        masa_final = _masa_agua(olla_fase.peso_con_agua_final_kg, olla.peso_seco_kg)
        if masa_final is not None:
            finales.append(masa_final)

    if not iniciales:
        return None, None, None

    masa_inicial = sum(iniciales, Decimal("0"))
    masa_final = (sum(finales, Decimal("0"))
        if len(finales) == len(iniciales)
        else None
    )
    evaporada = (masa_inicial - masa_final if masa_final is not None else None)
    return masa_inicial, masa_final, evaporada


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
    resultado = fase.resultados[0] if fase.resultados else None
    masa_inicial, masa_final, masa_evaporada = _agua_fase(fase)

    ollas = sorted(
        fase.olla_fase,
        key=lambda olla_fase: (
            olla_fase.olla.numero_olla
            if olla_fase.olla is not None
            else 0
        ),
    )
    return {
        "id": fase.id,
        "tipo_fase": fase.tipo_fase,
        "t_inicial": _fecha(fase.t_inicial),
        "t_final": _fecha(fase.t_final),
        "peso_combustible_inicial_kg": _num(fase.peso_combustible_inicial_kg),
        "peso_combustible_final_kg": _num(fase.peso_combustible_final_kg),
        "peso_carbon_con_recipiente_kg": _num(fase.peso_carbon_con_recipiente_kg),
        "peso_cenizas_kg": _num(fase.peso_cenizas_kg),
        "observaciones": fase.observaciones,
        "agua": {
            "masa_inicial_kg": _num(masa_inicial),
            "masa_final_kg": _num(masa_final),
            "masa_evaporada_kg": _num(masa_evaporada),
        },
        "ollas": [_olla_fase_a_dict(olla_fase) for olla_fase in ollas],
        "mediciones_opcionales": _medicion_a_dict(fase.medicion),
        "resultado": _resultado_a_dict(resultado),
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


# ------------------------------------------------------------
# Consulta principal
# ------------------------------------------------------------
def obtener_prueba_completa(prueba_id):
    """Carga la prueba con sus fases, ollas, mediciones y catálogos."""
    stmt = (
        select(PruebaWBT)
        .options(
            selectinload(PruebaWBT.fase_prueba)
            .selectinload(FasePrueba.medicion),
            selectinload(PruebaWBT.fase_prueba)
            .selectinload(FasePrueba.resultados),
            selectinload(PruebaWBT.fase_prueba)
            .selectinload(FasePrueba.olla_fase)
            .selectinload(OllaFase.olla),
            joinedload(PruebaWBT.combustible),
            joinedload(PruebaWBT.cond_ambientales),
            joinedload(PruebaWBT.conjunto_pruebas)
            .joinedload(ConjuntoPruebas.estufa),
        )
        .where(PruebaWBT.id == prueba_id)
    )
    return db.session.execute(stmt).scalar_one_or_none()


def get_datos(prueba_id):
    """Devuelve todo lo necesario para calcular una prueba, listo para JSON."""
    prueba = obtener_prueba_completa(prueba_id)
    if prueba is None:
        return None

    conjunto = prueba.conjunto_pruebas
    estufa = conjunto.estufa if conjunto is not None else None

    return {
        "prueba": _prueba_a_dict(prueba),
        "conjunto_pruebas": _conjunto_a_dict(conjunto),
        "estufa": _estufa_a_dict(estufa),
        "combustible": _combustible_a_dict(prueba.combustible),
        "condiciones_ambientales": _condiciones_a_dict(prueba.cond_ambientales),
        "fases": [_fase_a_dict(fase) for fase in prueba.fase_prueba],
    }


def exist_prueba_wbt():
    result = db.session.execute(
        text("SELECT to_regclass('public.prueba_wbt')")
    ).scalar()
    return result is not None
