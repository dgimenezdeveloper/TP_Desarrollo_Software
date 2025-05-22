# App_LUMINOVA/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.forms import UserCreationForm, UserChangeForm # Mantén esto para tus vistas de usuario
from django.contrib.auth.decorators import login_required # Mantén login_required
from django.db import transaction
from .models import (
    Insumo, ProductoTerminado, CategoriaInsumo, CategoriaProductoTerminado, # Asegúrate que CategoriaProductoTerminado esté aquí
    AuditoriaAcceso, Orden, Proveedor, Cliente, Factura, RolDescripcion
)

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt # Para AJAX, pero considera csrf_protect si es posible
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.hashers import make_password # Para hashear contraseñas
# from django.db.models import Count # No se usa activamente en la vista deposito ahora

# Importar TODOS los formularios necesarios
from .forms import (
    InsumoForm,
    ProductoTerminadoForm,
    CategoriaInsumoForm,         
    CategoriaProductoTerminadoForm,
    RolForm, PermisosRolForm
)


def compras(req):
    return render(req, "compras/compras.html")

def produccion(req):
    return render(req, "produccion/produccion.html")

def ventas(req):
    return render(req, "ventas/ventas.html")

@login_required
def deposito(req):
    categorias_insumos = CategoriaInsumo.objects.all().order_by('nombre')
    categorias_productos = CategoriaProductoTerminado.objects.all().order_by('nombre')

    form_agregar_insumo = InsumoForm()
    form_agregar_producto = ProductoTerminadoForm()
    form_crear_categoria_insumo = CategoriaInsumoForm() 
    form_crear_categoria_producto = CategoriaProductoTerminadoForm() 

    context = {
        "categorias_insumos": categorias_insumos,
        "categorias_productos_terminados": categorias_productos, 
        "form_agregar_insumo": form_agregar_insumo,
        "form_agregar_producto": form_agregar_producto,
        "form_crear_categoria_insumo": form_crear_categoria_insumo,
        "form_crear_categoria_producto": form_crear_categoria_producto,
    }
    return render(req, "deposito/deposito.html", context)


def control_calidad(req):
    return render(req, "control_calidad/control_calidad.html")

def inicio(request):
    if request.user.is_authenticated:
        return redirect('App_LUMINOVA:dashboard')
    return redirect('App_LUMINOVA:login')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('App_LUMINOVA:dashboard')
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST.get('username'),
            password=request.POST.get('password'),
        )
        if user:
            login(request, user)
            return redirect('App_LUMINOVA:dashboard')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    return render(request, 'login.html')

@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html')

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "Has cerrado sesión correctamente.")
    return redirect('App_LUMINOVA:login')

@login_required # Añadir login_required si es necesario
def roles_permisos(request):
    # Asegúrate que Group y RolDescripcion son importados y usados correctamente
    roles = Group.objects.prefetch_related('permissions', 'descripcion_extendida').all()
    context = {'roles': roles}
    return render(request, 'dashboard/roles_permisos.html', context)


@login_required # Añadir login_required
def auditoria(request):
    auditorias = AuditoriaAcceso.objects.all().order_by('-fecha_acceso')
    context = {'auditorias': auditorias}
    return render(request, 'dashboard/auditoria.html', context)

# --- CRUD de usuario (mantener como estaba si funcionaba) ---
@login_required
def lista_usuarios(request):
    usuarios = User.objects.all().prefetch_related('groups') # prefetch groups para eficiencia
    return render(request, 'dashboard/usuarios.html', {'usuarios': usuarios})

