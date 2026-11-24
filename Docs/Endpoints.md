# API del backend SICEE

**Proyecto:** SICEE — Sistema Integrado de Caracterización Energética y Emisiones
**Backend:** Flask + SQLAlchemy + PostgreSQL
**Fecha de elaboración:** 23 de noviembre de 2026
**Estado:** documento de referencia del estado actual del código

---

## 0. Convenciones generales

| Tema | Comportamiento |
|---|---|
| URL base | `http://localhost:5000` (el puerto depende de `docker-compose.yaml`) |
| Autenticación | No existe. El sistema es on-premise y de un solo actor (Investigador). |
| Formato | Todas las peticiones y respuestas son `application/json` |
| Decimales | Se aceptan como número (`18.5`) o como texto numérico (`"18.5"`). Siempre se devuelven como número. |
| Fechas | Se aceptan en ISO 8601: `2026-11-02`, `2026-11-02T08:00`, `2026-11-02T08:00:00` |
| Cadenas vacías | Un `""` se guarda como `NULL`. Las cadenas se recortan (`strip`) antes de guardar. |
| Nulos | Los campos opcionales se devuelven como `null` |
| Métodos | Solo `GET` y `POST`. **No hay `PUT`, `PATCH` ni `DELETE`** en ningún módulo. |
| Prefijos | `/api/investigadores`, `/api/catalogos`, `/api/pruebas`, `/api/calculos` |

### Formato de error

Todas las validaciones devuelven un objeto con una sola clave:

```json
{ "error": "Datos inválidos: El campo investigador_id es obligatorio" }
```

| Módulo | Prefijo del mensaje | Código |
|---|---|---|
| `pruebas` | `Datos inválidos: ...` | 400 |
| `catalogos` | mensaje directo, sin prefijo | 400 |
| `investigadores` | mensaje directo, sin prefijo | 400 |

Los errores de base de datos (clave duplicada, llave foránea inexistente) también salen como `400` con el texto crudo de PostgreSQL:

```json
{
  "error": "Datos inválidos: No se pudo guardar: duplicate key value violates unique constraint \"fase_prueba_prueba_wbt_id_tipo_fase_key\"\nDETAIL:  Key (prueba_wbt_id, tipo_fase)=(1, inicio_frio) already exists.\n"
}
```

---

## 1. Resumen de endpoints

| # | Método | URL | Devuelve |
|---|---|---|---|
| 1 | GET | `/api/health` | Estado del servicio |
| 2 | GET | `/api/health/db` | Estado de PostgreSQL |
| 3 | GET | `/api/investigadores/` | Lista de investigadores |
| 4 | POST | `/api/investigadores/` | Investigador creado |
| 5 | GET | `/api/investigadores/<id>` | Un investigador |
| 6 | GET | `/api/investigadores/searchId` | Investigador por nombre |
| 7 | GET | `/api/catalogos/combustible` | Lista de combustibles |
| 8 | POST | `/api/catalogos/combustible` | Combustible creado |
| 9 | GET | `/api/catalogos/estufas` | Lista de estufas |
| 10 | POST | `/api/catalogos/estufas` | Estufa creada |
| 11 | GET | `/api/catalogos/labs` | Lista de laboratorios |
| 12 | POST | `/api/catalogos/labs` | Laboratorio creado |
| 13 | GET | `/api/pruebas/condiciones_ambientales` | Lista de condiciones |
| 14 | POST | `/api/pruebas/condiciones_ambientales` | Condiciones creadas |
| 15 | GET | `/api/pruebas/conjunto_pruebas` | Lista de conjuntos |
| 16 | POST | `/api/pruebas/conjunto_pruebas` | Conjunto creado |
| 17 | GET | `/api/pruebas/pruebas_wbt` | Lista de pruebas |
| 18 | POST | `/api/pruebas/pruebas_wbt` | Prueba creada |
| 19 | GET | `/api/pruebas/Fase_Prueba` | Lista de fases |
| 20 | POST | `/api/pruebas/Fase_Prueba` | Fase creada |
| 21 | GET | `/api/pruebas/ollas` | Lista de ollas |
| 22 | POST | `/api/pruebas/ollas` | Olla creada |
| 23 | GET | `/api/pruebas/olla_fase` | Lista de ollas por fase |
| 24 | POST | `/api/pruebas/olla_fase` | Olla por fase creada |
| 25 | GET | `/api/pruebas/mediciones_opcionales` | Lista de mediciones |
| 26 | POST | `/api/pruebas/mediciones_opcionales` | Medición creada |
| 27 | GET | `/api/pruebas/muestras_humedad` | Lista de mediciones de humedad |
| 28 | POST | `/api/pruebas/muestras_humedad` | Humedad de la prueba guardada |
| 29 | GET | `/api/calculos/datos/pruebawbt` | ¿Existe la tabla `prueba_wbt`? |
| 30 | GET | `/api/calculos/datos/list/<prueba_id>` | Prueba completa con fases y ollas |
| 31 | GET | `/api/calculos/datos/calcular/<prueba_id>` | Resultados calculados en memoria |
| 32 | GET | `/api/calculos/datos/<prueba_id>` | ⚠️ Roto: devuelve 500 (ver 6.4) |

