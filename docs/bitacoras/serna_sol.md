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