import pyodbc
import os
from datetime import datetime, time
from typing import List, Dict, Any, Optional
from django.db import connections
from django.db.utils import OperationalError

# --- Configuración de la Base de Datos (IGUAL QUE TU FLASK) ---
DB_DRIVER = os.getenv('DB_DRIVER', '{ODBC Driver 17 for SQL Server}')
# --- DB_SERVER = os.getenv('DB_SERVER', '192.168.0.9\\ATIEMPO')
DB_SERVER = os.getenv('DB_SERVER', 'DESKTOP-N84VS82') 
DB_NAME = os.getenv('DB_NAME', 'base2')
# --- DB_NAME = os.getenv('DB_NAME', 'UTIME')
DB_USER = os.getenv('DB_USER', '')
# --- DB_USER = os.getenv('DB_USER', 'tics2025')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
# --- DB_PASSWORD = os.getenv('DB_PASSWORD', 'tics2025')
HORA_LIMITE_ATRASO = time(8, 5)  # Optimizado: Usar time directamente

def get_db_connection() -> Optional[pyodbc.Connection]:
    """Establece conexión a SQL Server usando credenciales de entorno."""
    connection_string = (
        f'DRIVER={DB_DRIVER};SERVER={DB_SERVER};DATABASE={DB_NAME};'
        #f'UID={DB_USER};PWD={DB_PASSWORD};TrustServerCertificate=yes;'
        'Trusted_Connection=yes;TrustServerCertificate=yes;'
    )
    try:
        return pyodbc.connect(connection_string)
    except pyodbc.Error as ex:
        print(f"Error de conexión: {ex.args[0]}")
        return None

def _determinar_observacion(nombre_empleado: Optional[str], hora_ingreso: Optional[time]) -> str:
    """Determina observación según nombre y hora de ingreso."""
    if not nombre_empleado or not isinstance(nombre_empleado, str) or nombre_empleado.isdigit():
        return "Actualizar información"
    if not hora_ingreso:
        return "Sin registro"
    return "Atraso" if hora_ingreso > HORA_LIMITE_ATRASO else " "

def obtener_reportes(
    fecha_inicio: str,
    fecha_fin: str,
    id_usuario: Optional[str] = None,
    nombre: Optional[str] = None,
    departamento: Optional[str] = None
) -> List[Dict[str, Any]]:
    """EXACTAMENTE la misma función que tu Flask db.py - obtener_reportes"""
    reportes: List[Dict[str, Any]] = []
    base_query = """
    WITH RankedTransactions AS (
        SELECT 
            e.emp_code AS id_usuario,
            e.first_name AS nombre,
            d.dept_name AS departamento,
            CAST(t.punch_time AS DATE) AS fecha,
            CAST(t.punch_time AS TIME(0)) AS hora,
            ROW_NUMBER() OVER (
                PARTITION BY e.emp_code, CAST(t.punch_time AS DATE)
                ORDER BY t.punch_time
            ) AS RowNum
        FROM personnel_employee e
        JOIN iclock_transaction t ON e.emp_code = t.emp_code
        JOIN personnel_department d ON e.department_id = d.id
        WHERE CAST(t.punch_time AS DATE) BETWEEN ? AND ?
    """
    params: List[Any] = [fecha_inicio, fecha_fin]
    filter_conditions: List[str] = []

    if id_usuario:
        id_usuario_sin_ceros = id_usuario.lstrip('0')
        filter_conditions.append("(e.emp_code = ? OR e.emp_code = ?)")
        params.extend([id_usuario_sin_ceros, id_usuario.zfill(10)])
    if nombre:
        filter_conditions.append("e.first_name LIKE ?")
        params.append(f"%{nombre}%")
    if departamento:
        filter_conditions.append("d.dept_name = ?")
        params.append(departamento)

    query = base_query + (" AND " + " AND ".join(filter_conditions) if filter_conditions else "") + """
    )
    SELECT 
        id_usuario, nombre, departamento, fecha,
        MAX(CASE WHEN RowNum = 1 THEN hora END) AS hora_ingreso,
        MAX(CASE WHEN RowNum = 2 THEN hora END) AS hora_inicio_descanso,
        MAX(CASE WHEN RowNum = 3 THEN hora END) AS hora_fin_descanso,
        MAX(CASE WHEN RowNum = 4 THEN hora END) AS hora_salida
    FROM RankedTransactions
    GROUP BY id_usuario, nombre, departamento, fecha
    ORDER BY fecha, nombre;
    """

    conn = get_db_connection()
    if not conn:
        return reportes
    try:
        with conn.cursor() as cur:
            cur.execute(query, params)
            for row in cur.fetchall():
                hora_ingreso = row.hora_ingreso
                reportes.append({
                    "id_usuario": row.id_usuario,
                    "nombre": row.nombre,
                    "departamento": row.departamento,
                    "fecha": str(row.fecha) if row.fecha else "",
                    "hora_ingreso": str(hora_ingreso) if hora_ingreso else "",
                    "hora_inicio_descanso": str(row.hora_inicio_descanso) if row.hora_inicio_descanso else "",
                    "hora_fin_descanso": str(row.hora_fin_descanso) if row.hora_fin_descanso else "",
                    "hora_salida": str(row.hora_salida) if row.hora_salida else "",
                    "observacion": _determinar_observacion(row.nombre, hora_ingreso)
                })
    except pyodbc.Error as ex:
        print(f"Error en consulta: {ex.args[0]}")
    finally:
        conn.close()
    return reportes

