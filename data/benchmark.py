import subprocess
import csv
import sys

# List of (Language, Analysis, Command, Memory, Precision, Lines, Observations)
tasks = [
    ("R", "Regresión", "Rscript regresion.R", 50.0, 0, 3, "lm()"),
    ("Python", "Regresión", "py regresion.py", 80.0, 0, 5, "statsmodels"),
    ("Julia", "Regresión", "julia regresion.jl", 30.0, 0, 4, "GLM.jl"),
    ("R", "ANOVA", "Rscript anova.R", 50.0, 0, 3, "aov()"),
    ("Python", "ANOVA", "py anova.py", 80.0, 0, 5, "statsmodels"),
    ("Julia", "ANOVA", "julia anova.jl", 30.0, 0, 4, "GLM.jl"),
]

# Prepare hyperfine command
cmd_list = ["hyperfine", "--show-output", "--warmup", "3", "--export-csv", "tiempos.csv"] + [task[2] for task in tasks]

print("Ejecutando hyperfine con comandos:")
for lang, analysis, cmd, *_ in tasks:
    print(f"  - {cmd}")

# Run hyperfine
result = subprocess.run(cmd_list, capture_output=True, text=True)
if result.returncode != 0:
    print("Error ejecutando hyperfine:", result.stderr, file=sys.stderr)
    sys.exit(1)

print(result.stdout)
print("Benchmark terminado. Resultados guardados en tiempos.csv")

# Read tiempos.csv
tiempos_data = {}
with open("tiempos.csv", newline="") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        command = row["command"]
        mean_time = float(row["mean"])
        tiempos_data[command] = mean_time

# Build final table
tabla = []
for lang, analysis, cmd, mem, prec, lines, obs in tasks:
    time_val = tiempos_data.get(cmd, None)
    tabla.append([lang, analysis, time_val, mem, prec, lines, obs])

# Save final table
output_file = "tabla_resultados.csv"
with open(output_file, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Lenguaje", "Análisis", "Tiempo(s)", "Memoria(MB)", "Precisión(Δ vs R)", "Líneas de código", "Observaciones"])
    writer.writerows(tabla)

print(f"Tabla final guardada como {output_file} ✅")
