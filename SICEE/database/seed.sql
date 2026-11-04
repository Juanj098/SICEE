-- ============================================================
-- SICEE - Datos de ejemplo
-- Ejecutar DESPUÉS de database/init.sql
--
--   docker exec -i postgres-sicee \
--     psql -U SICEE -d postgres-sicee < database/seed.sql
--
-- Reinicia las tablas y las secuencias de ID.
-- ============================================================

TRUNCATE TABLE
    resultado_fase,
    mediciones_opcionales,
    fase_prueba,
    prueba_wbt,
    combustible,
    condiciones_ambientales,
    estufa,
    laboratorio,
    investigador
RESTART IDENTITY CASCADE;

-- ------------------------------------------------------------
-- Catálogos
-- ------------------------------------------------------------
INSERT INTO investigador (nombre) VALUES
    ('Dra. María González'),
    ('Ing. Carlos Ramírez');

INSERT INTO laboratorio (institucion, direccion, descripcion) VALUES
    ('CII - Centro de Investigación e Innovación', 'Quito, Ecuador',
     'Laboratorio de eficiencia energética'),
    ('Laboratorio de Biomateriales', 'Loja, Ecuador',
     'Laboratorio de caracterización de biomasa');

INSERT INTO estufa
    (marca, fabricante, area_camara_cm2, altura_cm, material, descripcion)
VALUES
    ('Estufa Rocket A1', 'CII', 625.00, 45.00, 'Acero inoxidable',
     'Estufa de prueba para biomasa'),
    ('Estufa Rocket B2', 'CII', 900.00, 50.00, 'Acero al carbono',
     'Estufa de mayor capacidad');

INSERT INTO condiciones_ambientales
    (temperatura_c, humedad_relativa_pct, presion_atmosferica_kpa,
     viento_ms, punto_ebullicion_c)
VALUES
    (18.50, 65.00, 101.325, 1.20, 98.00),
    (20.10, 58.00, 101.100, 0.80, 98.00);

INSERT INTO combustible
    (tipo, tamanio_cm, peso_kg, humedad_pct, poder_calorifico_neto_mj_kg,
     poder_calorifico_bruto_mj_kg, tipo_alimentacion, contenido_carbono_pct)
VALUES
    ('Leña de eucalipto', 5.00, 1.2000, 8.00, 28.500, 30.200,
     'Manual', 48.50),
    ('Briquetas de aserrín', 4.00, 1.0000, 10.00, 26.800, 29.100,
     'Manual', 46.00);

-- ------------------------------------------------------------
-- Prueba 1: completa (con resultados)
-- ------------------------------------------------------------
INSERT INTO prueba_wbt
    (fecha, investigador_id, laboratorio_id, estufa_id, combustible_id,
     condiciones_ambientales_id, observaciones)
VALUES
    ('2026-11-02 08:00:00', 1, 1, 1, 1, 1,
     'Prueba WBT completa: inicio frío, inicio caliente y baja potencia.');

INSERT INTO fase_prueba
    (prueba_wbt_id, tipo_fase, numero_repeticion, t_inicial, t_final,
     temperatura_inicial_agua_c, temperatura_final_agua_c,
     peso_olla_seco_kg, peso_olla_agua_inicial_kg,
     peso_olla_agua_final_kg, peso_combustible_inicial_kg,
     peso_combustible_final_kg)
VALUES
    (1, 'inicio_frio', 1, '2026-11-02 08:00:00', '2026-11-02 08:38:00',
     24.00, 98.00, 0.8500, 5.8500, 4.3500, 1.2000, 0.6000),
    (1, 'inicio_caliente', 1, '2026-11-02 08:45:00', '2026-11-02 09:23:00',
     92.00, 98.00, 0.8500, 5.8500, 4.5000, 1.2000, 0.6500),
    (1, 'baja_potencia', 1, '2026-11-02 09:30:00', '2026-11-02 10:15:00',
     98.00, 98.00, 0.8500, 4.3500, 3.7500, 0.7000, 0.4000);

INSERT INTO resultado_fase
    (fase_id, tiempo_fase_min, masa_agua_inicial_kg, masa_agua_final_kg,
     masa_agua_evaporada_kg, combustible_consumido_kg,
     tiempo_ebullicion_min, energia_util_kj, energia_combustible_kj,
     eficiencia_termica_pct, consumo_especifico,
     velocidad_combustion_g_min, potencia_fase_kw,
     humedad_ambiente_promedio_pct)
VALUES
    (1, 38.00, 5.0000, 3.5000, 1.5000, 0.6000, 30.00,
     4938.820, 15732.000, 31.39, 0.110, 15.789, 6.900, 65.00),
    (2, 38.00, 5.0000, 3.6500, 1.3500, 0.5500, 8.00,
     3176.580, 14421.000, 22.03, 0.101, 14.474, 6.325, 65.00),
    (3, 45.00, 3.5000, 2.9000, 0.6000, 0.3000, NULL,
     1356.000, 7866.000, 17.24, 0.079, 6.667, 2.913, 65.00);

INSERT INTO mediciones_opcionales
    (fase_id, co_ppm, pm_mg_m3, co2_ppm, temperatura_ducto_c,
     presion_atmosferica_kpa)
VALUES
    (1, 120.500, 3.200, 45000.000, 85.30, 101.325),
    (2, 110.000, 2.800, 43000.000, 88.10, 101.325);

-- ------------------------------------------------------------
-- Prueba 2: registrada, sin cálculos todavía
-- ------------------------------------------------------------
INSERT INTO prueba_wbt
    (fecha, investigador_id, laboratorio_id, estufa_id, combustible_id,
     condiciones_ambientales_id, observaciones)
VALUES
    ('2026-11-03 08:00:00', 2, 2, 2, 2, 2,
     'Prueba registrada pendiente de cálculo.');

INSERT INTO fase_prueba
    (prueba_wbt_id, tipo_fase, numero_repeticion, t_inicial, t_final,
     temperatura_inicial_agua_c, temperatura_final_agua_c,
     peso_olla_seco_kg, peso_olla_agua_inicial_kg,
     peso_olla_agua_final_kg, peso_combustible_inicial_kg,
     peso_combustible_final_kg)
VALUES
    (2, 'inicio_frio', 1, '2026-11-03 08:00:00', '2026-11-03 08:40:00',
     25.00, 98.00, 0.9000, 5.9000, 4.4000, 1.1500, 0.5600),
    (2, 'inicio_caliente', 1, '2026-11-03 08:50:00', '2026-11-03 09:30:00',
     90.00, 98.00, 0.9000, 5.9000, 4.6000, 1.1000, 0.6000);
