from datetime import datetime

CP_AGUA_KJ_KG_C = 4.186
H_VAPORIZACION_KJ_KG = 2260
H_VAPORIZACION_COMBUSTIBLE_KJ_KG = 2257
T_REF_BAJA_C = 25
DELTA_T_REF_C = 75

TIPOS_FASE = {
    'inicio_frio',
    'inicio_caliente',
    'baja_potencia'
}

CAMPOS_OLLA = (
    'peso_con_agua_inicial_kg',
    'peso_con_agua_final_kg',
    'temperatura_inicial_agua_c',
    'temperatura_final_agua_c'
)

def _ollas_con_datos(ollas_fase):
    validas = []
    for ollas in ollas_fase:
        n_olla = ollas.get('numero_olla')
        faltan = [campo for campo in CAMPOS_OLLA if ollas.get(campo) is None]
        if len(faltan) == len(CAMPOS_OLLA):
            continue
        if faltan:
            raise ValueError(f'Olla {n_olla} con datos incompletos: faltan {faltan}')
        if ollas.get('peso_seco_kg') is None:
            raise ValueError(f'Olla {n_olla} sin peso_seco_kg')
        validas.append(ollas)
    if not validas:
        raise ValueError('La fase no tiene ninguna olla con datos')
    return validas

# /--- Utilidades ---/
# Función 1
def _f(valor):
    """Convierte Decimal/str a float. La BD devuelve Decimal y no se puede mezclar con float."""
    return None if valor is None else float(valor)


# Función 2
def _a_datetime(valor):
    return datetime.fromisoformat(valor) if isinstance(valor, str) else valor

# pcn / ec. 2
def poder_calorifico_neto_mj_kg(neto, bruto):
    if neto is not None:
        return _f(neto)
    if bruto is None:
        raise ValueError('El combustible requiere poder calorifico neto o bruto')
    return max(_f(bruto)-1.32, 0.0)
    
# /--- Tiempos ---/
# Función 3  |  Ec. (6)
def tiempo_fase_min(t_inicial, t_final):
    if t_inicial is None or t_final is None:
        return None
    t_inicial = _a_datetime(t_inicial)
    t_final = _a_datetime(t_final)
    if t_final < t_inicial:
        raise ValueError("t_final no puede ser anterior a t_inicial")
    return round((t_final - t_inicial).total_seconds() / 60, 2)


# En las fases de alta potencia t_final es el momento de ebullición,
# así que el tiempo de ebullición es el mismo cálculo.
# (alias de la Función 3)
tiempo_ebullicion_min = tiempo_fase_min


# /--- Agua (por olla) ---/
# Función 4  |  Ec. (3) y (4)
def masa_agua_kg(peso_con_agua_kg, peso_seco_kg):
    return _f(peso_con_agua_kg) - _f(peso_seco_kg)


# Función 5  |  Ec. (5)
def masa_agua_evaporada_kg(ollas_fase):
    total_kg = 0.0
    for olla in ollas_fase:
        total_kg += (_f(olla['peso_con_agua_inicial_kg']) - _f(olla['peso_con_agua_final_kg']))
    return total_kg


# Función 6  |  Ec. (13) y (14)
def masa_agua_efectiva_kg(
        ollas_fase,
        pto_ebullicion_c,
        tipo_fase
    ):
    t_ebullicion = _f(pto_ebullicion_c)
    total_kg = 0.0

    for olla in ollas_fase:

        agua_final_kg = masa_agua_kg(olla['peso_con_agua_final_kg'], olla['peso_seco_kg'])
        t_fin = _f(olla['temperatura_final_agua_c'])

        if tipo_fase == 'baja_potencia':
            if olla.get('numero_olla') == 1:
                total_kg += agua_final_kg
                continue
            t_ref = T_REF_BAJA_C
        else:
            t_ref = _f(olla['temperatura_inicial_agua_c'])

        if t_ebullicion <= t_ref:
            raise ValueError('Punto_ebullicion_c debe ser mayor que la temperatura de referencia...')

        factor = (t_fin - t_ref)/(t_ebullicion - t_ref)

        total_kg += agua_final_kg * factor

    return total_kg


