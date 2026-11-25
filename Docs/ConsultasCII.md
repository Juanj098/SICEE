# Consultas pendientes al CII

**Proyecto:** SICEE — Sistema Integrado de Caracterización Energética y Emisiones
**Ensayo:** Water Boiling Test (WBT) versión 4.2.3
**Área:** Tecnología de la Madera, Centro de Investigación de Ingeniería (CII), Facultad de Ingeniería, USAC
**Fecha de elaboración:** 17 de noviembre de 2026
**Estado:** borrador para revisión

---

## 0. Cómo usar este documento

Este documento reúne las decisiones de protocolo que el equipo de SICEE **no puede resolver por su cuenta**: son datos o criterios que dependen de cómo el CII ejecuta realmente el ensayo.

- Cada consulta tiene un **ID** (`CII-01`, `CII-02`, ...) para poder referenciarla en reuniones, correos y actas.
- La columna **Respuesta del CII** queda vacía para que se complete en la reunión.
- La columna **Impacto** indica qué ecuación o parte del sistema cambia según la respuesta.
- Los estados posibles son: `Pendiente`, `En revisión`, `Resuelta`.
- Las referencias a ecuaciones usan la numeración de [`tablas.md`](./tablas.md); las referencias de hoja usan la sintaxis `Hoja!celda` del archivo [`WBT y seguridad.xlsx`](./WBT%20y%20seguridad.xlsx).

> Regla de trabajo: mientras una consulta siga `Pendiente`, el sistema aplica la **decisión asumida** registrada en la sección 9. Si el CII responde distinto, se corrigen el código, el modelo de datos y las ecuaciones.

---

## 1. Resumen de prioridades

| Prioridad | IDs | Motivo |
|---|---|---|
| **Alta** — cambia resultados ya calculados | CII-01, CII-02, CII-04, CII-05, CII-06, CII-14, CII-15 | Afectan directamente $F_d$, eficiencia, consumo específico y potencia |
| **Media** — afecta validación y captura | CII-07, CII-08, CII-10, CII-11, CII-12, CII-16, CII-17, CII-18 | Definen cuándo una prueba es válida o qué datos son obligatorios |
| **Baja** — afecta reportes y secciones futuras | CII-03, CII-09, CII-13, CII-19, CII-20, CII-21, CII-22, CII-23, CII-24 | Se necesitan al construir `resultado_prueba` y los reportes |

---

## 2. Combustible

| ID | Consulta | Impacto | Respuesta del CII |
|---|---|---|---|
| **CII-01** | La humedad que reporta el laboratorio, ¿está en **base seca** o en **base húmeda**? | Ec. (1): $H = H_{bs}/(1+H_{bs})$ solo si viene en base seca. Hoy el sistema asume base húmeda. Si es seca, cambian $F_d$, la eficiencia, el consumo específico y la potencia de **todas** las pruebas. | |
| **CII-02** | ¿Se mide el **poder calorífico neto (PCN)**, el **bruto (PCB)**, o ambos? Si solo se mide el bruto, ¿es válido estimar $PCN = PCB - 1.32$ MJ/kg para cualquier especie? | Ec. (2). El sistema usa el neto si existe y, si no, lo estima desde el bruto. Afecta $F_d$, $Q_{comb}$, eficiencia, $SE$ y $FP$. | |
| **CII-03** | ¿La humedad se determina **por prueba**, **por lote** de leña o **por especie**? ¿Cada cuánto se actualiza? | `combustible.humedad_pct` se guarda por registro de combustible, no por prueba. Define si hay que repetir el análisis de humedad en cada ensayo. | |

---

## 3. Carbón

| ID | Consulta | Impacto | Respuesta del CII |
|---|---|---|---|
| **CII-04** | ¿El carbón se pesa **al final de cada una de las tres fases**? ¿Se retira del brasero para pesarlo o se pesa dentro de él? | Ec. (9a), (9b) y (9c). Sin este dato no se puede descontar la energía que quedó en el carbón sin quemar, y $F_d$ sale sobreestimado. | |
| **CII-05** | El **recipiente** donde se pesa el carbón, ¿es el mismo en las tres fases y en todas las pruebas? ¿Su peso se registra una vez por prueba? | `prueba_wbt.peso_recipiente_carbon_kg`. Hoy es opcional. Si falta y sí se pesó carbón, el cálculo se detiene con un aviso. | |
| **CII-06** | Si **no se pesó el carbón** de una fase, ¿qué debe hacer el sistema: asumir $\Delta C = 0$, marcar la prueba como inválida, o dejar el resultado vacío? | Ec. (9) y (11). Hoy se asume $\Delta C = 0$, lo que equivale a "no hay corrección por carbón". Es una decisión de protocolo, no de código. | |

