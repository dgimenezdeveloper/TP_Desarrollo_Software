# App_LUMINOVA/models.py
from django.db import models
from django.contrib.auth.models import User, Group

# NUEVO: Modelo CategoriaProductoTerminado
class CategoriaProductoTerminado(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    imagen = models.ImageField(upload_to='categorias_productos/', null=True, blank=True)

    class Meta:
        verbose_name = "Categoría de Producto Terminado"
        verbose_name_plural = "Categorías de Productos Terminados"

    def __str__(self):
        return self.nombre

class ProductoTerminado(models.Model):
    descripcion = models.CharField(max_length=100)
    # CAMBIO: ForeignKey a CategoriaProductoTerminado
    categoria = models.ForeignKey(CategoriaProductoTerminado, on_delete=models.SET_NULL, null=True, blank=True)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    # OPCIONAL: Si quieres imagen para ProductoTerminado
    imagen = models.ImageField(upload_to='productos_terminados/', null=True, blank=True)


    def __str__(self):
        return f"{self.descripcion} ({self.categoria.nombre if self.categoria else 'Sin Categoría'})"

class CategoriaInsumo(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    # AÑADIDO: Campo de imagen
    imagen = models.ImageField(upload_to='categorias_insumos/', null=True, blank=True)

    class Meta:
        verbose_name = "Categoría de Insumo"
        verbose_name_plural = "Categorías de Insumos"

    def __str__(self):
        return self.nombre

class Insumo(models.Model):
    descripcion = models.CharField(max_length=100)
    categoria = models.ForeignKey(CategoriaInsumo, on_delete=models.SET_NULL, null=True, blank=True)
    fabricante = models.CharField(max_length=60)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    tiempo_entrega = models.IntegerField() # Tiempo de entrega en días
    imagen = models.ImageField(upload_to='insumos/', null=True, blank=True) # Modificada ruta de upload
    proveedor = models.CharField(max_length=60)
    stock = models.IntegerField()

    def __str__(self):
        return f"{self.descripcion} ({self.categoria.nombre if self.categoria else 'Sin Categoría'})"

class Orden(models.Model):
    TIPO_ORDEN_CHOICES = [
        ('produccion', 'Orden de Producción'),
        ('compra', 'Orden de Compra'),
        ('venta', 'Orden de Venta'),
    ]
    numero_orden = models.CharField(max_length=20, unique=True)
    tipo_orden = models.CharField(max_length=10, choices=TIPO_ORDEN_CHOICES)
    fecha_creacion = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.numero_orden

class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    contacto = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return self.nombre

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.TextField()
    telefono = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return self.nombre

class Factura(models.Model):
    numero_factura = models.CharField(max_length=20, unique=True)
    fecha = models.DateField()
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.numero_factura

class RolDescripcion(models.Model):
    group = models.OneToOneField(Group, on_delete=models.CASCADE, related_name='descripcion_extendida')
    descripcion = models.TextField("Descripción del rol", blank=True)

    def __str__(self):
        return f"Descripción para {self.group.name}"

class AuditoriaAcceso(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    fecha_acceso = models.DateTimeField(auto_now_add=True) # CORRECTO
    accion = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Auditoría de Acceso"
        verbose_name_plural = "Auditorías de Acceso"
        ordering = ['-fecha_acceso']

    def __str__(self):
        return f"[{self.fecha_acceso.strftime('%Y-%m-%d %H:%M:%S')}] {self.usuario} - {self.accion}"