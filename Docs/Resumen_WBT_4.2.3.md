# Resumen funcional del protocolo WBT 4.2.3

Este documento resume las partes del protocolo **Prueba de Ebullición de Agua (WBT 4.2.3)** relevantes para el registro de datos, el procesamiento y los reportes de SICEE.

> **Fuente:** `Docs/prueba de wbt.pdf`, publicado el 19 de marzo de 2014.
>
> **Nota:** el PDF remite las ecuaciones detalladas a los apéndices 4 y 6, pero esos apéndices no están incluidos en el archivo proporcionado. Las fórmulas de la sección 6 se contrastaron con las fórmulas del libro `WBT_y_seguridad.xlsx` (estructura de la hoja WBT 4.2.3; hojas `Test-1`, `Results` y `Lists`) y llevan entre paréntesis la celda de referencia. Antes de darlas por definitivas, conviene cargar una misma prueba real en la hoja y en SICEE y comparar los resultados.

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

### 6.1 Convenciones, constantes y casos especiales

**Subíndices**

- `c` = inicio frío, `h` = inicio caliente, `s` = baja potencia (simmer).
- `i` = número de olla (1 a 4). La olla 1 es la que define el tiempo de ebullición.
- `ini` / `fin` = valor al inicio / al final de la fase.

**Unidades de cálculo (las de la hoja):** masas en g, tiempos en min, temperaturas en °C, poder calorífico en kJ/kg, energía en J y potencia en W. SICEE almacena masas en kg y poder calorífico en MJ/kg, por lo que antes de calcular se convierte: `kg × 1000 = g` y `MJ/kg × 1000 = kJ/kg`. Con esas unidades, `g × kJ/kg = J`, y `J / s = W`.

**Constantes**

| Constante | Valor | Uso |
|---|---|---|
| `c_agua` | 4.186 kJ/(kg·°C) | calor sensible del agua y corrección del combustible |
| `h_vap` (eficiencia) | 2260 kJ/kg | calor latente en la eficiencia térmica |
| `h_vap` (combustible) | 2257 kJ/kg | energía para evaporar la humedad del combustible |
| `ΔT_ref` | 75 °C | corrección por temperatura de tiempo y consumo |
| `ΔHHV→LHV` | 1320 kJ/kg | neto a partir del bruto medido |
| `T_ref_simmer` | 25 °C | ponderación del agua restante de las ollas 2 a 4 |
| `R` | 0.008314 kJ/(mol·K) | conversión de concentraciones a masa (emisiones) |
| `LHV_carbón` por defecto | 29 500 kJ/kg (biomasa) | si no se mide |
| `fC_carbón` por defecto | 0.95 | fracción másica de carbono del carbón |

La hoja usa dos valores de calor latente (2260 y 2257). Para reproducir sus resultados se conservan ambos; deben quedar como constantes con nombre y versión del protocolo, no como números sueltos en el código.

**Casos especiales de la hoja**

- Si no se registró inicio caliente (`f_m,h = 0`), sus resultados quedan en 0 y los promedios de alta potencia usan solo el inicio frío.
- Los promedios entre pruebas incluyen solo valores mayores que 0.
- Una olla sin datos se trata como 0 g.
- Se supone `1 L de agua = 1000 g`.

### 6.2 Preparación de datos

```text
MC_bh = MC_bs / (1 + MC_bs)            # si el medidor entrega base seca (hoja Fuel Moisture!F14)
LHV   = max(HHV_medido − 1320, 0)      # si se midió el bruto y no el neto (hoja General Information!L19)
```

`MC` es la humedad del combustible en **base húmeda y como fracción** (0.12, no 12). Si el combustible no se midió, el poder calorífico, el poder calorífico del carbón y la fracción de carbono se toman de la tabla de valores por defecto de la hoja (`Calorific values`).

### 6.3 Masa de agua por olla

```text
m_agua_ini,i = P_ini,i − m_seca,i
m_agua_fin,i = P_fin,i − m_seca,i
m_evap       = Σ_i ( P_ini,i − P_fin,i )          # hoja W31, AA31, AP31
```

`P` es el peso de la olla con agua y `m_seca` el peso de la olla vacía.

### 6.4 Tiempo de fase y tiempo de ebullición

```text
Δt = t_fin − t_ini                                # min (hoja: (AA6−W6)×1440, etc.)
Δt_corr = Δt × 75 / (T_b − T_ini,1)               # solo c y h, con la olla 1 (hoja W34, AA34)
```

