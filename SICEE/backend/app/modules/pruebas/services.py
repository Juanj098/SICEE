from app.extensions import db
from .models import Cond_Ambientales

# /---Cond_Ambientales---/
def list_condicion_ambiental():
    return Cond_Ambientales.query.all()

def crear_condicion_ambiental(temperatura, humedad, presion_atm, viento, pto_ebullicion):
    condiciones_ambientales = Cond_Ambientales(
        temperatura = temperatura,
        humedad = humedad,
        presion_atm = presion_atm,
        viento = viento,
        pto_ebullicion = pto_ebullicion
    )
    db.session.add(condiciones_ambientales)
    db.session.commit()
    return condiciones_ambientales