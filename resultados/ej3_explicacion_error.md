# Ejercicio 3: Explicación del error controlado

**Error introducido:** en `01_cargar_ventas` se activó la línea `df = df.select("columna_inexistente")`, que pide una columna que no existe en el DataFrame de ventas.

**Qué pasó:** la tarea `cargar_ventas` falló con un error de análisis de Spark (`UNRESOLVED_COLUMN`: no se puede resolver `columna_inexistente`). Como `transformar_ventas` depende de ella con la condición "todas exitosas", no llegó a ejecutarse y quedó con estado **Upstream failed**. Así se evitó transformar datos de una carga que no terminó bien.

**Cómo se identificó la causa:** en el historial (Runs) del job, la ejecución aparecía como *Failed*. Al abrir la tarea en rojo se vio el mensaje de error y la celda exacta del notebook que lo generó. El mismo detalle quedó en `resultados/ej3_run_fallida.txt` (estado y duración por tarea, y mensaje de error).

**Corrección:** se volvió a comentar la línea, se subió de nuevo el notebook y se ejecutó el job. Las dos tareas terminaron en *Succeeded* (`resultados/ej3_run_exitosa.txt`).
