from app.extensions import db


class Laboratorio(db.Model):
    __tablename__ = "laboratorio"

    id = db.Column(db.Integer, primary_key=True)
    institucion = db.Column(db.String(150), nullable=False)
    direccion = db.Column(db.String(255))
    descripcion = db.Column(db.String(500))

    pruebas_wbt = db.relationship("PruebaWBT", back_populates="laboratorio")


class Estufas(db.Model):
    __tablename__ = "estufa"

    id = db.Column(db.Integer, primary_key=True)
    marca = db.Column(db.String(100))
    fabricante = db.Column(db.String(100))
    area_camara_cm2 = db.Column(db.Numeric(12, 4))
    altura_cm = db.Column(db.Numeric(12, 4))
    numero_hornillas = db.Column(db.Integer)
    material = db.Column(db.String(100))
    descripcion = db.Column(db.String(500))

    conjunto_pruebas = db.relationship(
        "ConjuntoPruebas",
        back_populates="estufa",
    )


class Combustibles(db.Model):
    __tablename__ = "combustible"

    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(100), nullable=False)
    longitud_combustible_cm = db.Column(db.Numeric(8, 2))
    ancho_combustible_cm = db.Column(db.Numeric(8, 2))
    humedad_pct = db.Column(db.Numeric(5, 2))
    poder_calorifico_neto_mj_kg = db.Column(db.Numeric(8, 3))
    poder_calorifico_bruto_mj_kg = db.Column(db.Numeric(8, 3))
    poder_calorifico_carbon_mj_kg = db.Column(db.Numeric(8, 3))
    contenido_carbono_carbon_pct = db.Column(db.Numeric(5, 2))
    tipo_alimentacion = db.Column(db.String(100))
    contenido_carbono_pct = db.Column(db.Numeric(5, 2))
    descripcion = db.Column(db.String(500))

    pruebas_wbt = db.relationship("PruebaWBT", back_populates="combustible")
