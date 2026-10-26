from app.extensions import db
from .models import Combustibles, Estufas, Laboratorio 

# /---Combustibles---/
def listar_combustible():
    return Combustibles.query.all()

def crear_combustible(tipo, tamanio_cm, peso_kg, humedad_pct, poder_Calorifico_neto_mj_kg, poder_calorifico_bruto_mj_kg, tipo_alimentacion, contenido_carbono_pct):
    combustible =Combustibles(
      tipo=tipo,
      tamanio_cm=tamanio_cm,
      peso_kg=peso_kg,
      humedad_pct=humedad_pct,
      poder_Calorifico_neto_mj_kg=poder_Calorifico_neto_mj_kg,
      poder_calorifico_bruto_mj_kg=poder_calorifico_bruto_mj_kg,
      tipo_alimentacion=tipo_alimentacion,
      contenido_carbono_pct=contenido_carbono_pct,
    )
    db.session.add(combustible)
    db.session.commit()
    return combustible

# /------Estufa------/
def listar_estufas():
    return Estufas.query.all()

def newEstufa(marca, fabricante, area_camara_cm2, altura_cm, material, descripcion):
    estufa = Estufas(
        marca = marca,
        fabricante = fabricante,
        area_camara_cm2 = area_camara_cm2,
        altura_cm = altura_cm,
        material = material,
        descripcion = descripcion
    )
    db.session.add(estufa)
    db.session.commit()
    return estufa

# /-------Labs-------/
def listar_labs():
    return Laboratorio.query.all()

def newLab(institucion, direccion, descripcion):
    laboratorio = Laboratorio(
        institucion = institucion,
        direccion = direccion,
        descripcion = descripcion
    )
    db.session.add(laboratorio)
    db.session.commit()
    return laboratorio