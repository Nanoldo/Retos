import numpy as np
 
# Configuracion para reproducibilidad
np.random.seed(42)
 
 
# =====================================================================
# GENERACION DE DATOS DE SENSORES
# =====================================================================
 
def generar_datos() -> dict:
    """Genera los arrays 3D de temperatura, humedad y CO2 para las 5
    estaciones de monitoreo de la CDMX, junto con sus promedios diarios.
    """
    estaciones = ['Coyoacán', 'Azcapotzalco', 'Xochimilco', 'Tlalpan', 'Miguel Hidalgo']
    n_estaciones = len(estaciones)
    n_dias = 7
    n_horas = 24
 
    # ----------------------------------------------------------------
    # TEMPERATURA (C) - Array 3D: (estaciones, dias, horas)
    # ----------------------------------------------------------------
    temp_base = np.array([22, 24, 20, 19, 23])  # Temperatura base por estacion
 
    hora_del_dia = np.arange(24)
    variacion_diaria = 5 * np.sin((hora_del_dia - 6) * np.pi / 12)  # Max 14h, min 6h
 
    temperatura = np.zeros((n_estaciones, n_dias, n_horas))
    for i in range(n_estaciones):
        for d in range(n_dias):
            temperatura[i, d, :] = temp_base[i] + variacion_diaria + np.random.normal(0, 1.5, n_horas)
 
    # Sensores desconectados (valores faltantes)
    temperatura[1, 2, 10:14] = np.nan  # Azcapotzalco, dia 3, horas 10-13
    temperatura[3, 5, 0:3] = np.nan    # Tlalpan, dia 6, horas 0-2
 
    # ----------------------------------------------------------------
    # HUMEDAD RELATIVA (%) - Array 3D: (estaciones, dias, horas)
    # ----------------------------------------------------------------
    humedad_base = np.array([55, 45, 70, 65, 50])  # Xochimilco y Tlalpan mas humedos
 
    variacion_humedad = -15 * np.sin((hora_del_dia - 6) * np.pi / 12)
 
    humedad = np.zeros((n_estaciones, n_dias, n_horas))
    for i in range(n_estaciones):
        for d in range(n_dias):
            humedad[i, d, :] = humedad_base[i] + variacion_humedad + np.random.normal(0, 5, n_horas)
 
    humedad = np.clip(humedad, 20, 95)
    humedad[0, 4, 15:18] = np.nan  # Coyoacan, dia 5, horas 15-17
 
    # ----------------------------------------------------------------
    # NIVELES DE CO2 (ppm) - Array 3D: (estaciones, dias, horas)
    # ----------------------------------------------------------------
    co2_base = np.array([380, 420, 360, 350, 410])  # Zonas con mas trafico
 
    patron_trafico = np.zeros(24)
    patron_trafico[7:10] = 30   # Hora pico mañana
    patron_trafico[17:20] = 40  # Hora pico tarde
    patron_trafico[12:14] = 15  # Mediodia
 
    co2 = np.zeros((n_estaciones, n_dias, n_horas))
    for i in range(n_estaciones):
        for d in range(n_dias):
            co2[i, d, :] = co2_base[i] + patron_trafico + np.random.normal(0, 10, n_horas)
 
    co2[:, 3, :] *= 1.15  # Dia de contingencia (dia 4) - CO2 elevado
    co2[2, 1, 5:8] = np.nan  # Xochimilco, dia 2, horas 5-7
 
    # ----------------------------------------------------------------
    # Array 2D simplificado: promedios diarios por estacion
    # ----------------------------------------------------------------
    temp_promedio_diario = np.nanmean(temperatura, axis=2)      # Shape: (5, 7)
    humedad_promedio_diario = np.nanmean(humedad, axis=2)
    co2_promedio_diario = np.nanmean(co2, axis=2)
 
    print("+" + "=" * 64 + "+")
    print("|              DATOS GENERADOS EXITOSAMENTE                    |")
    print("+" + "=" * 64 + "+")
    print(f"|  temperatura     : shape {temperatura.shape}")
    print(f"|  humedad         : shape {humedad.shape}")
    print(f"|  co2             : shape {co2.shape}")
    print(f"|  temp_promedio_diario    : shape {temp_promedio_diario.shape}")
    print(f"|  humedad_promedio_diario : shape {humedad_promedio_diario.shape}")
    print(f"|  co2_promedio_diario     : shape {co2_promedio_diario.shape}")
    print("+" + "=" * 64 + "+")
    print("\nEstaciones:", estaciones)
 
    return {
        "estaciones": estaciones,
        "n_estaciones": n_estaciones,
        "n_dias": n_dias,
        "n_horas": n_horas,
        "temperatura": temperatura,
        "humedad": humedad,
        "co2": co2,
        "temp_promedio_diario": temp_promedio_diario,
        "humedad_promedio_diario": humedad_promedio_diario,
        "co2_promedio_diario": co2_promedio_diario,
    }
 
 
