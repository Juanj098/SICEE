# Resumen funcional del protocolo WBT 4.2.3

Este documento resume las partes del protocolo **Prueba de Ebullición de Agua (WBT 4.2.3)** relevantes para el registro de datos, el procesamiento y los reportes de SICEE.

> **Fuente:** `Docs/prueba de wbt.pdf`, publicado el 19 de marzo de 2014.
>
> **Nota:** el PDF remite las ecuaciones detalladas a los apéndices 4 y 6, pero esos apéndices no están incluidos en el archivo proporcionado. Las fórmulas indicadas como generales deben validarse contra la hoja oficial `WBT_data-calculation_sheet_4.2.3.xls` antes de implementarse.

## 1. Objetivo y alcance

El WBT simula una tarea de cocción controlada para medir el tiempo de ebullición, consumo de combustible, eficiencia térmica, capacidad de operación a alta y baja potencia y, opcionalmente, emisiones. Permite comparar estufas bajo condiciones equivalentes, pero no representa directamente la exposición de una persona a contaminantes ni sustituye una prueba de campo.

## 2. Proceso de la prueba

Una prueba completa tiene tres fases consecutivas y debe repetirse al menos tres veces por estufa. La versión 4.2.3 permite registrar hasta diez repeticiones.

### Fase I: inicio frío / alta potencia

La estufa comienza a temperatura ambiente. Se pesa el combustible, se coloca agua medida a temperatura ambiente, se registran temperatura y hora inicial, se enciende el fuego de forma reproducible y se calienta hasta el punto de ebullición local. Al finalizar se registran hora y temperatura final, combustible no utilizado, carbón restante y peso de la olla con agua.

### Fase II: inicio caliente / alta potencia

Se realiza inmediatamente después de la fase I, mientras la estufa continúa caliente. Se utiliza un nuevo paquete de combustible pesado previamente y agua a temperatura ambiente. Se repite el calentamiento hasta el punto de ebullición y se registran los pesos y tiempos finales. Después se reincorpora el combustible para la fase III.

### Fase III: baja potencia / hervir a fuego lento

Durante 45 minutos se mantiene el agua aproximadamente **3 °C por debajo** del punto de ebullición local. La prueba es inválida si la temperatura cae más de **6 °C por debajo** de dicho punto. Al finalizar se registran tiempo, temperatura, combustible no utilizado, carbón restante y peso del agua restante.

## 3. Condiciones normalizadas

- Olla grande: aproximadamente 7 litros, con 5 litros de agua por fase.
- Olla pequeña: aproximadamente 3.5 litros, con 2.5 litros de agua por fase.
- Usar la misma olla, cantidad de agua, tipo, tamaño y humedad del combustible en repeticiones comparables.
- Como referencia, el protocolo menciona leña de aproximadamente 1.5 cm × 1.5 cm y humedad baja, alrededor de 6.5 % o 10 % en base húmeda.
- El laboratorio debe estar protegido del viento y suficientemente ventilado.
- Balanzas, termómetros, cronómetros y equipo de emisiones deben calibrarse periódicamente.

## 4. Variables de entrada

### altura estufa (cm)

### area de camara de combustion (cm²)

### Identificación y configuración

- Código o número de prueba, fecha, lugar y evaluador.
- Número de repetición y conjunto de pruebas.
- Altitud y punto de ebullición local del agua.
- Modelo, fabricante, descripción, dimensiones y materiales de la estufa.
- Número y descripción de hornillos.

### Condiciones ambientales

- Temperatura del aire (°C).
- Humedad relativa (%).
- Presión atmosférica (kPa), si se miden emisiones.
- Condiciones de viento.

### Combustible

- Tipo, descripción, dimensiones y humedad (%).
- Poder calorífico neto y bruto.
- Contenido de carbono, si está disponible.
- Tipo de alimentación: continua o por lotes.
- Descripción del encendido y de la alimentación del fuego.

### Datos por fase

- Peso inicial y final del combustible (g).
- Peso del carbón y ceniza, cuando corresponda (g).
- Peso seco de la olla (g).
- Peso de la olla con agua al inicio y al final (g).
- Temperatura inicial y final del agua (°C).
- Hora o tiempo de inicio y finalización.
- Observaciones, interrupciones y cambios al protocolo.

## 5. Mediciones opcionales de emisiones

El protocolo contempla mediciones en la chimenea o campana de:

- `CO₂` (ppm).
- `CO` (ppm).
- Material particulado `PM` (µg/m³).
- Temperatura del ducto (°C).
- Flujo de chimenea o campana (m³/h).
- `Pitot delta-P` y presión atmosférica.
- Concentraciones base antes de iniciar cada fase.

El sistema debe guardar el método de captura, intervalo, equipo y unidades. Una concentración en ppm o µg/m³ no es suficiente para calcular masa emitida sin flujo, tiempo y condiciones del gas.

## 6. Fórmulas y variables derivadas

### Masa de agua

```text
m_agua_inicial = m_olla_agua_inicial - m_olla_seca
m_agua_final = m_olla_agua_final - m_olla_seca
m_agua_evaporada = m_agua_inicial - m_agua_final
```

### Tiempo de ebullición

```text
tiempo_ebullicion = tiempo_final - tiempo_inicial
```

Se calcula para inicio frío e inicio caliente usando la primera olla. El final ocurre cuando el agua alcanza el punto de ebullición local.

### Combustible consumido

```text
m_combustible_consumido = m_combustible_inicial - m_combustible_no_quemado_final
m_combustible_seco = m_combustible_consumido × (1 - humedad)
```

Cuando se pesa el carbón restante, el cálculo oficial debe aplicar la corrección de energía del carbón definida por el protocolo.

### Tiempo de ebullición corregido

