import numpy as np

# ==========================================================
# CONFIGURACIÓN
# ==========================================================

np.random.seed(2024)
np.set_printoptions(precision=2, suppress=True)

categorias = [
    "Supermercados",
    "Restaurantes",
    "Gasolineras",
    "Tiendas_Online",
    "Entretenimiento"
]

n_categorias = len(categorias)

params_categorias = {
    "Supermercados": (800, 400),
    "Restaurantes": (350, 150),
    "Gasolineras": (700, 250),
    "Tiendas_Online": (1200, 800),
    "Entretenimiento": (200, 100)
}

n_transacciones_por_cat = 500

# ==========================================================
# GENERACIÓN DE DATOS
# ==========================================================

transacciones = {}
ids_transaccion = {}

for i, cat in enumerate(categorias):
    media, std = params_categorias[cat]

    montos = np.random.normal(
        media,
        std,
        n_transacciones_por_cat
    )

    montos = np.maximum(montos, 10)

    n_anomalias_altas = np.random.randint(8, 15)
    n_anomalias_bajas = np.random.randint(5, 10)

    indices_altas = np.random.choice(
        n_transacciones_por_cat,
        n_anomalias_altas,
        replace=False
    )

    montos[indices_altas] = (
        media +
        np.random.uniform(4, 8, n_anomalias_altas) * std
    )

    indices_bajas = np.random.choice(
        [x for x in range(n_transacciones_por_cat)
         if x not in indices_altas],
        n_anomalias_bajas,
        replace=False
    )

    montos[indices_bajas] = np.random.uniform(
        1,
        15,
        n_anomalias_bajas
    )

    transacciones[cat] = montos

    ids_transaccion[cat] = np.arange(
        i * 1000 + 1,
        i * 1000 + n_transacciones_por_cat + 1
    )

montos_matriz = np.array(
    [transacciones[cat] for cat in categorias]
)

# ==========================================================
# PARTE 1.1 ESTADÍSTICAS
# ==========================================================

medias = np.mean(montos_matriz, axis=1)
medianas = np.median(montos_matriz, axis=1)
stds = np.std(montos_matriz, axis=1)
minimos = np.min(montos_matriz, axis=1)
maximos = np.max(montos_matriz, axis=1)

print("\nESTADÍSTICAS DESCRIPTIVAS\n")

for i, cat in enumerate(categorias):
    print(
        f"{cat:20s}"
        f" Media={medias[i]:.2f}"
        f" Mediana={medianas[i]:.2f}"
        f" Std={stds[i]:.2f}"
    )

# ==========================================================
# PARTE 1.2 CUARTILES E IQR
# ==========================================================

Q1_arr = np.percentile(montos_matriz, 25, axis=1)
Q2_arr = np.percentile(montos_matriz, 50, axis=1)
Q3_arr = np.percentile(montos_matriz, 75, axis=1)

IQR_arr = Q3_arr - Q1_arr

# ==========================================================
# PARTE 1.3 LÍMITES
# ==========================================================

FACTOR_IQR = 1.5

limites_inf = Q1_arr - FACTOR_IQR * IQR_arr
limites_sup = Q3_arr + FACTOR_IQR * IQR_arr

# ==========================================================
# PARTE 2.1 OUTLIERS IQR
# ==========================================================

outliers_iqr = {}
n_outliers_iqr = np.zeros(n_categorias, dtype=int)

for i, cat in enumerate(categorias):

    datos = montos_matriz[i]
    ids = ids_transaccion[cat]

    mascara_outliers = (
        (datos < limites_inf[i]) |
        (datos > limites_sup[i])
    )

    mascara_inf = datos < limites_inf[i]
    mascara_sup = datos > limites_sup[i]

    outliers_iqr[cat] = {
        "ids": ids[mascara_outliers],
        "montos": datos[mascara_outliers],
        "n_total": np.sum(mascara_outliers),
        "n_inferiores": np.sum(mascara_inf),
        "n_superiores": np.sum(mascara_sup)
    }

    n_outliers_iqr[i] = np.sum(mascara_outliers)

