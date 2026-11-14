# Databricks notebook source
# MAGIC %md
# MAGIC # 02_transformar_ventas
# MAGIC Limpia `ventas_bronze`, crea `ventas_silver` y `ventas_por_categoria`. Se puede ejecutar varias veces sin duplicar datos (modo overwrite).

# COMMAND ----------

from pyspark.sql import functions as F
CAT, ESQ = "workspace", "ingenieria_datos_pablo"

bronze = spark.read.table(f"{CAT}.{ESQ}.ventas_bronze")
antes = bronze.count()

sin_duplicados = bronze.dropDuplicates()                      # registros idénticos
limpio = (sin_duplicados
          .filter(F.col("producto").isNotNull() & (F.trim(F.col("producto")) != ""))
          .filter((F.col("cantidad") > 0) & (F.col("precio_unitario") > 0)))
silver = limpio.withColumn("total_venta", F.round(F.col("cantidad") * F.col("precio_unitario"), 2))

silver.write.mode("overwrite").option("overwriteSchema", "true").saveAsTable(f"{CAT}.{ESQ}.ventas_silver")

resumen = (spark.read.table(f"{CAT}.{ESQ}.ventas_silver")
           .groupBy("categoria")
           .agg(F.round(F.sum("total_venta"), 2).alias("valor_total"), F.count("*").alias("num_ventas"))
           .orderBy("categoria"))
resumen.write.mode("overwrite").option("overwriteSchema", "true").saveAsTable(f"{CAT}.{ESQ}.ventas_por_categoria")

despues = spark.table(f"{CAT}.{ESQ}.ventas_silver").count()
print(f"Registros ANTES de la limpieza (bronze): {antes}")
print(f"Después de quitar duplicados:            {sin_duplicados.count()}")
print(f"Registros DESPUÉS de la limpieza (silver): {despues}")

# COMMAND ----------

display(spark.table(f"{CAT}.{ESQ}.ventas_por_categoria"))

# COMMAND ----------

# Control de repetición: cada ejecución deja una fila; los conteos deben ser iguales en todas
(spark.createDataFrame([(antes, despues, spark.table(f"{CAT}.{ESQ}.ventas_por_categoria").count())],
                       "registros_bronze INT, registros_silver INT, filas_resumen INT")
 .withColumn("ejecutado_en", F.current_timestamp())
 .write.mode("append").saveAsTable(f"{CAT}.{ESQ}.control_ejecuciones_02"))
display(spark.table(f"{CAT}.{ESQ}.control_ejecuciones_02").orderBy("ejecutado_en"))
