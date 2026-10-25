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