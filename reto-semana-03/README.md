# Reto semana 03

Programa que genera reporte de ventas.

## Instrucciones de uso

Usar un archivo de texto con la información a trabajar que contenga la fecha, producto, cantidad y precio unitario. El programa deberá devolver un reporte con el producto, unidades vendidas, ingreso total y precio promedio.

Meter en terminal el siguiente comando:

```bash
python3 main.py < entrada.txt > salida.txt
```

Esto generará una salida de texto con la información procesada y limpia.

## Ejemplo

**Entrada:**


fecha,producto,cantidad,precio_unitario

2026-01-01,Laptop,2,15000.00

2026-01-02,Mouse,10,250.00

2026-01-03,Laptop,1,14500.00

2026-01-04,Teclado,5,800.00

2026-01-05,Mouse,8,250.00


**Salida:** 


producto,unidades_vendidas,ingreso_total,precio_promedio

Laptop,3,44500.00,14833.33

Mouse,18,4500.00,250.00

Teclado,5,4000.00,800.00

## Autor

Pérez Jiménez Emiliano