# Reto Semana 8: MeteoSense Analytics
 
**Sistema de Análisis de Datos Meteorológicos con NumPy**
Programación para Ciencia de Datos — IPN
Febrero - Julio 2026
 
## Descripción
 
MeteoSense es una red de 5 estaciones de monitoreo ambiental en la Ciudad de México que registra **temperatura, humedad relativa y CO2** cada hora durante 7 días. Este programa genera esos datos sintéticos como arrays 3D de NumPy y aplica un pipeline completo de exploración, estadística, operaciones vectorizadas y análisis avanzado, terminando con un reporte ejecutivo.
 
Todo el procesamiento usa **NumPy puro**: indexación, slicing, broadcasting y funciones `nan*` para manejar valores faltantes (sensores desconectados). Las Partes 2, 3 y 4 están resueltas **sin loops** (`for`/`while`), solo con operaciones vectorizadas, tal como lo exige la consigna.
 
## Requisitos
 
```bash
pip install numpy
```
 
## Uso
 
```bash
python main.py
```
 
El script genera los datos (con semilla fija `np.random.seed(42)` para reproducibilidad) y ejecuta, en orden, las 4 partes del reto más el bonus, imprimiendo cada resultado en consola.
 
## Estructura de los datos
 
| Variable | Forma (shape) | Descripción |
|---|---|---|
| `temperatura` | `(5, 7, 24)` | °C, por estación / día / hora |
| `humedad` | `(5, 7, 24)` | % relativa, por estación / día / hora |
| `co2` | `(5, 7, 24)` | ppm, por estación / día / hora |
| `temp_promedio_diario` | `(5, 7)` | Promedio de temperatura por estación y día |
| `humedad_promedio_diario` | `(5, 7)` | Promedio de humedad por estación y día |
| `co2_promedio_diario` | `(5, 7)` | Promedio de CO2 por estación y día |
 
**Estaciones** (índice 0 a 4): Coyoacán, Azcapotzalco, Xochimilco, Tlalpan, Miguel Hidalgo.
 
Los datos incluyen valores `NaN` simulando sensores desconectados:
- Temperatura: Azcapotzalco día 3 (horas 10-13) y Tlalpan día 6 (horas 0-2) → 7 NaN.
- Humedad: Coyoacán día 5 (horas 15-17) → 3 NaN.
- CO2: Xochimilco día 2 (horas 5-7) → 3 NaN.
El día 4 (índice 3) simula una **contingencia ambiental**: el CO2 de ese día se multiplica por 1.15.
 
## Estructura del código
 
### Generación de datos
- **`generar_datos()`** — construye los 3 arrays 3D con sus patrones (ciclo día/noche en temperatura y humedad, horas pico de tráfico en CO2), inserta los NaN y calcula los promedios diarios.
### Parte 1 — Exploración de Arrays
- **`ejercicio_1_1`** — propiedades del array (`ndim`, `shape`, `size`, `dtype`, `nbytes`).
- **`ejercicio_1_2`** — indexación puntual: un valor específico, un corte 1D, una fila del array de promedios, el último elemento con índices negativos.
- **`ejercicio_1_3`** — slicing avanzado: rango de horas, subconjunto de estaciones/días, paso (`::2`) para estaciones pares, inversión de orden (`::-1`).
### Parte 2 — Estadísticas Básicas
- **`ejercicio_2_1`** — estadísticas globales de temperatura usando `np.nanmean`, `np.nanmax`, `np.nanmin`, `np.nanstd` (ignoran los NaN).
- **`ejercicio_2_2`** — estadísticas por eje con tuplas de ejes (`axis=(1,2)`, `axis=(0,1)`, `axis=(0,2)`) para colapsar las dimensiones correctas en cada caso.
### Parte 3 — Operaciones Vectorizadas
- **`ejercicio_3_1`** — conversión Celsius→Fahrenheit y Celsius→Kelvin, y normalización min-max de humedad a `[0, 1]`; todo con operaciones de array completas, sin loops.
- **`ejercicio_3_2`** — Índice de Confort Térmico `ICT = temperatura + 0.05 * humedad` calculado con broadcasting sobre el array 3D completo, y clasificación en 4 categorías mediante indexación booleana (`<`, `>=`, `&`).
### Parte 4 — Análisis Avanzado
- **`ejercicio_4_1`** — detección de anomalías de CO2: un valor es anómalo si está a más de 2 desviaciones estándar de la media; se construye una máscara booleana que excluye explícitamente los `NaN`.
- **`ejercicio_4_2`** — análisis de la contingencia del día 4: compara el promedio de CO2 ese día contra el promedio de los 6 días normales (global y por estación), calcula el incremento porcentual y usa `np.argmax` para identificar la estación más afectada.
### Bonus — Reporte Ejecutivo
- **`reporte_ejecutivo`** — combina rankings (`np.argmax`/`np.argmin` sobre promedios por estación), patrones horarios (hora más calurosa y de peor calidad de aire) y un resumen de calidad de datos (conteo de `NaN` con `np.isnan` + `np.sum`), todo presentado en un reporte con formato de caja.
## Notas
 
- El texto usa caracteres ASCII simples (`+`, `-`, `|`, `#`) en los recuadros para máxima compatibilidad de consola, en lugar de los caracteres de caja Unicode (`╔`, `═`, etc.) y emojis del notebook original.
- Las funciones están separadas por ejercicio para facilitar pruebas individuales o reutilización en otros scripts/notebooks.
- Los resultados numéricos exactos dependen de `np.random.seed(42)`; si se cambia la semilla o el orden de las llamadas a `np.random`, los valores variarán pero la lógica y los shapes se mantienen.
 
 ## Alumno
 Pérez Jiménez Emiliano
 3AM1