# =====================================================================
# PARTE 1: Exploracion de Arrays
# =====================================================================
 
def ejercicio_1_1(temperatura: np.ndarray) -> None:
    """1.1 Inspeccion de propiedades del array temperatura."""
    n_dimensiones = temperatura.ndim
    forma = temperatura.shape
    total_elementos = temperatura.size
    tipo_datos = temperatura.dtype
    memoria_bytes = temperatura.nbytes
 
    print("PROPIEDADES DEL ARRAY TEMPERATURA")
    print("-" * 40)
    print(f"Dimensiones: {n_dimensiones}D")
    print(f"Forma: {forma}")
    print(f"  -> {forma[0]} estaciones")
    print(f"  -> {forma[1]} dias")
    print(f"  -> {forma[2]} horas por dia")
    print(f"Total de mediciones: {total_elementos:,}")
    print(f"Tipo de datos: {tipo_datos}")
    print(f"Memoria: {memoria_bytes:,} bytes ({memoria_bytes/1024:.2f} KB)")
 
 
def ejercicio_1_2(temperatura: np.ndarray, co2: np.ndarray, temp_promedio_diario: np.ndarray) -> None:
    """1.2 Indexacion basica."""
    # 1. Temperatura de Coyoacan (0), dia 1 (0), 12:00h (12)
    temp_coyoacan_d1_12h = temperatura[0, 0, 12]
    print(f"Coyoacan, Dia 1, 12:00h: {temp_coyoacan_d1_12h:.1f}C")
 
    # 2. Todas las temperaturas de Xochimilco (2) en el dia 3 (2)
    temp_xochimilco_d3 = temperatura[2, 2, :]
    print(f"\nXochimilco, Dia 3 (24 horas):")
    print(f"   Primeras 6 horas: {temp_xochimilco_d3[:6].round(1)}")
 
    # 3. Temperatura promedio diario de Miguel Hidalgo (4) para los 7 dias
    temp_mh_7dias = temp_promedio_diario[4, :]
    print(f"\nMiguel Hidalgo - Promedio por dia:")
    print(f"   {temp_mh_7dias.round(1)}")
 
    # 4. Ultimo valor de CO2 registrado
    ultimo_co2 = co2[-1, -1, -1]
    print(f"\nUltimo CO2 registrado: {ultimo_co2:.1f} ppm")
 
 
def ejercicio_1_3(temperatura: np.ndarray, humedad: np.ndarray, co2: np.ndarray) -> None:
    """1.3 Slicing avanzado."""
    # 1. Todas las estaciones/dias, horas de tarde (12-18) -> shape (5, 7, 6)
    temp_tardes = temperatura[:, :, 12:18]
    print(f"Temperaturas de tardes (12-17h)")
    print(f"   Shape: {temp_tardes.shape}")
 
    # 2. Primeras 3 estaciones, ultimos 3 dias, todas las horas -> shape (3, 3, 24)
    humedad_subset = humedad[:3, -3:, :]
    print(f"\nSubset de humedad")
    print(f"   Shape: {humedad_subset.shape}")
 
    # 3. Estaciones pares (0,2,4), todos los dias, horas de mañana (6-12) -> shape (3, 7, 6)
    co2_mananas_pares = co2[::2, :, 6:12]
    print(f"\nCO2 mañanas (estaciones pares)")
    print(f"   Shape: {co2_mananas_pares.shape}")
 
    # 4. Temperaturas en orden inverso de dias
    temp_inverso = temperatura[:, ::-1, :]
    print(f"\nTemperatura dias invertidos")
    print(f"   Shape: {temp_inverso.shape}")
 
 
