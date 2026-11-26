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
    muestra_humedad,
    olla_fase,
    olla,
    fase_prueba,
    prueba_wbt,
    conjunto_pruebas,
    combustible,
    condiciones_ambientales,
    estufa,
    laboratorio,
    investigador
RESTART IDENTITY CASCADE;

-- ------------------------------------------------------------
-- Catálogos
-- ------------------------------------------------------------
INSERT INTO investigador (nombre, activo) VALUES
    ('Dra. María González', TRUE),
    ('Ing. Carlos Ramírez', TRUE);

INSERT INTO laboratorio (institucion, direccion, descripcion) VALUES
    ('CII - Centro de Investigación e Innovación', 'Quito, Ecuador',
     'Laboratorio de eficiencia energética'),
    ('Laboratorio de Biomateriales', 'Loja, Ecuador',
     'Laboratorio de caracterización de biomasa');

INSERT INTO estufa
    (marca, fabricante, area_camara_cm2, altura_cm, numero_hornillas,
     material, descripcion)
VALUES
    ('Estufa Rocket A1', 'CII', 625.0000, 45.0000, 1,
     'Acero inoxidable', 'Estufa de prueba para biomasa'),
    ('Estufa Rocket B2', 'CII', 900.0000, 50.0000, 2,
     'Acero al carbono', 'Estufa de mayor capacidad');

INSERT INTO condiciones_ambientales
    (temperatura_c, humedad_relativa_pct, altitud_m,
     presion_atmosferica_kpa, viento_ms, condicion_viento,
     punto_ebullicion_c)
VALUES
    (18.50, 65.00, 2850.00, 101.325, 1.20, 'Viento leve', 98.00),
    (20.10, 58.00, 2100.00, 101.100, 0.80, 'Sin viento', 98.00);

INSERT INTO combustible
    (tipo, longitud_combustible_cm, ancho_combustible_cm,
     poder_calorifico_neto_mj_kg, poder_calorifico_bruto_mj_kg,
     poder_calorifico_carbon_mj_kg, contenido_carbono_carbon_pct,
     tipo_alimentacion, contenido_carbono_pct, descripcion)
VALUES
    ('Leña de eucalipto', 30.00, 8.00, 18.500, 19.800,
     28.500, 80.00, 'Manual', 48.50,
     'Trozos de eucalipto de aproximadamente 30 cm'),
    ('Briquetas de aserrín', 10.00, 6.00, 16.800, 18.000,
     25.000, 75.00, 'Manual', 46.00,
     'Briquetas cilíndricas de aserrín');

-- ------------------------------------------------------------
-- Conjuntos de prueba
-- ------------------------------------------------------------
INSERT INTO conjunto_pruebas (estufa_id, descripcion) VALUES
    (1, 'Conjunto de pruebas estufa Rocket A1'),
    (2, 'Conjunto de pruebas estufa Rocket B2');

-- ------------------------------------------------------------
-- Prueba 1: completa (con resultados)
-- ------------------------------------------------------------
INSERT INTO prueba_wbt
    (fecha, investigador_id, laboratorio_id, combustible_id,
     condiciones_ambientales_id, conjunto_pruebas_id,
     peso_recipiente_carbon_kg, numero_repeticion, es_valida,
     version_protocolo, observaciones)
VALUES
    ('2026-11-02 08:00:00', 1, 1, 1, 1, 1, 0.1500, 1, TRUE, '4.2.3',
     'Prueba WBT completa con dos ollas: inicio frío, inicio caliente y baja potencia.');

-- Humedad del combustible: 3 leños × 3 mediciones. Promedio = 8.00 %.
INSERT INTO muestra_humedad
    (prueba_wbt_id, numero_lenio, numero_medicion, humedad_pct)
VALUES
    (1, 1, 1, 8.00), (1, 1, 2, 8.40), (1, 1, 3, 7.60),
    (1, 2, 1, 8.20), (1, 2, 2, 7.80), (1, 2, 3, 8.10),
    (1, 3, 1, 7.90), (1, 3, 2, 8.30), (1, 3, 3, 7.70);

INSERT INTO fase_prueba
    (prueba_wbt_id, tipo_fase, t_inicial, t_final,
     peso_combustible_inicial_kg, peso_combustible_final_kg,
     peso_carbon_con_recipiente_kg, peso_cenizas_kg, observaciones)
VALUES
    (1, 'inicio_frio', '2026-11-02 08:00:00', '2026-11-02 08:30:00',
     1.2000, 0.5500, 0.2000, 0.0500, 'Fase de inicio frío, termina cuando hierve la olla 1'),
    (1, 'inicio_caliente', '2026-11-02 08:45:00', '2026-11-02 08:53:00',
     1.2000, 0.6000, 0.1900, 0.0400, 'Fase de inicio caliente, termina cuando hierve la olla 1'),
    (1, 'baja_potencia', '2026-11-02 09:30:00', '2026-11-02 10:15:00',
     0.7000, 0.4200, 0.1700, 0.0300, 'Fase de baja potencia, 45 min');

INSERT INTO olla
    (prueba_wbt_id, numero_olla, peso_seco_kg, capacidad_l)
VALUES
    (1, 1, 0.8500, 5.00),
    (1, 2, 0.7000, 3.00);

INSERT INTO olla_fase
    (olla_id, fase_id, temperatura_inicial_agua_c, temperatura_final_agua_c,
     peso_con_agua_inicial_kg, peso_con_agua_final_kg)