---

## 2. Health

### 2.1 `GET /api/health`

Verifica que la aplicación responde.

**Respuesta `200`**

```json
{ "status": "ok" }
```

### 2.2 `GET /api/health/db`

Verifica la conexión a PostgreSQL con un `SELECT 1`.

**Respuesta `200`**

```json
{ "status": "ok", "database": "ok" }
```

**Respuesta `503`**

```json
{
  "status": "error",
  "database": "unreachable",
  "detail": "connection to server at \"postgres-sicee\" ... failed"
}
```

---

## 3. Investigadores

Prefijo: `/api/investigadores`

### 3.1 `GET /api/investigadores/`

Devuelve todos los investigadores.

**Respuesta `200`**

```json
[
  { "id": 1, "nombre": "Dra. María González" },
  { "id": 2, "nombre": "Ing. Carlos Pérez" }
]
```

### 3.2 `POST /api/investigadores/`

**Cuerpo**

| Campo | Tipo | Obligatorio | Notas |
|---|---|---|---|
| `nombre` | string | Sí | Se recorta; un `""` se rechaza |

```json
{ "nombre": "Dra. María González" }
```

**Respuesta `201`**

```json
{ "id": 3, "nombre": "Dra. María González" }
```

**Respuesta `400`**

```json
{ "error": "El nombre es obligatorio" }
```

### 3.3 `GET /api/investigadores/<id>`

**Respuesta `200`**

```json
{ "id": 1, "nombre": "Dra. María González" }
```

**Si no existe:** devuelve `200` (no `404`) con:

```json
{ "error": "investigador no encontrado" }
```

### 3.4 `GET /api/investigadores/searchId`

Busca por nombre exacto. **Aunque es `GET`, espera un cuerpo JSON.**

**Cuerpo**

| Campo | Tipo | Obligatorio |
|---|---|---|
| `nombre` | string | Sí |

```json
{ "nombre": "Dra. María González" }
```

**Respuesta `200`**

```json
{ "id": 1, "nombre": "Dra. María González" }
```

**Respuesta `404`**

```json
{ "error": "Investigador no encontrado" }
```

**Sin nombre:** `200` con `{ "error": "Ingrese nombre del investigador a buscar" }`.

---

## 4. Catálogos

Prefijo: `/api/catalogos`

> En este módulo los números **no admiten `null`**: si se omiten, se guardan como `0.00`.

### 4.1 `GET /api/catalogos/combustible`

**Respuesta `200`**

```json
[
  {
    "id": 1,
    "tipo": "Leña de eucalipto",
    "longitud_combustible_cm": 30.0,
    "ancho_combustible_cm": 8.0,
    "poder_calorifico_neto_mj_kg": 18.5,
    "poder_calorifico_bruto_mj_kg": 19.8,
    "poder_calorifico_carbon_mj_kg": 28.5,
    "contenido_carbono_carbon_pct": 80.0,
    "tipo_alimentacion": "Manual",
    "contenido_carbono_pct": 48.5,
    "descripcion": "Trozos de eucalipto de aproximadamente 30 cm"
  }
]
```

### 4.2 `POST /api/catalogos/combustible`

**Cuerpo**

| Campo | Tipo | Obligatorio | Por defecto |
|---|---|---|---|
| `tipo` | string | **Sí** | — |
| `longitud_combustible_cm` | number | No | `0.00` |
| `ancho_combustible_cm` | number | No | `0.00` |
| `poder_calorifico_neto_mj_kg` | number | No | `0.00` |
| `poder_calorifico_bruto_mj_kg` | number | No | `0.00` |
| `poder_calorifico_carbon_mj_kg` | number | No | `0.00` |
| `contenido_carbono_carbon_pct` | number | No | `0.00` |
| `contenido_carbono_pct` | number | No | `0.00` |
| `tipo_alimentacion` | string | No | `""` |
| `descripcion` | string | No | `""` |

```json
{
  "tipo": "Leña de eucalipto",
  "longitud_combustible_cm": 30,
  "ancho_combustible_cm": 8,
  "poder_calorifico_neto_mj_kg": 18.5,
  "poder_calorifico_bruto_mj_kg": 19.8,
  "poder_calorifico_carbon_mj_kg": 28.5,
  "contenido_carbono_carbon_pct": 80,
  "contenido_carbono_pct": 48.5,
  "tipo_alimentacion": "Manual",
  "descripcion": "Trozos de eucalipto de aproximadamente 30 cm"
}
```

**Respuesta `201`:** el objeto completo, igual que en el `GET`.

