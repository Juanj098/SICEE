# Modelo de datos propuesto para SICEE

Este documento propone una estructura relacional para PostgreSQL basada en las tablas de `Docs/Hoja de cálculo sin título.xlsx` y en las variables del protocolo WBT 4.2.3.

## Criterios de diseño

- `pruebas_wbt` es la entidad principal.
- Las fases pertenecen a una prueba y a una repetición.
- Las mediciones originales se almacenan separadas de los resultados calculados.
- Las claves foráneas deben representar las relaciones entre las tablas.
- Los resultados calculados pueden volver a generarse sin perder los datos originales.
- Las emisiones son opcionales y se relacionan con una fase específica.
- No se incluye gestión de usuarios, autenticación ni permisos.

## Modelo conceptual

```text
Investigador
      │
      ▼
Prueba WBT
 ├── Laboratorio
 ├── Estufa
 ├── Combustible
 ├── Condiciones ambientales
 └── Fases de prueba
       ├── Inicio frío
       ├── Inicio caliente
       └── Baja potencia
              ├── Mediciones
              ├── Resultados
              └── Emisiones opcionales
      │
      ├── Resumen de resultados
      └── Reportes PDF
```

## Tablas principales

### `investigadores`

Almacena los datos del investigador que realiza una prueba. Esto no representa cuentas de usuario.

| Campo | Tipo sugerido | Restricciones | Descripción |
|---|---|---|---|
| `id` | `bigint` | PK | Identificador del investigador. |
| `nombre` | `varchar(150)` | NOT NULL | Nombre del investigador. |
| `correo` | `varchar(150)` | NULL | Correo de contacto, si aplica. |
| `telefono` | `varchar(30)` | NULL | Teléfono, si aplica. |

### `laboratorios`

| Campo | Tipo sugerido | Restricciones | Descripción |
|---|---|---|---|
| `id` | `bigint` | PK | Identificador del laboratorio. |
| `institucion` | `varchar(200)` | NOT NULL | Institución donde se realiza la prueba. |
| `direccion` | `varchar(250)` | NULL | Dirección del laboratorio. |

### `estufas`

| Campo | Tipo sugerido | Restricciones | Descripción |
|---|---|---|---|
| `id` | `bigint` | PK | Identificador de la estufa. |
| `marca` | `varchar(100)` | NULL | Marca de la estufa. |
| `fabricante` | `varchar(150)` | NULL | Fabricante. |
| `modelo` | `varchar(100)` | NULL | Modelo o código. |
| `altura_cm` | `numeric(10,2)` | NULL | Altura de la estufa en centímetros. |
| `area_camara_cm2` | `numeric(12,2)` | NULL | Área de la cámara de combustión en cm². |
| `material` | `varchar(150)` | NULL | Material principal. |
| `descripcion` | `text` | NULL | Descripción y observaciones. |

### `condiciones_ambientales`

| Campo | Tipo sugerido | Restricciones | Descripción |
|---|---|---|---|
| `id` | `bigint` | PK | Identificador del registro. |
| `temperatura_aire_c` | `numeric(6,2)` | NOT NULL | Temperatura del aire. |
| `humedad_relativa_pct` | `numeric(6,2)` | NOT NULL | Humedad relativa. |
| `presion_atmosferica_kpa` | `numeric(8,3)` | NULL | Presión atmosférica. |
| `viento` | `varchar(80)` | NULL | Condición del viento. |
| `punto_ebullicion_c` | `numeric(6,2)` | NOT NULL | Punto de ebullición local. |

### `combustibles`

| Campo | Tipo sugerido | Restricciones | Descripción |
|---|---|---|---|
| `id` | `bigint` | PK | Identificador del combustible. |
| `tipo` | `varchar(100)` | NOT NULL | Tipo de combustible. |
| `descripcion` | `text` | NULL | Descripción del combustible. |
| `tamano` | `varchar(80)` | NULL | Dimensiones o tamaño. |
| `humedad_pct` | `numeric(6,3)` | NULL | Contenido de humedad. |
| `poder_calorifico_neto_mj_kg` | `numeric(10,4)` | NULL | Poder calorífico neto. |
| `poder_calorifico_bruto_mj_kg` | `numeric(10,4)` | NULL | Poder calorífico bruto. |
| `contenido_carbono_pct` | `numeric(6,3)` | NULL | Contenido de carbono. |
| `tipo_alimentacion` | `varchar(30)` | NOT NULL | Continua o por lotes. |

