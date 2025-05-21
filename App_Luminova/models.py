from django.db import models
from django.contrib.auth.models import User

class ProductoTerminado(models.Model):
    descripcion = models.CharField(max_length=100)
    categoria = models.CharField(max_length=50)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()

    def __str__(self):
        return self.descripcion

class Insumo(models.Model):
    descripcion = models.CharField(max_length=100)
    categoria = models.CharField(max_length=50)
    fabricante = models.CharField(max_length=60)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    tiempo_entrega = models.IntegerField()  # Tiempo de entrega en días
    imagen = models.ImageField(null=True, blank=True, upload_to='insumos' )
    proveedor = models.CharField(max_length=60)
    stock = models.IntegerField()

    def __str__(self):
        return f"{self.descripcion}"

class Orden(models.Model):
    TIPO_ORDEN_CHOICES = [
        ('produccion', 'Orden de Producción'),
        ('compra', 'Orden de Compra'),
        ('venta', 'Orden de Venta'),
    ]

    numero_orden = models.CharField(max_length=20)
    fecha = models.DateField()
    tipo_orden = models.CharField(max_length=10, choices=TIPO_ORDEN_CHOICES)
    estado = models.CharField(max_length=20, default='Pendiente')

    def __str__(self):
        return self.numero_orden

class DetalleOrden(models.Model):
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE)
    insumo = models.ForeignKey(Insumo, on_delete=models.CASCADE, null=True, blank=True)
    producto_terminado = models.ForeignKey(ProductoTerminado, on_delete=models.CASCADE, null=True, blank=True)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        if self.insumo:
            return f"Detalle de Orden {self.orden.numero_orden}: {self.insumo.descripcion} x {self.cantidad}"
        elif self.producto_terminado:
            return f"Detalle de Orden {self.orden.numero_orden}: {self.producto_terminado.descripcion} x {self.cantidad}"
        return f"Detalle de Orden {self.orden.numero_orden}"

class AuditoriaAcceso(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_acceso = models.DateTimeField(auto_now_add=True)
    accion = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.usuario.username} - {self.fecha_acceso} - {self.accion}'

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.TextField()
    telefono = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return self.nombre

class Factura(models.Model):
    numero_factura = models.CharField(max_length=20)
    fecha = models.DateField()
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.numero_factura

from django.contrib.auth.models import Group

class RolDescripcion(models.Model):
    group = models.OneToOneField(Group, on_delete=models.CASCADE, related_name='descripcion_extendida')
    descripcion = models.TextField("Descripción del rol", blank=True)

    def __str__(self):
        return self.group.name