import re
import json
from typing import Dict, List, Optional, Tuple
from collections import Counter, defaultdict


# =====================================================================
# PARTE 1: Parsers de Logs
# =====================================================================

# Patrón para log HTTP (Apache/Nginx) - usa re.VERBOSE para legibilidad
# Ej: 192.168.1.100 - - [15/Mar/2024:10:23:45 -0600] "GET /api/users HTTP/1.1" 200 1234 "https://ejemplo.com" "Mozilla/5.0"
PATRON_HTTP = re.compile(r'''
    ^(?P<ip>\d{1,3}(?:\.\d{1,3}){3})\s+        # Dirección IP
    -\s+-\s+                                    # Identidad / usuario (sin usar, típicamente "-")
    \[(?P<timestamp>[^\]]+)\]\s+                # Fecha/hora entre corchetes
    "(?P<method>[A-Z]+)\s+                      # Método HTTP
    (?P<path>\S+)\s+                            # Ruta solicitada
    HTTP/[\d.]+"\s+                             # Versión de protocolo
    (?P<status>\d{3})\s+                        # Código de estado
    (?P<bytes>\d+)\s+                           # Bytes enviados
    "(?P<referer>[^"]*)"\s+                     # Referer
    "(?P<user_agent>[^"]*)"                     # User-Agent
''', re.VERBOSE)


def parse_http_log(linea: str) -> Optional[Dict]:
    """
    Parsea una línea de log HTTP.

    Ejemplo de entrada:
    192.168.1.100 - - [15/Mar/2024:10:23:45 -0600] "GET /api/users HTTP/1.1" 200 1234 "https://ejemplo.com" "Mozilla/5.0"
    """
    match = PATRON_HTTP.match(linea)
    if not match:
        return None
    data = match.groupdict()
    return {
        "ip": data["ip"],
        "timestamp": data["timestamp"],
        "method": data["method"],
        "path": data["path"],
        "status": int(data["status"]),
        "bytes": int(data["bytes"]),
        "referer": data["referer"],
        "user_agent": data["user_agent"],
    }


# Patrón para log de errores
# Ej: [2024-03-15 10:25:12] ERROR app.module.submodule - DatabaseConnectionError: Connection refused
PATRON_ERROR = re.compile(r'''
    ^\[(?P<timestamp>\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\]\s+   # [YYYY-MM-DD HH:MM:SS]
    (?P<level>ERROR|WARNING|INFO|DEBUG|CRITICAL)\s+                # Nivel del log
    (?P<module>[\w.]+)\s+                                          # Módulo (con puntos)
    -\s+
    (?:(?P<error_type>\w+)\s*:\s*(?P<message>.*)                   # ErrorType: mensaje
       |
       (?P<solo_mensaje>.*)                                        # mensaje simple (ej. INFO)
    )$
''', re.VERBOSE)


def parse_error_log(linea: str) -> Optional[Dict]:
    """
    Parsea una línea de log de errores.

    Ejemplo de entrada:
    [2024-03-15 10:25:12] ERROR app.module.submodule - DatabaseConnectionError: Connection refused
    """
    match = PATRON_ERROR.match(linea)
    if not match:
        return None
    data = match.groupdict()
    error_type = data["error_type"] or ""
    message = data["message"] if data["message"] is not None else (data["solo_mensaje"] or "")
    return {
        "timestamp": data["timestamp"],
        "level": data["level"],
        "module": data["module"],
        "error_type": error_type,
        "message": message,
    }


# Patrón para log de autenticación
# Usa lookbehind (?<=...) para extraer valores después de '='
# Ej: [AUTH] 2024-03-15 10:30:00 | user=admin@empresa.com | action=LOGIN | status=SUCCESS | ip=10.0.0.5 | session=abc123xyz
PATRON_AUTH = re.compile(r'''
    ^\[AUTH\]\s+
    (?P<timestamp>\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\s*\|\s*
    (?<=\|\s)user=(?P<user>[^\s|]+)\s*\|\s*
    (?<=\|\s)action=(?P<action>[^\s|]+)\s*\|\s*
    (?<=\|\s)status=(?P<status>[^\s|]+)\s*\|\s*
    (?<=\|\s)ip=(?P<ip>[^\s|]+)
    (?:\s*\|\s*(?<=\|\s)session=(?P<session>[^\s|]+))?
    (?:\s*\|\s*(?<=\|\s)attempts=(?P<attempts>[^\s|]+))?
''', re.VERBOSE)


