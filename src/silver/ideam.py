
"""
Capa plata: limpieza de precipitacion y temperatura IDEAM.
Normaliza fechas, valores numericos y municipios.
Asocia las estaciones con codigos oficiales DIVIPOLA.
Valida con Pandera y guarda datos limpios y cuarentena.
"""

import unicodedata

import pandas as pd
from src.quality.esquemas import (
    ESQUEMA_IDEAM_PRECIPITACION as ESQUEMA_PRECIPITACION,
    ESQUEMA_IDEAM_TEMPERATURA as ESQUEMA_TEMPERATURA,
)

from src import config



# ---------------------------------------------------------------------------
# NORMALIZACION DE MUNICIPIOS
# ---------------------------------------------------------------------------

def normalizar_nombre(texto):
    """Quita tildes, espacios adicionales y diferencias de mayusculas."""
    if pd.isna(texto):
        return None

    texto = " ".join(str(texto).upper().split())

    return "".join(
        c for c in unicodedata.normalize("NFD", texto)
        if unicodedata.category(c) != "Mn"
    )


def asociar_divipola(df):
    """Relaciona el municipio IDEAM con el catalogo oficial DANE."""

    dane = pd.read_parquet(
        config.DIR_SILVER / "dane_divipola.parquet"
    )

    # IDEAM corresponde a estaciones de Antioquia.
    dane = dane[dane["cod_dpto"] == "05"].copy()

    dane["clave"] = dane["nom_mpio"].map(normalizar_nombre)

    # Verificar que el catalogo no tenga nombres ambiguos.
    if dane["clave"].duplicated().any():
        raise ValueError(
            "DIVIPOLA contiene municipios con nombres duplicados"
        )

    catalogo = dane.set_index("clave")

    # Conservar el nombre original para auditoria.
    df["municipio_origen"] = df["municipio"]

    claves = df["municipio"].map(normalizar_nombre)

    # Corregir la diferencia detectada entre IDEAM y DANE.
    claves = claves.replace({
        "SAN VICENTE": "SAN VICENTE FERRER",
    })

    # Asignar codigo y nombre oficial del municipio.
    df["cod_mpio"] = claves.map(
        catalogo["cod_mpio"]
    ).astype("string")

    df["municipio"] = claves.map(
        catalogo["nom_mpio"]
    ).astype("string")

    return df


# ---------------------------------------------------------------------------
# LIMPIEZA DE IDEAM
# ---------------------------------------------------------------------------

def limpiar_ideam(nombre, indicadores, esquema):
    """Limpia IDEAM, valida con Pandera y guarda los resultados."""

    df = pd.read_parquet(
        config.DIR_BRONZE / f"{nombre}.parquet"
    ).copy()

    # 1. Limpiar textos.
    for columna in ["codigoestacion", "nombreestacion", "municipio"]:
        df[columna] = (
            df[columna]
            .astype("string")
            .str.strip()
            .str.replace(r"\s+", " ", regex=True)
            .replace("", pd.NA)
        )

    df["municipio"] = df["municipio"].str.upper()

    # 2. Asociar municipios con DIVIPOLA.
    df = asociar_divipola(df)

    # 3. Convertir fechas.
    df["fecha"] = pd.to_datetime(
        df["fecha"], errors="coerce"
    ).dt.normalize()

    # 4. Convertir mediciones y coordenadas a numeros.
    for columna in indicadores + ["latitud", "longitud", "n_obs"]:
        df[columna] = pd.to_numeric(
            df[columna], errors="coerce"
        ).astype("float64")

    # 5. Identificar registros invalidos.
    obligatorias = [
        "codigoestacion",
        "nombreestacion",
        "municipio",
        "cod_mpio",
        "fecha",
        *indicadores,
    ]

    motivos = pd.Series("", index=df.index, dtype="string")

    invalidos = df[obligatorias].isna().any(axis=1)

    motivos.loc[invalidos] = (
        "Dato obligatorio invalido o municipio sin DIVIPOLA"
    )

    # 6. Reglas especificas por indicador.
    if nombre == "ideam_precipitacion_diaria":
        negativos = df["precipitacion_mm"] < 0

        motivos.loc[(motivos == "") & negativos] = (
            "Precipitacion negativa"
        )

    else:
        inconsistentes = (
            (df["temp_min_c"] > df["temp_media_c"])
            | (df["temp_media_c"] > df["temp_max_c"])
        )

        motivos.loc[(motivos == "") & inconsistentes] = (
            "Temperaturas inconsistentes"
        )

    # 7. Identificar duplicados entre registros validos.
    validos = motivos == ""

    duplicados = df.loc[validos].duplicated(
        subset=["codigoestacion", "fecha"],
        keep="first",
    )

    motivos.loc[duplicados.index[duplicados]] = (
        "Estacion y fecha duplicadas"
    )

    # 8. Separar limpios y cuarentena.
    df["motivo_cuarentena"] = motivos

    limpias = df.loc[
        df["motivo_cuarentena"] == ""
    ].drop(columns=["motivo_cuarentena"]).copy()

    cuarentena = df.loc[
        df["motivo_cuarentena"] != ""
    ].copy()

    # 9. Validar con Pandera antes de guardar.
    esquema.validate(limpias, lazy=True)

    # 10. Guardar capa plata.
    config.DIR_SILVER.mkdir(
        parents=True, exist_ok=True
    )

    limpias.to_parquet(
        config.DIR_SILVER / f"{nombre}.parquet",
        index=False,
    )

    cuarentena.to_parquet(
        config.DIR_SILVER / f"{nombre}_cuarentena.parquet",
        index=False,
    )

    assert len(limpias) + len(cuarentena) == len(df)

    # 11. Mostrar resultados.
    print(f"\n========== {nombre.upper()} ==========")
    print("Originales:", len(df))
    print("Limpios:", len(limpias))
    print("Cuarentena:", len(cuarentena))
    print("Sin DIVIPOLA en plata:", limpias["cod_mpio"].isna().sum())
    print("Pandera: OK")

    ejemplo = limpias.loc[
        limpias["municipio_origen"] == "SAN VICENTE",
        ["municipio_origen", "municipio", "cod_mpio"],
    ].drop_duplicates()

    if not ejemplo.empty:
        print("\nMunicipio corregido:")
        print(ejemplo.to_string(index=False))


# ---------------------------------------------------------------------------
# PROGRAMA PRINCIPAL
# ---------------------------------------------------------------------------

def main():
    limpiar_ideam(
        "ideam_precipitacion_diaria",
        ["precipitacion_mm"],
        ESQUEMA_PRECIPITACION,
    )

    limpiar_ideam(
        "ideam_temperatura_diaria",
        ["temp_media_c", "temp_min_c", "temp_max_c"],
        ESQUEMA_TEMPERATURA,
    )

    print("\nLIMPIEZA DE IDEAM FINALIZADA")


if __name__ == "__main__":
    main()