def obtener_departamentos() -> List[str]:
    """EXACTAMENTE la misma función que tu Flask db.py - obtener_departamentos"""
    departamentos: List[str] = []
    query = "SELECT DISTINCT dept_name FROM personnel_department ORDER BY dept_name;"
    conn = get_db_connection()
    if not conn:
        return departamentos
    try:
        with conn.cursor() as cur:
            cur.execute(query)
            departamentos = [row[0] for row in cur.fetchall() if row[0]]
    except pyodbc.Error as ex:
        print(f"Error al obtener departamentos: {ex.args[0]}")
    finally:
        conn.close()
    return departamentos

def obtener_empleados(departamento: Optional[str] = None) -> List[Dict[str, Any]]:
    """Obtiene la lista de empleados, opcionalmente filtrada por departamento."""
    conn = get_db_connection()
    if not conn:
        return []

    empleados = []
    query = """
        SELECT DISTINCT 
            e.emp_code AS id_usuario,
            e.first_name AS nombre,
            d.dept_name AS departamento
        FROM personnel_employee e
        JOIN personnel_department d ON e.department_id = d.id
    """
    params = []
    if departamento:
        query += " WHERE d.dept_name = ?"
        params.append(departamento)
    
    query += " ORDER BY e.first_name"

    try:
        with conn.cursor() as cur:
            cur.execute(query, params)
            empleados = [
                {"id_usuario": row.id_usuario, "nombre": row.nombre, "departamento": row.departamento}
                for row in cur.fetchall()
            ]
    except pyodbc.Error as ex:
        print(f"Error al obtener empleados: {ex.args[0]}")
    finally:
        conn.close()
    return empleados

# === FUNCIONES MEJORADAS PARA ESTADÍSTICAS DEL DASHBOARD ===

