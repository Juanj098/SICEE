#!/usr/bin/env python3
"""Importa database/data/especies_madera.json a la tabla especie_madera.

Uso, desde SICEE/backend con su venv:

    .venv/bin/python ../database/import_especies.py
    DB_NAME=sicee_tmp .venv/bin/python ../database/import_especies.py

El script es idempotente: usa ON CONFLICT (especie, fuente_codigo) y
actualiza los valores si la especie ya existe.
"""
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
BACKEND = RAIZ.parent / "backend"
sys.path.insert(0, str(BACKEND))

from sqlalchemy.dialects.postgresql import insert

from app import create_app
from app.extensions import db
from app.modules.catalogos.models import EspecieMadera

DATOS = RAIZ / "data" / "especies_madera.json"

CAMPOS_ACTUALIZABLES = (
    "nombres_comunes",
    "poder_calorifico_bruto_mj_kg",
    "poder_calorifico_neto_mj_kg",
    "poder_calorifico_carbon_mj_kg",
    "contenido_carbono_pct",
    "fuente",
)


def limpiar(texto):
    """Normaliza espacios y quita marcas invisibles de dirección."""
    if texto is None:
        return None
    texto = str(texto).replace("\u200e", "").replace("\u200f", "")
    return " ".join(texto.split()) or None


def cargar(ruta):
    with open(ruta, encoding="utf-8") as archivo:
        crudo = json.load(archivo)

    filas = {}
    for item in crudo:
        especie = limpiar(item.get("especie"))
        if not especie:
            continue

        clave = (especie, item.get("fuente_codigo"))
        if clave in filas:
            continue

        filas[clave] = {
            "especie": especie,
            "nombres_comunes": limpiar(item.get("nombres_comunes")),
            "poder_calorifico_bruto_mj_kg": item.get("poder_calorifico_bruto_mj_kg"),
            "poder_calorifico_neto_mj_kg": item.get("poder_calorifico_neto_mj_kg"),
            "poder_calorifico_carbon_mj_kg": item.get("poder_calorifico_carbon_mj_kg"),
            "contenido_carbono_pct": item.get("contenido_carbono_pct"),
            "fuente_codigo": item.get("fuente_codigo"),
            "fuente": limpiar(item.get("fuente")),
        }

    return list(filas.values())


def importar(filas):
    existentes = {
        (especie, fuente_codigo)
        for especie, fuente_codigo in db.session.query(
            EspecieMadera.especie, EspecieMadera.fuente_codigo
        ).all()
    }

    stmt = insert(EspecieMadera).values(filas)
    stmt = stmt.on_conflict_do_update(
        constraint="uq_especie_madera_especie_fuente",
        set_={
            campo: getattr(stmt.excluded, campo)
            for campo in CAMPOS_ACTUALIZABLES
        },
    )
    db.session.execute(stmt)
    db.session.commit()

    insertadas = sum(
        1 for fila in filas
        if (fila["especie"], fila["fuente_codigo"]) not in existentes
    )
    return insertadas, len(filas) - insertadas


def main():
    app = create_app()
    with app.app_context():
        filas = cargar(DATOS)
        if not filas:
            print("No hay especies para importar.")
            return
        insertadas, actualizadas = importar(filas)
        total = EspecieMadera.query.count()

    print(f"Especies procesadas: {len(filas)}")
    print(f"Insertadas: {insertadas} | Actualizadas: {actualizadas}")
    print(f"Total en especie_madera: {total}")


if __name__ == "__main__":
    main()
