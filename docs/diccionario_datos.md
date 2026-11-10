# Diccionario de datos — Capa oro EA2

## 1. Descripción general

El Observatorio de Energía y Clima utiliza un modelo dimensional implementado con **dbt y DuckDB**.

La capa oro está compuesta por **3 tablas de hechos y 5 dimensiones**, que permiten analizar ventas de energía, precios de bolsa, demanda eléctrica y generación por recurso.

## 2. Dimensiones

### 2.1. dim_mes

**Grano:** una fila por mes con ventas.

| Columna | Tipo | Descripción |
|---|---|---|
| mes_id | INTEGER | Identificador único del mes, formato AAAAMM. |
| periodo | VARCHAR | Período comercial, formato AAAA-MM. |
| anio | INTEGER | Año del período. |
| mes | INTEGER | Número de mes, entre 1 y 12. |
| trimestre | INTEGER | Trimestre del año, entre 1 y 4. |

### 2.2. dim_municipio

**Grano:** una fila por municipio presente en las ventas de EnerAndes.

| Columna | Tipo | Descripción |
|---|---|---|
| municipio_id | VARCHAR | Código DIVIPOLA de cinco dígitos. Llave primaria. |
| municipio | VARCHAR | Nombre normalizado del municipio. |

### 2.3. dim_segmento

**Grano:** una fila por segmento comercial.

| Columna | Tipo | Descripción |
|---|---|---|
| segmento_id | BIGINT | Identificador único del segmento. |
| segmento | VARCHAR | Nombre del segmento: Residencial, Comercial, Industrial o No informado. |

### 2.4. dim_fecha

**Grano:** una fila por día calendario.

| Columna | Tipo | Descripción |
|---|---|---|
| fecha_id | INTEGER | Identificador de fecha, formato AAAAMMDD. |
| fecha | DATE | Fecha calendario. |
| anio | INTEGER | Año. |
| mes | INTEGER | Mes, entre 1 y 12. |
| dia | INTEGER | Día del mes. |
| trimestre | INTEGER | Trimestre del año. |
| dia_semana | INTEGER | Día de la semana ISO: lunes = 1, domingo = 7. |
| fase_enso | VARCHAR | Fase climática de NOAA: El Niño, La Niña, Neutral o Sin dato. |

### 2.5. dim_recurso

**Grano:** una fila por código de recurso eléctrico de XM.

| Columna | Tipo | Descripción |
|---|---|---|
| recurso_id | VARCHAR | Código único del recurso. Llave primaria. |
| nombre_recurso | VARCHAR | Nombre del recurso o identificador provisional si falta en el catálogo. |
| tipo | VARCHAR | Clasificación general del catálogo XM. |
| tipo_recurso | VARCHAR | Tipo de recurso registrado por XM. |
| fuente_energetica | VARCHAR | Fuente energética asociada al recurso. |
| codigo_empresa | VARCHAR | Código de la empresa responsable. |
| estado | VARCHAR | Estado operativo registrado en el catálogo. |
| despacho | VARCHAR | Información de despacho del recurso. |
| fecha_inicio_operacion | TIMESTAMP | Fecha de inicio de operación, cuando está disponible. |
| en_catalogo | BOOLEAN | `true` si aparece en el catálogo XM; `false` si solo aparece en la generación histórica. |

**Observación:** se incorporaron diez códigos históricos que no estaban en el catálogo. Sus atributos desconocidos se conservan como `NULL`, sin inventar información.

## 3. Tablas de hechos

### 3.1. fact_ventas_mensual

**Fuente:** EnerAndes, capa plata.

**Grano:** una fila por mes, municipio, segmento y tipo de compra.

**Llave compuesta:** `mes_id`, `municipio_id`, `segmento_id`, `tipo_compra`.

