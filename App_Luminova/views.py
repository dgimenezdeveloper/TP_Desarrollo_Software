# App_LUMINOVA/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.decorators import user_passes_test, login_required

# ¡IMPORTANTE!: Asegúrate de que esta línea contenga EXACTAMENTE los modelos que DEFINES en models.py
# Si alguno de estos no está en tu models.py, ELIMÍNALO de esta lista.
from .models import (
    Insumo, ProductoTerminado, CategoriaInsumo, # Asegúrate de que estos existen y estén definidos correctamente
    AuditoriaAcceso, # Asegúrate de que AuditoriaAcceso está definido en models.py, si no, ELIMÍNALO
    Orden, Proveedor, Cliente, Factura, RolDescripcion # Asegúrate de que estos existen en models.py
)

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from django.db.models import Count
from .forms import InsumoForm, ProductoTerminadoForm

# Crea tus vistas aquí.

def compras(req):
    return render(req, "compras.html")

def produccion(req):
    return render(req, "produccion.html")

def ventas(req):
    return render(req, "ventas.html")

def deposito(req):
    categorias_insumos_objetos = CategoriaInsumo.objects.all().order_by('nombre')
    categorias_productos_terminados = ProductoTerminado.objects.values_list('categoria', flat=True).distinct().order_by('categoria')

    form_agregar_insumo = InsumoForm()
    form_agregar_producto = ProductoTerminadoForm()

    context = {
        "categorias_insumos": categorias_insumos_objetos,
        "categorias_productos_terminados": categorias_productos_terminados,
        "form_agregar_insumo": form_agregar_insumo,
        "form_agregar_producto": form_agregar_producto,
    }
    return render(req, "deposito.html", context)

def control_calidad(req):
    return render(req, "control_calidad.html")

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

def roles_permisos(request):
    roles = []
    context = {'roles': roles}
    return render(request, 'roles_permisos.html', context)

def auditoria(request):
    # Asegúrate de que AuditoriaAcceso exista y se importe correctamente
    # Si no quieres usar este modelo, puedes eliminar esta vista y las referencias a ella.
    auditorias = AuditoriaAcceso.objects.all().order_by('-fecha_acceso') # Ejemplo de cómo usarlo
    context = {'auditorias': auditorias}
    return render(request, 'auditoria.html', context)

# CRUD de usuario
def lista_usuarios(request):
    usuarios = User.objects.all()
    return render(request, 'usuarios.html', {'usuarios': usuarios})

def crear_usuario(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_usuarios')
    else:
        form = UserCreationForm()
    return render(request, 'crear_usuario.html', {'form': form})

def editar_usuario(request, id):
    usuario = get_object_or_404(User, id=id)
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('lista_usuarios')
    else:
        form = UserChangeForm(instance=usuario)
    return render(request, 'editar_usuario.html', {'form': form})

def eliminar_usuario(request, id):
    usuario = get_object_or_404(User, id=id)
    usuario.delete()
    return redirect('lista_usuarios')

def depo_seleccion(request):
    return render(request, "depo-seleccion.html")

def depo_enviar(request):
    return render(request, "depo-enviar.html")

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

@require_GET
def get_insumos_por_categoria(request):
    categoria_nombre = request.GET.get('categoria', '')
    
    insumos_query = Insumo.objects.all()
    if categoria_nombre:
        insumos_query = insumos_query.filter(categoria__nombre=categoria_nombre)
    
    insumos_data = []
    for insumo in insumos_query:
        insumos_data.append({
            'id': insumo.id,
            'descripcion': insumo.descripcion,
            'categoria': insumo.categoria.nombre if insumo.categoria else None,
            'fabricante': insumo.fabricante,
            'precio_unitario': str(insumo.precio_unitario),
            'tiempo_entrega': insumo.tiempo_entrega,
            'imagen_url': insumo.imagen.url if insumo.imagen else '',
            'proveedor': insumo.proveedor,
            'stock': insumo.stock,
        })
    return JsonResponse({'success': True, 'insumos': insumos_data})

@require_GET
def get_insumo_data(request):
    insumo_id = request.GET.get('id')
    try:
        insumo = Insumo.objects.get(id=insumo_id)
        data = {
            'id': insumo.id,
            'descripcion': insumo.descripcion,
            'categoria': insumo.categoria.nombre if insumo.categoria else None,
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
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    except Insumo.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Insumo no encontrado'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


# Vistas AJAX para Productos Terminados (se mantienen como CharField por ahora)
@csrf_exempt
@require_POST
def agregar_producto_ajax(request):
    if request.method == 'POST':
        form = ProductoTerminadoForm(request.POST, request.FILES) 
        if form.is_valid():
            producto = form.save()
            return JsonResponse({'success': True, 'producto_id': producto.id})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False, 'error': 'Método de petición inválido.'}, status=400)

@require_GET
def get_productos_terminados(request):
    categoria = request.GET.get('categoria', '')
    if categoria:
        productos = ProductoTerminado.objects.filter(categoria=categoria)
    else:
        productos = ProductoTerminado.objects.all()
    
    productos_data = [{
        'id': producto.id,
        'descripcion': producto.descripcion,
        'categoria': producto.categoria, # Se mantiene como CharField
        'precio_unitario': str(producto.precio_unitario),
        'stock': producto.stock,
    } for producto in productos]
    return JsonResponse({'success': True, 'productos': productos_data})

@require_GET
def get_producto_terminado_data(request):
    producto_id = request.GET.get('id')
    try:
        producto = ProductoTerminado.objects.get(id=producto_id)
        data = {
            'id': producto.id,
            'descripcion': producto.descripcion,
            'categoria': producto.categoria, # Se mantiene como CharField
            'precio_unitario': str(producto.precio_unitario),
            'stock': producto.stock,
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
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    except ProductoTerminado.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Producto no encontrado'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@csrf_exempt
@require_POST
def eliminar_articulo_ajax(request):
    if request.method == 'POST':
        item_id = request.POST.get('id')
        model_type = request.POST.get('model_type')

        if not item_id or not model_type:
            return JsonResponse({'success': False, 'error': 'ID y tipo de modelo son requeridos.'}, status=400)

        try:
            if model_type == 'insumo':
                item = Insumo.objects.get(id=item_id)
            elif model_type == 'producto':
                item = ProductoTerminado.objects.get(id=item_id)
            else:
                return JsonResponse({'success': False, 'error': 'Tipo de modelo inválido.'}, status=400)
            
            item.delete()
            return JsonResponse({'success': True})
        except (Insumo.DoesNotExist, ProductoTerminado.DoesNotExist):
            return JsonResponse({'success': False, 'error': 'Artículo no encontrado.'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'success': False, 'error': 'Método de petición inválido.'}, status=400)


def desglose(req):
    return render(req, "desglose.html")

def seguimiento(req):
    return render(req, "seguimiento.html")

def tracking(req):
    return render(req, "tracking.html")

def desglose2(req):
    return render(req, "desglose2.html")

def ordenes(req):
    return render(req, "ordenes.html")

def planificacion(req):
    return render(req, "planificacion.html")

def reportes(req):
    return render(req, "reportes.html")