### `pruebas_wbt`

Entidad principal de una prueba completa.

| Campo | Tipo sugerido | Restricciones | Descripción |
|---|---|---|---|
| `id` | `bigint` | PK | Identificador de la prueba. |
| `codigo` | `varchar(50)` | UNIQUE, NOT NULL | Código de la prueba. |
| `fecha` | `date` | NOT NULL | Fecha de realización. |
| `investigador_id` | `bigint` | FK, NOT NULL | Relación con `investigadores`. |
| `laboratorio_id` | `bigint` | FK, NOT NULL | Relación con `laboratorios`. |
| `estufa_id` | `bigint` | FK, NOT NULL | Relación con `estufas`. |
| `combustible_id` | `bigint` | FK, NOT NULL | Relación con `combustibles`. |
| `condiciones_ambientales_id` | `bigint` | FK, NOT NULL | Condiciones utilizadas. |
| `estado` | `varchar(30)` | NOT NULL | Registrada, en ejecución, finalizada, inválida o eliminada. |
| `observaciones` | `text` | NULL | Notas y cambios al protocolo. |
| `created_at` | `timestamp` | NOT NULL | Fecha de creación. |
| `updated_at` | `timestamp` | NOT NULL | Fecha de última actualización. |

### `fases_prueba`

Una prueba debe tener una fila por fase y repetición.

| Campo | Tipo sugerido | Restricciones | Descripción |
|---|---|---|---|
| `id` | `bigint` | PK | Identificador de la fase. |
| `prueba_id` | `bigint` | FK, NOT NULL | Relación con `pruebas_wbt`. |
| `tipo_fase` | `varchar(30)` | NOT NULL | Inicio frío, inicio caliente o baja potencia. |
| `numero_repeticion` | `smallint` | NOT NULL | Número de repetición del conjunto WBT. |
| `tiempo_inicial` | `timestamp` | NOT NULL | Inicio de la fase. |
| `tiempo_final` | `timestamp` | NULL | Final de la fase. |
| `temperatura_agua_inicial_c` | `numeric(6,2)` | NOT NULL | Temperatura inicial del agua. |
| `temperatura_agua_final_c` | `numeric(6,2)` | NULL | Temperatura final del agua. |
| `peso_olla_seca_g` | `numeric(10,3)` | NOT NULL | Peso de la olla sin agua. |
| `peso_olla_agua_inicial_g` | `numeric(10,3)` | NOT NULL | Peso inicial de olla más agua. |
| `peso_olla_agua_final_g` | `numeric(10,3)` | NULL | Peso final de olla más agua. |
| `peso_combustible_inicial_g` | `numeric(10,3)` | NOT NULL | Combustible al inicio. |
| `peso_combustible_final_g` | `numeric(10,3)` | NULL | Combustible no quemado al final. |
| `peso_carbon_final_g` | `numeric(10,3)` | NULL | Carbón restante, cuando corresponda. |
| `observaciones` | `text` | NULL | Notas de la fase. |

Restricción recomendada:

```text
UNIQUE (prueba_id, tipo_fase, numero_repeticion)
```

## Resultados calculados

### `resultados_fase`

Almacena resultados derivados de una fase sin reemplazar las mediciones originales.

| Campo | Tipo sugerido | Descripción |
|---|---|---|
| `id` | `bigint` PK | Identificador del resultado. |
| `fase_id` | `bigint` FK | Fase a la que pertenece. |
| `tiempo_fase_s` | `numeric(12,3)` | Duración de la fase en segundos. |
| `masa_agua_g` | `numeric(12,3)` | Masa inicial o útil de agua. |
| `masa_agua_evaporada_g` | `numeric(12,3)` | Agua evaporada. |
| `combustible_consumido_g` | `numeric(12,3)` | Combustible consumido. |
| `combustible_seco_g` | `numeric(12,3)` | Combustible equivalente seco. |
| `tiempo_ebullicion_s` | `numeric(12,3)` | Tiempo para llegar al punto de ebullición. |
| `tiempo_ebullicion_corregido_s` | `numeric(12,3)` | Tiempo corregido. |
| `energia_util_kj` | `numeric(14,4)` | Energía útil transferida al agua. |
| `energia_combustible_kj` | `numeric(14,4)` | Energía del combustible. |
| `eficiencia_termica_pct` | `numeric(8,4)` | Eficiencia térmica. |
| `consumo_especifico_g_l` | `numeric(12,4)` | Consumo por litro. |
| `consumo_energetico_mj_l` | `numeric(12,4)` | Consumo energético por litro. |
| `velocidad_combustion_g_min` | `numeric(12,4)` | Velocidad de combustión. |
| `potencia_fase_w` | `numeric(14,4)` | Potencia de la fase. |
| `calculo_version` | `varchar(30)` | Versión de las fórmulas utilizadas. |

