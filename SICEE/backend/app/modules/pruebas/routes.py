from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from uuid import UUID

from flask import current_app, request

from app.extensions import db
from app.modules.calculos import services as calculos_services
from . import bp, services
from .constants import TIPOS_FASE


# ------------------------------------------------------------
# Utilidades de serialización y conversión
# ------------------------------------------------------------
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

def _entero(valor, campo):
    if valor is None or valor == '':
        raise ValueError(f'El campo {campo} es obligatorio')
    try:
        return int(valor)
    except (TypeError, ValueError):
        raise ValueError(f'{campo} debe ser un número entero')

def _entero_opcional(valor, campo):
    if valor is None or valor == '':
        return None
    return _entero(valor, campo)

def _texto_opcional(valor):
    if valor is None:
        return None
    texto = str(valor).strip()
    return texto or None

def _booleano(valor, campo, por_defecto=None):
    if valor is None or valor == '':
        return por_defecto
    if isinstance(valor, bool):
        return valor
    if isinstance(valor, int) and valor in (0, 1):
        return bool(valor)
    if isinstance(valor, str):
        normalizado = valor.strip().lower()
        if normalizado in ('true', '1', 'si', 'sí'):
            return True
        if normalizado in ('false', '0', 'no'):
            return False
    raise ValueError(f'{campo} debe ser verdadero o falso')

def _fecha(valor, campo):
    if valor is None or valor == '':
        return None
    if isinstance(valor, datetime):
        return valor
    try:
        return datetime.fromisoformat(str(valor))
    except (TypeError, ValueError):
        raise ValueError(f'{campo} debe tener formato ISO 8601')


# ------------------------------------------------------------
# condiciones_ambientales
# ------------------------------------------------------------
@bp.get('/condiciones_ambientales')
def list_condiciones_ambientales():
    return [_a_dict(c_a) for c_a in services.list_condicion_ambiental()]

@bp.post('/condiciones_ambientales')
def crear_condiciones_ambientales():
    datos = request.get_json(silent=True) or {}
    try:
        condiciones_ambientales = services.crear_condicion_ambiental(
            temperatura_c=_decimal_opcional(datos.get('temperatura_c'), 'temperatura_c'),
            humedad_relativa_pct=_decimal_opcional(datos.get('humedad_relativa_pct'), 'humedad_relativa_pct'),
            altitud_m=_decimal_opcional(datos.get('altitud_m'), 'altitud_m'),
            presion_atmosferica_kpa=_decimal_opcional(datos.get('presion_atmosferica_kpa'), 'presion_atmosferica_kpa',),
            viento_ms=_decimal_opcional(datos.get('viento_ms'), 'viento_ms'),
            condicion_viento=_texto_opcional(datos.get('condicion_viento')),
            punto_ebullicion_c=_decimal_opcional(datos.get('punto_ebullicion_c'), 'punto_ebullicion_c'),
        )
    except (TypeError, ValueError) as exc:
        return {'error': f'Datos inválidos: {exc}'}, 400

    return _a_dict(condiciones_ambientales), 201


# ------------------------------------------------------------
# conjunto_pruebas
# ------------------------------------------------------------
@bp.get('/conjunto_pruebas')
def list_conjuntos_pruebas():
    return [_a_dict(c) for c in services.list_conjuntos_pruebas()]

@bp.post('/conjunto_pruebas')
def crear_conjunto_pruebas():
    datos = request.get_json(silent=True) or {}
    try:
        conjunto = services.crear_conjunto_pruebas(
            estufa_id=_entero(datos.get('estufa_id'), 'estufa_id'),
            descripcion=_texto_opcional(datos.get('descripcion')),
        )
    except (TypeError, ValueError) as exc:
        return {'error': f'Datos inválidos: {exc}'}, 400

    return _a_dict(conjunto), 201


# ------------------------------------------------------------
# prueba_wbt
# ------------------------------------------------------------
@bp.get('/pruebas_wbt')
def list_pruebas_wbt():
    return [_a_dict(wbt) for wbt in services.list_pruebas_wbt()]

