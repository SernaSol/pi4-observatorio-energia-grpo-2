# Perfilamiento de datos - Observatorio de Energía y Clima

## Objetivo

Evaluar la estructura, completitud y calidad inicial de los datos almacenados en la capa bronce.
**Archivos analizados:** 14

Los datos se analizan sin modificar los archivos originales.

## dane_divipola.parquet

- **Filas:** 1,122
- **Columnas:** 10
- **Filas duplicadas:** 0
- **Rango de fechas:** No aplica (catálogo geográfico)

| Columna | Tipo de dato | Nulos |
|---|---|---:|
| `cod_dpto` | `str` | 0.00% |
| `dpto` | `str` | 0.00% |
| `cod_mpio` | `str` | 0.00% |
| `nom_mpio` | `str` | 0.00% |
| `tipo_municipio` | `str` | 0.00% |
| `longitud` | `str` | 0.00% |
| `latitud` | `str` | 0.00% |
| `_fuente` | `str` | 0.00% |
| `_origen` | `str` | 0.00% |
| `_extraido_en` | `str` | 0.00% |

## enerandes_ventas_2023.parquet

- **Filas:** 1,114
- **Columnas:** 10
- **Filas duplicadas:** 32
- **Rango de fechas:** No determinado: el archivo conserva encabezados y fechas sin normalizar

| Columna | Tipo de dato | Nulos |
|---|---|---:|
| `col_0` | `str` | 0.00% |
| `col_1` | `str` | 0.09% |
| `col_2` | `str` | 1.44% |
| `col_3` | `str` | 0.09% |
| `col_4` | `str` | 0.90% |
| `col_5` | `str` | 0.72% |
| `col_6` | `str` | 0.09% |
| `_fuente` | `str` | 0.00% |
| `_origen` | `str` | 0.00% |
| `_extraido_en` | `str` | 0.00% |

## enerandes_ventas_2024.parquet

- **Filas:** 1,114
- **Columnas:** 11
- **Filas duplicadas:** 32
- **Rango de fechas:** No determinado: el archivo conserva encabezados y fechas sin normalizar

| Columna | Tipo de dato | Nulos |
|---|---|---:|
| `col_0` | `str` | 0.00% |
| `col_1` | `str` | 0.09% |
| `col_2` | `str` | 0.36% |
| `col_3` | `str` | 0.09% |
| `col_4` | `str` | 0.72% |
| `col_5` | `str` | 0.09% |
| `col_6` | `str` | 1.08% |
| `col_7` | `str` | 0.09% |
| `_fuente` | `str` | 0.00% |
| `_origen` | `str` | 0.00% |
| `_extraido_en` | `str` | 0.00% |

## enerandes_ventas_2025.parquet

- **Filas:** 1,117
- **Columnas:** 10
- **Filas duplicadas:** 32
- **Rango de fechas:** No determinado: el archivo conserva encabezados y fechas sin normalizar

| Columna | Tipo de dato | Nulos |
|---|---|---:|
| `col_0` | `str` | 0.09% |
| `col_1` | `str` | 0.36% |
| `col_2` | `str` | 0.90% |
| `col_3` | `str` | 0.36% |
| `col_4` | `str` | 0.90% |
| `col_5` | `str` | 0.72% |
| `col_6` | `str` | 0.36% |
| `_fuente` | `str` | 0.00% |
| `_origen` | `str` | 0.00% |
| `_extraido_en` | `str` | 0.00% |

## enerandes_ventas_2026.parquet

- **Filas:** 839
- **Columnas:** 10
- **Filas duplicadas:** 24
- **Rango de fechas:** No determinado: el archivo conserva encabezados y fechas sin normalizar

| Columna | Tipo de dato | Nulos |
|---|---|---:|
| `col_0` | `str` | 0.12% |
| `col_1` | `str` | 0.48% |
| `col_2` | `str` | 1.07% |
| `col_3` | `str` | 0.48% |
| `col_4` | `str` | 1.07% |
| `col_5` | `str` | 1.31% |
| `col_6` | `str` | 0.48% |
| `_fuente` | `str` | 0.00% |
| `_origen` | `str` | 0.00% |
| `_extraido_en` | `str` | 0.00% |

## ideam_precipitacion_diaria.parquet

- **Filas:** 29,804
- **Columnas:** 12
- **Filas duplicadas:** 0
- **Rango de fechas:** 2025-01-01 a 2026-07-24

