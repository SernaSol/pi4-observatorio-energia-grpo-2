"""
Fuente 2 - IDEAM en datos.gov.co (plataforma Socrata, lenguaje de consulta SoQL).
  
  - Dos datasets: precipitacion (s54a-sgyg) y temperatura del aire (sbwg-7ju4)
  - Cada uno tiene MILLONES de observaciones (una cada pocos minutos desde 2005)
  - Por eso FILTRAMOS ($where) y AGREGAMOS ($select + $group) EN EL SERVIDOR:
    viaja un resumen diario por estacion, no millones de filas
        precipitacion -> sum()             = lluvia total del dia
      temperatura   -> avg(), min(), max() = media, minima y maxima del dia
  - Paginamos con $limit / $offset por si una semana trae muchas filas
  - Como son ~92 semanas por dataset, cada semana se guarda en una carpeta
    temporal: si la descarga se corta, al ejecutar de nuevo continua donde iba
Documentacion SoQL: https://dev.socrata.com/docs/queries/
"""
# ---------------------------------------------------------------------------
# IMPORTS (traer codigo que ya existe)
# ---------------------------------------------------------------------------
import pandas as pd     # pandas: libreria de tablas. "as pd" le pone el nombre corto pd.
                        # Aqui se usa para convertir la lista de filas en tabla (DataFrame).
import json             # json: leer y escribir los archivos temporales de cada semana
import shutil
from datetime import timedelta                      

from src import config  # config.py: datasets del IDEAM, departamento, fechas y ventana
from src.utils import guardar_bronce, http_json, log, ventanas, ya_existe
# Funciones de utils.py de este proyecto:
#   guardar_bronce: guarda la tabla en Parquet con 3 columnas de linaje
#   http_json:      le envia un pedido a una API y devuelve la respuesta; reintenta si falla
#   log:            escribe un mensaje en pantalla con la hora
#   ventanas:       parte un rango de fechas en bloques (aqui, de 7 dias)
#   ya_existe:      dice si el archivo ya esta en bronce (para no descargarlo otra vez)

# ---------------------------------------------------------------------------
# CONSTANTES: valores fijos de este extractor (en MAYUSCULAS por convencion)
# ---------------------------------------------------------------------------
# Columnas que describen la estacion; son iguales en los dos datasets.
CAMPOS = "codigoestacion, nombreestacion, municipio, zonahidrografica, latitud, longitud"
PAGINA = 50000          # filas maximas por pedido ($limit)                          # filas maximas por pedido ($limit)



def consulta_soql(agregacion: str, inicio, fin, offset: int) -> dict:
    """Arma los parametros SoQL: filtrar Antioquia y la semana, y resumir por estacion y dia.
       agregacion: lo que se calcula del valor observado, por ejemplo
                "sum(valorobservado) AS precipitacion_mm"
    """

    return {
        "$select": f"{CAMPOS}, date_trunc_ymd(fechaobservacion) AS fecha, "   # el dia
                   f"{agregacion}, count(*) AS n_obs",                         # resumen + conteo
        "$where": (
            f"departamento = '{config.IDEAM_DEPARTAMENTO}' AND "
            f"fechaobservacion >= '{inicio}T00:00:00' AND "
            f"fechaobservacion < '{fin + timedelta(days=1)}T00:00:00' AND "
            "valorobservado IS NOT NULL"
        ),  # filtra Antioquia y la semana, y descarta nulos
        "$group": f"{CAMPOS}, fecha",             # un grupo por estacion y dia
        "$order": "fecha, codigoestacion",        # ordenado por fecha y estacion
        "$limit": PAGINA,                         # filas por pagina
        "$offset": offset,                        # filas que se saltan (para pedir la pagina siguiente)
    }




def descargar_semana(url: str, agregacion: str, inicio, fin) -> list:
    """Pide UNA semana al servidor, pagina por pagina, y devuelve todas sus filas."""
    filas = []
    offset = 0                                    # empezar por la primera pagina
    while True:                                   # paginacion: repetir hasta la ultima pagina
        lote = http_json("GET", url, params=consulta_soql(agregacion, inicio, fin, offset))
        filas.extend(lote)
        if len(lote) < PAGINA:                    # llegaron menos que el limite: era la ultima
            return filas
        offset += PAGINA                          # pedir la pagina siguiente


def extraer_dataset(nombre: str, url: str, agregacion: str, forzar: bool) -> None:
    """Descarga un dataset del IDEAM semana por semana y lo guarda en bronce."""
    if ya_existe(nombre, forzar):                 # si el Parquet final ya esta...
        return                                    # ...no se descarga otra vez
    # Carpeta temporal con un .json por semana: data/bronze/_tmp_<nombre>/
    temporal = config.DIR_BRONZE / f"_tmp_{nombre}"
    if forzar and temporal.exists():
        shutil.rmtree(temporal)                   # --forzar: empezar de cero
    temporal.mkdir(parents=True, exist_ok=True)

    filas = []
    for inicio, fin in ventanas(config.IDEAM_FECHA_INICIO, config.IDEAM_FECHA_FIN, config.IDEAM_DIAS_VENTANA):
        archivo = temporal / f"{inicio}.json"
        if archivo.exists():                      # esta semana ya se habia bajado antes
            semana = json.loads(archivo.read_text(encoding="utf-8"))
            estado = "ya estaba"
        else:
            semana = descargar_semana(url, agregacion, inicio, fin)
            auxiliar = archivo.with_suffix(".json.part")
            auxiliar.write_text(
                json.dumps(semana),encoding="utf-8"
            )  # primero escribe un .part para no dejar un .json incompleto
            auxiliar.replace(archivo)               # renombra .part -> .json cuando termina
            estado = "descargada"
        filas.extend(semana)
        log(f"   semana {inicio} a {fin}: {len(semana)} filas ({estado})")

    # Todas las semanas listas: un solo Parquet en bronce y se borra lo temporal
    guardar_bronce(pd.DataFrame(filas), nombre, fuente="IDEAM", origen=url)
    shutil.rmtree(temporal)






def extraer(forzar: bool = False) -> None:
    """Descarga los datasets del IDEAM definidos en config.IDEAM_DATASETS."""

    log("IDEAM - datos abiertos (SoQL)")

    for nombre, url, agregacion in config.IDEAM_DATASETS:
        log(f" {nombre}")
        extraer_dataset(nombre, url, agregacion, forzar)


# ---------------------------------------------------------------------------
# Este bloque solo se ejecuta cuando se corre ESTE archivo directamente:
#     python -m src.extract.ideam
# Cuando otro archivo lo importa (como pipeline.py), este bloque NO se ejecuta.
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import sys      # sys.argv: lista con lo que se escribio en el comando
    extraer(forzar="--forzar" in sys.argv)   # True si el comando trae --forzar
