-- ============================================================
-- SICEE - Script de creación de base de datos (PostgreSQL)
-- Unidades: temperaturas en °C, masas en kg, tiempos en minutos,
-- energía en kJ, poder calorífico en MJ/kg, potencia en kW.
--
-- NOTA: las tablas de emisiones (emisiones_prueba,
-- resultado_emisiones_fase y resultado_prueba) todavía no se
-- crean en este script.
-- ============================================================

-- ------------------------------------------------------------
-- Tipos
-- ------------------------------------------------------------
CREATE TYPE tipo_fase_enum AS ENUM (
    'inicio_frio',
    'inicio_caliente',
    'baja_potencia'
);

-- ------------------------------------------------------------
-- Catálogos
-- ------------------------------------------------------------
CREATE TABLE investigador (
    id      INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre  VARCHAR(150) NOT NULL
);

CREATE TABLE laboratorio (
    id           INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    institucion  VARCHAR(150) NOT NULL,
    direccion    VARCHAR(255),
    descripcion  VARCHAR(500)
);

CREATE TABLE estufa (
    id               INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    marca            VARCHAR(100),
    fabricante       VARCHAR(100),
    area_camara_cm2  DECIMAL(12,4),
    altura_cm        DECIMAL(12,4),
    numero_hornillas INTEGER,
    material         VARCHAR(100),
    descripcion      VARCHAR(500)
);

CREATE TABLE condiciones_ambientales (
    id                       INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    temperatura_c            DECIMAL(6,2),
    humedad_relativa_pct     DECIMAL(5,2),
    altitud_m                DECIMAL(7,2),
    presion_atmosferica_kpa  DECIMAL(7,3),
    viento_ms                DECIMAL(5,2),
    condicion_viento         VARCHAR(500),
    punto_ebullicion_c       DECIMAL(6,2)
);

CREATE TABLE combustible (
    id                           INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    tipo                         VARCHAR(100) NOT NULL,
    longitud_combustible_cm      DECIMAL(8,2),
    ancho_combustible_cm         DECIMAL(8,2),
    humedad_pct                  DECIMAL(5,2),
    poder_calorifico_neto_mj_kg  DECIMAL(8,3),
    poder_calorifico_bruto_mj_kg DECIMAL(8,3),
    poder_calorifico_carbon_mj_kg DECIMAL(8,3),
    contenido_carbono_carbon_pct DECIMAL(5,2),
    tipo_alimentacion            VARCHAR(100),
    contenido_carbono_pct        DECIMAL(5,2),
    descripcion                  VARCHAR(500)
);

-- ------------------------------------------------------------
-- Conjunto de pruebas
-- ------------------------------------------------------------
CREATE TABLE conjunto_pruebas (
    id           INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    estufa_id    INTEGER NOT NULL REFERENCES estufa(id),
    descripcion  VARCHAR(500)
);

-- ------------------------------------------------------------
-- Prueba WBT
-- ------------------------------------------------------------
CREATE TABLE prueba_wbt (
    id                          INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    uuid                        UUID NOT NULL UNIQUE DEFAULT gen_random_uuid(),
    fecha                       TIMESTAMP NOT NULL,
    investigador_id             INTEGER NOT NULL REFERENCES investigador(id),
    laboratorio_id              INTEGER NOT NULL REFERENCES laboratorio(id),
    combustible_id              INTEGER NOT NULL REFERENCES combustible(id),
    condiciones_ambientales_id  INTEGER NOT NULL REFERENCES condiciones_ambientales(id),
    conjunto_pruebas_id         INTEGER NOT NULL REFERENCES conjunto_pruebas(id),
    peso_recipiente_carbon_kg   DECIMAL(8,4),
    numero_repeticion           INTEGER NOT NULL DEFAULT 1,
    es_valida                   BOOLEAN NOT NULL DEFAULT TRUE,
    motivo_invalidez            VARCHAR(500),
    version_protocolo           VARCHAR(10) NOT NULL DEFAULT '4.2.3',
    observaciones               VARCHAR,
    created_at                  TIMESTAMP NOT NULL DEFAULT now(),
    updated_at                  TIMESTAMP NOT NULL DEFAULT now(),
    UNIQUE (conjunto_pruebas_id, numero_repeticion)
);

CREATE TABLE fase_prueba (
    id                           INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    prueba_wbt_id                INTEGER NOT NULL REFERENCES prueba_wbt(id) ON DELETE CASCADE,
    tipo_fase                    tipo_fase_enum NOT NULL,
    t_inicial                    TIMESTAMP(3),
    t_final                      TIMESTAMP(3),
    peso_combustible_inicial_kg  DECIMAL(8,4),
    peso_combustible_final_kg    DECIMAL(8,4),
    peso_carbon_con_recipiente_kg DECIMAL(8,4),
    peso_cenizas_kg              DECIMAL(8,4),
    observaciones                VARCHAR(500),
    UNIQUE (prueba_wbt_id, tipo_fase)
);