**Errores**

| Caso | Código | Cuerpo |
|---|---|---|
| Sin `tipo` | `400` | `{ "error": "El tipo de combustible es obligatorio" }` |
| Número inválido | `400` | `{ "error": "Datos inválidos: could not convert string to float: 'abc'" }` |

### 4.3 `GET /api/catalogos/estufas`

**Respuesta `200`**

```json
[
  {
    "id": 1,
    "marca": "Estufa Rocket A1",
    "fabricante": "CII",
    "area_camara_cm2": 625.0,
    "altura_cm": 45.0,
    "numero_hornillas": 1,
    "material": "Acero inoxidable",
    "descripcion": "Estufa de prueba para biomasa"
  }
]
```

### 4.4 `POST /api/catalogos/estufas`

**Cuerpo**

| Campo | Tipo | Obligatorio | Por defecto |
|---|---|---|---|
| `marca` | string | **Sí** | — |
| `fabricante` | string | **Sí** | — |
| `area_camara_cm2` | number | No | `0.00` |
| `altura_cm` | number | No | `0.00` |
| `numero_hornillas` | int | No | `0` |
| `material` | string | No | `""` |
| `descripcion` | string | No | `""` |

```json
{
  "marca": "Estufa Rocket A1",
  "fabricante": "CII",
  "area_camara_cm2": 625,
  "altura_cm": 45,
  "numero_hornillas": 1,
  "material": "Acero inoxidable",
  "descripcion": "Estufa de prueba para biomasa"
}
```

**Respuesta `201`:** el objeto completo.

**Respuesta `400`:** `{ "error": "faltan datos (marca o fabricante)" }`

### 4.5 `GET /api/catalogos/labs`

**Respuesta `200`**

```json
[
  {
    "id": 1,
    "institucion": "CII - Centro de Investigación e Innovación",
    "direccion": "Quito, Ecuador",
    "descripcion": "Laboratorio de eficiencia energética"
  }
]
```

### 4.6 `POST /api/catalogos/labs`

**Cuerpo**

| Campo | Tipo | Obligatorio |
|---|---|---|
| `institucion` | string | **Sí** |
| `direccion` | string | No |
| `descripcion` | string | No |

```json
{
  "institucion": "CII - Centro de Investigación e Innovación",
  "direccion": "Quito, Ecuador",
  "descripcion": "Laboratorio de eficiencia energética"
}
```

**Respuesta `201`:** el objeto completo.

**Error:** si falta `institucion`, devuelve `200` con `{ "error": "falta nombre institucion" }`.

---

## 5. Pruebas

Prefijo: `/api/pruebas`

El orden de registro es obligatorio por las llaves foráneas:

```text
investigador ─┐
laboratorio ──┤
combustible ──┼─> prueba_wbt ─┬─> fase_prueba ─┬─> olla_fase
estufa ─> conjunto_pruebas ───┘                └─> mediciones_opcionales
condiciones_ambientales ──────┘
olla (de la prueba) ─────────────────────────────> olla_fase
```

### 5.1 `GET /api/pruebas/condiciones_ambientales`

**Respuesta `200`**

```json
[
  {
    "id": 1,
    "temperatura_c": 18.5,
    "humedad_relativa_pct": 65.0,
    "altitud_m": 2850.0,
    "presion_atmosferica_kpa": 101.325,
    "viento_ms": 1.2,
    "condicion_viento": "Viento leve",
    "punto_ebullicion_c": 98.0
  }
]
```

### 5.2 `POST /api/pruebas/condiciones_ambientales`

**Todos los campos son opcionales.** Se puede crear un registro vacío.

| Campo | Tipo | Obligatorio |
|---|---|---|
| `temperatura_c` | number | No |
| `humedad_relativa_pct` | number | No |
| `altitud_m` | number | No |
| `presion_atmosferica_kpa` | number | No |
| `viento_ms` | number | No |
| `condicion_viento` | string | No |
| `punto_ebullicion_c` | number | No |

```json
{
  "temperatura_c": 18.5,
  "humedad_relativa_pct": 65,
  "altitud_m": 2850,
  "presion_atmosferica_kpa": 101.325,
  "viento_ms": 1.2,
  "condicion_viento": "Viento leve",
  "punto_ebullicion_c": 98
}
```

**Respuesta `201`:** el objeto completo.

**Respuesta `400`:** `{ "error": "Datos inválidos: temperatura_c debe ser un número" }`

### 5.3 `GET /api/pruebas/conjunto_pruebas`

**Respuesta `200`**

```json
[
  {
    "id": 1,
    "estufa_id": 1,
    "descripcion": "Conjunto de pruebas estufa Rocket A1"
  }
]
```

### 5.4 `POST /api/pruebas/conjunto_pruebas`

**Cuerpo**

| Campo | Tipo | Obligatorio |
|---|---|---|
| `estufa_id` | int | **Sí** |
| `descripcion` | string | No |

