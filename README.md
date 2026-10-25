# Observatorio de Energía y Clima – Equipo 2

> Proyecto Integrado IV – Integración de Información | IU Digital de Antioquia | 2026-2

## 👥 Integrantes

| Nombre | Usuario GitHub | Rol |
|---|---|---|
| Sol Elena Serna Vargas | SernaSol| Líder técnico / Data Engineer |
| Esteban Urrutia | estebanurrutia1 | Data Quality Analyst |
| Sol Elena Serna Vargas | SernaSol| Analytics Engineer |
| Esteban Urrutia | estebanurrutia1 | BI Analyst / Storyteller |

## 🎯 Objetivo

Integrar información del mercado eléctrico colombiano (XM), variables climáticas (IDEAM y NOAA), datos comerciales de EnerAndes e información geográfica oficial del DANE para analizar las relaciones entre las condiciones climáticas, los recursos hídricos y el comportamiento del sector energético colombiano.

### Pregunta de negocio

¿Qué relación existe entre las precipitaciones registradas en Antioquia, los niveles de los embalses y los precios de la energía eléctrica en Colombia durante 2025 y 2026?

La incorporación de información geográfica permitirá identificar los municipios de Antioquia y complementar el análisis territorial de las estaciones meteorológicas.

## 📦 Fuentes de datos – Capa bronce

El proyecto utiliza cinco fuentes de información. Los datos extraídos se almacenan en formato Parquet dentro de `data/bronze/`.

| Fuente | Tipo | Archivos generados |
|---|---|---|
| XM – Sinergox | API REST | `xm_precio_bolsa.parquet`, `xm_demanda.parquet`, `xm_embalses.parquet`, `xm_generacion_recurso.parquet`, `xm_aportes_hidricos.parquet`, `xm_listado_recursos.parquet` |
| IDEAM – Datos Abiertos Colombia | API Socrata / SoQL | `ideam_precipitacion_diaria.parquet`, `ideam_temperatura_diaria.parquet` |
| NOAA | Archivo de texto | `noaa_oni.parquet` |
| EnerAndes | Archivo Excel | `enerandes_ventas_2023.parquet`, `enerandes_ventas_2024.parquet`, `enerandes_ventas_2025.parquet`, `enerandes_ventas_2026.parquet` |
| DANE – DIVIPOLA | API REST | `dane_divipola.parquet` |

En total, el pipeline genera **14 archivos Parquet**.

### XM – Mercado eléctrico

La extracción comprende el período del 1 de enero de 2024 al 30 de septiembre de 2026.

Se incluyen los siguientes indicadores:

- Precio de bolsa nacional.
- Demanda real de energía.
- Porcentaje de volumen útil de embalses.
- Generación de energía por recurso.
- Aportes hídricos.
- Listado de recursos de generación.

Las consultas históricas se realizan mediante ventanas de fechas. El listado de recursos se obtiene mediante el servicio de catálogos de XM.

### IDEAM – Información climática

Se extraen datos de estaciones de Antioquia desde el 1 de enero de 2025 hasta el 30 de septiembre de 2026, sujeto a la disponibilidad de registros publicados.

**Precipitación diaria:** se calcula la suma de los valores observados por estación y día.

**Temperatura diaria:** se calculan promedio, mínimo y máximo de temperatura por estación y día.

Las agregaciones se realizan directamente en el servidor mediante consultas SoQL, para reducir el volumen de información transferida.

En los datos descargados y perfilados, la última fecha observada en ambas fuentes es el 24 de julio de 2026.

### NOAA – Índice ONI

Se descarga información del índice Oceanic Niño Index (ONI), que permite complementar el análisis de las condiciones climáticas asociadas con El Niño y La Niña.

Origen: https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt

### EnerAndes – Ventas internas

Se utiliza el archivo `ventas_enerandes_2023_2026.xlsx`, que contiene información comercial organizada en hojas correspondientes a los años 2023, 2024, 2025 y 2026.

Los datos se conservan en la capa bronce sin aplicar limpieza ni transformaciones de negocio.

### Fuente adicional: DIVIPOLA – DANE

**Fuente:** Departamento Administrativo Nacional de Estadística (DANE).

**Descripción:** DIVIPOLA contiene información de los departamentos y municipios de Colombia, incluidos sus códigos oficiales, nombres y coordenadas geográficas.

**Origen:** https://www.datos.gov.co/resource/gdxc-w37w.json

**Objetivo:** complementar el análisis climático y energético mediante la identificación geográfica de los municipios de Antioquia.

**Uso en el proyecto:** facilitar la identificación territorial de las estaciones meteorológicas del IDEAM. La relación entre nombres y códigos municipales requerirá validación y estandarización en una etapa posterior.

**Extracción:** se utiliza el módulo `src/extract/divipola.py`, que consulta el servicio mediante HTTP GET y almacena el resultado en `data/bronze/dane_divipola.parquet`.

En la ejecución validada se obtuvieron 1.122 registros y 10 columnas, incluidas las columnas de linaje.

## ⚙️ Requisitos para ejecutar el proyecto

Se necesita:

- Python y pip instalados.
- Acceso a internet para consultar las APIs.
- Archivo Excel de EnerAndes disponible localmente.
- Permisos para crear archivos y carpetas en el proyecto.

Las dependencias de Python se encuentran en `requirements.txt`.

## 🚀 Instalación y ejecución

### 1. Clonar el repositorio

```powershell
git clone https://github.com/SernaSol/pi4-observatorio-energia-grpo-2.git
cd pi4-observatorio-energia-grpo-2
```

### 2. Crear el entorno virtual

```powershell
python -m venv .venv
```

### 3. Activar el entorno virtual

En Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Instalar las dependencias

```powershell
python -m pip install -r requirements.txt
```

### 5. Preparar el archivo de EnerAndes

Crear la carpeta `data/insumos/`, si todavía no existe.

```powershell
New-Item -ItemType Directory -Force data/insumos
```

Copiar el archivo `ventas_enerandes_2023_2026.xlsx` dentro de esa carpeta.

La ruta esperada es:

`data/insumos/ventas_enerandes_2023_2026.xlsx`

El archivo debe ser proporcionado por el equipo o por el responsable de los datos.

### 6. Ejecutar el pipeline de extracción

```powershell
python -m src.pipeline
```

El pipeline ejecuta los extractores de XM, IDEAM, NOAA, EnerAndes y DIVIPOLA.

Los resultados se almacenan en `data/bronze/`.

Para repetir una extracción completa y reemplazar los archivos existentes:

```powershell
python -m src.pipeline --forzar
```

Las fechas y parámetros de las consultas se encuentran en `src/config.py`.

El tiempo de ejecución depende de la conexión a internet, la disponibilidad de las APIs y el volumen de datos solicitados.

## 📄 Generación de muestras CSV

Para evitar subir los archivos originales de la capa bronce a GitHub, el repositorio incluye muestras de los datos.

Cada muestra contiene las primeras 200 filas del archivo Parquet correspondiente, o menos si el archivo original tiene menos registros.

Para regenerar las muestras:

```powershell
python -m src.generar_muestras
```

Los archivos CSV se almacenan en:

`data/sample/`

En la ejecución validada se generaron 14 archivos CSV de 200 filas cada uno.

## 🧪 Pruebas automáticas

El proyecto contiene pruebas automáticas desarrolladas con pytest para validar funciones de soporte y componentes de extracción.

Para ejecutar las pruebas:

```powershell
python -m pytest -v
```

Las pruebas incluyen verificaciones de:

- Generación de ventanas de fechas.
- Comprobación de archivos existentes.
- Procesamiento de respuestas JSON de XM.
- Construcción de consultas SoQL del IDEAM.

En la última ejecución validada, las cuatro pruebas finalizaron correctamente.

## 📊 Perfilamiento de calidad de datos

El archivo `docs/perfilamiento.md` contiene el análisis inicial de calidad de los 14 archivos de bronce.

Se documentan:

- Cantidad de filas y columnas.
- Tipos de datos.
- Porcentaje de valores nulos por columna.
- Número de registros duplicados exactos.
- Rangos temporales, cuando corresponda.
- Hallazgos de calidad sustentados con evidencia numérica.
- Recomendaciones para etapas posteriores de limpieza y transformación.

Para regenerar el perfilamiento:

```powershell
python -m src.perfilar_datos
```

El perfilamiento no modifica los archivos originales de la capa bronce.

## 🏗️ Arquitectura

```text
FUENTES DE DATOS
   |
   |-- XM
   |-- IDEAM
   |-- NOAA
   |-- EnerAndes
   |-- DANE - DIVIPOLA
   |
   v
CAPA BRONCE
Datos originales + trazabilidad
   |
   v
CAPA PLATA
Limpieza y estandarización (etapa posterior)
   |
   v
CAPA ORO
Modelo analítico (etapa posterior)
   |
   v
VISUALIZACIÓN
Indicadores y dashboard (etapa posterior)
```

Los archivos de la capa bronce contienen tres campos adicionales para asegurar la trazabilidad:

- `_fuente`: fuente de los registros.
- `_origen`: dirección o recurso utilizado.
- `_extraido_en`: fecha y hora de extracción.

## 📁 Organización del proyecto

```text
pi4-observatorio-energia-grpo-2/
|
|-- data/
|   |-- bronze/
|   |-- insumos/
|   |-- sample/
|
|-- docs/
|   |-- bitacoras/
|   |-- perfilamiento.md
|
|-- src/
|   |-- extract/
|   |   |-- xm.py
|   |   |-- ideam.py
|   |   |-- noaa.py
|   |   |-- enerandes.py
|   |   |-- divipola.py
|   |
|   |-- config.py
|   |-- pipeline.py
|   |-- generar_muestras.py
|   |-- perfilar_datos.py
|
|-- tests/
|   |-- test_utils.py
|   |-- test_xm.py
|   |-- test_ideam.py
|
|-- .gitignore
|-- requirements.txt
|-- README.md
```

## 🔒 Control de versiones

El repositorio utiliza Git y GitHub para el control de versiones.

Se trabaja mediante ramas de desarrollo y Pull Requests que permiten revisar los cambios antes de integrarlos en `main`.

Los datos originales almacenados en `data/bronze/` no deben subirse al repositorio.

Las muestras disponibles en `data/sample/` forman parte de los entregables del proyecto.

## 🤖 Uso de inteligencia artificial

Durante el desarrollo del proyecto se utilizó ChatGPT como herramienta de apoyo para comprender requisitos, diseñar componentes de extracción, revisar código Python, estructurar pruebas automáticas y preparar documentación técnica.

Las propuestas se revisaron y probaron localmente antes de incorporarlas al proyecto.

## 📌 Limitaciones y consideraciones

- La disponibilidad de registros del IDEAM depende de su publicación en los conjuntos de datos consultados.
- Los datos de EnerAndes requieren disponer del archivo Excel original.
- La capa bronce conserva los valores recibidos, por lo que puede incluir columnas almacenadas como texto y valores incompletos.
- Las relaciones geográficas entre las estaciones del IDEAM y DIVIPOLA requieren validación adicional.
- Las transformaciones analíticas y visualizaciones corresponden a etapas posteriores del proyecto.
