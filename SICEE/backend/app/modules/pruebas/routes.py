from flask import request
from . import bp, services
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from uuid import UUID


def _json_value(valor):
    if isinstance(valor, Decimal):
        return float(valor)
    if isinstance(valor, (datetime, date)):
        return valor.isoformat()
    if isinstance(valor, UUID):
        return str(valor)
    return valor


def _a_dict(obj):
    return {
        columna.name: _json_value(getattr(obj, columna.name))
        for columna in obj.__table__.columns
    }


def _decimal_opcional(valor, campo):
    if valor is None or valor == '':
        return None
    try:
        return Decimal(str(valor))
    except (InvalidOperation, ValueError, TypeError):
        raise ValueError(f'{campo} debe ser un número')

# /---Cond_Ambientales---/
@bp.get('/condiciones_ambientales')
def list_condiciones_ambientales():
    return [_a_dict(c_a) for c_a in services.list_condicion_ambiental()]

@bp.post('/condiciones_ambientales')
def crear_condiciones_ambientales():
    datos = request.get_json(silent=True) or {}
    try:
        condiciones_ambientales = services.crear_condicion_ambiental(
            temperatura_c=(
                float(datos['temperatura_c'])
                if datos.get('temperatura_c') is not None
                else None
            ),
            humedad_relativa_pct=(
                float(datos['humedad_relativa_pct'])
                if datos.get('humedad_relativa_pct') is not None
                else None
            ),
            presion_atmosferica_kpa=(
                float(datos['presion_atmosferica_kpa'])
                if datos.get('presion_atmosferica_kpa') is not None
                else None
            ),
            viento_ms=(
                float(datos['viento_ms'])
                if datos.get('viento_ms') is not None
                else None
            ),
            punto_ebullicion_c=(
                float(datos['punto_ebullicion_c'])
                if datos.get('punto_ebullicion_c') is not None
                else None
            ),
        )
    except (TypeError, ValueError) as exc:
        return {'error': f'Datos inválidos: {exc}'}, 400

    return _a_dict(condiciones_ambientales), 201

# /---Prueba_WBT---/
@bp.get('/pruebas_wbt')
def list_pruebas_wbt():
    return [_a_dict(wbt) for wbt in services.list_pruebas_wbt()]

@bp.post('/pruebas_wbt')
def registrar_prueba_wbt():
    datos = request.get_json(silent = True) or {}
    try:
        investigador_id = int(datos['investigador_id'])
        laboratorio_id = int(datos['laboratorio_id'])
        estufa_id = int(datos['estufa_id'])
        combustible_id = int(datos['combustible_id'])
        condiciones_ambientales_id = int(datos['condiciones_ambientales_id'])
    except KeyError as exc:
        return {
            'error':f'Falta campo obligatorio: {exc.args[0]}'
        }, 400
    except (TypeError, ValueError) as exc:
        return {
            'error': f'Datos Invalidos: {exc}'
        }, 400
    observaciones = (datos.get('observaciones') or '').strip()
    fecha = datetime.now()

    prueba = services.registrar_Prueba_wbt(
        fecha,
        investigador_id,
        laboratorio_id,
        estufa_id,
        combustible_id,
        condiciones_ambientales_id,
        observaciones
    )
    return _a_dict(prueba), 201

# /--- Fase_Prueba ---/
@bp.get('/Fase_Prueba')
def list_fases():
    return [_a_dict(f) for f in services.list_fases_prueba()]

