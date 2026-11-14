# Taller Databricks – Ingeniería de Datos (EIA 2026-2)

Autor: Pablo López Restrepo (Pablo122705) · Databricks Free Edition, cómputo serverless, catálogo `workspace`, esquema `ingenieria_datos_pablo`.

| Carpeta / archivo | Contenido |
|---|---|
| `respuestas_investigacion.md` | Preguntas de investigación con fuentes |
| `notebooks/` | `01_cargar_ventas`, `01b_leer_ventas`, `02_transformar_ventas`, `03_pipeline_ventas`, `04_agregar_venta` |
| `jobs/job_ventas.json` | Definición del job `job_ventas_pablo` (2 tareas con dependencia) |
| `pipelines/pipeline_ventas.json` | Definición del pipeline `pipeline_ventas_pablo` |
| `resultados/` | Notebooks ejecutados con resultados (.ipynb/.html), conteos, ejecuciones del job y del pipeline, explicaciones |
| `evidencias/` | Capturas que pide el taller |
| `scripts/dbx.sh` | Automatización con Databricks CLI |

## Reproducir
```bash
databricks configure                 # host y token del workspace
bash scripts/dbx.sh schema && bash scripts/dbx.sh deploy
# Ejecutar en Databricks: 01_cargar_ventas, 01b_leer_ventas, 02_transformar_ventas (dos veces)
bash scripts/dbx.sh job-create && bash scripts/dbx.sh job-run exitosa
bash scripts/dbx.sh pipeline-create && bash scripts/dbx.sh pipeline-run antes
```
