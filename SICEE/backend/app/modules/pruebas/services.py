from app.extensions import db
from .models import (
    Cond_Ambientales, 
    FasePrueba,
    MedicionesOps,
    PruebaWBT
)
# /---Cond_Ambientales---/
def list_condicion_ambiental():
    return Cond_Ambientales.query.all()

def crear_condicion_ambiental(temperatura, humedad, presion_atm, viento, pto_ebullicion):
    condiciones_ambientales = Cond_Ambientales(
        temperatura = temperatura,
        humedad = humedad,
        presion_atm = presion_atm,
        viento = viento,
        pto_ebullicion = pto_ebullicion
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
    pruebaWBT = PruebaWBT(
        fecha = fecha,
        investigador_id = investigador_id,
        laboratorio_id = laboratorio_id,
        estufa_id = estufa_id,
        combustible_id = combustible_id,
        condiciones_ambientales_id = condiciones_amb_id,
        observaciones = observaciones,
    )
    db.session.add(pruebaWBT)
    db.aession.commit()
    return pruebaWBT

# /--- Fase_Prueba ---/
def list_fases_prueba():
    return FasePrueba.query.all()

def registrar_fase_prueba(
        prueba_wbt_id, 
        tipo_fase, 
        n_repeticion,
        t_inicial,
        t_final = None,
        temp_inicial_agua_c = None,
        temp_final_agua_c = None,
        peso_olla_seco_kg = None,
        peso_olla_agua_inicial_kg = None,
        peso_olla_agua_final_kg = None,
        peso_combustible_inicial_kg = None,
        peso_combustible_final_kg = None 
    ):
    fase = FasePrueba(
        prueba_wbt_id = prueba_wbt_id,
        tipo_fase = tipo_fase,
        numero_repeticion = n_repeticion,
        t_inicial = t_inicial,
        t_final = t_final,
        temp_inicial_agua_c = temp_inicial_agua_c,
        temp_final_agua_c = temp_final_agua_c,
        peso_olla_seco_kg = peso_olla_seco_kg,
        peso_olla_agua_inicial_kg = peso_olla_agua_inicial_kg,
        peso_olla_agua_final_kg = peso_olla_agua_final_kg,
        peso_combustible_inicial_kg = peso_combustible_inicial_kg,
        peso_combustible_final_kg = peso_combustible_final_kg
    )
    db.session.add(fase)
    db.session.commit()
    return fase

# /--- Mediciones_Opcionales ---/
def list_mediciones_ops():
    return MedicionesOps.query.all()

def registrar_mediciones_ops(
        fase_id,
        co_ppm,
        pm_mg_m3,
        co2_ppm,
        temperatura_ducto_c,
        presion_atmosferica_kpa
    ):
    medOps = MedicionesOps(
        fase_id = fase_id,
        co_ppm = co_ppm,
        pm_mg_m3 = pm_mg_m3,
        co2_ppm = co2_ppm,
        temperatura_ducto_c = temperatura_ducto_c,
        presion_atmosferica_kpa = presion_atmosferica_kpa
    )
    db.session.add(medOps)
    db.session.commit()
    return medOps

