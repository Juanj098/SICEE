# Módulos del backend

El backend de SICEE se organizará como un **monolito modular** desarrollado con Flask. Todos los módulos se ejecutarán dentro de la misma aplicación, pero cada uno tendrá una responsabilidad específica del negocio.

## Estructura

```text
SICEE/backend/app/modules/
├── investigadores/
├── pruebas/
├── validaciones/
├── calculos/
├── historial/
├── reportes/
└── configuracion/
```

El sistema no tendrá módulos de usuarios, autenticación, roles ni permisos. El módulo `investigadores` almacenará únicamente los datos del investigador asociados a una prueba.

## 1. Módulo `investigadores`

### Propósito

Administrar los datos del investigador que realiza una prueba WBT.

### Responsabilidades

- Registrar nombre y datos de contacto, si son necesarios.
- Consultar los datos del investigador asociados a una prueba.
- Asociar un investigador con una prueba WBT.
- Validar los datos básicos del investigador.

### No incluye

- Inicio de sesión.
- Creación de cuentas.
- Contraseñas.
- Roles o permisos.

### Relación con otros módulos

```text
Investigadores ──▶ Pruebas WBT
```

## 2. Módulo `pruebas`

### Propósito

Gestionar el registro y la ejecución de las pruebas de ebullición de agua.

### Responsabilidades

- Crear una prueba WBT.
- Registrar la estufa, combustible, laboratorio y condiciones ambientales.
- Registrar las tres fases de la prueba:
  - Inicio frío.
  - Inicio caliente.
  - Baja potencia.
- Registrar las mediciones de cada fase.
- Iniciar y finalizar una prueba.
- Mantener el estado de la prueba.
- Editar una prueba cuando sea permitido.
- Solicitar la eliminación o marcado de una prueba.

### Estados posibles

```text
REGISTRADA → EN_EJECUCION → FINALIZADA
                         └──→ INVALIDA
```

### Relación con otros módulos

```text
Investigadores
       │
       ▼
Pruebas WBT ──▶ Validaciones
       │
       └──────▶ Cálculos
```

## 3. Módulo `validaciones`

### Propósito

Verificar que los datos ingresados cumplan las reglas del sistema y del protocolo WBT 4.2.3.

### Responsabilidades

- Verificar campos obligatorios.
- Validar tipos de datos y unidades.
- Validar pesos, temperaturas y tiempos.
- Verificar que una prueba tenga sus fases requeridas.
- Validar que la fase de baja potencia dure 45 minutos.
- Verificar que la temperatura no baje más de 6 °C bajo el punto de ebullición local.
- Detectar mediciones incompletas o inconsistentes.
- Informar errores al módulo de pruebas.

### Tipos de validación

| Tipo | Ejemplo |
|---|---|
| Obligatoria | La prueba debe tener investigador, estufa y combustible. |
| Rango | La humedad debe estar entre valores válidos. |
| Consistencia | El peso final no debe ser mayor que el peso inicial sin justificación. |
| Protocolo | La baja potencia debe durar 45 minutos. |
| Estado | Solo una prueba registrada puede iniciar su ejecución. |

## 4. Módulo `calculos`

### Propósito

Procesar las mediciones de las pruebas y calcular sus resultados.

### Responsabilidades

- Calcular masa de agua inicial y final.
- Calcular agua evaporada.
- Calcular combustible consumido.
- Calcular combustible seco equivalente.
- Calcular tiempo de fase.
- Calcular tiempo de ebullición.
- Calcular tiempo de ebullición corregido.
- Calcular energía útil.
- Calcular energía del combustible.
- Calcular eficiencia térmica.
- Calcular consumo específico.
- Calcular velocidad de combustión.
- Calcular potencia de cada fase.
- Calcular potencia alta y baja.
- Calcular emisiones, cuando existan mediciones.
- Generar resultados por fase y resultados generales.

### Dependencias

- `NumPy` para operaciones numéricas.
- `Pandas` para organizar mediciones y resultados.
- Datos validados por el módulo `validaciones`.

### Regla importante

Las fórmulas deben permanecer en este módulo y no dentro de las rutas Flask. Los datos originales deben conservarse para permitir recalcular los resultados.

## 5. Módulo `historial`

### Propósito

Consultar y administrar las pruebas almacenadas.

### Responsabilidades