## Emisiones opcionales

### `mediciones_emisiones`

| Campo | Tipo sugerido | Descripción |
|---|---|---|
| `id` | `bigint` PK | Identificador de la medición. |
| `fase_id` | `bigint` FK | Fase asociada. |
| `fecha_hora` | `timestamp` | Momento de la medición. |
| `co2_ppm` | `numeric(12,4)` | Concentración de CO₂. |
| `co_ppm` | `numeric(12,4)` | Concentración de CO. |
| `pm_ug_m3` | `numeric(12,4)` | Material particulado. |
| `temperatura_ducto_c` | `numeric(8,3)` | Temperatura del ducto. |
| `flujo_ducto_m3_h` | `numeric(12,4)` | Flujo de la chimenea o campana. |
| `presion_atmosferica_kpa` | `numeric(8,3)` | Presión durante el muestreo. |
| `metodo_medicion` | `varchar(80)` | Tiempo real o filtro. |
| `observaciones` | `text` | Notas del muestreo. |

### Resultados de emisiones

Los valores derivados como emisiones por tarea, combustible, tiempo o energía pueden almacenarse en `resultados_fase` o en una tabla separada si se requieren varias versiones del cálculo.

## Resumen de la prueba

### `resumenes_prueba`

Esta tabla evita repetir todos los campos de cada fase en `pruebas_wbt`.

| Campo | Tipo sugerido | Descripción |
|---|---|---|
| `id` | `bigint` PK | Identificador del resumen. |
| `prueba_id` | `bigint` FK, UNIQUE | Prueba resumida. |
| `potencia_alta_w` | `numeric(14,4)` | Potencia combinada de inicio frío y caliente. |
| `potencia_baja_w` | `numeric(14,4)` | Potencia de baja potencia. |
| `eficiencia_promedio_pct` | `numeric(8,4)` | Eficiencia promedio. |
| `consumo_promedio_g_l` | `numeric(12,4)` | Consumo específico promedio. |
| `resultado_valido` | `boolean` | Indica si el conjunto es válido. |
| `calculado_at` | `timestamp` | Fecha del cálculo. |

## Reportes

### `reportes`

| Campo | Tipo sugerido | Descripción |
|---|---|---|
| `id` | `bigint` PK | Identificador del reporte. |
| `prueba_id` | `bigint` FK | Prueba reportada. |
| `fecha_generacion` | `timestamp` | Fecha de generación. |
| `ruta_archivo` | `varchar(300)` | Ubicación del PDF. |
| `estado` | `varchar(30)` | Generando, generado o error. |
| `mensaje_error` | `text` | Detalle si la generación falla. |

## Relaciones principales

```text
investigadores 1 ──── N pruebas_wbt
laboratorios 1 ───── N pruebas_wbt
estufas 1 ────────── N pruebas_wbt
combustibles 1 ───── N pruebas_wbt
condiciones_ambientales 1 ─── 1 pruebas_wbt
pruebas_wbt 1 ────── N fases_prueba
fases_prueba 1 ───── 1 resultados_fase
fases_prueba 1 ───── N mediciones_emisiones
pruebas_wbt 1 ────── 1 resumenes_prueba
pruebas_wbt 1 ────── N reportes
```

## Cambios respecto a la hoja de cálculo

| En la hoja | Propuesta |
|---|---|
| `fase` mezcla datos y resultados | Separar `fases_prueba` y `resultados_fase`. |
| `Prueba_wbt` repite resultados de fases | Usar `resumenes_prueba` para agregados. |
| `peso_olla` es ambiguo | Separar peso seco, inicial y final. |
| `mediciones_opc` no identifica una fase | Relacionar `mediciones_emisiones` con `fase_id`. |
| Faltan relaciones entre tablas | Agregar claves foráneas. |
| Falta el registro de reportes | Agregar tabla `reportes`. |
| `tiempo_fase` es un dato derivado | Calcularlo a partir de los tiempos inicial y final. |
