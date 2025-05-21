"""
Configuración de URL para el proyecto Proyecto_LUMINOVA.

La lista `urlpatterns` enruta las URLs a las vistas. Para más información, consulta:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Ejemplos:
Vistas de función
    1. Agrega una importación: from my_app import views
    2. Agrega una URL a urlpatterns: path('', views.home, name='home')
Vistas basadas en clases
    1. Agrega una importación: from other_app.views import Home
    2. Agrega una URL a urlpatterns: path('', Home.as_view(), name='home')
Inclusión de otra configuración de URL
    1. Importa la función include(): from django.urls import include, path
    2. Agrega una URL a urlpatterns: path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *
from . import views
from django.conf import settings # Importa settings
from django.conf.urls.static import static # Importa static

app_name = 'App_LUMINOVA'

urlpatterns = [
    path("", inicio, name="inicio"),
    path("compras/", compras, name="compras"),
    path("produccion/", produccion, name="produccion"),
    path("ventas/", ventas, name="ventas"),
    path("deposito/", deposito, name="deposito"),
    path("control_calidad/", control_calidad, name="control_calidad"),

    path('login/', auth_views.LoginView.as_view(template_name='login.html', next_page='App_LUMINOVA:dashboard'), name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard_view, name='dashboard'),
    
    path('roles-permisos/', views.roles_permisos, name='roles_permisos'),
    path('auditoria/', views.auditoria, name='auditoria'),

    # Ruta para el CRUD de Usuario
    path('usuarios/', lista_usuarios, name='lista_usuarios'),
    path('usuarios/crear/', crear_usuario, name='crear_usuario'),
    path('usuarios/editar/<int:id>/', editar_usuario, name='editar_usuario'),
    path('usuarios/eliminar/<int:id>/', eliminar_usuario, name='eliminar_usuario'),

# Rutas para los botones del sidebar de Compras
    path("desglose/", desglose, name="desglose"),
    path("seguimiento/", seguimiento, name="seguimiento"),
    path("tracking/", tracking, name="tracking"),
    path("desglose2/", desglose2, name="desglose2"),

# Rutas para los botones del sidebar de Producción
    path('ordenes/', ordenes, name='ordenes'),
    path('planificacion/', planificacion, name='planificacion'),
    path('reportes/', reportes, name='reportes'),

# Rutas para el botón Seleccionar de la tabla de OP// los botones del sidebar de Depósito
    path('depo-seleccion/', depo_seleccion, name='depo_seleccion'),
    path('depo-enviar/', depo_enviar, name='depo_enviar'),

    # URLs AJAX para Depósito
    path('agregar-insumo/', agregar_insumo_ajax, name='agregar_insumo_ajax'),
    path('get-insumos-por-categoria/', get_insumos_por_categoria, name='get_insumos_por_categoria'),
    path('get-insumo-data/', get_insumo_data, name='get_insumo_data'),
    path('editar-insumo/', editar_insumo_ajax, name='editar_insumo_ajax'),

    path('agregar-producto/', agregar_producto_ajax, name='agregar_producto_ajax'),
    path('get-productos-terminados/', get_productos_terminados, name='get_productos_terminados'),
    path('get-producto-terminado-data/', get_producto_terminado_data, name='get_producto_terminado_data'),
    path('editar-producto-terminado/', editar_producto_terminado_ajax, name='editar_producto_terminado_ajax'),

    path('eliminar-articulo/', eliminar_articulo_ajax, name='eliminar_articulo_ajax'), # Eliminación unificada

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # Sirve los archivos de medios durante el desarrollo