# =====================================================================
# PARTE 2: Estadisticas Basicas
# =====================================================================
 
def ejercicio_2_1(temperatura: np.ndarray) -> None:
    """2.1 Estadisticas globales de temperatura (con manejo de NaN)."""
    temp_promedio = np.nanmean(temperatura)
    temp_maxima = np.nanmax(temperatura)
    temp_minima = np.nanmin(temperatura)
    temp_std = np.nanstd(temperatura)
    temp_rango = temp_maxima - temp_minima
 
    print("+" + "=" * 64 + "+")
    print("|           ESTADISTICAS GLOBALES DE TEMPERATURA               |")
    print("+" + "=" * 64 + "+")
    print(f"|  Promedio:     {temp_promedio:>6.2f} C")
    print(f"|  Maxima:       {temp_maxima:>6.2f} C")
    print(f"|  Minima:       {temp_minima:>6.2f} C")
    print(f"|  Desv. Est.:   {temp_std:>6.2f} C")
    print(f"|  Rango:        {temp_rango:>6.2f} C")
    print("+" + "=" * 64 + "+")
 
 
def ejercicio_2_2(temperatura: np.ndarray, humedad: np.ndarray, co2: np.ndarray,
                   estaciones: list, n_dias: int) -> None:
    """2.2 Estadisticas por eje."""
    # 1. Temperatura promedio POR ESTACION (sobre dias y horas -> axis=(1,2))
    temp_por_estacion = np.nanmean(temperatura, axis=(1, 2))
 
    print("TEMPERATURA PROMEDIO POR ESTACION")
    print("-" * 40)
    for i, est in enumerate(estaciones):
        print(f"   {est:15s}: {temp_por_estacion[i]:5.1f} C")
 
    # 2. Humedad promedio POR HORA DEL DIA (sobre estaciones y dias -> axis=(0,1))
    humedad_por_hora = np.nanmean(humedad, axis=(0, 1))
 
    print("\nHUMEDAD PROMEDIO POR HORA")
    print("-" * 40)
    print("   Hora | Humedad")
    for h in [0, 6, 12, 18]:
        print(f"   {h:02d}:00 | {humedad_por_hora[h]:5.1f}%")
 
    # 3. CO2 maximo POR DIA (sobre estaciones y horas -> axis=(0,2))
    co2_max_por_dia = np.nanmax(co2, axis=(0, 2))
 
    print("\nCO2 MAXIMO POR DIA")
    print("-" * 40)
    for d in range(n_dias):
        print(f"   Dia {d+1}: {co2_max_por_dia[d]:6.1f} ppm")
 
 
# =====================================================================
# PARTE 3: Operaciones Vectorizadas
# =====================================================================
 
def ejercicio_3_1(temperatura: np.ndarray, humedad: np.ndarray):
    """3.1 Conversiones de unidades (sin loops)."""
    # 1. Celsius -> Fahrenheit
    temperatura_fahrenheit = temperatura * 9 / 5 + 32
 
    print("TEMPERATURA EN FAHRENHEIT")
    print(f"   Promedio: {np.nanmean(temperatura_fahrenheit):.1f} F")
    print(f"   Maxima:   {np.nanmax(temperatura_fahrenheit):.1f} F")
    print(f"   Minima:   {np.nanmin(temperatura_fahrenheit):.1f} F")
 
    # 2. Celsius -> Kelvin
    temperatura_kelvin = temperatura + 273.15
 
    print(f"\nTEMPERATURA EN KELVIN")
    print(f"   Promedio: {np.nanmean(temperatura_kelvin):.1f} K")
 
    # 3. Normalizar humedad a rango [0, 1]
    humedad_min = np.nanmin(humedad)
    humedad_max = np.nanmax(humedad)
    humedad_normalizada = (humedad - humedad_min) / (humedad_max - humedad_min)
 
    print(f"\nHUMEDAD NORMALIZADA [0-1]")
    print(f"   Promedio: {np.nanmean(humedad_normalizada):.3f}")
    print(f"   Min:      {np.nanmin(humedad_normalizada):.3f}")
    print(f"   Max:      {np.nanmax(humedad_normalizada):.3f}")
 
    return temperatura_fahrenheit, temperatura_kelvin, humedad_normalizada
 
 
