# Reporte de calidad — EA2 · Capa plata

**Proyecto:** Observatorio de Energía y Clima  
**Alcance:** EnerAndes, XM, IDEAM, NOAA y DANE (DIVIPOLA)  
**Elaboración:** 9 de noviembre de 2026  
**Validación:** esquemas Pandera ejecutados antes del guardado; `python -m pytest` con **26 pruebas aprobadas**.

## 1. Resumen de fuentes procesadas

| Fuente / tabla de plata | Entrada evaluada | Registros limpios | Cuarentena | Resultado |
|---|---:|---:|---:|---|
| EnerAndes, ventas mensuales 2023–2026 | 4.170 ventas | 4.007 | 163 | Pandera OK |
| XM, precio de bolsa + demanda | 1.004 días por indicador | 24.096 horas consolidadas | 0 | Pandera OK |
| XM, generación por recurso | 350.361 filas diarias × 24 horas | 5.935.449 horas | 2.473.215 horas | Pandera por lotes OK |
| XM, embalses | 1.004 días | 1.004 | 0 | Pandera OK |
| XM, aportes hídricos | 1.004 días | 1.004 | 0 | Pandera OK |
| XM, catálogo `ListadoRecursos` | 2.493 recursos | 2.491 | 2 | Pandera OK |
| IDEAM, precipitación diaria | 29.804 | 29.804 | 0 | Pandera OK |
| IDEAM, temperatura diaria | 17.349 | 17.349 | 0 | Pandera OK |
| NOAA, ONI mensual | 920 trimestres móviles | 920 meses | 0 | Pandera OK |
| DANE, DIVIPOLA | 1.122 municipios | 1.122 | 0 | Pandera OK |

**Total de filas almacenadas en las 10 tablas limpias:** 6.017.246.  
**Total de filas almacenadas en los archivos de cuarentena:** 2.473.380.

> **Nota de interpretación:** las entradas no son sumables entre fuentes porque su granularidad cambia (por ejemplo, XM pasa de una fila diaria con 24 columnas a 24 filas horarias). En EnerAndes, las 4.170 ventas evaluadas excluyen cuatro filas `TOTAL`; estas se documentan aparte. Las filas de encabezados y notas también se excluyeron al preparar los Excel.

## 2. EnerAndes — ventas mensuales 2023–2026

| # | Problema o indicador (métrica) | Antes | Después en plata | Regla aplicada |
|---:|---|---:|---:|---|
| 1 | Estructuras de encabezados distintas | 4 | 1 | Unificar columnas de 2023, 2024, 2025 y 2026. |
| 2 | Fechas no reconocidas por el analizador inicial | 124 | 0 | Reconocer meses en español e inglés; retirar los resúmenes `TOTAL`. |
| 3 | Filas `TOTAL` que no representan ventas | 4 | 0 | Excluir filas de resumen antes de consolidar. |
| 4 | Nombres distintos de municipios por año (2023/2024/2025/2026) | 31 / 32 / 30 / 29 | 15 / 15 / 15 / 15 | Normalizar tildes, espacios, alias y códigos DIVIPOLA. |
| 5 | Filas duplicadas después de normalizar | 120 | 0 | Conservar primera aparición; registrar copias en cuarentena. |
| 6 | Registros con energía vacía o no numérica | 27 | 0 | Enviar a cuarentena, sin imputación. |
| 7 | Registros con energía negativa | 18 | 0 | Enviar a cuarentena. |
| 8 | Variantes de tipo de compra en la hoja 2026 | 4 | 2 | Unificar `Bolsa`, `bolsa`, `Contrato` y `CONTRATOS`. |
| 9 | Valor facturado nulo | 29 | 28 | Conservar nulos legítimos; una observación quedó en cuarentena por otro problema. |
| 10 | Segmento `No informado` | 29 | 28 | Conservar la categoría explícita; una observación quedó en cuarentena por otro problema. |

La energía de 2024 se convirtió de **MWh a kWh** cuando correspondía (factor × 1.000). Se conserva la unidad original en `unidad_origen`. La validación de la tabla consolidada abarca 14 columnas.

**Desglose por año:**

