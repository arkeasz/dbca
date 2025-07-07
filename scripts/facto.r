# # Propuesta de Diseño Estadístico y Rol de Media y Desviación Estándar

# ## 1. Diseño Experimental Sugerido

# - Diseño completamente aleatorizado (CRD)  
#   - Cada tratamiento (nivel de cobre) se asigna al azar a las macetas.  
#   - Garantiza que las variaciones del ambiente no sesguen los resultados.  
#   - Facilita el uso de ANOVA de un solo factor para comparar medias entre niveles de cobre.


# Comparar respuestas de las plantas entre los cinco niveles de Cu

# Contrastar hipótesis mediante ANOVA de un factor.

# Verificar supuestos del ANOVA

# Normalidad de residuos (Shapiro–Wilk).

# Homogeneidad de varianzas (Levene o Bartlett).

# Realizar comparaciones múltiples post-hoc

# Si ANOVA es significativo, aplicar testeos por pares (Tukey HSD o LSD).

# Cuantificar el tamaño del efecto y la potencia estadística

# A partir de la media y la desviación estándar definir si el experimento detecta diferencias relevantes.

# Modelar la relación dosis–respuesta

# Ajustar regresión (lineal o no lineal) para predecir la medida de toxicidad según la concentración de Cu.

# 2. **Modelar la relación dosis–respuesta**  
#    - Construir modelos de regresión múltiple por pasos (stepwise) para predecir concentración de cobre en hojas a partir de fracciones extractables del suelo.  
#    - Evaluar ajuste del modelo mediante R² y significancia de coeficientes.

# 3. **Control de variabilidad experimental**  
#    - Detectar fuentes de error (entre réplicas, entre ensayos).  
#    - Optimizar número de réplicas para alcanzar potencia estadística deseada.

# ---

# ## 3. Utilidad de la Media y la Desviación Estándar

# - **Media ( x̄ )**  
#   - Representa el valor central de un conjunto de mediciones (concentración, peso, altura).  
#   - Base para comparar tratamientos y calcular la magnitud del efecto.

# - **Desviación estándar (SD)**  
#   - Mide la dispersión de los datos alrededor de la media.  
#   - Un SD pequeño indica alta consistencia entre réplicas; uno grande revela variabilidad elevada.  
#   - Es esencial para:
#     - Verificar supuestos de homogeneidad (Levene).  
#     - Construir intervalos de confianza.  
#     - Evaluar la precisión y reproducibilidad de los resultados.

# ---

# ## 4. Aplicaciones Prácticas

# - Seleccionar el número mínimo de réplicas necesarias (basado en SD) para garantizar detección de diferencias reales.  
# - Ajustar factores de cultivo o sistemas de remediación al conocer qué niveles de cobre producen variabilidad crítica en el rendimiento.  
# - Validar y comparar modelos predictivos al observar la dispersión de residuos (diferencia entre valores medidos y predichos).

# ---

# ¿Te gustaría profundizar en cómo calcular la potencia estadística en función del SD o explorar ejemplos de análisis factorial?


# install.packages("car")
# install.packages("readxl");
# install.packages("lmtest")
library(lmtest)

library(readxl)
library(car)


# https://www.mdpi.com/2071-1050/11/22/6215?utm_source=chatgpt.com#table_body_display_sustainability-11-06215-t001

data <- read_xlsx("./scripts/COBRE.xlsx")
# View(data)

attach(data)
names(data)

# Numero de Ensayos
data$TRIAL <- as.factor(data$TRIAL)
# Nivel de Concentración de cobre en el suelo
data$NIVEL <- as.factor(data$NIVEL)
# Cada valor representa la media
data$MEDIA <- as.numeric(data$MEDIA)

class(data$TRIAL)
class(data$MEDIA)
class(data$NIVEL)

model <- aov(MEDIA ~ TRIAL + NIVEL, data = data)

res <- residuals(model)
summary(res)


shapiro.test(res)

qqnorm(res)
qqline(res)

# prueba de independencia
#prueba de independencia de los residuos(DURBIN WATSON), Ho: hay independencia de residuos, H1: no hay
#pv>0.05 no se rechaza HO
dwtest(MEDIA~TRIAL + NIVEL, data= data)
# DURBIN WATSON(AUTOCORRELACION ENTRE RESIDUOS EN RL: DW=2 NO HAY AUTOC, DW<2 
#HAY AUTOCORRELACION POSITIVA, DW>2 HAY CORRELACION NEGATIVA, DW= 0 AUTOCORRELACIÓN 
#POSITIVA MUY FUERTE, DW= 4 AUTOCORRELACION NEGATIVA MUY FUERTE)
durbinWatsonTest(aov(MEDIA~TRIAL+NIVEL
, data= data))

plot(resid(aov(MEDIA~TRIAL+NIVEL, data=data)),type= "p", col= "blue", ylab= "residuos", xlab= "Observación", main= "Residuos vs Orden de Orservación")
abline(h=0, lty=2, col="red")

install.packages("ggplot2")
library(ggplot2)
acf(resid(aov(MEDIAS~TRIAL+NIVEL, data= data)), main = "ACF DE LOS RESIDUOS")

leveneTest(MEDIAS~TRIAL, data =data, center= mean)

leveneTest(MEDIAS~NIVEL, data =data, center= mean)