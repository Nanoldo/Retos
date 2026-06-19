import sys
import re

DEPARTAMENTOS_VALIDOS = ['VEN', 'ADM', 'TEC', 'LOG', 'RHH']
SERIES_VALIDAS = ['A', 'B', 'C', 'D', 'E']


def detectar_tipo(codigo):
    """Detecta el tipo de codigo por su estructura (flexible, case-insensitive)."""
    if re.match(r'^[A-Za-z]{3}-\d{4}-[A-Za-z]{2}$', codigo):
        return 'producto'
    elif re.match(r'^ENV-\d{4}-\d{2}-\d{2}-\d{6}$', codigo):
        return 'envio'
    elif re.match(r'^EMP-[A-Za-z]{3}-\d{4}$', codigo):
        return 'empleado'
    elif re.match(r'^FAC-[A-Za-z]-\d{6}$', codigo):
        return 'factura'
    else:
        return 'desconocido'


def validar_producto(codigo):
    """Valida que categoria y pais sean exactamente mayusculas."""
    return bool(re.match(r'^[A-Z]{3}-\d{4}-[A-Z]{2}$', codigo))


def validar_envio(codigo):
    """Valida rangos de fecha: año 2020-2030, mes 01-12, dia 01-31."""
    m = re.match(r'^ENV-(\d{4})-(\d{2})-(\d{2})-(\d{6})$', codigo)
    if not m:
        return False
    anio = int(m.group(1))
    mes = int(m.group(2))
    dia = int(m.group(3))
    return (2020 <= anio <= 2030) and (1 <= mes <= 12) and (1 <= dia <= 31)


def validar_empleado(codigo):
    """Valida departamento valido y que el numero no empiece con 0."""
    m = re.match(r'^EMP-([A-Z]{3})-([1-9]\d{3})$', codigo)
    if not m:
        return False
    departamento = m.group(1)
    return departamento in DEPARTAMENTOS_VALIDOS


def validar_factura(codigo):
    """Valida que la serie sea A-E en mayuscula."""
    m = re.match(r'^FAC-([A-Z])-\d{6}$', codigo)
    if not m:
        return False
    serie = m.group(1)
    return serie in SERIES_VALIDAS


def validar_codigo(codigo):
    """Detecta tipo y valida. Retorna (tipo, es_valido)."""
    tipo = detectar_tipo(codigo)
    if tipo == 'producto':
        return tipo, validar_producto(codigo)
    elif tipo == 'envio':
        return tipo, validar_envio(codigo)
    elif tipo == 'empleado':
        return tipo, validar_empleado(codigo)
    elif tipo == 'factura':
        return tipo, validar_factura(codigo)
    else:
        return 'desconocido', False


def main():
    print("codigo,tipo,valido")
    for linea in sys.stdin:
        codigo = linea.strip()
        if not codigo:
            continue
        tipo, es_valido = validar_codigo(codigo)
        print(f"{codigo},{tipo},{'VALIDO' if es_valido else 'INVALIDO'}")


if __name__ == "__main__":
    main()
