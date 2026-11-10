
-- TABLA DE HECHOS: MERCADO HORARIO XM
-- Grano: una fila por fecha, hora, entidad y codigo.
-- Medidas: precio de bolsa y demanda.

select
    -- Relacion con la dimension fecha.
    f.fecha_id,

    -- Hora del dia (1 a 24).
    m.hora,

    -- Identificadores originales de XM.
    m.entidad,
    m.codigo,

    -- Medidas del mercado electrico.
    m.precio_bolsa,
    m.demanda

from {{ source('plata', 'xm_mercado_horario') }} as m

-- Relacionar cada registro con su fecha.
join {{ ref('dim_fecha') }} as f
    on cast(m.fecha as date) = f.fecha
