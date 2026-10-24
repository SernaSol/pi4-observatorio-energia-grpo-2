from src.extract.xm import aplanar


def test_aplanar_json_hourly():
    """Verifica la conversion de JSON horario de XM."""

    respuesta = {
        "Items": [
            {
                "Date": "2025-01-01",
                "HourlyEntities": [
                    {
                        "Id": "Sistema",
                        "Values": {
                            "Hour01": 100,
                            "Hour02": 150
                        }
                    }
                ]
            }
        ]
    }

    resultado = aplanar(respuesta, "hourly")

    assert len(resultado) == 1
    assert resultado[0]["Date"] == "2025-01-01"
    assert resultado[0]["Id"] == "Sistema"
    assert resultado[0]["Hour01"] == 100
    assert resultado[0]["Hour02"] == 150