```json
{ "estufa_id": 1, "descripcion": "Conjunto de pruebas estufa Rocket A1" }
```

**Respuesta `201`:** el objeto completo.

**Errores**

| Caso | Código | Cuerpo |
|---|---|---|
| Sin `estufa_id` | `400` | `{ "error": "Datos inválidos: El campo estufa_id es obligatorio" }` |
| `estufa_id` inexistente | `400` | `{ "error": "Datos inválidos: No se pudo guardar: insert or update on table \"conjunto_pruebas\" violates foreign key constraint ..." }` |

### 5.5 `GET /api/pruebas/pruebas_wbt`

**Respuesta `200`**

```json
[
  {
    "id": 1,
    "uuid": "5df503d8-021c-4fac-b1ec-c33f15459417",
    "fecha": "2026-11-02T08:00:00",
    "investigador_id": 1,
    "laboratorio_id": 1,
    "combustible_id": 1,
    "condiciones_ambientales_id": 1,
    "conjunto_pruebas_id": 1,
    "peso_recipiente_carbon_kg": 0.15,
    "numero_repeticion": 1,
    "es_valida": true,
    "motivo_invalidez": null,
    "version_protocolo": "4.2.3",
    "observaciones": "Prueba WBT completa con dos ollas.",
    "created_at": "2026-11-17T02:49:17.503666",
    "updated_at": "2026-11-17T02:49:17.503666"
  }
]
```

### 5.6 `POST /api/pruebas/pruebas_wbt`

**Cuerpo**

| Campo | Tipo | Obligatorio | Por defecto | Notas |
|---|---|---|---|---|
| `investigador_id` | int | **Sí** | — | FK a `investigador` |
| `laboratorio_id` | int | **Sí** | — | FK a `laboratorio` |
| `combustible_id` | int | **Sí** | — | FK a `combustible` |
| `condiciones_ambientales_id` | int | **Sí** | — | FK a `condiciones_ambientales` |
| `conjunto_pruebas_id` | int | **Sí** | — | FK a `conjunto_pruebas` |
| `fecha` | fecha ISO | No | `now()` | Inicio de la prueba |
| `numero_repeticion` | int | No | `1` | 1 a 10 |
| `peso_recipiente_carbon_kg` | number | No | `null` | Peso del recipiente vacío |
| `es_valida` | bool | No | `true` | Acepta `true/false`, `1/0`, `si/no` |
| `motivo_invalidez` | string | No | `null` | — |
| `version_protocolo` | string | No | `"4.2.3"` | — |
| `observaciones` | string | No | `null` | — |

`uuid`, `created_at` y `updated_at` los genera la base de datos; no se envían.

```json
{
  "investigador_id": 1,
  "laboratorio_id": 1,
  "combustible_id": 1,
  "condiciones_ambientales_id": 1,
  "conjunto_pruebas_id": 1,
  "fecha": "2026-11-02T08:00:00",
  "numero_repeticion": 1,
  "peso_recipiente_carbon_kg": 0.15,
  "es_valida": true,
  "version_protocolo": "4.2.3",
  "observaciones": "Prueba WBT completa con dos ollas."
}
```

**Respuesta `201`:** el objeto completo, igual que en el `GET`.

**Errores**

| Caso | Código | Cuerpo |
|---|---|---|
| Falta un FK obligatorio | `400` | `{ "error": "Datos inválidos: El campo investigador_id es obligatorio" }` |
| `fecha` no ISO | `400` | `{ "error": "Datos inválidos: fecha debe tener formato ISO 8601" }` |
| Repetición duplicada | `400` | `{ "error": "Datos inválidos: No se pudo guardar: duplicate key value violates unique constraint \"prueba_wbt_conjunto_pruebas_id_numero_repeticion_key\" ..." }` |

> El par (`conjunto_pruebas_id`, `numero_repeticion`) es único. Si no se envía `numero_repeticion`, se usa `1` y la segunda prueba del mismo conjunto falla.

### 5.7 `GET /api/pruebas/Fase_Prueba`

> El nombre de la ruta lleva mayúsculas: `Fase_Prueba`.

**Respuesta `200`**

```json
[
  {
    "id": 1,
    "prueba_wbt_id": 1,
    "tipo_fase": "inicio_frio",
    "t_inicial": "2026-11-02T08:00:00",
    "t_final": "2026-11-02T08:30:00",
    "peso_combustible_inicial_kg": 1.2,
    "peso_combustible_final_kg": 0.55,
    "peso_carbon_con_recipiente_kg": 0.2,
    "peso_cenizas_kg": 0.05,
    "observaciones": "Fase de inicio frío, termina cuando hierve la olla 1"
  }
]
```

### 5.8 `POST /api/pruebas/Fase_Prueba`

**Cuerpo**

