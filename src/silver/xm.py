
"""
Capa plata: transformacion de los datos horarios de XM.

Convierte las columnas Hour01 a Hour24 en registros
individuales por fecha y hora.

No elimina registros: primero transforma y despues
permite identificar problemas de calidad.
"""

import pandas as pd


HORAS_XM = [f"Hour{hora:02d}" for hora in range(1, 25)]

LINAJE = ["_fuente", "_origen", "_extraido_en"]


def transformar_horario(bronce: pd.DataFrame, nombre_valor: str) -> pd.DataFrame:
    """
    Convierte una tabla de XM del formato ancho al formato largo.

    Ejemplo:
        Date        Hour01  Hour02
        2024-01-01  250     300

    Resultado:
        fecha       hora  valor
        2024-01-01  1     250
        2024-01-01  2     300
    """
    faltantes = [col for col in HORAS_XM if col not in bronce.columns]

    if faltantes:
        raise ValueError(
            f"Faltan columnas horarias de XM: {faltantes}"
        )

    # Conservar identificadores y columnas de trazabilidad.
    identificadores = ["Date", "Id", "code"]
    identificadores += [
        col for col in LINAJE if col in bronce.columns
    ]

    # Pasar de 24 columnas horarias a una sola columna de valores.
    df = bronce.melt(
        id_vars=identificadores,
        value_vars=HORAS_XM,
        var_name="hora_original",
        value_name=nombre_valor,
    )

    # Estandarizar nombres de columnas.
    df = df.rename(
        columns={
            "Date": "fecha",
            "Id": "entidad",
            "code": "codigo",
        }
    )

    # Hour01 -> 1, Hour02 -> 2, ..., Hour24 -> 24.
    df["hora"] = (
        df["hora_original"]
        .str.replace("Hour", "", regex=False)
        .astype(int)
    )

    # Convertir la fecha al formato AAAA-MM-DD.
    df["fecha"] = (
        pd.to_datetime(df["fecha"], errors="coerce")
        .dt.strftime("%Y-%m-%d")
    )

    # Convertir los valores que llegaron como texto a numeros.
    df[nombre_valor] = pd.to_numeric(
        df[nombre_valor],
        errors="coerce",
    )

    # Ya no necesitamos la columna Hour01, Hour02, etc.
    df = df.drop(columns=["hora_original"])

    # Ordenar por fecha y hora.
    df = df.sort_values(
        ["fecha", "hora", "entidad", "codigo"]
    ).reset_index(drop=True)

    return df



def consolidar_mercado_horario(
    bronce_precio: pd.DataFrame,
    bronce_demanda: pd.DataFrame,
) -> pd.DataFrame:
    """
    Une precio de bolsa y demanda de XM por fecha,
    hora, entidad y codigo.

    Verifica que no existan duplicados ni registros
    sin correspondencia entre las dos fuentes.
    """

    precio = transformar_horario(
        bronce_precio, "precio_bolsa"
    )

    demanda = transformar_horario(
        bronce_demanda, "demanda"
    )

    claves = ["fecha", "hora", "entidad", "codigo"]

    # Verificar claves antes de unir.
    for nombre, tabla in [
        ("precio_bolsa", precio),
        ("demanda", demanda),
    ]:
        if tabla[claves].isna().any().any():
            raise ValueError(
                f"{nombre}: existen claves vacias"
            )

        if tabla.duplicated(subset=claves).any():
            raise ValueError(
                f"{nombre}: existen claves duplicadas"
            )

    # Unir ambas fuentes sin descartar registros.
    mercado = precio[
        claves + ["precio_bolsa"]
    ].merge(
        demanda[claves + ["demanda"]],
        on=claves,
        how="outer",
        validate="one_to_one",
        indicator=True,
    )

    # Comprobar que cada precio tenga su demanda
    # y cada demanda tenga su precio.
    sin_correspondencia = mercado["_merge"] != "both"

    if sin_correspondencia.any():
        raise ValueError(
            "XM: hay "
            f"{int(sin_correspondencia.sum())} "
            "registros sin correspondencia entre "
            "precio y demanda"
        )

    mercado = mercado.drop(columns=["_merge"])

    # Ordenar los registros cronologicamente.
    mercado = mercado.sort_values(
        ["fecha", "hora", "entidad", "codigo"]
    ).reset_index(drop=True)

    return mercado