""" @login_required
@require_POST # Es buena práctica restringir a POST para acciones que modifican datos
def crear_usuario(request):
    # Esta vista debería manejar la creación completa, incluyendo la asignación de rol (grupo) y estado
    # Aquí un ejemplo simplificado que asume que el formulario maneja la creación básica.
    # Necesitarías un formulario más completo o lógica adicional aquí.
    if request.method == 'POST':
        # Aquí deberías usar un formulario personalizado, no UserCreationForm directamente
        # para manejar el rol y el estado. Por ahora, mantenemos tu lógica original
        # pero ten en cuenta que UserCreationForm no maneja grupos ni is_active directamente.
        # username = request.POST.get('username')
        # email = request.POST.get('email')
        # password = make_password(request.POST.get('password')) # ¡DEBES HASHEAR LA CONTRASEÑA!
        # rol_name = request.POST.get('rol')
        # estado_str = request.POST.get('estado')
        # is_active = estado_str == 'Activo'

        # user = User.objects.create_user(username=username, email=email, password=password, is_active=is_active)
        # if rol_name:
        #     group = Group.objects.get(name=rol_name)
        #     user.groups.add(group)
        # messages.success(request, f"Usuario {username} creado exitosamente.")
        # return redirect('App_LUMINOVA:lista_usuarios')
        #
        # MANTENIENDO TU LÓGICA ORIGINAL POR AHORA:
        form = UserCreationForm(request.POST) # UserCreationForm no maneja roles/grupos ni estado is_active
        if form.is_valid():
            user = form.save() # Guarda el usuario básico
            # Lógica adicional para rol y estado
            rol_name = request.POST.get('rol')
            if rol_name:
                try:
                    group = Group.objects.get(name=rol_name)
                    user.groups.add(group)
                except Group.DoesNotExist:
                    messages.error(request, f"El rol '{rol_name}' no existe.")

            estado_str = request.POST.get('estado')
            user.is_active = (estado_str == 'Activo')
            user.save() # Guardar cambios de rol y estado

            messages.success(request, f"Usuario '{user.username}' creado exitosamente.")
            return redirect('App_LUMINOVA:lista_usuarios')
        else:
            # Si el formulario no es válido, renderiza la plantilla de usuarios con errores
            # o una plantilla específica de creación con el formulario y sus errores.
            # Para simplificar, redirigimos con un mensaje de error.
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error en {field}: {error}")
            return redirect('App_LUMINOVA:lista_usuarios') # O renderizar un form_crear_usuario.html

    # Si no es POST, simplemente redirige (o muestra un formulario GET si lo tienes)
    return redirect('App_LUMINOVA:lista_usuarios')
"""
@login_required
def dashboard_view(request):
    return render(request, 'dashboard/dashboard.html')

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "Has cerrado sesión correctamente.")
    return redirect('App_LUMINOVA:login')

@login_required # Añadir login_required si es necesario
def roles_permisos(request):
    # Asegúrate que Group y RolDescripcion son importados y usados correctamente
    roles = Group.objects.prefetch_related('permissions', 'descripcion_extendida').all()
    context = {'roles': roles}
    return render(request, 'dashboard/roles_permisos.html', context)


@login_required # Añadir login_required
def auditoria(request):
    auditorias = AuditoriaAcceso.objects.all().order_by('-fecha_acceso')
    context = {'auditorias': auditorias}
    return render(request, 'dashboard/auditoria.html', context)

# --- CRUD de usuario (mantener como estaba si funcionaba) ---
@login_required
def lista_usuarios(request):
    usuarios = User.objects.all().prefetch_related('groups') # prefetch groups para eficiencia
    return render(request, 'dashboard/usuarios.html', {'usuarios': usuarios})