| Campo | Tipo | Obligatorio | Notas |
|---|---|---|---|
| `prueba_wbt_id` | int | **Sí** | FK a `prueba_wbt` |
| `tipo_fase` | string | **Sí** | `inicio_frio`, `inicio_caliente` o `baja_potencia` (acepta mayúsculas) |
| `t_inicial` | fecha ISO | No | — |
| `t_final` | fecha ISO | No | Debe ser ≥ `t_inicial` |
| `peso_combustible_inicial_kg` | number | No | — |
| `peso_combustible_final_kg` | number | No | — |
| `peso_carbon_con_recipiente_kg` | number | No | Carbón + recipiente al final |
| `peso_cenizas_kg` | number | No | — |
| `observaciones` | string | No | — |

```json
{
  "prueba_wbt_id": 1,
  "tipo_fase": "inicio_frio",
  "t_inicial": "2026-11-02T08:00:00",
  "t_final": "2026-11-02T08:30:00",
  "peso_combustible_inicial_kg": 1.2,
  "peso_combustible_final_kg": 0.55,
  "peso_carbon_con_recipiente_kg": 0.2,
  "peso_cenizas_kg": 0.05,
  "observaciones": "Fase de inicio frío, termina cuando hierve la olla 1"
}
```

**Respuesta `201`:** el objeto completo.

**Errores**

| Caso | Código | Cuerpo |
|---|---|---|
| Sin `tipo_fase` o inválido | `400` | `{ "error": "Datos inválidos: tipo_fase debe ser inicio_frio, inicio_caliente o baja_potencia" }` |
| `t_final` < `t_inicial` | `400` | `{ "error": "Datos inválidos: t_final no puede ser anterior a t_inicial" }` |
| Fase repetida en la misma prueba | `400` | `{ "error": "Datos inválidos: No se pudo guardar: duplicate key value ..." }` |

> (`prueba_wbt_id`, `tipo_fase`) es único: cada prueba tiene como máximo una fase de cada tipo.

### 5.9 `GET /api/pruebas/ollas`

**Respuesta `200`**

```json
[
  {
    "id": 1,
    "prueba_wbt_id": 1,
    "numero_olla": 1,
    "peso_seco_kg": 0.85,
    "capacidad_l": 5.0
  }
]
```

### 5.10 `POST /api/pruebas/ollas`

**Cuerpo**

| Campo | Tipo | Obligatorio | Notas |
|---|---|---|---|
| `prueba_wbt_id` | int | **Sí** | FK a `prueba_wbt` |
| `numero_olla` | int | **Sí** | Debe ser ≥ 1 |
| `peso_seco_kg` | number | No | Olla vacía y seca |
| `capacidad_l` | number | No | Litros |

```json
{
  "prueba_wbt_id": 1,
  "numero_olla": 1,
  "peso_seco_kg": 0.85,
  "capacidad_l": 5.0
}
```

**Respuesta `201`:** el objeto completo.

**Errores**

| Caso | Código | Cuerpo |
|---|---|---|
| `numero_olla` < 1 | `400` | `{ "error": "Datos inválidos: numero_olla debe ser mayor o igual a 1" }` |
| Olla repetida en la prueba | `400` | `{ "error": "Datos inválidos: No se pudo guardar: duplicate key value ..." }` |

> (`prueba_wbt_id`, `numero_olla`) es único.

### 5.11 `GET /api/pruebas/olla_fase`

**Respuesta `200`**

```json
[
  {
    "id": 1,
    "olla_id": 1,
    "fase_id": 1,
    "temperatura_inicial_agua_c": 24.0,
    "temperatura_final_agua_c": 98.0,
    "peso_con_agua_inicial_kg": 5.85,
    "peso_con_agua_final_kg": 5.15
  }
]
```

### 5.12 `POST /api/pruebas/olla_fase`

**Cuerpo**

| Campo | Tipo | Obligatorio | Notas |
|---|---|---|---|
| `olla_id` | int | **Sí** | Debe existir |
| `fase_id` | int | **Sí** | Debe existir y ser de la misma prueba que la olla |
| `temperatura_inicial_agua_c` | number | No | — |
| `temperatura_final_agua_c` | number | No | — |
| `peso_con_agua_inicial_kg` | number | No | Olla + agua al inicio |
| `peso_con_agua_final_kg` | number | No | Olla + agua al final |

```json
{
  "olla_id": 1,
  "fase_id": 1,
  "temperatura_inicial_agua_c": 24.0,
  "temperatura_final_agua_c": 98.0,
  "peso_con_agua_inicial_kg": 5.85,
  "peso_con_agua_final_kg": 5.15
}
```

**Respuesta `201`:** el objeto completo.

**Errores**

