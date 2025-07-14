---
theme: default
class: text-center
highlighter: shiki
lineNumbers: true
# colorSchema: dark
info: |
  ### Comparación R, Python y Julia en ANOVA y Regresión Lineal
  
  Análisis comparativo de rendimiento y eficiencia entre lenguajes de programación estadística
drawings:
  persist: false
transition: slide-left
title: Comparación R, Python y Julia en ANOVA y Regresión Lineal
---

<div class="flex flex-col items-center justify-center h-full bg-gray-800 text-white p-6 rounded-lg shadow-lg">
  <h2 class="text-2xl font-bold mb-2">Comparación R, Python y Julia</h2>
  <h3 class="text-xl mb-2">ANOVA y Regresión Lineal</h3>

<!-- ## Comparación R, Python y Julia
### ANOVA y Regresión Lineal -->

</div>

**Antonio Rafael Arias Romero**

Universidad Nacional del Callao

Escuela Profesional de Física
---

# Introducción

<div class="grid grid-cols-1 gap-4">

En el análisis de datos, los lenguajes de programación son herramientas fundamentales para investigadores y profesionales:

- **R, Python y Julia** destacan por su adopción y capacidad analítica
- Diferencias en **sintaxis, paradigmas y optimización**
- Impacto directo en **tiempo de ejecución, memoria y precisión**
- Procedimientos estadísticos: **regresión lineal y ANOVA**

</div>
---

# Objetivos

<div class="grid place-items-center h-full">

<div class="grid grid-cols-3 gap-4">

<div class="bg-green-50 p-4 rounded-lg">
<h3 class="text-green-800 font-bold">⏱️ Tiempo de Ejecución</h3>
<p class="text-green-700">Variación entre R, Python y Julia en regresión lineal múltiple y ANOVA</p>
</div>

<div class="bg-blue-50 p-4 rounded-lg">
<h3 class="text-blue-800 font-bold">🎯 Precisión Numérica</h3>
<p class="text-blue-700">Diferencias en coeficientes, errores estándar y valores p (R como referencia)</p>
</div>

<div class="bg-purple-50 p-4 rounded-lg">
<h3 class="text-purple-800 font-bold">💻 Complejidad Sintáctica</h3>
<p class="text-purple-700">Líneas de código y facilidad de implementación</p>
</div>

</div>

</div>

---

# Conjunto de Datos

<div class="grid grid-cols-1 gap-4">

## 📊 Metodología Experimental

- **Archivo común**: `data.csv` leído por todos los lenguajes
- **Métricas evaluadas**:
  - Tiempo de ejecución (`system.time`, `time`)
  - Precisión numérica (vs. R como referencia)
  - Facilidad de uso (líneas de código)

<div class="bg-gray-50 text-blue p-4 rounded-lg mt-4">
<h3 class="font-bold">Procedimientos</h3>
<ul>
<li><strong>ANOVA</strong>: Mismo modelo de regresión con factor</li>
<li><strong>Regresión Lineal</strong>: Modelo lineal múltiple</li>
</ul>
</div>

</div>

---

# Implementación en R

<div class="grid grid-cols-1 gap-4">

##### 🔵 Características R

- **Funciones**: `lm()` para regresión, `aov()` para ANOVA
- **Sintaxis**: Muy concisa (1-2 líneas por modelo)
- **Resultados**: Estadísticos completos con `summary()`

```r {all}
# Leer datos
datos <- read.csv("data.csv")

# ANOVA
modelo <- aov(Y ~ GRUPO, data = datos)
print(summary(modelo))

# Regresión lineal múltiple
modelo <- lm(Y ~ X1 + X2, data = datos)
print(summary(modelo))
```

<div class="bg-gray-800 p-3 rounded-lg mt-4 text-green-400">
<strong>✅ Ventaja:</strong> Sintaxis vectorizada y funciones estadísticas integradas
</div>

</div>

---

# Implementación en Python