def parse_auth_log(linea: str) -> Optional[Dict]:
    """
    Parsea una línea de log de autenticación.

    Ejemplo de entrada:
    [AUTH] 2024-03-15 10:30:00 | user=admin@empresa.com | action=LOGIN | status=SUCCESS | ip=10.0.0.5
    """
    match = PATRON_AUTH.match(linea)
    if not match:
        return None
    data = match.groupdict()

    extra = {}
    if data.get("session"):
        extra["session"] = data["session"]
    if data.get("attempts"):
        extra["attempts"] = int(data["attempts"])

    return {
        "timestamp": data["timestamp"],
        "user": data["user"],
        "action": data["action"],
        "status": data["status"],
        "ip": data["ip"],
        "extra": extra,
    }


# Patrón para log de base de datos
# Debe detectar QUERY y SLOW_QUERY
# Ej: [DB-2024-03-15 10:35:22] QUERY executed in 0.045s: SELECT * FROM users
# Ej: [DB-2024-03-15 10:36:00] SLOW_QUERY (2.5s): SELECT * FROM orders JOIN products
PATRON_DB = re.compile(r'''
    ^\[DB-(?P<timestamp>\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\]\s+   # [DB-YYYY-MM-DD HH:MM:SS]
    (?P<query_type>QUERY|SLOW_QUERY)\s+
    (?:
        executed\s+in\s+(?P<tiempo_query>[\d.]+)s          # QUERY executed in 0.045s
        |
        \((?P<tiempo_slow>[\d.]+)s\)                        # SLOW_QUERY (2.5s)
    )
    \s*:\s*
    (?P<query>.+)$                                          # Consulta SQL completa
''', re.VERBOSE)


def parse_db_log(linea: str) -> Optional[Dict]:
    """
    Parsea una línea de log de base de datos.

    Ejemplos de entrada:
    [DB-2024-03-15 10:35:22] QUERY executed in 0.045s: SELECT * FROM users
    [DB-2024-03-15 10:36:00] SLOW_QUERY (2.5s): SELECT * FROM orders JOIN products
    """
    match = PATRON_DB.match(linea)
    if not match:
        return None
    data = match.groupdict()
    tiempo = data["tiempo_query"] if data["tiempo_query"] is not None else data["tiempo_slow"]
    return {
        "timestamp": data["timestamp"],
        "query_type": data["query_type"],
        "execution_time": float(tiempo),
        "query": data["query"].strip(),
    }


# =====================================================================
# PARTE 2: Analizador de Seguridad
# =====================================================================

def detectar_ataques_fuerza_bruta(logs_auth: List[Dict]) -> List[Dict]:
    """
    Detecta IPs con múltiples intentos fallidos de login.
    Criterio: más de 3 intentos FAILED desde la misma IP.

    Retorna: lista de IPs sospechosas con número de intentos.
    """
    fallidos_por_ip = Counter()

    for log in logs_auth:
        if log.get("action") == "LOGIN" and log.get("status") == "FAILED":
            fallidos_por_ip[log["ip"]] += 1

    alertas = [
        {"ip": ip, "intentos": intentos}
        for ip, intentos in fallidos_por_ip.items()
        if intentos > 3
    ]
    alertas.sort(key=lambda a: a["intentos"], reverse=True)
    return alertas


# Patrones de SQL Injection a detectar
PATRONES_SQL_INJECTION = [
    r"(?i)\bOR\b\s+['\"]?\d+['\"]?\s*=\s*['\"]?\d+",  # OR 1=1
    r"(?i)\bUNION\b.*\bSELECT\b",                       # UNION SELECT
    r"--",                                               # Comentario SQL
    r"(?i)\bDROP\b\s+\bTABLE\b",                        # DROP TABLE
    r"(?i)\bDELETE\b\s+\bFROM\b.*\bWHERE\b\s+1\s*=\s*1", # DELETE WHERE 1=1
]

