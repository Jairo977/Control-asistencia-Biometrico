# Arquitectura del Sistema Biométrico

Este documento describe la arquitectura general del sistema, el flujo de datos y la relación entre los principales módulos.

## Componentes principales

- **Django**: Framework web principal.
- **SQL Server**: Base de datos biométrica externa.
- **pyodbc**: Conector para consultas directas a SQL Server.
- **Bootstrap**: Interfaz de usuario responsiva.

## Flujo general

1. El usuario accede al sistema y se autentica.
2. Según su rol, accede a dashboards, reportes o administración.
3. Las vistas consultan la base biométrica usando funciones de `db_utils.py`.
4. Los datos se muestran en tablas, dashboards o se exportan a PDF/Excel.

## Relación de módulos

- `views.py`: Controla la lógica de negocio y renderiza las vistas.
- `db_utils.py`: Realiza todas las consultas SQL directas.
- `models.py`: Define el modelo de usuario y roles.
- `templates/`: Contiene los HTMLs para cada sección.

---

El sistema está optimizado para consultas rápidas y acceso seguro a datos biométricos reales.
