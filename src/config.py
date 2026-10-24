"""
Configuracion central del pipeline.
Todo lo que puede cambiar (fechas, URLs, rutas) vive AQUI y no regado en el codigo.
Si hay que cambiar una fecha o una URL, se cambia en este archivo y en ningun otro.
"""
# ---------------------------------------------------------------------------
# IMPORTS (traer codigo que ya existe)
# ---------------------------------------------------------------------------
from datetime import date   # datetime: libreria de Python para fechas y horas.
                            # date sirve para escribir una fecha: date(2026, 1, 1)
from pathlib import Path    # pathlib: libreria de Python para manejar rutas de
                            # carpetas y archivos sin preocuparse por / o \

# --- Rango de fechas a extraer --------------------------------------------
# EA1 pide rango de fechas a mínimo 2 años, desde el 1 de enero de 2024 hasta el 30 de septiembre de 2026
FECHA_INICIO = date(2024, 1, 1)     # primer dia que se descarga
FECHA_FIN = date(2026, 9, 30)       # ultimo dia que se descarga

# --- Rutas (relativas a la raiz del proyecto) ------------------------------
# __file__ es la ruta de ESTE archivo (src/config.py).
# .resolve() la vuelve ruta completa; .parent sube una carpeta.
# Dos veces .parent: de src/config.py sube a src/ y luego a la raiz del proyecto.
RAIZ = Path(__file__).resolve().parent.parent
DIR_INSUMOS = RAIZ / "data" / "insumos"     # el operador / une partes de una ruta
DIR_BRONZE = RAIZ / "data" / "bronze"       # aqui se guardan los datos descargados

# --- Fuente 1: API de XM (mercado electrico) -------------------------------
XM_URL = "https://servapibi.xm.com.co/{periodo}"   # periodo: hourly | daily | lists
XM_MAX_DIAS = 30                                    # la API no acepta rangos mas largos
XM_METRICAS = [
    # Lista de tuplas. Cada tupla es una metrica a descargar:
    # (MetricId, Entity, periodo, nombre del archivo en bronce)

      # Precio de bolsa por hora
    ("PrecBolsNaci", "Sistema", "hourly", "xm_precio_bolsa"),
    # Demanda real por hora
    ("DemaReal", "Sistema", "hourly", "xm_demanda"),
    # Porcentaje de embalses por día
    ("PorcVoluUtilDiar", "Sistema", "daily", "xm_embalses"),
    # Generación por hora de cada planta
    ("Gene", "Recurso", "hourly", "xm_generacion_recurso"),
    # Aportes hídricos por día
    ("AporEner", "Sistema", "daily", "xm_aportes_hidricos"),
    # Catálogo de plantas, sin rango de fechas
    ("ListadoRecursos", "Sistema", "lists", "xm_listado_recursos"),
]

# --- Fuente 2: IDEAM en datos.gov.co (API Socrata / SoQL) ------------------
IDEAM_DEPARTAMENTO = "ANTIOQUIA"
IDEAM_DIAS_VENTANA = 7          # pedir de a una semana evita timeouts del servidor
# EA1 pide mínimo 1 año, desde el 1 de enero de 2025.
# El IDEAM puede tardar en responder, por eso se consulta en ventanas de 7 dias.
# Cada dataset se descargara desde el 01/01/2025 hasta el 30/09/2026.

IDEAM_FECHA_INICIO = date(2025, 1, 1)
IDEAM_FECHA_FIN = date(2026, 9, 30)
# Datasets del IDEAM
IDEAM_DATASETS = [
    # (nombre del archivo en bronce, URL del dataset, agregacion SoQL del dia)
    # La agregacion la hace el SERVIDOR: viaja un resumen por estacion y dia.
    ("ideam_precipitacion_diaria",
     "https://www.datos.gov.co/resource/s54a-sgyg.json",
     "sum(valorobservado) AS precipitacion_mm"),               # lluvia total del dia
    ("ideam_temperatura_diaria",
     "https://www.datos.gov.co/resource/sbwg-7ju4.json",
     "avg(valorobservado) AS temp_media_c, "                   # temperatura media del dia
     "min(valorobservado) AS temp_min_c, "                     # la mas baja del dia
     "max(valorobservado) AS temp_max_c"),                     # la mas alta del dia
]



# --- Fuente 3: NOAA, indice de El Nino (archivo de texto) ------------------
NOAA_ONI_URL = "https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt"

# --- Fuente 4: archivo interno de EnerAndes (Excel) ------------------------
ENERANDES_EXCEL = DIR_INSUMOS / "ventas_enerandes_2023_2026.xlsx"

# --- Comportamiento HTTP ---------------------------------------------------
HTTP_TIMEOUT = 120      # segundos que se espera una respuesta antes de rendirse
HTTP_REINTENTOS = 4     # intentos ante fallas de red o del servidor