| Columna | Tipo | Descripción |
|---|---|---|
| mes_id | INTEGER | Llave foránea hacia dim_mes. |
| municipio_id | VARCHAR | Llave foránea hacia dim_municipio. |
| segmento_id | BIGINT | Llave foránea hacia dim_segmento. |
| tipo_compra | VARCHAR | Modalidad comercial: Bolsa o Contrato. |
| energia_kwh | DOUBLE | Energía vendida, expresada en kilovatios-hora. |
| valor_cop | DOUBLE | Valor facturado en pesos colombianos. Puede ser nulo. |
| clientes | BIGINT | Número de clientes registrados. |

**Medidas principales:** energía vendida, valor facturado y clientes.

### 3.2. fact_mercado_horario

**Fuente:** XM, mercado horario de la capa plata.

**Grano:** una fila por fecha, hora, entidad y código.

**Llave compuesta:** `fecha_id`, `hora`, `entidad`, `codigo`.

| Columna | Tipo | Descripción |
|---|---|---|
| fecha_id | INTEGER | Llave foránea hacia dim_fecha. |
| hora | INTEGER | Hora XM, entre 1 y 24. |
| entidad | VARCHAR | Identificador de entidad de XM. |
| codigo | VARCHAR | Código de la entidad o indicador. |
| precio_bolsa | DOUBLE | Precio de bolsa reportado por XM. |
| demanda | DOUBLE | Demanda eléctrica reportada por XM. |

**Medidas principales:** precio de bolsa y demanda.

### 3.3. fact_generacion_recurso

**Fuente:** XM, generación por recurso de la capa plata.

**Grano:** una fila por fecha, hora y recurso.

**Llave compuesta:** `fecha_id`, `hora`, `recurso_id`.

| Columna | Tipo | Descripción |
|---|---|---|
| fecha_id | INTEGER | Llave foránea hacia dim_fecha. |
| hora | INTEGER | Hora XM, entre 1 y 24. |
| recurso_id | VARCHAR | Llave foránea hacia dim_recurso. |
| entidad | VARCHAR | Identificador de entidad original de XM. |
| generacion | DOUBLE | Valor de generación eléctrica reportado por XM. |

**Medida principal:** generación por recurso.

## 4. Relaciones e integridad

Las relaciones del modelo dimensional son:

| Tabla de hechos | Dimensión relacionada | Llave |
|---|---|---|
| fact_ventas_mensual | dim_mes | mes_id |
| fact_ventas_mensual | dim_municipio | municipio_id |
| fact_ventas_mensual | dim_segmento | segmento_id |
| fact_mercado_horario | dim_fecha | fecha_id |
| fact_generacion_recurso | dim_fecha | fecha_id |
| fact_generacion_recurso | dim_recurso | recurso_id |

Se aplican pruebas dbt de valores no nulos, unicidad, relaciones entre hechos y dimensiones, valores aceptados y ausencia de duplicados en las llaves compuestas.

## 5. Consideraciones de calidad

- Las ventas comerciales tienen granularidad mensual; el mercado y la generación, granularidad horaria.
- La fase ENSO se asigna a los días a partir del mes central del índice ONI de NOAA.
- Los recursos que no aparecen en el catálogo original se conservan mediante registros identificados con `en_catalogo = false`.
- No se eliminan observaciones válidas de generación por ausencia de información descriptiva del catálogo.
- Las unidades exactas de `precio_bolsa`, `demanda` y `generacion` deben confirmarse con los metadatos de las métricas originales de XM antes de hacer conversiones o comparaciones de magnitudes.

## 6. Herramientas y ejecución

- **DuckDB:** almacenamiento y consultas de la capa oro.
- **dbt-duckdb:** transformación dimensional.
- **Pandera:** validación previa de la capa plata.
- **Pruebas dbt:** integridad de dimensiones y hechos.

Desde la raíz del repositorio:

```powershell
dbt build --project-dir dbt --profiles-dir dbt
```

El modelo dimensional y sus relaciones se presentan en `docs/modelo_dimensional.md`.
