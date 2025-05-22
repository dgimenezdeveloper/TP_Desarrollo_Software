# App_Luminova/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import * # Importa todas tus vistas
from . import views # También podrías importar selectivamente
from django.conf import settings
from django.conf.urls.static import static
from .views import editar_usuario

app_name = 'App_LUMINOVA'

urlpatterns = [
    path("", inicio, name="inicio"),
    path("compras/", compras, name="compras"),
    path("produccion/", produccion, name="produccion"), # Esta podría ser 'ordenes'
    path("ventas/", ventas, name="ventas"),
    path("deposito/", deposito, name="deposito"),
    path("control_calidad/", control_calidad, name="control_calidad"),

    path('login/', auth_views.LoginView.as_view(template_name='login.html', next_page='App_LUMINOVA:dashboard'), name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard_view, name='dashboard'),
    
    path('roles-permisos/', views.roles_permisos, name='roles_permisos'),
    path('auditoria/', views.auditoria, name='auditoria'),

    path('usuarios/', lista_usuarios, name='lista_usuarios'),
    path('usuarios/crear/', crear_usuario, name='crear_usuario'),
    path('usuarios/editar/<int:id>/', editar_usuario, name='editar_usuario'),
    path('usuarios/eliminar/<int:id>/', eliminar_usuario, name='eliminar_usuario'),

    path("desglose/", desglose, name="desglose"),
    path("seguimiento/", seguimiento, name="seguimiento"),
    path("tracking/", tracking, name="tracking"),
    path("desglose2/", desglose2, name="desglose2"),

    path('ordenes/', ordenes, name='ordenes'), # Producción -> Órdenes
    path('planificacion/', planificacion, name='planificacion'), # Producción -> Planificación
    path('reportes/', reportes, name='reportes'), # Producción -> Reportes

    path('depo-seleccion/', depo_seleccion, name='depo_seleccion'),
    path('depo-enviar/', depo_enviar, name='depo_enviar'),

    # URLs AJAX para Depósito (NUEVAS Y MODIFICADAS)
    path('ajax/agregar-categoria-insumo/', agregar_categoria_insumo_ajax, name='agregar_categoria_insumo_ajax'),
    path('ajax/agregar-categoria-producto/', agregar_categoria_producto_ajax, name='agregar_categoria_producto_ajax'),
    path('ajax/get-items-por-categoria/', get_items_por_categoria_ajax, name='get_items_por_categoria_ajax'),
    
    path('ajax/agregar-insumo/', agregar_insumo_ajax, name='agregar_insumo_ajax'),
    path('ajax/get-insumo-data/', get_insumo_data, name='get_insumo_data'), # Para editar insumo
    path('ajax/editar-insumo/', editar_insumo_ajax, name='editar_insumo_ajax'),

    path('ajax/agregar-producto/', agregar_producto_ajax, name='agregar_producto_ajax'),
    path('ajax/get-producto-data/', get_producto_terminado_data, name='get_producto_terminado_data'), # Para editar producto
    path('ajax/editar-producto/', editar_producto_terminado_ajax, name='editar_producto_terminado_ajax'),

    path('ajax/eliminar-articulo/', eliminar_articulo_ajax, name='eliminar_articulo_ajax'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)