@login_required
@csrf_exempt
def download_pdf(request):
    """Genera y descarga un reporte en PDF con texto ajustado automáticamente."""
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    id_usuario = request.GET.get('id_usuario')
    nombre = request.GET.get('nombre')
    departamento = request.GET.get('departamento')
    
    reportes = db_utils.obtener_reportes(fecha_inicio, fecha_fin, id_usuario, nombre, departamento)
    
    # Determinar el encabezado y nombre de archivo dinámicamente
    if id_usuario:
        nombre_empleado = reportes[0]['nombre'] if reportes and reportes[0]['nombre'] else f"ID_{id_usuario}"
        header_title = f"Reporte Individual de {nombre_empleado}"
        filename_pdf = f"Reporte_de_{nombre_empleado.replace(' ', '_')}.pdf"
    elif nombre:
        header_title = f"Reporte Individual de {nombre}"
        filename_pdf = f"Reporte_de_{nombre.replace(' ', '_')}.pdf"
    elif departamento:
        header_title = f"Reporte de {departamento}"
        filename_pdf = f"Reporte_de_{departamento.replace(' ', '_')}.pdf"
    else:
        header_title = "Reporte General"
        filename_pdf = "Reporte_General.pdf"

    buffer = BytesIO()
    # Usar landscape para todos los reportes para mejor aprovechamiento del espacio
    page_size = landscape(letter)
    p = canvas.Canvas(buffer, pagesize=page_size)
    width, height = page_size

    # Encabezado principal
    p.setFont("Helvetica-Bold", 16)
    p.drawString(40, height - 40, header_title.upper())
    p.setFont("Helvetica", 10)
    p.drawString(40, height - 60, f"Periodo: {fecha_inicio or ''} a {fecha_fin or ''}")
    p.drawString(40, height - 75, f"Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

    if not reportes:
        p.setFont("Helvetica-Bold", 14)
        p.drawString(40, height - 120, "NO HAY DATOS PARA MOSTRAR")
    else:
        # Configuración optimizada para landscape (792 puntos de ancho)
        y = height - 100
        base_row_height = 20  # Altura base mínima por fila
        
        # Configuración de columnas con anchos optimizados para todo el ancho de página
        headers = ["ID\nUSUARIO", "NOMBRE\nCOMPLETO", "DEPARTAMENTO\nORGANIZACIÓN", "FECHA\nREGISTRO", "PRIMERA\nMARCACIÓN", "SEGUNDA\nMARCACIÓN", "TERCERA\nMARCACIÓN", "CUARTA\nMARCACIÓN", "OBSERVACIONES\nESTADO"]
        col_positions = [40, 110, 200, 300, 360, 430, 500, 570, 640]
        col_widths = [65, 85, 95, 55, 65, 65, 65, 65, 85]
        
        # Dibujar headers con texto centrado y ajustado
        p.setFont("Helvetica-Bold", 8)
        for i, header in enumerate(headers):
            lines = header.split('\n')
            for j, line in enumerate(lines):
                p.drawString(col_positions[i], y - (j * 10), line)
        
        # Línea separadora
        p.line(35, y-25, width-35, y-25)
        y -= 35
        
        # Datos con ajuste automático
        p.setFont("Helvetica", 8)
        for reporte in reportes:
            # Preparar datos
            datos = [
                str(reporte['id_usuario']) if reporte['id_usuario'] else "",
                str(reporte['nombre']) if reporte['nombre'] else "",
                str(reporte['departamento']) if reporte['departamento'] else "",
                reporte['fecha'] or "",
                reporte['hora_ingreso'] or "",
                reporte['hora_inicio_descanso'] or "",
                reporte['hora_fin_descanso'] or "",
                reporte['hora_salida'] or "",
                str(reporte['observacion']) if reporte['observacion'] else ""
            ]
            
            # Calcular la altura necesaria para esta fila
            max_lines = 1
            wrapped_data = []
            
            for i, dato in enumerate(datos):
                if dato:
                    # Calcular cuántas líneas necesita este dato
                    chars_per_line = max(1, int(col_widths[i] / 6))  # Aproximación de caracteres por línea
                    wrapped_text = textwrap.fill(str(dato), width=chars_per_line)
                    lines = wrapped_text.split('\n')
                    max_lines = max(max_lines, len(lines))
                    wrapped_data.append(lines)
                else:
                    wrapped_data.append([''])
            
            row_height = max(base_row_height, max_lines * 12)
            
            # Verificar si necesitamos nueva página
            if y - row_height < 60:
                p.showPage()
                y = height - 100
                # Repetir headers en nueva página
                p.setFont("Helvetica-Bold", 8)
                for i, header in enumerate(headers):
                    lines = header.split('\n')
                    for j, line in enumerate(lines):
                        p.drawString(col_positions[i], y - (j * 10), line)
                p.line(35, y-25, width-35, y-25)
                y -= 35
                p.setFont("Helvetica", 8)
            
            # Resaltar atrasos
            if reporte.get('observacion') == 'Atraso':
                p.setFillColorRGB(1, 0.95, 0.95)
                p.rect(35, y-row_height+8, width-70, row_height-3, stroke=0, fill=1)
                p.setFillColorRGB(0, 0, 0)
            
            # Dibujar cada celda con texto ajustado
            for i, lines in enumerate(wrapped_data):
                for j, line in enumerate(lines):
                    if line:
                        p.drawString(col_positions[i], y - (j * 10), line)
            
            y -= row_height

    p.save()
    buffer.seek(0)
    
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename_pdf}"'
    return response
