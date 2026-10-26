from flask import request
from . import bp, services

def _a_dict(obj):
    return {
        columna.name: getattr(obj, columna.name)
        for columna in obj.__table__.columns
    }

# /---Combustibles---/
@bp.get("/combustible")
def listCombustible():
    return [_a_dict(c) for c in services.listar_combustible()]

@bp.post("/combustible")
def newCombustible():
    datos = request.get_json(silent=True) or {}
    tipo = (datos.get('tipo') or '').strip()
    tamanio_cm = float(datos.get('tamanio_cm'))
    peso_kg = float(datos.get('peso_kg') or 0.00)
    humedad_pct = float(datos.get('humedad_pct') or 0.00)
    poder_calorifico_neto_mj_kg = float(datos.get('poder_calorifico_neto_mj_kg') or 0.00)
    poder_calorifico_bruto_mj_kg = float(datos.get('poder_calorifico_bruto_mj_kg') or 0.00)
    tipo_alimentacion = (datos.get('tipo_alimentacion') or '').strip()
    contenido_carbono_pct = float(datos.get('contenido_carbono_pct') or 0.00)
    if not tipo:
        return {'error':'El tipo de combustible es obligatorio'}, 400
    combustible = services.crear_combustible(tipo, tamanio_cm, peso_kg, humedad_pct, poder_calorifico_neto_mj_kg, poder_calorifico_bruto_mj_kg, tipo_alimentacion, contenido_carbono_pct)
    return _a_dict(combustible), 201

# /------Estufa------/
@bp.get('/estufas')
def listEstufas():
    return [_a_dict(e) for e in services.listar_estufas()]


@bp.post('/estufas')
def newEstufa():
    datos = request.get_json(silent=True) or {}
    marca = (datos.get('marca')).strip()
    fabricante = (datos.get('fabricante') or "").strip()
    area_camara_cm2 = float(datos.get('area_camara_cm2') or 0.00)
    altura_cm = float(datos.get('altura_cm') or 0.00)
    material = (datos.get('material') or '').strip()
    descripcion = (datos.get('descripcion') or '').strip()
    if  marca == '' or fabricante == '':
        return {'error': 'faltan datos (marca ó fabricanteS)'} 
    estufa = services.newEstufa(marca, fabricante, area_camara_cm2, altura_cm, material, descripcion)
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