# Bitácora – Sol Serna

**Proyecto:** Observatorio de Energía y Clima – Equipo 2  
**Asignatura:** Proyecto Integrado IV 
**Institución:** IU Digital de Antioquia  
**Periodo:** 2026-2
**Rol:** Líder técnico / Data Engineer - Analytics Engineer

## 1. Objetivo de mi participación

Mi participación se enfocó en los puntos 1, 2, 3, 4 y 8 de la actividad, relacionados con la organización del repositorio, la ampliación de las fuentes de información del sector energético y climático, la conservación de datos originales y la implementación de pruebas automáticas.

Estas actividades buscaron fortalecer la organización del proyecto y la confiabilidad de los procesos de extracción.

## 2. Actividades desarrolladas

### Punto 1. Organización del repositorio y trabajo colaborativo

Se trabajó en la organización del proyecto mediante Git y GitHub, utilizando ramas independientes y Pull Requests.

Las actividades incluyeron:

- Configuración del repositorio del equipo.
- Aplicación de reglas de protección para la rama `main`.
- Organización del trabajo mediante ramas de desarrollo.
- Participación en la creación y revisión de Pull Requests.
- Seguimiento de los cambios realizados en los módulos del proyecto.

Este proceso permitió organizar las contribuciones y evitar modificaciones directas en la rama principal sin revisión.

**Commit:** https://github.com/SernaSol/pi4-observatorio-energia-grpo-2/commit/4a21a839f7483bf635a3cddf29bd720988e72580

### Punto 2. Ampliación de la extracción de XM

Se trabajó en la ampliación de la extracción histórica de datos del mercado eléctrico colombiano mediante la API de XM.

El período de extracción se extendió desde el 1 de enero de 2024 hasta el 30 de septiembre de 2026.

Se incluyeron las siguientes métricas:

- Precio de bolsa nacional.
- Demanda real de energía.
- Porcentaje de volumen útil de embalses.
- Generación por recurso.
- Aportes hídricos.
- Listado de recursos.

Para las consultas históricas se utilizaron ventanas de fechas y se implementó el procesamiento de las respuestas recibidas.

**Resultado:** se generaron seis archivos Parquet con información energética, entre ellos `xm_generacion_recurso.parquet`, con 350.361 registros.
**Commit:** https://github.com/SernaSol/pi4-observatorio-energia-grpo-2/commit/91deaf42b4b6f7fca05c4f8c91c50f6c5ec1e403
**PR:** Merge pull request #1 from SernaSol/feature/ampliacion-extractores

### Punto 3. Ampliación de información climática del IDEAM

Se trabajó en la extracción de información del IDEAM utilizando la API Socrata de datos.gov.co.

Se incluyeron dos indicadores:

**Precipitación diaria:** agregación de valores observados por estación y fecha.

**Temperatura diaria:** cálculo de valores promedio, mínimo y máximo por estación y fecha.

Las consultas se realizaron mediante SoQL y se organizaron por ventanas semanales para facilitar el procesamiento.

**Dificultad:** gestionar la descarga de información histórica sin realizar solicitudes excesivamente grandes.

**Solución:** dividir las consultas en períodos más pequeños y conservar los resultados antes de generar los archivos finales.

**Resultado:** se obtuvieron 29.804 registros de precipitación y 17.349 registros de temperatura.
**Commit:** https://github.com/SernaSol/pi4-observatorio-energia-grpo-2/commit/eed71afe9385f09fe1bb23c4cfb9fead5351328e

### Punto 4. Conservación de fuentes NOAA y EnerAndes

Se revisaron los procesos de extracción de NOAA y EnerAndes para asegurar que la información original se conservara en la capa bronce.

Para NOAA se mantuvo la lectura del índice ONI desde su archivo de texto.

Para EnerAndes se conservó la información proveniente de las hojas del archivo Excel, incluyendo su estructura original, encabezados y totales.

**Resultado:** se generó un archivo Parquet para NOAA y cuatro archivos correspondientes a los años 2023, 2024, 2025 y 2026 de EnerAndes.

### Punto 8. Implementación de pruebas automáticas

Se incorporaron pruebas automáticas utilizando pytest para validar componentes importantes del pipeline.

Se desarrollaron pruebas para:

- Generación de ventanas de fechas.
- Verificación de archivos existentes.
- Procesamiento de respuestas JSON de XM.
- Construcción de consultas SoQL del IDEAM.

Las pruebas se implementaron en los archivos `tests/test_utils.py`, `tests/test_xm.py` y `tests/test_ideam.py`.

También se agregó pytest a las dependencias del proyecto.

**Resultado:** las cuatro pruebas finalizaron correctamente mediante el comando `python -m pytest -v`.
**Commit:** https://github.com/SernaSol/pi4-observatorio-energia-grpo-2/commit/96c70a0c86feff71523d16af5d54c428f19664ee
**PR:** Merge pull request #2 from SernaSol/feature/pruebas-automaticas

