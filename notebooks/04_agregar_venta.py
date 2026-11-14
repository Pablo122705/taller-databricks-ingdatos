# Databricks notebook source
# MAGIC %md
# MAGIC # 04_agregar_venta (ejercicio 4)
# MAGIC Ejecutar celda por celda, en orden. NO ejecutar 01_cargar_ventas durante esta prueba.

# COMMAND ----------

# MAGIC %sql
# MAGIC -- CELDA 1: RESUMEN ANTES (pipeline ejecutado una vez)
# MAGIC SELECT * FROM workspace.ingenieria_datos_pablo.pipeline_ventas_por_categoria ORDER BY categoria

# COMMAND ----------

# MAGIC %sql
# MAGIC -- CELDA 2: agrega UNA venta válida a ventas_bronze (1 x 200 = 200 en Electrónica). No se duplica si se repite.
# MAGIC INSERT INTO workspace.ingenieria_datos_pablo.ventas_bronze
# MAGIC SELECT 16, DATE'2026-11-09', 'Impresora', 'Electrónica', 1, CAST(200.0 AS DOUBLE)
# MAGIC WHERE NOT EXISTS (SELECT 1 FROM workspace.ingenieria_datos_pablo.ventas_bronze WHERE id_venta = 16)

# COMMAND ----------

# MAGIC %sql
# MAGIC -- CELDA 3: RESUMEN DESPUÉS (ejecutar SOLO después de volver a correr el pipeline)
# MAGIC SELECT * FROM workspace.ingenieria_datos_pablo.pipeline_ventas_por_categoria ORDER BY categoria