_PATRONES_SQL_COMPILADOS = [re.compile(p) for p in PATRONES_SQL_INJECTION]


def detectar_sql_injection(logs_db: List[Dict]) -> List[Dict]:
    """
    Detecta posibles intentos de SQL injection en las queries.
    """
    alertas = []
    for log in logs_db:
        query = log.get("query", "")
        for patron in _PATRONES_SQL_COMPILADOS:
            if patron.search(query):
                alertas.append(log)
                break
    return alertas


def detectar_path_traversal(logs_http: List[Dict]) -> List[Dict]:
    """
    Detecta intentos de path traversal en las rutas HTTP.
    Busca patrones como: ../, ..\\, %2e%2e%2f
    """
    patron_traversal = re.compile(r'''
        \.\.[/\\]
        # ../  o  ..\  (subida de directorio)
        |
        %2e%2e%2f
        # ..%2f codificado en URL
    ''', re.VERBOSE | re.IGNORECASE)

    alertas = []
    for log in logs_http:
        path = log.get("path", "")
        if patron_traversal.search(path):
            alertas.append(log)
    return alertas


def detectar_errores_criticos(logs_error: List[Dict]) -> List[Dict]:
    """
    Filtra y retorna errores de nivel ERROR o CRITICAL,
    ordenados por timestamp.
    """
    criticos = [log for log in logs_error if log.get("level") in ("ERROR", "CRITICAL")]
    criticos.sort(key=lambda log: log["timestamp"])
    return criticos


# =====================================================================
# PARTE 3: Generador de Reportes
# =====================================================================

def clasificar_linea(linea: str) -> str:
    """
    Clasifica una línea de log por su tipo.
    Retorna: 'http', 'error', 'auth', 'db', o 'desconocido'
    """
    if linea.startswith("[AUTH]"):
        return "auth"
    if linea.startswith("[DB-"):
        return "db"
    if re.match(r'^\d{1,3}(?:\.\d{1,3}){3}\s+-\s+-\s+\[', linea):
        return "http"
    if re.match(r'^\[\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}\]\s+(ERROR|WARNING|INFO|DEBUG|CRITICAL)\b', linea):
        return "error"
    return "desconocido"


def _clasificar_status(status: int) -> str:
    """Clasifica un código de estado HTTP en su categoría (2xx, 3xx, 4xx, 5xx)."""
    return f"{status // 100}xx"


