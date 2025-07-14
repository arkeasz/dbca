library(pryr)
datos <- read.csv("data.csv")
modelo <- aov(Y ~ GRUPO, data = datos)
print(summary(modelo))
write.csv(summary(modelo)[[1]], "resultados_anova_R.csv")
mem_usage <- mem_used() / 1024^2  
cat(paste0("MEM_USAGE:", mem_usage, "\n"))