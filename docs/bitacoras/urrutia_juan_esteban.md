# Bitácora – Esteban Urrutia

**Proyecto:** Observatorio de Energía y Clima – Equipo 2  
**Asignatura:** Proyecto Integrado IV
**Institución:** IU Digital de Antioquia  
**Periodo:** 2026-2
**Rol** Data Quality Analyst - BI Analyst / Storyteller

## 1. Objetivo de mi participación

Mi participación se enfocó en los puntos 5, 6 y 7 de la actividad, relacionados con la incorporación de una fuente de información adicional, la generación de muestras de datos y el perfilamiento de calidad de la capa bronce.

Estas actividades permitieron complementar las fuentes existentes y facilitar la revisión de la información obtenida mediante el pipeline.

## 2. Actividades desarrolladas

### Punto 5. Incorporación de una fuente adicional

Se incorporó DIVIPOLA del DANE como quinta fuente de información del proyecto.

Esta fuente proporciona datos geográficos oficiales sobre municipios y departamentos de Colombia, incluyendo códigos y coordenadas.

Las actividades asociadas fueron:

- Configuración de la fuente en `src/config.py`.
- Creación del extractor `src/extract/divipola.py`.
- Integración del extractor en `src/pipeline.py`.
- Validación de la respuesta obtenida mediante la API.
- Almacenamiento de los registros en formato Parquet.

**Resultado:** se obtuvieron 1.122 registros distribuidos en 10 columnas, guardados en `data/bronze/dane_divipola.parquet`.

**PR:** Merge pull request #3 from SernaSol/feature/fuente-divipola
**Commit:** https://github.com/SernaSol/pi4-observatorio-energia-grpo-2/commit/aae523bc745e968fe3cb57a98a0f74b8e0a9a6c9


La fuente permitirá complementar los análisis geográficos relacionados con las estaciones meteorológicas del IDEAM.

### Punto 6. Reproducibilidad y generación de muestras

Se incorporó el script `src/generar_muestras.py` para automatizar la generación de muestras representativas de los archivos de la capa bronce.

Se generaron archivos CSV con las primeras 200 filas de cada Parquet, sin modificar los archivos originales.

**Resultado:** se generaron y verificaron 14 archivos CSV, cada uno con 200 registros.

Además, se revisó el archivo `.gitignore` para mantener excluidos los datos completos de `data/bronze/`.

Se comprobó que el pipeline reconociera los 14 archivos Parquet existentes y finalizara sin errores.

La validación completa desde un repositorio recién clonado queda diferenciada de esta comprobación.

**PR:** Merge pull request #4 from SernaSol/feature/muestras-csv
**Commit:** https://github.com/SernaSol/pi4-observatorio-energia-grpo-2/commit/977f4471640fca654760660e20366d0a3815ab57



### Punto 7. Perfilamiento de calidad de los datos

Se elaboró el perfilamiento inicial de los archivos de la capa bronce mediante Python y pandas.

Se analizaron:

- Cantidad de filas y columnas.
- Tipos de datos.
- Porcentajes de valores nulos.
- Registros duplicados.
- Rangos de fechas disponibles.

**Resultado:** se documentaron 14 archivos Parquet y cinco hallazgos de calidad con evidencia numérica.

Entre los hallazgos identificados se encuentran los 120 registros duplicados exactos contabilizados en los archivos de EnerAndes, las diferencias de estructura entre años y las limitaciones de cobertura temporal en los datos del IDEAM.


**PR:** Merge pull request #5 from SernaSol/feature/perfilamiento-datos
**Commit:** https://github.com/SernaSol/pi4-observatorio-energia-grpo-2/commit/fc9ce945fa7bf3b3dd1df2642876b469965f820c

El resultado se documentó en `docs/perfilamiento.md`.

## 3. Dificultades y soluciones

Uno de los principales retos fue integrar una fuente adicional sin modificar el funcionamiento de los extractores existentes.

Para abordarlo, se reutilizaron las funciones compartidas del proyecto y se mantuvo la misma estructura de los módulos de extracción.

Otra dificultad fue analizar archivos provenientes de distintas fuentes y formatos. Se utilizó un procedimiento automatizado de perfilamiento para obtener métricas comparables y documentar posibles problemas de calidad.

## 4. Evidencias

| Actividad | Evidencia |
|---|---|
| Fuente adicional | `src/extract/divipola.py` |
| Configuración e integración | `src/config.py` y `src/pipeline.py` |
| Muestras CSV | `src/generar_muestras.py` y `data/sample/` |
| Perfilamiento | `src/perfilar_datos.py` |
| Informe de calidad | `docs/perfilamiento.md` |
| Colaboración GitHub | Registrar enlaces de commits y PR correspondientes |

## 5. Aprendizajes

Estas actividades permitieron fortalecer conocimientos relacionados con el consumo de APIs, el almacenamiento de datos en formato Parquet, la generación automática de archivos CSV y el análisis de calidad de la información.

También permitieron comprender la importancia de conservar los datos originales y separar la extracción de las transformaciones posteriores.