# ==========================================================
# PARTE 2.2 ANÁLISIS IQR
# ==========================================================

for cat in categorias:

    info = outliers_iqr[cat]

    if info["n_total"] > 0:

        montos_out = info["montos"]

        monto_min_outlier = np.min(montos_out)
        monto_max_outlier = np.max(montos_out)
        monto_promedio_outlier = np.mean(montos_out)

        print(f"\n{cat}")
        print("Outliers:", info["n_total"])
        print("Min:", round(monto_min_outlier, 2))
        print("Max:", round(monto_max_outlier, 2))
        print("Promedio:", round(monto_promedio_outlier, 2))

# ==========================================================
# PARTE 3.1 Z-SCORE
# ==========================================================

UMBRAL_ZSCORE = 3

zscores_matriz = np.zeros_like(montos_matriz)

for i in range(n_categorias):

    media_cat = np.mean(montos_matriz[i])
    std_cat = np.std(montos_matriz[i])

    zscores_matriz[i] = (
        (montos_matriz[i] - media_cat)
        / std_cat
    )

# ==========================================================
# PARTE 3.2 OUTLIERS Z-SCORE
# ==========================================================

outliers_zscore = {}
n_outliers_zscore = np.zeros(n_categorias, dtype=int)

for i, cat in enumerate(categorias):

    datos = montos_matriz[i]
    zscores = zscores_matriz[i]
    ids = ids_transaccion[cat]

    mascara_outliers_z = (
        np.abs(zscores) > UMBRAL_ZSCORE
    )

    mascara_z_neg = zscores < -UMBRAL_ZSCORE
    mascara_z_pos = zscores > UMBRAL_ZSCORE

    outliers_zscore[cat] = {
        "ids": ids[mascara_outliers_z],
        "montos": datos[mascara_outliers_z],
        "zscores": zscores[mascara_outliers_z],
        "n_total": np.sum(mascara_outliers_z),
        "n_bajos": np.sum(mascara_z_neg),
        "n_altos": np.sum(mascara_z_pos)
    }

    n_outliers_zscore[i] = np.sum(
        mascara_outliers_z
    )

# ==========================================================
# PARTE 4.1 COMPARACIÓN
# ==========================================================

total_iqr = np.sum(n_outliers_iqr)
total_zscore = np.sum(n_outliers_zscore)

print("\nCOMPARACIÓN DE MÉTODOS")
print("IQR:", total_iqr)
print("Z-Score:", total_zscore)

# ==========================================================
# PARTE 4.2 REPORTE FINAL
# ==========================================================

total_alta_prioridad = 0
union_ids = set()

for cat in categorias:

    ids_iqr = set(outliers_iqr[cat]["ids"])
    ids_zscore = set(outliers_zscore[cat]["ids"])

    ids_ambos = ids_iqr & ids_zscore

    total_alta_prioridad += len(ids_ambos)

    union_ids.update(ids_iqr)
    union_ids.update(ids_zscore)

total_transacciones = (
    n_categorias *
    n_transacciones_por_cat
)

total_outliers_unicos = len(union_ids)

pct_anomalias = (
    total_outliers_unicos /
    total_transacciones
) * 100

print("\nREPORTE EJECUTIVO")
print("Transacciones:", total_transacciones)
print("Sospechosas:", total_outliers_unicos)
print("Alta prioridad:", total_alta_prioridad)
print("Porcentaje:", round(pct_anomalias, 2), "%")

# ==========================================================
# BONUS CORRELACIÓN
# ==========================================================

matriz_correlacion = np.corrcoef(
    montos_matriz
)

max_corr = 0
par_max = ("", "")

for i in range(n_categorias):
    for j in range(i + 1, n_categorias):

        if abs(matriz_correlacion[i, j]) > abs(max_corr):
            max_corr = matriz_correlacion[i, j]
            par_max = (
                categorias[i],
                categorias[j]
            )

print("\nCORRELACIÓN MÁS ALTA")
print(par_max[0], "<->", par_max[1])
print("Valor:", round(max_corr, 4))