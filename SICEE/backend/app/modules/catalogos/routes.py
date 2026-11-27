from decimal import Decimal

from flask import request
from . import bp, services
from .models import Combustibles, EspecieMadera, Estufas, Laboratorio


def _json_value(valor):
    return float(valor) if isinstance(valor, Decimal) else valor


def _a_dict(obj):
    return {
        columna.name: _json_value(getattr(obj, columna.name))
        for columna in obj.__table__.columns
    }


def _numero_opcional(datos, campo, defecto=None):
    valor = datos.get(campo)
    if valor in (None, ''):
        return defecto
    return float(valor)

# /---Combustibles---/
def _combustible_a_dict(combustible):
    referencia = combustible.especie
    return {
        **_a_dict(combustible),
        'especie': referencia.especie if referencia else None,
        'fuente': referencia.fuente if referencia else None,
    }


@bp.get("/combustible")
def listCombustible():
    return [_combustible_a_dict(c) for c in services.listar_combustible()]

@bp.get("/combustible/activos")
def listCombustiblesActivos():
    return [_combustible_a_dict(c) for c in services.listar_combustibles_activos()]

@bp.post("/combustible")
def newCombustible():
    datos = request.get_json(silent=True) or {}
    tipo = (datos.get('tipo') or '').strip()
    if not tipo:
        return {'error': 'El tipo de combustible es obligatorio'}, 400
    try:
        especie_id = datos.get('especie_id')
        if especie_id in (None, ''):
            especie_id = None
        elif isinstance(especie_id, bool) or not str(especie_id).isdecimal():
            raise ValueError('especie_id debe ser un entero')
        else:
            especie_id = int(especie_id)
        defecto = 0 if especie_id is None else None
        longitud_combustible_cm = float(datos.get('longitud_combustible_cm') or 0.00)
        ancho_combustible_cm = float(datos.get('ancho_combustible_cm') or 0.00)
        poder_calorifico_neto_mj_kg = _numero_opcional(datos, 'poder_calorifico_neto_mj_kg', defecto)
        poder_calorifico_bruto_mj_kg = _numero_opcional(datos, 'poder_calorifico_bruto_mj_kg', defecto)
        poder_calorifico_carbon_mj_kg = _numero_opcional(datos, 'poder_calorifico_carbon_mj_kg', defecto)
        contenido_carbono_carbon_pct = float(datos.get('contenido_carbono_carbon_pct') or 0.00)
        contenido_carbono_pct = _numero_opcional(datos, 'contenido_carbono_pct', defecto)
        tipo_alimentacion = (datos.get('tipo_alimentacion') or '').strip()
        descripcion = (datos.get('descripcion') or '').strip()
    except (TypeError, ValueError) as exc:
        return {'error': f'Datos inválidos: {exc}'}, 400
    try:
        combustible = services.crear_combustible(
            tipo,
            longitud_combustible_cm,
            ancho_combustible_cm,
            poder_calorifico_neto_mj_kg,
            poder_calorifico_bruto_mj_kg,
            poder_calorifico_carbon_mj_kg,
            tipo_alimentacion,
            contenido_carbono_pct,
            contenido_carbono_carbon_pct,
            descripcion,
            especie_id
        )
    except ValueError as exc:
        return {'error': str(exc)}, 400
    return _combustible_a_dict(combustible), 201

# /---Especies de madera---/
@bp.get('/especies')
def listEspecies():
    return [_a_dict(e) for e in services.listar_especies_todas()]


@bp.get('/especies/activos')
def listEspeciesActivas():
    return [_a_dict(e) for e in services.listar_especies()]


