from app.extensions import db

class Laboratorio(db.Model):
    __tablename__="laboratorio"

    id = db.Column(db.Integer, primary_key=True)
    institucion = db.Column(db.String(150), nullable=False)
    direccion = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.String(500))

class Estufas(db.Model):
    __tablename__="estufa"

    id = db.Column(db.Integer, primary_key=True)
    marca = db.Column(db.String(100))
    fabricante = db.Column(db.String(100))
    area_camara_cm2 = db.Column(db.Numeric(10,2))
    altura_cm = db.Column(db.Numeric(10,2))
    material = db.Column(db.String(100))
    descripcion = db.Column(db.String(500))

class Combustibles(db.Model):
    __tablename__="combustible"

    id = db.Column(db.Integer, primary_key=True)                #INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    tipo = db.Column(db.String(100), nullable=False)            #VARCHAR(100) NOT NULL,
    tamanio_cm = db.Column(db.Numeric(8,2))                     #DECIMAL(8,2),
    peso_kg = db.Column(db.Numeric(8,4))                        #DECIMAL(8,4),
    humedad_pct = db.Column(db.Numeric(5,2))                    #DECIMAL(5,2),
    poder_calorifico_neto_mj_kg = db.Column(db.Numeric(8,3))    #DECIMAL(8,3),
    poder_calorifico_bruto_mj_kg = db.Column(db.Numeric(8,3))   #DECIMAL(8,3),
    tipo_alimentacion = db.Column(db.String(100))               #VARCHAR(100),
    contenido_carbono_pct = db.Column(db.Numeric(5,2))          #DECIMAL(5,2)