@login_required
# @require_POST # Descomentar si es solo AJAX POST
def crear_usuario(request):
    if request.method == 'POST':
        # ESTE FORMULARIO ES MUY BÁSICO. Deberías crear un CustomUserCreationForm
        # que incluya campos para email, rol, y estado.
        # Por ahora, tomaremos los datos directamente del POST y validaremos manualmente.

        username = request.POST.get('username')
        email = request.POST.get('email')
        rol_name = request.POST.get('rol')
        estado_str = request.POST.get('estado')
        password = request.POST.get('password', 'luminova123') # Deberías tener un campo de contraseña en el modal
        
        errors = {}
        if not username: errors['username'] = 'Este campo es requerido.'
        if User.objects.filter(username=username).exists(): errors['username'] = 'Este nombre de usuario ya existe.'
        if not email: errors['email'] = 'Este campo es requerido.'
        # Añadir más validaciones (ej. formato de email)

        if errors:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest': # Si es AJAX
                return JsonResponse({'success': False, 'errors': errors})
            else: # Si es un POST normal
                for field, error_list in errors.items():
                    for err in error_list if isinstance(error_list, list) else [error_list]:
                         messages.error(request, f"Error en {field}: {err}")
                return redirect('App_LUMINOVA:lista_usuarios')


        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password # ¡DEBE SER HASHEADA! Usa make_password si no usas un form de Django que lo haga.
            )
            user.is_active = (estado_str == 'Activo')

            if rol_name:
                try:
                    group = Group.objects.get(name=rol_name)
                    user.groups.add(group)
                except Group.DoesNotExist:
                    # Manejar el caso de que el grupo no exista, quizás con un error.
                    user.delete() # Rollback de la creación del usuario
                    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                        return JsonResponse({'success': False, 'errors': {'rol': [f"El rol '{rol_name}' no existe."]}})
                    else:
                        messages.error(request, f"El rol '{rol_name}' no existe.")
                        return redirect('App_LUMINOVA:lista_usuarios')
            
            user.save()

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True, 
                    'user': { # Devuelve los datos del usuario para añadirlo a la tabla dinámicamente
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'rol': rol_name if rol_name else "Sin Rol",
                        'estado': "Activo" if user.is_active else "Inactivo"
                    }
                })
            else:
                messages.success(request, f"Usuario '{user.username}' creado exitosamente.")
                return redirect('App_LUMINOVA:lista_usuarios')

        except Exception as e:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': {'__all__': [str(e)]}})
            else:
                messages.error(request, f"Error al crear usuario: {str(e)}")
                return redirect('App_LUMINOVA:lista_usuarios')
    
    # Si es GET, podrías renderizar un formulario o simplemente no hacer nada si el modal se maneja en la misma página.
    # Por ahora, si no es POST, no hacemos nada especial, asumiendo que el modal está en lista_usuarios.html
    return redirect('App_LUMINOVA:lista_usuarios') # O renderizar la página con el modal

@login_required
@require_POST # Es buena práctica
def editar_usuario(request, id):
    usuario = get_object_or_404(User, id=id)
    if request.method == 'POST':
        # De nuevo, UserChangeForm es limitado. Un form personalizado es mejor.
        # form = UserChangeForm(request.POST, instance=usuario)
        # if form.is_valid():
        #     form.save()
        #     messages.success(request, f"Usuario '{usuario.username}' actualizado.")
        #     return redirect('App_LUMINOVA:lista_usuarios')
        # else:
        #     for field, errors in form.errors.items():
        #         for error in errors:
        #             messages.error(request, f"Error al editar {field}: {error}")
        #     return redirect('App_LUMINOVA:lista_usuarios') # O renderizar form_editar_usuario.html

        # Lógica manual para actualizar campos básicos, rol y estado
        usuario.username = request.POST.get('username', usuario.username)
        usuario.email = request.POST.get('email', usuario.email)
        
        # Actualizar rol
        rol_name = request.POST.get('rol')
        usuario.groups.clear() # Limpiar roles existentes
        if rol_name:
            try:
                group = Group.objects.get(name=rol_name)
                usuario.groups.add(group)
            except Group.DoesNotExist:
                messages.error(request, f"El rol '{rol_name}' no existe.")
        
        # Actualizar estado
        estado_str = request.POST.get('estado')
        if estado_str: # Asegurarse que 'estado' está en POST
            usuario.is_active = (estado_str == 'Activo')
        
        usuario.save()
        messages.success(request, f"Usuario '{usuario.username}' actualizado exitosamente.")
        return redirect('App_LUMINOVA:lista_usuarios')
    return redirect('App_LUMINOVA:lista_usuarios') # Si no es POST


@login_required
@require_POST # Es buena práctica
def eliminar_usuario(request, id):
    usuario = get_object_or_404(User, id=id)
    if usuario == request.user:
        messages.error(request, "No puedes eliminar tu propia cuenta.")
        return redirect('App_LUMINOVA:lista_usuarios')
    try:
        nombre_usuario = usuario.username
        usuario.delete()
        messages.success(request, f"Usuario '{nombre_usuario}' eliminado exitosamente.")
    except Exception as e:
        messages.error(request, f"Error al eliminar usuario: {str(e)}")
    return redirect('App_LUMINOVA:lista_usuarios')

