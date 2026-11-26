from app.extensions import db
from .models import Investigador
from sqlalchemy import update

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

def update_investigador(id,state):
    stmt = (
        update(Investigador)
        .where(Investigador.id == id)
        .values(activo = state)
        .execution_options(synchronize_session=False)
    )
    result = db.session.execute(stmt)
    db.session.commit()
    return result.rowcount > 0

def listar_activos():
    consulta = Investigador.query.filter_by(activo=True)
    return consulta.all()