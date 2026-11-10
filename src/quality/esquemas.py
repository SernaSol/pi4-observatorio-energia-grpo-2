"""
Reglas de calidad de la capa plata, escritas con pandera.

Un ESQUEMA es la lista de condiciones que una tabla limpia DEBE cumplir:
que columnas tiene, de que tipo es cada una y que valores acepta.
Si una sola fila no cumple, pandera detiene el programa y dice cual fila
y cual regla fallo. Asi, ningun dato sucio llega a la capa oro.

Este archivo SOLO GUARDA las reglas: no revisa nada por si solo.
Quien las usa es OTRO archivo: src/silver/enerandes.py (la limpieza).
Ese archivo, despues de limpiar, escribe estas dos lineas:

    from src.quality.esquemas import ESQUEMA_VENTAS
    ESQUEMA_VENTAS.validate(limpias, lazy=True)

  - La primera trae las reglas de este archivo (la variable ESQUEMA_VENTAS).
  - La segunda revisa la tabla limpia con esas reglas.
    Si una regla falla, el programa se detiene y la tabla NO se guarda.
    lazy=True: revisa toda la tabla y muestra TODOS los errores juntos
    (sin lazy=True, se detiene en el primer error y no se sabe si hay mas).

Las reglas van en un archivo aparte para escribirlas una sola vez:
las usan la limpieza (enerandes.py) y las pruebas (tests/).
"""
# ---------------------------------------------------------------------------
# IMPORTS
# ---------------------------------------------------------------------------
# pandera: libreria para revisar que una tabla de pandas cumpla reglas.
# .pandas es la parte de pandera para tablas de pandas; "as pa" le da el nombre corto pa
import pandera.pandas as pa
# Column: las reglas de UNA columna (su tipo y sus condiciones)
# Check: una condicion, por ejemplo ">= 0" o "esta en esta lista"
from pandera.pandas import Check, Column

# ---------------------------------------------------------------------------
# VALORES ACEPTADOS en las columnas de categorias
# ---------------------------------------------------------------------------
# Los unicos 4 valores que puede tener la columna segmento
SEGMENTOS = ["Residencial", "Comercial", "Industrial", "No informado"]
# Los unicos 2 valores que puede tener la columna tipo_compra
TIPOS_COMPRA = ["Bolsa", "Contrato"]

# ---------------------------------------------------------------------------
# EL ESQUEMA de la tabla limpia
# ---------------------------------------------------------------------------
# pa.DataFrameSchema(...) crea el esquema. Recibe un diccionario
# {nombre de columna: Column(tipo, condicion)} y algunas reglas de toda la tabla
ESQUEMA_VENTAS = pa.DataFrameSchema(
    {
        # periodo: texto (str) que cumpla el patron AAAA-MM con un mes de 01 a 12.
        # r"^\d{4}-(0[1-9]|1[0-2])$" es una expresion regular (un patron de texto):
        #   ^ inicio, \d{4} cuatro digitos, - un guion, (0[1-9]|1[0-2]) del 01 al 12, $ fin
        # Ejemplo: '2023-04' cumple; '2023-13' y 'TOTAL' no cumplen
        "periodo": Column(str, Check.str_matches(r"^\d{4}-(0[1-9]|1[0-2])$")),
        # divipola: texto de exactamente 5 digitos (^\d{5}$). '05001' cumple; '5001' no
        "divipola": Column(str, Check.str_matches(r"^\d{5}$")),
        # municipio: texto, sin condicion extra (el nombre oficial ya viene de MUNICIPIOS)
        "municipio": Column(str),
        # segmento: texto que este en la lista SEGMENTOS (.isin = "esta en")
        "segmento": Column(str, Check.isin(SEGMENTOS)),
        # tipo_compra: texto que este en la lista TIPOS_COMPRA: solo Bolsa o Contrato
        "tipo_compra": Column(str, Check.isin(TIPOS_COMPRA)),
        # energia_kwh: numero con decimales (float) mayor o igual a 0 (ge = greater or equal)
        "energia_kwh": Column(float, Check.ge(0)),
        # valor_cop: numero >= 0; nullable=True permite celdas vacias (regla 9 de la limpieza)
        "valor_cop": Column(float, Check.ge(0), nullable=True),
        # clientes: numero entero (int) mayor o igual a 0
        "clientes": Column(int, Check.ge(0)),
    },
    # unique: no puede haber dos filas con el mismo periodo, municipio, segmento y tipo
    # de compra; si las hay, es una venta repetida
    unique=["periodo", "divipola", "segmento", "tipo_compra"],
    # strict=True: la tabla no puede traer columnas que no esten en este esquema
    strict=True,
)



