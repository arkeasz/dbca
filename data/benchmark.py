import subprocess
import sys
import re
import json
import numpy as np
import pandas as pd
from pathlib import Path

# Configuración experimental\ nREPLICAS = 30
WARMUP_RUNS = 3
REPLICAS = 30
# Lista de tareas con metadatos:
# (Lenguaje, Análisis, Comando, Ruta al script, Observaciones)
tasks = [
    ("R",      "Regresión", "Rscript regresion.R", "regresion.R", "lm()"),
    ("Python", "Regresión", "py regresion.py",      "regresion.py",  "statsmodels"),
    ("Julia",  "Regresión", "julia regresion.jl",   "regresion.jl", "GLM.jl"),
    ("R",      "ANOVA",      "Rscript anova.R",      "anova.R",      "aov()"),
    ("Python", "ANOVA",      "py anova.py",          "anova.py",      "statsmodels"),
    ("Julia",  "ANOVA",      "julia anova.jl",       "anova.jl",      "GLM.jl"),
]

def run_hyperfine_benchmark():
    """Ejecuta Hyperfine exportando a JSON."""
    cmd_list = [
        "hyperfine",
        "--show-output",
        "--warmup", str(WARMUP_RUNS),
        "--runs",   str(REPLICAS),
        "--export-json", "tiempos.json",
    ] + [t[2] for t in tasks]

    print(f"Ejecutando Hyperfine con {REPLICAS} réplicas por comando (export JSON)...")
    subprocess.run(cmd_list, check=True)
    print("-> 'tiempos.json' generado.")

import subprocess
import re
import numpy as np

def measure_memory_usage():
    """Mide el pico real de memoria (RSS) con '/usr/bin/time -v' para todos los comandos."""
    mem_results = {}
    print("\nMedición de memoria:")
    for lang, analysis, cmd, *_ in tasks:
        print(f"  - {cmd}")
        try:
            # Envuelve el comando en /usr/bin/time para que informe el pico RSS
            wrapped = f"/usr/bin/time -v {cmd}"
            # El comando time emite su salida en stderr
            result = subprocess.run(wrapped.split(), capture_output=True, text=True, timeout=300)
            out = result.stderr  # /usr/bin/time -v va a stderr

            # Busca la línea "Maximum resident set size (kbytes): <n>"
            m = re.search(r"Maximum resident set size.*: (\d+)", out)
            if m:
                # Convertir kbytes a MBytes
                rss_mb = int(m.group(1)) / 1024.0
            else:
                rss_mb = np.nan

            mem_results[cmd] = rss_mb

        except Exception as e:
            print(f"Error en {cmd}: {e}")
            mem_results[cmd] = np.nan
    print(mem_results)
    return mem_results



# def measure_memory_usage():
#     """Mide el uso de memoria para cada tarea."""
#     mem_results = {}
#     print("\nMedición de memoria:")
#     for lang, analysis, cmd, *_ in tasks:
#         try:
#             result = subprocess.run(cmd.split(), capture_output=True, text=True, timeout=300)
#             out = result.stdout + result.stderr
#             pat = r"MEM_USAGE:(\d+\.\d+)" if lang=="R" else (r"PEAK_MEMORY:(\d+\.\d+)" if lang=="Python" else r"MAX_MEMORY:(\d+\.\d+)")
#             m = re.search(pat, out)
#             mem_results[cmd] = float(m.group(1)) if m else np.nan
#         except:
#             mem_results[cmd] = np.nan
#     return mem_results


def count_lines(path):
    """Cuenta líneas de código no vacías."""
    p = Path(path)
    if not p.exists(): return np.nan
    return sum(1 for l in p.read_text(encoding='utf-8').splitlines() if l.strip())


def generate_summary_table(mem_results):
    """Lee tiempos.json y genera tabla resumen con métricas unificadas."""
    data = json.load(open("tiempos.json"))
    # Construir DataFrame de tiempos por réplica
    records = []
    for res in data["results"]:
        cmd = res["command"]
        meta = next(t for t in tasks if t[2]==cmd)
        lang, analysis, _, script, obs = meta
        for t in res["times"]:
            records.append({"Lenguaje":lang, "Análisis":analysis, "Tiempo":t, "Comando":cmd})
    df_time = pd.DataFrame.from_records(records)

    # DataFrame de memoria
    df_time["Memoria"] = df_time["Comando"].map(mem_results)
    # Líneas y observaciones
    df_time["Líneas"] = df_time["Comando"].map({t[2]:count_lines(t[3]) for t in tasks})
    df_time["Obs"]     = df_time["Comando"].map({t[2]:t[4] for t in tasks})

    # Agrupar para resumen
    summary = df_time.groupby(["Lenguaje","Análisis"]).agg(
        Tiempo_mu  = ("Tiempo", "mean"),
        Tiempo_sd  = ("Tiempo", "std"),
        Memoria_mu = ("Memoria", "mean"),
        Memoria_sd = ("Memoria", "std"),
        Líneas     = ("Líneas", "first"),
        Obs        = ("Obs",     "first")
    ).reset_index()

    # Calcular deltas vs R
    ref = summary[summary.Lenguaje=="R"][['Análisis','Tiempo_mu','Memoria_mu']].set_index('Análisis')
    summary['ΔTiempo(%)'] = summary.apply(lambda r: (r.Tiempo_mu-ref.loc[r.Análisis,'Tiempo_mu'])/ref.loc[r.Análisis,'Tiempo_mu']*100 if r.Lenguaje!='R' else 0, axis=1)
    summary['ΔMemoria(%)']= summary.apply(lambda r: (r.Memoria_mu-ref.loc[r.Análisis,'Memoria_mu'])/ref.loc[r.Análisis,'Memoria_mu']*100 if r.Lenguaje!='R' else 0, axis=1)

    # Reordenar y renombrar columnas
    cols = ["Lenguaje","Análisis",
            "Tiempo_mu","Tiempo_sd","ΔTiempo(%)",
            "Memoria_mu","Memoria_sd","ΔMemoria(%)",
            "Líneas","Obs"]
    summary.columns = ["Lenguaje","Análisis",
                       "Tiempo μ(s)","Tiempo σ(s)","ΔTiempo (%)",
                       "Memoria μ(MB)","Memoria σ(MB)","ΔMemoria (%)",
                       "Líneas de código","Observaciones"]
    return summary

