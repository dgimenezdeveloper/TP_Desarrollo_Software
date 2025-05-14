from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Case, When, Value, IntegerField
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

#  Funciones para los botones del sidebar del Admin
def roles_permisos_view(request):
    return render(request, 'roles_permisos.html')

def auditoria_view(request):
    return render(request, 'auditoria.html')

# Funciones para las páginas de cada sección 
def compras_view(request):
    return render(request, 'compras.html')

def deposito_view(request):
    return render(request, 'deposito.html')

def produccion_view(request):
    return render(request, 'produccion.html')


# Funciones para los botones del sidebar de Producción
def ordenes_view(request):
    return render(request, 'ordenes.html')

def planificacion_view(request):
    return render(request, 'planificacion.html')

def reportes_view(request):
    return render(request, 'reportes.html')



# Funciones CRUD para los Usuarios
# Función para verificar si el usuario es administrador
def es_admin(user):
    return user.is_superuser

# Lista de usuarios
@login_required
@user_passes_test(es_admin)
def lista_usuarios(request):
    # Ordenar usuarios: primero el superusuario, luego los demás por ID
    usuarios = User.objects.annotate(
        es_superuser=Case(
            When(is_superuser=True, then=Value(0)),
            default=Value(1),
            output_field=IntegerField()
        )
    ).order_by('es_superuser', 'id')
    form = UserCreationForm() # Inicializa el formulario aquí para que esté disponible al renderizar la página
    return render(request, 'usuarios.html', {'usuarios': usuarios, 'form': form})

# Creación de usuario
@login_required
@user_passes_test(es_admin)
def crear_usuario(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario creado exitosamente.')
            return redirect('App_Luminova:lista_usuarios')
        else:
            messages.error(request, 'Error al crear el usuario.')
            return redirect('App_Luminova:lista_usuarios')  # Redirige de nuevo a la lista
    else:
        form = UserCreationForm() # Inicializa el formulario aquí
    return render(request, 'crear_usuario.html', {'form': form}) # Esto puede que no sea necesario

# Edición de usuario
@login_required
@user_passes_test(es_admin)
def editar_usuario(request, id):
    usuario = get_object_or_404(User, id=id)
    if request.method == 'POST':
        form = UserCreationForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario editado exitosamente.')
            return redirect('App_Luminova:lista_usuarios')
        else:
            messages.error(request, 'Error al editar el usuario.')
            return redirect('App_Luminova:lista_usuarios') #REdireccionamos a la lista
    else:
        form = UserCreationForm(instance=usuario) # Inicializa el form
    return render(request, 'editar_usuario.html', {'form': form, 'usuario': usuario}) # Esto puede que no sea necesario

# Eliminación de usuario
@login_required
@user_passes_test(es_admin)
def eliminar_usuario(request, id):
    usuario = get_object_or_404(User, id=id)
    if request.method == 'POST':
        usuario.delete()
        messages.success(request, 'Usuario eliminado exitosamente.')
        return redirect('App_Luminova:lista_usuarios')
    return render(request, 'eliminar_usuario.html', {'usuario': usuario}) # Esto puede que no ser necesario
