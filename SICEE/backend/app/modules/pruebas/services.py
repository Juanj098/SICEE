from datetime import datetime
from decimal import Decimal, InvalidOperation

from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.modules.catalogos.models import Combustibles, Laboratorio
from app.modules.investigadores.models import Investigador
from .constants import TIPOS_FASE
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


# /--- Prueba completa (una sola transacción) ---/
def _c_decimal(valor, campo):
    if valor is None or valor == '':
        return None
    try:
        return Decimal(str(valor))
    except (InvalidOperation, ValueError, TypeError):
        raise ValueError(f'{campo} debe ser un número')

def _c_entero(valor, campo, obligatorio=True):
    if valor is None or valor == '':
        if obligatorio:
            raise ValueError(f'El campo {campo} es obligatorio')
        return None
    try:
        return int(valor)
    except (TypeError, ValueError):
        raise ValueError(f'{campo} debe ser un número entero')

def _c_texto(valor):
    if valor is None:
        return None
    texto = str(valor).strip()
    return texto or None

def _c_fecha(valor, campo):
    if valor is None or valor == '':
        return None
    try:
        return datetime.fromisoformat(str(valor))
    except (TypeError, ValueError):
        raise ValueError(f'{campo} debe tener formato ISO 8601')

def _c_existe(modelo, id_, etiqueta):
    if db.session.get(modelo, id_) is None:
        raise ValueError(f'No existe {etiqueta} con id {id_}')

