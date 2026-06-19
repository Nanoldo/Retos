import sys

def procesar_linea(linea):
    """
    Procesa una linea del CSV.
    Retorna (ciudad, celsius, clasificacion) o ignora si es invalida.
    """
    # Separar
    partes = linea.strip().split(',')
    if len(partes) != 3:
        return None
    
    ciudad = partes[0].strip()
    temp_str = partes[1]
    unidad = partes[2].strip().upper()
    
    # Validar unidad
    if unidad not in ['C', 'F']:
        return None
    
    # Convertir temperatura
    try:
        temperatura = float(temp_str)
    except ValueError:
        return None
    
    # Convertir a Celsius si es necesario
    if unidad == 'F':
        celsius = (temperatura - 32) * 5 / 9
    else:
        celsius = temperatura
    
    # Clasificar
    if celsius < 0:
        clasificacion = "Congelante"
    elif celsius <= 15:
        clasificacion = "Frio"
    elif celsius <= 25:
        clasificacion = "Templado"
    elif celsius <= 35:
        clasificacion = "Calido"
    else:
        clasificacion = "Extremo"
    
    return (ciudad, celsius, clasificacion)

def main():
    print("ciudad,temperatura_celsius,clasificacion")
    for linea in sys.stdin:
        resultado = procesar_linea(linea)
        if resultado is None:
            continue
        else:
            ciudad, celsius, clasif = resultado
            print(f"{ciudad},{celsius:.1f},{clasif}")

if __name__ == "__main__":
    main()
