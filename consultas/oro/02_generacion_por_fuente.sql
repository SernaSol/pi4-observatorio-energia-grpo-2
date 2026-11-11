
-- CONSULTA 2: GENERACION POR FUENTE ENERGETICA
-- Pregunta: ¿Que fuentes aportaron mas generacion
-- electrica durante 2025 y 2026?

SELECT
    f.anio,

    -- Identificar la fuente energetica.
    COALESCE(
        r.fuente_energetica,
        'Sin informacion en catalogo'
    ) AS fuente_energetica,

    -- Cantidad de recursos diferentes.
    COUNT(DISTINCT g.recurso_id) AS cantidad_recursos,

    -- Cantidad de registros horarios.
    COUNT(*) AS registros_horarios,

    -- Generacion total reportada.
    ROUND(
        SUM(g.generacion), 2
    ) AS generacion_total

FROM main.fact_generacion_recurso AS g

JOIN main.dim_fecha AS f
    ON g.fecha_id = f.fecha_id

JOIN main.dim_recurso AS r
    ON g.recurso_id = r.recurso_id

WHERE f.anio IN (2025, 2026)

GROUP BY
    f.anio,
    COALESCE(
        r.fuente_energetica,
        'Sin informacion en catalogo'
    )

ORDER BY
    f.anio,
    generacion_total DESC;
