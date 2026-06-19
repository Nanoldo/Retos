# Sistema de Inventario Modular

## Descripcion
Sistema que genera reportes de productos que necesitan reorden.

## Estructura del Proyecto
```
reto_semana_04/
│
├── main.py                    # Punto de entrada
├── README.md                  # Documentacion
├── .gitignore                 # Archivos a ignorar
│
├── models/                    # Clases de dominio
│   ├── __init__.py
│   └── producto.py            # Clase Producto
│
├── utils/                     # Utilidades
│   ├── __init__.py
│   ├── io.py                  # Funciones de lectura/escritura
│   └── validators.py          # Funciones de validacion
│
├── data/                      # Datos de entrada
│   └── inventario.csv
│
└── outputs/                   # Resultados
    └── reporte_inventario.csv
```

## Como Ejecutar
```bash
python3 main.py
```
## Entrada
Archivo: data/inventario.csv

IMPORTANTE: Cada producto aparece una sola vez en el archivo de entrada, identificado por su SKU unico. No hay registros duplicados para el mismo producto, por lo tanto no se requiere consolidacion ni agrupacion. Cada linea representa el estado actual de un producto en el inventario.

### Columnas

Columna, Tipo, Descripción, Ejemplo  
sku, texto, Identificador único del producto, SKU001  
nombre, texto, Nombre del producto, Laptop HP  
categoría, texto, Categoría del producto, Electrónica  
precio, decimal, Precio unitario, 15000.00  
stock, entero, Cantidad actual en inventario, 5  
stock_mínimo, entero, Nivel mínimo antes de reordenar, 10

### Ejemplo entrada

csv  
sku,nombre,categoria,precio,stock,stock_minimo  
SKU001,Laptop HP,Electronica,15000.00,5,10  
SKU002,Mouse Logitech,Accesorios,350.00,3,15  
SKU003,Teclado Mecanico,Accesorios,N/A,20,10  
SKU004,Monitor LG,Electronica,6000.00,abc,5  
SKU005,Audifonos Sony,Accesorios,1200.00,2,???  
SKU006,Webcam HD,Accesorios  
SKU007,SSD 1TB,Almacenamiento,1800.00,0,5,dato_extra,otro

## Salida
Archivo: outputs/reporte_inventario.csv

El reporte debe contener solo productos que necesitan reorden (stock < stock_minimo).

IMPORTANTE: Como cada producto aparece una sola vez en la entrada (identificado por SKU unico), no se requiere hacer agregaciones ni consolidacion. Cada producto valido de la entrada que cumpla la condicion de reorden aparecera como una sola linea en la salida.

### Columnas de Salida

Columna, Tipo,	Descripción  
sku,	texto,	SKU del producto  
nombre,	texto,	Nombre del producto  
categoria,	texto,	Categoria  
stock_actual,	entero,	Stock actual  
stock_minimo,	entero,	Stock minimo requerido  
unidades_faltantes,	entero,	stock_minimo - stock_actual  
valor_inventario,	decimal, (2 dec)	precio * stock_actual

### Ordenamiento

Ordenar por unidades_faltantes descendente (los que necesitan mas unidades primero).

Ejemplo de Salida
Dada la entrada valida del ejemplo anterior (SKU001-SKU007 sin errores):

csv  
sku,nombre,categoria,stock_actual,stock_minimo,unidades_faltantes,valor_inventario  
SKU002,Mouse Logitech,Accesorios,3,15,12,1050.00  
SKU005,Audifonos Sony,Accesorios,2,10,8,2400.00  
SKU001,Laptop HP,Electronica,5,10,5,75000.00  
SKU007,SSD 1TB,Almacenamiento,0,5,5,0.00

## Autor
Pérez Jiménez Emiliano