from app.extensions import db


# resultado de fases
class resultado_fase(db.Model):
    __tablename__ = "resultado_fase"

    id = db.Column(db.Integer, primary_key=True)
    fase_id = db.Column(db.Integer, db.ForeignKey("fase_prueba.id", ondelete="CASCADE"), nullable=False, unique=True)
    tiempo_fase_min = db.Column(db.Numeric(8, 2))
    masa_agua_inicial_kg = db.Column(db.Numeric(8, 4))
    masa_agua_final_kg = db.Column(db.Numeric(8, 4))
    masa_agua_evaporada_kg = db.Column(db.Numeric(8, 4))
    masa_agua_efectiva_kg = db.Column(db.Numeric(6,4))
    combustible_consumido_kg = db.Column(db.Numeric(8, 4))
    tiempo_ebullicion_min = db.Column(db.Numeric(8, 2))
    tiempo_ebullicion_corregido_min = db.Column(db.Numeric(8,2))
    energia_util_kj = db.Column(db.Numeric(12, 3))
    energia_combustible_kj = db.Column(db.Numeric(12, 3))
    eficiencia_termica_pct = db.Column(db.Numeric(6, 2))
    consumo_especifico_g_l = db.Column(db.Numeric(8, 3))
    velocidad_combustion_g_min = db.Column(db.Numeric(10, 3))
    potencia_fase_kw = db.Column(db.Numeric(10, 3))
    energia_especifica_corregida_kj_l = db.Column(db.Numeric(8,3))
    combustible_seco_equivalente_kg = db.Column(db.Numeric(6,4))
    cambio_carbon_kg = db.Column(db.Numeric(6,4))
    consumo_especifico_corregido_g_l = db.Column(db.Numeric(8,3))

    fase_prueba = db.relationship("FasePrueba", back_populates="resultados")