def depo_seleccion(request):
    return render(request, "depo-seleccion.html")

def depo_enviar(request):
    return render(request, "depo-enviar.html")

# --- Rutas y vistas para botones de sidebar de Compras y Producción (mantener si ya existen) ---
def desglose(req): return render(req, "desglose.html")
def seguimiento(req): return render(req, "seguimiento.html")
def tracking(req): return render(req, "tracking.html")
def desglose2(req): return render(req, "desglose2.html")
def ordenes(req): return render(req, "ordenes.html")
def planificacion(req): return render(req, "planificacion.html")
def reportes(req): return render(req, "reportes.html")
def depo_seleccion(request): return render(request, "depo-seleccion.html")
def depo_enviar(request): return render(request, "depo-enviar.html")



# Vistas AJAX para Insumos
@csrf_exempt
@require_POST
def agregar_insumo_ajax(request):
    if request.method == 'POST':
        form = InsumoForm(request.POST, request.FILES)
        if form.is_valid():
            insumo = form.save()
            categoria_nombre = insumo.categoria.nombre if insumo.categoria else None
            return JsonResponse({'success': True, 'insumo_id': insumo.id, 'categoria_nombre': categoria_nombre})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False, 'error': 'Método de petición inválido.'}, status=400)


# NUEVA: Vista AJAX para agregar CategoriaInsumo
@csrf_exempt # Considerar usar csrf_protect si el JS puede manejarlo
@require_POST
def agregar_categoria_insumo_ajax(request):
    form = CategoriaInsumoForm(request.POST, request.FILES)
    if form.is_valid():
        categoria = form.save()
        return JsonResponse({'success': True, 'categoria_id': categoria.id, 'nombre': categoria.nombre, 'imagen_url': categoria.imagen.url if categoria.imagen else ''})
    return JsonResponse({'success': False, 'errors': form.errors})

# NUEVA: Vista AJAX para agregar CategoriaProductoTerminado
@csrf_exempt
@require_POST
def agregar_categoria_producto_ajax(request):
    form = CategoriaProductoTerminadoForm(request.POST, request.FILES)
    if form.is_valid():
        categoria = form.save()
        return JsonResponse({'success': True, 'categoria_id': categoria.id, 'nombre': categoria.nombre, 'imagen_url': categoria.imagen.url if categoria.imagen else ''})
    return JsonResponse({'success': False, 'errors': form.errors})



# MODIFICADA/NUEVA: Vista AJAX para obtener ítems por categoría
@require_GET
def get_items_por_categoria_ajax(request):
    categoria_id = request.GET.get('categoria_id')
    item_type = request.GET.get('item_type')
    items_data = []
    success = False

    if not categoria_id or not item_type:
        return JsonResponse({'success': False, 'error': 'Faltan parámetros: categoria_id o item_type.'}, status=400)

    try:
        if item_type == 'insumo':
            categoria = get_object_or_404(CategoriaInsumo, id=categoria_id)
            items = Insumo.objects.filter(categoria=categoria)
            for item in items:
                items_data.append({
                    'id': item.id,
                    'descripcion': item.descripcion,
                    'fabricante': item.fabricante,
                    'precio_unitario': str(item.precio_unitario),
                    'stock': item.stock,
                    'imagen_url': item.imagen.url if item.imagen else None,
                })
            success = True
        elif item_type == 'producto':
            categoria = get_object_or_404(CategoriaProductoTerminado, id=categoria_id)
            items = ProductoTerminado.objects.filter(categoria=categoria)
            for item in items:
                items_data.append({
                    'id': item.id,
                    'descripcion': item.descripcion,
                    'precio_unitario': str(item.precio_unitario),
                    'stock': item.stock,
                    'imagen_url': item.imagen.url if item.imagen else None, # Si ProductoTerminado tiene imagen
                })
            success = True
        else:
            return JsonResponse({'success': False, 'error': 'Tipo de ítem no válido.'}, status=400)
        
        return JsonResponse({'success': success, 'items': items_data, 'categoria_nombre': categoria.nombre})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