## 6. Conclusión personal

Mi participación contribuyó a ampliar las fuentes de información disponibles en el observatorio y a facilitar la evaluación inicial de los datos.

La generación de muestras y el perfilamiento ayudan a que el equipo pueda consultar, comprender y validar la información antes de avanzar hacia las siguientes etapas del proyecto.
----------------------------------
# EA2

### Objetivo de mi participación

Durante la segunda entrega participé en el desarrollo del modelo dimensional de la capa oro, la elaboración de consultas SQL para responder preguntas de negocio, la documentación técnica y la automatización de la ejecución reproducible de la capa plata.

### Actividades desarrolladas

- Construcción del modelo dimensional mediante dbt y DuckDB.
- Creación de cinco dimensiones y tres tablas de hechos.
- Implementación de pruebas de integridad referencial, unicidad, valores obligatorios y granularidad.
- Elaboración del diagrama entidad-relación y el diccionario de datos.
- Desarrollo y ejecución de tres consultas SQL sobre la capa oro.
- Implementación de `src/transformar.py` para ejecutar las transformaciones de plata desde un único comando.
- Actualización del README y documentación de los resultados de negocio.

### Resultados obtenidos

La ejecución de `python -m src.transformar` finalizó correctamente, procesando las cinco fuentes y ejecutando las validaciones Pandera.

La construcción de la capa oro mediante `dbt build` generó ocho tablas y una vista, con 33 pruebas de datos aprobadas y un resultado final de `PASS=42 WARN=0 ERROR=0`.

Se documentaron tres consultas sobre precio y demanda por fase ENSO, generación por fuente energética y ventas por municipio y segmento.

### Evidencias de colaboración

- Pull Request #10: modelo dimensional y pruebas dbt.
- Pull Request #11: documentación, consultas SQL y reproducibilidad.
- Archivos de evidencia: `dbt/models/marts/`, `consultas/oro/`, `docs/modelo_dimensional.md`, `docs/diccionario_datos.md` y `src/transformar.py`.

### Aprendizajes

Esta entrega permitió fortalecer conocimientos de modelado dimensional, bases de datos analíticas, validación de integridad con dbt, consultas SQL y automatización de pipelines reproducibles.


---

# EA3 — Modelado analítico, dashboard y hallazgos

**Integrante:** Juan Esteban Urrutia  
**Rol principal:** BI Analyst / Storyteller  
**Rol complementario:** Analytics Engineer  
**Periodo académico:** 2026-2

## 1. Objetivo de mi participación

Durante la Evidencia 3 participé en la ampliación del modelo analítico del Observatorio de Energía y Clima y en el desarrollo de un dashboard interactivo que permite visualizar información del mercado eléctrico colombiano, los recursos hídricos, las condiciones climáticas y el comportamiento comercial de EnerAndes.

Mi participación se orientó a transformar los datos de la capa oro en indicadores y visualizaciones que respondieran las seis preguntas de negocio del proyecto.

## 2. Actividades desarrolladas

### 2.1. Ampliación de las métricas históricas de XM

Amplié la configuración y los procesos de extracción de XM para incorporar nuevas métricas y períodos históricos necesarios para el análisis de la Evidencia 3.

Las actividades desarrolladas incluyeron:

- Ampliación de la información histórica de embalses desde enero de 2015.
- Incorporación de aportes hídricos desde enero de 2023.
- Integración de precios de bolsa diarios.
- Incorporación de información de precios de contratos.
- Incorporación de la media histórica de aportes hídricos.
- Adecuación de las consultas por ventanas de fechas.

Estas ampliaciones permiten estudiar las variaciones de los indicadores energéticos e hídricos durante períodos más extensos.

