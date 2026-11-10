
"""Pruebas nuevas de las reglas de limpieza de la EA2."""

import pandas as pd
import pytest
from pandera.errors import SchemaErrors

from src.silver.enerandes import (
    normalizar_periodo,
    normalizar_fechas_y_energia,
    normalizar_municipios,
    separar_calidad,
)
from src.silver.xm import (
    transformar_horario,
    consolidar_mercado_horario,
)
from src.quality.esquemas import ESQUEMA_MERCADO_HORARIO


# 1. Conversion de MWh a kWh.
def test_conversion_mwh_a_kwh():
    datos = pd.DataFrame({
        "periodo": ["jun-24"],
        "energia_kwh": ["2.5"],
        "unidad": ["MWh"],
    })

    resultado = normalizar_fechas_y_energia(datos)

    assert resultado["energia_kwh"].iloc[0] == 2500
    assert resultado["unidad"].iloc[0] == "kWh"


# 2. Fechas de EnerAndes en formatos diferentes.
def test_fechas_enerandes():
    assert normalizar_periodo("mar-24") == "2024-03"
    assert normalizar_periodo("03/2024") == "2024-03"
    assert normalizar_periodo("jan-24") == "2024-01"


# 3. XM: convertir 24 columnas en 24 filas.
def test_xm_transformacion_24_horas():
    fila = {
        "Date": "2024-01-01",
        "Id": "Sistema",
        "code": "Sistema",
    }

    for hora in range(1, 25):
        fila[f"Hour{hora:02d}"] = str(hora * 10)

    bronce = pd.DataFrame([fila])

    resultado = transformar_horario(bronce, "precio_bolsa")

    assert len(resultado) == 24
    assert resultado["hora"].tolist() == list(range(1, 25))
    assert resultado["precio_bolsa"].iloc[0] == 10
    assert resultado["precio_bolsa"].iloc[-1] == 240


# 4. XM: unir precio de bolsa y demanda correctamente.
def test_xm_consolidacion_mercado():
    base = {
        "Date": "2024-01-01",
        "Id": "Sistema",
        "code": "Sistema",
    }

    precio = pd.DataFrame([{
        **base,
        **{f"Hour{h:02d}": "100" for h in range(1, 25)},
    }])

    demanda = pd.DataFrame([{
        **base,
        **{f"Hour{h:02d}": "5000" for h in range(1, 25)},
    }])

    resultado = consolidar_mercado_horario(precio, demanda)

    assert len(resultado) == 24
    assert (resultado["precio_bolsa"] == 100).all()
    assert (resultado["demanda"] == 5000).all()


# 5. EnerAndes: enviar energia invalida a cuarentena.
def test_energia_invalida_en_cuarentena():
    datos = pd.DataFrame({
        "periodo": ["2024-01", "2024-02", "2024-03"],
        "divipola": ["05001"] * 3,
        "segmento": ["Residencial"] * 3,
        "tipo_compra": ["Bolsa"] * 3,
        "energia_kwh": [100, -50, None],
        "valor_cop": [1000, 2000, 3000],
        "clientes": [10, 10, 10],
    })

    limpias, cuarentena, _ = separar_calidad(datos)

    assert len(limpias) == 1
    assert len(cuarentena) == 2
    assert (limpias["energia_kwh"] >= 0).all()
    assert cuarentena["motivo_cuarentena"].str.contains(
        "Energia"
    ).all()


# 6. EnerAndes: normalizar nombres y codigos DIVIPOLA.
def test_normalizacion_municipios():
    datos = pd.DataFrame({
        "municipio": ["Rio Negro", "Medellín D.E."],
    })

    resultado = normalizar_municipios(datos)

    assert resultado["municipio"].tolist() == [
        "Rionegro", "Medellín"
    ]
    assert resultado["divipola"].tolist() == [
        "05615", "05001"
    ]


# 7. Pandera: rechazar precios de bolsa negativos.
def test_pandera_rechaza_precio_negativo():
    datos = pd.DataFrame({
        "fecha": ["2024-01-01"],
        "hora": [1],
        "entidad": ["Sistema"],
        "codigo": ["Sistema"],
        "precio_bolsa": [-100.0],
        "demanda": [5000.0],
    })

    with pytest.raises(SchemaErrors):
        ESQUEMA_MERCADO_HORARIO.validate(
            datos, lazy=True
        )
