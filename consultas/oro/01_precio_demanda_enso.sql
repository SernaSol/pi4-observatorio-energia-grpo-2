
-- CONSULTA 1: PRECIO, DEMANDA Y FASE ENSO
-- Pregunta: ¿Cómo cambian el precio de bolsa y la demanda
-- según las fases climáticas durante 2025 y 2026?

SELECT
    f.anio,
    f.fase_enso,

    -- Cantidad de observaciones horarias.
    COUNT(*) AS registros_horarios,

    -- Precio promedio del mercado electrico.
    ROUND(AVG(m.precio_bolsa), 2) AS precio_bolsa_promedio,

    -- Demanda promedio.
    ROUND(AVG(m.demanda), 2) AS demanda_promedio

FROM main.fact_mercado_horario AS m

-- Relacion con la dimension fecha y ENSO.
JOIN main.dim_fecha AS f
    ON m.fecha_id = f.fecha_id

WHERE f.anio IN (2025, 2026)

GROUP BY
    f.anio,
    f.fase_enso

ORDER BY
    f.anio,
    f.fase_enso;
