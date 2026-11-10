import uuid
from datetime import datetime, timezone

from app.extensions import db


def _ahora():
    """Fecha local sin zona horaria, como TIMESTAMP en PostgreSQL."""
    return datetime.now(timezone.utc).replace(tzinfo=None)


# condiciones_ambientales
class Cond_Ambientales(db.Model):
    __tablename__ = "condiciones_ambientales"

    id = db.Column(db.Integer, primary_key=True)
    temperatura_c = db.Column(db.Numeric(6, 2))
    humedad_relativa_pct = db.Column(db.Numeric(5, 2))
    altitud_m = db.Column(db.Numeric(7, 2))
    presion_atmosferica_kpa = db.Column(db.Numeric(7, 3))
    viento_ms = db.Column(db.Numeric(5, 2))
    condicion_viento = db.Column(db.String(500))
    punto_ebullicion_c = db.Column(db.Numeric(6, 2))

    pruebas_wbt = db.relationship("PruebaWBT", back_populates="cond_ambientales")


# prueba_wbt
class PruebaWBT(db.Model):
    __tablename__ = "prueba_wbt"

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.Uuid, unique=True, nullable=False, default=uuid.uuid4)
    fecha = db.Column(db.DateTime, nullable=False, default=_ahora)
    investigador_id = db.Column(db.Integer, db.ForeignKey("investigador.id"), nullable=False)
    laboratorio_id = db.Column(db.Integer, db.ForeignKey("laboratorio.id"), nullable=False)
    combustible_id = db.Column(db.Integer, db.ForeignKey("combustible.id"), nullable=False)
    condiciones_ambientales_id = db.Column(db.Integer, db.ForeignKey("condiciones_ambientales.id"), nullable=False)
    conjunto_pruebas_id = db.Column(db.Integer, db.ForeignKey("conjunto_pruebas.id"), nullable=False)
    peso_recipiente_carbon_kg = db.Column(db.Numeric(8, 4))
    numero_repeticion = db.Column(db.Integer, nullable=False, default=1)
    es_valida = db.Column(db.Boolean, nullable=False, default=True, server_default=db.text("true"))
    motivo_invalidez = db.Column(db.String(500))
    version_protocolo = db.Column(db.String(10), nullable=False, default="4.2.3", server_default=db.text("'4.2.3'"))
    observaciones = db.Column(db.String(1000))
    created_at = db.Column(db.DateTime, nullable=False, default=_ahora)
    updated_at = db.Column(db.DateTime, nullable=False, default=_ahora, onupdate=_ahora)

    investigador = db.relationship("Investigador", back_populates="pruebas_wbt")
    laboratorio = db.relationship("Laboratorio", back_populates="pruebas_wbt")
    combustible = db.relationship("Combustibles", back_populates="pruebas_wbt")
    cond_ambientales = db.relationship("Cond_Ambientales", back_populates="pruebas_wbt")
    conjunto_pruebas = db.relationship("ConjuntoPruebas", back_populates="prueba_wbt")
    olla = db.relationship("Olla", back_populates="prueba_wbt", cascade="all, delete-orphan")
    fase_prueba = db.relationship("FasePrueba", back_populates="prueba", cascade="all, delete-orphan")

    __table_args__ = (
        db.UniqueConstraint(
            "conjunto_pruebas_id",
            "numero_repeticion",
            name="uq_prueba_wbt_conjunto_repeticion",
        ),
    )


# fase_prueba
class FasePrueba(db.Model):
    __tablename__ = "fase_prueba"

    id = db.Column(db.Integer, primary_key=True)
    prueba_wbt_id = db.Column(db.Integer, db.ForeignKey("prueba_wbt.id", ondelete="CASCADE"), nullable=False)
    tipo_fase = db.Column(db.String(48), nullable=False)
    t_inicial = db.Column(db.DateTime)
    t_final = db.Column(db.DateTime)
    peso_combustible_inicial_kg = db.Column(db.Numeric(8, 4))
    peso_combustible_final_kg = db.Column(db.Numeric(8, 4))
    peso_carbon_con_recipiente_kg = db.Column(db.Numeric(8, 4))
    peso_cenizas_kg = db.Column(db.Numeric(8, 4))
    observaciones = db.Column(db.String(500))

    prueba = db.relationship("PruebaWBT", back_populates="fase_prueba")
    medicion = db.relationship("MedicionesOps", back_populates="fase", uselist=False, cascade="all, delete-orphan")
    olla_fase = db.relationship("OllaFase", back_populates="fase", cascade="all, delete-orphan")
    resultados = db.relationship("resultado_fase", back_populates="fase_prueba", cascade="all, delete-orphan")

    __table_args__ = (
        db.UniqueConstraint(
            "prueba_wbt_id",
            "tipo_fase",
            name="uq_fase_prueba_prueba_tipo",
        ),
    )


