# Reto 7: Extractor y Analizador de Logs
 
**Programación para Ciencia de Datos — IPN**
 
## Descripción
 
Programa en Python que parsea logs de servidor en distintos formatos (HTTP, errores de aplicación, autenticación y base de datos), detecta patrones de seguridad sospechosos y genera un reporte estadístico completo.
 
Todo el procesamiento se basa en **expresiones regulares avanzadas**: grupos con nombre, `re.VERBOSE`, lookbehind y combinación de múltiples patrones.
 
## Requisitos
 
- Python 3.8 o superior
- Sin dependencias externas (solo librería estándar: `re`, `json`, `collections`, `typing`)
## Uso
 
```bash
python main.py
```
 
Al ejecutarse, el script:
1. Prueba cada parser individualmente con una línea de ejemplo.
2. Genera y muestra un reporte completo sobre el log de prueba (`LOGS_PRUEBA`).
3. Exporta el reporte a `reporte_logs.json`.
4. Muestra el análisis temporal (requests por hora) y los bots detectados.
Para usar tus propios logs, reemplaza la variable `LOGS_PRUEBA` o llama a `generar_reporte(tu_texto_de_logs)` directamente.
 
## Estructura del código
 
### Parte 1 — Parsers de logs
 
| Función | Formato de entrada | Detalle técnico |
|---|---|---|
| `parse_http_log(linea)` | `IP - - [fecha] "MÉTODO /ruta HTTP/1.1" status bytes "referer" "user-agent"` | Grupos nombrados + `re.VERBOSE` |
| `parse_error_log(linea)` | `[YYYY-MM-DD HH:MM:SS] NIVEL módulo - TipoError: mensaje` | Tipo de error y mensaje opcionales (soporta logs `INFO` sin esa parte) |
| `parse_auth_log(linea)` | `[AUTH] fecha \| user=... \| action=... \| status=... \| ip=... \| session=/attempts=` | Lookbehind `(?<=\|\s)` tras cada `=` |
| `parse_db_log(linea)` | `[DB-fecha] QUERY executed in Xs: ...` o `SLOW_QUERY (Xs): ...` | Detecta ambos subtipos en un solo patrón |
 
Cada parser retorna un `dict` con los campos extraídos, o `None` si la línea no coincide con el formato esperado.
 
### Parte 2 — Analizador de seguridad
 
- **`detectar_ataques_fuerza_bruta(logs_auth)`** — IPs con más de 3 intentos `LOGIN` con `status=FAILED`.
- **`detectar_sql_injection(logs_db)`** — usa la lista `PATRONES_SQL_INJECTION` (OR 1=1, UNION SELECT, comentarios `--`, DROP TABLE, DELETE FROM...WHERE 1=1) con `re.IGNORECASE`.
- **`detectar_path_traversal(logs_http)`** — busca `../`, `..\` y la variante codificada `%2e%2e%2f` en la ruta solicitada.
- **`detectar_errores_criticos(logs_error)`** — filtra niveles `ERROR`/`CRITICAL`, ordenados por timestamp.
### Parte 3 — Generador de reportes
 
- **`clasificar_linea(linea)`** — determina el tipo de una línea (`http`, `error`, `auth`, `db`, `desconocido`) antes de parsearla.
- **`generar_reporte(logs)`** — orquesta todo el pipeline: clasifica, parsea, calcula estadísticas (status HTTP agrupado en 2xx/3xx/4xx/5xx, top rutas sin query string, top IPs, errores por nivel/módulo) y ejecuta los 4 análisis de seguridad más el resumen de rendimiento (queries lentos y tiempo promedio).
- **`mostrar_reporte(reporte)`** — imprime el reporte con formato legible y emojis por sección.
### Bonus
 
- **`exportar_reporte_json(reporte, archivo)`** — guarda el reporte como `.json` (UTF-8, indentado).
- **`analisis_temporal(logs_http)`** — agrupa requests HTTP por hora del día.
- **`detectar_bots(logs_http)`** — identifica User-Agents típicos de bots/herramientas automatizadas (`curl`, `wget`, `python-requests`, `scrapy`, `sqlmap`, `PostmanRuntime`, etc.).
## Estructura del reporte (`generar_reporte`)
 
```python
{
    "resumen": {
        "total_lineas": int,
        "por_tipo": {"http": int, "error": int, "auth": int, "db": int}
    },
    "http": {
        "total_requests": int,
        "por_status": {"2xx": int, "3xx": int, "4xx": int, "5xx": int},
        "top_rutas": [(ruta, count), ...],
        "top_ips": [(ip, count), ...]
    },
    "errores": {
        "total": int,
        "por_nivel": {"ERROR": int, "WARNING": int, ...},
        "por_modulo": {modulo: count, ...}
    },
    "seguridad": {
        "alertas_fuerza_bruta": [...],
        "alertas_sql_injection": [...],
        "alertas_path_traversal": [...]
    },
    "rendimiento": {
        "queries_lentos": [...],
        "tiempo_promedio_queries": float
    }
}
```
 
## Notas
 
- Los datos de prueba (`LOGS_PRUEBA`) contienen 24 líneas válidas y producen 7 logs HTTP, 5 de error, 6 de autenticación y 6 de base de datos.
- El conteo de líneas y queries puede diferir ligeramente de ejemplos previos de la consigna si esos ejemplos no contaban correctamente sus propios datos de prueba; este programa refleja el conteo real de `LOGS_PRUEBA`.
- Todos los parsers son tolerantes a fallos: si una línea no coincide con el patrón, retornan `None` en lugar de lanzar una excepción.

## Alumno
Pérez Jiménez Emiliano