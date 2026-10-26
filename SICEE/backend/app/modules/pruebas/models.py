from app.extensions import db

class Cond_Ambientales(db.Model):
    __tablename__="condiciones_ambientales"

    id = db.Column(db.Integer, primary_key=True)
    temperatura_c = db.Column(db.Numeric(5,2))
    humedad_relativa_pct = db.Column(db.Numeric(5,2))
    presion_atmosferica_kpa = db.Column(db.Numeric(7,3))
    viento_ms = db.Column(db.Numeric(5,2))
    punto_ebullicion_c = db.Column(db.Numeric(5,2))