@bp.post('/pruebas_wbt')
def registrar_prueba_wbt():
    datos = request.get_json(silent=True) or {}
    try:
        numero_repeticion = _entero_opcional(datos.get('numero_repeticion'), 'numero_repeticion')
        if numero_repeticion is None:
            numero_repeticion = 1

        prueba = services.registrar_Prueba_wbt(
            fecha=_fecha(datos.get('fecha'), 'fecha') or datetime.now(),
            investigador_id=_entero(datos.get('investigador_id'), 'investigador_id'),
            laboratorio_id=_entero(datos.get('laboratorio_id'), 'laboratorio_id'),
            combustible_id=_entero(datos.get('combustible_id'), 'combustible_id'),
            condiciones_amb_id=_entero(datos.get('condiciones_ambientales_id'),'condiciones_ambientales_id',),
            conjunto_pruebas_id=_entero(datos.get('conjunto_pruebas_id'), 'conjunto_pruebas_id'),
            peso_recipiente_carbon_kg=_decimal_opcional(datos.get('peso_recipiente_carbon_kg'), 'peso_recipiente_carbon_kg'),
            numero_repeticion=numero_repeticion,
            es_valida=_booleano(datos.get('es_valida'), 'es_valida', True),
            motivo_invalidez=_texto_opcional(datos.get('motivo_invalidez')),
            version_protocolo=(_texto_opcional(datos.get('version_protocolo')) or '4.2.3'),
            observaciones=_texto_opcional(datos.get('observaciones')),
        )
    except (TypeError, ValueError) as exc:
        return {'error': f'Datos inválidos: {exc}'}, 400

    return _a_dict(prueba), 201


# ------------------------------------------------------------
# fase_prueba
# ------------------------------------------------------------
@bp.get('/Fase_Prueba')
def list_fases():
    return [_a_dict(f) for f in services.list_fases_prueba()]

@bp.post('/Fase_Prueba')
def registrar_fase_prueba():
    datos = request.get_json(silent=True) or {}
    try:
        tipo_fase = (_texto_opcional(datos.get('tipo_fase')) or '').lower()
        if tipo_fase not in TIPOS_FASE:
            raise ValueError(
                'tipo_fase debe ser inicio_frio, inicio_caliente '
                'o baja_potencia'
            )

        t_inicial = _fecha(datos.get('t_inicial'), 't_inicial')
        t_final = _fecha(datos.get('t_final'), 't_final')
        if t_inicial and t_final and t_final < t_inicial:
            raise ValueError('t_final no puede ser anterior a t_inicial')

        fase = services.crear_fase_prueba(
            prueba_wbt_id=_entero(datos.get('prueba_wbt_id'), 'prueba_wbt_id'),
            tipo_fase=tipo_fase,
            t_inicial=t_inicial,
            t_final=t_final,
            peso_combustible_inicial_kg=_decimal_opcional(datos.get('peso_combustible_inicial_kg'), 'peso_combustible_inicial_kg'),
            peso_combustible_final_kg=_decimal_opcional(datos.get('peso_combustible_final_kg'),'peso_combustible_final_kg'),
            peso_carbon_con_recipiente_kg=_decimal_opcional(datos.get('peso_carbon_con_recipiente_kg'),'peso_carbon_con_recipiente_kg'),
            peso_cenizas_kg=_decimal_opcional(datos.get('peso_cenizas_kg'), 'peso_cenizas_kg'),
            observaciones=_texto_opcional(datos.get('observaciones')),
        )
    except (TypeError, ValueError) as exc:
        return {'error': f'Datos inválidos: {exc}'}, 400

    return _a_dict(fase), 201


# ------------------------------------------------------------
# olla
# ------------------------------------------------------------
@bp.get('/ollas')
def list_ollas():
    return [_a_dict(o) for o in services.list_ollas()]

