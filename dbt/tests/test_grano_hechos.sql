
-- Verificar que no existan llaves compuestas duplicadas
-- en ninguna de las tres tablas de hechos.

with ventas_duplicadas as (
    select
        mes_id, municipio_id, segmento_id, tipo_compra
    from {{ ref('fact_ventas_mensual') }}
    group by 1, 2, 3, 4
    having count(*) > 1
),

mercado_duplicado as (
    select
        fecha_id, hora, entidad, codigo
    from {{ ref('fact_mercado_horario') }}
    group by 1, 2, 3, 4
    having count(*) > 1
),

generacion_duplicada as (
    select
        fecha_id, hora, recurso_id
    from {{ ref('fact_generacion_recurso') }}
    group by 1, 2, 3
    having count(*) > 1
)

select 'ventas' as tabla from ventas_duplicadas
union all
select 'mercado' as tabla from mercado_duplicado
union all
select 'generacion' as tabla from generacion_duplicada