| Columna | Tipo de dato | Nulos |
|---|---|---:|
| `codigoestacion` | `str` | 0.00% |
| `nombreestacion` | `str` | 0.00% |
| `municipio` | `str` | 0.00% |
| `zonahidrografica` | `str` | 0.00% |
| `latitud` | `str` | 0.00% |
| `longitud` | `str` | 0.00% |
| `fecha` | `str` | 0.00% |
| `precipitacion_mm` | `str` | 0.00% |
| `n_obs` | `str` | 0.00% |
| `_fuente` | `str` | 0.00% |
| `_origen` | `str` | 0.00% |
| `_extraido_en` | `str` | 0.00% |

## ideam_temperatura_diaria.parquet

- **Filas:** 17,349
- **Columnas:** 14
- **Filas duplicadas:** 0
- **Rango de fechas:** 2025-01-01 a 2026-07-24

| Columna | Tipo de dato | Nulos |
|---|---|---:|
| `codigoestacion` | `str` | 0.00% |
| `nombreestacion` | `str` | 0.00% |
| `municipio` | `str` | 0.00% |
| `zonahidrografica` | `str` | 0.00% |
| `latitud` | `str` | 0.00% |
| `longitud` | `str` | 0.00% |
| `fecha` | `str` | 0.00% |
| `temp_media_c` | `str` | 0.00% |
| `temp_min_c` | `str` | 0.00% |
| `temp_max_c` | `str` | 0.00% |
| `n_obs` | `str` | 0.00% |
| `_fuente` | `str` | 0.00% |
| `_origen` | `str` | 0.00% |
| `_extraido_en` | `str` | 0.00% |

## noaa_oni.parquet

- **Filas:** 920
- **Columnas:** 7
- **Filas duplicadas:** 0
- **Rango de fechas:** No determinado: ONI registra el año en `YR` y la temporada en `SEAS`

| Columna | Tipo de dato | Nulos |
|---|---|---:|
| `SEAS` | `str` | 0.00% |
| `YR` | `str` | 0.00% |
| `TOTAL` | `str` | 0.00% |
| `ANOM` | `str` | 0.00% |
| `_fuente` | `str` | 0.00% |
| `_origen` | `str` | 0.00% |
| `_extraido_en` | `str` | 0.00% |

## xm_aportes_hidricos.parquet

- **Filas:** 1,004
- **Columnas:** 6
- **Filas duplicadas:** 0
- **Rango de fechas:** 2024-01-01 a 2026-09-30

| Columna | Tipo de dato | Nulos |
|---|---|---:|
| `Date` | `str` | 0.00% |
| `Id` | `str` | 0.00% |
| `Value` | `str` | 0.00% |
| `_fuente` | `str` | 0.00% |
| `_origen` | `str` | 0.00% |
| `_extraido_en` | `str` | 0.00% |

## xm_demanda.parquet

- **Filas:** 1,004
- **Columnas:** 30
- **Filas duplicadas:** 0
- **Rango de fechas:** 2024-01-01 a 2026-09-30

| Columna | Tipo de dato | Nulos |
|---|---|---:|
| `Date` | `str` | 0.00% |
| `Id` | `str` | 0.00% |
| `code` | `str` | 0.00% |
| `Hour01` | `str` | 0.00% |
| `Hour02` | `str` | 0.00% |
| `Hour03` | `str` | 0.00% |
| `Hour04` | `str` | 0.00% |
| `Hour05` | `str` | 0.00% |
| `Hour06` | `str` | 0.00% |
| `Hour07` | `str` | 0.00% |
| `Hour08` | `str` | 0.00% |
| `Hour09` | `str` | 0.00% |
| `Hour10` | `str` | 0.00% |
| `Hour11` | `str` | 0.00% |
| `Hour12` | `str` | 0.00% |
| `Hour13` | `str` | 0.00% |
| `Hour14` | `str` | 0.00% |
| `Hour15` | `str` | 0.00% |
| `Hour16` | `str` | 0.00% |
| `Hour17` | `str` | 0.00% |
| `Hour18` | `str` | 0.00% |
| `Hour19` | `str` | 0.00% |
| `Hour20` | `str` | 0.00% |
| `Hour21` | `str` | 0.00% |
| `Hour22` | `str` | 0.00% |
| `Hour23` | `str` | 0.00% |
| `Hour24` | `str` | 0.00% |
| `_fuente` | `str` | 0.00% |
| `_origen` | `str` | 0.00% |
| `_extraido_en` | `str` | 0.00% |

