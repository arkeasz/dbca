import pandas as pd
import statsmodels.formula.api as smf
import tracemalloc
tracemalloc.start()
# Lee el mismo CSV que usan los demás
df = pd.read_csv("data.csv")

# Ajusta el modelo de regresión
modelo = smf.ols('Y ~ X1 + X2', data=df).fit()
print(modelo.summary())

# Guarda coeficientes, errores estándar y p-valores en un DataFrame
res_df = pd.DataFrame({
    'coef': modelo.params,
    'std_err': modelo.bse,
    'pvalue': modelo.pvalues
})
res_df.to_csv("resultados_regresion_Python.csv", index=True)
current, peak = tracemalloc.get_traced_memory()
print(f"PEAK_MEMORY:{peak / 1024**2}")