| Caso | Código | Cuerpo |
|---|---|---|
| Olla inexistente | `400` | `{ "error": "Datos inválidos: No existe la olla con id 999" }` |
| Fase inexistente | `400` | `{ "error": "Datos inválidos: No existe la fase con id 999" }` |
| Olla y fase de pruebas distintas | `400` | `{ "error": "Datos inválidos: La olla y la fase pertenecen a pruebas WBT distintas" }` |
| Registro repetido | `400` | `{ "error": "Datos inválidos: No se pudo guardar: duplicate key value ..." }` |

> (`olla_id`, `fase_id`) es único; `mediciones_opcionales.fase_id` también.

### 5.13 `GET /api/pruebas/mediciones_opcionales`

**Respuesta `200`**

```json
[
  {
    "id": 1,
    "fase_id": 1,
    "temperatura_ducto_c": 85.3,
    "co_ppm": 120.5,
    "pm_ug_m3": 3200.0,
    "co2_ppm": 45000.0,
    "co2_fondo_ppm": 420.0,
    "co_fondo_ppm": 0.5,
    "pm_fondo_ug_m3": 5.0,
    "co2_total_g": null,
    "co_total_g": null,
    "pm_total_g": null
  }
]
```

### 5.14 `POST /api/pruebas/mediciones_opcionales`

**Cuerpo**

| Campo | Tipo | Obligatorio |
|---|---|---|
| `fase_id` | int | **Sí** |
| `temperatura_ducto_c` | number | No |
| `co_ppm` | number | No |
| `pm_ug_m3` | number | No |
| `co2_ppm` | number | No |
| `co2_fondo_ppm` | number | No |
| `co_fondo_ppm` | number | No |
| `pm_fondo_ug_m3` | number | No |
| `co2_total_g` | number | No |
| `co_total_g` | number | No |
| `pm_total_g` | number | No |

```json
{
  "fase_id": 1,
  "temperatura_ducto_c": 85.3,
  "co_ppm": 120.5,
  "pm_ug_m3": 3200,
  "co2_ppm": 45000,
  "co2_fondo_ppm": 420,
  "co_fondo_ppm": 0.5,
  "pm_fondo_ug_m3": 5
}
```

**Respuesta `201`:** el objeto completo.

**Error:** si la fase ya tiene mediciones, `400` por la clave única `fase_id`.

> Los totales `co2_total_g`, `co_total_g` y `pm_total_g` se guardan si se envían, pero **no se calculan**: la sección de emisiones está diferida.

---

### 5.15 `GET /api/pruebas/muestras_humedad`

Devuelve las mediciones de humedad del combustible. La humedad se mide **en cada prueba**: 3 leños × 3 mediciones = 9 filas. El promedio de esas filas es la humedad que usa el cálculo.

**Parámetro opcional:** `?prueba_wbt_id=1` filtra por prueba.

**Respuesta `200`**

```json
[
  { "id": 1, "prueba_wbt_id": 1, "numero_lenio": 1, "numero_medicion": 1, "humedad_pct": 8.0 },
  { "id": 2, "prueba_wbt_id": 1, "numero_lenio": 1, "numero_medicion": 2, "humedad_pct": 8.4 },
  { "id": 3, "prueba_wbt_id": 1, "numero_lenio": 1, "numero_medicion": 3, "humedad_pct": 7.6 }
]
```

### 5.16 `POST /api/pruebas/muestras_humedad`

Reemplaza **todas** las mediciones de humedad de una prueba. Es un POST idempotente por prueba: se envía el juego completo de 9 valores.

**Cuerpo**

| Campo | Tipo | Obligatorio | Notas |
|---|---|---|---|
| `prueba_wbt_id` | int | **Sí** | Debe existir |
| `muestras` | array | **Sí** | Al menos una medición |
| `muestras[].numero_lenio` | int | **Sí** | Mayor que 0 |
| `muestras[].numero_medicion` | int | **Sí** | Mayor que 0 |
| `muestras[].humedad_pct` | number | **Sí** | Entre 0 y 100 |

```json
{
  "prueba_wbt_id": 1,
  "muestras": [
    { "numero_lenio": 1, "numero_medicion": 1, "humedad_pct": 8.0 },
    { "numero_lenio": 1, "numero_medicion": 2, "humedad_pct": 8.4 },
    { "numero_lenio": 1, "numero_medicion": 3, "humedad_pct": 7.6 },
    { "numero_lenio": 2, "numero_medicion": 1, "humedad_pct": 8.2 },
    { "numero_lenio": 2, "numero_medicion": 2, "humedad_pct": 7.8 },
    { "numero_lenio": 2, "numero_medicion": 3, "humedad_pct": 8.1 },
    { "numero_lenio": 3, "numero_medicion": 1, "humedad_pct": 7.9 },
    { "numero_lenio": 3, "numero_medicion": 2, "humedad_pct": 8.3 },
    { "numero_lenio": 3, "numero_medicion": 3, "humedad_pct": 7.7 }
  ]
}
```

**Respuesta `201`**

