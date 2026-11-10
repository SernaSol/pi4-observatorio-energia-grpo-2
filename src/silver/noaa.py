
"""Limpieza NOAA: indice ONI y clasificacion ENSO."""

import pandas as pd

from src import config
from src.quality.esquemas import ESQUEMA_NOAA_ONI


# Mes central de cada trimestre movil.
MESES_CENTRALES = {
    "DJF": 1,
    "JFM": 2,
    "FMA": 3,
    "MAM": 4,
    "AMJ": 5,
    "MJJ": 6,
    "JJA": 7,
    "JAS": 8,
    "ASO": 9,
    "SON": 10,
    "OND": 11,
    "NDJ": 12,
}


def main():
    # 1. Leer bronce.
    df = pd.read_parquet(
        config.DIR_BRONZE / "noaa_oni.parquet"
    ).copy()

    # 2. Normalizar trimestre, año y ONI.
    df["trimestre_movil"] = (
        df["SEAS"].astype("string").str.strip().str.upper()
    )

    df["anio"] = pd.to_numeric(
        df["YR"], errors="coerce"
    ).astype("Int64")

    df["mes"] = df["trimestre_movil"].map(MESES_CENTRALES)

    df["oni"] = pd.to_numeric(
        df["ANOM"], errors="coerce"
    )

    # 3. Asignar cada trimestre a su mes central.
    df["fecha"] = pd.to_datetime(
        df["anio"].astype("string")
        + "-"
        + df["mes"].astype("Int64").astype("string").str.zfill(2)
        + "-01",
        errors="coerce",
    )

    # 4. Clasificar el fenomeno ENSO.
    df["fase_enso"] = "Neutral"

    df.loc[df["oni"] >= 0.5, "fase_enso"] = "El Niño"
    df.loc[df["oni"] <= -0.5, "fase_enso"] = "La Niña"

    # 5. Identificar registros invalidos.
    invalidos = (
        df["fecha"].isna()
        | df["mes"].isna()
        | df["oni"].isna()
    )

    motivos = pd.Series("", index=df.index, dtype="string")
    motivos.loc[invalidos] = "Fecha, trimestre u ONI invalido"

    # Separar duplicados entre los registros validos.
    duplicados = df.loc[~invalidos].duplicated(
        subset=["fecha"], keep="first"
    )

    motivos.loc[duplicados.index[duplicados]] = "Mes duplicado"

    columnas = [
        "fecha", "anio", "mes",
        "trimestre_movil", "oni", "fase_enso"
    ]

    limpias = df.loc[motivos == "", columnas].copy()

    cuarentena = df.loc[motivos != "", columnas].copy()
    cuarentena["motivo_cuarentena"] = motivos.loc[
        motivos != ""
    ]

    # 6. Preparar tipos y validar.
    limpias["anio"] = limpias["anio"].astype("int64")
    limpias["mes"] = limpias["mes"].astype("int64")
    limpias["oni"] = limpias["oni"].astype("float64")

    ESQUEMA_NOAA_ONI.validate(limpias, lazy=True)

    # 7. Guardar en plata.
    config.DIR_SILVER.mkdir(parents=True, exist_ok=True)

    limpias = limpias.sort_values("fecha")

    limpias.to_parquet(
        config.DIR_SILVER / "noaa_oni.parquet",
        index=False,
    )

    cuarentena.to_parquet(
        config.DIR_SILVER / "noaa_oni_cuarentena.parquet",
        index=False,
    )

    assert len(limpias) + len(cuarentena) == len(df)

    print("\n========== NOAA ONI ==========")
    print("Originales:", len(df))
    print("Limpios:", len(limpias))
    print("Cuarentena:", len(cuarentena))
    print("Pandera: OK")

    print("\nFASES ENSO:")
    print(limpias["fase_enso"].value_counts().to_string())

    print("\nPRIMEROS REGISTROS:")
    print(limpias.head(5).to_string(index=False))


if __name__ == "__main__":
    main()
