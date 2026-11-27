-- Para volúmenes existentes de PostgreSQL 16. Los lotes previos quedan sin especie.
BEGIN;
CREATE TABLE IF NOT EXISTS especie_madera (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    especie VARCHAR(100) NOT NULL,
    nombres_comunes VARCHAR(500),
    poder_calorifico_bruto_mj_kg DECIMAL(8,3),
    poder_calorifico_neto_mj_kg DECIMAL(8,3),
    poder_calorifico_carbon_mj_kg DECIMAL(8,3),
    contenido_carbono_pct DECIMAL(5,2),
    fuente_codigo INTEGER,
    fuente VARCHAR(500),
    activo BOOLEAN NOT NULL DEFAULT TRUE
);
-- Admite también instalaciones con la primera versión de la restricción,
-- que permitía repetir (especie, NULL). Si hay duplicados, falla sin borrar filas.
ALTER TABLE especie_madera DROP CONSTRAINT IF EXISTS uq_especie_madera_especie_fuente;
ALTER TABLE especie_madera ADD CONSTRAINT uq_especie_madera_especie_fuente
    UNIQUE NULLS NOT DISTINCT (especie, fuente_codigo);
ALTER TABLE combustible ADD COLUMN IF NOT EXISTS especie_id INTEGER REFERENCES especie_madera(id);
COMMIT;