## xm_embalses.parquet

- **Filas:** 1,004
- **Columnas:** 6
- **Filas duplicadas:** 0
- **Rango de fechas:** 2024-01-01 a 2026-09-30

| Columna | Tipo de dato | Nulos |
|---|---|---:|
| `Date` | `str` | 0.00% |
| `Id` | `str` | 0.00% |
| `Value` | `str` | 0.00% |
| `_fuente` | `str` | 0.00% |
| `_origen` | `str` | 0.00% |
| `_extraido_en` | `str` | 0.00% |

## xm_generacion_recurso.parquet

- **Filas:** 350,361
- **Columnas:** 30
- **Filas duplicadas:** 0
- **Rango de fechas:** 2024-01-01 a 2026-09-30

| Columna | Tipo de dato | Nulos |
|---|---|---:|
| `Date` | `str` | 0.00% |
| `Id` | `str` | 0.00% |
| `code` | `str` | 0.00% |
| `Hour01` | `str` | 0.00% |
| `Hour02` | `str` | 0.00% |
| `Hour03` | `str` | 0.00% |
| `Hour04` | `str` | 0.00% |
| `Hour05` | `str` | 0.00% |
| `Hour06` | `str` | 0.00% |
| `Hour07` | `str` | 0.00% |
| `Hour08` | `str` | 0.00% |
| `Hour09` | `str` | 0.00% |
| `Hour10` | `str` | 0.00% |
| `Hour11` | `str` | 0.00% |
| `Hour12` | `str` | 0.00% |
| `Hour13` | `str` | 0.00% |
| `Hour14` | `str` | 0.00% |
| `Hour15` | `str` | 0.00% |
| `Hour16` | `str` | 0.00% |
| `Hour17` | `str` | 0.00% |
| `Hour18` | `str` | 0.00% |
| `Hour19` | `str` | 0.00% |
| `Hour20` | `str` | 0.00% |
| `Hour21` | `str` | 0.00% |
| `Hour22` | `str` | 0.00% |
| `Hour23` | `str` | 0.00% |
| `Hour24` | `str` | 0.00% |
| `_fuente` | `str` | 0.00% |
| `_origen` | `str` | 0.00% |
| `_extraido_en` | `str` | 0.00% |

## xm_listado_recursos.parquet

- **Filas:** 2,493
- **Columnas:** 14
- **Filas duplicadas:** 2
- **Rango de fechas:** No aplica (catálogo de recursos; la fecha registrada no es un rango histórico)

| Columna | Tipo de dato | Nulos |
|---|---|---:|
| `Date` | `str` | 0.00% |
| `Id` | `str` | 0.00% |
| `Code` | `str` | 0.00% |
| `Name` | `str` | 0.00% |
| `Type` | `str` | 0.00% |
| `Disp` | `str` | 0.00% |
| `RecType` | `str` | 0.00% |
| `CompanyCode` | `str` | 0.00% |
| `EnerSource` | `str` | 0.00% |
| `OperStartdate` | `str` | 0.00% |
| `State` | `str` | 0.00% |
| `_fuente` | `str` | 0.00% |
| `_origen` | `str` | 0.00% |
| `_extraido_en` | `str` | 0.00% |

## xm_precio_bolsa.parquet

- **Filas:** 1,004
- **Columnas:** 30
- **Filas duplicadas:** 0
- **Rango de fechas:** 2024-01-01 a 2026-09-30

| Columna | Tipo de dato | Nulos |
|---|---|---:|
| `Date` | `str` | 0.00% |
| `Id` | `str` | 0.00% |
| `code` | `str` | 0.00% |
| `Hour01` | `str` | 0.00% |
| `Hour02` | `str` | 0.00% |
| `Hour03` | `str` | 0.00% |
| `Hour04` | `str` | 0.00% |
| `Hour05` | `str` | 0.00% |
| `Hour06` | `str` | 0.00% |
| `Hour07` | `str` | 0.00% |
| `Hour08` | `str` | 0.00% |
| `Hour09` | `str` | 0.00% |
| `Hour10` | `str` | 0.00% |
| `Hour11` | `str` | 0.00% |
| `Hour12` | `str` | 0.00% |
| `Hour13` | `str` | 0.00% |
| `Hour14` | `str` | 0.00% |
| `Hour15` | `str` | 0.00% |
| `Hour16` | `str` | 0.00% |
| `Hour17` | `str` | 0.00% |
| `Hour18` | `str` | 0.00% |
| `Hour19` | `str` | 0.00% |
| `Hour20` | `str` | 0.00% |
| `Hour21` | `str` | 0.00% |
| `Hour22` | `str` | 0.00% |
| `Hour23` | `str` | 0.00% |
| `Hour24` | `str` | 0.00% |
| `_fuente` | `str` | 0.00% |
| `_origen` | `str` | 0.00% |
| `_extraido_en` | `str` | 0.00% |