# /--- Energía transferida al agua (por olla) ---/
# Función 7  |  Ec. (15), (19), (20)
def energia_sensible_kj(
        ollas_fase,
        pto_ebullicion,
        tipo_fase
    ):
    t_eb = _f(pto_ebullicion)
    # Baja_potencia
    if tipo_fase == 'baja_potencia':
        olla_1 = next((o for o in ollas_fase if o.get('numero_olla') == 1),None)
        if olla_1 is None:
            raise ValueError('baja potencia requiere la olla 1')            
        
        a_ini_1 = masa_agua_kg(olla_1['peso_con_agua_inicial_kg'], olla_1['peso_seco_kg'])
        a_rest = masa_agua_efectiva_kg(ollas_fase,t_eb,tipo_fase)
        a_prom = (a_ini_1 + a_rest)/2
        delta_t = _f(olla_1['temperatura_final_agua_c']) - _f(olla_1['temperatura_inicial_agua_c'])
        return a_prom * CP_AGUA_KJ_KG_C * delta_t

    
    # Inicio frio, Inicio caliente
    q_sens = 0.0
    for olla in ollas_fase:

        a_ini = masa_agua_kg(olla['peso_con_agua_inicial_kg'], olla['peso_seco_kg'])
        delta_t = _f(olla['temperatura_final_agua_c'])-_f(olla['temperatura_inicial_agua_c'])
        q_sens += CP_AGUA_KJ_KG_C * a_ini * delta_t
    return q_sens


# Función 8  |  Ec. (16)
def energia_latente_kj(ollas_fase):
    return masa_agua_evaporada_kg(ollas_fase) * H_VAPORIZACION_KJ_KG


# Función 9  |  Ec. (17)
# q_util = q_sens+q_lat
def energia_util_kj(ollas_fase, pto_ebullicion,tipo_fase):
    q_util = energia_sensible_kj(ollas_fase,pto_ebullicion,tipo_fase) + energia_latente_kj(ollas_fase)
    return q_util


# /--- Combustible ---/
# Función 10  |  Ec. (8)
def combustible_consumido_kg(peso_combustible_inicial_kg, peso_combustible_final_kg):
    return _f(peso_combustible_inicial_kg) - _f(peso_combustible_final_kg)


# Función 11  |  Ec. (11)
def combustible_seco_equivalente_kg(
        peso_combustible_inicial_kg, 
        peso_combustible_final_kg, 
        humedad_pct,
        poder_calorifico_neto_mj_kg,
        poder_calorifico_carbon_mj_kg,
        peso_recipiente_carbon_kg,
        peso_carbon_con_recipiente_kg,
        temperatura_aire_c,
        punto_ebullicion_c,
        tipo_fase,
        cambio_carbon_frio_kg = None
    ):

    q_agua = CP_AGUA_KJ_KG_C * (_f(punto_ebullicion_c) - _f(temperatura_aire_c)) + H_VAPORIZACION_COMBUSTIBLE_KJ_KG
    cambio_carbon = cambio_carbon_kg(tipo_fase, peso_carbon_con_recipiente_kg,peso_recipiente_carbon_kg,cambio_carbon_frio_kg)
    f_cons = (_f(peso_combustible_inicial_kg) -_f(peso_combustible_final_kg))
    h = _f(humedad_pct)/100
    pcn = _f(poder_calorifico_neto_mj_kg) * 1000
    pcn_carbon = _f(poder_calorifico_carbon_mj_kg) * 1000

    energia_leña_kj = f_cons*(pcn*(1-h)-h*q_agua)
    energia_neta_kj = energia_leña_kj - cambio_carbon * pcn_carbon 
    return energia_neta_kj/pcn


# Función 12  |  Ec. (12)
def energia_combustible_kj(combustible_seco_equivalente_kg, poder_calorifico_neto_mj_kg):
    return combustible_seco_equivalente_kg * _f(poder_calorifico_neto_mj_kg) * 1000


# /--- Indicadores de la fase ---/
# Función 13  |  Ec. (18)
def eficiencia_termica_pct(energia_util_kj, energia_combustible_kj):
    if not energia_combustible_kj:
        return None
    return 100 * energia_util_kj / energia_combustible_kj


# Función 14  |  Ec. (22a) y (22b)
def consumo_especifico_g_l(combustible_seco_equivalente_kg, masa_agua_efectiva_kg):
    if not masa_agua_efectiva_kg:
        return None
    return combustible_seco_equivalente_kg * 1000 / masa_agua_efectiva_kg