# ---------------------------------------------------------------------------
# ESQUEMA DE VENTAS CONSOLIDADAS: 2023-2026
# ---------------------------------------------------------------------------
# Conserva las reglas originales y agrega columnas de trazabilidad.

ESQUEMA_VENTAS_CONSOLIDADA = pa.DataFrameSchema(
    {
        **ESQUEMA_VENTAS.columns,

        # Todas las energias deben quedar expresadas en kWh.
        "unidad": Column(str, Check.isin(["kWh"])),

        # Año del archivo de origen.
        "anio_origen": Column(
            int,
            Check.isin([2023, 2024, 2025, 2026])
        ),

        # Valores originales, conservados para auditoria.
        "unidad_origen": Column(str, nullable=True),
        "municipio_origen": Column(str, nullable=True),
        "segmento_origen": Column(str, nullable=True),
        "tipo_compra_origen": Column(str, nullable=True),
    },
    unique=["periodo", "divipola", "segmento", "tipo_compra"],
    strict=True,
)


# ---------------------------------------------------------------------------
# ESQUEMA XM: MERCADO HORARIO
# ---------------------------------------------------------------------------

ESQUEMA_MERCADO_HORARIO = pa.DataFrameSchema(
    {
        # Fecha en formato AAAA-MM-DD.
        "fecha": Column(
            str,
            Check.str_matches(
                r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$"
            ),
        ),

        # XM utiliza horas del 1 al 24.
        "hora": Column(
            int,
            Check.in_range(1, 24),
        ),

        # Identificadores provenientes de XM.
        "entidad": Column(str),
        "codigo": Column(str),

        # Indicadores numericos no negativos.
        "precio_bolsa": Column(
            float,
            Check.ge(0),
        ),

        "demanda": Column(
            float,
            Check.ge(0),
        ),
    },

    # Una fila por fecha, hora, entidad y codigo.
    unique=["fecha", "hora", "entidad", "codigo"],

    # No permitir columnas inesperadas.
    strict=True,
)

# ---------------------------------------------------------------------------
# ESQUEMA XM: GENERACION HORARIA POR RECURSO
# ---------------------------------------------------------------------------

ESQUEMA_GENERACION_RECURSO = pa.DataFrameSchema(
    {
        # Fecha de generacion en formato AAAA-MM-DD.
        "fecha": Column(
            str,
            Check.str_matches(
                r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$"
            ),
        ),

        # XM identifica las horas del 1 al 24.
        "hora": Column(
            int,
            Check.in_range(1, 24),
        ),

        # Identificacion de la planta o recurso.
        "entidad": Column(str),
        "codigo": Column(str, Check.str_length(min_value=1)),

        # La generacion debe ser numerica y no negativa.
        # El cero es valido.
        "generacion": Column(
            float,
            Check.ge(0),
            nullable=False,
        ),
    },

    # Una observacion por fecha, hora y recurso.
    unique=["fecha", "hora", "codigo"],

    strict=True,
)

ESQUEMA_CATALOGO_XM = pa.DataFrameSchema(
    {
        "fecha_catalogo": Column(pa.DateTime),
        "entidad": Column(str, nullable=True),
        "codigo_recurso": Column(str, Check.str_length(min_value=1)),
        "nombre_recurso": Column(str, Check.str_length(min_value=1)),
        "tipo": Column(str, nullable=True),
        "despacho": Column(str, nullable=True),
        "tipo_recurso": Column(str, nullable=True),
        "codigo_empresa": Column(str, nullable=True),
        "fuente_energetica": Column(str, nullable=True),
        "fecha_inicio_operacion": Column(pa.DateTime, nullable=True),
        "estado": Column(str, Check.isin(["OPERACION", "PRUEBAS"])),
    },
    unique=["codigo_recurso"],
    strict=True,
)

ESQUEMA_NOAA_ONI = pa.DataFrameSchema(
    {
        "fecha": Column(pa.DateTime),
        "anio": Column(int),
        "mes": Column(int, Check.in_range(1, 12)),
        "trimestre_movil": Column(str),
        "oni": Column(float),
        "fase_enso": Column(
            str, Check.isin(["El Niño", "La Niña", "Neutral"])
        ),
    },
    unique=["fecha"],
    strict=True,
)
