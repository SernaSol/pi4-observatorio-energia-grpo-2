
from datetime import date

from src.utils import ventanas, ya_existe


def test_ventanas_divide_rango_correctamente():
    """Verifica que las ventanas cubran todo el rango."""

    resultado = list(
        ventanas(date(2025, 1, 1), date(2025, 1, 15), 7)
    )

    esperado = [
        (date(2025, 1, 1), date(2025, 1, 7)),
        (date(2025, 1, 8), date(2025, 1, 14)),
        (date(2025, 1, 15), date(2025, 1, 15)),
    ]

    assert resultado == esperado


def test_ya_existe_omite_archivo_descargado(tmp_path, monkeypatch):
    """Verifica que un archivo existente no se descargue otra vez."""

    from src import config

    monkeypatch.setattr(config, "DIR_BRONZE", tmp_path)

    archivo = tmp_path / "prueba.parquet"
    archivo.touch()

    assert ya_existe("prueba", forzar=False) is True
    assert ya_existe("prueba", forzar=True) is False