<div class="grid grid-cols-1 gap-4">

##### 🟡 Características Python

- **Librerías**: `pandas` + `statsmodels`
- **Sintaxis**: Clara y declarativa
- **Flexibilidad**: Amplio ecosistema de paquetes

```python {all}
import pandas as pd
import statsmodels.formula.api as smf
import statsmodels.stats.api as sms

# Leer datos
df = pd.read_csv("data.csv")

# Regresión lineal múltiple
modelo = smf.ols('Y ~ X1 + X2', data=df).fit()
print(modelo.summary())

# ANOVA
modelo = smf.ols('Y ~ C(GRUPO)', data=df).fit()
anova_table = sms.anova_lm(modelo, typ=2)
```

<div class="bg-gray-800 p-3 rounded-lg mt-4 text-yellow-400">
<strong>✅ Ventaja:</strong> Ecosistema extenso y sintaxis expresiva
</div>

</div>

---

# Implementación en Julia

<div class="grid grid-cols-1 gap-4">

##### 🟣 Características Julia

- **Librerías**: `GLM.jl` + `DataFrames.jl`
- **Rendimiento**: Compilación JIT
- **Sintaxis**: Similar a R, expresiva

```julia {all}
using CSV, DataFrames, GLM, StatsModels
# Leer datos
df = CSV.read("data.csv", DataFrame)

# Regresión lineal múltiple
modelo = lm(@formula(Y ~ X1 + X2), df)
println(coeftable(modelo))

# ANOVA (implementación manual)
model = lm(@formula(Y ~ GRUPO), df)
```

<div class="bg-gray-800 p-3 rounded-lg mt-4 text-purple-400">
</div>

</div>

---

# Diseño Experimental

<div class="grid grid-cols-1 gap-4">

###### Estructura del Experimento

| Lenguaje | Análisis | Réplica | Tiempo | Líneas | Observación |
|----------|----------|---------|---------|--------|-------------|
| R        | Regresión| 1       | 2.8464  | 9      | lm()        |

<div class="grid grid-cols-2 gap-4 mt-4">

<div class="bg-green-50 p-4 rounded-lg">
<h3 class="text-green-800 font-bold">Factores</h3>
<ul class="text-green-700">
<li><strong>Lenguaje:</strong> R, Python, Julia</li>
<li><strong>Análisis:</strong> Regresión, ANOVA</li>
<li><strong>Réplicas:</strong> 30 por combinación</li>
</ul>
</div>

<div class="bg-blue-50 p-4 rounded-lg">
<h3 class="text-blue-800 font-bold">Total</h3>
<ul class="text-blue-700">
<li><strong>Combinaciones:</strong> 3 × 2 = 6</li>
<li><strong>Observaciones:</strong> 180 filas</li>
<li><strong>Variable respuesta:</strong> Tiempo</li>
</ul>
</div>

</div>

</div>

---

# Hipótesis y Modelo

<div class="grid grid-cols-1 gap-4">

######  Hipótesis Estadísticas

<div class="grid grid-cols-2 gap-4">

<div class="bg-red-50 p-3 rounded-lg">
<h5 class="text-red-800 font-bold">H₀ (Nula)</h5>
<p class="text-red-700 text-sm">No existen diferencias significativas entre lenguajes en tiempo de ejecución</p>
</div>

<div class="bg-green-50 p-3 rounded-lg">
<h5 class="text-green-800 font-bold">H₁ (Alternativa)</h5>
<p class="text-green-700 text-sm">Existen diferencias significativas entre lenguajes</p>
</div>

</div>

###### Modelo Estadístico

$$Y_{ijr} = \mu + \alpha_i + \beta_j + (\alpha\beta)_{ij} + \varepsilon_{ijr}$$
<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem;">
<div>

- $Y_{ijr}$: Tiempo de respuesta
- μ: Media global
- $α_i$: Efecto del lenguaje i

</div>
<div>

