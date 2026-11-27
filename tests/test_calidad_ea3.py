
"""
Pruebas de calidad de datos - Evidencia 3.
Responsable: Data Quality Analyst.
"""

from datetime import date
from pathlib import Path

import duckdb
import pytest


RAIZ = Path(__file__).resolve().parents[1]
RUTA_DB = RAIZ / "data" / "observatorio.duckdb"


@pytest.fixture(scope="module")
def conexion():
    """Abre la base de la capa oro para las pruebas."""

    assert RUTA_DB.exists(), (
        "No existe observatorio.duckdb. "
        "Ejecuta primero dbt build."
    )

    con = duckdb.connect(str(RUTA_DB), read_only=True)

    yield con

    con.close()


# -------------------------------------------------
# PRUEBA 1: INTEGRIDAD DEL CALENDARIO
# -------------------------------------------------

def test_calendario_sin_fechas_duplicadas(conexion):
    total, distintas, nulas, inicio, fin = conexion.execute(
        """
        SELECT
            COUNT(*),
            COUNT(DISTINCT fecha),
            COUNT(*) - COUNT(fecha),
            MIN(fecha),
            MAX(fecha)
        FROM main.dim_fecha
        """
    ).fetchone()

    assert total > 0
    assert total == distintas, "Hay fechas duplicadas"
    assert nulas == 0, "Hay fechas nulas"

    # Cobertura historica necesaria para EA3
    assert inicio <= date(2015, 1, 1)
    assert fin >= date(2026, 9, 30)


# -------------------------------------------------
# PRUEBA 2: CALCULO DE INDICADORES HIDRICOS
# -------------------------------------------------

def test_porcentaje_aportes_hidricos_correcto(conexion):
    total, calculados, incorrectos = conexion.execute(
        """
        SELECT
            COUNT(*),

            COUNT(porcentaje_aportes_vs_media),

            COUNT(*) FILTER (
                WHERE porcentaje_aportes_vs_media IS NOT NULL
                AND (
                    valor_aportes IS NULL
                    OR aportes_media_historica IS NULL
                    OR aportes_media_historica <= 0
                    OR ABS(
                        porcentaje_aportes_vs_media
                        - ROUND(
                            100.0 * valor_aportes
                            / NULLIF(aportes_media_historica, 0),
                            2
                        )
                    ) > 0.01
                )
            )

        FROM main.fact_indicadores_hidricos
        """
    ).fetchone()

    assert total > 0
    assert calculados > 0, "No hay porcentajes calculados"
    assert incorrectos == 0, (
        f"Hay {incorrectos} porcentajes incorrectos"
    )


# -------------------------------------------------
# PRUEBA 3: GRANULARIDAD DE DATOS CLIMATICOS
# -------------------------------------------------

def test_clima_sin_duplicados_por_mes_municipio(conexion):
    total, combinaciones, incompletos = conexion.execute(
        """
        SELECT
            COUNT(*),
            COUNT(DISTINCT (mes, cod_mpio)),
            COUNT(*) FILTER (
                WHERE mes IS NULL OR cod_mpio IS NULL
            )
        FROM main.fact_clima_mensual
        """
    ).fetchone()

    assert total > 0
    assert incompletos == 0, (
        "Hay registros climaticos sin mes o municipio"
    )
    assert total == combinaciones, (
        "Existen duplicados por mes y municipio"
    )
