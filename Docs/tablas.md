* Investigador
    └── Nombre_investigador

* Laboratorio
    ├── Institucion
    ├── Direccion
    └── Descripcion

* Estufa
    ├── Marca
    ├── Fabricante
    ├── Area_camara_cm2
    ├── Altura_cm
    ├── Numero_hornillas
    ├── Material
    └── Descripcion

* Condiciones_ambientales
    ├── Temperatura_c
    ├── Humedad_relativa_pct
    ├── Altitud_m
    ├── Presion_atmosferica_kpa
    ├── Viento_ms
    ├── Condicion_viento
    └── Punto_ebullicion_c

* Combustible
    ├── Tipo
    ├── Longitud_combustible_cm
    ├── Ancho_combustible_cm
    ├── Humedad_pct
    ├── Poder_calorifico_neto_mj_kg
    ├── Poder_calorifico_bruto_mj_kg
    ├── Poder_calorifico_carbon_mj_kg
    ├── Contenido_carbono_carbon_pct
    ├── Tipo_alimentacion
    ├── Contenido_carbono_pct
    └── Descripcion

* Conjunto_pruebas
    ├── Estufa (selección de una existente)
    └── Descripcion

* Prueba_wbt
    ├── Fecha
    ├── Investigador (selección)
    ├── Laboratorio (selección)
    ├── Combustible (selección)
    ├── Condiciones_ambientales (selección)
    ├── Conjunto_pruebas (selección)
    ├── Peso_recipiente_carbon_kg
    ├── Numero_repeticion
    ├── Es_valida
    ├── Motivo_invalidez
    └── Observaciones

* Fase_prueba (una por cada fase: inicio frío, inicio caliente, baja potencia)
    ├── Tipo_fase
    ├── T_inicial
    ├── T_final
    ├── Peso_combustible_inicial_kg
    ├── Peso_combustible_final_kg
    ├── Peso_carbon_con_recipiente_kg
    ├── Peso_cenizas_kg
    └── Observaciones

* Olla (una por cada olla de la prueba)
    ├── Numero_olla
    ├── Peso_seco_kg
    └── Capacidad_l

* Olla_fase (una por cada olla en cada fase)
    ├── Temperatura_inicial_agua_c
    ├── Temperatura_final_agua_c
    ├── Peso_con_agua_inicial_kg
    └── Peso_con_agua_final_kg

* Emisiones_prueba (solo si la prueba mide emisiones)
    ├── Caudal_campana_m3_h
    ├── Metodo_captura
    ├── Metodo_calculo (1 = balance de carbono, 2 = captura total, 3 = totales ingresados)
    ├── Intervalo_muestreo_s
    └── Delta_p_pitot_pa

* Mediciones_opcionales (una por fase, solo si hay mediciones)
    ├── Temperatura_ducto_c
    ├── CO_ppm
    ├── PM_ug_m3
    ├── CO2_ppm
    ├── CO2_fondo_ppm
    ├── CO_fondo_ppm
    ├── PM_fondo_ug_m3
    ├── CO2_total_g   (solo si metodo_calculo = 3)
    ├── CO_total_g    (solo si metodo_calculo = 3)
    └── PM_total_g    (solo si metodo_calculo = 3)



# ecuaciones a utilizar

# Ecuaciones del cálculo WBT 4.2.3 en SICEE

Basado en la sección 6 del resumen funcional del protocolo. Cada ecuación trae una línea **En palabras** para entender qué hace.

## 0. Cómo leer este documento

**Unidades que usa SICEE:** masas en kg, tiempos en min, temperaturas en °C. El poder calorífico se guarda en MJ/kg, pero en las ecuaciones se usa en kJ/kg (se multiplica por 1000 al leerlo). Con estas unidades, `kg × kJ/kg = kJ` y `kJ / s = kW`.

**Fases:** inicio frío, inicio caliente (ambas de *alta potencia*) y baja potencia. Cada fase se calcula por separado.

