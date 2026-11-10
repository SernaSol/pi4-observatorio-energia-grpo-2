
-- TABLA DE HECHOS: GENERACION POR RECURSO
-- Grano: una fila por fecha, hora y recurso.
-- Medida: generacion electrica.

select
    -- Relacion con la dimension fecha.
    f.fecha_id,

    -- Hora del dia (1 a 24).
    g.hora,

    -- Relacion con la dimension recurso.
    g.codigo as recurso_id,

    -- Identificador original de XM.
    g.entidad,

    -- Medida de generacion.
    g.generacion

from {{ source('plata', 'xm_generacion_recurso') }} as g

left join {{ ref('dim_fecha') }} as f
    on cast(g.fecha as date) = f.fecha
