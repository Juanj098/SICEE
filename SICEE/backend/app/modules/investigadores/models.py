from app.extensions import db

class Investigador(db.Model):
    __tablename__ = "investigador"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    activo = db.Column(db.Boolean, nullable=False, default=True, server_default=db.text('true'))

    pruebas_wbt = db.relationship("PruebaWBT", back_populates="investigador")
