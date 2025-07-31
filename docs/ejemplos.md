# Ejemplos de Uso y Casos Comunes

## 1. ¿Cómo agregar un nuevo usuario admin?
- Ingresa como superusuario.
- Ve al panel de administración.
- Haz clic en "Nuevo usuario", completa los datos y selecciona el rol `admin`.

## 2. ¿Cómo cambiar el nombre de un departamento?
- Cambia el nombre directamente en la base de datos SQL Server en la tabla `personnel_department`.
- Los cambios se reflejan automáticamente en el sistema.

## 3. ¿Cómo agregar una columna extra al reporte?
- Edita la función de exportación en `views.py`.
- Agrega la columna en la consulta SQL y en la lista de headers del Excel o PDF.

## 4. ¿Cómo cambiar el logo o los colores?
- Cambia el archivo de imagen en `static/img/`.
- Edita los archivos CSS en `static/css/` para personalizar colores.

## 5. ¿Cómo agregar un nuevo filtro a los reportes?
- Modifica la función `obtener_reportes` en `db_utils.py` para aceptar el nuevo filtro.
- Agrega el campo en el formulario del template correspondiente.
