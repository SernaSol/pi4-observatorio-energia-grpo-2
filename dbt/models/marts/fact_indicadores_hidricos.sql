
-- TABLA DE HECHOS: INDICADORES HIDRICOS
-- Grano: una fila por fecha y entidad.
-- Relaciona embalses, aportes hidricos y fase ENSO.

select
    f.fecha_id,
    f.fecha,
    f.anio,
    f.mes,
    f.fase_enso,

    e.entidad,
    e.valor_embalse,

    a.valor_aportes,

    h.aportes_media_historica,

    case
        when h.aportes_media_historica > 0
        then round(
            100.0 * a.valor_aportes / h.aportes_media_historica,
            2
        )
        else null
    end as porcentaje_aportes_vs_media

from {{ source('plata', 'xm_embalses') }} as e

join {{ ref('dim_fecha') }} as f
    on cast(e.fecha as date) = f.fecha

left join {{ source('plata', 'xm_aportes_hidricos') }} as a
    on cast(e.fecha as date) = cast(a.fecha as date)
    and e.entidad = a.entidad

left join {{ ref('stg_xm_aportes_media') }} as h
    on cast(e.fecha as date) = h.fecha
    and e.entidad = h.entidad
