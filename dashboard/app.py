
"""
Dashboard del Observatorio de Energia y Clima.
Evidencia 3 - Proyecto Integrado IV.
"""

import streamlit as st
import pandas as pd

from datos import cargar_datos


st.set_page_config(
    page_title="Observatorio de Energia y Clima",
    page_icon="⚡",
    layout="wide",
)

st.title("Observatorio de Energia y Clima")
st.caption("Proyecto Integrado IV | Evidencia 3")

st.markdown(
    """
    Analisis del mercado electrico colombiano,
    los recursos hidricos, las condiciones climaticas
    y el comportamiento comercial de EnerAndes.
    """
)

# Cargar datos de la capa oro
datos = cargar_datos()



# Municipios disponibles en los datos climaticos
clima_base = datos["fact_clima_mensual"].copy()

municipios = sorted(
    clima_base["cod_mpio"].dropna().astype(str).unique()
)

municipios_seleccionados = st.sidebar.multiselect(
    "Municipios (codigo DANE)",
    options=municipios,
    default=municipios,
)


# -------------------------------------------------
# FILTROS COMERCIALES DE ENERANDES
# -------------------------------------------------

segmentos_disponibles = sorted(
    datos["dim_segmento"]["segmento"].dropna().unique()
)

segmentos_seleccionados = st.sidebar.multiselect(
    "Segmento de clientes",
    options=segmentos_disponibles,
    default=segmentos_disponibles,
)

municipios_enerandes = sorted(
    datos["dim_municipio"]["municipio"].dropna().unique()
)

municipios_comerciales = st.sidebar.multiselect(
    "Municipios EnerAndes",
    options=municipios_enerandes,
    default=municipios_enerandes,
)


# -------------------------------------------------
# FILTROS DEL DASHBOARD
# -------------------------------------------------

st.sidebar.header("Filtros del observatorio")

# Fechas disponibles en el calendario
calendario = datos["dim_fecha"].copy()
calendario["fecha"] = pd.to_datetime(calendario["fecha"])

fecha_minima = calendario["fecha"].min().date()
fecha_maxima = calendario["fecha"].max().date()

rango_fechas = st.sidebar.date_input(
    "Periodo de analisis",
    value=(fecha_minima, fecha_maxima),
    min_value=fecha_minima,
    max_value=fecha_maxima,
)

# Fase del fenomeno ENSO
fases = sorted(calendario["fase_enso"].dropna().unique())

fase_seleccionada = st.sidebar.multiselect(
    "Fase ENSO",
    options=fases,
    default=fases,
)

st.sidebar.caption(
    "Los filtros se aplicaran a las visualizaciones del observatorio."
)


st.success("Datos de la capa oro cargados correctamente")

# Indicadores iniciales
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Tablas disponibles", len(datos))

with col2:
    st.metric(
        "Registros climaticos",
        len(datos["fact_clima_mensual"]),
    )

with col3:
    st.metric(
        "Registros hidricos",
        len(datos["fact_indicadores_hidricos"]),
    )

st.subheader("Fuentes disponibles")

for nombre, tabla in datos.items():
    st.write(f"{nombre}: {len(tabla):,} registros")



# -------------------------------------------------
# PREGUNTA 1: EMBALSES Y FENOMENO ENSO
# -------------------------------------------------

st.divider()
st.header("1. Embalses y fenomeno ENSO")

st.markdown(
    "¿Como cambia el nivel de los embalses durante "
    "las diferentes fases de El Niño y La Niña?"
)

hidricos = datos["fact_indicadores_hidricos"].copy()
hidricos["fecha"] = pd.to_datetime(hidricos["fecha"])

# Aplicar el filtro de fechas
if len(rango_fechas) == 2:
    fecha_inicio, fecha_fin = rango_fechas

    hidricos = hidricos[
        (hidricos["fecha"].dt.date >= fecha_inicio)
        & (hidricos["fecha"].dt.date <= fecha_fin)
    ]

# Aplicar filtro ENSO
hidricos = hidricos[
    hidricos["fase_enso"].isin(fase_seleccionada)
]

if hidricos.empty:
    st.warning("No hay datos para los filtros seleccionados.")
