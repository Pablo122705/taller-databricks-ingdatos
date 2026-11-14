# Databricks notebook source
# Pipeline declarativo: Databricks deduce que ventas_por_categoria depende de ventas_limpias
from pyspark import pipelines as dp
from pyspark.sql import functions as F

FUENTE = "workspace.ingenieria_datos_pablo.ventas_bronze"

@dp.materialized_view(name="pipeline_ventas_limpias",
                      comment="Ventas sin duplicados, con producto, cantidad > 0 y precio > 0, con total_venta")
def pipeline_ventas_limpias():
    return (spark.read.table(FUENTE)
            .dropDuplicates()
            .filter(F.col("producto").isNotNull() & (F.trim(F.col("producto")) != ""))
            .filter((F.col("cantidad") > 0) & (F.col("precio_unitario") > 0))
            .withColumn("total_venta", F.round(F.col("cantidad") * F.col("precio_unitario"), 2)))

@dp.materialized_view(name="pipeline_ventas_por_categoria",
                      comment="Valor total vendido por categoría")
def pipeline_ventas_por_categoria():
    return (spark.read.table("pipeline_ventas_limpias")
            .groupBy("categoria")
            .agg(F.round(F.sum("total_venta"), 2).alias("valor_total"), F.count("*").alias("num_ventas")))
