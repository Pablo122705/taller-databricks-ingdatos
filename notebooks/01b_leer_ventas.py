# Databricks notebook source
# MAGIC %md
# MAGIC # 01b_leer_ventas
# MAGIC Lee `ventas_bronze` desde otro notebook usando el nombre completo catalogo.esquema.tabla.

# COMMAND ----------

ventas = spark.read.table("workspace.ingenieria_datos_pablo.ventas_bronze")
print("Total de registros:", ventas.count())

# COMMAND ----------

# Ventas de la categoría Electrónica
display(ventas.filter(ventas.categoria == "Electrónica").orderBy("id_venta"))