else:
    # Convertir la fraccion de embalse a porcentaje
    hidricos["embalse_porcentaje"] = (
        hidricos["valor_embalse"] * 100
    )

    # Promedio diario para evitar duplicar fechas
    serie_embalses = (
        hidricos.groupby("fecha", as_index=False)
        ["embalse_porcentaje"].mean()
        .sort_values("fecha")
    )

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Nivel promedio del embalse",
            f"{hidricos['embalse_porcentaje'].mean():.2f} %"
        )

    with col2:
        st.metric(
            "Registros analizados",
            f"{len(hidricos):,}"
        )

    st.subheader("Evolucion historica del nivel de embalses")

    st.line_chart(
        serie_embalses.set_index("fecha")[
            "embalse_porcentaje"
        ],
        y_label="Nivel de embalses (%)",
        x_label="Fecha",
    )

    st.caption(
        "Fuente: XM y NOAA. El nivel del embalse "
        "se presenta como porcentaje de volumen util. "
        "La seleccion ENSO se aplica a los registros visibles."
    )


# -------------------------------------------------
# PREGUNTA 2: APORTES HIDRICOS VS MEDIA HISTORICA
# -------------------------------------------------

st.divider()
st.header("2. Aportes hidricos frente a su media historica")

st.markdown(
    "¿Como se comportan los aportes hidricos frente a "
    "su media historica durante El Niño y La Niña?"
)

# Reutilizar los datos que ya filtramos en la pregunta 1
aportes = hidricos[
    hidricos["porcentaje_aportes_vs_media"].notna()
].copy()

if aportes.empty:
    st.warning(
        "No hay informacion de aportes hidricos "
        "para los filtros seleccionados."
    )
else:
    promedio_aportes = aportes[
        "porcentaje_aportes_vs_media"
    ].mean()

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Aportes frente a la media",
            f"{promedio_aportes:.2f} %"
        )

    with col2:
        st.metric(
            "Dias con informacion",
            f"{aportes['fecha'].nunique():,}"
        )

    st.subheader("Evolucion de aportes frente a la media")

    serie_aportes = (
        aportes.groupby("fecha")[
            "porcentaje_aportes_vs_media"
        ]
        .mean()
        .sort_index()
    )

    st.line_chart(
        serie_aportes,
        x_label="Fecha",
        y_label="Aportes respecto a la media (%)",
    )

    st.caption(
        "Fuente: XM y NOAA. Un valor de 100 % "
        "indica aportes iguales a la media historica; "
        "valores inferiores indican aportes por debajo "
        "de la referencia. Periodo disponible: 2023-2026."
    )


# -------------------------------------------------
# PREGUNTA 3: PRECIOS DE ENERGIA Y DEMANDA
# -------------------------------------------------

st.divider()
st.header("3. Precios de energia y demanda")

st.markdown(
    "¿Como evolucionan los precios de bolsa y la demanda "
    "electrica durante las diferentes fases ENSO?"
)

mercado = datos["fact_mercado_mensual"].copy()
mercado["mes"] = pd.to_datetime(mercado["mes"])

# Relacionar el mercado mensual con la fase ENSO
# utilizando el primer dia de cada mes.
enso_mensual = calendario[
    calendario["fecha"].dt.day == 1
][["fecha", "fase_enso"]].copy()

mercado = mercado.merge(
    enso_mensual,
    left_on="mes",
    right_on="fecha",
    how="left",
)

# Aplicar filtros del dashboard
if len(rango_fechas) == 2:
    fecha_inicio, fecha_fin = rango_fechas

    mercado = mercado[
        (mercado["mes"].dt.date >= fecha_inicio)
        & (mercado["mes"].dt.date <= fecha_fin)
    ]

mercado = mercado[
    mercado["fase_enso"].isin(fase_seleccionada)
]

if mercado.empty:
    st.warning(
        "No hay informacion de mercado para los filtros seleccionados."
    )
else:
    mercado = mercado.sort_values("mes")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Precio promedio de bolsa",
            f"{mercado['precio_bolsa_promedio'].mean():,.2f}"
        )

    with col2:
        st.metric(
            "Meses analizados",
            f"{len(mercado):,}"
        )

    st.subheader("Evolucion mensual del precio de bolsa")

    st.line_chart(
        mercado.set_index("mes")[["precio_bolsa_promedio"]],
        x_label="Mes",
        y_label="Precio promedio de bolsa",
    )

    st.subheader("Evolucion mensual de la demanda electrica")

    st.bar_chart(
        mercado.set_index("mes")[["demanda_total"]],
        x_label="Mes",
        y_label="Demanda agregada",
    )

    st.caption(
        "Fuente: XM y NOAA. Los precios corresponden a "
        "promedios mensuales de registros horarios. "
        "La demanda es la suma de los registros disponibles. "
        "Las unidades deben verificarse antes de interpretar "
        "los valores como energia mensual."
    )


