from sqlalchemy.exc import IntegrityError

from app.extensions import db
from .models import (
    Cond_Ambientales,
    ConjuntoPruebas,
    FasePrueba,
    MedicionesOps,
    MuestraHumedad,
    Olla,
    OllaFase,
    PruebaWBT,
)


def _guardar(obj):
    """Agrega, confirma y traduce errores de integridad a ValueError."""
    db.session.add(obj)
    try:
        db.session.commit()
    except IntegrityError as exc:
        db.session.rollback()
        raise ValueError(f'No se pudo guardar: {exc.orig}') from exc
    return obj


# /---Cond_Ambientales---/
def list_condicion_ambiental():
    return Cond_Ambientales.query.all()


def crear_condicion_ambiental(
    temperatura_c=None,
    humedad_relativa_pct=None,
    altitud_m=None,
    presion_atmosferica_kpa=None,
    viento_ms=None,
    condicion_viento=None,
    punto_ebullicion_c=None,
):
    condiciones_ambientales = Cond_Ambientales(
        temperatura_c=temperatura_c,
        humedad_relativa_pct=humedad_relativa_pct,
        altitud_m=altitud_m,
        presion_atmosferica_kpa=presion_atmosferica_kpa,
        viento_ms=viento_ms,
        condicion_viento=condicion_viento,
        punto_ebullicion_c=punto_ebullicion_c,
    )
    return _guardar(condiciones_ambientales)


# /---Conjunto_Pruebas---/
def list_conjuntos_pruebas():
    return ConjuntoPruebas.query.all()


def crear_conjunto_pruebas(
    estufa_id,
    descripcion=None,
):
    conjunto = ConjuntoPruebas(
        estufa_id=estufa_id,
        descripcion=descripcion,
    )
    return _guardar(conjunto)


# /---Prueba_WBT---/
def list_pruebas_wbt():
    return PruebaWBT.query.all()


def registrar_Prueba_wbt(
    fecha,
    investigador_id,
    laboratorio_id,
    combustible_id,
    condiciones_amb_id,
    conjunto_pruebas_id,
    peso_recipiente_carbon_kg=None,
    numero_repeticion=1,
    es_valida=True,
    motivo_invalidez=None,
    version_protocolo='4.2.3',
    observaciones=None,
):
    prueba_wbt = PruebaWBT(
        fecha=fecha,
        investigador_id=investigador_id,
        laboratorio_id=laboratorio_id,
        combustible_id=combustible_id,
        condiciones_ambientales_id=condiciones_amb_id,
        conjunto_pruebas_id=conjunto_pruebas_id,
        peso_recipiente_carbon_kg=peso_recipiente_carbon_kg,
        numero_repeticion=numero_repeticion,
        es_valida=es_valida,
        motivo_invalidez=motivo_invalidez,
        version_protocolo=version_protocolo,
        observaciones=observaciones,
    )
    return _guardar(prueba_wbt)


# /--- Fase_Prueba ---/
def list_fases_prueba():
    return FasePrueba.query.all()


def crear_fase_prueba(
    prueba_wbt_id,
    tipo_fase,
    t_inicial=None,
    t_final=None,
    peso_combustible_inicial_kg=None,
    peso_combustible_final_kg=None,
    peso_carbon_con_recipiente_kg=None,
    peso_cenizas_kg=None,
    observaciones=None,
):
    fase = FasePrueba(
        prueba_wbt_id=prueba_wbt_id,
        tipo_fase=tipo_fase,
        t_inicial=t_inicial,
        t_final=t_final,
        peso_combustible_inicial_kg=peso_combustible_inicial_kg,
        peso_combustible_final_kg=peso_combustible_final_kg,
        peso_carbon_con_recipiente_kg=peso_carbon_con_recipiente_kg,
        peso_cenizas_kg=peso_cenizas_kg,
        observaciones=observaciones,
    )
    return _guardar(fase)

# /--- Olla ---/
def list_ollas():
    return Olla.query.all()


def crear_olla(
    prueba_wbt_id,
    numero_olla,
    peso_seco_kg=None,
    capacidad_l=None,
):
    olla = Olla(
        prueba_wbt_id=prueba_wbt_id,
        numero_olla=numero_olla,
        peso_seco_kg=peso_seco_kg,
        capacidad_l=capacidad_l,
    )
    return _guardar(olla)


# /--- Olla_Fase ---/
def list_ollas_fase():
    return OllaFase.query.all()