def procesar_generacion_por_lotes(tamano_lote=1000):
    """
    Procesa la generacion horaria de XM por lotes.
    Valida cada lote con Pandera y escribe dos Parquet:
    registros limpios y registros en cuarentena.
    """
    import pyarrow as pa
    import pyarrow.parquet as pq

    from src import config
    from src.quality.esquemas import ESQUEMA_GENERACION_RECURSO

    origen = config.DIR_BRONZE / "xm_generacion_recurso.parquet"
    config.DIR_SILVER.mkdir(parents=True, exist_ok=True)

    ruta_limpias = config.DIR_SILVER / "xm_generacion_recurso.parquet"
    ruta_cuarentena = config.DIR_SILVER / "xm_generacion_cuarentena.parquet"

    # Archivos temporales para evitar dejar resultados incompletos.
    tmp_limpias = config.DIR_SILVER / "xm_generacion_recurso.tmp.parquet"
    tmp_cuarentena = config.DIR_SILVER / "xm_generacion_cuarentena.tmp.parquet"

    esquema_limpias = pa.schema([
        ("fecha", pa.string()),
        ("hora", pa.int64()),
        ("entidad", pa.string()),
        ("codigo", pa.string()),
        ("generacion", pa.float64()),
    ])

    esquema_cuarentena = (
        esquema_limpias
        .append(pa.field("valor_original", pa.string()))
        .append(pa.field("motivo_cuarentena", pa.string()))
    )

    conteos = {
        "procesados": 0,
        "limpios": 0,
        "cuarentena": 0,
        "vacios": 0,
        "negativos": 0,
        "ceros_validos": 0,
    }

    # Permite detectar duplicados incluso entre lotes distintos.
    claves_vistas = set()

    print("\nIniciando XM: generacion por recurso")

    try:
        with (
            pq.ParquetWriter(
                tmp_limpias, esquema_limpias, compression="snappy"
            ) as escritor_limpias,
            pq.ParquetWriter(
                tmp_cuarentena, esquema_cuarentena, compression="snappy"
            ) as escritor_cuarentena,
        ):
            lector = pq.ParquetFile(origen)

            for numero, lote in enumerate(
                lector.iter_batches(batch_size=tamano_lote),
                start=1,
            ):
                bronce = lote.to_pandas()

                # Verificar duplicados diarios dentro y entre lotes.
                claves = list(
                    bronce[["Date", "Id", "code"]]
                    .itertuples(index=False, name=None)
                )
                claves_lote = set(claves)

                if (
                    len(claves_lote) != len(claves)
                    or not claves_vistas.isdisjoint(claves_lote)
                ):
                    raise ValueError(
                        "Hay fechas y recursos duplicados en bronce"
                    )

                claves_vistas.update(claves_lote)

                # Pasar de Hour01...Hour24 a una fila por hora.
                df = bronce.melt(
                    id_vars=["Date", "Id", "code"],
                    value_vars=HORAS_XM,
                    var_name="hora_original",
                    value_name="valor_original",
                )

                df = df.rename(columns={
                    "Date": "fecha",
                    "Id": "entidad",
                    "code": "codigo",
                })

                df["fecha"] = (
                    pd.to_datetime(df["fecha"], errors="coerce")
                    .dt.strftime("%Y-%m-%d")
                )

                df["hora"] = (
                    df["hora_original"]
                    .str.replace("Hour", "", regex=False)
                    .astype("int64")
                )

                # No continuar si falta una clave esencial.
                if df[["fecha", "entidad", "codigo"]].isna().any().any():
                    raise ValueError(
                        "Hay fechas o identificadores invalidos"
                    )

                # Conservar el dato original antes de convertirlo.
                df["valor_original"] = df["valor_original"].astype("string")

                df["generacion"] = pd.to_numeric(
                    df["valor_original"], errors="coerce"
                ).astype("float64")

                vacios = df["generacion"].isna()
                negativos = df["generacion"] < 0
                invalidos = vacios | negativos

                columnas = [
                    "fecha", "hora", "entidad", "codigo", "generacion"
                ]

                limpias = df.loc[
                    ~invalidos, columnas
                ].copy()

                cuarentena = df.loc[
                    invalidos, columnas + ["valor_original"]
                ].copy()

                cuarentena["motivo_cuarentena"] = (
                    "Generacion vacia o no numerica"
                )

                cuarentena.loc[
                    cuarentena["generacion"] < 0,
                    "motivo_cuarentena",
                ] = "Generacion negativa"

                # Validar antes de escribir en plata.
                if not limpias.empty:
                    ESQUEMA_GENERACION_RECURSO.validate(
                        limpias, lazy=True
                    )

                    tabla_limpias = pa.Table.from_pandas(
                        limpias,
                        schema=esquema_limpias,
                        preserve_index=False,
                    )
                    escritor_limpias.write_table(tabla_limpias)

                if not cuarentena.empty:
                    tabla_cuarentena = pa.Table.from_pandas(
                        cuarentena,
                        schema=esquema_cuarentena,
                        preserve_index=False,
                    )
                    escritor_cuarentena.write_table(tabla_cuarentena)

                conteos["procesados"] += len(df)
                conteos["limpios"] += len(limpias)
                conteos["cuarentena"] += len(cuarentena)
                conteos["vacios"] += int(vacios.sum())
                conteos["negativos"] += int(negativos.sum())
                conteos["ceros_validos"] += int(
                    (limpias["generacion"] == 0).sum()
                )

                # Mostrar avance sin imprimir todos los lotes.
                if numero % 50 == 0:
                    print(
                        f"Lote {numero}: "
                        f"{conteos['procesados']:,} registros procesados"
                    )

        # Comprobar que ningun registro se haya perdido.
        assert (
            conteos["limpios"] + conteos["cuarentena"]
            == conteos["procesados"]
        )

        # Publicar los archivos solo tras terminar correctamente.
        tmp_limpias.replace(ruta_limpias)
        tmp_cuarentena.replace(ruta_cuarentena)

    except Exception:
        tmp_limpias.unlink(missing_ok=True)
        tmp_cuarentena.unlink(missing_ok=True)
        raise

    print("\n========== RESUMEN GENERACION XM ==========")
    for nombre, cantidad in conteos.items():
        print(f"{nombre}: {cantidad}")

    # Guardar metricas sin sobrescribir el reporte de EnerAndes.
    config.DIR_DOCS.mkdir(parents=True, exist_ok=True)

    reporte = [
        "# Calidad XM - Generacion por recurso",
        "",
        f"- Posiciones horarias procesadas: {conteos['procesados']}",
        f"- Registros limpios: {conteos['limpios']}",
        f"- Registros en cuarentena: {conteos['cuarentena']}",
        "",
        "| Problema | Antes | Despues en plata | Regla |",
        "|---|---:|---:|---|",
        f"| Generacion vacia o no numerica | {conteos['vacios']} | 0 | Cuarentena |",
        f"| Generacion negativa | {conteos['negativos']} | 0 | Cuarentena |",
        f"| Generacion igual a cero | {conteos['ceros_validos']} | {conteos['ceros_validos']} | Conservar |",
        "",
        "Los valores faltantes no se reemplazan por cero.",
        "La cuarentena conserva fecha, hora, recurso, valor original y motivo.",
        "",
    ]

    (config.DIR_DOCS / "reporte_calidad_xm_generacion.md").write_text(
        "\n".join(reporte), encoding="utf-8"
    )

    print("\nValidacion Pandera por lotes: OK")
    print(f"Archivo limpio: {ruta_limpias}")
    print(f"Archivo cuarentena: {ruta_cuarentena}")

    return conteos