## Hallazgos de calidad de los datos

Los hallazgos siguientes se basan en el perfilamiento de los 14 archivos Parquet de la capa bronce. Son alertas para revisión: la presencia de duplicados, valores nulos o diferencias estructurales no implica automáticamente que el origen tenga datos erróneos.

### Hallazgo 1. Filas duplicadas en las ventas de EnerAndes

Se identificaron **120 filas duplicadas exactas** en los cuatro archivos de ventas: **32** en 2023, **32** en 2024, **32** en 2025 y **24** en 2026. Es necesario establecer si estas repeticiones corresponden a transacciones, encabezados, totales u otras filas conservadas del Excel original.

**Recomendación:** identificar las filas de datos reales y establecer una clave de negocio antes de decidir si procede eliminar duplicados en la capa plata.

### Hallazgo 2. Valores nulos en EnerAndes

En el archivo de 2023, **`col_2` presenta 1,44 % de nulos**; en el de 2026, **`col_5` presenta 1,31 %**. En ambos casos se trata de las tasas máximas de nulidad entre las columnas de cada archivo, según el perfilamiento.

**Recomendación:** interpretar los encabezados originales y distinguir las celdas vacías propias del formato de las ausencias de información que puedan afectar los indicadores de ventas.

### Hallazgo 3. Estructuras distintas entre las hojas de EnerAndes

Los archivos de **2023, 2025 y 2026 tienen 10 columnas** cada uno, mientras que **2024 tiene 11** (incluidas las tres columnas de linaje). Por tanto, las hojas no son estructuralmente idénticas y no deben combinarse directamente por posición de columna.

**Recomendación:** identificar los encabezados reales por hoja y homologar los campos en la capa plata sin alterar los archivos originales de bronce.

### Hallazgo 4. Menor cobertura observada de IDEAM frente al rango consultado

Se solicitaron registros desde **2025-01-01 hasta 2026-09-30**, pero la última fecha presente en ambos archivos IDEAM es **2026-07-24**. Se obtuvieron **29.804 filas** de precipitación y **17.349 filas** de temperatura. Esto representa una brecha de **68 días naturales** entre la última fecha registrada y el final solicitado. La observación se limita a los resultados obtenidos con los filtros utilizados; no demuestra ausencia de datos en todo IDEAM.

**Recomendación:** registrar esta diferencia de cobertura y verificar periódicamente si la API ofrece información adicional para los mismos filtros.

### Hallazgo 5. Duplicados exactos en el catálogo de recursos de XM

`xm_listado_recursos.parquet` contiene **2.493 registros**, con **2 filas duplicadas exactas** (aproximadamente **0,08 %**). Antes de relacionar este catálogo con la generación por planta, se debe revisar si los duplicados afectan la unicidad de los identificadores de recursos.

**Recomendación:** inspeccionar los valores `Id` y `Code`, y definir la clave de relación apropiada en la capa plata.

## Consideraciones sobre los tipos de datos y las fechas

Las columnas originales se conservaron mayoritariamente como texto (`str`) en la capa bronce, incluso cuando representan cantidades o fechas. Esto es consistente con conservar los datos de origen, pero los análisis numéricos y temporales requerirán conversiones validadas en la capa plata.

El catálogo DIVIPOLA y `ListadoRecursos` no tienen un rango histórico aplicable. En NOAA, el período está representado por `YR` y `SEAS`, y en EnerAndes aún es necesario interpretar las columnas originales para determinar rangos de fechas confiables.

## Conclusión del perfilamiento

El análisis de los **14 archivos** permitió documentar filas, columnas, tipos de datos, porcentajes de nulos, duplicados y cobertura temporal cuando era identificable. Las principales alertas se relacionan con duplicados y diferencias estructurales en EnerAndes, registros duplicados en el catálogo XM y una brecha de cobertura de las consultas IDEAM.

Se mantendrán los archivos originales de la capa bronce sin modificaciones. La estandarización de esquemas, la interpretación de fechas y la validación de posibles errores se realizarán en las siguientes etapas del pipeline.