## 3. Dificultades y soluciones

Durante el desarrollo surgieron retos relacionados con la ampliación de los períodos históricos, el procesamiento de respuestas de distintas APIs y la organización de los cambios mediante Git.

Para resolverlos, se realizaron ejecuciones por períodos, validaciones sobre los archivos generados y pruebas automáticas para verificar funciones específicas sin depender constantemente de las APIs externas.

También se aplicó el flujo de Pull Requests para organizar las contribuciones y facilitar su revisión.

## 4. Evidencias

| Actividad | Evidencia |
|---|---|
| Configuración del proyecto | Repositorio GitHub y protección de `main` |
| Extracción XM | `src/extract/xm.py` |
| Extracción IDEAM | `src/extract/ideam.py` |
| NOAA y EnerAndes | `src/extract/noaa.py` y `src/extract/enerandes.py` |
| Pruebas automáticas | `tests/test_utils.py`, `tests/test_xm.py` y `tests/test_ideam.py` |
| Resultado de pruebas | 4 pruebas aprobadas |
| Colaboración | Commits y Pull Requests asociados a las actividades |

## 5. Aprendizajes

El desarrollo de estas actividades permitió fortalecer conocimientos de integración de datos, consultas a APIs, manejo de información histórica, control de versiones y pruebas automáticas.

Comprendí la importancia de organizar los extractores, validar las respuestas de servicios externos y aplicar pruebas para detectar problemas antes de ejecutar el proceso completo.

También reforcé el manejo de Git y GitHub como herramientas para el trabajo colaborativo.



## 6. Conclusión personal

Mi participación contribuyó a mejorar la cobertura histórica de las fuentes energéticas y climáticas, conservar la información de las fuentes originales y fortalecer las validaciones del proyecto mediante pruebas automáticas.

Estas actividades permiten que el equipo disponga de una base técnica organizada para continuar con las siguientes etapas de integración y análisis de datos.

------------------------------------
# EA2

### Objetivo de mi participación

Durante la segunda entrega participé en la transformación de las fuentes de datos hacia la capa plata, la implementación de controles de calidad y las pruebas automáticas, procurando conservar los datos originales y garantizar la trazabilidad de los registros.

### Actividades desarrolladas

- Limpieza y consolidación de las ventas de EnerAndes correspondientes a 2023-2026.
- Transformación y estandarización de datos de XM, IDEAM, NOAA y DIVIPOLA.
- Implementación de esquemas de validación con Pandera.
- Desarrollo de pruebas automáticas para verificar reglas de limpieza y calidad.
- Consolidación del reporte de calidad de la capa plata.

### Resultados obtenidos

Se obtuvieron 4.007 registros limpios de EnerAndes y 163 registros en cuarentena. Para XM, se procesaron 5.935.449 registros válidos de generación y se separaron 2.473.215 registros en cuarentena.

La batería de pruebas de Python de EA2 alcanzó 26 pruebas aprobadas.

### Evidencias de colaboración

- Pull Request #8: integración de las primeras transformaciones de la capa plata.
- Pull Request #9: integración de las validaciones, pruebas y documentación de calidad.
- Archivos de evidencia: `docs/reporte_calidad.md`, `src/silver/`, `src/quality/esquemas.py` y `tests/`.

### Aprendizajes

La segunda entrega permitió profundizar en procesos ETL, validación de datos con Pandera, gestión de registros en cuarentena y construcción de información confiable para su posterior modelado analítico.

---

# EA3 — Automatización y calidad de datos

**Integrante:** Sol Elena Serna Vargas  
**Rol principal:** Data Quality Analyst  
**Rol complementario:** Data Engineer  
**Periodo académico:** 2026-2

## 1. Objetivo de mi participación

Durante la Evidencia 3 participé en la automatización del pipeline del Observatorio de Energía y Clima y en el fortalecimiento de los controles de calidad de los datos.

Mi trabajo se enfocó en integrar las etapas de extracción, transformación, modelado y pruebas automáticas mediante GitHub Actions, garantizando que los resultados puedan verificarse de forma reproducible.

## 2. Actividades desarrolladas

### 2.1. Automatización del pipeline con GitHub Actions

Implementé y ajusté el workflow `.github/workflows/pipeline.yml`, incorporando las siguientes funcionalidades:

- Ejecución automática diaria mediante `schedule`.
- Ejecución manual mediante `workflow_dispatch`.
- Ejecución de pruebas cuando se crean o actualizan Pull Requests hacia `main`.
- Extracción de datos de las cinco fuentes del observatorio.
- Transformación y validación de la capa plata mediante Pandera.
- Construcción y validación de la capa oro utilizando dbt y DuckDB.
- Ejecución de pruebas automatizadas con pytest.
- Exportación de las tablas de la capa oro en formato Parquet.
- Publicación de artefactos y del reporte de calidad en GitHub Actions.

