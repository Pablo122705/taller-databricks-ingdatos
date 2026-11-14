# Ejercicio 4: Resumen antes y después de agregar la venta

| Categoría | Antes | Después | Diferencia |
|---|---|---|---|
| Electrónica | 2495.0 (6 ventas) | 2695.0 (7 ventas) | +200.0 |
| Muebles | 730.0 | 730.0 | 0 |
| Papelería | 61.0 | 61.0 | 0 |

**Venta agregada:** id 16, Impresora, Electrónica, cantidad 1 × precio 200.0 = total 200.0, insertada directamente en `ventas_bronze` (sin ejecutar el notebook de carga).

**Conclusión:** el resultado coincide. Al volver a ejecutar el pipeline, Databricks recalculó primero `pipeline_ventas_limpias` (la venta es válida y pasó los filtros) y luego `pipeline_ventas_por_categoria`, porque depende de la anterior. Solo Electrónica aumentó, exactamente en 200.0. No fue necesario indicar el orden: el pipeline lo dedujo de las definiciones.
