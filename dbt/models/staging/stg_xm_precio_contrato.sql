
-- STAGING: PRECIO PROMEDIO DE CONTRATOS XM
-- Fuente: capa bronce, Evidencia 3.
-- Grano esperado: una fila por fecha e identificador.

select
    cast("Date" as date) as fecha,
    cast("Id" as varchar) as entidad,
    try_cast("Value" as double) as precio_contrato,
    "_fuente" as fuente,
    "_origen" as origen,
    "_extraido_en" as extraido_en

from {{ source('bronce', 'xm_precio_contrato') }}
