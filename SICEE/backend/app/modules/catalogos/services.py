from app.extensions import db
from sqlalchemy import update
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError
from .models import Combustibles, EspecieMadera, Estufas, Laboratorio


# /---Combustibles---/
def listar_combustible():
    return Combustibles.query.options(joinedload(Combustibles.especie)).filter_by(activo=True).all()


def crear_combustible(
    tipo,
    longitud_combustible_cm,
    ancho_combustible_cm,
    poder_calorifico_neto_mj_kg,
    poder_calorifico_bruto_mj_kg,
    poder_calorifico_carbon_mj_kg,
    tipo_alimentacion,
    contenido_carbono_pct,
    contenido_carbono_carbon_pct,
    descripcion,
    especie_id=None
):
    if especie_id is not None:
        especie = db.session.get(EspecieMadera, especie_id, with_for_update=True)
        if especie is None:
            raise ValueError(f'No existe la especie con id {especie_id}')
        if not especie.activo:
            raise ValueError('La especie seleccionada está inactiva')

        # El lote guarda una copia de los valores de la especie. Si el
        # formulario no los envió, se toman de la especie.
        if poder_calorifico_neto_mj_kg is None:
            poder_calorifico_neto_mj_kg = especie.poder_calorifico_neto_mj_kg
        if poder_calorifico_bruto_mj_kg is None:
            poder_calorifico_bruto_mj_kg = especie.poder_calorifico_bruto_mj_kg
        if poder_calorifico_carbon_mj_kg is None:
            poder_calorifico_carbon_mj_kg = especie.poder_calorifico_carbon_mj_kg
        if contenido_carbono_pct is None:
            contenido_carbono_pct = especie.contenido_carbono_pct

    combustible = Combustibles(
        tipo=tipo,
        especie_id=especie_id,
        longitud_combustible_cm=longitud_combustible_cm,
        ancho_combustible_cm=ancho_combustible_cm,
        poder_calorifico_neto_mj_kg=poder_calorifico_neto_mj_kg,
        poder_calorifico_bruto_mj_kg=poder_calorifico_bruto_mj_kg,
        poder_calorifico_carbon_mj_kg=poder_calorifico_carbon_mj_kg,
        tipo_alimentacion=tipo_alimentacion,
        contenido_carbono_pct=contenido_carbono_pct,
        contenido_carbono_carbon_pct=contenido_carbono_carbon_pct,
        descripcion=descripcion
    )
    db.session.add(combustible)
    db.session.commit()
    return combustible


def listar_combustibles_activos():
    return listar_combustible()


# /---Especies de madera---/
def listar_especies():
    return EspecieMadera.query.filter_by(activo=True).all()


def listar_especies_todas():
    return EspecieMadera.query.all()


def crear_especie(
    especie,
    nombres_comunes=None,
    poder_calorifico_bruto_mj_kg=None,
    poder_calorifico_neto_mj_kg=None,
    poder_calorifico_carbon_mj_kg=None,
    contenido_carbono_pct=None,
    fuente_codigo=None,
    fuente=None
):
    nueva = EspecieMadera(
        especie=especie,
        nombres_comunes=nombres_comunes,
        poder_calorifico_bruto_mj_kg=poder_calorifico_bruto_mj_kg,
        poder_calorifico_neto_mj_kg=poder_calorifico_neto_mj_kg,
        poder_calorifico_carbon_mj_kg=poder_calorifico_carbon_mj_kg,
        contenido_carbono_pct=contenido_carbono_pct,
        fuente_codigo=fuente_codigo,
        fuente=fuente,
    )
    db.session.add(nueva)
    try:
        db.session.commit()
    except IntegrityError as exc:
        db.session.rollback()
        raise ValueError(
            'Ya existe una especie con ese nombre y fuente'
        ) from exc
    return nueva


# /------Estufa------/
def listar_estufas():
    return Estufas.query.filter_by(activo=True).all()


def newEstufa(marca, fabricante, area_camara_cm2, altura_cm, numero_hornillas, material, descripcion):
    estufa = Estufas(
        marca=marca,
        fabricante=fabricante,
        area_camara_cm2=area_camara_cm2,
        altura_cm=altura_cm,
        numero_hornillas=numero_hornillas,
        material=material,
        descripcion=descripcion,
    )
    db.session.add(estufa)
    db.session.commit()
    return estufa


# /-------Labs-------/
def listar_labs():
    return Laboratorio.query.filter_by(activo=True).all()


def newLab(institucion, direccion, descripcion):
    laboratorio = Laboratorio(
        institucion=institucion,
        direccion=direccion,
        descripcion=descripcion,
    )
    db.session.add(laboratorio)
    db.session.commit()
    return laboratorio


# /-------Baja lógica-------/
def cambiar_activo(modelo, id_, activo):
    """Activa o desactiva un registro del catálogo sin borrarlo."""
    stmt = (
        update(modelo)
        .where(modelo.id == id_)
        .values(activo=activo)
        .execution_options(synchronize_session=False)
    )
    resultado = db.session.execute(stmt)
    db.session.commit()
    return resultado.rowcount > 0
