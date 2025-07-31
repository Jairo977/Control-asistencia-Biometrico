from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    # Redirigir la raíz a la página de login de reportes
    path('', RedirectView.as_view(url='/reportes/login/', permanent=False), name='index_redirect'),
    # Sistema de reportes principal bajo el prefijo /reportes/
    path('reportes/', include('reportes.urls')),
]

# Servir archivos estáticos durante el desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