def generate_datasets(mem_results):
    """Lee tiempos.json y genera:
       - df_raw: todos los tiempos por réplica (180 filas)
       - df_summary: la tabla resumida (6 filas)
    """
    data = json.load(open("tiempos.json"))
    raw_records = []
    for res in data["results"]:
        cmd = res["command"]
        lang, analysis, _, script, obs = next(t for t in tasks if t[2] == cmd)
        for replica_index, t in enumerate(res["times"], start=1):
            raw_records.append({
                "Lenguaje": lang,
                "Análisis": analysis,
                "Replica": replica_index,
                "Tiempo": t,
                "Memoria": mem_results[cmd],
                "Líneas": count_lines(script),
                "Obs": obs
            })
    df_raw = pd.DataFrame(raw_records)

    # Guarda los datos “brutos”
    df_raw.to_csv("tiempos_replicas.csv", index=False, encoding="utf-8")

    # Ahora el resumen
    summary = (
        df_raw
        .groupby(["Lenguaje", "Análisis"])
        .agg(
            Tiempo_mu  = ("Tiempo", "mean"),
            Tiempo_sd  = ("Tiempo", "std"),
            Memoria_mu = ("Memoria", "mean"),
            Memoria_sd = ("Memoria", "std"),
            Líneas     = ("Líneas", "first"),
            Obs        = ("Obs",     "first")
        )
        .reset_index()
    )

    # Delas vs R
    ref = summary[summary.Lenguaje == "R"].set_index("Análisis")
    summary["ΔTiempo (%)"] = summary.apply(
        lambda r: 0 if r.Lenguaje=="R" else
                  (r.Tiempo_mu - ref.loc[r.Análisis,"Tiempo_mu"])/ref.loc[r.Análisis,"Tiempo_mu"]*100,
        axis=1
    )
    summary["ΔMemoria (%)"] = summary.apply(
        lambda r: 0 if r.Lenguaje=="R" else
                  (r.Memoria_mu - ref.loc[r.Análisis,"Memoria_mu"])/ref.loc[r.Análisis,"Memoria_mu"]*100,
        axis=1
    )

    # Renombrar columnas para tu CSV final
    summary = summary.rename(columns={
        "Tiempo_mu":    "Tiempo μ(s)",
        "Tiempo_sd":    "Tiempo σ(s)",
        "Memoria_mu":   "Memoria μ(MB)",
        "Memoria_sd":   "Memoria σ(MB)",
        "Líneas":       "Líneas de código",
        "Obs":          "Observaciones"
    })

    # Guarda el resumen
    summary.to_csv("benchmark_summary_full.csv", index=False, encoding="utf-8")
    return df_raw, summary

def main():
    run_hyperfine_benchmark()
    mem = measure_memory_usage()
    df_raw, df_summary = generate_datasets(mem)
    print("Datos brutos (primeras filas):")
    print(df_raw.head())
    print("\nResumen final:")
    print(df_summary)



# def main():
#     run_hyperfine_benchmark()
#     mem = measure_memory_usage()
#     summary = generate_summary_table(mem)
#     summary.to_csv("benchmark_summary_full.csv", index=False)
#     print(summary)

if __name__=="__main__":
    main()

#     Resumen final:
#   Lenguaje   Análisis  Tiempo μ(s)  Tiempo σ(s)  ...  Líneas de código  Observaciones  ΔTiempo (%) ΔMemoria (%)     
# 0    Julia      ANOVA    18.621625     2.575255  ...                27         GLM.jl   976.577824          NaN     
# 1    Julia  Regresión    63.525970    16.172241  ...                59         GLM.jl  3175.214081          NaN     
# 2   Python      ANOVA     4.899266     0.656203  ...                11    statsmodels   183.242802   -98.950997     
# 3   Python  Regresión     4.952344     0.552378  ...                18    statsmodels   155.328416   -98.567562     
# 4        R      ANOVA     1.729705     0.412167  ...                 7          aov()     0.000000     0.000000     
# 5        R  Regresión     1.939597     0.404531  ...                 9           lm()     0.000000     0.000000     
#   Lenguaje   Análisis  Tiempo μ(s)  Tiempo σ(s)  ...  Líneas de código  Observaciones  ΔTiempo (%) ΔMemoria (%)     
# 0    Julia      ANOVA    18.621625     2.575255  ...                27         GLM.jl   976.577824          NaN     
# 1    Julia  Regresión    63.525970    16.172241  ...                59         GLM.jl  3175.214081          NaN     
# 2   Python      ANOVA     4.899266     0.656203  ...                11    statsmodels   183.242802   -98.950997     
# 3   Python  Regresión     4.952344     0.552378  ...                18    statsmodels   155.328416   -98.567562     
# 4        R      ANOVA     1.729705     0.412167  ...                 7          aov()     0.000000     0.000000     
# 5        R  Regresión     1.939597     0.404531  ...                 9           lm()     0.000000     0.000000     

# [6 rows x 10 columns]