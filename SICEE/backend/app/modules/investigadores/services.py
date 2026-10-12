from app.extensions import db
from .models import Investigador

def listar():
    return Investigador.query.all()

def newInvestigador(name):
    investigador = Investigador(nombre=name)
    db.session.add(investigador)
    db.session.commit()
    return investigador

def obtener_por_id(id):
    return db.session.get(Investigador, id)

def buscar_por_nombre(nombre):
    return Investigador.query.filter_by(nombre=nombre).first()