| Año | Ventas evaluadas | Limpias | Cuarentena | Filas `TOTAL` excluidas |
|---|---:|---:|---:|---:|
| 2023 | 1.112 | 1.064 | 48 | 1 |
| 2024 | 1.112 | 1.071 | 41 | 1 |
| 2025 | 1.112 | 1.071 | 41 | 1 |
| 2026 | 834 | 801 | 33 | 1 |
| **Total** | **4.170** | **4.007** | **163** | **4** |

## 3. XM — precio de bolsa y demanda

**Periodo cubierto:** 2024-01-01 al 2026-09-30. Cada indicador contiene 1.004 fechas originales.

| # | Problema o indicador (métrica) | Antes | Después en plata | Regla aplicada |
|---:|---|---:|---:|---|
| 11 | Columnas horarias por fuente (`Hour01`–`Hour24`) | 24 | 0 | Transformar de formato ancho a largo. |
| 12 | Filas de precio de bolsa | 1.004 diarias | 24.096 horarias | Crear una fila por fecha y hora. |
| 13 | Filas de demanda | 1.004 diarias | 24.096 horarias | Crear una fila por fecha y hora. |
| 14 | Valores de precio vacíos/no numéricos | 0 | 0 | Convertir a número y verificar que no haya nulos. |
| 15 | Valores de demanda vacíos/no numéricos | 0 | 0 | Convertir a número y verificar que no haya nulos. |
| 16 | Claves fecha–hora–entidad–código duplicadas | 0 | 0 | Unión uno a uno y validación de unicidad con Pandera. |

**Salida:** `xm_mercado_horario.parquet`, con 24.096 registros y las columnas `fecha`, `hora`, `entidad`, `codigo`, `precio_bolsa` y `demanda`. Las horas se conservan como **1–24**, según XM. No hubo cuarentena en estas fuentes.

## 4. XM — generación horaria por recurso

Se transformaron **350.361 filas diarias** en **8.408.664 posiciones horarias**. La conversión, validación y escritura se ejecutaron por lotes para limitar el consumo de memoria.

| # | Problema o indicador (métrica) | Antes | Después en plata | Regla aplicada |
|---:|---|---:|---:|---|
| 17 | Columnas horarias por recurso | 24 | 0 | Transformar `Hour01`–`Hour24` a filas. |
| 18 | Horas con generación vacía/no numérica | 2.473.215 | 0 | Enviar esas horas —no las 24 horas del recurso— a cuarentena. |
| 19 | Valores de generación negativos | 0 | 0 | Rechazar valores negativos según Pandera. |
| 20 | Claves fecha–recurso repetidas en bronce | 0 | 0 | Comprobar duplicados incluso entre lotes. |

**Resultado:** 5.935.449 horas limpias y 2.473.215 horas en cuarentena. Los faltantes **no se reemplazan por cero**; los ceros válidos sí se conservarían. La cuarentena registra `fecha`, `hora`, `codigo`, `valor_original` y `motivo_cuarentena`.

## 5. XM — embalses, aportes hídricos y catálogo de plantas

| # | Fuente y problema (métrica) | Antes | Después en plata | Regla aplicada |
|---:|---|---:|---:|---|
| 21 | Embalses: valores fuera del intervalo 0–1 | 0 | 0 | Convertir `Value` a número y validar proporción entre 0 y 1. |
| 22 | Embalses: fechas/entidades duplicadas | 0 | 0 | Validar clave diaria única. |
| 23 | Aportes hídricos: valores negativos | 0 | 0 | Convertir `Value` a número y validar no negatividad. |
| 24 | Catálogo: códigos de recurso duplicados | 2 | 0 | Conservar primera aparición y enviar 2 copias a cuarentena. |
| 25 | Catálogo: estado escrito `Operacion` | 198 | 0 | Normalizar estados a `OPERACION` o `PRUEBAS`. |

**Embalses:** 1.004 valores válidos; rango observado **0,28564–0,85961**.  
**Aportes hídricos:** 1.004 valores válidos; rango observado **55.795.000–643.075.500** (se conserva la escala de origen, sin asignarle una unidad no verificada).  
**Catálogo:** 2.491 registros limpios; 2.285 en `OPERACION` y 206 en `PRUEBAS`. Los códigos duplicados encontrados fueron `5J8H` y `5PUN`.

## 6. IDEAM — precipitación y temperatura diaria

Los códigos de estación se conservaron como texto para mantener ceros iniciales. Se normalizaron fechas, mediciones, coordenadas y municipios. La relación geográfica se efectuó mediante el catálogo DANE de Antioquia (`cod_dpto = 05`).

