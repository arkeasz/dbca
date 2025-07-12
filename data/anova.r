datos <- read.csv("data.csv")

modelo <- aov(Y ~ GRUPO, data = datos)
print(summary(modelo))

# Guardar tabla ANOVA
write.csv(summary(modelo)[[1]], "resultados_anova_R.csv")
