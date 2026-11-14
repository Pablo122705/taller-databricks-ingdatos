#!/usr/bin/env bash
set -eo pipefail
REPO="$HOME/taller-databricks-ingdatos"
CAT="workspace"; ESQ="ingenieria_datos_pablo"
EST="$REPO/.estado"; touch "$EST"; source "$EST"
RES="$REPO/resultados"; mkdir -p "$RES"
guardar(){ grep -v "^$1=" "$EST" > "$EST.tmp" || true; echo "$1=$2" >> "$EST.tmp"; mv "$EST.tmp" "$EST"; }
jget(){ python3 -c "import sys,json; d=json.load(sys.stdin); print($1)"; }
ws(){ U=$(databricks current-user me -o json | jget "d['userName']"); echo "/Users/$U/taller_databricks"; }

resumen_run(){ python3 - "$1" << 'PY'
import json, sys, subprocess
d = json.load(open('/tmp/run.json'))
st = d['state']
out = [f"Run {d['run_id']} | resultado: {st.get('result_state', st['life_cycle_state'])} | {st.get('state_message','')}"]
for t in d.get('tasks', []):
    s = t['state']
    dur = (t['end_time'] - t['start_time']) / 1000 if t.get('start_time') and t.get('end_time') else 0
    out.append(f"- {t['task_key']}: {s.get('result_state', s['life_cycle_state'])} | duración {dur:.0f} s | {s.get('state_message','')}")
    if s.get('result_state') == 'FAILED':
        r = subprocess.run(['databricks','jobs','get-run-output',str(t['run_id']),'-o','json'], capture_output=True, text=True)
        try: out.append("    error: " + json.loads(r.stdout).get('error',''))
        except Exception: pass
txt = "\n".join(out); print(txt); open(sys.argv[1],'w').write(txt + "\n")
PY
}

case "${1:-}" in
  schema)
    databricks schemas create "$ESQ" "$CAT" >/dev/null 2>&1 || echo "(el esquema ya existía)"
    databricks schemas get "$CAT.$ESQ" -o json | jget "'Esquema: ' + d['full_name']" ;;
  deploy)
    W=$(ws); databricks workspace mkdirs "$W"
    databricks workspace import-dir "$REPO/notebooks" "$W" --overwrite
    echo "Notebooks en Databricks ($W):"; databricks workspace list "$W" ;;
  tabla)
    T="${2:-ventas_bronze}"
    databricks tables get "$CAT.$ESQ.$T" -o json \
      | jget "'\n'.join(c['name'] + ' : ' + c['type_text'] for c in d['columns'])" | tee "$RES/ej1_columnas_$T.txt" ;;
  export)
    W=$(ws); shift
    for n in "$@"; do
      databricks workspace export "$W/$n" --format JUPYTER --file "$RES/$n.ipynb"
      databricks workspace export "$W/$n" --format HTML --file "$RES/$n.html"
      echo "Exportado: resultados/$n.ipynb y .html"
    done ;;
  job-create)
    sed "s#__WS__#$(ws)#g" "$REPO/jobs/job_ventas.json" > /tmp/job.json
    ID=$(databricks jobs create --json @/tmp/job.json -o json | jget "d['job_id']")
    guardar JOB_ID "$ID"; echo "Job creado: job_ventas_pablo (JOB_ID=$ID)" ;;
  job-run)
    TAG="${2:-exitosa}"
    RUN=$(databricks jobs run-now "$JOB_ID" --no-wait -o json | jget "d['run_id']")
    echo "Ejecución $RUN lanzada. Esperando (2-5 min)..."
    while true; do
      databricks jobs get-run "$RUN" -o json > /tmp/run.json
      ST=$(jget "d['state']['life_cycle_state']" < /tmp/run.json)
      case "$ST" in TERMINATED|INTERNAL_ERROR|SKIPPED) break ;; esac
      echo "  estado: $ST"; sleep 15
    done
    cp /tmp/run.json "$RES/ej3_run_$TAG.json"; resumen_run "$RES/ej3_run_$TAG.txt" ;;
  error-on)
    sed -i 's|^# df = df.select("columna_inexistente")|df = df.select("columna_inexistente")|' "$REPO/notebooks/01_cargar_ventas.py"
    grep -n "columna_inexistente" "$REPO/notebooks/01_cargar_ventas.py"; "$0" deploy >/dev/null; echo "Error controlado ACTIVADO y notebook subido" ;;
  error-off)
    sed -i 's|^df = df.select("columna_inexistente")|# df = df.select("columna_inexistente")|' "$REPO/notebooks/01_cargar_ventas.py"
    grep -n "columna_inexistente" "$REPO/notebooks/01_cargar_ventas.py"; "$0" deploy >/dev/null; echo "Error controlado DESACTIVADO y notebook subido" ;;
  pipeline-create)
    sed "s#__WS__#$(ws)#g" "$REPO/pipelines/pipeline_ventas.json" > /tmp/pl.json
    ID=$(databricks pipelines create --json @/tmp/pl.json -o json | jget "d['pipeline_id']")
    guardar PL_ID "$ID"; echo "Pipeline creado: pipeline_ventas_pablo (PL_ID=$ID)" ;;
  pipeline-run)
    TAG="${2:-ejecucion}"
    UP=$(databricks pipelines start-update "$PL_ID" -o json | jget "d['update_id']")
    echo "Actualización $UP lanzada. Esperando (3-8 min)..."
    while true; do
      S=$(databricks pipelines get-update "$PL_ID" "$UP" -o json | jget "d['update']['state']")
      case "$S" in COMPLETED|FAILED|CANCELED) break ;; esac
      echo "  estado: $S"; sleep 20
    done
    echo "Pipeline $PL_ID | update $UP | estado final: $S" | tee "$RES/ej4_pipeline_$TAG.txt" ;;
  subir)
    cd "$REPO"; git add -A; git commit -m "${2:-avance}" || true; git push -u origin main ;;
  *) echo "Uso: dbx {schema|deploy|tabla|export|job-create|job-run|error-on|error-off|pipeline-create|pipeline-run|subir}" ;;
esac
