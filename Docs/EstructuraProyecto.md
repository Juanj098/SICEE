# Distribución propuesta del proyecto

Esta estructura corresponde a la arquitectura propuesta para SICEE como un **monolito modular** con Flask, PostgreSQL y un frontend web. Es una guía de organización; actualmente el repositorio contiene principalmente documentación.

```text
SICEE/
├── backend/
│   ├── app/
│   │   ├── __init__.py              # create_app(), registra los blueprints
│   │   ├── config.py                # configuración por entorno (.env)
│   │   ├── extensions.py            # db, migrate, cors
│   │   ├── shared/
│   │   │   ├── __init__.py
│   │   │   ├── errors.py            # excepciones y manejadores de error
│   │   │   └── responses.py         # formato único de respuesta
│   │   └── modules/
│   │       ├── __init__.py
│   │       ├── investigadores/
│   │       │   ├── __init__.py      # expone el blueprint
│   │       │   ├── models.py
│   │       │   ├── schemas.py
│   │       │   ├── routes.py
│   │       │   └── service.py
│   │       ├── pruebas/
│   │       │   ├── __init__.py
│   │       │   ├── models.py
│   │       │   ├── schemas.py
│   │       │   ├── routes.py
│   │       │   ├── service.py
│   │       │   └── validators.py
│   │       ├── calculos/
│   │       │   ├── __init__.py
│   │       │   └── wbt.py           # fórmulas puras, sin Flask ni BD
│   │       ├── historial/
│   │       │   ├── __init__.py
│   │       │   ├── routes.py
│   │       │   └── service.py
│   │       └── reportes/
│   │           ├── __init__.py
│   │           ├── routes.py
│   │           ├── pdf.py
│   │           └── charts.py
│   ├── migrations/
│   ├── tests/
│   │   ├── unit/
│   │   └── integration/
│   ├── requirements.txt
│   ├── .env.example
│   └── run.py
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   │   ├── RegistroPrueba/
│   │   │   ├── EjecucionPrueba/
│   │   │   ├── Historial/
│   │   │   ├── Resultados/
│   │   │   └── Reportes/
│   │   ├── services/
│   │   ├── hooks/
│   │   └── utils/
│   ├── public/
│   ├── tests/
│   └── package.json
│
├── database/
│   ├── seeds/
│   └── scripts/
│
├── infra/
│   ├── docker/
│   │   ├── Dockerfile.backend
│   │   └── Dockerfile.frontend
│   ├── docker-compose.yml
│   └── k8s/
│       ├── backend-deployment.yaml
│       ├── frontend-deployment.yaml
│       ├── postgres-statefulset.yaml
│       ├── services.yaml
│       └── ingress.yaml
│
├── Docs/
│   ├── README.md
│   ├── AnteProyecto.md
│   ├── CDU.md
│   ├── DiseñoTecnico.md
│   ├── ModeloDatos.md
│   ├── Tecnologias.md
│   ├── Pruebas.md
│   ├── Resumen_WBT_4.2.3.md
│   ├── EstructuraProyecto.md
│   ├── diagramas/
│   └── mockups/
│
├── .env.example
├── .gitignore
└── README.md
```

## Responsabilidad de las áreas principales

| Área | Responsabilidad |
|---|---|
| `backend/app/routes` | Recibir peticiones HTTP y devolver respuestas. |
| `backend/app/modules` | Contener la lógica de negocio separada por módulos. |
| `backend/app/repositories` | Consultar y persistir datos en PostgreSQL. |
| `backend/app/modules/calculos` | Implementar las fórmulas y procesamiento del WBT. |
| `backend/app/modules/reportes` | Generar gráficas y archivos PDF. |
| `frontend/src/pages` | Implementar las pantallas principales del sistema. |
| `database` | Scripts, datos iniciales y tareas relacionadas con la base de datos. |
| `infra` | Docker, Docker Compose y manifiestos de despliegue. |
| `Docs` | Requisitos, casos de uso, arquitectura y demás documentación. |

## Flujo recomendado dentro del backend

```text
Route
  ↓
Service del módulo
  ↓
Validación y reglas de negocio
  ↓
Repositorio
  ↓
PostgreSQL
```

Las rutas no deberían contener las fórmulas del WBT ni consultas complejas. Los cálculos deben permanecer en `modules/calculos` y el acceso a datos en `repositories`.

## Alcance de los módulos

- `pruebas_wbt`: registro y ejecución de las pruebas.
- `calculos`: estandarización, fórmulas y procesamiento de resultados.
- `historial`: búsqueda, filtros y consulta de pruebas.
- `reportes`: gráficas y generación de PDF.
- `configuracion`: parámetros del protocolo, unidades y valores de referencia.

No se incluye un módulo de usuarios, autenticación o permisos porque no forma parte del alcance actual del sistema.
