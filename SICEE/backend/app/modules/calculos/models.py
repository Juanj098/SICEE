from app.extensions import db

# resultado de fases
class resultado_fase(db.Model):
    __tablename__="resultado_fase"

    id = db.Column(db.Integer, primary_key=True)
    fase_id = db.Column(db.Integer, db.ForeignKey("fase_prueba.id"), nullable=False)
    tiempo_fase = db.Column(db.Numeric(8,2))
    masa_agua_i = db.Column(db.Numeric(6,2))
    masa_agua_f = db.Column(db.Numeric(6,2))
    masa_agua_eva = db.Column(db.Numeric(6,4))
    combustible_consumido = db.Column(db.Numeric(6,4))
    tiempo_ebullicion = db.Column(db.Numeric(6,4))
    energia_util = db.Column(db.Numeric(8,3))
    energia_combustible = db.Column(db.Numeric(8,3))
    eficiencia_termica = db.Column(db.Numeric(8,3))
    consumo_especifico = db.Column(db.Numeric(8,3))
    vel_combustion = db.Column(db.Numeric(8,3))
    potencia_fase = db.Column(db.Numeric(8,3))
    humedad_promedio = db.Column(db.Numeric(8,3))

    fase_prueba = db.relationship("FasePrueba",back_population = "resultados")