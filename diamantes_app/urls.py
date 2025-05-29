from django.urls import path
from . import views
from .views import prediccion_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.lista_diamantes, name='lista_diamantes'),
    path('prediccion/', prediccion_view, name='prediccion'),
    path('batch_prediccion/', views.batch_prediccion_view, name='batch_prediccion'),
]

# 👇 Esto permite servir archivos subidos por el usuario (como tus CSV procesados)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)