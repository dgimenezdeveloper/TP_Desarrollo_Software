from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
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
    form = UserCreationForm()
    return render(request, 'usuarios.html', {'usuarios': usuarios, 'form': form})

# Creación de usuario
@login_required
@user_passes_test(es_admin)
def crear_usuario(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        rol_nombre = request.POST.get('rol')
        estado = request.POST.get('estado')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya existe.')
            return redirect('App_Luminova:lista_usuarios')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'El correo electrónico ya existe.')
            return redirect('App_Luminova:lista_usuarios')

        user = User.objects.create_user(username=username, email=email, is_active=(estado == 'Activo'))
        user.set_password('temporal')  # Establecer una contraseña temporal
        user.save()

        # Asignar rol
        try:
            rol = Group.objects.get(name=rol_nombre)
            user.groups.add(rol)
        except Group.DoesNotExist:
            messages.error(request, f'No existe el rol "{rol_nombre}".')
            user.delete()
            return redirect('App_Luminova:lista_usuarios')

        messages.success(request, 'Usuario creado exitosamente. La contraseña es "temporal".')
        return redirect('App_Luminova:lista_usuarios')
    else:
        form = UserCreationForm()
        return render(request, 'usuarios.html', {'form': form})

# Edición de usuario
@login_required
@user_passes_test(es_admin)
def editar_usuario(request, id):
    usuario = get_object_or_404(User, id=id)
    if request.method == 'POST':
        usuario.username = request.POST.get('username')
        usuario.email = request.POST.get('email')
        rol_nombre = request.POST.get('rol')
        usuario.is_active = request.POST.get('estado') == 'Activo'
        usuario.save()

         # Actualizar rol
        try:
            rol = Group.objects.get(name=rol_nombre)
            usuario.groups.clear()  # Elimina los roles anteriores
            usuario.groups.add(rol) # Agrega el nuevo rol
        except Group.DoesNotExist:
             messages.error(request, f'No existe el rol "{rol_nombre}".')
             return redirect('App_Luminova:lista_usuarios')

        messages.success(request, 'Usuario editado exitosamente.')
        return redirect('App_Luminova:lista_usuarios')
    else:
        form = UserChangeForm(instance=usuario)
        return render(request, 'usuarios.html', {'form': form, 'usuario': usuario})

# Eliminación de usuario
@login_required
@user_passes_test(es_admin)
def eliminar_usuario(request, id):
    usuario = get_object_or_404(User, id=id)
    if request.method == 'POST':
        usuario.delete()
        messages.success(request, 'Usuario eliminado exitosamente.')
        return redirect('App_Luminova:lista_usuarios')
    return render(request, 'eliminar_usuario.html', {'usuario': usuario})