
"""
EA2 - Ejecucion reproducible de la capa plata.

Uso desde la raiz del proyecto:
    python -m src.transformar

Ejecuta las limpiezas, validaciones Pandera
y genera los archivos Parquet de la capa plata.
"""

from src import config
from src.silver import divipola, enerandes, ideam, noaa, xm


# Archivos de bronce necesarios para la transformacion.
ARCHIVOS_BRONCE = [
    "dane_divipola",
    "enerandes_ventas_2023",
    "enerandes_ventas_2024",
    "enerandes_ventas_2025",
    "enerandes_ventas_2026",
    "ideam_precipitacion_diaria",
    "ideam_temperatura_diaria",
    "noaa_oni",
    "xm_precio_bolsa",
    "xm_demanda",
    "xm_generacion_recurso",
    "xm_embalses",
    "xm_aportes_hidricos",
    "xm_listado_recursos",
]


def main():
    print("\n========== CAPA PLATA EA2 ==========")

    # 1. Comprobar que existen todos los insumos.
    faltantes = [
        nombre
        for nombre in ARCHIVOS_BRONCE
        if not (
            config.DIR_BRONZE / f"{nombre}.parquet"
        ).exists()
    ]

    if faltantes:
        raise FileNotFoundError(
            "Faltan archivos en data/bronze/: "
            + ", ".join(faltantes)
            + ". Ejecuta primero python -m src.pipeline"
        )

    config.DIR_SILVER.mkdir(
        parents=True,
        exist_ok=True,
    )

    # 2. Ejecutar las limpiezas en el orden correcto.
    procesos = [
        ("DIVIPOLA", divipola.main),
        ("EnerAndes", enerandes.main),
        ("IDEAM", ideam.main),
        ("NOAA", noaa.main),
        ("XM", xm.main),
    ]

    for nombre, proceso in procesos:
        print(f"\n========== {nombre} ==========")
        proceso()
        print(f"{nombre}: FINALIZADO CORRECTAMENTE")

    print("\n====================================")
    print("CAPA PLATA COMPLETADA")
    print("Validaciones Pandera ejecutadas")
    print("====================================")


if __name__ == "__main__":
    main()