def crear_prueba_completa(datos):
    """Crea la prueba con todas sus mediciones en una sola transacción.

    Valida todo antes de escribir: si algo falla, no se inserta ninguna fila.
    Las fases y las muestras referencian las ollas por `numero_olla`, porque
    sus ids todavía no existen.
    """
    if not isinstance(datos, dict):
        raise ValueError('El cuerpo debe ser un objeto JSON')

    prueba_datos = datos.get('prueba') or {}
    condiciones_datos = datos.get('condiciones') or {}
    muestras_datos = datos.get('muestras') or []
    ollas_datos = datos.get('ollas') or []
    fases_datos = datos.get('fases') or []

    for nombre, lista in (
        ('muestras', muestras_datos),
        ('ollas', ollas_datos),
        ('fases', fases_datos),
    ):
        if not isinstance(lista, list) or not lista:
            raise ValueError(f'Debe enviar al menos una entrada en {nombre}')

    investigador_id = _c_entero(prueba_datos.get('investigador_id'), 'investigador_id')
    laboratorio_id = _c_entero(prueba_datos.get('laboratorio_id'), 'laboratorio_id')
    combustible_id = _c_entero(prueba_datos.get('combustible_id'), 'combustible_id')
    conjunto_pruebas_id = _c_entero(
        prueba_datos.get('conjunto_pruebas_id'), 'conjunto_pruebas_id'
    )

    _c_existe(Investigador, investigador_id, 'el investigador')
    _c_existe(Laboratorio, laboratorio_id, 'el laboratorio')
    _c_existe(Combustibles, combustible_id, 'el combustible')
    _c_existe(ConjuntoPruebas, conjunto_pruebas_id, 'el conjunto de pruebas')

    numero_repeticion = _c_entero(
        prueba_datos.get('numero_repeticion'), 'numero_repeticion', obligatorio=False
    )
    if numero_repeticion is None:
        numero_repeticion = 1
    if numero_repeticion < 1:
        raise ValueError('numero_repeticion debe ser mayor o igual a 1')

    condiciones = Cond_Ambientales(
        temperatura_c=_c_decimal(condiciones_datos.get('temperatura_c'), 'temperatura_c'),
        humedad_relativa_pct=_c_decimal(
            condiciones_datos.get('humedad_relativa_pct'), 'humedad_relativa_pct'
        ),
        altitud_m=_c_decimal(condiciones_datos.get('altitud_m'), 'altitud_m'),
        presion_atmosferica_kpa=_c_decimal(
            condiciones_datos.get('presion_atmosferica_kpa'),
            'presion_atmosferica_kpa',
        ),
        viento_ms=_c_decimal(condiciones_datos.get('viento_ms'), 'viento_ms'),
        condicion_viento=_c_texto(condiciones_datos.get('condicion_viento')),
        punto_ebullicion_c=_c_decimal(
            condiciones_datos.get('punto_ebullicion_c'), 'punto_ebullicion_c'
        ),
    )

    muestras = []
    claves_humedad = set()
    for i, muestra in enumerate(muestras_datos):
        if not isinstance(muestra, dict):
            raise ValueError(f'muestras[{i}] debe ser un objeto')

        numero_lenio = _c_entero(
            muestra.get('numero_lenio'), f'muestras[{i}].numero_lenio'
        )
        numero_medicion = _c_entero(
            muestra.get('numero_medicion'), f'muestras[{i}].numero_medicion'
        )
        humedad_pct = _c_decimal(
            muestra.get('humedad_pct'), f'muestras[{i}].humedad_pct'
        )

        if numero_lenio < 1 or numero_medicion < 1:
            raise ValueError('numero_lenio y numero_medicion deben ser mayores que 0')
        if humedad_pct is None or not (0 <= humedad_pct <= 100):
            raise ValueError('humedad_pct debe estar entre 0 y 100')

        clave = (numero_lenio, numero_medicion)
        if clave in claves_humedad:
            raise ValueError(
                f'Medición de humedad repetida: leño {numero_lenio}, '
                f'medición {numero_medicion}'
            )
        claves_humedad.add(clave)

        muestras.append(
            MuestraHumedad(
                numero_lenio=numero_lenio,
                numero_medicion=numero_medicion,
                humedad_pct=humedad_pct,
            )
        )

    ollas = {}
    for i, olla_datos in enumerate(ollas_datos):
        if not isinstance(olla_datos, dict):
            raise ValueError(f'ollas[{i}] debe ser un objeto')

        numero_olla = _c_entero(olla_datos.get('numero_olla'), f'ollas[{i}].numero_olla')
        if numero_olla < 1:
            raise ValueError('numero_olla debe ser mayor o igual a 1')
        if numero_olla in ollas:
            raise ValueError(f'Olla repetida: {numero_olla}')

        ollas[numero_olla] = Olla(
            numero_olla=numero_olla,
            peso_seco_kg=_c_decimal(
                olla_datos.get('peso_seco_kg'), f'ollas[{i}].peso_seco_kg'
            ),
            capacidad_l=_c_decimal(
                olla_datos.get('capacidad_l'), f'ollas[{i}].capacidad_l'
            ),
        )

    fases = []
    tipos_vistos = set()
    for i, fase_datos in enumerate(fases_datos):
        if not isinstance(fase_datos, dict):
            raise ValueError(f'fases[{i}] debe ser un objeto')

        tipo_fase = (_c_texto(fase_datos.get('tipo_fase')) or '').lower()
        if tipo_fase not in TIPOS_FASE:
            raise ValueError(
                f'fases[{i}].tipo_fase debe ser inicio_frio, '
                'inicio_caliente o baja_potencia'
            )
        if tipo_fase in tipos_vistos:
            raise ValueError(f'Fase repetida: {tipo_fase}')
        tipos_vistos.add(tipo_fase)

        t_inicial = _c_fecha(fase_datos.get('t_inicial'), f'fases[{i}].t_inicial')
        t_final = _c_fecha(fase_datos.get('t_final'), f'fases[{i}].t_final')
        if t_inicial and t_final and t_final < t_inicial:
            raise ValueError(f'fases[{i}].t_final no puede ser anterior a t_inicial')

        fase = FasePrueba(
            tipo_fase=tipo_fase,
            t_inicial=t_inicial,
            t_final=t_final,
            peso_combustible_inicial_kg=_c_decimal(
                fase_datos.get('peso_combustible_inicial_kg'),
                f'fases[{i}].peso_combustible_inicial_kg',
            ),
            peso_combustible_final_kg=_c_decimal(
                fase_datos.get('peso_combustible_final_kg'),
                f'fases[{i}].peso_combustible_final_kg',
            ),
            peso_carbon_con_recipiente_kg=_c_decimal(
                fase_datos.get('peso_carbon_con_recipiente_kg'),
                f'fases[{i}].peso_carbon_con_recipiente_kg',
            ),
            peso_cenizas_kg=_c_decimal(
                fase_datos.get('peso_cenizas_kg'), f'fases[{i}].peso_cenizas_kg'
            ),
            observaciones=_c_texto(fase_datos.get('observaciones')),
        )

        ollas_fase = fase_datos.get('ollas') or []
        if not isinstance(ollas_fase, list):
            raise ValueError(f'fases[{i}].ollas debe ser una lista')

        numeros_fase = set()
        for j, olla_fase_datos in enumerate(ollas_fase):
            if not isinstance(olla_fase_datos, dict):
                raise ValueError(f'fases[{i}].ollas[{j}] debe ser un objeto')

            numero_olla = _c_entero(
                olla_fase_datos.get('numero_olla'),
                f'fases[{i}].ollas[{j}].numero_olla',
            )
            if numero_olla not in ollas:
                raise ValueError(
                    f'fases[{i}].ollas[{j}] referencia la olla {numero_olla}, '
                    'que no está en ollas'
                )
            if numero_olla in numeros_fase:
                raise ValueError(
                    f'La olla {numero_olla} está repetida en la fase {tipo_fase}'
                )
            numeros_fase.add(numero_olla)

            fase.olla_fase.append(
                OllaFase(
                    olla=ollas[numero_olla],
                    temperatura_inicial_agua_c=_c_decimal(
                        olla_fase_datos.get('temperatura_inicial_agua_c'),
                        f'fases[{i}].ollas[{j}].temperatura_inicial_agua_c',
                    ),
                    temperatura_final_agua_c=_c_decimal(
                        olla_fase_datos.get('temperatura_final_agua_c'),
                        f'fases[{i}].ollas[{j}].temperatura_final_agua_c',
                    ),
                    peso_con_agua_inicial_kg=_c_decimal(
                        olla_fase_datos.get('peso_con_agua_inicial_kg'),
                        f'fases[{i}].ollas[{j}].peso_con_agua_inicial_kg',
                    ),
                    peso_con_agua_final_kg=_c_decimal(
                        olla_fase_datos.get('peso_con_agua_final_kg'),
                        f'fases[{i}].ollas[{j}].peso_con_agua_final_kg',
                    ),
                )
            )

        fases.append(fase)

    prueba = PruebaWBT(
        fecha=_c_fecha(prueba_datos.get('fecha'), 'fecha'),
        investigador_id=investigador_id,
        laboratorio_id=laboratorio_id,
        combustible_id=combustible_id,
        conjunto_pruebas_id=conjunto_pruebas_id,
        peso_recipiente_carbon_kg=_c_decimal(
            prueba_datos.get('peso_recipiente_carbon_kg'),
            'peso_recipiente_carbon_kg',
        ),
        numero_repeticion=numero_repeticion,
        observaciones=_c_texto(prueba_datos.get('observaciones')),
    )
    prueba.cond_ambientales = condiciones
    prueba.muestra_humedad = muestras
    prueba.olla = list(ollas.values())
    prueba.fase_prueba = fases

    db.session.add(prueba)
    try:
        db.session.commit()
    except IntegrityError as exc:
        db.session.rollback()
        raise ValueError(f'No se pudo guardar la prueba: {exc.orig}') from exc

    return prueba
