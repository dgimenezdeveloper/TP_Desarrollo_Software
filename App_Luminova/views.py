from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib import messages


def inicio(request):
    if request.user.is_authenticated:
        return redirect('App_Luminova:dashboard')  # Redirige al dashboard si está autenticado
    return redirect('App_Luminova:login')  # Redirige al login si no está autenticado

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard.html')

    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST.get('username'),
            password=request.POST.get('password'),
        )
        if user:
            login(request, user)
            return redirect('App_Luminova:dashboard')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')

    return render(request, 'login.html')  

@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html') 

def logout_view(request):
    logout(request)
    return redirect('login')


def usuarios_view(request):
    return render(request, 'usuarios.html')  

def roles_permisos_view(request):
    return render(request, 'roles_permisos.html')

def auditoria_view(request):
    return render(request, 'auditoria.html')