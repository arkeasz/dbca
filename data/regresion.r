library(pryr)
# Librerías base, no necesitas paquetes externos
datos <- read.csv("data.csv")

modelo <- lm(Y ~ X1 + X2, data = datos)
print(summary(modelo))

# Guardar coeficientes
write.csv(summary(modelo)$coefficients, "resultados_regresion_R.csv")

mem_usage <- mem_used() / 1024^2  # Convertir a MB
cat(paste0("MEM_USAGE:", mem_usage, "\n"))