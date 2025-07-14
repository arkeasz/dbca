library(dplyr)
library(ggplot2)
library(car)
library(emmeans)
library(peakRAM)

# 1) Importar datos y preparar factores
df <- read_csv("benchmark_results.csv") %>%
  mutate(
    Lenguaje = factor(Lenguaje, levels = c("R", "Python", "Julia")),
    Analisis = factor(Análisis, levels = c("Regresión", "ANOVA"))
  )

# 2) ANOVA de dos vías para Tiempo (con medición de memoria y tiempo interno)
mem_time <- peakRAM({
  tiempo_time <- system.time(
    aov_time <- aov(Tiempo ~ Lenguaje * Analisis, data = df)
  )
})
print(mem_time)
summary(aov_time)

# Supuestos para Tiempo
shapiro.test(residuals(aov_time))        # Normalidad
leveneTest(Tiempo ~ Lenguaje * Analisis, data = df)  # Homogeneidad

# Post-hoc para Tiempo
posthoc_time <- emmeans(aov_time, pairwise ~ Lenguaje | Analisis, adjust = "tukey")
print(posthoc_time)

# 3) ANOVA de dos vías para Memoria
mem_mem <- peakRAM({
  tiempo_mem <- system.time(
    aov_mem <- aov(Memoria ~ Lenguaje * Analisis, data = df)
  )
})
print(mem_mem)
summary(aov_mem)

# Supuestos para Memoria
shapiro.test(residuals(aov_mem))
leveneTest(Memoria ~ Lenguaje * Analisis, data = df)

# Post-hoc para Memoria
posthoc_mem <- emmeans(aov_mem, pairwise ~ Lenguaje | Analisis, adjust = "tukey")
print(posthoc_mem)

# 4) MANOVA combinada (Tiempo + Memoria)
manova_res <- Manova(manova(cbind(Tiempo, Memoria) ~ Lenguaje * Analisis, data = df), test = "Pillai")
summary(manova_res)

# 5) Gráficos de caja
ggplot(df, aes(x = Lenguaje, y = Tiempo, fill = Analisis)) +
  geom_boxplot() + labs(title = "Boxplot de Tiempo")

ggplot(df, aes(x = Lenguaje, y = Memoria, fill = Analisis)) +
  geom_boxplot() + labs(title = "Boxplot de Memoria")