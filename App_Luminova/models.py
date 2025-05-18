from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    imagen = models.ImageField(upload_to='productos/')


# Creacion del modelo RolDescripcion
from django.db import models
from django.contrib.auth.models import Group

class RolDescripcion(models.Model):
    group = models.OneToOneField(Group, on_delete=models.CASCADE, related_name='descripcion_extendida')
    descripcion = models.TextField("Descripción del rol", blank=True)

    def __str__(self):
        return f"{self.group.name}"

# Creacion del modelo AuditoriaAcceso
class AuditoriaAcceso(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    accion = models.CharField(max_length=100)
    fecha_hora = models.DateTimeField(auto_now_add=True)