@bp.post('/Fase_Prueba')
def registrar_fase_prueba():
    datos = request.get_json(silent = True) or {}
    try:
        prueba_wbt_id = int(datos['prueba_wbt_id'])
        numero_repeticion = int(datos['numero_repeticion'])
        tipo_fase = (datos.get('tipo_fase') or '').strip()
        if not tipo_fase:
            return {'error':'El tipo de fase es obligatorio'}, 400
        t_inicial = datetime.fromisoformat(datos['t_inicial'])
        t_final = (
            datetime.fromisoformat(datos['t_final'])
            if datos.get('t_final')
            else None
        )
        if t_final is not None and t_final < t_inicial:
            return {
                'error':'t_final no puede ser anterior a t_inicial'
            }, 400
        temp_inicial_agua_c = _decimal_opcional(
            datos.get('temperatura_inicial_agua_c'),
            'temperatura_inicial_agua_c'
        )
        temp_final_agua_c = _decimal_opcional(
            datos.get('temperatura_final_agua_c'),
            'temperatura_final_agua_c'
        )
        peso_olla_seca_kg = _decimal_opcional(
            datos.get('peso_olla_seco_kg'),
            'peso_olla_seco_kg'
        )
        peso_olla_agua_incial_kg = _decimal_opcional(
            datos.get('peso_olla_agua_inicial_kg'),
            'peso_olla_agua_inicial_kg'
        )
        peso_olla_agua_final_kg = _decimal_opcional(
            datos.get('peso_olla_agua_final_kg'),
            'peso_olla_agua_final_kg'
        )
        peso_combustible_inicial_kg = _decimal_opcional(
            datos.get('peso_combustible_inicial_kg'),
            'peso_combustible_inicial_kg',
        )
        peso_combustible_final_kg = _decimal_opcional(
            datos.get('peso_combustible_final_kg'),
            'peso_combustible_final_kg',
        )

        fase = services.crear_fase_prueba(
            prueba_wbt_id=prueba_wbt_id,
            tipo_fase=tipo_fase,
            numero_repeticion=numero_repeticion,
            t_inicial=t_inicial,
            t_final=t_final,
            temperatura_inicial_agua_c=temp_inicial_agua_c,
            temperatura_final_agua_c=temp_final_agua_c,
            peso_olla_seco_kg=peso_olla_seca_kg,
            peso_olla_agua_inicial_kg=peso_olla_agua_incial_kg,
            peso_olla_agua_final_kg=peso_olla_agua_final_kg,
            peso_combustible_inicial_kg=peso_combustible_inicial_kg,
            peso_combustible_final_kg=peso_combustible_final_kg,
        )
    except KeyError as exc:
        return {'error':f'falta el campo obligatorio: {exc.args[0]}'}, 400
    except (TypeError, ValueError) as exc:
        return {'error':f'Datos inválidos: {exc}'}, 400
    return _a_dict(fase), 201


# /--- Mediciones_Opcionales ---/
@bp.get('/mediciones_opcionales')
def list_mediciones_opcionales():
    return [ _a_dict(medicion) for medicion in services.listar_mediciones_opcionales()]

@bp.post('/mediciones_opcionales')
def crear_medicion_opcional():
    datos = request.get_json(silent=True) or {}

    try:
        fase_id = int(datos['fase_id'])

        co_ppm = _decimal_opcional(
            datos.get('co_ppm'),
            'co_ppm',
        )
        pm_mg_m3 = _decimal_opcional(
            datos.get('pm_mg_m3'),
            'pm_mg_m3',
        )
        co2_ppm = _decimal_opcional(
            datos.get('co2_ppm'),
            'co2_ppm',
        )
        temperatura_ducto_c = _decimal_opcional(
            datos.get('temperatura_ducto_c'),
            'temperatura_ducto_c',
        )
        presion_atmosferica_kpa = _decimal_opcional(
            datos.get('presion_atmosferica_kpa'),
            'presion_atmosferica_kpa',
        )

        medicion = services.registrar_mediciones_ops(
            fase_id=fase_id,
            co_ppm=co_ppm,
            pm_mg_m3=pm_mg_m3,
            co2_ppm=co2_ppm,
            temperatura_ducto_c=temperatura_ducto_c,
            presion_atmosferica_kpa=presion_atmosferica_kpa,
        )
    except KeyError as exc:
        return {
            'error': f'Falta el campo obligatorio: {exc.args[0]}'
        }, 400
    except (TypeError, ValueError) as exc:
        return {'error': f'Datos inválidos: {exc}'}, 400

    return _a_dict(medicion), 201