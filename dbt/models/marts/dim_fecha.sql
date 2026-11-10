
-- DIMENSION FECHA
-- Grano: una fila por dia.
-- Relaciona el calendario con la fase ENSO de NOAA.

with limites as (
    select
        min(cast(periodo || '-01' as date)) as fecha_inicio,
        greatest(
            max(last_day(cast(periodo || '-01' as date))),
            (
                select max(cast(fecha as date))
                from {{ source('plata', 'xm_mercado_horario') }}
            )
        ) as fecha_fin
    from {{ ref('stg_ventas') }}
),

calendario as (
    select cast(d.fecha as date) as fecha
    from limites l,
    generate_series(
        l.fecha_inicio,
        l.fecha_fin,
        interval 1 day
    ) as d(fecha)
),

enso_mensual as (
    select
        cast(date_trunc('month', fecha) as date) as mes_oni,
        fase_enso
    from {{ source('plata', 'noaa_oni') }}
)

select
    cast(strftime(c.fecha, '%Y%m%d') as integer) as fecha_id,
    c.fecha,
    year(c.fecha) as anio,
    month(c.fecha) as mes,
    day(c.fecha) as dia,
    quarter(c.fecha) as trimestre,
    extract(isodow from c.fecha) as dia_semana,
    coalesce(e.fase_enso, 'Sin dato') as fase_enso

from calendario c

left join enso_mensual e
    on cast(date_trunc('month', c.fecha) as date) = e.mes_oni
