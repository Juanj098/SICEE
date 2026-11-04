from datetime import datetime, timezone
import uuid

from app.extensions import db


# condiciones_ambientales
class Cond_Ambientales(db.Model):
    __tablename__ = "condiciones_ambientales"

    id = db.Column(db.Integer, primary_key=True)
    temperatura_c = db.Column(db.Numeric(5, 2))
    humedad_relativa_pct = db.Column(db.Numeric(5, 2))
    presion_atmosferica_kpa = db.Column(db.Numeric(7, 3))
    viento_ms = db.Column(db.Numeric(5, 2))
    punto_ebullicion_c = db.Column(db.Numeric(5, 2))

    pruebas_wbt = db.relationship(
        "PruebaWBT",
        back_populates="cond_ambientales",
    )


# prueba_wbt
class PruebaWBT(db.Model):
    __tablename__ = "prueba_wbt"

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(
        db.Uuid,
        unique=True,
        nullable=False,
        default=uuid.uuid4,
    )
    fecha = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc).replace(tzinfo=None),
    )
    investigador_id = db.Column(
        db.Integer,
        db.ForeignKey("investigador.id"),
        nullable=False,
    )
    laboratorio_id = db.Column(
        db.Integer,
        db.ForeignKey("laboratorio.id"),
        nullable=False,
    )
    estufa_id = db.Column(
        db.Integer,
        db.ForeignKey("estufa.id"),
        nullable=False,
    )
    combustible_id = db.Column(
        db.Integer,
        db.ForeignKey("combustible.id"),
        nullable=False,
    )
    condiciones_ambientales_id = db.Column(
        db.Integer,
        db.ForeignKey("condiciones_ambientales.id"),
        nullable=False,
    )
    observaciones = db.Column(db.String(1000))
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc).replace(tzinfo=None),
    )
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc).replace(tzinfo=None),
        onupdate=lambda: datetime.now(timezone.utc).replace(tzinfo=None),
    )

    investigador = db.relationship(
        "Investigador",
        back_populates="pruebas_wbt",
    )
    laboratorio = db.relationship(
        "Laboratorio",
        back_populates="pruebas_wbt",
    )
    estufa = db.relationship("Estufas", back_populates="pruebas_wbt")
    combustible = db.relationship("Combustibles", back_populates="pruebas_wbt")
    cond_ambientales = db.relationship(
        "Cond_Ambientales",
        back_populates="pruebas_wbt",
    )

    fase_prueba = db.relationship(
        "FasePrueba",
        back_populates="prueba",
        cascade="all, delete-orphan",
    )


# fase_prueba
class FasePrueba(db.Model):
    __tablename__ = "fase_prueba"

    id = db.Column(db.Integer, primary_key=True)
    prueba_wbt_id = db.Column(
        db.Integer,
        db.ForeignKey("prueba_wbt.id", ondelete="CASCADE"),
        nullable=False,
    )
    tipo_fase = db.Column(db.String(48), nullable=False)
    numero_repeticion = db.Column(db.Integer, nullable=False)
    t_inicial = db.Column(db.DateTime)
    t_final = db.Column(db.DateTime)
    temperatura_inicial_agua_c = db.Column(db.Numeric(5, 2))
    temperatura_final_agua_c = db.Column(db.Numeric(5, 2))
    peso_olla_seco_kg = db.Column(db.Numeric(8, 4))
    peso_olla_agua_inicial_kg = db.Column(db.Numeric(8, 4))
    peso_olla_agua_final_kg = db.Column(db.Numeric(8, 4))
    peso_combustible_inicial_kg = db.Column(db.Numeric(8, 4))
    peso_combustible_final_kg = db.Column(db.Numeric(8, 4))

    prueba = db.relationship("PruebaWBT", back_populates="fase_prueba")
    medicion = db.relationship(
        "MedicionesOps",
        back_populates="fase",
        uselist=False,
        cascade="all, delete-orphan",
    )
    resultados = db.relationship(
        "resultado_fase",
        back_populates="fase_prueba",
        cascade="all, delete-orphan",
    )


# mediciones_opcionales
class MedicionesOps(db.Model):
    __tablename__ = "mediciones_opcionales"

    id = db.Column(db.Integer, primary_key=True)
    fase_id = db.Column(
        db.Integer,
        db.ForeignKey("fase_prueba.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    co_ppm = db.Column(db.Numeric(10, 3))
    pm_mg_m3 = db.Column(db.Numeric(10, 3))
    co2_ppm = db.Column(db.Numeric(10, 3))
    temperatura_ducto_c = db.Column(db.Numeric(7, 2))
    presion_atmosferica_kpa = db.Column(db.Numeric(7, 3))

    fase = db.relationship("FasePrueba", back_populates="medicion")