# -------------------------------------------------
# PREGUNTA 4: GENERACION POR FUENTE ENERGETICA
# -------------------------------------------------

st.divider()
st.header("4. Generacion por fuente energetica")

st.markdown(
    "¿Que fuentes energeticas aportan mas a la generacion "
    "electrica y como cambia su participacion en el tiempo?"
)

generacion = datos["fact_generacion_mensual"].copy()
recursos = datos["dim_recurso"].copy()

generacion["mes"] = pd.to_datetime(generacion["mes"])

# Relacionar cada recurso con su fuente energetica
generacion = generacion.merge(
    recursos[["recurso_id", "fuente_energetica"]],
    on="recurso_id",
    how="left",
)

generacion["fuente_energetica"] = (
    generacion["fuente_energetica"]
    .fillna("Sin clasificar")
)

# Relacionar la generacion mensual con ENSO
generacion = generacion.merge(
    enso_mensual,
    left_on="mes",
    right_on="fecha",
    how="left",
)

# Aplicar los filtros
if len(rango_fechas) == 2:
    fecha_inicio, fecha_fin = rango_fechas

    generacion = generacion[
        (generacion["mes"].dt.date >= fecha_inicio)
        & (generacion["mes"].dt.date <= fecha_fin)
    ]

generacion = generacion[
    generacion["fase_enso"].isin(fase_seleccionada)
]

if generacion.empty:
    st.warning(
        "No hay datos de generacion para los filtros seleccionados."
    )
else:
    # Generacion acumulada por fuente energetica
    resumen_fuentes = (
        generacion.groupby(
            "fuente_energetica", as_index=False
        )["generacion_total"]
        .sum()
        .sort_values("generacion_total", ascending=False)
    )

    total_generacion = resumen_fuentes[
        "generacion_total"
    ].sum()

    if total_generacion > 0:
        resumen_fuentes["participacion_pct"] = (
            100 * resumen_fuentes["generacion_total"]
            / total_generacion
        )

        st.metric(
            "Fuentes energeticas identificadas",
            generacion["fuente_energetica"].nunique(),
        )

        st.subheader("Participacion por fuente energetica")

        st.bar_chart(
            resumen_fuentes.set_index("fuente_energetica")[
                "participacion_pct"
            ],
            x_label="Fuente energetica",
            y_label="Participacion (%)",
        )

        # Evolucion mensual de la generacion
        evolucion = (
            generacion.groupby(
                ["mes", "fuente_energetica"]
            )["generacion_total"]
            .sum()
            .unstack(fill_value=0)
            .sort_index()
        )

        st.subheader("Evolucion mensual por fuente")

        st.area_chart(
            evolucion,
            x_label="Mes",
            y_label="Generacion agregada",
        )

        st.caption(
            "Fuente: XM y NOAA. La participacion se "
            "calcula sobre la generacion agregada de "
            "los recursos disponibles. La categoria "
            "'Sin clasificar' identifica recursos sin "
            "fuente energetica informada. Las unidades "
            "de generacion deben verificarse antes "
            "de interpretarlas como MWh o GWh."
        )
    else:
        st.warning(
            "La generacion total es cero para los filtros seleccionados."
        )


# -------------------------------------------------
# PREGUNTA 5: CLIMA POR MUNICIPIO Y FASE ENSO
# -------------------------------------------------

st.divider()
st.header("5. Clima por municipio")

st.markdown(
    "¿Como varian la temperatura y la precipitacion "
    "entre municipios y fases ENSO?"
)

clima = datos["fact_clima_mensual"].copy()
clima["mes"] = pd.to_datetime(clima["mes"])
clima["cod_mpio"] = clima["cod_mpio"].astype(str)

# Filtrar por municipio
clima = clima[
    clima["cod_mpio"].isin(municipios_seleccionados)
]

# Filtrar por fecha
if len(rango_fechas) == 2:
    fecha_inicio, fecha_fin = rango_fechas

    clima = clima[
        (clima["mes"].dt.date >= fecha_inicio)
        & (clima["mes"].dt.date <= fecha_fin)
    ]

# Filtrar por fase ENSO
clima = clima[
    clima["fase_enso"].isin(fase_seleccionada)
]

if clima.empty:
    st.warning(
        "No hay informacion climatica para los filtros seleccionados."
    )
