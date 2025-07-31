"""
URLs DJANGO REPORTES - Sistema limpio y funcional
"""
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'reportes'

urlpatterns = [
    # Vista de registros de hoy
    path('registros-hoy/', views.registros_hoy, name='registros_hoy'),
    path('registros-hoy/dashboard/', views.registros_hoy_dashboard, name='registros_hoy_dashboard'),
    # Página de inicio como raíz y bienvenida
    path('', views.bienvenida, name='index'),
    path('bienvenida/', views.bienvenida, name='bienvenida'),
    # Elimina duplicados y rutas a inicio_view
    path('dashboard/', views.index, name='dashboard'),
    
    # Autenticación usando las vistas de Django
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('registros-hoy/excel/', views.descargar_excel_registros_hoy, name='descargar_excel_registros_hoy'),
    path('registros-hoy/pdf/', views.descargar_pdf_registros_hoy, name='descargar_pdf_registros_hoy'),
    path('logout/', auth_views.LogoutView.as_view(next_page='reportes:login'), name='logout'),
    
    # API endpoints
    path('api/reports/', views.api_reports, name='api_reports'),
    path('api/reports/pdf/', views.download_pdf, name='download_pdf'),
    path('api/reports/excel/', views.download_excel_simple, name='download_excel_simple'),
    path('api/reports/excel-advanced/', views.download_excel_advanced, name='download_excel_advanced'),
    path('api/departamentos/', views.api_departamentos, name='api_departamentos'),
    path('api/empleados/', views.api_empleados, name='api_empleados'),

    # Sección de reportes
    path('reportes/', views.reportes_view, name='reportes_section'),

    # Sección de configuración
    path('configuracion/', views.configuracion_view, name='configuracion_section'),
    path('cambiar-credenciales/', views.cambiar_credenciales, name='cambiar_credenciales'),

    # Ayuda
    path('ayuda/', views.ayuda_view, name='ayuda'),

    # Rutas para administración
    path('dashboard-admin/', views.dashboard_admin, name='dashboard_admin'),
    path('usuarios-admin/', views.usuarios_admin, name='usuarios_admin'),
    path('usuario-nuevo/', views.usuario_nuevo, name='usuario_nuevo'),
    path('usuario-editar/<int:usuario_id>/', views.usuario_editar, name='usuario_editar'),
    path('usuario-eliminar/<int:usuario_id>/', views.usuario_eliminar, name='usuario_eliminar'),
]
