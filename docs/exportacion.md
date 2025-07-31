# Documentación de Exportación de Reportes

## Exportar a PDF
- Usa la librería ReportLab.
- Las vistas `download_pdf` y `descargar_pdf_registros_hoy` generan un PDF con los datos filtrados.
- El PDF incluye encabezados, datos tabulares y estilos.
- Si quieres cambiar el formato, edita la lógica en `views.py` (función `download_pdf`).

## Exportar a Excel
- Usa la librería openpyxl.
- Las vistas `download_excel_simple` y `descargar_excel_registros_hoy` generan archivos `.xlsx`.
- El archivo incluye estilos, colores y autoajuste de columnas.
- Para agregar nuevas columnas, edita la lista `headers` y los datos en la función correspondiente.

---

**¿Cómo agregar un nuevo tipo de exportación?**
- Crea una nueva función en `views.py` usando la librería deseada.
- Agrega la ruta en `urls.py` y el botón en el template correspondiente.
