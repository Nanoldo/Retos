# 🔍 SecureBank Fraud Detection

Sistema de detección de anomalías en transacciones bancarias utilizando NumPy.

## Objetivo

Identificar transacciones sospechosas mediante dos técnicas estadísticas:

- Método IQR (Interquartile Range)
- Método Z-Score

## Tecnologías

- Python 3
- NumPy

## Estructura
reto_09_detector_anomalias/
│
├── main.py
└── README.md

## Funcionalidades

### 1. Generación de Datos

Se generan 500 transacciones por categoría:

- Supermercados
- Restaurantes
- Gasolineras
- Tiendas Online
- Entretenimiento

Además se insertan anomalías simuladas para representar posibles fraudes.

### 2. Estadísticas Descriptivas

Para cada categoría se calcula:

- Media
- Mediana
- Desviación estándar
- Valor mínimo
- Valor máximo

### 3. Método IQR

Se calculan:

- Q1
- Q2
- Q3
- IQR
- Límites inferior y superior

Posteriormente se detectan transacciones fuera de los límites.

### 4. Método Z-Score

Se calcula:

\[
z = \frac{x-\mu}{\sigma}
\]

Una transacción se considera anómala cuando:

\[
|z| > 3
\]

### 5. Comparación de Métodos

Se comparan los resultados obtenidos por:

- IQR
- Z-Score

y se identifican las transacciones detectadas por ambos métodos.

### 6. Análisis de Correlación

Se calcula una matriz de correlación entre categorías para identificar posibles relaciones en los patrones de gasto.

## Ejecución

```bash
python main.py
```
 ## Alumno
Pérez Jiménez Emiliano
3AM1