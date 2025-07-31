# Documentación de Vistas

Este documento describe cada vista del sistema, su URL, propósito, parámetros y lógica principal.

## Vistas principales

### 1. `registros_hoy_dashboard`
- **URL:** `/reportes/registros-hoy/dashboard/`
- **Propósito:** Lista todos los usuarios y su última marcación.
- **Lógica:** Consulta optimizada a SQL Server para obtener empleados y su última marcación en una sola consulta. Renderiza la tabla en el template.

### 2. `reportes_view`
- **URL:** `/reportes/reportes-section/`
- **Propósito:** Permite filtrar y consultar reportes de asistencia por fecha, usuario o departamento.
- **Parámetros:** `fecha_inicio`, `fecha_fin`, `id_usuario`, `nombre`, `departamento`.
- **Lógica:** Llama a `obtener_reportes` de `db_utils.py` y muestra los resultados.

### 3. `dashboard_admin`
- **URL:** `/reportes/dashboard-admin/`
- **Propósito:** Panel de administración de usuarios (solo superusuarios).
- **Lógica:** CRUD de usuarios usando el modelo de Django.

### 4. `configuracion_view`
- **URL:** `/reportes/configuracion-section/`
- **Propósito:** Permite cambiar credenciales y ajustar parámetros del sistema.

### 5. `descargar_excel_registros_hoy` y `descargar_pdf_registros_hoy`
- **Propósito:** Exportan la lista de usuarios y su última marcación a Excel o PDF.

---

Cada vista está protegida por autenticación y permisos según el rol del usuario.