| # | Problema o indicador (métrica) | Antes | Después en plata | Regla aplicada |
|---:|---|---:|---:|---|
| 26 | Precipitación: registros `SAN VICENTE` sin coincidencia exacta en DIVIPOLA | 522 | 0 | Asociar el alias con `SAN VICENTE FERRER` (`05674`). |
| 27 | Temperatura: registros `SAN VICENTE` sin coincidencia exacta en DIVIPOLA | 514 | 0 | Aplicar la misma equivalencia y conservar `municipio_origen`. |
| 28 | Precipitación: valores negativos/no numéricos retenidos | 0 | 0 | Validar mediciones y separar inválidos antes del guardado. |
| 29 | Temperatura: registros con orden mínimo ≤ medio ≤ máximo incumplido | 0 | 0 | Validar consistencia física con Pandera. |

**Precipitación:** 29.804 registros limpios, 72 estaciones y cuarentena 0.  
**Temperatura:** 17.349 registros limpios, 44 estaciones y cuarentena 0.  
**Cobertura DIVIPOLA:** cero registros de plata sin código municipal después de la asociación.

## 7. NOAA — ONI y fases ENSO

| # | Problema o indicador (métrica) | Antes | Después en plata | Regla aplicada |
|---:|---|---:|---:|---|
| 30 | Observaciones con mes central asignado | 0 en la tabla original | 920 | Convertir los trimestres móviles a su mes central: `DJF` → enero, `JFM` → febrero, etc. |
| 31 | Observaciones con fase ENSO clasificada | 0 en la tabla original | 920 | `El Niño` si ONI ≥ 0,5; `La Niña` si ONI ≤ −0,5; `Neutral` en otro caso. |

**Resultado:** 920 registros limpios y cuarentena 0. Distribución: **448 Neutral**, **238 La Niña**, **234 El Niño**. Se validó una única observación por mes.

## 8. DANE — DIVIPOLA

| # | Problema o indicador (métrica) | Antes | Después en plata | Regla aplicada |
|---:|---|---:|---:|---|
| 32 | Coordenadas almacenadas como cadenas de texto | 1.122 filas | 0 filas | Convertir coma decimal a punto y almacenar latitud/longitud numéricas. |
| 33 | Registros con código de municipio duplicado | 0 | 0 | Preservar `cod_mpio` como texto de cinco dígitos y validar unicidad. |

**Resultado:** 1.122 municipios válidos y cuarentena 0. El archivo limpio es la referencia geográfica para IDEAM y las dimensiones territoriales.

## 9. Cuarentenas: cantidades y motivos

| Fuente | Motivo registrado | Filas |
|---|---|---:|
| EnerAndes | Registro duplicado | 118 |
| EnerAndes | Energía vacía o no numérica | 25 |
| EnerAndes | Energía negativa | 18 |
| EnerAndes | Registro duplicado **y** energía vacía/no numérica | 2 |
| XM generación | Generación vacía o no numérica | 2.473.215 |
| XM catálogo | Código duplicado | 2 |
| XM mercado, embalses, aportes, IDEAM, NOAA, DIVIPOLA | Sin registros en cuarentena | 0 |
| **Total** | | **2.473.380** |

Los motivos se presentan por **combinación registrada en cada fila**, de modo que una observación con dos causas no se cuenta dos veces. En EnerAndes existen 120 duplicados (118 aislados y 2 combinados con ausencia de energía), 27 energías vacías y 18 negativas.

## 10. Controles de ejecución y trazabilidad

- Los Parquet de bronce permanecen sin modificaciones; la capa plata se guarda en `data/silver/`.
- Las tablas limpias se validaron con Pandera **antes** de guardarse; las que contienen inválidos tienen archivos de cuarentena asociados.
- Para XM generación se utilizó validación y escritura por lotes, sin cargar las 8.408.664 posiciones horarias simultáneamente en memoria.
- La ejecución de `python -m pytest` reportó **26 pruebas aprobadas**, incluidas **7 pruebas adicionales de EA2** con datos pequeños.
- Este documento reúne **33 controles/reglas** y sus resultados antes y después, superando el mínimo de 15.
- Los conteos aquí consignados provienen de las ejecuciones y las salidas de calidad verificadas durante la actividad; si se regeneran los datos o cambia el periodo de extracción, las cifras deberán actualizarse.
