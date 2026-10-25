
"""
Fuente 5 - DIVIPOLA del DANE (Division Politico-Administrativa).

Contiene los codigos de departamentos y municipios de Colombia,
sus nombres y coordenadas geograficas.

Se utiliza para complementar los datos del IDEAM y facilitar
analisis geograficos de precipitacion y temperatura.

Los datos se guardan en la capa bronce sin limpieza.
"""

# ---------------------------------------------------------------------------
# IMPORTS
# ---------------------------------------------------------------------------
import pandas as pd

from src import config
from src.utils import guardar_bronce, http_json, log, ya_existe


# ---------------------------------------------------------------------------
# EXTRACCION
# ---------------------------------------------------------------------------
def extraer(forzar: bool = False) -> None:
    """Descarga el catalogo DIVIPOLA y lo guarda en bronce."""

    nombre = config.DIVIPOLA_NOMBRE

    log("DANE - Catalogo DIVIPOLA")

    # No repetir la descarga si ya existe el Parquet.
    if ya_existe(nombre, forzar):
        return

    # El catalogo tiene aproximadamente 1122 registros.
    # Solicitamos hasta 5000 para recuperar todos los municipios.
    parametros = {
        "$limit": 5000,
        "$order": "cod_mpio"
    }

    datos = http_json(
        "GET",
        config.DIVIPOLA_URL,
        params=parametros
    )

    # Validar la respuesta antes de guardarla.
    if not isinstance(datos, list):
        raise ValueError("DIVIPOLA devolvio una respuesta inesperada")

    if not datos:
        raise ValueError("DIVIPOLA no devolvio registros")

    # Construir tabla sin transformar los valores.
    df = pd.DataFrame(datos)

    # Verificar columnas principales del catalogo.
    columnas = {"cod_dpto", "dpto", "cod_mpio", "nom_mpio"}

    faltantes = columnas - set(df.columns)

    if faltantes:
        raise ValueError(
            f"Faltan columnas en DIVIPOLA: {faltantes}"
        )

    log(f"   DIVIPOLA: {len(df)} registros obtenidos")

    # Guardar datos originales en bronce.
    guardar_bronce(
        df,
        nombre,
        fuente="DANE",
        origen=config.DIVIPOLA_URL
    )


# ---------------------------------------------------------------------------
# EJECUCION DIRECTA
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import sys

    extraer(forzar="--forzar" in sys.argv)