# Función 15  |  Ec. (24a)
def energia_especifica_corregida_kj_l(consumo_especifico_corregido_g_l, poder_calorifico_neto_mj_kg):
    # g/L * MJ/kg = kJ/L
    return consumo_especifico_corregido_g_l * _f(poder_calorifico_neto_mj_kg)


# Función 16  |  Ec. (25)
def velocidad_combustion_g_min(combustible_seco_eq_kg, t_inicio, t_final):
    delta_t = tiempo_fase_min(t_inicio, t_final)
    if not delta_t:
        return None
    r = (1000 * combustible_seco_eq_kg) / delta_t
    return r


# Función 17  |  Ec. (26)
def potencia_fase_kw(
        combustible_seco_equivalente_kg, 
        poder_calorifico_neto_mj_kg, 
        t_inicial, 
        t_final
    ):
    q_comb = energia_combustible_kj(combustible_seco_equivalente_kg, poder_calorifico_neto_mj_kg)
    delta_t = tiempo_fase_min(t_inicial, t_final)
    if not delta_t:
        return None
    fp = q_comb / (60 * delta_t)
    return fp


# Función 18 | Ec. (9a), (9b), (9c)
def cambio_carbon_kg(
        tipo_fase,
        peso_carbon_con_recipiente_kg,
        peso_recipiente_carbon_kg,
        cambio_carbon_frio_kg = None
    ):
    if peso_carbon_con_recipiente_kg is None:
        return 0.0
    if peso_recipiente_carbon_kg is None:
        raise ValueError(
            'falta peso_recipiente_carbon_kg: se pesó el carbón de la fase '
            'pero no el recipiente vacío'
        )
    delta = _f(peso_carbon_con_recipiente_kg) - _f(peso_recipiente_carbon_kg)
    if tipo_fase == 'baja_potencia':
        if cambio_carbon_frio_kg is None:
            raise ValueError('baja_potencia requiere cambio_carbon_frio_kg')
        return delta - _f(cambio_carbon_frio_kg)
    return delta


# Función 19 | Ec. (23)
def consumo_especifico_corregido_g_l(ollas_fase, tipo_fase, pto_ebullicion_c, consumo_especifico_g_l):
    if tipo_fase == 'baja_potencia' or consumo_especifico_g_l is None:
        return None

    olla_1 = next((o for o in ollas_fase if o.get('numero_olla') == 1), None)
    if not olla_1 or olla_1.get('temperatura_inicial_agua_c') is None:
        return None
    
    t_ini = _f(olla_1['temperatura_inicial_agua_c'])
    delta_t = _f(pto_ebullicion_c) - t_ini
    if delta_t <= 0:
        raise ValueError('pto_ebullicion debe ser mayor que la temperatura inicial')
    
    sc_corr = consumo_especifico_g_l * (DELTA_T_REF_C/delta_t)
    return sc_corr


# Funcion 20 | Ec. (7)
def tiempo_ebullicion_corregido_min(t_ini, t_fin, pto_ebullicion_c, ollas_fase, tipo_fase):
    if tipo_fase == 'baja_potencia':
        return None
    delta_t = tiempo_fase_min(t_ini, t_fin)
    if delta_t is None:
        return None
    t_eb = _f(pto_ebullicion_c)
    olla_1 = next((o for o in ollas_fase if o.get('numero_olla') == 1), None)
    if olla_1 is None or olla_1.get('temperatura_inicial_agua_c') is None:
        return None
    t_ini_1 = _f(olla_1['temperatura_inicial_agua_c'])
    delta_eb = t_eb - t_ini_1
    if delta_eb <= 0:
        raise ValueError('pto_ebullicion debe ser mayor a temperatura inicial de la olla 1')
    delta_t_corr = delta_t * (DELTA_T_REF_C/delta_eb)
    return delta_t_corr


