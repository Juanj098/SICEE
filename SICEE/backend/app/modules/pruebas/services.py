from app.extensions import db
from .models import (
    Cond_Ambientales,
    FasePrueba,
    MedicionesOps,
    PruebaWBT,
)


# /---Cond_Ambientales---/
def list_condicion_ambiental():
    return Cond_Ambientales.query.all()


def crear_condicion_ambiental(
    temperatura_c,
    humedad_relativa_pct,
    presion_atmosferica_kpa,
    viento_ms,
    punto_ebullicion_c,
):
    condiciones_ambientales = Cond_Ambientales(
        temperatura_c=temperatura_c,
        humedad_relativa_pct=humedad_relativa_pct,
        presion_atmosferica_kpa=presion_atmosferica_kpa,
        viento_ms=viento_ms,
        punto_ebullicion_c=punto_ebullicion_c,
    )
    db.session.add(condiciones_ambientales)
    db.session.commit()
    return condiciones_ambientales


# /---Prueba_WBT---/
def list_pruebas_wbt():
    return PruebaWBT.query.all()


def registrar_Prueba_wbt(
    fecha,
    investigador_id,
    laboratorio_id,
    estufa_id,
    combustible_id,
    condiciones_amb_id,
    observaciones,
):
    prueba_wbt = PruebaWBT(
        fecha=fecha,
        investigador_id=investigador_id,
        laboratorio_id=laboratorio_id,
        estufa_id=estufa_id,
        combustible_id=combustible_id,
        condiciones_ambientales_id=condiciones_amb_id,
        observaciones=observaciones,
    )
    db.session.add(prueba_wbt)
    db.session.commit()
    return prueba_wbt


# /--- Fase_Prueba ---/
def list_fases_prueba():
    return FasePrueba.query.all()


def crear_fase_prueba(
    prueba_wbt_id,
    tipo_fase,
    numero_repeticion,
    t_inicial,
    t_final=None,
    temperatura_inicial_agua_c=None,
    temperatura_final_agua_c=None,
    peso_olla_seco_kg=None,
    peso_olla_agua_inicial_kg=None,
    peso_olla_agua_final_kg=None,
    peso_combustible_inicial_kg=None,
    peso_combustible_final_kg=None,
):
    fase = FasePrueba(
        prueba_wbt_id=prueba_wbt_id,
        tipo_fase=tipo_fase,
        numero_repeticion=numero_repeticion,
        t_inicial=t_inicial,
        t_final=t_final,
        temperatura_inicial_agua_c=temperatura_inicial_agua_c,
        temperatura_final_agua_c=temperatura_final_agua_c,
        peso_olla_seco_kg=peso_olla_seco_kg,
        peso_olla_agua_inicial_kg=peso_olla_agua_inicial_kg,
        peso_olla_agua_final_kg=peso_olla_agua_final_kg,
        peso_combustible_inicial_kg=peso_combustible_inicial_kg,
        peso_combustible_final_kg=peso_combustible_final_kg,
    )
    db.session.add(fase)
    db.session.commit()
    return fase


# /--- Mediciones_Opcionales ---/
def listar_mediciones_opcionales():
    return MedicionesOps.query.all()


def registrar_mediciones_ops(
    fase_id,
    co_ppm=None,
    pm_mg_m3=None,
    co2_ppm=None,
    temperatura_ducto_c=None,
    presion_atmosferica_kpa=None,
):
    med_ops = MedicionesOps(
        fase_id=fase_id,
        co_ppm=co_ppm,
        pm_mg_m3=pm_mg_m3,
        co2_ppm=co2_ppm,
        temperatura_ducto_c=temperatura_ducto_c,
        presion_atmosferica_kpa=presion_atmosferica_kpa,
    )
    db.session.add(med_ops)
    db.session.commit()
    return med_ops
