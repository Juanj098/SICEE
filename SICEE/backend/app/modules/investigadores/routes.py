from flask import request
from . import ibp, services

def _a_dict(investigador):
    return {"id":investigador.id, "nombre": investigador.nombre}

@ibp.get("")
def listar():
    return [_a_dict(i) for i in services.listar()]

@ibp.post("/")
def crear():
    datos = request.get_json(silent=True) or {}
    nombre = (datos.get("nombre") or "").strip()
    if not nombre:
        return {"error":"El nombre es obligatorio"}, 400
    investigador = services.newInvestigador(nombre)
    return _a_dict(investigador), 201

@ibp.get("/<int:id>")
def getName(id):
    investigador = services.obtener_por_id(id)
    if investigador is None:
        return {"error":"investigador no encontrado"}
    return _a_dict(investigador)

@ibp.get("/searchId")
def getId():
    datos = request.get_json(silent=True) or {}
    nombre = (datos.get("nombre") or "").strip()
    if not nombre:
        return {"error":"Ingrese nombre del investigador a buscar"}
    
    investigador = services.buscar_por_nombre(nombre)
    if investigador is None:
        return {"error": "Investigador no encontrado"}, 404
    
    return _a_dict(investigador)