def generar_reporte(logs: str) -> Dict:
    """
    Genera un reporte completo analizando todos los logs.
    """
    lineas = [l for l in logs.strip().split("\n") if l.strip()]

    logs_http: List[Dict] = []
    logs_error: List[Dict] = []
    logs_auth: List[Dict] = []
    logs_db: List[Dict] = []

    por_tipo = Counter()

    parsers = {
        "http": parse_http_log,
        "error": parse_error_log,
        "auth": parse_auth_log,
        "db": parse_db_log,
    }
    destinos = {
        "http": logs_http,
        "error": logs_error,
        "auth": logs_auth,
        "db": logs_db,
    }

    for linea in lineas:
        tipo = clasificar_linea(linea)
        por_tipo[tipo] += 1

        if tipo in parsers:
            resultado = parsers[tipo](linea)
            if resultado is not None:
                destinos[tipo].append(resultado)

    # --- Resumen ---
    resumen = {
        "total_lineas": len(lineas),
        "por_tipo": {
            "http": por_tipo.get("http", 0),
            "error": por_tipo.get("error", 0),
            "auth": por_tipo.get("auth", 0),
            "db": por_tipo.get("db", 0),
        },
    }

    # --- HTTP ---
    por_status = Counter()
    rutas = Counter()
    ips = Counter()
    for log in logs_http:
        por_status[_clasificar_status(log["status"])] += 1
        ruta_base = log["path"].split("?", 1)[0]
        rutas[ruta_base] += 1
        ips[log["ip"]] += 1

    http_stats = {
        "total_requests": len(logs_http),
        "por_status": dict(por_status),
        "top_rutas": rutas.most_common(),
        "top_ips": ips.most_common(),
    }

    # --- Errores ---
    por_nivel = Counter(log["level"] for log in logs_error)
    por_modulo = Counter(log["module"] for log in logs_error)

    errores_stats = {
        "total": len(logs_error),
        "por_nivel": dict(por_nivel),
        "por_modulo": dict(por_modulo),
    }

    # --- Seguridad ---
    seguridad_stats = {
        "alertas_fuerza_bruta": detectar_ataques_fuerza_bruta(logs_auth),
        "alertas_sql_injection": detectar_sql_injection(logs_db),
        "alertas_path_traversal": detectar_path_traversal(logs_http),
    }

    # --- Rendimiento ---
    queries_lentos = [log for log in logs_db if log["query_type"] == "SLOW_QUERY"]
    tiempos = [log["execution_time"] for log in logs_db]
    tiempo_promedio = sum(tiempos) / len(tiempos) if tiempos else 0.0

    rendimiento_stats = {
        "queries_lentos": queries_lentos,
        "tiempo_promedio_queries": tiempo_promedio,
    }

    return {
        "resumen": resumen,
        "http": http_stats,
        "errores": errores_stats,
        "seguridad": seguridad_stats,
        "rendimiento": rendimiento_stats,
    }


# =====================================================================
# Datos de Prueba
# =====================================================================

LOGS_PRUEBA = """
192.168.1.100 - - [15/Mar/2024:10:23:45 -0600] "GET /api/users HTTP/1.1" 200 1234 "https://ejemplo.com" "Mozilla/5.0 (Windows NT 10.0)"
192.168.1.101 - - [15/Mar/2024:10:23:46 -0600] "POST /api/login HTTP/1.1" 200 89 "-" "curl/7.68.0"
192.168.1.102 - - [15/Mar/2024:10:23:47 -0600] "GET /admin/../../../etc/passwd HTTP/1.1" 403 0 "-" "sqlmap/1.0"
[2024-03-15 10:24:00] INFO app.startup - Application started successfully on port 8080
[2024-03-15 10:25:12] ERROR app.database - DatabaseConnectionError: Connection refused to host db.server.com:5432
[2024-03-15 10:25:15] WARNING app.cache - CacheWarning: Redis connection timeout, using fallback
[2024-03-15 10:26:00] ERROR app.auth - AuthenticationError: Invalid token for user admin@empresa.com
[AUTH] 2024-03-15 10:30:00 | user=admin@empresa.com | action=LOGIN | status=SUCCESS | ip=10.0.0.5 | session=abc123xyz
[AUTH] 2024-03-15 10:31:00 | user=hacker@mail.com | action=LOGIN | status=FAILED | ip=192.168.1.50 | attempts=1
[AUTH] 2024-03-15 10:31:30 | user=hacker@mail.com | action=LOGIN | status=FAILED | ip=192.168.1.50 | attempts=2
[AUTH] 2024-03-15 10:32:00 | user=hacker@mail.com | action=LOGIN | status=FAILED | ip=192.168.1.50 | attempts=3
[AUTH] 2024-03-15 10:32:30 | user=hacker@mail.com | action=LOGIN | status=FAILED | ip=192.168.1.50 | attempts=4
[AUTH] 2024-03-15 10:33:00 | user=otro@empresa.com | action=LOGOUT | status=SUCCESS | ip=10.0.0.10 | session=def456uvw
[DB-2024-03-15 10:35:22] QUERY executed in 0.045s: SELECT * FROM users WHERE email = 'admin@empresa.com'
[DB-2024-03-15 10:35:25] QUERY executed in 0.012s: SELECT id, name FROM products WHERE active = 1
[DB-2024-03-15 10:36:00] SLOW_QUERY (2.5s): SELECT * FROM orders o JOIN products p ON o.product_id = p.id JOIN users u ON o.user_id = u.id
[DB-2024-03-15 10:37:00] QUERY executed in 0.001s: SELECT * FROM users WHERE username = 'admin' OR 1=1--'
[DB-2024-03-15 10:38:00] QUERY executed in 0.002s: SELECT * FROM users UNION SELECT * FROM passwords
192.168.1.200 - - [15/Mar/2024:10:40:00 -0600] "GET /products?id=1 HTTP/1.1" 200 5678 "https://tienda.com" "Mozilla/5.0"
192.168.1.200 - - [15/Mar/2024:10:40:05 -0600] "GET /products?id=2 HTTP/1.1" 200 4321 "https://tienda.com" "Mozilla/5.0"
192.168.1.201 - - [15/Mar/2024:10:41:00 -0600] "GET /api/users HTTP/1.1" 401 123 "-" "PostmanRuntime/7.26.8"
192.168.1.201 - - [15/Mar/2024:10:41:05 -0600] "GET /api/users HTTP/1.1" 500 0 "-" "PostmanRuntime/7.26.8"
[2024-03-15 10:42:00] ERROR app.api - NullPointerException: Cannot read property 'id' of undefined
[DB-2024-03-15 10:45:00] SLOW_QUERY (5.2s): SELECT COUNT(*) FROM logs WHERE date > '2024-01-01'
""".strip()


