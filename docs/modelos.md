# Modelos de Datos

## Usuario (Custom User)
- Hereda de `AbstractUser` de Django.
- Campos adicionales:
  - `rol`: CharField, valores posibles: 'admin', 'user'.
- Métodos:
  - `es_admin()`: Devuelve True si el usuario es admin o superusuario.

## Tablas externas (SQL Server)
- `personnel_employee`: Empleados biométricos (id, nombre, departamento, etc.)
- `iclock_transaction`: Marcaciones biométricas (emp_code, punch_time, etc.)
- `personnel_department`: Departamentos

> Nota: No se migran estas tablas, se consultan directamente vía pyodbc.