- Listar pruebas anteriores.
- Buscar por código o fecha.
- Filtrar por investigador, estufa o estado.
- Ordenar resultados.
- Consultar el detalle de una prueba.
- Mostrar las fases, mediciones y resultados.
- Permitir acceder a las acciones de editar, eliminar y generar reporte.

### Restricción de rendimiento

El historial debe mostrar hasta 500 registros en un tiempo no mayor a 3 segundos, según los requisitos documentados.

## 6. Módulo `reportes`

### Propósito

Generar reportes PDF de las pruebas finalizadas.

### Responsabilidades

- Verificar que la prueba esté finalizada.
- Verificar que existan resultados procesados.
- Consultar datos generales, fases y resultados.
- Incluir gráficas de temperatura, consumo y emisiones.
- Generar el archivo PDF.
- Registrar el estado de la generación.
- Permitir reintentar cuando ocurre un error.
- Preparar el reporte para visualización o descarga.

### Posibles estados del reporte

```text
GENERANDO → GENERADO
          └→ ERROR
```

La generación del PDF y de las gráficas se ejecutará dentro del backend en esta primera versión. No se requiere un servidor independiente de reportes.

## 7. Módulo `configuracion`

### Propósito

Centralizar los parámetros utilizados por el protocolo y por el sistema.

### Responsabilidades

- Administrar unidades de medida.
- Definir tipos de fase.
- Definir estados de pruebas y reportes.
- Mantener parámetros del protocolo WBT.
- Mantener el punto de ebullición local cuando aplique.
- Definir valores de referencia del combustible.
- Centralizar constantes utilizadas por los cálculos.

### Ejemplos de configuración

```text
DURACION_BAJA_POTENCIA_MIN = 45
TEMPERATURA_OBJETIVO_BAJA_POTENCIA_C = 3
CAIDA_MAXIMA_BAJA_POTENCIA_C = 6
TEMPERATURA_REFERENCIA_CORRECCION_C = 75
```

Los parámetros que puedan cambiar no deberían estar escritos directamente dentro de las fórmulas.

## Flujo general entre módulos

```text
Investigador
     │
     ▼
Módulo de pruebas
     │
     ▼
Módulo de validaciones
     │
     ├── Datos inválidos → devolver errores
     │
     ▼
Módulo de persistencia
     │
     ▼
Módulo de cálculos
     │
     ▼
Resultados almacenados
     │
     ├── Módulo de historial
     └── Módulo de reportes
```

## Dependencias entre módulos

```text
configuracion ──▶ validaciones
configuracion ──▶ calculos
investigadores ─▶ pruebas
pruebas ────────▶ validaciones
pruebas ────────▶ calculos
historial ──────▶ pruebas
historial ──────▶ calculos
reportes ───────▶ calculos
reportes ───────▶ historial
```

## Separación de responsabilidades

Las rutas Flask deben recibir solicitudes y devolver respuestas. La lógica debe distribuirse de la siguiente manera:

```text
Route
  ↓
Service del módulo
  ↓
Validación o cálculo
  ↓
Repositorio
  ↓
PostgreSQL
```

- Las rutas no deben contener fórmulas del WBT.
- Los cálculos no deben depender de detalles de Flask.
- Las validaciones deben poder probarse sin levantar el servidor.
- Los reportes deben utilizar resultados procesados y no repetir fórmulas.
- La persistencia debe estar separada de la lógica de negocio.


## Archivos por módulo

Cada módulo contiene únicamente los archivos que necesita. No todos requieren rutas, modelos o esquemas, y no se crean archivos vacíos por anticipado.

### Qué hace cada tipo de archivo

| Archivo | Función |
|---|---|
| `__init__.py` | Marca la carpeta como paquete. En módulos con endpoints define y expone el blueprint; en los demás queda vacío. |
| `routes.py` | Endpoints HTTP. Recibe la solicitud, llama al servicio y devuelve la respuesta. No contiene lógica de negocio. |
| `service.py` | Lógica del módulo e interfaz que usan los demás módulos. |
| `models.py` | Modelos SQLAlchemy de las tablas que pertenecen al módulo. |
| `schemas.py` | Validación de formato de entrada y serialización de salida. |
| `repository.py` | Consultas a la base de datos, separadas de la lógica de negocio. Se crea solo cuando las consultas del servicio crecen. |

### Estructura general

```text
SICEE/backend/app/
├── __init__.py          # create_app() y registro de blueprints
├── config.py            # configuración desde variables de entorno
├── extensions.py        # db, migrate, cors
├── shared/
│   ├── errors.py        # excepciones propias y manejador de errores
│   └── responses.py     # formato único de respuesta
└── modules/
    ├── investigadores/
    ├── pruebas/
    ├── validaciones/
    ├── calculos/
    ├── historial/
    ├── reportes/
    └── configuracion/
```

