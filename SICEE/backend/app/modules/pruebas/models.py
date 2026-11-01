from app.extensions import db
from datetime import date, datetime, time

#condiciones_ambientales
class Cond_Ambientales(db.Model):
    __tablename__="condiciones_ambientales"

    id = db.Column(db.Integer, primary_key=True)
    temperatura_c = db.Column(db.Numeric(5,2))
    humedad_relativa_pct = db.Column(db.Numeric(5,2))
    presion_atmosferica_kpa = db.Column(db.Numeric(7,3))
    viento_ms = db.Column(db.Numeric(5,2))
    punto_ebullicion_c = db.Column(db.Numeric(5,2))

    pruebas_wbt = db.relationship("PruebaWBT", back_populates="cond_ambientales")

# prueba_wbt
class PruebaWBT(db.Model):
    __tablename__="prueba_wbt"

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(32), nullable=False)
    fecha = db.Column(db.Date, nullable=False, default=date.today)
    investigador_id = db.Column(db.Integer, db.ForeignKey("investigador.id"), nullable=False)
    laboratorio_id = db.Column(db.Integer, db.ForeignKey("laboratorio.id"), nullable=False)
    estufa_id = db.Column(db.Integer, db.ForeignKey("estufa.id"), nullable=False)
    combustible_id = db.Column(db.Integer, db.ForeignKey("combustible.id"), nullable=False)
    condiciones_ambientales_id = db.Column(db.Integer, db.ForeignKey("condiciones_ambientales.id"), nullable=False)
    observaciones = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    investigador = db.relationship("Investigador", back_populates = "pruebas_wbt")
    laboratorio = db.relationship("Laboratorio", back_populates = "pruebas_wbt")
    estufa = db.relationship("Estufas", back_populates = "pruebas_wbt")
    combustible = db.relationalship("Combustibles", back_populates = "pruebas_wbt")
    cond_ambientales = db.relationship("Cond_Ambientales", back_populates = "pruebas_wbt")

    fase_prueba = db.relationship("FasePrueba", back_populates = "pruebas_wbt")

#fase_prueba
class FasePrueba(db.Model):
    __tablename__="fase_prueba"

    id = db.Column(db.Integer, primary_key=True)
    P_WBT_id = db.Column(db.Integer, db.ForeignKey("prueba_wbt.id"), nullable=False)
    tipo_fase = db.Column(db.String(16), nullable=False)
    n_repeticion = db.Column(db.Integer)
    t_inicial = db.Column(db.Time, nullable=False)
    t_final = db.Column(db.Time, nullable=False)
    temp_inicial_agua = db.Column(db.Numeric(5,2))
    temp_final_agua = db.Column(db.Numeric(5,2))
    peso_olla_seco = db.Column(db.Numeric(8,4))
    peso_olla_agua_inicial = db.Column(db.Numeric(8,4))
    peso_olla_agua_final = db.Column(db.Numeric(8,4))
    peso_combustible_inicial = db.Column(db.Numeric(8,4))
    peso_combustible_final = db.Column(db.Numeric(8,4))

    pruebas_wbt = db.relationship("PruebaWBT", back_populates="fase_prueba")
    mediciones = db.relationship("MedicionesOps", back_populates="fase_prueba")

#mediciones_opcionales
class MedicionesOps(db.Model):
    __tablename__="mediciones_opcionales"

    id = db.Column(db.Integer, primary_key=True)
    fase_id = db.Column(db.Integer, db.ForeignKey("fase_prueba.id"))
    co_ppm = db.Column(db.Numeric(10,3))
    pm_mg_m3 = db.Column(db.Numeric(10,3))
    co2_ppm = db.Column(db.Numeric(10,3))
    temp_ducto = db.Column(db.Numeric(7,2))
    presion_atm_kpa = db.Column(db.Numeric(7,3))

    fase_prueba = db.relationship("FasePrueba", back_populates = "mediciones")