- $β_j$: Efecto del análisis j
- $(αβ)_{ij}$: Interacción
- $\epsilon_{ijr}$: Error aleatorio

</div>
</div>

</div>

<style>
  .slidev-layout p  {
    margin: 0;
    padding: 0;
  }
</style>
---

# Preparación de Datos

<div class="grid grid-cols-1 gap-4">

###### Procesamiento en R

```r {all}
# Instalación de paquetes
install.packages(c("dplyr", "ggplot2", "car", "nortest", "readxl"))
# Carga de librerías
library(dplyr)
library(ggplot2)
library(car)
library(readxl)
library(nortest)

# Importación y factorización
df <- read_xlsx("benchmarks_results.xlsx")
df$Lenguaje <- factor(df$Lenguaje, levels = c("R", "Python", "Julia"))
df$Analisis <- factor(df$Analisis, levels = c("Regresión", "ANOVA"))
```

<div class="bg-gray-800 p-4 rounded-lg mt-4 text-orange-400">
<h5 class="text-orange-300 font-bold"> Transformación Logarítmica</h5>
<p>Se aplicó <code class="bg-gray-700 px-2 py-1 rounded">log()</code> para estabilizar varianza y mejorar normalidad</p>
</div>

</div>

---

# Resultados ANOVA

<!-- <div class="grid grid-cols-1 gap-4"> -->

###### ANOVA de Dos Vías

```r {all}
aov_time <- aov(Tiempo ~ Lenguaje * Analisis, data = df)
summary(aov_time)
```

<div class="bg-gray-800 p-2 rounded-lg mt-4">
<table class="w-full text-sm">
<thead class="bg-gray-700">
<tr class="text-gray-300">
<th class="p-2 text-left">Factor</th>
<th class="p-2 text-center">Df</th>
<th class="p-2 text-center">Sum Sq</th>
<th class="p-2 text-center">Mean Sq</th>
<th class="p-2 text-center">F value</th>
<th class="p-2 text-center">Pr(>F)</th>
</tr>
</thead>
<tbody class="text-gray-300">
<tr class="bg-gray-800">
<td class="p-2 font-mono">Lenguaje</td>
<td class="p-2 text-center">2</td>
<td class="p-2 text-center">278.74</td>
<td class="p-2 text-center">139.37</td>
<td class="p-2 text-center text-red-400">2357.0</td>
<td class="p-2 text-center text-red-400">&lt;2e-16 ***</td>
</tr>
<tr class="bg-gray-900">
<td class="p-2 font-mono">Analisis</td>
<td class="p-2 text-center">1</td>
<td class="p-2 text-center">7.19</td>
<td class="p-2 text-center">7.19</td>
<td class="p-2 text-center text-red-400">121.7</td>
<td class="p-2 text-center text-red-400">&lt;2e-16 ***</td>
</tr>
<tr class="bg-gray-800">
<td class="p-2 font-mono">Lenguaje:Analisis</td>
<td class="p-2 text-center">2</td>
<td class="p-2 text-center">12.36</td>
<td class="p-2 text-center">6.18</td>
<td class="p-2 text-center text-red-400">104.5</td>
<td class="p-2 text-center text-red-400">&lt;2e-16 ***</td>
</tr>
<tr class="bg-gray-900">
<td class="p-2 font-mono">Residuals</td>
<td class="p-2 text-center">174</td>
<td class="p-2 text-center">10.29</td>
<td class="p-2 text-center">0.06</td>
<td class="p-2 text-center">-</td>
<td class="p-2 text-center">-</td>
</tr>
</tbody>
</table>
</div>

<div class="bg-red-900 p-4 rounded-lg mt-4 border border-red-700">
<h3 class="text-red-300 font-bold text-sm">Todos los efectos son altamente significativos (p < 0.001)</h3>
</div>

<!-- </div> -->

---

# Verificación de Supuestos

<div class="grid grid-cols-2 gap-8">
  <!-- Columna izquierda - Texto -->