def transformar_diario(
    bronce: pd.DataFrame,
    nombre_valor: str,
) -> pd.DataFrame:
    """
    Normaliza las fuentes diarias de XM:
    embalses y aportes hidricos.

    Conserva los valores originales y el linaje
    para facilitar las auditorias de calidad.
    """

    requeridas = {"Date", "Id", "Value"}
    faltantes = requeridas - set(bronce.columns)

    if faltantes:
        raise ValueError(
            f"Faltan columnas de XM: {sorted(faltantes)}"
        )

    df = bronce.copy()

    # Estandarizar nombres.
    df = df.rename(columns={
        "Date": "fecha",
        "Id": "entidad",
        "Value": nombre_valor,
    })

    # Normalizar fecha.
    df["fecha"] = (
        pd.to_datetime(df["fecha"], errors="coerce")
        .dt.strftime("%Y-%m-%d")
    )

    # Normalizar entidad.
    df["entidad"] = (
        df["entidad"].astype("string").str.strip()
    )

    df["entidad"] = df["entidad"].replace("", pd.NA)

    # Conservar el dato original antes de convertirlo.
    df["valor_original"] = (
        df[nombre_valor].astype("string")
    )

    # Convertir el indicador a numero.
    df[nombre_valor] = pd.to_numeric(
        df[nombre_valor],
        errors="coerce",
    ).astype("float64")

    # Ordenar por fecha y entidad.
    df = df.sort_values(
        ["fecha", "entidad"],
        na_position="last",
    ).reset_index(drop=True)

    return df


