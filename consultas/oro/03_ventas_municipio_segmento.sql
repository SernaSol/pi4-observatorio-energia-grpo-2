
-- CONSULTA 3: VENTAS POR MUNICIPIO Y SEGMENTO
-- Identifica las 10 combinaciones con mayor energia
-- vendida en cada año.

WITH ventas AS (
    SELECT
        f.anio,
        m.municipio,
        s.segmento,

        COUNT(DISTINCT v.mes_id) AS meses_registrados,

        ROUND(
            SUM(v.energia_kwh), 2
        ) AS energia_total_kwh,

        ROUND(
            SUM(v.valor_cop), 2
        ) AS valor_total_cop

    FROM main.fact_ventas_mensual AS v

    JOIN main.dim_mes AS f
        ON v.mes_id = f.mes_id

    JOIN main.dim_municipio AS m
        ON v.municipio_id = m.municipio_id

    JOIN main.dim_segmento AS s
        ON v.segmento_id = s.segmento_id

    WHERE f.anio IN (2025, 2026)

    GROUP BY
        f.anio,
        m.municipio,
        s.segmento
),

clasificacion AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY anio
            ORDER BY energia_total_kwh DESC
        ) AS posicion
    FROM ventas
)

SELECT
    anio,
    posicion,
    municipio,
    segmento,
    meses_registrados,
    energia_total_kwh,
    valor_total_cop

FROM clasificacion

WHERE posicion <= 10

ORDER BY
    anio,
    posicion;