def ejercicio_3_2(temperatura: np.ndarray, humedad: np.ndarray):
    """3.2 Indice de Confort Termico (ICT) y su distribucion por categorias."""
    # 1. ICT = temperatura + 0.05 * humedad (broadcasting)
    ict = temperatura + 0.05 * humedad
 
    print("INDICE DE CONFORT TERMICO (ICT)")
    print("-" * 45)
    print(f"   Shape del array ICT: {ict.shape}")
    print(f"   ICT promedio: {np.nanmean(ict):.2f}")
    print(f"   ICT maximo:   {np.nanmax(ict):.2f}")
    print(f"   ICT minimo:   {np.nanmin(ict):.2f}")
 
    # 2. Clasificacion por categorias usando indexacion booleana
    n_frio = np.sum(ict < 20)
    n_confortable = np.sum((ict >= 20) & (ict < 25))
    n_calido = np.sum((ict >= 25) & (ict < 30))
    n_muy_caluroso = np.sum(ict >= 30)
 
    n_validas = np.sum(~np.isnan(ict))
 
    print("\nDISTRIBUCION DE CONDICIONES")
    print("-" * 45)
    print(f"   Frio (<20):           {n_frio:5d} ({100*n_frio/n_validas:5.1f}%)")
    print(f"   Confortable (20-25):  {n_confortable:5d} ({100*n_confortable/n_validas:5.1f}%)")
    print(f"   Calido (25-30):       {n_calido:5d} ({100*n_calido/n_validas:5.1f}%)")
    print(f"   Muy caluroso (>=30):  {n_muy_caluroso:5d} ({100*n_muy_caluroso/n_validas:5.1f}%)")
    print(f"   ----------------------------------------")
    print(f"   Total validas:           {n_validas:5d}")
 
    return ict
 
 
# =====================================================================
# PARTE 4: Analisis Avanzado
# =====================================================================
 
def ejercicio_4_1(co2: np.ndarray):
    """4.1 Deteccion de anomalias en CO2 (mas de 2 desviaciones estandar)."""
    co2_media = np.nanmean(co2)
    co2_std = np.nanstd(co2)
 
    limite_inferior = co2_media - 2 * co2_std
    limite_superior = co2_media + 2 * co2_std
 
    print("ANALISIS DE ANOMALIAS EN CO2")
    print("-" * 45)
    print(f"   Media CO2:       {co2_media:.1f} ppm")
    print(f"   Desv. Est.:      {co2_std:.1f} ppm")
    print(f"   Limite inferior: {limite_inferior:.1f} ppm")
    print(f"   Limite superior: {limite_superior:.1f} ppm")
 
    # Mascara booleana de anomalias, excluyendo NaN
    mascara_anomalias = ((co2 < limite_inferior) | (co2 > limite_superior)) & ~np.isnan(co2)
 
    n_anomalias = np.sum(mascara_anomalias)
    valores_anomalos = co2[mascara_anomalias]
 
    print(f"\nANOMALIAS DETECTADAS: {n_anomalias}")
    if n_anomalias > 0:
        print(f"   Valores: {valores_anomalos[:10].round(1)}")
        if n_anomalias > 10:
            print(f"   ... y {n_anomalias - 10} mas")
 
    return mascara_anomalias
 
 