**Ollas:** el subíndice *j* es el número de olla (1 a 4). La **olla 1** es la que define el tiempo de ebullición y la temperatura de referencia.

**Casos especiales**

- Si no hay inicio caliente, sus resultados quedan en 0 y los promedios usan solo el inicio frío.
- Una olla sin datos cuenta como 0 kg.
- Se supone 1 L de agua = 1 kg.

### Datos que se miden o ingresan

| Símbolo | Qué es | Unidad | Columna |
|---|---|---|---|
| $P_{ini,j}$, $P_{fin,j}$ | Peso de la olla *j* **con agua**, al inicio y al final de la fase | kg | `olla_fase.peso_con_agua_*_kg` |
| $P_{seca,j}$ | Peso de la olla *j* **vacía** | kg | `olla.peso_seco_kg` |
| $T_{ini,j}$, $T_{fin,j}$ | Temperatura del agua de la olla *j*, al inicio y al final | °C | `olla_fase.temperatura_*_agua_c` |
| $T_{eb}$ | Punto de ebullición local del agua | °C | `condiciones_ambientales.punto_ebullicion_c` |
| $T_{aire}$ | Temperatura del aire del laboratorio | °C | `condiciones_ambientales.temperatura_c` |
| $F_{ini}$, $F_{fin}$ | Peso de la leña antes y después de la fase | kg | `fase_prueba.peso_combustible_*_kg` |
| $H$ | Humedad de la leña como **fracción** (12 % → 0.12) | – | `combustible.humedad_pct` ÷ 100 |
| $PCN$ | Poder calorífico neto de la leña | kJ/kg | `combustible.poder_calorifico_neto_mj_kg` × 1000 |
| $PCN_{carb}$ | Poder calorífico neto del carbón | kJ/kg | `combustible.poder_calorifico_carbon_mj_kg` × 1000 |
| $C_{fase}$ | Peso del carbón **con su recipiente** al final de la fase | kg | `fase_prueba.peso_carbon_con_recipiente_kg` |
| $C_{rec}$ | Peso del recipiente del carbón **vacío** | kg | `prueba_wbt.peso_recipiente_carbon_kg` |
| $t_{ini}$, $t_{fin}$ | Hora de inicio y fin de la fase | timestamp | `fase_prueba.t_inicial`, `t_final` |

### Constantes

| Constante | Valor | Para qué sirve |
|---|---|---|
| $c_{agua}$ | 4.186 kJ/(kg·°C) | Energía para subir 1 °C la temperatura de 1 kg de agua |
| $h_{vap}$ | 2260 kJ/kg | Energía para evaporar 1 kg de agua (se usa en la eficiencia) |
| $h_{vap,comb}$ | 2257 kJ/kg | Energía para evaporar 1 kg de agua **de la leña** (se usa en $F_d$) |
| $\Delta T_{ref}$ | 75 °C | Subida de temperatura de referencia (25 → 100 °C) para corregir tiempo y consumo |
| $T_{ref,baja}$ | 25 °C | Temperatura de referencia para ponderar las ollas 2 a 4 en baja potencia |

Los dos valores de calor latente (2260 y 2257) son distintos a propósito: así lo hace la hoja de referencia.

## 1. Preparación de datos

Si el medidor de humedad de la leña entrega base seca ($H_{bs}$), se pasa a base húmeda:

$$H = \frac{H_{bs}}{1 + H_{bs}} \qquad (1)$$

Si solo se midió el poder calorífico bruto ($PCB$, kJ/kg), el neto se obtiene así:

$$PCN = \max(PCB - 1320,\ 0) \qquad (2)$$

**En palabras:** la humedad debe estar siempre en base húmeda y como fracción. El poder calorífico neto es el bruto menos la energía que se va al evaporar el agua que se forma al quemar.

## 2. Agua por olla

