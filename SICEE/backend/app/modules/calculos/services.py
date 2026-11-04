from sqlalchemy import select, text
from sqlalchemy.orm import joinedload, selectinload

from app.extensions import db
from app.modules.pruebas.models import FasePrueba, PruebaWBT
from .models import resultado_fase


def _num(valor):
    """Convierte Decimal a float para que el JSON sea numérico."""
    return float(valor) if valor is not None else None


def _fecha(valor):
    return valor.isoformat() if valor is not None else None


def _resultado_a_dict(resultado):
    if resultado is None:
        return None
    return {
        "id": resultado.id,
        "tiempo_fase_min": _num(resultado.tiempo_fase_min),
        "masa_agua_inicial_kg": _num(resultado.masa_agua_inicial_kg),
        "masa_agua_final_kg": _num(resultado.masa_agua_final_kg),
        "masa_agua_evaporada_kg": _num(resultado.masa_agua_evaporada_kg),
        "combustible_consumido_kg": _num(resultado.combustible_consumido_kg),
        "tiempo_ebullicion_min": _num(resultado.tiempo_ebullicion_min),
        "energia_util_kj": _num(resultado.energia_util_kj),
        "energia_combustible_kj": _num(resultado.energia_combustible_kj),
        "eficiencia_termica_pct": _num(resultado.eficiencia_termica_pct),
        "consumo_especifico": _num(resultado.consumo_especifico),
        "velocidad_combustion_g_min": _num(resultado.velocidad_combustion_g_min),
        "potencia_fase_kw": _num(resultado.potencia_fase_kw),
        "humedad_ambiente_promedio_pct": _num(
            resultado.humedad_ambiente_promedio_pct
        ),
    }


def _fase_a_dict(fase):
    medicion = fase.medicion
    resultado = fase.resultados[0] if fase.resultados else None
    return {
        "id": fase.id,
        "tipo_fase": fase.tipo_fase,
        "numero_repeticion": fase.numero_repeticion,
        "t_inicial": _fecha(fase.t_inicial),
        "t_final": _fecha(fase.t_final),
        "temperatura_inicial_agua_c": _num(fase.temperatura_inicial_agua_c),
        "temperatura_final_agua_c": _num(fase.temperatura_final_agua_c),
        "peso_olla_seco_kg": _num(fase.peso_olla_seco_kg),
        "peso_olla_agua_inicial_kg": _num(fase.peso_olla_agua_inicial_kg),
        "peso_olla_agua_final_kg": _num(fase.peso_olla_agua_final_kg),
        "peso_combustible_inicial_kg": _num(fase.peso_combustible_inicial_kg),
        "peso_combustible_final_kg": _num(fase.peso_combustible_final_kg),
        "mediciones_opcionales": (
            {
                "id": medicion.id,
                "co_ppm": _num(medicion.co_ppm),
                "pm_mg_m3": _num(medicion.pm_mg_m3),
                "co2_ppm": _num(medicion.co2_ppm),
                "temperatura_ducto_c": _num(medicion.temperatura_ducto_c),
                "presion_atmosferica_kpa": _num(
                    medicion.presion_atmosferica_kpa
                ),
            }
            if medicion
            else None
        ),
        "resultado": _resultado_a_dict(resultado),
    }


def obtener_prueba_completa(prueba_id):
    """Carga la prueba con fases, mediciones, combustible y condiciones."""
    stmt = (
        select(PruebaWBT)
        .options(
            selectinload(PruebaWBT.fase_prueba)
            .selectinload(FasePrueba.medicion),
            selectinload(PruebaWBT.fase_prueba)
            .selectinload(FasePrueba.resultados),
            joinedload(PruebaWBT.combustible),
            joinedload(PruebaWBT.cond_ambientales),
        )
        .where(PruebaWBT.id == prueba_id)
    )
    return db.session.execute(stmt).scalar_one_or_none()


def get_datos(prueba_id):
    """Devuelve todo lo necesario para calcular una prueba, listo para JSON."""
    prueba = obtener_prueba_completa(prueba_id)
    if prueba is None:
        return None

    combustible = prueba.combustible
    condiciones = prueba.cond_ambientales

    return {
        "prueba": {
            "id": prueba.id,
            "uuid": str(prueba.uuid),
            "fecha": _fecha(prueba.fecha),
            "observaciones": prueba.observaciones,
            "investigador_id": prueba.investigador_id,
            "laboratorio_id": prueba.laboratorio_id,
            "estufa_id": prueba.estufa_id,
            "combustible_id": prueba.combustible_id,
            "condiciones_ambientales_id": prueba.condiciones_ambientales_id,
        },
        "combustible": (
            {
                "id": combustible.id,
                "tipo": combustible.tipo,
                "humedad_pct": _num(combustible.humedad_pct),
                "poder_calorifico_neto_mj_kg": _num(
                    combustible.poder_calorifico_neto_mj_kg
                ),
                "poder_calorifico_bruto_mj_kg": _num(
                    combustible.poder_calorifico_bruto_mj_kg
                ),
                "contenido_carbono_pct": _num(
                    combustible.contenido_carbono_pct
                ),
            }
            if combustible
            else None
        ),
        "condiciones_ambientales": (
            {
                "id": condiciones.id,
                "temperatura_c": _num(condiciones.temperatura_c),
                "humedad_relativa_pct": _num(
                    condiciones.humedad_relativa_pct
                ),
                "presion_atmosferica_kpa": _num(
                    condiciones.presion_atmosferica_kpa
                ),
                "viento_ms": _num(condiciones.viento_ms),
                "punto_ebullicion_c": _num(condiciones.punto_ebullicion_c),
            }
            if condiciones
            else None
        ),
        "fases": [_fase_a_dict(fase) for fase in prueba.fase_prueba],
    }


def exist_prueba_wbt():

    result = db.session.execute(
        text("SELECT to_regclass('public.prueba_wbt')")
    ).scalar()
    return result is not None