def crear_olla_fase(
    olla_id,
    fase_id,
    temperatura_inicial_agua_c=None,
    temperatura_final_agua_c=None,
    peso_con_agua_inicial_kg=None,
    peso_con_agua_final_kg=None,
):
    olla = db.session.get(Olla, olla_id)
    fase = db.session.get(FasePrueba, fase_id)
    if olla is None:
        raise ValueError(f'No existe la olla con id {olla_id}')
    if fase is None:
        raise ValueError(f'No existe la fase con id {fase_id}')
    if olla.prueba_wbt_id != fase.prueba_wbt_id:
        raise ValueError(
            'La olla y la fase pertenecen a pruebas WBT distintas'
        )

    olla_fase = OllaFase(
        olla_id=olla_id,
        fase_id=fase_id,
        temperatura_inicial_agua_c=temperatura_inicial_agua_c,
        temperatura_final_agua_c=temperatura_final_agua_c,
        peso_con_agua_inicial_kg=peso_con_agua_inicial_kg,
        peso_con_agua_final_kg=peso_con_agua_final_kg,
    )
    return _guardar(olla_fase)


# /--- Mediciones_Opcionales ---/
def listar_mediciones_opcionales():
    return MedicionesOps.query.all()


def registrar_mediciones_ops(
    fase_id,
    temperatura_ducto_c=None,
    co_ppm=None,
    pm_ug_m3=None,
    co2_ppm=None,
    co2_fondo_ppm=None,
    co_fondo_ppm=None,
    pm_fondo_ug_m3=None,
    co2_total_g=None,
    co_total_g=None,
    pm_total_g=None,
):
    med_ops = MedicionesOps(
        fase_id=fase_id,
        temperatura_ducto_c=temperatura_ducto_c,
        co_ppm=co_ppm,
        pm_ug_m3=pm_ug_m3,
        co2_ppm=co2_ppm,
        co2_fondo_ppm=co2_fondo_ppm,
        co_fondo_ppm=co_fondo_ppm,
        pm_fondo_ug_m3=pm_fondo_ug_m3,
        co2_total_g=co2_total_g,
        co_total_g=co_total_g,
        pm_total_g=pm_total_g,
    )
    return _guardar(med_ops)


# /--- Muestra de humedad ---/
def list_muestras_humedad(prueba_wbt_id=None):
    consulta = MuestraHumedad.query
    if prueba_wbt_id is not None:
        consulta = consulta.filter(MuestraHumedad.prueba_wbt_id == prueba_wbt_id)
    return consulta.order_by(
        MuestraHumedad.numero_lenio,
        MuestraHumedad.numero_medicion,
    ).all()


def promedio_humedad(prueba_wbt_id):
    valores = [
        float(humedad)
        for (humedad,) in db.session.query(MuestraHumedad.humedad_pct)
        .filter(MuestraHumedad.prueba_wbt_id == prueba_wbt_id)
        .all()
        if humedad is not None
    ]
    if not valores:
        return None
    return round(sum(valores) / len(valores), 2)


def reemplazar_muestras_humedad(prueba_wbt_id, muestras):
    """Reemplaza las mediciones de humedad de una prueba.

    `muestras` es una lista de dicts con numero_lenio, numero_medicion y
    humedad_pct (Decimal). Se valida que no haya pares repetidos antes de
    escribir, para devolver un mensaje claro en vez de un error de Postgres.
    """
    if db.session.get(PruebaWBT, prueba_wbt_id) is None:
        raise ValueError(f'No existe la prueba WBT con id {prueba_wbt_id}')
    if not muestras:
        raise ValueError('Debe enviar al menos una medición de humedad')

    vistas = set()
    filas = []
    for muestra in muestras:
        numero_lenio = muestra.get('numero_lenio')
        numero_medicion = muestra.get('numero_medicion')
        humedad_pct = muestra.get('humedad_pct')
        if numero_lenio is None or numero_medicion is None:
            raise ValueError('Cada muestra requiere numero_lenio y numero_medicion')
        if humedad_pct is None:
            raise ValueError('Cada muestra requiere humedad_pct')

        clave = (numero_lenio, numero_medicion)
        if clave in vistas:
            raise ValueError(
                f'Medición repetida: leño {numero_lenio}, medición {numero_medicion}'
            )
        vistas.add(clave)

        filas.append(
            MuestraHumedad(
                prueba_wbt_id=prueba_wbt_id,
                numero_lenio=numero_lenio,
                numero_medicion=numero_medicion,
                humedad_pct=humedad_pct,
            )
        )

    try:
        MuestraHumedad.query.filter_by(prueba_wbt_id=prueba_wbt_id).delete()
        db.session.add_all(filas)
        db.session.commit()
    except IntegrityError as exc:
        db.session.rollback()
        raise ValueError(f'No se pudieron guardar las muestras: {exc.orig}') from exc

    return filas
