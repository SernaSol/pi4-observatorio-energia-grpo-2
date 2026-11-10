
"""Limpieza de DIVIPOLA del DANE para la capa plata."""

import pandas as pd
import pandera.pandas as pa
from pandera.pandas import Column, Check

from src import config


ESQUEMA_DIVIPOLA = pa.DataFrameSchema(
    {
        "cod_dpto": Column(str, Check.str_matches(r"^\d{2}$")),
        "dpto": Column(str, Check.str_length(min_value=1)),
        "cod_mpio": Column(str, Check.str_matches(r"^\d{5}$")),
        "nom_mpio": Column(str, Check.str_length(min_value=1)),
        "tipo_municipio": Column(str, nullable=True),
        "longitud": Column(float, Check.in_range(-180, 180)),
        "latitud": Column(float, Check.in_range(-90, 90)),
    },
    unique=["cod_mpio"],
    strict=True,
)


def main():
    bronce = pd.read_parquet(
        config.DIR_BRONZE / "dane_divipola.parquet"
    )

    columnas = [
        "cod_dpto", "dpto", "cod_mpio", "nom_mpio",
        "tipo_municipio", "longitud", "latitud"
    ]

    df = bronce[columnas].copy()

    # Limpiar textos, conservando ceros iniciales.
    for columna in columnas[:5]:
        df[columna] = (
            df[columna].astype("string")
            .str.strip()
            .replace("", pd.NA)
        )

    for columna in ["dpto", "nom_mpio", "tipo_municipio"]:
        df[columna] = df[columna].str.upper()

    # Convertir coordenadas con coma decimal.
    for columna in ["longitud", "latitud"]:
        df[columna] = pd.to_numeric(
            df[columna].astype("string")
            .str.replace(",", ".", regex=False),
            errors="coerce",
        ).astype("float64")

    # Detectar codigos repetidos.
    duplicados = df.duplicated(
        subset=["cod_mpio"], keep="first"
    )

    # Detectar campos y codigos invalidos.
    obligatorias = [
        "cod_dpto", "dpto", "cod_mpio",
        "nom_mpio", "longitud", "latitud"
    ]

    invalidos = (
        df[obligatorias].isna().any(axis=1)
        | ~df["cod_dpto"].str.fullmatch(r"\d{2}").fillna(False)
        | ~df["cod_mpio"].str.fullmatch(r"\d{5}").fillna(False)
        | ~df["latitud"].between(-90, 90)
        | ~df["longitud"].between(-180, 180)
        | ~(
            df["cod_mpio"].str[:2] == df["cod_dpto"]
        ).fillna(False)
    )

    # Separar registros limpios y cuarentena.
    df["motivo_cuarentena"] = ""

    df.loc[invalidos, "motivo_cuarentena"] = "Dato invalido"
    df.loc[
        duplicados & ~invalidos,
        "motivo_cuarentena"
    ] = "Codigo duplicado"

    cuarentena = df.loc[
        df["motivo_cuarentena"] != ""
    ].copy()

    limpias = df.loc[
        df["motivo_cuarentena"] == ""
    ].drop(columns="motivo_cuarentena").copy()

    # Validar antes de guardar.
    ESQUEMA_DIVIPOLA.validate(limpias, lazy=True)

    config.DIR_SILVER.mkdir(parents=True, exist_ok=True)

    limpias.to_parquet(
        config.DIR_SILVER / "dane_divipola.parquet",
        index=False,
    )

    cuarentena.to_parquet(
        config.DIR_SILVER / "dane_divipola_cuarentena.parquet",
        index=False,
    )

    assert len(limpias) + len(cuarentena) == len(bronce)

    print("\n========== DIVIPOLA DANE ==========")
    print("Originales:", len(bronce))
    print("Limpios:", len(limpias))
    print("Cuarentena:", len(cuarentena))
    print("Pandera: OK")

    print("\nEjemplo:")
    print(
        limpias[["cod_mpio", "nom_mpio", "latitud", "longitud"]]
        .head(5).to_string(index=False)
    )


if __name__ == "__main__":
    main()
