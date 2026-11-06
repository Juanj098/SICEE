import pandas as pd
import numpy as np
from datetime import datetime

# /--- Masa_agua---/
def masa_agua_inicial(m_olla_agua_i, m_olla_seca):
    return (m_olla_agua_i - m_olla_seca)

def masa_agua_final(m_olla_agua_f, m_olla_seca):
    return (m_olla_agua_f - m_olla_seca)

def masa_agua_eva(m_olla_agua_i, m_olla_agua_f, m_olla_seca):
    m_agua_i = masa_agua_inicial(m_olla_agua_i, m_olla_seca)
    m_agua_f = masa_agua_final(m_olla_agua_f, m_olla_seca)
    return (m_agua_i - m_agua_f)

# /--- t_ebullicion ---/
def t_ebullicion(tiempo_final, tiempo_inicial):
    if tiempo_inicial is None or tiempo_final is None:
        return None

    if isinstance(tiempo_inicial, str):
        tiempo_inicial = datetime.fromisoformat(tiempo_inicial)

    if isinstance(tiempo_final, str):
        tiempo_final = datetime.fromisoformat(tiempo_final)

    if tiempo_final < tiempo_inicial:
        raise ValueError('timpo_final no puede ser anterior a tiempo_inicial')

    return round((tiempo_final - tiempo_inicial).total_seconds() / 60, 2)

def Tiempo_fase_min(tiempo_incial, tiempo_final):
    if tiempo_final is None or tiempo_incial is None:
        return None
    if isinstance(tiempo_incial, str):
        tiempo_incial = datetime.fromisoformat(tiempo_incial)

    if isinstance(tiempo_final, str):
        tiempo_final = datetime.fromisoformat(tiempo_final)

    if tiempo_final < tiempo_incial:
        raise ValueError('Tiempo_final no puede ser anterior a Tiempo_final')
    return round((tiempo_final - tiempo_incial).total_seconds() / 60, 2)

# /--- Combustible_consumido ---/
def m_combustible_consumido(m_combustible_inicial, m_combustible_final):
    return m_combustible_inicial - m_combustible_final

def m_combustible_seco(m_combustible_i, m_combustible_f, humedad_combustible):
    humedad_combustible = float(humedad_combustible)/100
    m_combustible_seco = (
        m_combustible_consumido(m_combustible_i, m_combustible_f) * (1-humedad_combustible)
    )
    return m_combustible_seco

# /--- Energia_transferida_agua ---/
def Q_sensible(m_olla_agua_i, m_olla_agua_f, m_olla_seca, temp_i, temp_f):
    m_agua_inicial = masa_agua_inicial(m_olla_agua_i, m_olla_seca)
    m_agua_final = masa_agua_final(m_olla_agua_f, m_olla_seca)
    m_agua_prom = (m_agua_final+m_agua_inicial)/2
    CP_AGUA_KJ_KG_C = 4.186
    q_sensible = m_agua_prom*CP_AGUA_KJ_KG_C*(temp_f - temp_i)
    return q_sensible

def Q_latente(m_olla_agua_i, m_olla_agua_f, m_olla_seca):
    H_VAPORIZACION_KJ_KG = 2260
    m_agua_eva = masa_agua_eva(m_olla_agua_i,m_olla_agua_f, m_olla_seca)
    q_latente = m_agua_eva * H_VAPORIZACION_KJ_KG
    return q_latente

def Q_util(m_olla_agua_i, m_olla_agua_f, m_olla_seca, temp_i, temp_f):
    q_util = Q_sensible(m_olla_agua_i, m_olla_agua_f, m_olla_seca, temp_i, temp_f) + Q_latente(m_olla_agua_i, m_olla_agua_f, m_olla_seca)
    return q_util

# /--- Eficiencia_termica ---/
def Q_combustible(m_combustible_i, m_combustible_f, humedad_combustible, PCI):
    # PCI -> poder_calorifico_neto
    q_combustible = m_combustible_seco(m_combustible_i, m_combustible_f, humedad_combustible) * PCI
    return q_combustible

def Eficiencia_termica(m_olla_agua_i, m_olla_agua_f, m_olla_seca, temp_i, temp_f, m_combustible_i, m_combustible_f, humedad_combustible,PCI):
    eficiencia_termica = 100 * Q_util(m_olla_agua_i, m_olla_agua_f, m_olla_seca, temp_i, temp_f)/Q_combustible(m_combustible_i, m_combustible_f, humedad_combustible,PCI)
    return eficiencia_termica

# /--- Consumo especifico ---/
def Combustible_seco_equivalente(peso_combustible_i_kg, peso_combustible_f_kg, humedad_pct):
    combustible_seco_equivalente = (peso_combustible_i_kg - peso_combustible_f_kg) * (1 - (humedad_pct/100))
    return combustible_seco_equivalente

def Consumo_especifico(peso_olla_agua_i, peso_olla_seco, temp_i, temp_f, pto_ebullicion, peso_combustible_i_kg, peso_combustible_f_kg, humedad_pct):
    litros_agua_utiles = (peso_olla_agua_i - peso_olla_seco)*((temp_f - temp_i)/(pto_ebullicion - temp_i))
    consumo_especifico = Combustible_seco_equivalente(peso_combustible_i_kg, peso_combustible_f_kg, humedad_pct) / litros_agua_utiles
    return consumo_especifico

def Consumo_energetico(peso_olla_agua_i, peso_olla_seco, temp_i, temp_f, pto_ebullicion, peso_combustible_i_kg, peso_combustible_f_kg, humedad_pct, PCI):
    consumo_energetico = Consumo_especifico(peso_olla_agua_i, peso_olla_seco, temp_i, temp_f, pto_ebullicion, peso_combustible_i_kg, peso_combustible_f_kg, humedad_pct) * PCI
    return consumo_energetico

# /--- Caracterizacion de estufa ---/
def Velocidad_combustion(peso_combustible_i_kg, peso_combustible_f_kg, tiempo_inicial, tiempo_final):
    combustible_consumido_g = (peso_combustible_i_kg - peso_combustible_f_kg)*1000
    tiempo_fase = Tiempo_fase_min(tiempo_inicial, tiempo_final)
    return combustible_consumido_g / tiempo_fase

def Potencia_fuego_kw (m_combustible_i, m_combustible_f, humedad_combustible, pci, tiempo_inicial, tiempo_final):
    combustible_seco_kg = m_combustible_seco(m_combustible_i, m_combustible_f, humedad_combustible)
    energia_kj = (combustible_seco_kg*pci)*1000
    tiempo_fase_s = Tiempo_fase_min(tiempo_inicial, tiempo_final)*60

    return energia_kj / tiempo_fase_s