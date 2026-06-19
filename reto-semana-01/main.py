import sys

def limpiar_valor(valor):
    """
    Limpia un valor individual:
    - Quita espacios
    - Elimina caracteres no validos
    - Retorna el numero limpio como string
    """
    valor_sin_espacios = valor.strip()
    caracteres_validos = '0123456789.-'
    resultado = ''
    for char in valor_sin_espacios:
        if char in caracteres_validos:
            resultado += char
    return resultado

def procesar_linea(linea):
    """
    Procesa una linea completa:
    - Separa por comas
    - Limpia cada valor
    - Trunca a entero
    - Suma todos
    - Retorna el resultado
    """
    # dividir en campos separados por coma, ignorando la nueva línea al final
    valores = linea.strip().split(',')
    # si la línea está vacía (e.g. sólo un salto de línea) su suma es 0
    if not valores or (len(valores) == 1 and valores[0] == ''):
        return 0

    suma = 0
    for valor in valores:
        valor_limpio = limpiar_valor(valor)
        # los campos vacíos ("", "   ") se consideran cero y se saltan
        if valor_limpio == '':
            continue
        try:
            numero = int(float(valor_limpio))  # Primero a float, luego a int
        except ValueError:
            # si no se puede convertir simplemente lo ignoramos como 0
            continue
        suma += numero
    return suma

def main():
    """
    Lee de stdin linea por linea
    Procesa cada linea
    Imprime el resultado
    """
    for linea in sys.stdin:
        suma_total = procesar_linea(linea)
        print(suma_total)

if __name__ == "__main__":
    main()