`shared/` contiene código transversal sin dominio propio. No es un módulo de negocio y no importa nada de `modules/`.

### `investigadores`

```text
investigadores/
├── __init__.py      # blueprint
├── routes.py        # listar, obtener y registrar investigadores
├── service.py       # lógica de consulta y registro
├── models.py        # tabla investigador
└── schemas.py       # validación de nombre y datos de contacto
```

### `pruebas`

```text
pruebas/
├── __init__.py      # blueprint
├── routes.py        # crear, consultar, iniciar y finalizar pruebas
├── service.py       # orquesta el flujo: valida, guarda y solicita cálculos
├── models.py        # prueba, fases, mediciones y resultados
├── schemas.py       # formato de entrada y salida
└── states.py        # transiciones permitidas entre estados de la prueba
```

`pruebas` es el módulo central. Llama a `validaciones` antes de guardar y a `calculos` para obtener los resultados, que luego persiste en sus propias tablas.

### `validaciones`

```text
validaciones/
├── __init__.py      # vacío
├── service.py       # interfaz pública: validar_prueba(), validar_fase()
└── rules.py         # reglas de obligatoriedad, rango, consistencia, protocolo y estado
```

No tiene rutas, modelos ni acceso a la base de datos. Recibe datos, aplica las reglas y devuelve los errores encontrados, por lo que se puede probar sin levantar Flask.

### `calculos`

```text
calculos/
├── __init__.py      # vacío
├── wbt.py           # fórmulas del WBT 4.2.3 como funciones puras
├── processors.py    # organiza mediciones (Pandas/NumPy) y arma resultados por fase y generales
└── service.py       # interfaz pública: calcular_resultados(prueba)
```

No tiene rutas ni modelos y no importa Flask ni SQLAlchemy. Recibe mediciones y devuelve resultados; guardarlos es responsabilidad de `pruebas`. Los parámetros del protocolo se leen de `configuracion`, no se escriben dentro de las fórmulas.

### `historial`

```text
historial/
├── __init__.py      # blueprint
├── routes.py        # listar, buscar, filtrar y consultar el detalle
├── service.py       # consultas con filtros, orden y paginación
└── schemas.py       # formato de los filtros y de la respuesta
```

No tiene modelos propios: lee las tablas de `pruebas` a través de su servicio. Debe cumplir el requisito de mostrar hasta 500 registros en menos de 3 segundos.

### `reportes`

```text
reportes/
├── __init__.py      # blueprint
├── routes.py        # generar, reintentar y descargar el reporte
├── service.py       # verifica que la prueba esté finalizada, consulta datos y orquesta la generación
├── pdf.py           # construcción del documento PDF
├── charts.py        # gráficas de temperatura, consumo y emisiones
└── models.py        # estado de generación (GENERANDO, GENERADO, ERROR)
```

`models.py` solo es necesario si el estado del reporte se guarda en la base de datos. Usa resultados ya procesados y no repite fórmulas.

### `configuracion`

```text
configuracion/
├── __init__.py      # vacío
├── constants.py     # parámetros del protocolo (duración de baja potencia, temperaturas de referencia)
├── enums.py         # estados de prueba y reporte, tipos de fase, unidades de medida
└── service.py       # lectura de parámetros para los demás módulos
```

Al inicio los valores viven en código. Si más adelante deben poder modificarse sin desplegar, se agrega `models.py` y `routes.py`.

### Resumen

| Módulo | `routes` | `service` | `models` | `schemas` | Otros |
|---|---|---|---|---|---|
| `investigadores` | sí | sí | sí | sí | |
| `pruebas` | sí | sí | sí | sí | `states.py` |
| `validaciones` | no | sí | no | no | `rules.py` |
| `calculos` | no | sí | no | no | `wbt.py`, `processors.py` |
| `historial` | sí | sí | no | sí | |
| `reportes` | sí | sí | opcional | no | `pdf.py`, `charts.py` |
| `configuracion` | no | sí | no | no | `constants.py`, `enums.py` |

### Regla de dependencia

Los módulos se comunican a través del `service.py` del otro módulo, nunca importando sus modelos ni funciones internas. Las dependencias son las del diagrama de la sección anterior, y no se permiten dependencias circulares.