<div class="grid grid-cols-1 gap-2">
  <div class=" border-l-4 border-blue-500 p-3 rounded-lg">
    <h6 class="text-blue-800 font-bold" style="color: black !important">Normalidad (Anderson-Darling)</h6>
    <span class="text-xs text-gray-800 p-1">
A = 0.64809
    </span>
    <span class="text-xs text-gray-800 p-1">
p-value = 0.08945
    </span>
    <p class="text-blue-700"><strong>No se rechaza normalidad</strong></p>
  </div>
  <div class="border-l-4 border-green-50 p-3 rounded-lg">
    <h6 class="text-green-800 font-bold" style="color: black !important">Homogeneidad (Levene)</h6>
    <span class="text-xs text-gray-800 p-1">
F = 8.3741 
    </span>
    <span class="text-xs text-gray-800 p-1">
p-value = 4.073e-07
    </span>
    <p class="text-green-700"><strong>Ligera heterocedasticidad</strong></p>
  </div>
  <div class="border-l-4 border-gray-50 p-3 rounded-lg">
    <h6 class="font-bold text-gray-800" style="color: black !important"> Gráfico Q-Q</h6>
    <p class="text-gray-800 text-sm">Los datos siguen aproximadamente una distribución normal en el cuerpo principal, con ligeras desviaciones en las colas</p>
  </div>
</div>

  <!-- Columna derecha - Imagen -->
  <div class="flex items-start justify-center">
    <img src="/qqgraphic.png" alt="Gráfico Q-Q de ANOVA" class="max-w-full h-auto rounded-lg shadow-lg" style="width: calc(100% - 120px);">
  </div>
</div>

---

# Comparaciones Post-Hoc

##### Prueba de Tukey HSD

###### Por Lenguaje
| Comparación | Diferencia | p-valor |
|-------------|------------|---------|
| Python - R | 0.597 | < 0.001 |
| Julia - R | 2.887 | < 0.001 |
| Julia - Python | 2.290 | < 0.001 |

###### Por Análisis
|Comparación |Diferencia | p-valor |
|-------------|------------|---------|
| ANOVA - Regresión | -0.400 | < 0.001 |

---

# Análisis Visual

<div class="grid grid-cols-2 gap-8">
  <!-- Columna izquierda - Imagen -->
  <div class="flex items-center justify-center">
    <img src="/plot.png" alt="Gráfico de análisis" class="max-w-full h-auto rounded-lg shadow-lg" style="width: calc(100% - 120px);">
  </div>
  <div class="flex flex-col gap-3">
    <div class="grid grid-cols-2 gap-3">
      <div class="bg-blue-50 p-3 rounded-lg">
        <h4 class="text-blue-800 font-bold text-sm">R</h4>
        <ul class="text-blue-700 text-xs">
          <li>Más rápido y consistente</li>
          <li>Poca dispersión</li>
          <li>< 15 segundos promedio</li>
        </ul>
      </div>
      <div class="bg-yellow-50 p-3 rounded-lg">
        <h4 class="text-yellow-800 font-bold text-sm">Python</h4>
        <ul class="text-yellow-700 text-xs">
          <li>Ligeramente más lento</li>
          <li>≈ 20 segundos</li>
          <li>Mayor variabilidad</li>
        </ul>
      </div>
    </div>
    <div class="bg-purple-50 p-3 rounded-lg">
      <h4 class="text-purple-800 font-bold text-sm">Julia</h4>
      <ul class="text-purple-700 text-xs">
        <li><strong>Regresión:</strong> Muy lento (≈ 85s) y variable</li>
        <li><strong>ANOVA:</strong> Mejora notablemente (≈ 25s)</li>
        <li>Mayor dispersión y outliers</li>
      </ul>
    </div>
  </div>
</div>

---

# Decisión sobre Hipótesis

<div class="grid grid-cols-1 gap-4">

###### Resultado del Contraste