$$A_{ini,j} = P_{ini,j} - P_{seca,j} \qquad (3)$$

$$A_{fin,j} = P_{fin,j} - P_{seca,j} \qquad (4)$$

$$A_{evap} = \sum_j \left(P_{ini,j} - P_{fin,j}\right) \qquad (5)$$

**En palabras:** se pesa la olla con agua y se resta la olla vacía para saber cuánta agua hay. El agua evaporada es lo que perdieron todas las ollas entre el inicio y el final.

Los totales de la fase son $A_{ini} = \sum_j A_{ini,j}$ y $A_{fin} = \sum_j A_{fin,j}$.

## 3. Tiempos

$$\Delta t = t_{fin} - t_{ini} \quad [\text{min}] \qquad (6)$$

$$\Delta t_{corr} = \Delta t \cdot \frac{75}{T_{eb} - T_{ini,1}} \quad [\text{min}] \qquad (7)$$

**En palabras:** $\Delta t$ es cuánto duró la fase. En inicio frío e inicio caliente es el tiempo hasta que la olla 1 hirvió; en baja potencia debe ser ≈ 45 min. $\Delta t_{corr}$ es ese tiempo "ajustado" como si el agua hubiera partido de 25 °C y subido 75 °C; así se pueden comparar pruebas que arrancaron a temperaturas distintas. **La ecuación (7) solo aplica en inicio frío e inicio caliente.**

## 4. Combustible

### 4.1 Combustible y carbón

$$F_{cons} = F_{ini} - F_{fin} \quad [\text{kg}] \qquad (8)$$

**En palabras:** es la leña que se gastó, tal como se pesó, con su humedad incluida.

El carbón que quedó sin quemar ($\Delta C$) depende de la fase:

$$\Delta C_{frío} = C_{frío} - C_{rec} \qquad (9a)$$

$$\Delta C_{caliente} = C_{caliente} - C_{rec} \qquad (9b)$$

$$\Delta C_{baja} = \left(C_{baja} - C_{rec}\right) - \Delta C_{frío} \qquad (9c)$$

**En palabras:** al peso del carbón con recipiente se le resta el recipiente vacío. En baja potencia además se descuenta el carbón que ya venía del inicio frío, para contar solo el que se formó en esa fase.

### 4.2 Combustible seco equivalente ($F_d$)

Primero, la energía que se gasta en calentar y evaporar el agua que trae la leña (por cada kg de agua):

$$q_{agua} = c_{agua}\,(T_{eb} - T_{aire}) + 2257 \quad [\text{kJ/kg}] \qquad (10)$$

Luego:

$$F_d = \frac{F_{cons}\left[PCN\,(1 - H) - H\,q_{agua}\right] - \Delta C \cdot PCN_{carb}}{PCN} \quad [\text{kg}] \qquad (11)$$

**En palabras:** $F_d$ son los kg de leña **seca** que habrían liberado la misma energía útil que la que realmente se aprovechó. Se parte de la energía de la leña seca consumida ($F_{cons}\,PCN\,(1-H)$), se resta la energía gastada en evaporar el agua de la leña ($F_{cons}\,H\,q_{agua}$) y la energía que quedó guardada en el carbón sin quemar ($\Delta C\,PCN_{carb}$). Al dividir entre $PCN$ el resultado vuelve a kg de leña.

**No es lo mismo que $F_{cons}(1 - H)$**: esa versión ignora los dos descuentos. $F_d$ es la base de casi todos los cálculos siguientes.

Energía del combustible:

$$Q_{comb} = F_d \cdot PCN \quad [\text{kJ}] \qquad (12)$$

## 5. Agua efectiva y agua restante

**Inicio frío e inicio caliente (agua efectiva):**

$$A_{ef} = \sum_j A_{fin,j}\cdot\frac{T_{fin,j} - T_{ini,j}}{T_{eb} - T_{ini,j}} \quad [\text{kg}] \qquad (13)$$

