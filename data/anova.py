import tracemalloc
import pandas as pd
import statsmodels.formula.api as smf
import statsmodels.stats.api as sms

tracemalloc.start()
df = pd.read_csv("data.csv")

modelo = smf.ols('Y ~ C(GRUPO)', data=df).fit()
anova_table = sms.anova_lm(modelo, typ=2)

anova_table.to_csv("resultados_anova_Python.csv")
current, peak = tracemalloc.get_traced_memory()
print(f"PEAK_MEMORY:{peak / 1024**2}")
