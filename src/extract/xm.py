"""
Fuente 1 - API REST de XM (operador del mercado electrico colombiano).
  - Metodo POST con un cuerpo JSON
  - Maximo 30 dias por consulta  ->  pedimos por VENTANAS
  - No requiere usuario ni clave
  - Tres endpoints: hourly (por hora), daily (por dia) y lists (catalogos)
  - ListadoRecursos (catalogo de plantas) va por "lists": NO recibe fechas
    y responde con otra estructura (ListEntities). Por eso tiene su propia funcion.


Documentacion: https://github.com/EquipoAnaliticaXM/API_XM
"""
# ---------------------------------------------------------------------------
# IMPORTS (traer codigo que ya existe)
# ---------------------------------------------------------------------------
import pandas as pd     # pandas: libreria de tablas. "as pd" le pone el nombre corto pd.
                        # Aqui se usa para convertir la lista de filas en tabla (DataFrame).

from src import config  # config.py de este proyecto: URL de XM, fechas y lista de metricas.
from src.utils import guardar_bronce, http_json, log, ventanas, ya_existe
# Funciones de utils.py de este proyecto:
#   guardar_bronce: guarda la tabla en Parquet con 3 columnas de linaje
#   http_json:      le envia un pedido a una API y devuelve la respuesta; reintenta si falla
#   log:            escribe un mensaje en pantalla con la hora
#   ventanas:       parte un rango de fechas en bloques de 30 dias
#   ya_existe:      dice si el archivo ya esta en bronce (para no descargarlo otra vez)


LLAVE_ENTIDADES = {
    "hourly": "HourlyEntities",     # datos por hora: Values trae Hour01 ... Hour24
    "daily": "DailyEntities",       # datos por dia: un solo Value por entidad
    "lists": "ListEntities",        # catalogos: Values trae los atributos (codigo, nombre, tipo...)
}


# ---------------------------------------------------------------------------
# NOTA sobre "respuesta: dict" o "-> list" en las funciones:
# son ANOTACIONES DE TIPO. Dicen que tipo de dato se espera (dict = diccionario,
# str = texto, bool = verdadero/falso, list = lista) y que devuelve la funcion
# (-> list). Python no las obliga: sirven para que el codigo se entienda mejor.
# ---------------------------------------------------------------------------


def aplanar(respuesta: dict, periodo: str) -> list:
    """Convierte el JSON anidado de XM en filas planas, SIN cambiar los valores.
    periodo = "hourly" | "daily" | "lists"
    """
    llave = LLAVE_ENTIDADES[periodo]               # HourlyEntities, DailyEntities o ListEntities

    filas = []                                     # lista vacia donde se van guardando las filas
    # .get("Items", []) toma la lista "Items" de la respuesta;
    # si XM no la mando, devuelve una lista vacia [] en vez de fallar.

    for item in respuesta.get("Items", []):        # en hourly/daily cada item es un dia
        for entidad in item.get(llave, []):
            fila = {"Date": item.get("Date"), "Id": entidad.get("Id")}
            if periodo == "daily":
                fila["Value"] = entidad.get("Value")           # un solo valor por dia
            else:
                # ** desempaca el diccionario Values dentro de la fila:
                #   hourly -> agrega Hour01 ... Hour24 (y el codigo de la planta en Recurso)
                #   lists  -> agrega los atributos del catalogo (nombre, tipo, fuente, agente...)
                fila.update(entidad.get("Values", {}))
            filas.append(fila)

    return filas                                   # entrega la lista de filas

def extraer_lista(metrica: str, entidad: str, nombre: str, forzar: bool) -> None:
    """Descarga un catalogo de XM (endpoint lists). Una sola peticion, sin fechas."""
    if ya_existe(nombre, forzar):
        return
    url = config.XM_URL.format(periodo="lists")    # https://servapibi.xm.com.co/lists
    cuerpo = {"MetricId": metrica, "Entity": entidad}   # sin StartDate, EndDate ni Filter
    respuesta = http_json("POST", url, json=cuerpo)
    filas = aplanar(respuesta, "lists")
    log(f"   {metrica}: {len(filas)} filas")
    guardar_bronce(pd.DataFrame(filas), nombre, fuente="XM", origen=f"{url} MetricId={metrica}")


def extraer_metrica(metrica: str, entidad: str, periodo: str, nombre: str, forzar: bool) -> None:
    """Descarga una metrica de XM en ventanas de 30 dias y la guarda en bronce."""
    if ya_existe(nombre, forzar):                  # si el archivo ya esta en bronce...
        return                                     # ...termina aqui, sin descargar
    url = config.XM_URL.format(periodo=periodo)    # reemplaza {periodo} por hourly o daily
    filas = []                                     # aqui se juntan las filas de todas las ventanas
    for inicio, fin in ventanas(config.FECHA_INICIO, config.FECHA_FIN, config.XM_MAX_DIAS):
        # cuerpo del pedido a la API de XM:
        # str(inicio) convierte la fecha en texto "2026-01-01", como la pide XM.
        cuerpo = {"MetricId": metrica, "Entity": entidad,
                  "StartDate": str(inicio), "EndDate": str(fin), "Filter": []}
        respuesta = http_json("POST", url, json=cuerpo)          # envia el pedido con POST
        nuevas = aplanar(respuesta, periodo)                     # JSON anidado -> filas
        filas.extend(nuevas)           
                                  # agrega las filas de esta ventana
        log(f"   {metrica}/{entidad} {inicio} a {fin}: {len(nuevas)} filas")
    guardar_bronce(pd.DataFrame(filas), nombre, fuente="XM",
                   origen=f"{url} MetricId={metrica} Entity={entidad}")


def extraer(forzar: bool = False) -> None:
    """Descarga todas las metricas de XM definidas en config.XM_METRICAS."""
    log("XM - API REST del mercado electrico")
    # Cada elemento de XM_METRICAS es una tupla de 4 valores;
    # el for la desempaca en 4 variables a la vez.
    for metrica, entidad, periodo, nombre in config.XM_METRICAS:
        if periodo == "lists":                     
            extraer_lista(metrica, entidad, nombre, forzar) # catalogo: otra forma de pedir
        else:                                      
            extraer_metrica(metrica, entidad, periodo, nombre, forzar) # serie de tiempo: por ventanas de 30 dias


# ---------------------------------------------------------------------------
# Este bloque solo se ejecuta cuando se corre ESTE archivo directamente:
#     python -m src.extract.xm
# Cuando otro archivo lo importa (como pipeline.py), este bloque NO se ejecuta.
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import sys      # sys.argv: lista con lo que se escribio en el comando
    extraer(forzar="--forzar" in sys.argv)   # True si el comando trae --forzar
