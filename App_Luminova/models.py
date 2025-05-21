# App_LUMINOVA/models.py
from django.db import models
from django.contrib.auth.models import User, Group # Asegúrate de importar Group si lo usas

class ProductoTerminado(models.Model):
    descripcion = models.CharField(max_length=100)
    categoria = models.CharField(max_length=50) # Assuming this is still a CharField for now, as per your forms.py
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()

    def __str__(self):
        return self.descripcion

# Definición del modelo CategoriaInsumo
class CategoriaInsumo(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    # Puedes añadir un campo para la imagen de la categoría si lo deseas
    # imagen = models.ImageField(upload_to='categorias_insumos/', null=True, blank=True)

    class Meta:
        verbose_name = "Categoría de Insumo"
        verbose_name_plural = "Categorías de Insumos"

    def __str__(self):
        return self.nombre

class Insumo(models.Model):
    descripcion = models.CharField(max_length=100)
    # ¡IMPORTANTE!: Esto DEBE ser ForeignKey
    categoria = models.ForeignKey(CategoriaInsumo, on_delete=models.SET_NULL, null=True, blank=True) # <-- ¡CORRECCIÓN CRÍTICA!
    fabricante = models.CharField(max_length=60)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    tiempo_entrega = models.IntegerField() # Tiempo de entrega en días
    imagen = models.ImageField(null=True, blank=True)
    proveedor = models.CharField(max_length=60)
    stock = models.IntegerField()

    def __str__(self):
        # Asegúrate de que insumo.categoria sea un objeto antes de acceder a .nombre
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
    # Puedes añadir un ForeignKey a Insumo o ProductoTerminado si una orden es para un solo tipo
    # O un ManyToManyField si una orden puede contener múltiples items
    # items = models.ManyToManyField(Insumo, through='OrdenInsumo') # Ejemplo
    # items_productos = models.ManyToManyField(ProductoTerminado, through='OrdenProducto') # Ejemplo

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
    fecha_acceso = models.DateTimeField(auto_now_add=True)
    accion = models.CharField(max_length=255) # Ejemplo: 'login', 'logout', 'acceso_deposito'

    class Meta:
        verbose_name = "Auditoría de Acceso"
        verbose_name_plural = "Auditorías de Acceso"
        ordering = ['-fecha_acceso']

    def __str__(self):
        return f"[{self.fecha_acceso.strftime('%Y-%m-%d %H:%M:%S')}] {self.usuario} - {self.accion}"