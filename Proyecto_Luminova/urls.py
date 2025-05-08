from django.contrib import admin
from django.urls import path, include
from App_Luminova import views  # Importar vistas para la ruta base

urlpatterns = [
    path('admin/', admin.site.urls),  # Ruta para el panel de administración
    path('', views.inicio, name='inicio'),  # Ruta base que redirige a la vista de inicio
    path('App_Luminova/', include('App_Luminova.urls')),  # Incluir las rutas de App_Luminova
]