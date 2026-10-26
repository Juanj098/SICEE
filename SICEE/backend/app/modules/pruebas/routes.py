from flask import request
from . import bp, services

def _a_dict(obj):
    return{
        columna.name: getattr(obj, columna.name)
        for columna in obj.__table__.columns
    }

# /---Cond_Ambientales---/
@bp.get('/condiciones_ambientales')
def list_condiciones_ambientales():
    return [_a_dict(c_a) for c_a in services.list_condicion_ambiental()]

@bp.post('/condiciones_ambientales')
def crear_condiciones_ambientales():
    datos = request.get_json(silent=True) or {}
    temperatura = float(datos.get('temperatura') or 0.00) 
    humedad = float(datos.get('humedad_pct') or 0.00)
    presion_atm = float(datos.get('presion_atm') or 0.00) 
    viento = float(datos.get('viento') or {}) 
    pto_ebullicion = float(datos.get('pto_ebullicion') or 0.00)
    condiciones_ambientales = services.crear_condicion_ambiental(pto_ebullicion, temperatura, humedad, presion_atm, viento)
    return _a_dict(condiciones_ambientales), 201

