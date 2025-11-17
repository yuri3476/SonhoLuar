# config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings               # <--- IMPORTANTE: Importe settings
from django.conf.urls.static import static     # <--- IMPORTANTE: Importe static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('catalogo.urls')),
]

# APENAS PARA AMBIENTE DE DESENVOLVIMENTO (DEBUG=True)
# Isso permite que o Django sirva arquivos estáticos e de mídia
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)