
"""
Genera muestras CSV de los archivos de la capa bronce.

- Lee todos los archivos Parquet de data/bronze.
- Extrae las primeras 200 filas.
- Guarda cada muestra en data/sample.
- No modifica los archivos originales.
"""

import pandas as pd

from src import config
from src.utils import log


def generar_muestras() -> None:
    """Genera una muestra CSV por cada archivo Parquet."""

    origen = config.DIR_BRONZE
    destino = config.RAIZ / "data" / "sample"

    destino.mkdir(parents=True, exist_ok=True)

    archivos = sorted(origen.glob("*.parquet"))

    if not archivos:
        raise FileNotFoundError(
            "No se encontraron archivos Parquet en data/bronze"
        )

    log("Generando muestras CSV de la capa bronce")

    for archivo in archivos:

        # Leer las primeras 200 filas del Parquet.
        df = pd.read_parquet(archivo).head(200)

        # Crear un CSV con el mismo nombre del Parquet.
        salida = destino / f"{archivo.stem}.csv"

        df.to_csv(
            salida,
            index=False,
            encoding="utf-8-sig"
        )

        log(
            f"   {salida.name}: "
            f"{len(df)} filas x {df.shape[1]} columnas"
        )

    log("Muestras CSV generadas correctamente")


if __name__ == "__main__":
    generar_muestras()
