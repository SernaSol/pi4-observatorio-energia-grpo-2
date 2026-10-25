
"""
Perfilamiento automatico de la capa bronce.

Genera docs/perfilamiento.md con:
- Numero de filas y columnas.
- Tipos de datos.
- Porcentaje de nulos por columna.
- Filas duplicadas.
- Rango de fechas.
- Hallazgos candidatos con evidencia numerica.

No modifica los datos originales.
"""

from pathlib import Path

import pandas as pd

from src import config
from src.utils import log


# Columnas que pueden representar fechas en las diferentes fuentes
COLUMNAS_FECHA = [
    "Date",
    "fecha",
    "fechaobservacion",
    "Fecha",
    "FECHA",
    "date",
]


def obtener_rango_fechas(df: pd.DataFrame) -> str:
    """Identifica el rango de fechas de un archivo."""

    for columna in COLUMNAS_FECHA:
        if columna not in df.columns:
            continue

        fechas = pd.to_datetime(
            df[columna],
            errors="coerce"
        )

        fechas = fechas.dropna()

        if not fechas.empty:
            return (
                f"{fechas.min().date()} "
                f"a {fechas.max().date()}"
            )

    return "No aplica / requiere interpretacion"


def perfilar_archivo(archivo: Path) -> tuple[str, dict]:
    """Genera el perfil de un archivo Parquet."""

    df = pd.read_parquet(archivo)

    filas = len(df)
    columnas = len(df.columns)
    duplicadas = int(df.duplicated().sum())

    # Calcular nulos por columna.
    if filas:
        nulos = df.isna().mean() * 100
    else:
        nulos = pd.Series(0.0, index=df.columns)

    rango = obtener_rango_fechas(df)

    lineas = [
        f"## {archivo.name}",
        "",
        f"- **Filas:** {filas:,}",
        f"- **Columnas:** {columnas}",
        f"- **Filas duplicadas:** {duplicadas:,}",
        f"- **Rango de fechas:** {rango}",
        "",
        "| Columna | Tipo de dato | Nulos |",
        "|---|---|---:|",
    ]

    for columna in df.columns:
        tipo = str(df[columna].dtype)
        porcentaje = nulos[columna]

        lineas.append(
            f"| `{columna}` | `{tipo}` | {porcentaje:.2f}% |"
        )

    lineas.append("")

    resumen = {
        "archivo": archivo.name,
        "filas": filas,
        "columnas": columnas,
        "duplicadas": duplicadas,
        "columnas_nulas": int((nulos > 0).sum()),
        "nulos_max": float(nulos.max()) if len(nulos) else 0.0,
        "rango": rango,
    }

    return "\n".join(lineas), resumen


def generar_perfilamiento() -> None:
    """Recorre todos los Parquet y genera el informe Markdown."""

    archivos = sorted(config.DIR_BRONZE.glob("*.parquet"))

    if not archivos:
        raise FileNotFoundError(
            "No se encontraron archivos Parquet en data/bronze/"
        )

    destino = config.RAIZ / "docs" / "perfilamiento.md"
    destino.parent.mkdir(parents=True, exist_ok=True)

    secciones = [
        "# Perfilamiento de datos - Observatorio de Energia y Clima",
        "",
        "## Objetivo",
        "",
        "Evaluar la estructura, completitud y calidad inicial de "
        "los datos almacenados en la capa bronce.",
        "",
        f"**Archivos analizados:** {len(archivos)}",
        "",
        "Los datos se analizan sin modificar los archivos originales.",
        "",
    ]

    resumenes = []

    for archivo in archivos:
        log(f"Perfilando {archivo.name}")

        seccion, resumen = perfilar_archivo(archivo)

        secciones.append(seccion)
        resumenes.append(resumen)

    # Los siguientes son candidatos, no conclusiones verificadas.
    secciones.extend([
        "## Hallazgos de calidad - Candidatos para revision",
        "",
        "Esta seccion identifica indicadores numericos. "
        "Se debe interpretar si cada caso constituye "
        "un problema real de calidad.",
        "",
    ])

    for resumen in resumenes:
        secciones.append(
            f"- **{resumen['archivo']}:** "
            f"{resumen['filas']:,} filas, "
            f"{resumen['duplicadas']:,} duplicadas exactas, "
            f"{resumen['columnas_nulas']} columnas con nulos, "
            f"maximo {resumen['nulos_max']:.2f}% de nulos."
        )

    destino.write_text(
        "\n".join(secciones),
        encoding="utf-8"
    )

    log(f"Informe generado: {destino}")


if __name__ == "__main__":
    generar_perfilamiento()
