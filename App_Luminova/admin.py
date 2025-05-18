from django.contrib import admin

# Register your models here.



# Registro del modelo RolDescripcion en el admin de Django
from django.contrib import admin
from .models import RolDescripcion

admin.site.register(RolDescripcion)