# Calidad XM - Generacion por recurso

- Posiciones horarias procesadas: 8408664
- Registros limpios: 5935449
- Registros en cuarentena: 2473215

| Problema | Antes | Despues en plata | Regla |
|---|---:|---:|---|
| Generacion vacia o no numerica | 2473215 | 0 | Cuarentena |
| Generacion negativa | 0 | 0 | Cuarentena |
| Generacion igual a cero | 0 | 0 | Conservar |

Los valores faltantes no se reemplazan por cero.
La cuarentena conserva fecha, hora, recurso, valor original y motivo.
