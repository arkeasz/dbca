import pandas as pd
import statsmodels.formula.api as smf
import statsmodels.stats.api as sms

df = pd.read_csv("data.csv")

modelo = smf.ols('Y ~ C(GRUPO)', data=df).fit()
anova_table = sms.anova_lm(modelo, typ=2)
print(anova_table)

anova_table.to_csv("resultados_anova_Python.csv")
