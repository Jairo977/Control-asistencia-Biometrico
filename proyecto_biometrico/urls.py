"""
URL Configuration for proyecto_biometrico project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse

def favicon_view(request):
    """Vista simple para manejar favicon.ico"""
    return HttpResponse(status=204)  # No Content

urlpatterns = [
    path('admin/', admin.site.urls),
    path('reportes/', include('reportes.urls')),
    path('', include('reportes.urls')),  # Redirigir raíz a reportes
    path('favicon.ico', favicon_view, name='favicon'),  # Manejar favicon
]

# Servir archivos estáticos en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
