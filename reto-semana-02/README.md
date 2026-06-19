# Reto semana 02

Programa que convierte temperatura farenheit a celcius y clasifica ciudades con base a la temperatura.

## Instrucciones de uso

Usar un archivo de texto con la información a trabajar que contenga el nombre de la ciudad, la temperatura y el tipo de temperatura (F o C).

Meter en terminal el siguiente comando:

```bash
python3 main.py < entrada.txt > salida.txt
```

Esto generará una salida de texto con la información procesada y limpia.

## Ejemplo

**Entrada:**

ciudad,temperatura,unidad

CDMX,22,C

Nueva York,50,F

Moscu,-10,C

Miami,95,F

Cancun,30,C

Chicago,14,F

Phoenix,104,F

Error,abc,C

Lima,25,C

Bangkok,36,C

**Salida:** 

ciudad,temperatura_celsius,clasificacion

CDMX,22.0,Templado

Nueva York,10.0,Frio

Moscu,-10.0,Congelante

Miami,35.0,Calido

Cancun,30.0,Calido

Chicago,-10.0,Congelante

Phoenix,40.0,Extremo

Lima,25.0,Templado

Bangkok,36.0,Extremo

## Autor

Pérez Jiménez Emiliano