# --- CRUDs AJAX para Insumo (ya existentes, pueden requerir pequeños ajustes) ---
@csrf_exempt
@require_POST
def agregar_insumo_ajax(request):
    form = InsumoForm(request.POST, request.FILES)
    if form.is_valid():
        insumo = form.save()
        return JsonResponse({
            'success': True, 
            'insumo': {
                'id': insumo.id,
                'descripcion': insumo.descripcion,
                'categoria_nombre': insumo.categoria.nombre if insumo.categoria else "Sin categoría",
                'fabricante': insumo.fabricante,
                'precio_unitario': str(insumo.precio_unitario),
                'stock': insumo.stock,
                'imagen_url': insumo.imagen.url if insumo.imagen else None,
            },
            'categoria_id_actual': insumo.categoria_id # Para saber qué tabla actualizar
        })
    return JsonResponse({'success': False, 'errors': form.errors})



@require_GET
def get_insumo_data(request): # Para poblar el modal de edición de insumo
    insumo_id = request.GET.get('id')
    try:
        insumo = Insumo.objects.get(id=insumo_id)
        data = {
            'id': insumo.id,
            'descripcion': insumo.descripcion,
            'categoria': insumo.categoria_id if insumo.categoria else '',
            'fabricante': insumo.fabricante,
            'precio_unitario': str(insumo.precio_unitario),
            'tiempo_entrega': insumo.tiempo_entrega,
            'imagen_url': insumo.imagen.url if insumo.imagen else '',
            'proveedor': insumo.proveedor,
            'stock': insumo.stock,
        }
        return JsonResponse({'success': True, 'insumo': data})
    except Insumo.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Insumo no encontrado'}, status=404)


@csrf_exempt
@require_POST
def editar_insumo_ajax(request):
    insumo_id = request.POST.get('id')
    try:
        insumo = Insumo.objects.get(id=insumo_id)
        form = InsumoForm(request.POST, request.FILES, instance=insumo)
        if form.is_valid():
            insumo = form.save()
            return JsonResponse({
                'success': True,
                'insumo': {
                    'id': insumo.id,
                    'descripcion': insumo.descripcion,
                    'categoria_nombre': insumo.categoria.nombre if insumo.categoria else "Sin categoría",
                    'fabricante': insumo.fabricante,
                    'precio_unitario': str(insumo.precio_unitario),
                    'stock': insumo.stock,
                    'imagen_url': insumo.imagen.url if insumo.imagen else None,
                },
                'categoria_id_actual': insumo.categoria_id
            })
        return JsonResponse({'success': False, 'errors': form.errors})
    except Insumo.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Insumo no encontrado'}, status=404)



# --- CRUDs AJAX para ProductoTerminado (ya existentes, pueden requerir pequeños ajustes) ---
@csrf_exempt
@require_POST
def agregar_producto_ajax(request):
    form = ProductoTerminadoForm(request.POST, request.FILES)
    if form.is_valid():
        producto = form.save()
        return JsonResponse({
            'success': True,
            'producto': {
                'id': producto.id,
                'descripcion': producto.descripcion,
                'categoria_nombre': producto.categoria.nombre if producto.categoria else "Sin categoría",
                'precio_unitario': str(producto.precio_unitario),
                'stock': producto.stock,
                'imagen_url': producto.imagen.url if producto.imagen else None, # Si tiene imagen
            },
            'categoria_id_actual': producto.categoria_id
        })
    return JsonResponse({'success': False, 'errors': form.errors})

@require_GET
def get_producto_terminado_data(request): # Para poblar el modal de edición
    producto_id = request.GET.get('id')
    try:
        producto = ProductoTerminado.objects.get(id=producto_id)
        data = {
            'id': producto.id,
            'descripcion': producto.descripcion,
            'categoria': producto.categoria_id if producto.categoria else '',
            'precio_unitario': str(producto.precio_unitario),
            'stock': producto.stock,
            'imagen_url': producto.imagen.url if producto.imagen else '', # Si tiene imagen
        }
        return JsonResponse({'success': True, 'producto': data})
    except ProductoTerminado.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Producto no encontrado'}, status=404)



