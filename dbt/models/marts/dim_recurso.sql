
-- DIMENSION RECURSO
-- Grano: una fila por codigo de recurso.
-- Incluye recursos del catalogo y recursos historicos
-- que aparecen en generacion pero no en el catalogo.

with catalogo as (
    select
        codigo_recurso as recurso_id,
        nombre_recurso,
        tipo,
        tipo_recurso,
        fuente_energetica,
        codigo_empresa,
        estado,
        despacho,
        fecha_inicio_operacion,
        true as en_catalogo

    from {{ source('plata', 'xm_listado_recursos') }}
),

recursos_faltantes as (
    select distinct
        g.codigo as recurso_id,

        'Sin catalogo: ' || g.codigo as nombre_recurso,

        cast(null as varchar) as tipo,
        cast(null as varchar) as tipo_recurso,
        cast(null as varchar) as fuente_energetica,
        cast(null as varchar) as codigo_empresa,
        cast(null as varchar) as estado,
        cast(null as varchar) as despacho,
        cast(null as timestamp) as fecha_inicio_operacion,

        false as en_catalogo

    from {{ source('plata', 'xm_generacion_recurso') }} as g

    left join catalogo as c
        on g.codigo = c.recurso_id

    where c.recurso_id is null
)

select * from catalogo

union all

select * from recursos_faltantes