`T_b` es el punto de ebullición local. Para inicio frío e inicio caliente, `Δt` es el tiempo hasta que la olla 1 alcanza la ebullición. Para baja potencia, `Δt_s` debe ser ≈ 45 min.

### 6.5 Combustible consumido, carbón y combustible seco equivalente

```text
f_m  = f_ini − f_fin                              # combustible húmedo consumido (hoja W28, AA28, AP28)

Δc_c = cc_c − m_rec                               # carbón neto, inicio frío (W29)
Δc_h = cc_h − m_rec                               # inicio caliente (AA29)
Δc_s = (cc_s − m_rec) − Δc_c                      # baja potencia: se descuenta lo del inicio frío (AP29)

q_agua = 4.186 × (T_b − T_a) + 2257               # kJ por kg de agua del combustible

f_d = [ f_m × ( LHV × (1 − MC) − MC × q_agua ) − Δc × LHV_carbón ] / LHV      # g (W30, AA30, AP30)
```

`cc` es el peso del carbón más su recipiente al final de la fase, `m_rec` el peso del recipiente vacío y `T_a` la temperatura del aire.

`f_d` es el **combustible seco equivalente**: los gramos de leña seca que liberarían la misma energía útil, una vez descontada la energía que se gasta en calentar y evaporar el agua del combustible y la energía del carbón que quedó sin quemar. Es la cantidad que se usa en todas las fórmulas siguientes (eficiencia, consumo, velocidad y potencia). **No equivale a `f_m × (1 − MC)`**, que ignora esos dos descuentos.

### 6.6 Agua efectiva y agua restante

Inicio frío e inicio caliente (hoja W32, AA32):

```text
m_ef = Σ_i  ( P_fin,i − m_seca,i ) × ( T_fin,i − T_ini,i ) / ( T_b − T_ini,i )
```

Baja potencia (hoja AP32):

```text
m_rest = ( P_fin,1 − m_seca,1 )
       + Σ_{i=2..4} ( P_fin,i − m_seca,i ) × ( T_fin,i − 25 ) / ( T_b − 25 )
```

### 6.7 Eficiencia térmica

Inicio frío e inicio caliente (hoja W35, AA35):

```text
Q_sensible = 4.186 × Σ_i ( P_ini,i − m_seca,i ) × ( T_fin,i − T_ini,i )     # J
Q_latente  = 2260 × m_evap                                                    # J
η = ( Q_sensible + Q_latente ) / ( f_d × LHV )                               # fracción; ×100 para %
```

Baja potencia (hoja AP34):

```text
m_prom = ( P_ini,1 − m_seca,1 + m_rest ) / 2
η_s = ( 4.186 × m_prom × ( T_fin,1 − T_ini,1 ) + 2260 × m_evap,s ) / ( f_d,s × LHV )
```

En baja potencia la hoja usa solo la temperatura de la olla 1.

### 6.8 Velocidad de combustión, consumo específico y energía específica

```text
r = f_d / Δt                                      # g/min (hoja W36, AA36, AP35)

SC      = 1000 × f_d / m_ef                       # g de combustible por litro hervido (W37, AA37)
SC_corr = SC × 75 / ( T_b − T_ini,1 )             # corregido por temperatura (W38, AA38)
SE_corr = SC_corr / 1000 × LHV                    # kJ/L (W39, AA39)

SC_s = 1000 × f_d,s / m_rest                      # g por litro de agua restante (AP36)
SE_s = SC_s / 1000 × LHV                          # kJ/L (AP39)
```

El consumo específico se calcula por separado para inicio frío, inicio caliente y baja potencia; no se mezclan.

### 6.9 Potencia de fuego (Firepower)

```text
FP [W] = f_d × LHV / ( Δt × 60 )                  # hoja W40, AA40, AP37
```

Con las unidades de SICEE: `FP [kW] = f_d [kg] × LHV [MJ/kg] × 1000 / ( Δt [min] × 60 )`.

Calcúlala siempre con `f_d` (6.5), no con `f_m × (1 − MC)`.

### 6.10 Relación de reducción y valores de referencia para 5 L

```text
TDR = FP_c / FP_s                                 # potencia del inicio frío / potencia de baja potencia (AP38)

BF = 5 × ( promedio(SC_corr,c ; SC_corr,h) + SC_s )     # g de combustible; si no hay hot start, solo SC_corr,c (AP40)
BE = BF / 1000 × LHV                                     # kJ (AP41)
```

### 6.11 Métricas IWA y niveles (tiers)

```text
η_alta  = ( η_c + η_h ) / 2                       # si no hay hot start, η_c (AE44)
SC_baja = f_d,s × LHV / ( m_rest × Δt_s × 1000 )  # MJ/(min·L) (AE45)
```