def ejercicio_4_2(co2: np.ndarray, estaciones: list):
    """4.2 Analisis de contingencia ambiental del dia 4 (indice 3)."""
    DIA_CONTINGENCIA = 3
 
    # 1. CO2 del dia de contingencia -> shape (5, 24)
    co2_contingencia = co2[:, DIA_CONTINGENCIA, :]
 
    # 2. CO2 de dias normales (todos excepto el dia 4) -> shape (5, 6, 24)
    dias_normales = [0, 1, 2, 4, 5, 6]
    co2_dias_normales = co2[:, dias_normales, :]
 
    # 3 y 4. Promedios globales
    promedio_contingencia = np.nanmean(co2_contingencia)
    promedio_normal = np.nanmean(co2_dias_normales)
 
    # 5. Incremento porcentual
    incremento_porcentual = ((promedio_contingencia - promedio_normal) / promedio_normal) * 100
 
    print("+" + "=" * 64 + "+")
    print("|           ANALISIS DE CONTINGENCIA AMBIENTAL                 |")
    print("|                        Dia 4                                 |")
    print("+" + "=" * 64 + "+")
    print(f"|  CO2 promedio dia contingencia: {promedio_contingencia:>7.1f} ppm")
    print(f"|  CO2 promedio dias normales:    {promedio_normal:>7.1f} ppm")
    print(f"|  Incremento:                    {incremento_porcentual:>7.1f} %")
    print("+" + "=" * 64 + "+")
 
    # 6. Estacion mas afectada (mayor incremento de CO2)
    co2_por_estacion_contingencia = np.nanmean(co2_contingencia, axis=1)   # (5,)
    co2_por_estacion_normal = np.nanmean(co2_dias_normales, axis=(1, 2))  # (5,)
 
    incremento_por_estacion = ((co2_por_estacion_contingencia - co2_por_estacion_normal) /
                                co2_por_estacion_normal) * 100
 
    idx_mas_afectada = np.argmax(incremento_por_estacion)
 
    print("\nIMPACTO POR ESTACION")
    print("-" * 50)
    for i, est in enumerate(estaciones):
        barra = "#" * int(incremento_por_estacion[i] / 2)
        print(f"   {est:15s}: +{incremento_por_estacion[i]:5.1f}% {barra}")
 
    print(f"\nEstacion mas afectada: {estaciones[idx_mas_afectada]}")
 
 
# =====================================================================
# BONUS: Reporte Ejecutivo
# =====================================================================
 
def reporte_ejecutivo(temperatura: np.ndarray, humedad: np.ndarray, co2: np.ndarray,
                       estaciones: list) -> None:
    """Genera el reporte ejecutivo semanal con las metricas clave."""
    temp_por_estacion = np.nanmean(temperatura, axis=(1, 2))
    humedad_por_estacion = np.nanmean(humedad, axis=(1, 2))
    co2_por_estacion = np.nanmean(co2, axis=(1, 2))
 
    # 1. Estacion mas calurosa (mayor temperatura promedio)
    idx_mas_calurosa = np.argmax(temp_por_estacion)
    estacion_mas_calurosa = estaciones[idx_mas_calurosa]
 
    # 2. Estacion mas humeda (mayor humedad promedio)
    idx_mas_humeda = np.argmax(humedad_por_estacion)
    estacion_mas_humeda = estaciones[idx_mas_humeda]
 
    # 3. Estacion con mejor calidad de aire (menor CO2 promedio)
    idx_mejor_aire = np.argmin(co2_por_estacion)
    estacion_mejor_aire = estaciones[idx_mejor_aire]
 
    # 4. Hora mas calurosa del dia
    temp_por_hora = np.nanmean(temperatura, axis=(0, 1))
    hora_mas_calurosa = int(np.argmax(temp_por_hora))
 
    # 5. Hora con peor calidad de aire
    co2_por_hora = np.nanmean(co2, axis=(0, 1))
    hora_peor_aire = int(np.argmax(co2_por_hora))
 
    # 6. Numero de valores faltantes en total
    nan_temperatura = int(np.sum(np.isnan(temperatura)))
    nan_humedad = int(np.sum(np.isnan(humedad)))
    nan_co2 = int(np.sum(np.isnan(co2)))
    total_nan = nan_temperatura + nan_humedad + nan_co2
 
    print("")
    print("+" + "=" * 72 + "+")
    print("|            METEOSENSE - REPORTE EJECUTIVO SEMANAL                    |")
    print("|                        CDMX - Semana de Analisis                     |")
    print("+" + "=" * 72 + "+")
    print("|  RESUMEN DE CONDICIONES")
    print("|  -------------------------------------------------------------------")
    print(f"|    Temperatura promedio:    {np.nanmean(temperatura):>5.1f} C")
    print(f"|    Humedad promedio:         {np.nanmean(humedad):>5.1f} %")
    print(f"|    CO2 promedio:            {np.nanmean(co2):>6.1f} ppm")
    print("|")
    print("|  RANKINGS")
    print("|  -------------------------------------------------------------------")
    print(f"|    Estacion mas calurosa:   {estacion_mas_calurosa:15s}")
    print(f"|    Estacion mas humeda:     {estacion_mas_humeda:15s}")
    print(f"|    Mejor calidad de aire:   {estacion_mejor_aire:15s}")
    print("|")
    print("|  PATRONES TEMPORALES")
    print("|  -------------------------------------------------------------------")
    print(f"|    Hora mas calurosa:       {hora_mas_calurosa:02d}:00 hrs")
    print(f"|    Hora con mas CO2:        {hora_peor_aire:02d}:00 hrs")
    print("|")
    print("|  CALIDAD DE DATOS")
    print("|  -------------------------------------------------------------------")
    print(f"|    Valores faltantes totales:  {total_nan:4d}")
    print(f"|      - Temperatura: {nan_temperatura:3d}")
    print(f"|      - Humedad:     {nan_humedad:3d}")
    print(f"|      - CO2:         {nan_co2:3d}")
    print("+" + "=" * 72 + "+")
    print("")
 
 