# =====================================================================
# Funciones de Visualización
# =====================================================================

def mostrar_reporte(reporte: Dict) -> None:
    """Muestra el reporte de forma legible."""
    print("=" * 70)
    print("                    REPORTE DE ANÁLISIS DE LOGS")
    print("=" * 70)

    # Resumen
    print("\n📊 RESUMEN GENERAL")
    print("-" * 40)
    print(f"Total de líneas procesadas: {reporte['resumen']['total_lineas']}")
    print("Por tipo:")
    for tipo, count in reporte['resumen']['por_tipo'].items():
        print(f"  • {tipo.upper()}: {count}")

    # HTTP
    if 'http' in reporte:
        print("\n🌐 LOGS HTTP")
        print("-" * 40)
        print(f"Total requests: {reporte['http']['total_requests']}")
        print("Por código de estado:")
        for status, count in reporte['http']['por_status'].items():
            print(f"  • {status}: {count}")
        print("Top 5 rutas más solicitadas:")
        for ruta, count in reporte['http'].get('top_rutas', [])[:5]:
            print(f"  • {ruta}: {count} requests")

    # Errores
    if 'errores' in reporte:
        print("\n❌ ERRORES")
        print("-" * 40)
        print(f"Total errores: {reporte['errores']['total']}")
        print("Por nivel:")
        for nivel, count in reporte['errores']['por_nivel'].items():
            print(f"  • {nivel}: {count}")

    # Seguridad
    if 'seguridad' in reporte:
        print("\n🔒 ALERTAS DE SEGURIDAD")
        print("-" * 40)

        fb = reporte['seguridad'].get('alertas_fuerza_bruta', [])
        if fb:
            print(f"⚠️  Posibles ataques de fuerza bruta: {len(fb)}")
            for alerta in fb:
                print(f"     IP: {alerta['ip']} - {alerta['intentos']} intentos fallidos")

        sql = reporte['seguridad'].get('alertas_sql_injection', [])
        if sql:
            print(f"⚠️  Posibles SQL Injection: {len(sql)}")
            for alerta in sql[:3]:  # Mostrar solo las primeras 3
                print(f"     Query: {alerta['query'][:60]}...")

        pt = reporte['seguridad'].get('alertas_path_traversal', [])
        if pt:
            print(f"⚠️  Posibles Path Traversal: {len(pt)}")
            for alerta in pt[:3]:
                print(f"     Ruta: {alerta['path']}")

    # Rendimiento
    if 'rendimiento' in reporte:
        print("\n⏱️  RENDIMIENTO")
        print("-" * 40)
        print(f"Queries lentos detectados: {len(reporte['rendimiento'].get('queries_lentos', []))}")
        if 'tiempo_promedio_queries' in reporte['rendimiento']:
            print(f"Tiempo promedio de queries: {reporte['rendimiento']['tiempo_promedio_queries']:.3f}s")

    print("\n" + "=" * 70)


