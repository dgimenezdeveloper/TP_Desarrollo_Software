from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'App_Luminova'  # Namespace para evitar conflictos de nombres

urlpatterns = [
    path('', views.inicio, name='inicio'),  # Página de inicio
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),  # Página de login
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # Cerrar sesión
    path('dashboard/', views.dashboard_view, name='dashboard'),  # Dashboard
    path('usuarios/', views.usuarios_view, name='usuarios'),  # Página de usuarios
    path('roles-permisos/', views.roles_permisos_view, name='roles-permisos'),  # Roles y permisos
    path('auditoria/', views.auditoria_view, name='auditoria'),  # Auditoría de accesos
    
    path('compras/', views.compras_view, name='compras'), # Página de compras
    path('deposito/', views.deposito_view, name='deposito'),
]