def guardar_diarios_xm():
    """Valida y guarda embalses y aportes hidricos."""
    from src import config
    from pandera.pandas import DataFrameSchema, Column, Check

    config.DIR_SILVER.mkdir(parents=True, exist_ok=True)

    fuentes = [
        ("xm_embalses", "valor_embalse", Check.in_range(0, 1)),
        ("xm_aportes_hidricos", "valor_aportes", Check.ge(0)),
    ]

    for archivo, indicador, regla in fuentes:
        bronce = pd.read_parquet(
            config.DIR_BRONZE / f"{archivo}.parquet"
        )

        df = transformar_diario(bronce, indicador)
        df = df[["fecha", "entidad", indicador]].copy()

        esquema = DataFrameSchema(
            {
                "fecha": Column(
                    str, Check.str_matches(r"^\d{4}-\d{2}-\d{2}$")
                ),
                "entidad": Column(str, Check.str_length(min_value=1)),
                indicador: Column(float, regla),
            },
            unique=["fecha", "entidad"],
            strict=True,
        )

        esquema.validate(df, lazy=True)

        df.to_parquet(
            config.DIR_SILVER / f"{archivo}.parquet",
            index=False,
        )

        print(f"{archivo}: {len(df)} registros - Pandera OK")


def guardar_catalogo_xm():
    """Limpia, valida y guarda el catalogo de recursos de XM."""
    from src import config
    from src.quality.esquemas import ESQUEMA_CATALOGO_XM

    bronce = pd.read_parquet(
        config.DIR_BRONZE / "xm_listado_recursos.parquet"
    )

    columnas = {
        "Date": "fecha_catalogo",
        "Id": "entidad",
        "Code": "codigo_recurso",
        "Name": "nombre_recurso",
        "Type": "tipo",
        "Disp": "despacho",
        "RecType": "tipo_recurso",
        "CompanyCode": "codigo_empresa",
        "EnerSource": "fuente_energetica",
        "OperStartdate": "fecha_inicio_operacion",
        "State": "estado",
    }

    df = bronce[list(columnas)].rename(columns=columnas).copy()

    # Limpiar espacios y campos vacios.
    columnas_texto = [
        c for c in df.columns if not c.startswith("fecha_")
    ]

    for columna in columnas_texto:
        df[columna] = (
            df[columna].astype("string").str.strip().replace("", pd.NA)
        )

    # Unificar los estados.
    df["estado"] = df["estado"].str.upper()

    # Convertir fechas.
    for columna in ["fecha_catalogo", "fecha_inicio_operacion"]:
        df[columna] = pd.to_datetime(
            df[columna], errors="coerce"
        )

    # Identificar duplicados y datos obligatorios invalidos.
    duplicados = df.duplicated(
        subset=["codigo_recurso"], keep="first"
    )

    invalidos = (
        df["codigo_recurso"].isna()
        | df["nombre_recurso"].isna()
        | df["fecha_catalogo"].isna()
        | ~df["estado"].isin(["OPERACION", "PRUEBAS"])
    )

    cuarentena = df.loc[duplicados | invalidos].copy()
    cuarentena["motivo_cuarentena"] = "Dato obligatorio invalido"
    cuarentena.loc[
        duplicados, "motivo_cuarentena"
    ] = "Codigo duplicado"

    limpias = df.loc[~(duplicados | invalidos)].copy()

    # Validar antes de guardar.
    ESQUEMA_CATALOGO_XM.validate(limpias, lazy=True)

    config.DIR_SILVER.mkdir(parents=True, exist_ok=True)

    limpias.to_parquet(
        config.DIR_SILVER / "xm_listado_recursos.parquet",
        index=False,
    )

    cuarentena.to_parquet(
        config.DIR_SILVER / "xm_catalogo_cuarentena.parquet",
        index=False,
    )

    assert len(limpias) + len(cuarentena) == len(bronce)

    print("Catalogo XM - Pandera OK")
    print("Registros originales:", len(bronce))
    print("Registros limpios:", len(limpias))
    print("Cuarentena:", len(cuarentena))
    print("Estados:", limpias["estado"].value_counts().to_dict())