@bp.post('/ollas')
def crear_olla():
    datos = request.get_json(silent=True) or {}
    try:
        numero_olla = _entero(datos.get('numero_olla'), 'numero_olla')
        if numero_olla < 1:
            raise ValueError('numero_olla debe ser mayor o igual a 1')

        olla = services.crear_olla(
            prueba_wbt_id=_entero(datos.get('prueba_wbt_id'), 'prueba_wbt_id'),
            numero_olla=numero_olla,
            peso_seco_kg=_decimal_opcional(datos.get('peso_seco_kg'), 'peso_seco_kg'),
            capacidad_l=_decimal_opcional(datos.get('capacidad_l'), 'capacidad_l'),
        )
    except (TypeError, ValueError) as exc:
        return {'error': f'Datos inválidos: {exc}'}, 400

    return _a_dict(olla), 201


# ------------------------------------------------------------
# olla_fase
# ------------------------------------------------------------
@bp.get('/olla_fase')
def list_ollas_fase():
    return [_a_dict(o_f) for o_f in services.list_ollas_fase()]

@bp.post('/olla_fase')
def crear_olla_fase():
    datos = request.get_json(silent=True) or {}
    try:
        olla_fase = services.crear_olla_fase(
            olla_id=_entero(datos.get('olla_id'), 'olla_id'),
            fase_id=_entero(datos.get('fase_id'), 'fase_id'),
            temperatura_inicial_agua_c=_decimal_opcional(datos.get('temperatura_inicial_agua_c'), 'temperatura_inicial_agua_c'),
            temperatura_final_agua_c=_decimal_opcional(datos.get('temperatura_final_agua_c'), 'temperatura_final_agua_c'),
            peso_con_agua_inicial_kg=_decimal_opcional(datos.get('peso_con_agua_inicial_kg'), 'peso_con_agua_inicial_kg'),
            peso_con_agua_final_kg=_decimal_opcional(datos.get('peso_con_agua_final_kg'), 'peso_con_agua_final_kg'),
        )
    except (TypeError, ValueError) as exc:
        return {'error': f'Datos inválidos: {exc}'}, 400

    return _a_dict(olla_fase), 201


# ------------------------------------------------------------
# mediciones_opcionales
# ------------------------------------------------------------
@bp.get('/mediciones_opcionales')
def list_mediciones_opcionales():
    return [
        _a_dict(medicion)
        for medicion in services.listar_mediciones_opcionales()
    ]

@bp.post('/mediciones_opcionales')
def crear_medicion_opcional():
    datos = request.get_json(silent=True) or {}
    try:
        medicion = services.registrar_mediciones_ops(
            fase_id=_entero(datos.get('fase_id'), 'fase_id'),
            temperatura_ducto_c=_decimal_opcional(datos.get('temperatura_ducto_c'), 'temperatura_ducto_c'),
            co_ppm=_decimal_opcional(datos.get('co_ppm'), 'co_ppm'),
            pm_ug_m3=_decimal_opcional(datos.get('pm_ug_m3'), 'pm_ug_m3'),
            co2_ppm=_decimal_opcional(datos.get('co2_ppm'), 'co2_ppm'),
            co2_fondo_ppm=_decimal_opcional(datos.get('co2_fondo_ppm'), 'co2_fondo_ppm'),
            co_fondo_ppm=_decimal_opcional(datos.get('co_fondo_ppm'), 'co_fondo_ppm'),
            pm_fondo_ug_m3=_decimal_opcional(datos.get('pm_fondo_ug_m3'), 'pm_fondo_ug_m3'),
            co2_total_g=_decimal_opcional(datos.get('co2_total_g'), 'co2_total_g'),
            co_total_g=_decimal_opcional(datos.get('co_total_g'), 'co_total_g'),
            pm_total_g=_decimal_opcional(datos.get('pm_total_g'), 'pm_total_g'),
        )
    except (TypeError, ValueError) as exc:
        return {'error': f'Datos inválidos: {exc}'}, 400

    return _a_dict(medicion), 201