VALUES
    -- Fase 1: inicio frío
    (1, 1, 24.00, 98.00, 5.8500, 5.1500),
    (2, 1, 24.00, 98.00, 3.7000, 3.3000),
    -- Fase 2: inicio caliente
    (1, 2, 92.00, 98.00, 5.8500, 5.2500),
    (2, 2, 92.00, 98.00, 3.7000, 3.4000),
    -- Fase 3: baja potencia
    (1, 3, 98.00, 98.00, 4.3500, 3.9500),
    (2, 3, 98.00, 98.00, 2.7000, 2.5000);

INSERT INTO resultado_fase
    (fase_id, tiempo_fase_min, masa_agua_inicial_kg, masa_agua_final_kg,
     masa_agua_evaporada_kg, masa_agua_efectiva_kg,
     combustible_consumido_kg, tiempo_ebullicion_min,
     tiempo_ebullicion_corregido_min, energia_util_kj,
     energia_combustible_kj, eficiencia_termica_pct,
     consumo_especifico_g_l, velocidad_combustion_g_min,
     potencia_fase_kw, energia_especifica_corregida_kj_l,
     combustible_seco_equivalente_kg, cambio_carbon_kg,
     consumo_especifico_corregido_g_l)
VALUES
    (1, 30.00, 8.0000, 6.9000, 1.1000, 6.9000,
     0.6500, 30.00, 30.405, 4964.112,
     9503.331, 52.235, 74.448, 17.123,
     5.280, 1395.906, 0.5137, 0.0500, 75.454),
    (2, 8.00, 8.0000, 7.1000, 0.9000, 7.1000,
     0.6000, 8.00, 100.000, 2234.928,
     8947.690, 24.978, 68.121, 60.457,
     18.641, 15752.976, 0.4837, 0.0400, 851.512),
    (3, 45.00, 5.5000, 4.9000, 0.6000, 4.9000,
     0.2800, NULL, NULL, 1356.000,
     5562.589, 24.377, 61.363, 6.682,
     2.060, 1135.222, 0.3007, -0.0300, NULL);

INSERT INTO mediciones_opcionales
    (fase_id, temperatura_ducto_c, co_ppm, pm_ug_m3, co2_ppm,
     co2_fondo_ppm, co_fondo_ppm, pm_fondo_ug_m3)
VALUES
    (1, 85.30, 120.500, 3200.000, 45000.000, 420.000, 0.500, 5.000),
    (2, 88.10, 110.000, 2800.000, 43000.000, 420.000, 0.500, 5.000),
    (3, 90.50, 95.000, 2100.000, 41000.000, 420.000, 0.500, 5.000);

-- ------------------------------------------------------------
-- Prueba 2: registrada, sin cálculos todavía
-- ------------------------------------------------------------
INSERT INTO prueba_wbt
    (fecha, investigador_id, laboratorio_id, combustible_id,
     condiciones_ambientales_id, conjunto_pruebas_id,
     peso_recipiente_carbon_kg, numero_repeticion, es_valida,
     version_protocolo, observaciones)
VALUES
    ('2026-11-03 08:00:00', 2, 2, 2, 2, 2, 0.1500, 1, TRUE, '4.2.3',
     'Prueba registrada pendiente de cálculo.');

-- Humedad del combustible: 3 leños × 3 mediciones. Promedio = 10.00 %.
INSERT INTO muestra_humedad
    (prueba_wbt_id, numero_lenio, numero_medicion, humedad_pct)
VALUES
    (2, 1, 1, 10.40), (2, 1, 2, 9.60), (2, 1, 3, 10.10),
    (2, 2, 1, 9.90), (2, 2, 2, 10.20), (2, 2, 3, 9.80),
    (2, 3, 1, 10.30), (2, 3, 2, 9.70), (2, 3, 3, 10.00);

INSERT INTO fase_prueba
    (prueba_wbt_id, tipo_fase, t_inicial, t_final,
     peso_combustible_inicial_kg, peso_combustible_final_kg,
     peso_carbon_con_recipiente_kg, peso_cenizas_kg, observaciones)
VALUES
    (2, 'inicio_frio', '2026-11-03 08:00:00', '2026-11-03 08:32:00',
     1.1500, 0.5200, 0.1800, 0.0400, 'Fase de inicio frío, termina cuando hierve la olla 1'),
    (2, 'inicio_caliente', '2026-11-03 08:50:00', '2026-11-03 09:00:00',
     1.1000, 0.5500, 0.1700, 0.0300, 'Fase de inicio caliente, termina cuando hierve la olla 1');

INSERT INTO olla
    (prueba_wbt_id, numero_olla, peso_seco_kg, capacidad_l)
VALUES
    (2, 1, 0.9000, 5.00);

INSERT INTO olla_fase
    (olla_id, fase_id, temperatura_inicial_agua_c, temperatura_final_agua_c,
     peso_con_agua_inicial_kg, peso_con_agua_final_kg)
VALUES
    (3, 4, 25.00, 98.00, 5.9000, 4.8000),
    (3, 5, 90.00, 98.00, 5.9000, 5.1000);

INSERT INTO mediciones_opcionales
    (fase_id, temperatura_ducto_c, co_ppm, pm_ug_m3, co2_ppm,
     co2_fondo_ppm, co_fondo_ppm, pm_fondo_ug_m3)
VALUES
    (4, 84.00, 130.000, 3500.000, 46000.000, 420.000, 0.500, 5.000),
    (5, 86.50, 115.000, 3000.000, 44000.000, 420.000, 0.500, 5.000);