# /--- Resultado completo de una fase (columnas de resultado_fase) ---/
# Función 21
def calcular_resultado_fase(
        fase, 
        ollas_fase, 
        combustible,
        condiciones_ambientales,
        peso_recipiente_carbon_kg,
        cambio_carbon_frio_kg = None
    ):

    tipo_fase = fase['tipo_fase']
    if tipo_fase not in TIPOS_FASE:
        raise ValueError(f'tipo_fase invalido: {tipo_fase!r}. Debe ser {TIPOS_FASE}')

    ollas_fase = _ollas_con_datos(ollas_fase)
    if not any(olla.get('numero_olla') == 1 for olla in ollas_fase):
        raise ValueError('La fase requiere la olla 1')

    pto_eb = condiciones_ambientales['punto_ebullicion_c']
    t_aire = condiciones_ambientales['temperatura_c']
    pcn_mj_kg = poder_calorifico_neto_mj_kg(combustible.get('poder_calorifico_neto_mj_kg'), combustible.get('poder_calorifico_bruto_mj_kg'))

    masa_inicial = sum(
        masa_agua_kg(o['peso_con_agua_inicial_kg'], o['peso_seco_kg'])
        for o in ollas_fase
    )

    masa_final = sum(
        masa_agua_kg(o['peso_con_agua_final_kg'], o['peso_seco_kg'])
        for o in ollas_fase
    )

    evaporada = masa_agua_evaporada_kg(ollas_fase)
    efectiva = masa_agua_efectiva_kg(ollas_fase,pto_eb, tipo_fase)

    t_min = tiempo_fase_min(fase['t_inicial'],fase['t_final'])
    t_corr_min = tiempo_ebullicion_corregido_min(fase['t_inicial'], fase['t_final'], pto_eb, ollas_fase, tipo_fase)
    f_cons = combustible_consumido_kg(fase['peso_combustible_inicial_kg'],fase['peso_combustible_final_kg'])

    delta_carbon = cambio_carbon_kg(
        tipo_fase, 
        fase.get('peso_carbon_con_recipiente_kg'),
        peso_recipiente_carbon_kg,
        cambio_carbon_frio_kg
    )

    seco_eq = combustible_seco_equivalente_kg(
        fase['peso_combustible_inicial_kg'],
        fase['peso_combustible_final_kg'],
        combustible['humedad_pct'],
        pcn_mj_kg,
        combustible['poder_calorifico_carbon_mj_kg'],
        peso_recipiente_carbon_kg,
        fase.get('peso_carbon_con_recipiente_kg'),
        t_aire,
        pto_eb,
        tipo_fase,
        cambio_carbon_frio_kg
    )

    q_util = energia_util_kj(
        ollas_fase,
        pto_eb,
        tipo_fase
    )

    q_combustible = energia_combustible_kj(seco_eq, pcn_mj_kg)
    ef_termica = eficiencia_termica_pct(q_util, q_combustible)
    sc = consumo_especifico_g_l(seco_eq, efectiva)
    sc_corr = consumo_especifico_corregido_g_l(
        ollas_fase, 
        tipo_fase, 
        pto_eb, 
        sc
    )

    consumo_para_energia = sc if tipo_fase == 'baja_potencia' else sc_corr

    v_comb = velocidad_combustion_g_min(
        seco_eq, 
        fase['t_inicial'],
        fase['t_final']
    )

    p_fase = potencia_fase_kw(
        seco_eq, 
        pcn_mj_kg, 
        fase['t_inicial'], 
        fase['t_final']
    )

    return {
        'tiempo_fase_min': t_min,
        'tiempo_ebullicion_min': (None if tipo_fase == 'baja_potencia' else t_min),
        'tiempo_ebullicion_corregido_min': t_corr_min,
        'masa_agua_inicial_kg': masa_inicial,
        'masa_agua_final_kg': masa_final,
        'masa_agua_evaporada_kg': evaporada,
        'masa_agua_efectiva_kg': efectiva,
        'combustible_consumido_kg': f_cons,
        'cambio_carbon_kg': delta_carbon,
        'combustible_seco_equivalente_kg': seco_eq,
        'energia_util_kj': q_util,
        'energia_combustible_kj': q_combustible,
        'eficiencia_termica_pct': ef_termica,
        'consumo_especifico_g_l': sc,
        'consumo_especifico_corregido_g_l':sc_corr,
        'energia_especifica_corregida_kj_l':(
            energia_especifica_corregida_kj_l(consumo_para_energia,pcn_mj_kg)
            if consumo_para_energia is not None else None
        ),
        'velocidad_combustion_g_min': v_comb,
        'potencia_fase_kw': p_fase
    }