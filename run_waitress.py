#!/usr/bin/env python
"""
Script para ejecutar Django con Waitress (Versión simplificada - Estilo Flask)
"""
import os
import django
from waitress import serve
from django.core.wsgi import get_wsgi_application

# Configurar Django (equivalente a "from app import app" en Flask)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reportes_asistencia.settings')
django.setup()
application = get_wsgi_application()  # Este es el "app" de Django

if __name__ == '__main__':
    # Simple como tu versión de Flask
    print("🚀 Iniciando servidor Django con Waitress...")
    print("📍 URL: http://0.0.0.0:8080")
    print("📍 URL Local: http://localhost:8080")
    print("🛑 Presiona Ctrl+C para detener")
    
    # Igual que tu Flask: serve(app, host='0.0.0.0', port=5000)
    serve(application, host='0.0.0.0', port=8080)