else:
    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Temperatura media",
            f"{clima['temperatura_media_c'].mean():.2f} °C"
        )

    with col2:
        st.metric(
            "Precipitacion media",
            f"{clima['precipitacion_media_mm'].mean():.2f} mm"
        )

    st.subheader("Evolucion mensual de la temperatura")

    temperatura = (
        clima.groupby("mes")["temperatura_media_c"]
        .mean()
        .sort_index()
    )

    st.line_chart(
        temperatura,
        x_label="Mes",
        y_label="Temperatura media (°C)",
    )

    st.subheader("Precipitacion media por municipio")

    precipitacion = (
        clima.groupby("cod_mpio")["precipitacion_media_mm"]
        .mean()
        .sort_values(ascending=False)
        .head(15)
    )

    st.bar_chart(
        precipitacion,
        x_label="Codigo DANE del municipio",
        y_label="Precipitacion media (mm)",
    )

    st.caption(
        "Fuente: IDEAM y NOAA. Los valores corresponden "
        "a promedios de los registros disponibles. "
        "La cobertura puede variar entre municipios, "
        "estaciones y periodos."
    )


# -------------------------------------------------
# PREGUNTA 6: COMPORTAMIENTO COMERCIAL ENERANDES
# -------------------------------------------------

st.divider()
st.header("6. Comportamiento comercial de EnerAndes")

st.markdown(
    "¿Como evolucionan las ventas de energia y los ingresos "
    "segun el segmento, municipio y tipo de compra?"
)

ventas = datos["fact_ventas_mensual"].copy()

# Incorporar nombres de segmentos y municipios
ventas = ventas.merge(
    datos["dim_segmento"][["segmento_id", "segmento"]],
    on="segmento_id",
    how="left",
)

ventas = ventas.merge(
    datos["dim_municipio"][["municipio_id", "municipio"]],
    on="municipio_id",
    how="left",
)

# Convertir mes_id (ejemplo: 202401) a fecha
ventas["mes"] = pd.to_datetime(
    ventas["mes_id"].astype(str),
    format="%Y%m",
)

# Relacionar ventas con ENSO
ventas = ventas.merge(
    enso_mensual,
    left_on="mes",
    right_on="fecha",
    how="left",
)

# Filtro de fechas
if len(rango_fechas) == 2:
    fecha_inicio, fecha_fin = rango_fechas

    ventas = ventas[
        (ventas["mes"].dt.date >= fecha_inicio)
        & (ventas["mes"].dt.date <= fecha_fin)
    ]

# Filtros de segmento, municipio y fase ENSO
ventas = ventas[
    ventas["segmento"].isin(segmentos_seleccionados)
    & ventas["municipio"].isin(municipios_comerciales)
    & ventas["fase_enso"].isin(fase_seleccionada)
]

if ventas.empty:
    st.warning(
        "No hay ventas para los filtros seleccionados."
    )
else:
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Energia vendida",
            f"{ventas['energia_kwh'].sum():,.0f} kWh"
        )

    with col2:
        st.metric(
            "Ingresos totales",
            f"$ {ventas['valor_cop'].sum():,.0f} COP"
        )

    with col3:
        st.metric(
            "Municipios analizados",
            ventas["municipio"].nunique()
        )

    # Evolucion de ingresos
    ingresos_mes = (
        ventas.groupby("mes")["valor_cop"]
        .sum()
        .sort_index()
    )

    st.subheader("Evolucion mensual de ingresos")

    st.line_chart(
        ingresos_mes,
        x_label="Mes",
        y_label="Ingresos (COP)",
    )

    # Energia vendida por segmento
    energia_segmento = (
        ventas.groupby("segmento")["energia_kwh"]
        .sum()
        .sort_values(ascending=False)
    )

    st.subheader("Energia vendida por segmento")

    st.bar_chart(
        energia_segmento,
        x_label="Segmento",
        y_label="Energia vendida (kWh)",
    )

    # Comparar tipos de compra
    compras = (
        ventas.groupby("tipo_compra")["valor_cop"]
        .sum()
        .sort_values(ascending=False)
    )

    st.subheader("Ingresos por tipo de compra")

    st.bar_chart(
        compras,
        x_label="Tipo de compra",
        y_label="Ingresos (COP)",
    )

    st.caption(
        "Fuente: EnerAndes y NOAA. Los indicadores "
        "representan los registros comerciales disponibles "
        "para los filtros seleccionados. Las comparaciones "
        "por fase ENSO son descriptivas."
    )
