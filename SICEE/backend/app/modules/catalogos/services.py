from app.extensions import db
from .models import Combustibles, Estufas, Laboratorio


# /---Combustibles---/
def listar_combustible():
    return Combustibles.query.all()


def crear_combustible(
    tipo,
    longitud_combustible_cm,
    ancho_combustible_cm,
    humedad_pct,
    poder_calorifico_neto_mj_kg,
    poder_calorifico_bruto_mj_kg,
    poder_calorifico_carbon_mj_kg,
    tipo_alimentacion,
    contenido_carbono_pct,
    contenido_carbono_carbon_pct,
    descripcion
):
    combustible = Combustibles(
        tipo=tipo,
        longitud_combustible_cm=longitud_combustible_cm,
        ancho_combustible_cm=ancho_combustible_cm,
        humedad_pct=humedad_pct,
        poder_calorifico_neto_mj_kg=poder_calorifico_neto_mj_kg,
        poder_calorifico_bruto_mj_kg=poder_calorifico_bruto_mj_kg,
        poder_calorifico_carbon_mj_kg=poder_calorifico_carbon_mj_kg,
        tipo_alimentacion=tipo_alimentacion,
        contenido_carbono_pct=contenido_carbono_pct,
        contenido_carbono_carbon_pct=contenido_carbono_carbon_pct,
        descripcion=descripcion
    )
    db.session.add(combustible)
    db.session.commit()
    return combustible


# /------Estufa------/
def listar_estufas():
    return Estufas.query.all()


def newEstufa(marca, fabricante, area_camara_cm2, altura_cm, numero_hornillas, material, descripcion):
    estufa = Estufas(
        marca=marca,
        fabricante=fabricante,
        area_camara_cm2=area_camara_cm2,
        altura_cm=altura_cm,
        numero_hornillas=numero_hornillas,
        material=material,
        descripcion=descripcion,
    )
    db.session.add(estufa)
    db.session.commit()
    return estufa


# /-------Labs-------/
def listar_labs():
    return Laboratorio.query.all()


def newLab(institucion, direccion, descripcion):
    laboratorio = Laboratorio(
        institucion=institucion,
        direccion=direccion,
        descripcion=descripcion,
    )
    db.session.add(laboratorio)
    db.session.commit()
    return laboratorio