**Evidencia:** [Commit `f014c21` — Ampliación de métricas XM](https://github.com/SernaSol/pi4-observatorio-energia-grpo-2/commit/f014c21edc1bc24e315f9fcae879b6be238ae728).

### 2.2. Desarrollo de nuevos modelos staging y analíticos

Desarrollé modelos de preparación y transformación de datos mediante dbt y DuckDB, ampliando la capa oro construida durante la Evidencia 2.

Se incorporaron los siguientes modelos staging:

- `stg_xm_precio_bolsa_diario`
- `stg_xm_precio_contrato`
- `stg_xm_aportes_media`

Asimismo, se desarrollaron cuatro modelos analíticos:

| Modelo | Objetivo |
|---|---|
| `fact_mercado_mensual` | Analizar mensualmente precios y demanda eléctrica. |
| `fact_generacion_mensual` | Consolidar la generación eléctrica por recurso y período. |
| `fact_indicadores_hidricos` | Analizar embalses y aportes frente a sus referencias históricas. |
| `fact_clima_mensual` | Analizar indicadores climáticos por municipio y mes. |

También se amplió la dimensión calendario para incorporar el período histórico desde 2015.

La ejecución de `dbt build` permitió validar los modelos mediante las pruebas de datos configuradas para el observatorio.

**Evidencias:**

- [Commit `53d6880` — Nuevos modelos staging](https://github.com/SernaSol/pi4-observatorio-energia-grpo-2/commit/53d6880e6e1b977da1c039afa71f11fefaddf7ef).
- [Commit `dd32b49` — Ampliación de la capa oro](https://github.com/SernaSol/pi4-observatorio-energia-grpo-2/commit/dd32b49f33d3fb4120543de2b2d32ee9d3bc245e).

### 2.3. Desarrollo del dashboard interactivo en Streamlit

Implementé el dashboard del Observatorio de Energía y Clima mediante Streamlit y Pandas, utilizando como fuente los archivos Parquet exportados desde la capa oro.

El dashboard se encuentra en `dashboard/app.py` y utiliza `dashboard/datos.py` para cargar las tablas analíticas.

Se desarrollaron seis análisis de negocio:

1. Evolución histórica del nivel de embalses durante las fases ENSO.
2. Comportamiento de los aportes hídricos frente a su media histórica.
3. Evolución de precios de bolsa y demanda eléctrica.
4. Participación y evolución de la generación por fuente energética.
5. Temperatura y precipitación por municipio.
6. Ventas de energía e ingresos de EnerAndes por segmento, municipio y tipo de compra.

Se incorporaron filtros por período de análisis, fase ENSO, municipios y segmento de clientes, según las dimensiones correspondientes a cada visualización.

La aplicación permite explorar tendencias y comparar indicadores mediante gráficas de líneas, barras y áreas, así como indicadores numéricos.

**Evidencia:** [Commit `54e1e33` — Implementación del dashboard Streamlit](https://github.com/SernaSol/pi4-observatorio-energia-grpo-2/commit/54e1e33e80fc74248415fbc8fb51bd3c8220c0d1).

### 2.4. Integración mediante Pull Request

Los cambios de extracción, modelado y visualización se desarrollaron en la rama `feature/dashboard` y se integraron a `main` mediante el Pull Request #18.

El Pull Request incluyó cuatro commits y fue revisado y aprobado por Sol Elena Serna Vargas antes de su integración.

**Evidencia:** [Pull Request #18 — Feature/dashboard](https://github.com/SernaSol/pi4-observatorio-energia-grpo-2/pull/18).

## 3. Resultados obtenidos

| Indicador | Resultado |
|---|---:|
| Modelos materializados de la capa oro | 12 |
| Pruebas de datos dbt aprobadas | 33 |
| Operaciones exitosas de `dbt build` | 49 |
| Tablas exportadas de oro | 12 |
| Análisis de negocio implementados | 6 |
| Pull Request de desarrollo | #18 |

El dashboard fue ejecutado localmente y permitió visualizar los indicadores construidos a partir de las tablas de la capa oro.

## 4. Dificultades y soluciones

Uno de los principales desafíos consistió en ampliar la cobertura histórica de XM, debido al volumen de información y a las respuestas variables de la API. Para abordar esta situación, se utilizaron consultas por períodos y archivos de datos que facilitan la recuperación de información.

Otro reto fue integrar información de diferentes fuentes y granularidades en un mismo dashboard. Para resolverlo, se incorporaron modelos analíticos mensuales y diarios, dimensiones de consulta y filtros interactivos.

Durante el análisis se consideraron las diferencias de cobertura temporal y las limitaciones de las unidades reportadas por las fuentes originales, evitando interpretar asociaciones descriptivas como relaciones causales.

## 5. Evidencias

| Actividad | Evidencia |
|---|---|
| Ampliación de métricas XM | `src/config.py` y `src/extract/xm.py` |
| Modelos staging | `dbt/models/staging/` |
| Modelos analíticos | `dbt/models/marts/` |
| Aplicación Streamlit | `dashboard/app.py` |
| Carga de datos Parquet | `dashboard/datos.py` |
| Capturas del dashboard | `docs/evidencias/ea3_dashboard_*.png` |
| Integración de cambios | [Pull Request #18](https://github.com/SernaSol/pi4-observatorio-energia-grpo-2/pull/18) |

## 6. Aprendizajes

Durante la Evidencia 3 fortalecí mis conocimientos sobre modelado analítico, transformación de datos mediante dbt y construcción de aplicaciones de visualización con Streamlit.

Comprendí la importancia de diseñar indicadores que respondan preguntas concretas de negocio, integrar correctamente las dimensiones de análisis y presentar información de forma clara para apoyar la toma de decisiones.

También reforcé las prácticas de trabajo colaborativo mediante Git, GitHub y revisión de Pull Requests.

## 7. Conclusión personal

Mi participación contribuyó a ampliar las capacidades analíticas del Observatorio de Energía y Clima y a transformar los datos procesados en visualizaciones que facilitan la interpretación de tendencias energéticas, hídricas, climáticas y comerciales.

La integración de los nuevos modelos de la capa oro con el dashboard Streamlit proporciona una herramienta de consulta que sirve como base para la elaboración del informe de hallazgos y recomendaciones dirigido a la gerencia de EnerAndes.