def main() -> None:
    """
    Ejecuta la limpieza completa de XM en la capa plata:
    - Precio de bolsa y demanda
    - Generacion por recurso
    - Embalses y aportes hidricos
    - Catalogo de plantas
    """

    from src import config
    from src.quality.esquemas import ESQUEMA_MERCADO_HORARIO

    print("Iniciando limpieza de XM: mercado horario")

    # 1. Leer precio de bolsa y demanda desde bronce.
    bronce_precio = pd.read_parquet(
        config.DIR_BRONZE / "xm_precio_bolsa.parquet"
    )

    bronce_demanda = pd.read_parquet(
        config.DIR_BRONZE / "xm_demanda.parquet"
    )

    # 2. Transformar y consolidar los indicadores horarios.
    mercado = consolidar_mercado_horario(
        bronce_precio,
        bronce_demanda,
    )

    # 3. Preparar tipos numericos.
    mercado["precio_bolsa"] = mercado["precio_bolsa"].astype(
        "float64"
    )
    mercado["demanda"] = mercado["demanda"].astype("float64")

    # 4. Validar el mercado horario con Pandera.
    ESQUEMA_MERCADO_HORARIO.validate(
        mercado,
        lazy=True,
    )

    print("Validacion Pandera mercado horario: OK")

    # 5. Guardar mercado horario en plata.
    config.DIR_SILVER.mkdir(
        parents=True,
        exist_ok=True,
    )

    ruta = config.DIR_SILVER / "xm_mercado_horario.parquet"

    mercado.to_parquet(ruta, index=False)

    print(f"Registros limpios: {len(mercado)}")
    print(f"Archivo generado: {ruta}")

    # 6. Procesar generacion por recurso.
    print("\n========== GENERACION POR RECURSO ==========")

    procesar_generacion_por_lotes(tamano_lote=1000)

    # 7. Limpiar y guardar embalses y aportes hidricos.
    print("\n========== EMBALSES Y APORTES HIDRICOS ==========")

    guardar_diarios_xm()

    # 8. Limpiar y guardar el catalogo de plantas.
    print("\n========== CATALOGO DE RECURSOS ==========")

    guardar_catalogo_xm()

    print("\n======================================")
    print("LIMPIEZA DE XM FINALIZADA CORRECTAMENTE")
    print("======================================")


if __name__ == "__main__":
    main()