# =====================================================================
# Bonus: Funcionalidades Extra
# =====================================================================

def exportar_reporte_json(reporte: Dict, archivo: str) -> None:
    """Exporta el reporte a un archivo JSON."""
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(reporte, f, indent=2, ensure_ascii=False)


def analisis_temporal(logs_http: List[Dict]) -> Dict:
    """
    Analiza distribución de requests por hora.

    Retorna:
        {"hora": count, ...}
    """
    patron_hora = re.compile(r':(?P<hora>\d{2}):\d{2}:\d{2}\s')
    conteo_por_hora = Counter()

    for log in logs_http:
        match = patron_hora.search(log["timestamp"] + " ")
        if match:
            conteo_por_hora[match.group("hora")] += 1

    return dict(sorted(conteo_por_hora.items()))


# User-Agents conocidos de bots
PATRON_BOTS = re.compile(
    r'(?i)\b(curl|wget|python-requests|scrapy|sqlmap|bot|spider|crawler|postmanruntime)\b'
)


def detectar_bots(logs_http: List[Dict]) -> List[Dict]:
    """
    Detecta requests que parecen venir de bots.
    Busca User-Agents conocidos de bots: curl, wget, python-requests, scrapy, etc.
    """
    return [log for log in logs_http if PATRON_BOTS.search(log.get("user_agent", ""))]


# =====================================================================
# Programa principal
# =====================================================================

def main() -> None:
    # Prueba de parsers individuales
    print("PRUEBA DE PARSERS")
    print("=" * 50)

    # HTTP
    linea_http = '192.168.1.100 - - [15/Mar/2024:10:23:45 -0600] "GET /api/users HTTP/1.1" 200 1234 "https://ejemplo.com" "Mozilla/5.0"'
    print("\n-- Parser HTTP --")
    print(f"Entrada: {linea_http[:60]}...")
    print(f"Resultado: {parse_http_log(linea_http)}")

    # Error
    linea_error = "[2024-03-15 10:25:12] ERROR app.database - DatabaseConnectionError: Connection refused"
    print("\n-- Parser Error --")
    print(f"Entrada: {linea_error}")
    print(f"Resultado: {parse_error_log(linea_error)}")

    # Auth
    linea_auth = "[AUTH] 2024-03-15 10:30:00 | user=admin@empresa.com | action=LOGIN | status=SUCCESS | ip=10.0.0.5 | session=abc123xyz"
    print("\n-- Parser Auth --")
    print(f"Entrada: {linea_auth}")
    print(f"Resultado: {parse_auth_log(linea_auth)}")

    # DB
    linea_db = "[DB-2024-03-15 10:35:22] QUERY executed in 0.045s: SELECT * FROM users"
    print("\n-- Parser DB --")
    print(f"Entrada: {linea_db}")
    print(f"Resultado: {parse_db_log(linea_db)}")

    # Prueba del reporte completo
    print("\nGENERANDO REPORTE COMPLETO...\n")
    reporte = generar_reporte(LOGS_PRUEBA)
    mostrar_reporte(reporte)

    # Bonus: exportar a JSON
    exportar_reporte_json(reporte, "reporte_logs.json")
    print("\n📁 Reporte exportado a 'reporte_logs.json'")

    # Bonus: análisis temporal
    logs_http = [log for log in (parse_http_log(l) for l in LOGS_PRUEBA.split("\n")) if log]
    print("\n⏰ ANÁLISIS TEMPORAL (requests por hora)")
    print("-" * 40)
    for hora, count in analisis_temporal(logs_http).items():
        print(f"  • {hora}:00 - {count} requests")

    # Bonus: detección de bots
    bots = detectar_bots(logs_http)
    print(f"\n🤖 BOTS DETECTADOS: {len(bots)}")
    print("-" * 40)
    for bot in bots:
        print(f"  • {bot['ip']} - {bot['user_agent']}")


if __name__ == "__main__":
    main()
