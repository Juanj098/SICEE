-- ============================================================
-- SICEE - Script de creación de base de datos (PostgreSQL)
-- Unidades: temperaturas en °C, masas en kg, tiempos en minutos,
-- energía en kJ, poder calorífico en MJ/kg, potencia en kW.
-- ============================================================

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
    area_camara_cm2  DECIMAL(10,2),
    altura_cm        DECIMAL(8,2),
    material         VARCHAR(100),
    descripcion      VARCHAR(500)
);

CREATE TABLE condiciones_ambientales (
    id                       INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    temperatura_c            DECIMAL(5,2),
    humedad_relativa_pct     DECIMAL(5,2),
    presion_atmosferica_kpa  DECIMAL(7,3),
    viento_ms                DECIMAL(5,2),
    punto_ebullicion_c       DECIMAL(5,2)
);

CREATE TABLE combustible (
    id                           INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    tipo                         VARCHAR(100) NOT NULL,
    tamanio_cm                   DECIMAL(8,2),
    peso_kg                      DECIMAL(8,4),
    humedad_pct                  DECIMAL(5,2),
    poder_calorifico_neto_mj_kg  DECIMAL(8,3),
    poder_calorifico_bruto_mj_kg DECIMAL(8,3),
    tipo_alimentacion            VARCHAR(100),
    contenido_carbono_pct        DECIMAL(5,2)
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
    estufa_id                   INTEGER NOT NULL REFERENCES estufa(id),
    combustible_id              INTEGER NOT NULL REFERENCES combustible(id),
    condiciones_ambientales_id  INTEGER NOT NULL REFERENCES condiciones_ambientales(id),
    observaciones               VARCHAR(1000),
    created_at                  TIMESTAMP NOT NULL DEFAULT now(),
    updated_at                  TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE fase_prueba (
    id                           INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    prueba_wbt_id                INTEGER NOT NULL REFERENCES prueba_wbt(id) ON DELETE CASCADE,
    tipo_fase                    VARCHAR(48) NOT NULL,
    numero_repeticion            INTEGER NOT NULL,
    t_inicial                    TIMESTAMP(3),
    t_final                      TIMESTAMP(3),
    temperatura_inicial_agua_c   DECIMAL(5,2),
    temperatura_final_agua_c     DECIMAL(5,2),
    peso_olla_seco_kg            DECIMAL(8,4),
    peso_olla_agua_inicial_kg    DECIMAL(8,4),
    peso_olla_agua_final_kg      DECIMAL(8,4),
    peso_combustible_inicial_kg  DECIMAL(8,4),
    peso_combustible_final_kg    DECIMAL(8,4)
);

CREATE TABLE resultado_fase (
    id                             INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    fase_id                        INTEGER NOT NULL UNIQUE REFERENCES fase_prueba(id) ON DELETE CASCADE,
    tiempo_fase_min                DECIMAL(8,2),
    masa_agua_inicial_kg           DECIMAL(8,4),
    masa_agua_final_kg             DECIMAL(8,4),
    masa_agua_evaporada_kg         DECIMAL(8,4),
    combustible_consumido_kg       DECIMAL(8,4),
    tiempo_ebullicion_min          DECIMAL(8,2),
    energia_util_kj                DECIMAL(12,3),
    energia_combustible_kj         DECIMAL(12,3),
    eficiencia_termica_pct         DECIMAL(6,2),
    consumo_especifico             DECIMAL(10,3),
    velocidad_combustion_g_min     DECIMAL(10,3),
    potencia_fase_kw               DECIMAL(10,3),
    humedad_ambiente_promedio_pct  DECIMAL(5,2)
);

CREATE TABLE mediciones_opcionales (
    id                       INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    fase_id                  INTEGER NOT NULL UNIQUE REFERENCES fase_prueba(id) ON DELETE CASCADE,
    co_ppm                   DECIMAL(10,3),
    pm_mg_m3                 DECIMAL(10,3),
    co2_ppm                  DECIMAL(10,3),
    temperatura_ducto_c      DECIMAL(7,2),
    presion_atmosferica_kpa  DECIMAL(7,3)
);

-- ------------------------------------------------------------
-- Índices (PostgreSQL no indexa las llaves foráneas automáticamente)
-- ------------------------------------------------------------
CREATE INDEX idx_prueba_wbt_fecha          ON prueba_wbt (fecha DESC);
CREATE INDEX idx_prueba_wbt_investigador   ON prueba_wbt (investigador_id);
CREATE INDEX idx_prueba_wbt_laboratorio    ON prueba_wbt (laboratorio_id);
CREATE INDEX idx_prueba_wbt_estufa         ON prueba_wbt (estufa_id);
CREATE INDEX idx_prueba_wbt_combustible    ON prueba_wbt (combustible_id);
CREATE INDEX idx_prueba_wbt_condiciones    ON prueba_wbt (condiciones_ambientales_id);
CREATE INDEX idx_fase_prueba_prueba        ON fase_prueba (prueba_wbt_id);