# =====================================================================
# Programa principal
# =====================================================================
 
def main() -> None:
    print("NumPy cargado correctamente")
    print(f"   Version: {np.__version__}\n")
 
    datos = generar_datos()
 
    estaciones = datos["estaciones"]
    n_dias = datos["n_dias"]
    temperatura = datos["temperatura"]
    humedad = datos["humedad"]
    co2 = datos["co2"]
    temp_promedio_diario = datos["temp_promedio_diario"]
 
    print("\n" + "=" * 70)
    print(" PARTE 1: EXPLORACION DE ARRAYS")
    print("=" * 70 + "\n")
 
    print("--- Ejercicio 1.1: Inspeccion de Datos ---")
    ejercicio_1_1(temperatura)
 
    print("\n--- Ejercicio 1.2: Indexacion Basica ---")
    ejercicio_1_2(temperatura, co2, temp_promedio_diario)
 
    print("\n--- Ejercicio 1.3: Slicing Avanzado ---")
    ejercicio_1_3(temperatura, humedad, co2)
 
    print("\n" + "=" * 70)
    print(" PARTE 2: ESTADISTICAS BASICAS")
    print("=" * 70 + "\n")
 
    print("--- Ejercicio 2.1: Estadisticas Globales ---")
    ejercicio_2_1(temperatura)
 
    print("\n--- Ejercicio 2.2: Estadisticas por Eje ---")
    ejercicio_2_2(temperatura, humedad, co2, estaciones, n_dias)
 
    print("\n" + "=" * 70)
    print(" PARTE 3: OPERACIONES VECTORIZADAS")
    print("=" * 70 + "\n")
 
    print("--- Ejercicio 3.1: Conversiones de Unidades ---")
    ejercicio_3_1(temperatura, humedad)
 
    print("\n--- Ejercicio 3.2: Indice de Confort Termico ---")
    ejercicio_3_2(temperatura, humedad)
 
    print("\n" + "=" * 70)
    print(" PARTE 4: ANALISIS AVANZADO")
    print("=" * 70 + "\n")
 
    print("--- Ejercicio 4.1: Deteccion de Anomalias ---")
    ejercicio_4_1(co2)
 
    print("\n--- Ejercicio 4.2: Analisis de Contingencia Ambiental ---")
    ejercicio_4_2(co2, estaciones)
 
    print("\n" + "=" * 70)
    print(" BONUS: REPORTE EJECUTIVO")
    print("=" * 70)
 
    reporte_ejecutivo(temperatura, humedad, co2, estaciones)
 
 
if __name__ == "__main__":
    main()