@csrf_exempt
@require_POST
def editar_producto_terminado_ajax(request):
    producto_id = request.POST.get('id')
    try:
        producto = ProductoTerminado.objects.get(id=producto_id)
        form = ProductoTerminadoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            producto = form.save()
            return JsonResponse({
                'success': True,
                'producto': {
                    'id': producto.id,
                    'descripcion': producto.descripcion,
                    'categoria_nombre': producto.categoria.nombre if producto.categoria else "Sin categoría",
                    'precio_unitario': str(producto.precio_unitario),
                    'stock': producto.stock,
                    'imagen_url': producto.imagen.url if producto.imagen else None,
                },
                'categoria_id_actual': producto.categoria_id
            })
        return JsonResponse({'success': False, 'errors': form.errors})
    except ProductoTerminado.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Producto no encontrado'}, status=404)


# --- Vista AJAX unificada para eliminar artículos ---
@csrf_exempt
@require_POST
def eliminar_articulo_ajax(request):
    item_id = request.POST.get('id')
    item_type = request.POST.get('item_type') # 'insumo' o 'producto'

    if not item_id or not item_type:
        return JsonResponse({'success': False, 'error': 'ID y tipo de ítem son requeridos.'}, status=400)

    try:
        if item_type == 'insumo':
            item = get_object_or_404(Insumo, id=item_id)
        elif item_type == 'producto':
            item = get_object_or_404(ProductoTerminado, id=item_id)
        else:
            return JsonResponse({'success': False, 'error': 'Tipo de ítem inválido.'}, status=400)
        
        item.delete()
        return JsonResponse({'success': True, 'item_id': item_id, 'item_type': item_type})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@login_required
@require_POST
@csrf_exempt # Considera csrf_protect y enviar token con JS
def crear_rol_ajax(request):
    form = RolForm(request.POST)
    if form.is_valid():
        nombre_rol = form.cleaned_data['nombre']
        descripcion_rol = form.cleaned_data['descripcion']
        try:
            with transaction.atomic(): # Para asegurar que ambas creaciones ocurran o ninguna
                nuevo_grupo = Group.objects.create(name=nombre_rol)
                if descripcion_rol:
                    RolDescripcion.objects.create(group=nuevo_grupo, descripcion=descripcion_rol)
                
                return JsonResponse({
                    'success': True,
                    'rol': {
                        'id': nuevo_grupo.id,
                        'nombre': nuevo_grupo.name,
                        'descripcion': descripcion_rol
                    }
                })
        except Exception as e:
            return JsonResponse({'success': False, 'errors': {'__all__': [str(e)]}})
    else:
        return JsonResponse({'success': False, 'errors': form.errors})

@login_required
@require_GET
def get_rol_data_ajax(request):
    rol_id = request.GET.get('rol_id')
    try:
        grupo = Group.objects.get(id=rol_id)
        descripcion_extendida = ""
        if hasattr(grupo, 'descripcion_extendida') and grupo.descripcion_extendida:
            descripcion_extendida = grupo.descripcion_extendida.descripcion
        
        return JsonResponse({
            'success': True,
            'rol': {
                'id': grupo.id,
                'nombre': grupo.name,
                'descripcion': descripcion_extendida
            }
        })
    except Group.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Rol no encontrado.'}, status=404)