También se incorporaron mecanismos de caché para reutilizar los archivos de extracción y reducir consultas repetidas a las fuentes externas.

### 2.2. Implementación de pruebas adicionales de calidad

Desarrollé tres pruebas automatizadas para verificar la consistencia de los datos analíticos de la capa oro.

Las pruebas se encuentran en `tests/test_calidad_ea3.py`:

| Prueba | Validación |
|---|---|
| `test_calendario_sin_fechas_duplicadas` | Comprueba que la dimensión calendario no contenga fechas duplicadas. |
| `test_porcentaje_aportes_hidricos_correcto` | Verifica la consistencia del cálculo del porcentaje de aportes hídricos frente a la media histórica. |
| `test_clima_sin_duplicados_por_mes_municipio` | Valida que los indicadores climáticos no contengan duplicados para una misma combinación de mes y municipio. |

Estas pruebas se integraron con las existentes de las Evidencias 1 y 2.

### 2.3. Ejecución y validación de pruebas

Ejecuté la batería de pruebas automatizadas utilizando el comando:

```powershell
python -m pytest -v
```

**Resultados de la ejecución local:**

| Indicador | Resultado |
|---|---:|
| Pruebas aprobadas | 30 |
| Pruebas nuevas EA3 | 3 |
| Pruebas fallidas | 0 |
| Tiempo de ejecución | 17,88 segundos |

También se verificó la construcción de la capa oro mediante `dbt build`, con 33 pruebas de datos aprobadas y sin errores.

### 2.4. Control de versiones y trabajo colaborativo

Desarrollé las actividades mediante ramas independientes de Git, utilizando Pull Requests para solicitar la revisión de los cambios antes de integrarlos a `main`.

Durante la Evidencia 3 se realizaron los siguientes Pull Requests:

| PR | Actividad |
|---|---|
| [#14](https://github.com/SernaSol/pi4-observatorio-energia-grpo-2/pull/14) | Implementación del pipeline automatizado y exportación de la capa oro. |
| [#15](https://github.com/SernaSol/pi4-observatorio-energia-grpo-2/pull/15) | Actualización del workflow con las tres capas, pytest y artefactos. |
| [#16](https://github.com/SernaSol/pi4-observatorio-energia-grpo-2/pull/16) | Ajustes adicionales de automatización. |
| [#17](https://github.com/SernaSol/pi4-observatorio-energia-grpo-2/pull/17) | Incorporación de la insignia del workflow en el README. |
| [#19](https://github.com/SernaSol/pi4-observatorio-energia-grpo-2/pull/19) | Incorporación de tres pruebas adicionales de calidad de EA3. |

Los cambios fueron revisados y aprobados por Juan Esteban Urrutia antes de su integración a la rama principal.

## 3. Dificultades y soluciones

Uno de los principales desafíos fue la ejecución de las extracciones históricas de XM dentro de GitHub Actions, debido a tiempos de respuesta elevados y errores intermitentes de la API.

Se utilizaron consultas por ventanas de fechas, mecanismos de caché y reintentos de las ejecuciones para facilitar el procesamiento y reducir las descargas innecesarias.

También fue necesario garantizar que las pruebas de calidad utilizaran correctamente las tablas generadas por dbt, respetando el orden de ejecución de las etapas del pipeline.

## 4. Evidencias

| Actividad | Evidencia |
|---|---|
| Automatización | `.github/workflows/pipeline.yml` |
| Pruebas de calidad EA3 | `tests/test_calidad_ea3.py` |
| Ejecución de pytest | `docs/evidencias/ea3_pytest.png` |
| Exportación de oro | `src/exportar_oro.py` |
| Ejecución del pipeline | [GitHub Actions](https://github.com/SernaSol/pi4-observatorio-energia-grpo-2/actions/workflows/pipeline.yml) |
| Integración de pruebas | [Pull Request #19](https://github.com/SernaSol/pi4-observatorio-energia-grpo-2/pull/19) |

## 5. Aprendizajes

Durante esta evidencia fortalecí mis conocimientos sobre integración continua y automatización de pipelines de datos con GitHub Actions.

Comprendí la importancia de integrar controles de calidad en cada etapa del procesamiento, ejecutar pruebas automáticas y publicar artefactos que permitan verificar los resultados.

También reforcé el uso de Git y GitHub para el desarrollo colaborativo, la revisión de código y la integración controlada de cambios.

## 6. Conclusión personal

Mi participación en la Evidencia 3 contribuyó a automatizar el procesamiento integral de los datos y fortalecer la confiabilidad del Observatorio de Energía y Clima.

La integración de GitHub Actions, Pandera, dbt y pytest permite detectar errores durante el procesamiento, validar los indicadores y disponer de información estructurada para el dashboard y los análisis de negocio.

Este trabajo proporciona mecanismos de automatización y calidad que respaldan los hallazgos y recomendaciones presentados a la gerencia de EnerAndes.