
-- TABLA DE HECHOS: CLIMA MENSUAL
-- Grano: un registro por mes y municipio.
-- Se agregan por separado los datos de precipitacion
-- y temperatura para evitar duplicar registros.

with precipitacion_estacion as (
    select
        cast(date_trunc('month', cast(fecha as date)) as date) as mes,
        cod_mpio,
        codigoestacion,
        avg(precipitacion_mm) as precipitacion_media_estacion
    from {{ source('plata', 'ideam_precipitacion_diaria') }}
    where cod_mpio is not null
    group by 1, 2, 3
),

precipitacion_mensual as (
    select
        mes,
        cod_mpio,
        round(avg(precipitacion_media_estacion), 2)
            as precipitacion_media_mm
    from precipitacion_estacion
    group by 1, 2
),

temperatura_mensual as (
    select
        cast(date_trunc('month', cast(fecha as date)) as date) as mes,
        cod_mpio,
        round(avg(temp_media_c), 2) as temperatura_media_c,
        round(avg(temp_min_c), 2) as temperatura_min_media_c,
        round(avg(temp_max_c), 2) as temperatura_max_media_c
    from {{ source('plata', 'ideam_temperatura_diaria') }}
    where cod_mpio is not null
    group by 1, 2
)

select
    coalesce(p.mes, t.mes) as mes,
    coalesce(p.cod_mpio, t.cod_mpio) as cod_mpio,
    p.precipitacion_media_mm,
    t.temperatura_media_c,
    t.temperatura_min_media_c,
    t.temperatura_max_media_c,
    f.fase_enso

from precipitacion_mensual p

full outer join temperatura_mensual t
    on p.mes = t.mes
    and p.cod_mpio = t.cod_mpio

left join {{ ref('dim_fecha') }} f
    on coalesce(p.mes, t.mes) = f.fecha