@bp.post('/especies')
def newEspecie():
    datos = request.get_json(silent=True) or {}
    especie = (datos.get('especie') or '').strip()
    if not especie:
        return {'error': 'El nombre de la especie es obligatorio'}, 400

    try:
        fuente_codigo = datos.get('fuente_codigo')
        fuente_codigo = (
            None if fuente_codigo in (None, '') else int(fuente_codigo)
        )
        creada = services.crear_especie(
            especie,
            nombres_comunes=(datos.get('nombres_comunes') or '').strip() or None,
            poder_calorifico_bruto_mj_kg=_numero_opcional(
                datos, 'poder_calorifico_bruto_mj_kg'
            ),
            poder_calorifico_neto_mj_kg=_numero_opcional(
                datos, 'poder_calorifico_neto_mj_kg'
            ),
            poder_calorifico_carbon_mj_kg=_numero_opcional(
                datos, 'poder_calorifico_carbon_mj_kg'
            ),
            contenido_carbono_pct=_numero_opcional(
                datos, 'contenido_carbono_pct'
            ),
            fuente_codigo=fuente_codigo,
            fuente=(datos.get('fuente') or '').strip() or None,
        )
    except (TypeError, ValueError) as exc:
        return {'error': f'Datos inválidos: {exc}'}, 400

    return _a_dict(creada), 201

# /------Estufa------/
@bp.get('/estufas')
def listEstufas():
    return [_a_dict(e) for e in services.listar_estufas()]


@bp.post('/estufas')
def newEstufa():
    datos = request.get_json(silent=True) or {}

    marca = (datos.get('marca') or '').strip()
    fabricante = (datos.get('fabricante') or '').strip()
    if not marca or not fabricante:
        return {'error': 'faltan datos (marca o fabricante)'}, 400
    try:
        area_camara_cm2 = float(datos.get('area_camara_cm2') or 0.00)
        altura_cm = float(datos.get('altura_cm') or 0.00)
        numero_hornillas = int(datos.get('numero_hornillas') or 0)
    except (TypeError, ValueError) as exc:
        return {'error': f'Datos inválidos: {exc}'}, 400
    material = (datos.get('material') or '').strip()
    descripcion = (datos.get('descripcion') or '').strip()
    estufa = services.newEstufa(
        marca,
        fabricante,
        area_camara_cm2,
        altura_cm,
        numero_hornillas,
        material,
        descripcion,
    )
    return _a_dict(estufa), 201

# /-------Labs-------/
@bp.get('/labs')
def listLabs():
    return [_a_dict(l) for l in services.listar_labs()]

@bp.post('/labs')
def newLabs():
    datos = request.get_json(silent=True) or {}
    institucion = (datos.get('institucion') or '').strip()
    direccion = (datos.get('direccion') or '').strip()
    descripcion = (datos.get('descripcion') or '').strip()
    if not institucion:
        return {'error':'falta nombre institucion'}
    lab = services.newLab(institucion, direccion, descripcion)
    return _a_dict(lab), 201

# /-------Baja lógica-------/
def _activo_del_cuerpo():
    datos = request.get_json(silent=True) or {}
    activo = datos.get('activo')
    return activo if isinstance(activo, bool) else None


@bp.patch('/combustible/<int:id>')
def updateCombustible(id):
    activo = _activo_del_cuerpo()
    if activo is None:
        return {'error': 'El campo activo debe ser booleano'}, 400
    if not services.cambiar_activo(Combustibles, id, activo):
        return {'error': 'Combustible no encontrado'}, 404
    return {'msg': 'Combustible actualizado'}, 200


@bp.patch('/especies/<int:id>')
def updateEspecie(id):
    activo = _activo_del_cuerpo()
    if activo is None:
        return {'error': 'El campo activo debe ser booleano'}, 400
    if not services.cambiar_activo(EspecieMadera, id, activo):
        return {'error': 'Especie no encontrada'}, 404
    return {'msg': 'Especie actualizada'}, 200


@bp.patch('/estufas/<int:id>')
def updateEstufa(id):
    activo = _activo_del_cuerpo()
    if activo is None:
        return {'error': 'El campo activo debe ser booleano'}, 400
    if not services.cambiar_activo(Estufas, id, activo):
        return {'error': 'Estufa no encontrada'}, 404
    return {'msg': 'Estufa actualizada'}, 200


@bp.patch('/labs/<int:id>')
def updateLab(id):
    activo = _activo_del_cuerpo()
    if activo is None:
        return {'error': 'El campo activo debe ser booleano'}, 400
    if not services.cambiar_activo(Laboratorio, id, activo):
        return {'error': 'Laboratorio no encontrado'}, 404
    return {'msg': 'Laboratorio actualizado'}, 200
