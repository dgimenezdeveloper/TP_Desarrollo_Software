from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'App_Luminova'  # Namespace para evitar conflictos de nombres

urlpatterns = [
    path('', views.inicio, name='inicio'),  # Página de inicio
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),  # Página de login
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # Cerrar sesión
    path('dashboard/', views.dashboard_view, name='dashboard'),  # Dashboard
    #path('usuarios/', views.usuarios_view, name='usuarios'),  # Página de usuarios
    path('roles-permisos/', views.roles_permisos_view, name='roles-permisos'),  # Roles y permisos
    path('auditoria/', views.auditoria_view, name='auditoria'),  # Auditoría de accesos
    
    path('compras/', views.compras_view, name='compras'), 
    path('deposito/', views.deposito_view, name='deposito'),
    
    # Path para las páginas de Producción y sus botones
    path('produccion/', views.produccion_view, name='produccion'),
    path('ordenes/', views.ordenes_view, name='ordenes'),
    path('planificacion/', views.planificacion_view, name='planificacion'),
    path('reportes/', views.reportes_view, name='reportes'),
    
    # Path para el crud de Usuario
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('usuarios/crear/', views.crear_usuario, name='crear_usuario'),
    path('usuarios/editar/<int:id>/', views.editar_usuario, name='editar_usuario'),
    path('usuarios/eliminar/<int:id>/', views.eliminar_usuario, name='eliminar_usuario'),
]