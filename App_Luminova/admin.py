# App_LUMINOVA/admin.py

from django.contrib import admin
from .models import (
    Insumo,
    ProductoTerminado,
    Orden,
    AuditoriaAcceso,
    Cliente,
    Factura,
    RolDescripcion,
    CategoriaInsumo,
    CategoriaProductoTerminado, # AÑADIDO
    Proveedor
)

admin.site.register(Insumo)
admin.site.register(ProductoTerminado)
admin.site.register(Orden)
admin.site.register(AuditoriaAcceso)
admin.site.register(Cliente)
admin.site.register(Factura)
admin.site.register(RolDescripcion)
admin.site.register(CategoriaInsumo)
admin.site.register(CategoriaProductoTerminado) # AÑADIDO
admin.site.register(Proveedor)

# ... (tus personalizaciones de ModelAdmin pueden seguir aquí)


# Opcional: Aquí puedes agregar clases de ModelAdmin para personalizar la visualización
# en el panel de administración, como se mencionó en respuestas anteriores.
# Por ejemplo:
# class InsumoAdmin(admin.ModelAdmin):
#     list_display = ('descripcion', 'categoria', 'stock', 'precio_unitario', 'proveedor')
#     search_fields = ('descripcion', 'categoria', 'proveedor')
#     list_filter = ('categoria', 'proveedor')
# admin.site.register(Insumo, InsumoAdmin)

# class ProductoTerminadoAdmin(admin.ModelAdmin):
#     list_display = ('descripcion', 'categoria', 'stock', 'precio_unitario')
#     search_fields = ('descripcion', 'categoria')
#     list_filter = ('categoria',)
# admin.site.register(ProductoTerminado, ProductoTerminadoAdmin)