# ------------------------------------------------------------
# muestra_humedad
# La humedad se mide en cada prueba: 3 leños × 3 mediciones.
# ------------------------------------------------------------
@bp.get('/muestras_humedad')
def list_muestras_humedad():
    try:
        prueba_wbt_id = _entero_opcional(
            request.args.get('prueba_wbt_id'), 'prueba_wbt_id'
        )
    except (TypeError, ValueError) as exc:
        return {'error': f'Datos inválidos: {exc}'}, 400

    return [
        _a_dict(muestra)
        for muestra in services.list_muestras_humedad(prueba_wbt_id)
    ]


@bp.post('/muestras_humedad')
def crear_muestras_humedad():
    """Reemplaza las mediciones de humedad de una prueba.

    Cuerpo: { "prueba_wbt_id": 1, "muestras": [
        { "numero_lenio": 1, "numero_medicion": 1, "humedad_pct": 8.1 }, ...
    ] }
    """
    datos = request.get_json(silent=True) or {}
    try:
        prueba_wbt_id = _entero(datos.get('prueba_wbt_id'), 'prueba_wbt_id')
        crudas = datos.get('muestras')
        if not isinstance(crudas, list) or not crudas:
            raise ValueError('muestras debe ser una lista con al menos una medición')

        muestras = []
        for cruda in crudas:
            if not isinstance(cruda, dict):
                raise ValueError('Cada muestra debe ser un objeto')
            humedad = _decimal_opcional(cruda.get('humedad_pct'), 'humedad_pct')
            if humedad is None:
                raise ValueError('humedad_pct es obligatorio en cada muestra')
            if humedad < 0 or humedad > 100:
                raise ValueError('humedad_pct debe estar entre 0 y 100')
            muestras.append({
                'numero_lenio': _entero(cruda.get('numero_lenio'), 'numero_lenio'),
                'numero_medicion': _entero(cruda.get('numero_medicion'), 'numero_medicion'),
                'humedad_pct': humedad,
            })

        filas = services.reemplazar_muestras_humedad(prueba_wbt_id, muestras)
    except (TypeError, ValueError) as exc:
        return {'error': f'Datos inválidos: {exc}'}, 400

    return {
        'prueba_wbt_id': prueba_wbt_id,
        'promedio_humedad_pct': services.promedio_humedad(prueba_wbt_id),
        'muestras': [_a_dict(muestra) for muestra in filas],
    }, 201


# ------------------------------------------------------------
# prueba completa (transacción única)
# ------------------------------------------------------------
@bp.post('/completa')
def crear_prueba_wbt_completa():
    datos = request.get_json(silent=True) or {}
    try:
        prueba = services.crear_prueba_completa(datos)
    except (TypeError, ValueError) as exc:
        return {'error': f'Datos inválidos: {exc}'}, 400

    # La prueba ya está guardada. Los resultados se escriben en resultado_fase
    # en su propia transacción: si el cálculo falla, la prueba no se pierde.
    resultados = None
    resultado_prueba = None
    error_calculo = None
    try:
        resultados = calculos_services.guardar_resultados(prueba.id)
        resultado_prueba = calculos_services.guardar_resultado_prueba(prueba.id)
    except (TypeError, ValueError) as exc:
        db.session.rollback()
        error_calculo = str(exc)
    except Exception:
        db.session.rollback()
        current_app.logger.exception(
            'Error inesperado al calcular la prueba %s', prueba.id
        )
        error_calculo = 'Error inesperado al calcular los resultados'

    return {
        'id': prueba.id,
        'uuid': str(prueba.uuid),
        'promedio_humedad_pct': services.promedio_humedad(prueba.id),
        'muestras': len(prueba.muestra_humedad),
        'ollas': len(prueba.olla),
        'fases': len(prueba.fase_prueba),
        'resultados': resultados,
        'resultado_prueba': resultado_prueba,
        'numero_repeticion': prueba.numero_repeticion,
        'conjunto_pruebas_id': prueba.conjunto_pruebas_id,
        'es_valida': prueba.es_valida,
        'motivo_invalidez': prueba.motivo_invalidez,
        'error_calculo': error_calculo,
    }, 201