**En palabras:** es el agua que quedó al final, "ponderada" por qué tanto se calentó cada olla. Una olla que llegó a ebullición cuenta completa; una que se quedó en 80 °C cuenta menos.

**Baja potencia (agua restante):**

$$A_{rest} = A_{fin,1} + \sum_{j=2}^{4} A_{fin,j}\cdot\frac{T_{fin,j} - 25}{T_{eb} - 25} \quad [\text{kg}] \qquad (14)$$

**En palabras:** la olla 1 cuenta completa porque es la que se mantiene a fuego lento. Las ollas 2 a 4 se ponderan por qué tan calientes terminaron respecto a 25 °C.

En `resultado_fase.masa_agua_efectiva_kg` se guarda $A_{ef}$ en inicio frío y caliente, y $A_{rest}$ en baja potencia.

## 6. Energía y eficiencia térmica

### 6.1 Inicio frío e inicio caliente

$$Q_{sens} = c_{agua}\sum_j A_{ini,j}\,\left(T_{fin,j} - T_{ini,j}\right) \quad [\text{kJ}] \qquad (15)$$

$$Q_{lat} = h_{vap}\cdot A_{evap} \quad [\text{kJ}] \qquad (16)$$

$$Q_{util} = Q_{sens} + Q_{lat} \quad [\text{kJ}] \qquad (17)$$

$$\eta = 100\cdot\frac{Q_{util}}{Q_{comb}} \quad [\%] \qquad (18)$$

### 6.2 Baja potencia

$$A_{prom} = \frac{A_{ini,1} + A_{rest}}{2} \quad [\text{kg}] \qquad (19)$$

$$Q_{sens,baja} = c_{agua}\cdot A_{prom}\,\left(T_{fin,1} - T_{ini,1}\right) \quad [\text{kJ}] \qquad (20)$$

$$\eta_{baja} = 100\cdot\frac{Q_{sens,baja} + h_{vap}\cdot A_{evap}}{Q_{comb}} \quad [\%] \qquad (21)$$

**En palabras:**

- $Q_{sens}$ es la energía que se usó para **calentar** el agua: masa × 4.186 × subida de temperatura.
- $Q_{lat}$ es la energía que se usó para **evaporar** agua.
- $Q_{util}$ es la energía que realmente llegó al agua: calor sensible más latente.
- $\eta$ es qué porcentaje de la energía de la leña llegó al agua.
- En baja potencia solo se usa la temperatura de la olla 1 y un promedio entre el agua inicial y la restante.

## 7. Consumo específico y energía específica

**Consumo específico** (g de leña seca por litro de agua):

$$SC = \frac{1000\cdot F_d}{A_{ef}} \quad [\text{g/L}] \quad \text{(inicio frío y caliente)} \qquad (22a)$$

$$SC_{baja} = \frac{1000\cdot F_d}{A_{rest}} \quad [\text{g/L}] \quad \text{(baja potencia)} \qquad (22b)$$

**Consumo específico corregido por temperatura** (solo inicio frío y caliente):

$$SC_{corr} = SC\cdot\frac{75}{T_{eb} - T_{ini,1}} \quad [\text{g/L}] \qquad (23)$$

**Energía específica** (kJ de energía de la leña por litro de agua):

$$SE_{corr} = \frac{SC_{corr}}{1000}\cdot PCN \quad [\text{kJ/L}] \quad \text{(inicio frío y caliente)} \qquad (24a)$$

$$SE_{baja} = \frac{SC_{baja}}{1000}\cdot PCN \quad [\text{kJ/L}] \quad \text{(baja potencia)} \qquad (24b)$$

**En palabras:**

- $SC$ responde "¿cuánta leña gasté por cada litro de agua que calenté?". Menos es mejor.
- $SC_{corr}$ lo ajusta a la misma subida de 75 °C para poder comparar pruebas.
- $SE$ es lo mismo pero en energía, no en gramos; así se pueden comparar combustibles distintos.
- El consumo se calcula por separado para cada fase; no se mezclan.

