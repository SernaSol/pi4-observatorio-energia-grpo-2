
"""
Carga de datos de la capa oro para el dashboard EA3.
Responsable: BI Analyst / Storyteller.
"""

from pathlib import Path
import pandas as pd
import streamlit as st

# Ruta principal del proyecto
RAIZ = Path(__file__).resolve().parent.parent
CARPETA_ORO = RAIZ / "data" / "gold"


@st.cache_data
def cargar_tabla(nombre: str) -> pd.DataFrame:
    """Carga una tabla Parquet de la capa oro."""

    archivo = CARPETA_ORO / f"{nombre}.parquet"

    if not archivo.exists():
        raise FileNotFoundError(
            f"No existe {archivo}. "
            "Ejecuta primero python -m src.exportar_oro"
        )

    return pd.read_parquet(archivo)


def cargar_datos() -> dict[str, pd.DataFrame]:
    """Carga las tablas necesarias para el dashboard."""

    tablas = [
        "dim_fecha",
        "dim_mes",
        "dim_municipio",
        "dim_recurso",
        "dim_segmento",
        "fact_ventas_mensual",
        "fact_mercado_mensual",
        "fact_generacion_mensual",
        "fact_indicadores_hidricos",
        "fact_clima_mensual",
    ]

    return {
        nombre: cargar_tabla(nombre)
        for nombre in tablas
    }
