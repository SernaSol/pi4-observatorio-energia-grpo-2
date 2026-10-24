from datetime import date

from src import config
from src.extract.ideam import consulta_soql


def test_consulta_soql_temperatura():
    """Verifica que la temperatura se agregue en Socrata."""

    agregacion = config.IDEAM_DATASETS[1][2]

    parametros = consulta_soql(
        agregacion,
        date(2025, 1, 1),
        date(2025, 1, 7),
        0
    )

    assert "avg(valorobservado)" in parametros["$select"]
    assert "min(valorobservado)" in parametros["$select"]
    assert "max(valorobservado)" in parametros["$select"]

    assert "$group" in parametros
    assert "$where" in parametros

    assert "ANTIOQUIA" in parametros["$where"]
    assert parametros["$limit"] == 50000
