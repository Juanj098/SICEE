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
        numero = Decimal(str(valor))
    except (InvalidOperation, ValueError, TypeError):
        raise ValueError(f'{campo} debe ser un número')
    if not numero.is_finite():
        raise ValueError(f'{campo} debe ser un número finito')
    return numero

def _c_entero(valor, campo, obligatorio=True):
    if valor is None or valor == '':
        if obligatorio:
            raise ValueError(f'El campo {campo} es obligatorio')
        return None
    try:
        entero = int(valor)
    except (TypeError, ValueError):
        raise ValueError(f'{campo} debe ser un número entero')
    if isinstance(valor, bool) or Decimal(str(valor)) != entero:
        raise ValueError(f'{campo} debe ser un número entero')
    return entero

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

def _validar_medicion_fase(fase, tara, condiciones):
    nombre = fase.tipo_fase
    if not fase.t_inicial or not fase.t_final or fase.t_final <= fase.t_inicial:
        raise ValueError(f'{nombre}: indique horas de inicio y fin con duración positiva')
    inicial, final = fase.peso_combustible_inicial_kg, fase.peso_combustible_final_kg
    if inicial is None or final is None or not 0 <= final <= inicial:
        raise ValueError(f'{nombre}: revise los pesos de combustible (0 ≤ final ≤ inicial)')
    carbon = fase.peso_carbon_con_recipiente_kg
    if carbon is not None and (tara is None or not 0 <= tara <= carbon):
        raise ValueError(f'{nombre}: se requiere una tara entre cero y el peso del carbón con recipiente')
    if condiciones.temperatura_c is None or condiciones.punto_ebullicion_c is None:
        raise ValueError(f'{nombre}: faltan la temperatura ambiente o el punto de ebullición local')
    if not 0 < condiciones.punto_ebullicion_c <= 110:
        raise ValueError(f'{nombre}: el punto de ebullición debe estar entre 0 y 110 °C')

    olla_principal = False
    for medicion in fase.olla_fase:
        numero = medicion.olla.numero_olla
        valores = (medicion.temperatura_inicial_agua_c, medicion.temperatura_final_agua_c,
                   medicion.peso_con_agua_inicial_kg, medicion.peso_con_agua_final_kg)
        if all(valor is None for valor in valores):
            continue
        if None in valores or medicion.olla.peso_seco_kg is None:
            raise ValueError(f'{nombre}, olla {numero}: faltan pesos o temperaturas')
        if (medicion.peso_con_agua_inicial_kg < medicion.olla.peso_seco_kg
                or medicion.peso_con_agua_final_kg < medicion.olla.peso_seco_kg):
            raise ValueError(f'{nombre}, olla {numero}: el peso con agua debe ser mayor o igual al peso seco de la olla')
        if medicion.peso_con_agua_final_kg > medicion.peso_con_agua_inicial_kg:
            raise ValueError(f'{nombre}, olla {numero}: el peso final con agua supera al inicial')
        if not 0 <= medicion.temperatura_inicial_agua_c <= 110 or not 0 <= medicion.temperatura_final_agua_c <= 110:
            raise ValueError(f'{nombre}, olla {numero}: las temperaturas del agua deben estar entre 0 y 110 °C')
        if nombre != 'baja_potencia' and medicion.temperatura_inicial_agua_c >= condiciones.punto_ebullicion_c:
            raise ValueError(f'{nombre}, olla {numero}: la temperatura inicial debe ser menor que la de ebullición')
        if nombre != 'baja_potencia' and medicion.temperatura_final_agua_c < medicion.temperatura_inicial_agua_c:
            raise ValueError(f'{nombre}, olla {numero}: en alta potencia la temperatura final no puede ser menor que la inicial')
        if numero == 1:
            olla_principal = True
    if not olla_principal:
        raise ValueError(f'{nombre}: faltan las mediciones de la olla 1')