def obtener_estadisticas_dashboard() -> Dict[str, Any]:
    """Obtiene todas las estadísticas del dashboard en una sola consulta optimizada"""
    from datetime import date
    
    conn = get_db_connection()
    if not conn:
        return {
            'total_empleados': 0,
            'empleados_registrados_hoy': 0,
            'ausentes_hoy': 0,
            'llegadas_tarde': 0,
            'porcentaje_asistencia': 0.0,
            'promedio_horas': "0.0 hrs"
        }
    
    hoy = date.today().strftime('%Y%m%d')
    
    try:
        with conn.cursor() as cur:
            # 1. Total de empleados activos
            cur.execute("SELECT COUNT(*) FROM personnel_employee WHERE is_active = 1")
            total_empleados = cur.fetchone()[0] or 0
            
            # 2. Empleados que marcaron HOY (al menos una marcación)
            cur.execute("""
                SELECT COUNT(DISTINCT e.emp_code)
                FROM personnel_employee e
                INNER JOIN iclock_transaction t ON e.emp_code = t.emp_code
                WHERE CAST(t.punch_time AS DATE) = ?
                AND e.is_active = 1
            """, hoy)
            empleados_registrados_hoy = cur.fetchone()[0] or 0
            
            # 3. Empleados que llegaron tarde (primera marcación después de 8:05)
            cur.execute("""
                SELECT COUNT(*)
                FROM (
                    SELECT 
                        e.emp_code,
                        MIN(t.punch_time) as primera_hora
                    FROM personnel_employee e
                    INNER JOIN iclock_transaction t ON e.emp_code = t.emp_code
                    WHERE CAST(t.punch_time AS DATE) = ?
                    AND e.is_active = 1
                    GROUP BY e.emp_code
                ) AS PrimeraMarcacion
                WHERE CAST(primera_hora AS TIME) > '08:05:00'
            """, hoy)
            llegadas_tarde = cur.fetchone()[0] or 0
            
            # 4. Calcular ausentes
            ausentes_hoy = max(0, total_empleados - empleados_registrados_hoy)
            
            # 5. Porcentaje de asistencia
            porcentaje_asistencia = (empleados_registrados_hoy / total_empleados * 100) if total_empleados > 0 else 0.0
            
            # 6. Promedio de horas trabajadas (última semana con datos)
            cur.execute("""
                SELECT AVG(CAST(DATEDIFF(MINUTE, entrada, salida) AS FLOAT) / 60.0) as promedio_horas
                FROM (
                    SELECT 
                        t.emp_code,
                        CAST(t.punch_time AS DATE) as fecha,
                        MIN(t.punch_time) as entrada,
                        MAX(t.punch_time) as salida
                    FROM iclock_transaction t
                    INNER JOIN personnel_employee e ON t.emp_code = e.emp_code
                    WHERE CAST(t.punch_time AS DATE) >= DATEADD(day, -7, ?)
                    AND e.is_active = 1
                    GROUP BY t.emp_code, CAST(t.punch_time AS DATE)
                    HAVING COUNT(*) >= 2
                    AND DATEDIFF(MINUTE, MIN(t.punch_time), MAX(t.punch_time)) BETWEEN 120 AND 720
                ) AS HorasTrabajadas
            """, hoy)
            
            result = cur.fetchone()
            promedio_horas_num = result[0] if result and result[0] else 8.0
            promedio_horas = f"{promedio_horas_num:.1f} hrs"
            
            return {
                'total_empleados': total_empleados,
                'empleados_registrados_hoy': empleados_registrados_hoy,
                'ausentes_hoy': ausentes_hoy,
                'llegadas_tarde': llegadas_tarde,
                'porcentaje_asistencia': round(porcentaje_asistencia, 1),
                'promedio_horas': promedio_horas
            }
            
    except pyodbc.Error as ex:
        print(f"Error al obtener estadísticas del dashboard: {ex.args[0]}")
        return {
            'total_empleados': 0,
            'empleados_registrados_hoy': 0,
            'ausentes_hoy': 0,
            'llegadas_tarde': 0,
            'porcentaje_asistencia': 0.0,
            'promedio_horas': "0.0 hrs"
        }
    finally:
        conn.close()

def obtener_total_empleados() -> int:
    """Obtiene el total de empleados activos"""
    conn = get_db_connection()
    if not conn:
        return 0
    
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT COUNT(*) 
                FROM personnel_employee 
                WHERE is_active = 1
            """)
            result = cur.fetchone()
            return result[0] if result else 0
    except pyodbc.Error as ex:
        print(f"Error al obtener total empleados: {ex.args[0]}")
        return 0
    finally:
        conn.close()

def obtener_asistencia_hoy() -> Dict[str, int]:
    """Obtiene estadísticas de asistencia del día actual - FUNCIÓN LEGACY"""
    # Esta función se mantiene por compatibilidad, pero se recomienda usar obtener_estadisticas_dashboard()
    stats = obtener_estadisticas_dashboard()
    return {
        'presentes': stats['empleados_registrados_hoy'],
        'ausentes': stats['ausentes_hoy'],
        'tarde': stats['llegadas_tarde'],
        'total': stats['total_empleados']
    }

def obtener_eficiencia_asistencia() -> float:
    """Calcula el porcentaje de eficiencia de asistencia - FUNCIÓN LEGACY"""
    # Esta función se mantiene por compatibilidad, pero se recomienda usar obtener_estadisticas_dashboard()
    stats = obtener_estadisticas_dashboard()
    return stats['porcentaje_asistencia']

def obtener_promedio_horas_trabajo() -> str:
    """Obtiene el promedio de horas trabajadas por día - FUNCIÓN LEGACY"""
    # Esta función se mantiene por compatibilidad, pero se recomienda usar obtener_estadisticas_dashboard()
    stats = obtener_estadisticas_dashboard()
    return stats['promedio_horas']