<div class="bg-green-50 p-6 py-2 rounded-lg">
<h5 class="text-green-800 font-bold text-xl">Se rechaza H₀</h5>
<p class="text-green-700 mt-2 text-sm">Existen diferencias significativas entre lenguajes en tiempo de ejecución</p>
</div>

###### Evidencia Estadística

- **Lenguaje**: F = 2357, p < 0.001
- **Análisis**: F = 121.7, p < 0.001  
- **Interacción**: F = 104.5, p < 0.001

<div class="bg-blue-50 p-4 py-2 rounded-lg mt-4">
<h5 class="text-blue-800 font-bold">Hallazgos Clave</h5>
<ul class="text-blue-700">
<li class="text-sm">R es consistentemente el más eficiente</li>
<li class="text-sm">ANOVA es más rápido que Regresión</li>
<li class="text-sm">El rendimiento relativo depende del tipo de análisis</li>
</ul>
</div>

</div>

---

# Recomendaciones de Uso

<div class="grid grid-cols-1 gap-4" style="height: calc(100% - 50px);">


<div class="grid grid-cols-3 gap-4 align-items-start">

<div class="bg-blue-50 p-4 rounded-lg">
<h3 class="text-blue-800 font-bold">🔵 R</h3>
<p class="text-blue-700 font-semibold">Recomendado para:</p>
<ul class="text-blue-700">
<li>Modelos lineales simples</li>
<li>Prototipado rápido</li>
<li>Análisis estadístico clásico</li>
</ul>
</div>

<div class="bg-yellow-50 p-4 rounded-lg">
<h3 class="text-yellow-800 font-bold">🟡 Python</h3>
<p class="text-yellow-700 font-semibold">Recomendado para:</p>
<ul class="text-yellow-700">
<li>Procesamiento a gran escala</li>
<li>Pipelines integrados</li>
<li>Ecosistema amplio</li>
</ul>
</div>

<div class="bg-purple-50 p-4 rounded-lg">
<h3 class="text-purple-800 font-bold">🟣 Julia</h3>
<p class="text-purple-700 font-semibold">Recomendado para:</p>
<ul class="text-purple-700">
<li>Simulaciones numéricas</li>
<li>Operaciones matriciales</li>
<li>Computación de alto rendimiento</li>
</ul>
</div>

</div>

</div>

---

# Conclusiones Principales

<div class="grid grid-cols-1 gap-4">

<div class="bg-green-50 p-4 py-2-1 rounded-lg">
<h5 class="text-green-800 font-bold">✅ R - El Más Eficiente</h5>
<p class="text-green-700">Tiempos bajos (< 15s), poca dispersión, estable en ambos análisis</p>
</div>

<div class="bg-yellow-50 p-4 py-2-1 rounded-lg">
<h5 class="text-yellow-800 font-bold">📊 Python - Equilibrado</h5>
<p class="text-yellow-700">Tiempo medio (≈ 20s), mayor variabilidad, ventajas en scripting</p>
</div>

<div class="bg-purple-50 p-4 py-2-1 rounded-lg">
<h5 class="text-purple-800 font-bold">⚡ Julia - Contexto Dependiente</h5>
<p class="text-purple-700">Lento en Regresión (≈ 85s), competitivo en ANOVA (≈ 25s)</p>
</div>

</div>
---

# Referencias

<div class="grid grid-cols-1 gap-4">

<div class="p-6 rounded-lg">

### Documentación Oficial

- **R Core Team (2023)**. R: A language and environment for statistical computing. R Foundation for Statistical Computing.

- **Bezanson J. et al. (2017)**. Julia: A fresh approach to numerical computing. SIAM Review.

### Librerías Utilizadas

- **R**: `car`, `dplyr`, `ggplot2`, `nortest`
- **Python**: `pandas`, `statsmodels`
- **Julia**: `GLM.jl`, `DataFrames.jl`, `StatsModels.jl`

</div>

</div>

---
layout: center
class: text-center
---

# ¡Gracias por su atención!