---

## 4. Fases y tiempos

| ID | Consulta | Impacto | Respuesta del CII |
|---|---|---|---|
| **CII-07** | ¿Se confirma que la fase de **alta potencia termina en el instante en que hierve la olla 1**, y que ese instante es el `t_final` que se registra? | Ec. (6) y (7). La hoja `Test-1` lo indica (`AA3`/`AA4` para inicio frío, `AI3`/`AI4` para inicio caliente) y el sistema ya lo aplica. Se pide confirmación formal para cerrar el tema. | |
| **CII-08** | ¿La fase de **baja potencia dura exactamente 45 minutos**? ¿Se acepta una tolerancia? ¿Se invalida la prueba si se excede? | Ec. (6), (25) y (26). La duración entra en la velocidad de combustión y en la potencia de fuego. La hoja dice `Finish: 45 min` (`AP3`). | |
| **CII-09** | El **inicio caliente** es opcional. Si no se realiza, ¿se registran sus resultados en cero o se omite la fase por completo? | Promedios de `resultado_prueba`. `tablas.md` indica que los resultados quedan en 0 y los promedios usan solo el inicio frío. | |
| **CII-10** | ¿La **olla 1** está presente siempre? ¿Puede faltar en alguna fase? | Ec. (7), (14), (20) y (23) usan la olla 1 como referencia. Hoy el sistema rechaza una fase sin olla 1. | |

---

## 5. Ollas y agua

| ID | Consulta | Impacto | Respuesta del CII |
|---|---|---|---|
| **CII-11** | ¿Cuántas ollas se permiten por prueba (1 a 4)? Si no se usan todas, ¿las celdas quedan vacías? | Regla "olla sin datos = 0 kg". Hoy una olla con los cuatro campos vacíos se ignora y una con datos parciales genera un aviso. Se necesita saber si "vacía" siempre significa "no se usó". | |
| **CII-12** | ¿Se registra la **temperatura inicial y final del agua de todas las ollas**, en todas las fases? | Ec. (13) requiere $T_{ini,j}$ de cada olla en alta potencia. La ec. (14) usa 25 °C fijo para las ollas 2 a 4 en baja potencia. Hoy el sistema exige los cuatro datos en todas las ollas. | |
| **CII-13** | ¿Debe validarse que la cantidad de agua sea la nominal (5 L en olla grande, 2.5 L en olla pequeña)? | Consistencia entre repeticiones. El modelo guarda `capacidad_l` y pesos, pero no una cantidad nominal de agua que permita comparar. | |

---

## 6. Temperaturas y punto de ebullición

| ID | Consulta | Impacto | Respuesta del CII |
|---|---|---|---|
| **CII-14** | ¿Cómo se obtiene el **punto de ebullición local** del agua: se mide, se calcula desde la presión barométrica o desde la altitud? ¿Quién lo registra? | Ec. (7), (13), (14) y (23). Un error de 1 °C en $T_{eb}$ mueve la corrección de 75 °C y por tanto el tiempo y el consumo corregidos. | |
| **CII-15** | En baja potencia, la referencia de **25 °C** para ponderar las ollas 2 a 4, ¿es un valor fijo o debe ser la temperatura del aire del laboratorio? | Ec. (14). Hoy es la constante `T_ref,baja = 25 °C`. | |
| **CII-16** | ¿El sistema debe **invalidar o advertir** si en baja potencia la temperatura se aparta más de 3 °C del punto de ebullición, o cae más de 6 °C por debajo? | Regla del protocolo ([`Resumen_WBT_4.2.3.md`](./Resumen_WBT_4.2.3.md), sección 2). Implementarlo exige guardar la serie de temperatura en el tiempo, que hoy no existe en el modelo. | |

---

## 7. Repeticiones y validez

| ID | Consulta | Impacto | Respuesta del CII |
|---|---|---|---|
| **CII-17** | El protocolo pide **mínimo 3 repeticiones** por estufa y permite hasta 10. ¿El sistema debe **bloquear** el reporte con menos de 3, o solo **advertir**? | `prueba_wbt.numero_repeticion` (1 a 10) y los promedios por conjunto de pruebas. | |
| **CII-18** | ¿Qué **motivos de invalidez** se registran y quién los decide? | `prueba_wbt.es_valida` y `prueba_wbt.motivo_invalidez`. Excluir pruebas inválidas cambia los promedios y los tiers. | |
| **CII-19** | ¿Se permiten **modificaciones al protocolo** durante un ensayo? ¿Dónde se documentan? | Trazabilidad del reporte. El resumen menciona un campo de modificaciones que aún no existe en el modelo. | |

