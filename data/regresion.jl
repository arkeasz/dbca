
import Pkg
Pkg.instantiate()

using CSV, DataFrames, GLM

df = CSV.read("data.csv", DataFrame)

modelo = lm(@formula(Y ~ X1 + X2), df)
println(coeftable(modelo))

CSV.write("resultados_regresion_Julia.csv", coeftable(modelo))
