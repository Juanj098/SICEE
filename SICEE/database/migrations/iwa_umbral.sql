-- WBT 4.2.3, hoja Lists (filas 15–22). T0 es el nivel residual.
BEGIN;
CREATE TABLE IF NOT EXISTS iwa_umbral (
    version INTEGER NOT NULL CHECK (version > 0),
    metrica VARCHAR(64) NOT NULL,
    mayor_es_mejor BOOLEAN NOT NULL,
    t1 NUMERIC NOT NULL,
    t2 NUMERIC NOT NULL,
    t3 NUMERIC NOT NULL,
    t4 NUMERIC NOT NULL,
    PRIMARY KEY (version, metrica),
    CHECK (CASE WHEN mayor_es_mejor THEN t1 < t2 AND t2 < t3 AND t3 < t4
               ELSE t1 > t2 AND t2 > t3 AND t3 > t4 END)
);
INSERT INTO iwa_umbral (version, metrica, mayor_es_mejor, t1, t2, t3, t4) VALUES
    (1, 'eficiencia_alta_pct', true, 15, 25, 35, 45),
    (1, 'consumo_especifico_baja_mj_min_l', false, 0.05, 0.039, 0.028, 0.017),
    (1, 'co_alta_g_mj', false, 16, 11, 9, 8),
    (1, 'co_baja_g_min_l', false, 0.2, 0.13, 0.1, 0.09),
    (1, 'pm_alta_mg_mj', false, 979, 386, 168, 41),
    (1, 'pm_baja_mg_min_l', false, 8, 4, 2, 1),
    (1, 'co_interior_g_min', false, 0.97, 0.62, 0.49, 0.42),
    (1, 'pm_interior_mg_min', false, 40, 17, 8, 2)
ON CONFLICT (version, metrica) DO NOTHING;
COMMIT;
