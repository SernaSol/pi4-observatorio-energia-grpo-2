
-- TABLA DE HECHOS: GENERACION ELECTRICA MENSUAL
-- Grano: una fila por mes y recurso.
-- Medida: suma de la generacion registrada.

select
    cast(date_trunc('month', f.fecha) as date) as mes,
    year(f.fecha) as anio,
    month(f.fecha) as numero_mes,
    g.recurso_id,
    round(sum(g.generacion), 2) as generacion_total,
    count(*) as registros_horarios

from {{ ref('fact_generacion_recurso') }} as g

join {{ ref('dim_fecha') }} as f
    on g.fecha_id = f.fecha_id

group by 1, 2, 3, 4
order by mes, recurso_id