def crear_prueba_completa(datos):
    """Crea la prueba con todas sus mediciones en una sola transacción.

    Valida todo antes de escribir: si algo falla, no se inserta ninguna fila.
    Las fases y las muestras referencian las ollas por `numero_olla`, porque
    sus ids todavía no existen.
    """
    if not isinstance(datos, dict):
        raise ValueError('El cuerpo debe ser un objeto JSON')

    prueba_datos = datos.get('prueba', {})
    condiciones_datos = datos.get('condiciones', {})
    prueba_datos = {} if prueba_datos is None else prueba_datos
    condiciones_datos = {} if condiciones_datos is None else condiciones_datos
    if not isinstance(prueba_datos, dict) or not isinstance(condiciones_datos, dict):
        raise ValueError('prueba y condiciones deben ser objetos JSON')
    es_valida = prueba_datos.get('es_valida', True)
    if not isinstance(es_valida, bool):
        raise ValueError('es_valida debe ser booleano')
    if not es_valida and not _c_texto(prueba_datos.get('motivo_invalidez')):
        raise ValueError('motivo_invalidez es obligatorio cuando es_valida es false')
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
    if numero_repeticion is not None and numero_repeticion < 1:
        raise ValueError('numero_repeticion debe ser mayor o igual a 1')
    fecha_prueba = _c_fecha(prueba_datos.get('fecha'), 'fecha')
    if fecha_prueba is None:
        raise ValueError('El campo fecha es obligatorio')

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
    if condiciones.humedad_relativa_pct is not None and not 0 <= condiciones.humedad_relativa_pct <= 100:
        raise ValueError('humedad_relativa_pct debe estar entre 0 y 100')
    if condiciones.altitud_m is not None and condiciones.altitud_m < 0:
        raise ValueError('altitud_m no puede ser negativa')
    if condiciones.presion_atmosferica_kpa is not None and condiciones.presion_atmosferica_kpa <= 0:
        raise ValueError('presion_atmosferica_kpa debe ser mayor que cero')
    if condiciones.viento_ms is not None and condiciones.viento_ms < 0:
        raise ValueError('viento_ms no puede ser negativo')

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
        if ollas[numero_olla].peso_seco_kg is not None and ollas[numero_olla].peso_seco_kg < 0:
            raise ValueError(f'El peso seco de la olla {numero_olla} no puede ser negativo')
        if ollas[numero_olla].capacidad_l is not None and ollas[numero_olla].capacidad_l <= 0:
            raise ValueError(f'La capacidad de la olla {numero_olla} debe ser mayor que cero')

    if es_valida:
        for numero_olla, olla in ollas.items():
            if olla.peso_seco_kg is None or olla.capacidad_l is None:
                raise ValueError(f'La olla {numero_olla} requiere peso seco y capacidad para una prueba válida')

    tara = _c_decimal(prueba_datos.get('peso_recipiente_carbon_kg'), 'peso_recipiente_carbon_kg')
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

        if es_valida:
            _validar_medicion_fase(fase, tara, condiciones)
        fases.append(fase)

    if es_valida and not {'inicio_frio', 'baja_potencia'}.issubset(tipos_vistos):
        raise ValueError('Una prueba WBT válida requiere inicio_frio y baja_potencia; inicio_caliente es opcional')

    # Serializa la numeración dentro del conjunto para guardados simultáneos.
    db.session.query(ConjuntoPruebas.id).filter_by(id=conjunto_pruebas_id).with_for_update().one()
    if numero_repeticion is None:
        ultima = db.session.query(db.func.max(PruebaWBT.numero_repeticion)).filter_by(
            conjunto_pruebas_id=conjunto_pruebas_id
        ).scalar()
        numero_repeticion = (ultima or 0) + 1

    prueba = PruebaWBT(
        fecha=fecha_prueba,
        investigador_id=investigador_id,
        laboratorio_id=laboratorio_id,
        combustible_id=combustible_id,
        conjunto_pruebas_id=conjunto_pruebas_id,
        peso_recipiente_carbon_kg=tara,
        numero_repeticion=numero_repeticion,
        observaciones=_c_texto(prueba_datos.get('observaciones')),
        es_valida=es_valida,
        motivo_invalidez=_c_texto(prueba_datos.get('motivo_invalidez')) if not es_valida else None,
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
