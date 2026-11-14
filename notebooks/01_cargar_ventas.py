# Databricks notebook source
# MAGIC %md
# MAGIC # 01_cargar_ventas
# MAGIC Crea el esquema y guarda las ventas como tabla Delta `ventas_bronze`.

# COMMAND ----------

from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DoubleType

CAT, ESQ = "workspace", "ingenieria_datos_pablo"
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {CAT}.{ESQ}")

ventas = [
    (1,  "2026-11-01", "Portátil",   "Electrónica", 1,  1200.0),
    (2,  "2026-11-01", "Mouse",      "Electrónica", 3,  25.0),
    (3,  "2026-11-02", "Teclado",    "Electrónica", 2,  45.0),
    (4,  "2026-11-02", "Silla",      "Muebles",     1,  180.0),
    (5,  "2026-11-03", "Escritorio", "Muebles",     1,  320.0),
    (6,  "2026-11-03", "Lámpara",    "Muebles",     2,  40.0),
    (7,  "2026-11-04", "Cuaderno",   "Papelería",   10, 3.5),
    (8,  "2026-11-04", "Lápiz",      "Papelería",   20, 0.8),
    (9,  "2026-11-05", "Monitor",    "Electrónica", 2,  300.0),
    (10, "2026-11-05", "Marcador",   "Papelería",   5,  2.0),
    (11, "2026-11-06", "Estantería", "Muebles",     1,  150.0),
    (12, "2026-11-06", "Audífonos",  "Electrónica", 1,  80.0),
    (13, "2026-11-07", None,         "Papelería",   4,  5.0),    # venta SIN producto
    (14, "2026-11-07", "Cojín",      "Muebles",     -2, 20.0),   # cantidad NEGATIVA
    (15, "2026-11-08", "Tablet",     "Electrónica", 1,  450.0),
    (2,  "2026-11-01", "Mouse",      "Electrónica", 3,  25.0),   # venta DUPLICADA
]
esquema = StructType([
    StructField("id_venta", IntegerType()), StructField("fecha", StringType()),
    StructField("producto", StringType()), StructField("categoria", StringType()),
    StructField("cantidad", IntegerType()), StructField("precio_unitario", DoubleType()),
])
df = spark.createDataFrame(ventas, esquema).withColumn("fecha", F.to_date("fecha"))

# df = df.select("columna_inexistente")  # ERROR_CONTROLADO (ejercicio 3)

df.write.mode("overwrite").option("overwriteSchema", "true").saveAsTable(f"{CAT}.{ESQ}.ventas_bronze")
print("Registros guardados en ventas_bronze:", spark.table(f"{CAT}.{ESQ}.ventas_bronze").count())
display(df)
