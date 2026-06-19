# Perfilador de Datasets

Herramienta que analiza archivos CSV y genera reportes de calidad de datos.

## Requisitos

- Python 3.8 o superior

## Instalacion

### 1. Clonar el repositorio
```bash
git clone https://github.com/usuario/reto-semana-05.git
cd reto-semana-05
```

### 2. Crear ambiente virtual
```bash
python -m venv .venv
```

### 3. Activar ambiente virtual
```bash
# Windows
.venv\\Scripts\\activate

# Linux/Mac
source .venv/bin/activate
```

### 4. Instalar dependencias
```bash
pip install -r requirements.txt
```

## Uso

```bash
python main.py --input <archivo_entrada.csv> --output <archivo_salida.csv>
```

### Ejemplo
```bash
python main.py --input data/ventas.csv --output outputs/perfil_ventas.csv
```

## Formato de Salida

El perfil generado contiene las siguientes columnas:

| Columna | Descripcion |
|---------|-------------|
| nombre_columna | Nombre de la columna |
| tipo_inferido | Tipo detectado (numerico/texto/fecha/booleano) |
| total_registros | Total de filas |
| valores_nulos | Cantidad de valores vacios |
| porcentaje_nulos | Porcentaje de nulos |
| valores_unicos | Cantidad de valores distintos |
| porcentaje_unicos | Porcentaje de unicidad |
| ejemplo_valor | Primer valor no nulo |

## Autor

Pérez Jiménez Emiliano - Mayo 2026