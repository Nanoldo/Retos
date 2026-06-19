# Reto Semana 6 – Validador de Códigos con Expresiones Regulares

**Programación para Ciencia de Datos – IPN, Semestre Febrero-Julio 2026**

---

## Descripción

Validador automático de códigos de una empresa de logística. Lee códigos desde `stdin` (uno por línea), detecta su tipo y verifica si cumplen el formato especificado, escribiendo el resultado como CSV en `stdout`.

## Tipos de código soportados

| Tipo | Formato | Ejemplo válido |
|------|---------|----------------|
| `producto` | `AAA-NNNN-XX` (3 mayús – 4 dígitos – 2 mayús) | `TEC-0001-MX` |
| `envio` | `ENV-YYYY-MM-DD-NNNNNN` (año 2020-2030, mes 01-12, día 01-31) | `ENV-2024-03-15-001234` |
| `empleado` | `EMP-DEP-NNNN` (depto válido, número no empieza en 0) | `EMP-VEN-1234` |
| `factura` | `FAC-S-NNNNNN` (serie A-E mayúscula, 6 dígitos) | `FAC-A-123456` |
| `desconocido` | No encaja en ningún formato | — siempre INVALIDO |

**Departamentos válidos:** `VEN`, `ADM`, `TEC`, `LOG`, `RHH`

## Uso

```bash
# Linux / Mac
python main.py < codigos.txt

# Guardar resultado
python main.py < codigos.txt > resultados.csv

# Windows PowerShell
Get-Content codigos.txt | python main.py

# Windows CMD
type codigos.txt | python main.py
```

## Ejemplo

**Entrada (`codigos.txt`):**
```
TEC-0001-MX
tec-0001-MX
ENV-2024-03-15-001234
EMP-VEN-0123
FAC-F-123456
XXX-1234
```

**Salida:**
```
codigo,tipo,valido
TEC-0001-MX,producto,VALIDO
tec-0001-MX,producto,INVALIDO
ENV-2024-03-15-001234,envio,VALIDO
EMP-VEN-0123,empleado,INVALIDO
FAC-F-123456,factura,INVALIDO
XXX-1234,desconocido,INVALIDO
```

## Estructura del proyecto

```
reto-semana-06/
├── README.md
├── main.py
├── .gitignore
└── tests/
    ├── codigos.txt
    └── salida_esperada.txt
```

## Cómo funciona

1. **`detectar_tipo(codigo)`** — usa `re.match` con patrones flexibles (case-insensitive) para identificar la estructura general del código.
2. **`validar_*(codigo)`** — aplica las reglas estrictas de cada tipo (mayúsculas, rangos numéricos, listas permitidas).
3. **`main()`** — lee `stdin` línea a línea, ignora líneas vacías, imprime el CSV.

## Requisitos

- Python 3.6+
- Sin dependencias externas (solo `re` y `sys` de la biblioteca estándar)

## Autor
Pérez Jiménez Emiliano
3AM1