-- ------------------------------------------------------------
-- Ollas y mediciones de agua por fase
-- ------------------------------------------------------------
CREATE TABLE olla (
    id              INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    prueba_wbt_id   INTEGER NOT NULL REFERENCES prueba_wbt(id) ON DELETE CASCADE,
    numero_olla     INTEGER NOT NULL,
    peso_seco_kg    DECIMAL(8,4),
    capacidad_l     DECIMAL(5,2),
    UNIQUE (prueba_wbt_id, numero_olla)
);

CREATE TABLE olla_fase (
    id                          INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    olla_id                     INTEGER NOT NULL REFERENCES olla(id) ON DELETE CASCADE,
    fase_id                     INTEGER NOT NULL REFERENCES fase_prueba(id) ON DELETE CASCADE,
    temperatura_inicial_agua_c  DECIMAL(5,2),
    temperatura_final_agua_c    DECIMAL(5,2),
    peso_con_agua_inicial_kg    DECIMAL(8,4),
    peso_con_agua_final_kg      DECIMAL(8,4),
    UNIQUE (olla_id, fase_id)
);

COMMENT ON TABLE olla_fase IS
    'La masa de agua se obtiene con peso_con_agua_inicial_kg o peso_con_agua_final_kg menos olla.peso_seco_kg.';

-- ------------------------------------------------------------
-- Resultados de cálculo térmico
-- ------------------------------------------------------------
CREATE TABLE resultado_fase (
    id                                      INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    fase_id                                 INTEGER NOT NULL UNIQUE REFERENCES fase_prueba(id) ON DELETE CASCADE,
    tiempo_fase_min                         DECIMAL(8,2),
    masa_agua_inicial_kg                    DECIMAL(8,4),
    masa_agua_final_kg                      DECIMAL(8,4),
    masa_agua_evaporada_kg                  DECIMAL(6,4),
    masa_agua_efectiva_kg                   DECIMAL(6,4),
    combustible_consumido_kg                DECIMAL(6,4),
    tiempo_ebullicion_min                   DECIMAL(8,3),
    tiempo_ebullicion_corregido_min         DECIMAL(8,3),
    energia_util_kj                         DECIMAL(8,3),
    energia_combustible_kj                  DECIMAL(8,3),
    eficiencia_termica_pct                  DECIMAL(8,3),
    consumo_especifico_g_l                  DECIMAL(8,3),
    velocidad_combustion_g_min              DECIMAL(8,3),
    potencia_fase_kw                        DECIMAL(8,3),
    energia_especifica_corregida_kj_l       DECIMAL(8,3),
    combustible_seco_equivalente_kg         DECIMAL(6,4),
    cambio_carbon_kg                        DECIMAL(6,4),
    consumo_especifico_corregido_g_l        DECIMAL(8,3)
);

COMMENT ON TABLE resultado_fase IS
    'Resultado agregado por fase. Las masas y energías de agua se suman sobre todas las ollas de olla_fase; el combustible y los tiempos son de la fase.';

-- ------------------------------------------------------------
-- Mediciones opcionales
-- Se mantiene por ahora la definición anterior. Su actualización
-- (pm_ug_m3, fondos y totales) queda pendiente junto con el
-- módulo de emisiones.
-- ------------------------------------------------------------
CREATE TABLE mediciones_opcionales (
    id                       INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    fase_id                  INTEGER NOT NULL UNIQUE REFERENCES fase_prueba(id) ON DELETE CASCADE,
    temperatura_ducto_c      DECIMAL(7,2),
    co_ppm                   DECIMAL(10,3),
    pm_ug_m3                 DECIMAL(10,3),
    co2_ppm                  DECIMAL(10,3),
    co2_fondo_ppm            DECIMAL(10,3),
    co_fondo_ppm             DECIMAL(10,3),
    pm_fondo_ug_m3           DECIMAL(10,3),
    co2_total_g              DECIMAL(12,3),
    co_total_g               DECIMAL(12,3),
    pm_total_g               DECIMAL(12,6)
);

-- ------------------------------------------------------------
-- Índices (PostgreSQL no indexa las llaves foráneas automáticamente)
-- ------------------------------------------------------------
CREATE INDEX idx_conjunto_pruebas_estufa     ON conjunto_pruebas (estufa_id);

CREATE INDEX idx_prueba_wbt_fecha            ON prueba_wbt (fecha DESC);
CREATE INDEX idx_prueba_wbt_investigador     ON prueba_wbt (investigador_id);
CREATE INDEX idx_prueba_wbt_laboratorio      ON prueba_wbt (laboratorio_id);
CREATE INDEX idx_prueba_wbt_combustible      ON prueba_wbt (combustible_id);
CREATE INDEX idx_prueba_wbt_condiciones      ON prueba_wbt (condiciones_ambientales_id);
CREATE INDEX idx_prueba_wbt_conjunto         ON prueba_wbt (conjunto_pruebas_id);

CREATE INDEX idx_fase_prueba_prueba          ON fase_prueba (prueba_wbt_id);

CREATE INDEX idx_olla_prueba                 ON olla (prueba_wbt_id);
CREATE INDEX idx_olla_fase_olla              ON olla_fase (olla_id);
CREATE INDEX idx_olla_fase_fase              ON olla_fase (fase_id);
