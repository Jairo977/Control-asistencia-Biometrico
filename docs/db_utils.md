# Funciones de Acceso a Base de Datos (`db_utils.py`)

## get_db_connection()
- Establece conexión a SQL Server usando pyodbc.

## obtener_reportes(fecha_inicio, fecha_fin, id_usuario, nombre, departamento)
- Devuelve reportes de asistencia filtrados.
- Consulta optimizada con CTE y partición por usuario y fecha.

## obtener_empleados(departamento=None)
- Devuelve todos los empleados o filtra por departamento.

## obtener_departamentos()
- Devuelve la lista de departamentos únicos.

## obtener_estadisticas_dashboard()
- Devuelve métricas globales: total empleados, presentes, ausentes, atrasos, promedio de horas.

---

Todas las funciones usan pyodbc y están optimizadas para consultas rápidas sobre grandes volúmenes de datos biométricos.