@login_required
@require_POST
@csrf_exempt # Considera csrf_protect
def editar_rol_ajax(request):
    rol_id = request.POST.get('rol_id') # rol_id viene del form
    try:
        grupo_a_editar = Group.objects.get(id=rol_id)
    except Group.DoesNotExist:
        return JsonResponse({'success': False, 'errors': {'__all__': ['Rol no encontrado.']}}, status=404)

    form = RolForm(request.POST, initial={'rol_id': rol_id}) # Pasar rol_id para validación de unicidad
    
    if form.is_valid():
        nombre_rol = form.cleaned_data['nombre']
        descripcion_rol = form.cleaned_data['descripcion']
        try:
            with transaction.atomic():
                grupo_a_editar.name = nombre_rol
                grupo_a_editar.save()

                desc_obj, created = RolDescripcion.objects.get_or_create(group=grupo_a_editar)
                desc_obj.descripcion = descripcion_rol
                desc_obj.save()
            
            return JsonResponse({
                'success': True,
                'rol': {
                    'id': grupo_a_editar.id,
                    'nombre': grupo_a_editar.name,
                    'descripcion': descripcion_rol
                }
            })
        except Exception as e:
            return JsonResponse({'success': False, 'errors': {'__all__': [str(e)]}})
    else:
        return JsonResponse({'success': False, 'errors': form.errors})


@login_required
@require_POST # Debería ser POST para una acción de eliminación
@csrf_exempt # Considera csrf_protect
def eliminar_rol_ajax(request):
    import json # Para parsear el body si es JSON
    try:
        data = json.loads(request.body)
        rol_id = data.get('rol_id')
        grupo = Group.objects.get(id=rol_id)
        
        # Opcional: Verificar si hay usuarios en este grupo antes de eliminar
        if grupo.user_set.exists():
            return JsonResponse({'success': False, 'error': 'No se puede eliminar el rol porque tiene usuarios asignados.'}, status=400)
            
        grupo.delete() # RolDescripcion se borrará en cascada
        return JsonResponse({'success': True})
    except Group.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Rol no encontrado.'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'JSON inválido.'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@login_required
@require_GET
def get_permisos_rol_ajax(request):
    rol_id = request.GET.get('rol_id')
    try:
        rol = Group.objects.get(id=rol_id)
        permisos_del_rol_ids = list(rol.permissions.values_list('id', flat=True))
        
        todos_los_permisos = Permission.objects.select_related('content_type').all()
        permisos_data = []
        for perm in todos_los_permisos:
            permisos_data.append({
                'id': perm.id,
                'name': perm.name, # Nombre legible
                'codename': perm.codename, # Codename (ej. add_user)
                'content_type_app_label': perm.content_type.app_label, # Nombre de la app (ej. auth, App_Luminova)
                'content_type_model': perm.content_type.model # Nombre del modelo (ej. user, insumo)
            })
            
        return JsonResponse({
            'success': True,
            'todos_los_permisos': permisos_data,
            'permisos_del_rol': permisos_del_rol_ids
        })
    except Group.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Rol no encontrado.'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@login_required
@require_POST
@csrf_exempt # Considera csrf_protect
def actualizar_permisos_rol_ajax(request):
    import json
    try:
        data = json.loads(request.body)
        rol_id = data.get('rol_id')
        permisos_ids_str = data.get('permisos_ids', []) # Lista de IDs como strings
        permisos_ids = [int(pid) for pid in permisos_ids_str]


        rol = Group.objects.get(id=rol_id)
        
        # Actualizar permisos
        rol.permissions.set(permisos_ids) # set() maneja agregar y quitar
        
        return JsonResponse({'success': True, 'message': 'Permisos actualizados.'})
    except Group.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Rol no encontrado.'}, status=404)
    except Permission.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Uno o más permisos no son válidos.'}, status=400)
    except ValueError:
        return JsonResponse({'success': False, 'error': 'IDs de permisos inválidos.'}, status=400)
    except json.JSONDecodeError:
         return JsonResponse({'success': False, 'error': 'Datos JSON inválidos.'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


# --- Rutas y vistas para botones de sidebar de Compras y Producción (mantener si ya existen) ---
def desglose(req):
    return render(req, "compras/desglose.html")

def seguimiento(req):
    return render(req, "compras/seguimiento.html")

def tracking(req):
    return render(req, "compras/tracking.html")

def desglose2(req):
    return render(req, "compras/desglose2.html")

def ordenes(req):
    return render(req, "produccion/ordenes.html")

def planificacion(req):
    return render(req, "produccion/planificacion.html")

def reportes(req):
    return render(req, "produccion/reportes.html")
