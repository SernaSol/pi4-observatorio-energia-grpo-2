# Reporte de calidad - Capa plata

## Fuente: EnerAndes (2023-2026)

- Registros de ventas procesados: 4170
- Registros limpios: 4007
- Registros en cuarentena: 163
- Filas TOTAL excluidas: 4

### Resultado por año

| Año | Entrada | Limpias | Cuarentena | TOTAL excluidas |
|---|---:|---:|---:|---:|
| 2023 | 1112 | 1064 | 48 | 1 |
| 2024 | 1112 | 1071 | 41 | 1 |
| 2025 | 1112 | 1071 | 41 | 1 |
| 2026 | 834 | 801 | 33 | 1 |

### Reglas de calidad: antes y después

| Problema | Antes | Después | Regla aplicada |
|---|---:|---:|---|
| Filas TOTAL | 4 | 0 | Excluir filas de resumen que no representan ventas |
| Duplicados normalizados | 120 | 0 | Conservar primera aparición y registrar copias en cuarentena |
| Energía vacía o negativa | 45 | 0 | Enviar registros inválidos a cuarentena |
| Valor facturado vacío | 29 | 28 | Conservar el valor nulo sin inventar información |
| Segmento no informado | 29 | 28 | Conservar categoría No informado |

### Transformaciones aplicadas

- Unificación de encabezados de los cuatro años.
- Normalización de fechas al formato AAAA-MM.
- Conversión de MWh a kWh.
- Estandarización de municipios y códigos DIVIPOLA.
- Normalización de segmentos y tipos de compra.
- Conversión de valores numéricos.
- Validación de las 14 columnas con Pandera.

### Motivos de cuarentena

| Motivo | Registros |
|---|---:|
| Registro duplicado | 118 |
| Energia vacia o no numerica | 25 |
| Energia negativa | 18 |
| Registro duplicado; Energia vacia o no numerica | 2 |

Nota: un registro puede tener varios motivos de cuarentena.
Las filas TOTAL se excluyen porque son resúmenes, no ventas.