Cada métrica se calcula por prueba. El nivel de una estufa se obtiene del **promedio de las pruebas válidas** y solo se reporta si hay **3 o más pruebas** (en otro caso, "NA").

| Métrica | Unidad | Tier 0 | Tier 1 | Tier 2 | Tier 3 | Tier 4 |
|---|---|---|---|---|---|---|
| Eficiencia térmica alta potencia | % | < 15 | ≥ 15 | ≥ 25 | ≥ 35 | ≥ 45 |
| Consumo específico baja potencia | MJ/(min·L) | > 0.05 | ≤ 0.05 | ≤ 0.039 | ≤ 0.028 | ≤ 0.017 |
| CO alta potencia | g/MJ | > 16 | ≤ 16 | ≤ 11 | ≤ 9 | ≤ 8 |
| CO baja potencia | g/(min·L) | > 0.2 | ≤ 0.2 | ≤ 0.13 | ≤ 0.1 | ≤ 0.09 |
| PM alta potencia | mg/MJ | > 979 | ≤ 979 | ≤ 386 | ≤ 168 | ≤ 41 |
| PM baja potencia | mg/(min·L) | > 8 | ≤ 8 | ≤ 4 | ≤ 2 | ≤ 1 |
| CO en interiores | g/min | > 0.97 | ≤ 0.97 | ≤ 0.62 | ≤ 0.49 | ≤ 0.42 |
| PM en interiores | mg/min | > 40 | ≤ 40 | ≤ 17 | ≤ 8 | ≤ 2 |

Fuente: hoja `Lists`, filas 15 a 22. Estos umbrales deben guardarse en una tabla, no en el código, para poder actualizarlos.

### 6.12 Emisiones

**Datos de partida.** Por fase: `C_CO2` y `C_CO` (ppm), `C_PM` (µg/m³), temperatura del ducto `T_d` (°C). Concentraciones de fondo: `b_CO2`, `b_CO`, `b_PM`. Presión atmosférica `P` (kPa), flujo de la campana `Q` (m³/h) y fracción de carbono del combustible `fC` y del carbón `fC_carbón`.

**Volumen y densidad molar del gas** (hoja W55, AE55):

```text
V   = Q × Δt / 60                                 # m³ de gas de escape en la fase
ρ_m = P / ( R × ( T_d + 273.15 ) )                # mol/m³
```

La hoja ofrece **tres métodos** para obtener la masa emitida `m` (g) de cada contaminante. El método debe guardarse con la prueba.

**Método 1: balance de carbono** (hoja W56 a W71)

```text
CC     = ( C_CO2 − b_CO2 ) + ( C_CO − b_CO ) + ( C_PM − b_PM ) / 15 / ρ_m      # ppm de carbono (W56)
Cc     = ρ_m × CC × 1e-6 × 12                                                   # g de C por m³ (W57)
f_est  = Cc × V / fC                                                            # g de combustible estimados (W58)
CB     = f_est / [ (1 − MC) × f_m − Δc × fC_carbón / fC ]                       # balance de carbono (W59)

EF_CO2 = ( ( C_CO2 − b_CO2 ) × 44/12 ) / ( CC / fC ) × 1000                     # g/kg de combustible (W65)
EF_CO  = ( ( C_CO  − b_CO  ) × 28/12 ) / ( CC / fC ) × 1000                     # (W66)
EF_PM  = ( C_PM − b_PM ) / ( Cc / fC ) × 1000 / 1e6                             # (W67)

m_x    = EF_x × [ f_m × (1 − MC) − Δc × fC_carbón / fC ] / 1000                 # g (W69 a W71)
```

**Método 2: captura total** (hoja W73 a W75)

```text
m_CO2 = V × ( C_CO2 − b_CO2 ) × 44 × P / ( R × ( T_d + 273.15 ) ) / 1e6
m_CO  = V × ( C_CO  − b_CO  ) × 28 × P / ( R × ( T_d + 273.15 ) ) / 1e6
m_PM  = V × ( C_PM  − b_PM  ) / 1e6
```

**Método 3: totales ingresados por el usuario.** Se usan directamente `m_CO2`, `m_CO` y `m_PM` medidos (g).

**Emisión por agua hervida** (W61 a W63): `E_x = m_x / m_ef × 1000` en g/L (en baja potencia se usa `m_rest`).

**Métricas IWA de emisiones** (hoja AE46 a AE51; `η` como fracción):