```json
{
  "prueba_wbt_id": 1,
  "promedio_humedad_pct": 8.0,
  "muestras": [
    { "id": 1, "prueba_wbt_id": 1, "numero_lenio": 1, "numero_medicion": 1, "humedad_pct": 8.0 }
  ]
}
```

**Errores `400`:** prueba inexistente, lista vacía, medición repetida (mismo leño y número), o `humedad_pct` fuera de 0–100.

> El promedio **no se envía**: lo calcula el backend y se guarda en `muestra_humedad`; el cálculo térmico lo toma de ahí. No existe columna `humedad_pct` en `combustible`.

---

## 6. Cálculos

Prefijo: `/api/calculos`

### 6.1 `GET /api/calculos/datos/pruebawbt`

Comprueba si la tabla `prueba_wbt` existe en la base.

**Respuesta `200`**

```json
{ "status": "ok", "existe_prueba_wbt": true }
```

### 6.2 `GET /api/calculos/datos/list/<prueba_id>`

Devuelve la prueba armada para el frontend: prueba, catálogos, fases y ollas de cada fase.

**Respuesta `200`**

```json
{
  "prueba": {
    "id": 1,
    "uuid": "5df503d8-021c-4fac-b1ec-c33f15459417",
    "fecha": "2026-11-02T08:00:00",
    "investigador_id": 1,
    "laboratorio_id": 1,
    "combustible_id": 1,
    "condiciones_ambientales_id": 1,
    "conjunto_pruebas_id": 1,
    "estufa_id": 1,
    "peso_recipiente_carbon_kg": 0.15,
    "numero_repeticion": 1,
    "es_valida": true,
    "motivo_invalidez": null,
    "version_protocolo": "4.2.3",
    "observaciones": "Prueba WBT completa con dos ollas.",
    "created_at": "2026-11-17T02:49:17.503666",
    "updated_at": "2026-11-17T02:49:17.503666"
  },
  "combustible": {
    "id": 1,
    "tipo": "Leña de eucalipto",
    "longitud_combustible_cm": 30.0,
    "ancho_combustible_cm": 8.0,
    "humedad_pct": 8.0,
    "poder_calorifico_neto_mj_kg": 18.5,    "poder_calorifico_bruto_mj_kg": 19.8,
    "poder_calorifico_carbon_mj_kg": 28.5,
    "contenido_carbono_carbon_pct": 80.0,
    "tipo_alimentacion": "Manual",
    "contenido_carbono_pct": 48.5,
    "descripcion": "Trozos de eucalipto de aproximadamente 30 cm"
  },
  "condiciones_ambientales": {
    "id": 1,
    "temperatura_c": 18.5,
    "humedad_relativa_pct": 65.0,
    "altitud_m": 2850.0,
    "presion_atmosferica_kpa": 101.325,
    "viento_ms": 1.2,
    "condicion_viento": "Viento leve",
    "punto_ebullicion_c": 98.0
  },
  "fases": [
    {
      "id": 1,
      "tipo_fase": "inicio_frio",
      "t_inicial": "Mon, 02 Nov 2026 08:00:00 GMT",
      "t_final": "Mon, 02 Nov 2026 08:30:00 GMT",
      "peso_combustible_inicial_kg": 1.2,
      "peso_combustible_final_kg": 0.55,
      "peso_carbon_con_recipiente_kg": 0.2,
      "peso_cenizas_kg": 0.05,
      "ollas": [
        {
          "olla_id": 1,
          "numero_olla": 1,
          "capacidad_l": 5.0,
          "peso_seco_kg": 0.85,
          "temperatura_inicial_agua_c": 24.0,
          "temperatura_final_agua_c": 98.0,
          "peso_con_agua_inicial_kg": 5.85,
          "peso_con_agua_final_kg": 5.15
        }
      ]
    }
  ]
}
```

Las fases se ordenan `inicio_frio` → `inicio_caliente` → `baja_potencia`, y las ollas por `numero_olla`.

**Respuesta `404`**

```json
{ "error": "No existe la prueba_wbt con id 99" }
```

**Detalles**

- Las fechas de las fases salen en formato RFC 822 (`Mon, 02 Nov 2026 08:00:00 GMT`), no en ISO 8601, porque `get_data()` las devuelve como objetos `datetime` sin convertir. En los demás `GET` sí salen en ISO.
- **No incluye** `mediciones_opcionales` ni resultados calculados.

### 6.3 `GET /api/calculos/datos/calcular/<prueba_id>`

Ejecuta `formulas.py` en memoria y devuelve los 18 campos de `resultado_fase` por cada fase. **No guarda nada en la base.**

**Respuesta `200`**

