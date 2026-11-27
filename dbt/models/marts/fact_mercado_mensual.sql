
-- TABLA DE HECHOS: MERCADO ELECTRICO MENSUAL
-- Grano: una fila por mes.
-- Precio de bolsa: promedio de los valores horarios.
-- Demanda: suma de los valores horarios.

select
    cast(date_trunc('month', cast(fecha as date)) as date) as mes,
    year(cast(fecha as date)) as anio,
    month(cast(fecha as date)) as numero_mes,
    round(avg(precio_bolsa), 2) as precio_bolsa_promedio,
    round(sum(demanda), 2) as demanda_total,
    count(*) as registros_horarios

from {{ source('plata', 'xm_mercado_horario') }}

group by 1, 2, 3
order by mes