## 8. Velocidad de combustión y potencia de fuego

$$r = \frac{1000\cdot F_d}{\Delta t} \quad [\text{g/min}] \qquad (25)$$

$$FP = \frac{Q_{comb}}{60\cdot\Delta t} \quad [\text{kW}] \qquad (26)$$

**En palabras:** $r$ es cuántos gramos de leña seca equivalente se queman por minuto. $FP$ (potencia de fuego) es la energía de la leña liberada por segundo: qué tan "fuerte" es el fuego. Ambas usan $F_d$, no la leña húmeda.

## 9. Correspondencia con `resultado_fase`

| Ecuación | Columna | Notas |
|---|---|---|
| (6) | `tiempo_fase_min` | |
| (7) | `tiempo_ebullicion_corregido_min` | solo frío y caliente |
| (3) suma | `masa_agua_inicial_kg` | $A_{ini}$ |
| (4) suma | `masa_agua_final_kg` | $A_{fin}$ |
| (5) | `masa_agua_evaporada_kg` | |
| (13) / (14) | `masa_agua_efectiva_kg` | $A_{ef}$ en alta; $A_{rest}$ en baja |
| (8) | `combustible_consumido_kg` | húmedo |
| (9a/b/c) | `cambio_carbon_kg` | $\Delta C$ |
| (11) | `combustible_seco_equivalente_kg` | $F_d$ |
| (17) | `energia_util_kj` | en baja: $Q_{sens,baja} + Q_{lat}$ |
| (12) | `energia_combustible_kj` | |
| (18) / (21) | `eficiencia_termica_pct` | |
| (22a) / (22b) | `consumo_especifico_g_l` | |
| (23) | `consumo_especifico_corregido_g_l` | solo frío y caliente |
| (24a) / (24b) | `energia_especifica_corregida_kj_l` | en baja es $SE_{baja}$, sin corrección de 75 °C |
| (25) | `velocidad_combustion_g_min` | |
| (26) | `potencia_fase_kw` | |

## 10. Qué cambió respecto a la versión anterior

| Tema | Antes | Ahora |
|---|---|---|
| Combustible seco | $F_{cons}(1-H)$ | $F_d$ con descuento de agua de la leña y carbón (11) |
| Calor sensible, alta potencia | Promedio de masa inicial y final | Masa **inicial** de cada olla (15) |
| Calor sensible, baja potencia | – | Promedio con $A_{rest}$, solo olla 1 (19, 20) |
| Agua efectiva, alta potencia | Masa inicial × factor | Masa **final** × factor, por olla (13) |
| Agua efectiva, baja potencia | Agua final | $A_{rest}$ ponderada (14) |
| Consumo específico | Un solo valor | Sin corregir (22) y corregido con 75 °C (23) |
| Velocidad de combustión | Combustible húmedo | $F_d$ (25) |
| Campos nuevos | – | `cambio_carbon_kg`, `tiempo_ebullicion_corregido_min`, `consumo_especifico_g_l` |

## 11. Pendientes

- El PDF del protocolo no incluye los apéndices 4 y 6. Estas fórmulas siguen el resumen funcional, que se contrastó con la hoja `WBT_y_seguridad.xlsx`. Antes de darlas por definitivas, cargar una misma prueba real en la hoja y en SICEE y comparar resultados.
- `energia_especifica_corregida_kj_l` guarda en baja potencia un valor que no lleva la corrección de 75 °C. Conviene decidir si se renombra la columna o se separan los dos casos.
- Falta confirmar con el CII cómo se pesa el carbón en cada fase (afecta a (9a), (9b) y (9c)).
- Las métricas IWA, los valores de referencia para 5 L, los tiers y las emisiones van en `resultado_prueba` y `resultado_emisiones_fase`, y no están en este documento.