```text
CO_alta  [g/MJ]       = 1e6 / LHV × ( m_CO,c / (η_c × f_d,c) + m_CO,h / (η_h × f_d,h) ) / 2
PM_alta  [mg/MJ]      = 1e9 / LHV × ( m_PM,c / (η_c × f_d,c) + m_PM,h / (η_h × f_d,h) ) / 2
CO_baja  [g/(min·L)]  = m_CO,s / ( Δt_s × m_rest ) × 1000
PM_baja  [mg/(min·L)] = m_PM,s / ( Δt_s × m_rest ) × 1e6

CO_int   [g/min]  = max( promedio( m_CO,c/Δt_c ; m_CO,h/Δt_h ) ; m_CO,s/Δt_s )
PM_int   [mg/min] = max( promedio( m_PM,c/Δt_c ; m_PM,h/Δt_h ) ; m_PM,s/Δt_s ) × 1000
```

Si no hay inicio caliente, los promedios usan solo el inicio frío.

**Referencia de emisiones para 5 L** (W77, W78): `CO_5L = 5 × ( promedio(E_CO,c ; E_CO,h) + E_CO,s )`, y lo mismo para PM.

Las emisiones se calculan solo si la prueba tiene mediciones. La conversión de concentración a masa debe seguir el método del Apéndice 6, que no está en el PDF disponible.

### 6.13 Diferencias con la versión anterior de este documento

| Tema | Versión anterior | Ahora (según la hoja) |
|---|---|---|
| Combustible seco | `consumido × (1 − humedad)` | `f_d` de 6.5, con descuento de energía del agua y del carbón |
| Energía del combustible | `seco × PCI` | `f_d × LHV` |
| Potencia de alta potencia | valor combinado ponderado por tiempo | se reporta por fase: la hoja no calcula un valor combinado |
| Relación de reducción | `potencia_alta / potencia_baja` | `FP_c / FP_s` (potencia del inicio frío) |
| Eficiencia alta potencia IWA | no definida | promedio simple de frío y caliente |
| Litros de agua en consumo específico | "litros útiles" | agua efectiva (frío, caliente) o agua restante (baja potencia) |
| Tiempo corregido | "validar contra la hoja" | confirmado: `× 75 / (T_b − T_ini,1)` |
| Calor latente | un solo valor | 2260 en eficiencia y 2257 en el combustible |

Si se quiere conservar un valor combinado de alta potencia, `(E_c + E_h) / (Δt_c + Δt_h)` puede calcularse como dato adicional, pero no es el valor oficial de la hoja.

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

## 10. Datos a agregar al modelo de datos

Cambios respecto a `sicee_schema.sql`. Se ordenan por lo que bloquea el cálculo.

### 10.1 Necesarios para reproducir los cálculos de la sección 6

| Tabla | Campo o tabla nueva | Para qué |
|---|---|---|
| `combustible` | `humedad_medida_base_seca_pct` (opcional) | el medidor entrega base seca; se convierte a base húmeda (6.2) |
| `combustible` | `poder_calorifico_medido` (boolean) | indica si el poder calorífico fue medido o tomado por defecto; si solo se midió el bruto, el neto es `bruto − 1.32 MJ/kg` |
| `combustible` | `descripcion`, `longitud_promedio_cm`, `seccion_transversal_cm`, `descripcion_encendido` | datos del combustible y del encendido que pide el protocolo; el material de encendido se pesa junto con la leña |
| `combustible_referencia` (nueva) | `tipo`, `poder_calorifico_bruto_mj_kg`, `poder_calorifico_neto_mj_kg`, `poder_calorifico_carbon_mj_kg`, `fraccion_carbono`, `fraccion_carbono_carbon` | valores por defecto de la hoja (`Calorific values`) cuando no se mide |
| `prueba_wbt` | `version_protocolo` (ej. "4.2.3") | congela las constantes de cálculo usadas, para no cambiar resultados antiguos si cambia el protocolo |
| `prueba_wbt` | `conjunto_pruebas_id` | agrupa las repeticiones de una estufa (3 a 10) para promedios y tiers |
| `conjunto_pruebas` (nueva) | `id`, `estufa_id`, `descripcion` | el conjunto de pruebas que menciona el protocolo; `unique (conjunto, numero_repeticion)` con repetición entre 1 y 10 |
| `prueba_wbt` | `es_valida` (boolean), `motivo_invalidez`, `modificaciones_protocolo` | excluir pruebas inválidas de los promedios y registrar cambios al protocolo |
| `fase_prueba` | `peso_ceniza_kg` (opcional), `observaciones` | el protocolo registra carbón y ceniza, y las interrupciones por fase |
| `olla` | `tipo` (grande o pequeña), `capacidad_l`, `agua_nominal_l`, `descripcion` | olla de 7 L con 5 L de agua, o de 3.5 L con 2.5 L; para validar consistencia entre repeticiones |
| `condiciones_ambientales` | `condicion_viento` (catálogo) | la hoja usa una lista de condiciones de viento además de la velocidad |
| `estufa` | `numero_hornillos`, `descripcion_hornillos`, `tipo_estufa` | variables de configuración del protocolo |
| `registro_temperatura` (nueva) | `fase_id`, `olla_id`, `instante`, `temperatura_c` | gráficas de temperatura contra tiempo y validar la baja potencia (3 °C y 6 °C bajo la ebullición) |