Corrige pruebas con temperaturas iniciales o puntos de ebullición diferentes:

```text
tiempo_corregido = tiempo_ebullicion × 75 / (T_ebullicion - T_inicial)
```

El valor de 75 °C corresponde al aumento de referencia indicado por el protocolo. Debe validarse contra la hoja oficial.

### Energía transferida al agua

```text
Q_sensible = m_agua × c_agua × (T_final - T_inicial)
Q_latente = m_agua_evaporada × h_vaporizacion
Q_util = Q_sensible + Q_latente
```

`c_agua` es el calor específico del agua y `h_vaporizacion` el calor latente. Las unidades deben normalizarse antes de calcular resultados.

### Eficiencia térmica

```text
eficiencia_termica (%) = 100 × Q_util / Q_combustible
Q_combustible = m_combustible_seco × poder_calorifico_neto
```

El cálculo definitivo debe incluir la corrección por carbón residual que corresponda.

### Consumo específico

```text
consumo_especifico = combustible_seco_equivalente / litros_de_agua_utiles
consumo_energetico = consumo_especifico × poder_calorifico_neto
```

Debe diferenciarse si el resultado pertenece a inicio frío, inicio caliente, baja potencia o al valor combinado.

### Características de la estufa

```text
tiempo_fase = tiempo_final_fase - tiempo_inicial_fase
velocidad_combustion = combustible_consumido / tiempo_fase
energia_combustible = combustible_seco_consumido × poder_calorifico_neto
potencia_fase = energia_combustible / tiempo_fase
```

El `tiempo_fase` se calcula con los registros de tiempo de cada fase:

```text
tiempo_inicio_frio = fin_inicio_frio - inicio_inicio_frio
tiempo_inicio_caliente = fin_inicio_caliente - inicio_inicio_caliente
tiempo_baja_potencia = fin_baja_potencia - inicio_baja_potencia
```

Para una prueba válida, `tiempo_baja_potencia` debe ser aproximadamente **45 minutos**, es decir, **2700 segundos**. En las fases de inicio frío e inicio caliente, el tiempo corresponde desde el encendido o inicio registrado hasta que la primera olla alcanza el punto de ebullición local.

La velocidad de combustión se expresa normalmente en `g/min`. Para calcular la potencia en vatios (`W`), la energía debe estar en joules y el tiempo en segundos:

```text
potencia_fase (W) = energia_combustible (J) / tiempo_fase (s)
```

Si el poder calorífico está expresado en `MJ/kg` y la masa en gramos:

```text
energia_combustible (J) = combustible_seco (g) × poder_calorifico (MJ/kg)
                         × 1000 J/g
```

Para reportar la alta potencia se pueden conservar los valores de cada fase:

```text
potencia_inicio_frio = energia_inicio_frio / tiempo_inicio_frio
potencia_inicio_caliente = energia_inicio_caliente / tiempo_inicio_caliente
```

Si se necesita un único valor combinado de alta potencia, la forma recomendada es ponderar por el tiempo:

```text
potencia_alta = (energia_inicio_frio + energia_inicio_caliente)
                / (tiempo_inicio_frio + tiempo_inicio_caliente)
```

La potencia de baja potencia se calcula con el combustible consumido durante la fase de 45 minutos:

```text
potencia_baja = energia_baja_potencia / tiempo_baja_potencia
```

Finalmente, la relación de reducción compara la potencia alta con la potencia baja:

```text
relacion_reduccion = potencia_alta / potencia_baja
```

El combustible consumido debe ser el equivalente seco y debe aplicarse la corrección por carbón residual cuando corresponda. La hoja oficial del WBT puede definir un método específico para combinar las fases, por lo que estas expresiones deben contrastarse con el Apéndice 4 o la hoja de cálculo oficial antes de implementarlas.

### Emisiones

Las métricas dependen del contaminante y del método:

```text
emision_por_tarea = masa_contaminante
emision_por_combustible = masa_contaminante / combustible_seco_consumido
emision_por_tiempo = masa_contaminante / duracion_fase
emision_por_energia = masa_contaminante / energia_util_para_coccion
```

Para baja potencia también puede reportarse una tasa por tiempo y litro de agua. La conversión de concentración a masa debe seguir el método del Apéndice 6.

## 7. Validaciones del sistema

- Exigir punto de ebullición local, unidades y valores válidos.
- Validar que la temperatura inicial sea cercana a la temperatura ambiente.
- Exigir las tres fases para una prueba completa.
- Validar duración de 45 minutos en baja potencia.
- Invalidar o advertir cuando la temperatura baje más de 6 °C bajo el punto de ebullición.
- Mantener consistentes combustible, olla y cantidad de agua entre repeticiones.
- Registrar cualquier modificación, interrupción o dato faltante.
- Excluir pruebas inválidas de los promedios o marcarlas explícitamente.

## 8. Resultados y reporte

El reporte debería incluir identificación de la prueba y estufa, condiciones ambientales, combustible, datos por fase y repetición, tiempos de ebullición, consumo específico, eficiencia térmica, velocidad y potencia de combustión, emisiones si fueron medidas, promedios, variabilidad, advertencias y gráficas de temperatura contra tiempo.

Las fases de alta y baja potencia deben analizarse por separado además del resultado combinado, porque una estufa puede rendir bien en una fase y mal en otra.

## 9. Equipamiento mínimo

- Balanza de al menos 6 kg y precisión de ±1 g.
- Termómetro digital con precisión aproximada de 0.5 °C.
- Cronómetro.
- Medidor de humedad o sistema de secado y pesaje.
- Ollas estandarizadas e instrumentos para medir combustible, carbón y estufa.
- Equipo opcional para `CO₂`, `CO` y `PM`.
