# Respuestas de investigación – Taller Databricks

## Ejercicio 1
**¿Qué es Unity Catalog?**
Es la capa central de gobierno de datos de Databricks. Organiza los datos en tres niveles (`catalogo.esquema.tabla`), controla quién puede leer o modificar cada objeto, y registra auditoría, linaje y metadatos para encontrar los datos desde cualquier notebook del workspace. En Free Edition viene el catálogo `workspace`.

**¿Diferencia entre un DataFrame de Spark y una tabla Delta?**
Un DataFrame es una estructura de datos distribuida y temporal: vive en la sesión de Spark mientras el código corre y desaparece al terminar. Una tabla Delta es almacenamiento persistente: archivos Parquet más un registro de transacciones (`_delta_log`) que da operaciones ACID, control de esquema e historial de versiones, y queda registrada en el catálogo. Un DataFrame se puede guardar como tabla Delta y una tabla Delta se puede leer como DataFrame.

## Ejercicio 3
**¿Qué es un job y para qué sirve?**
Es la herramienta de orquestación de Databricks: ejecuta automáticamente notebooks, scripts, SQL o pipelines, de forma manual, programada o por evento, con reintentos, notificaciones e historial de ejecuciones.

**¿Qué es una tarea y cómo se diferencia de un job?**
Una tarea es una unidad de trabajo concreta, por ejemplo ejecutar un notebook. El job es el contenedor que agrupa una o varias tareas junto con su configuración (cómputo, horario, parámetros, alertas).

**¿Qué significa establecer dependencias entre tareas?**
Definir el orden: una tarea solo empieza cuando la anterior termina, y bajo una condición (por ejemplo, que haya terminado bien). Así se forma un grafo (DAG). Si la tarea previa falla, la dependiente no se ejecuta y queda como *Upstream failed*.

**¿Qué información del historial permite identificar un fallo?**
El estado de la ejecución y de cada tarea (Succeeded, Failed, Upstream failed), la hora de inicio y fin y la duración, el mensaje de error con su traza, y la salida del notebook en la celda que falló.

## Ejercicio 4
**¿Qué es un pipeline de datos y cuáles son sus etapas?**
Es un flujo automatizado que lleva los datos desde la fuente hasta un destino listo para usar. Etapas habituales: ingesta, limpieza y transformación, validación de calidad, y publicación o carga (por ejemplo, el modelo bronze → silver → gold).

**¿Qué significa que sea declarativo?**
Que se define *qué* conjunto de datos se quiere (cada tabla o vista como una consulta) y no *cómo* ni en qué orden ejecutarlo. Databricks deduce las dependencias, el orden, la infraestructura y cómo actualizar los resultados.

**¿Diferencia entre un job con notebooks y un pipeline declarativo?**
En el job, uno programa pasos imperativos: escribe el código que crea las tablas, define a mano el orden entre tareas y se ocupa de la idempotencia (por ejemplo, con overwrite). En el pipeline declarativo solo se definen los conjuntos de datos; Databricks construye el grafo, administra las dependencias y el estado y actualiza los resultados. Un job puede incluso ejecutar un pipeline como una de sus tareas.

## Fuentes
- Databricks Docs – Unity Catalog: https://docs.databricks.com/aws/en/data-governance/unity-catalog/
- Databricks Docs – Delta Lake: https://docs.databricks.com/aws/en/delta/
- Apache Spark – Spark SQL, DataFrames and Datasets Guide: https://spark.apache.org/docs/latest/sql-programming-guide.html
- Databricks Docs – Lakeflow Jobs: https://docs.databricks.com/aws/en/jobs/
- Databricks Docs – Lakeflow Spark Declarative Pipelines: https://docs.databricks.com/aws/en/ldp/
- Databricks Docs – Develop pipeline code with Python: https://docs.databricks.com/aws/en/ldp/developer/python-dev
- Databricks Docs – Free Edition limitations: https://docs.databricks.com/aws/en/getting-started/free-edition-limitations