### 10.2 Resultados que hoy no tienen dónde guardarse

| Tabla | Campos | Notas |
|---|---|---|
| `resultado_fase` | `energia_especifica_corregida_kj_l` | `SE_corr` (6.8) |
| `resultado_fase` | semántica de `masa_agua_efectiva_kg` | en frío y caliente es `m_ef`; en baja potencia es `m_rest` (conviene documentarlo o separar en dos campos) |
| `resultado_prueba` (nueva) | `eficiencia_alta_pct`, `consumo_especifico_baja_mj_min_l`, `relacion_reduccion`, `combustible_ref_5l_g`, `energia_ref_5l_kj` | métricas IWA y valores de referencia por prueba (6.10 y 6.11) |
| `resultado_prueba` | `co_alta_g_mj`, `co_baja_g_min_l`, `pm_alta_mg_mj`, `pm_baja_mg_min_l`, `co_interior_g_min`, `pm_interior_mg_min`, `co_5l_g`, `pm_5l_g` | métricas de emisiones IWA (6.12) |
| `resultado_prueba` | un tier (0 a 4) por cada métrica | niveles por prueba |
| `resultado_conjunto` (nueva) | promedio, desviación estándar y coeficiente de variación de cada métrica; número de pruebas válidas; tier por métrica ("NA" si hay menos de 3 pruebas) | el reporte pide promedios y variabilidad |
| `resultado_emisiones_fase` (nueva) | `volumen_escape_m3`, `carbono_escape_g_m3`, `combustible_estimado_g`, `balance_carbono`, `ef_co2_g_kg`, `ef_co_g_kg`, `ef_pm_g_kg`, `masa_co2_g`, `masa_co_g`, `masa_pm_g`, `emision_por_litro_*` | resultados calculados; distintos de los totales que el usuario puede ingresar en `mediciones_opcionales` |
| `umbral_tier_iwa` (nueva) | `metrica`, `tier`, `operador`, `umbral` | tabla de 6.11; actualizable sin cambiar código |

### 10.3 Emisiones

| Tabla | Campos | Notas |
|---|---|---|
| `emisiones_prueba` | `metodo_calculo` (1 balance de carbono, 2 captura total, 3 totales ingresados) | define qué fórmulas de 6.12 se aplican |
| `emisiones_prueba` | `metodo_captura`, `intervalo_muestreo_s`, `delta_p_pitot_pa` | el protocolo pide guardar método, intervalo y Pitot ΔP |
| `mediciones_opcionales` | `co2_fondo_ppm`, `co_fondo_ppm`, `pm_fondo_ug_m3` por fase | el protocolo pide la concentración base antes de **cada fase**; la hoja usa un solo juego por prueba. Se propone guardarlo por fase y, si el usuario ingresa un solo valor, copiarlo a las tres fases |
| `equipo_medicion` (nueva) y `prueba_equipo` | `tipo`, `marca`, `modelo`, `serie`, `precision`, `unidades`, `fecha_calibracion` | trazabilidad de balanzas, termómetros y analizadores |

### 10.4 Puntos por confirmar con el CII

- **Carbón entre fases:** en la hoja, el carbón del inicio caliente toma por defecto el valor del inicio frío, y el de baja potencia se calcula como diferencia con el inicio frío. Confirmar cómo se pesa el carbón en cada fase en el laboratorio.
- **Concentraciones de fondo:** por fase (protocolo) o por prueba (hoja).
- **Seguridad:** la hoja `Lists` incluye niveles de seguridad (índice Johnson: 45, 75, 88 y 95), pero el libro recibido no trae una hoja de cálculo para ese dato. Confirmar si SICEE debe incluirlo.
- **Resultados calculados:** si se guardan como copia fija (recomendado, junto con `version_protocolo`) o se recalculan siempre.