---

## 8. Resultados por prueba y reportes

| ID | Consulta | Impacto | Respuesta del CII |
|---|---|---|---|
| **CII-20** | ¿Qué métricas debe reportar `resultado_prueba` y los promedios deben ser **simples** o **ponderados** por duración o por masa de agua? | Tabla `resultado_prueba`, aún no creada. Define el reporte y los tiers. | |
| **CII-21** | Si no hubo inicio caliente, ¿la eficiencia de alta potencia se reporta solo con el inicio frío? | Promedios. [`Resumen_WBT_4.2.3.md`](./Resumen_WBT_4.2.3.md) usa la media de frío y caliente, y el frío solo cuando no hay caliente. | |
| **CII-22** | En baja potencia, `energia_especifica_corregida_kj_l` guarda un valor **sin** la corrección de 75 °C. ¿Se renombra la columna o se separan los dos casos? | Claridad del modelo y del reporte. Es una decisión de nombres, no de cálculo. | |
| **CII-23** | Los **umbrales de tiers IWA** se toman de la hoja `Lists`, filas 15 a 22. ¿Se confirma que esa es la fuente vigente y que deben guardarse en una tabla actualizable? | Niveles por métrica en los reportes. | |
| **CII-24** | Para las emisiones, ¿cómo se convierten las concentraciones (ppm, µg/m³) a **gramos totales** por fase? ¿Qué caudal o factor de dilución se usa? | Campos `co2_total_g`, `co_total_g` y `pm_total_g`. Hoy se almacenan pero no se calculan; la sección de emisiones está diferida. | |

---

## 9. Decisiones asumidas por el sistema

Estas decisiones ya están aplicadas en el código y en la base. Se listan para que el CII las confirme o las corrija; si alguna cambia, se ajusta el sistema.

| Tema | Decisión asumida | Fuente |
|---|---|---|
| Fin de la fase de alta potencia | Termina cuando hierve la olla 1; ese instante es `t_final` | Hoja `Test-1`, celdas `AA3`/`AA4` y `AI3`/`AI4`; `tablas.md` |
| Duración de la baja potencia | 45 minutos | Hoja `Test-1`, celda `AP3` |
| Tiempo de ebullición | Es la duración de la fase; no se guarda como dato aparte | `tablas.md`, ec. (6) y (7) |
| Humedad del combustible | Se interpreta en base húmeda | Supuesto, ver CII-01 |
| Poder calorífico neto | Si falta, $PCN = \max(PCB-1.32,\ 0)$ MJ/kg | `tablas.md`, ec. (2) |
| Carbón no pesado | $\Delta C = 0$ (sin corrección por carbón) | Supuesto, ver CII-06 |
| Olla sin datos | Cuenta como 0 kg y se ignora | `tablas.md` |
| Olla con datos parciales | Genera un aviso, no se ignora en silencio | Criterio de robustez, ver CII-11 |
| Olla 1 | Obligatoria en todas las fases | Ec. (7), (14), (20) y (23) |
| Referencia de baja potencia | 25 °C fijo para las ollas 2 a 4 | `tablas.md`, constante $T_{ref,baja}$ |

---

## 10. Referencias

- [`tablas.md`](./tablas.md): ecuaciones (1) a (26) y correspondencia con `resultado_fase`.
- [`Resumen_WBT_4.2.3.md`](./Resumen_WBT_4.2.3.md): proceso del ensayo, condiciones normalizadas, métricas IWA y tiers.
- [`WBT y seguridad.xlsx`](./WBT%20y%20seguridad.xlsx): hoja de cálculo oficial del protocolo. Hojas relevantes: `Test Entry`, `Test-1`, `Results`, `IWA Summary`, `Fuel Moisture`, `Lists`.
- [`ModeloDatos.md`](./ModeloDatos.md) y [`er.dbml`](./er.dbml): estructura de la base de datos.
- [`ModulosBackend.md`](./ModulosBackend.md): módulos del backend.

---

## 11. Registro de respuestas

| Fecha | ID | Respuesta del CII | Acordado por | Cambios aplicados |
|---|---|---|---|---|
| | | | | |
