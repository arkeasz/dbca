# install.packages(c("readr", "dplyr", "ggplot2", "car", "nortest"))
library(readr)
library(nortest)
library(dplyr)
library(ggplot2)
library(car)

# 1) Importar datos y preparar factores
df <- read_csv("benchmarks_results.csv")
df$Lenguaje <- factor(df$Lenguaje, levels = c("R", "Python", "Julia"))
df$Analisis <- factor(df$Analisis, levels = c("Regresión", "ANOVA"))

df$Tiempo <- log(df$Tiempo)

# Repetir ANOVA con Log(Tiempo)
aov_time <- aov(Tiempo ~ Lenguaje * Analisis, data = df)
summary(aov_time)

# Verificar supuestos otra vez
ad.test(residuals(aov_time))  
leveneTest(Tiempo ~ Lenguaje * Analisis, data = df)

# Revisar Q-Q plot para la nueva variable
qqnorm(residuals(aov_time))
qqline(residuals(aov_time), col = "red")

# Nuevo post-hoc si mejora
TukeyHSD(aov_time)

TukeyHSD(aov_time)
ggplot(df, aes(x = Lenguaje, y = Tiempo, fill = Analisis)) +
  geom_boxplot() +
  labs(title = "Distribución de Tiempo por Lenguaje y Análisis", y = "Tiempo (s)")