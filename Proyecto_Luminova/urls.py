from django.contrib import admin
from django.urls import path, include
from App_Luminova import views  # Importar vistas para la ruta base
from django.conf import settings  # Importar configuraciones
from django.conf.urls.static import static  # Importar static

urlpatterns = [
    path('admin/', admin.site.urls),  # Ruta para el panel de administración
    path('', views.inicio, name='inicio'),  # Ruta base que redirige a la vista de inicio
    path('App_LUMINOVA/', include('App_Luminova.urls')),  # Incluir las rutas de App_LUMINOVA
]

if settings.DEBUG:  
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT) 