```json
{
  "inicio_frio": {
    "tiempo_fase_min": 30.0,
    "masa_agua_inicial_kg": 8.0,
    "masa_agua_final_kg": 6.9,
    "masa_agua_evaporada_kg": 1.1,
    "masa_agua_efectiva_kg": 6.9,
    "combustible_consumido_kg": 0.65,
    "tiempo_ebullicion_min": 30.0,
    "tiempo_ebullicion_corregido_min": 30.41,
    "energia_util_kj": 4964.11,
    "energia_combustible_kj": 9503.33,
    "eficiencia_termica_pct": 52.24,
    "consumo_especifico_g_l": 74.45,
    "velocidad_combustion_g_min": 17.12,
    "potencia_fase_kw": 5.28,
    "energia_especifica_corregida_kj_l": 1395.91,
    "combustible_seco_equivalente_kg": 0.51,
    "cambio_carbon_kg": 0.05,
    "consumo_especifico_corregido_g_l": 75.45
  },
  "inicio_caliente": { "...": "misma estructura" },
  "baja_potencia": { "...": "misma estructura" }
}
```

Las claves son los `tipo_fase` presentes en la prueba. Los valores se redondean a 2 decimales.

**Respuesta `404`**

```json
{ "error": "No existe la prueba_wbt con id 99" }
```

**Errores de datos**

Si los datos están incompletos, `formulas.py` lanza `ValueError` y la petición devuelve **`500`**, no `400`. Ejemplos:

| Situación | Mensaje |
|---|---|
| Fase sin olla 1 | `ValueError: la fase inicio_frio no tiene olla 1` |
| Olla con datos parciales | `ValueError: la olla 2 tiene datos incompletos...` |
| Carbón pesado sin recipiente | `ValueError: falta peso_recipiente_carbon_kg...` |
| Baja potencia sin `ΔC` del inicio frío | `ValueError: baja_potencia requiere cambio_carbon_frio_kg` |

El orden interno ya resuelve la dependencia: calcula `inicio_frio` primero y reutiliza su `cambio_carbon_kg` en `baja_potencia`.

### 6.4 `GET /api/calculos/datos/<prueba_id>` ⚠️

**Actualmente devuelve `500`.**

```json
AttributeError: module 'app.modules.calculos.services' has no attribute 'get_datos'
```

La ruta quedó llamando a `services.get_datos()`, pero la función se renombró a `get_data()` y esa ruta ahora es `/datos/list/<id>`. Para obtener los datos hay que usar `GET /api/calculos/datos/list/<prueba_id>`.

---

## 7. Restricciones de base de datos

| Tabla | Restricción | Efecto en la API |
|---|---|---|
| `prueba_wbt` | `UNIQUE (conjunto_pruebas_id, numero_repeticion)` | No se puede repetir el número de repetición en un conjunto |
| `prueba_wbt` | `UNIQUE (uuid)` | Lo genera el sistema |
| `fase_prueba` | `UNIQUE (prueba_wbt_id, tipo_fase)` | Una fase de cada tipo por prueba |
| `olla` | `UNIQUE (prueba_wbt_id, numero_olla)` | Una olla por número y prueba |
| `olla_fase` | `UNIQUE (olla_id, fase_id)` | Una medición de olla por fase |
| `mediciones_opcionales` | `UNIQUE (fase_id)` | Una medición por fase |
| `muestra_humedad` | `UNIQUE (prueba_wbt_id, numero_lenio, numero_medicion)` | No se repite una medición |
| `muestra_humedad` | `CHECK (humedad_pct BETWEEN 0 AND 100)` | Rechaza valores fuera de rango |
| `resultado_fase` | `UNIQUE (fase_id)` | Un resultado por fase (nadie lo escribe aún) |

Todas las llaves foráneas de fases, ollas, mediciones y resultados usan `ON DELETE CASCADE`, pero **no hay endpoint de borrado**.

---

## 8. Lo que todavía no existe

| Falta | Consecuencia |
|---|---|
| `PUT` / `PATCH` / `DELETE` | No se puede corregir ni borrar un registro; hay que crear otro |
| Escritura de `resultado_fase` | Los resultados calculados no se guardan; solo existen en la respuesta de `calcular` |
| `resultado_prueba` | No hay tabla ni promedios por prueba |
| Endpoint de emisiones calculadas | `co2_total_g`, `co_total_g` y `pm_total_g` solo se almacenan |
| Validaciones del protocolo | No se aplican las reglas de 3 °C / 6 °C ni la validez por repeticiones |
| Autenticación | No existe, por diseño |

---

## 9. Referencias

- [`tablas.md`](./tablas.md): ecuaciones y correspondencia con `resultado_fase`.
- [`ModeloDatos.md`](./ModeloDatos.md) y [`er.dbml`](./er.dbml): estructura de la base.
- [`ModulosBackend.md`](./ModulosBackend.md): módulos del backend.
- [`ConsultasCII.md`](./ConsultasCII.md): decisiones de protocolo pendientes.
- [`Resumen_WBT_4.2.3.md`](./Resumen_WBT_4.2.3.md): proceso del ensayo y métricas IWA.