# mediciones_opcionales
class MedicionesOps(db.Model):
    __tablename__ = "mediciones_opcionales"

    id = db.Column(db.Integer, primary_key=True)
    fase_id = db.Column(db.Integer, db.ForeignKey("fase_prueba.id", ondelete="CASCADE"), nullable=False, unique=True)
    temperatura_ducto_c = db.Column(db.Numeric(7, 2))
    co_ppm = db.Column(db.Numeric(10, 3))
    pm_ug_m3 = db.Column(db.Numeric(10, 3))
    co2_ppm = db.Column(db.Numeric(10, 3))
    co2_fondo_ppm = db.Column(db.Numeric(10, 3))
    co_fondo_ppm = db.Column(db.Numeric(10, 3))
    pm_fondo_ug_m3 = db.Column(db.Numeric(10, 3))
    co2_total_g = db.Column(db.Numeric(12, 3))
    co_total_g = db.Column(db.Numeric(12, 3))
    pm_total_g = db.Column(db.Numeric(12, 6))

    fase = db.relationship("FasePrueba", back_populates="medicion")


# conjunto_pruebas
class ConjuntoPruebas(db.Model):
    __tablename__ = "conjunto_pruebas"

    id = db.Column(db.Integer, primary_key=True)
    estufa_id = db.Column(db.Integer, db.ForeignKey("estufa.id"), nullable=False)
    descripcion = db.Column(db.String(500))

    estufa = db.relationship("Estufas", back_populates="conjunto_pruebas")
    prueba_wbt = db.relationship("PruebaWBT", back_populates="conjunto_pruebas")


# olla
class Olla(db.Model):
    __tablename__ = "olla"

    id = db.Column(db.Integer, primary_key=True)
    prueba_wbt_id = db.Column(db.Integer, db.ForeignKey("prueba_wbt.id", ondelete="CASCADE"), nullable=False)
    numero_olla = db.Column(db.Integer, nullable=False)
    peso_seco_kg = db.Column(db.Numeric(8, 4))
    capacidad_l = db.Column(db.Numeric(5, 2))

    prueba_wbt = db.relationship("PruebaWBT", back_populates="olla")
    olla_fase = db.relationship("OllaFase", back_populates="olla", cascade="all, delete-orphan")

    __table_args__ = (
        db.UniqueConstraint(
            "prueba_wbt_id",
            "numero_olla",
            name="uq_olla_prueba_numero",
        ),
    )


# olla_fase
class OllaFase(db.Model):
    __tablename__ = "olla_fase"

    id = db.Column(db.Integer, primary_key=True)
    olla_id = db.Column(db.Integer, db.ForeignKey("olla.id", ondelete="CASCADE"), nullable=False)
    fase_id = db.Column(db.Integer, db.ForeignKey("fase_prueba.id", ondelete="CASCADE"), nullable=False)
    temperatura_inicial_agua_c = db.Column(db.Numeric(5, 2))
    temperatura_final_agua_c = db.Column(db.Numeric(5, 2))
    peso_con_agua_inicial_kg = db.Column(db.Numeric(8, 4))
    peso_con_agua_final_kg = db.Column(db.Numeric(8, 4))

    olla = db.relationship("Olla", back_populates="olla_fase")
    fase = db.relationship("FasePrueba", back_populates="olla_fase")

    __table_args__ = (
        db.UniqueConstraint(
            "olla_id",
            "fase_id",
            name="uq_olla_fase_olla_fase",
        ),
    )
