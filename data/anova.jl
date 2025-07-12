using Pkg
Pkg.instantiate()

using CSV, DataFrames, StatsModels  # necesitas StatsModels para la fórmula
using AnovaBase                      # para anova_lm
using AnovaGLM                       # dependencia de AnovaBase

# 1) Lee los datos
df = CSV.read("data.csv", DataFrame)

# 2) Ejecuta ANOVA de un solo paso y obtén un DataFrame
df_anova = anova_lm(@formula(Y ~ GRUPO), df; type = 3, test = FTest)

# 3) Muestra la tabla
println(df_anova)

# 4) Guarda DIRECTAMENTE el DataFrame en CSV
CSV.write("resultados_anova_Julia.csv", df_anova)
