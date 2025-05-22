# App_LUMINOVA/forms.py
from django import forms
from .models import Insumo, ProductoTerminado, CategoriaInsumo, CategoriaProductoTerminado # Importar nuevos modelos

# NUEVO: Formulario para CategoriaInsumo
class CategoriaInsumoForm(forms.ModelForm):
    class Meta:
        model = CategoriaInsumo
        fields = ['nombre', 'imagen']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

# NUEVO: Formulario para CategoriaProductoTerminado
class CategoriaProductoTerminadoForm(forms.ModelForm):
    class Meta:
        model = CategoriaProductoTerminado
        fields = ['nombre', 'imagen']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class InsumoForm(forms.ModelForm):
    class Meta:
        model = Insumo
        fields = '__all__'
        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}), # Ya estaba como Select, correcto
            'fabricante': forms.TextInput(attrs={'class': 'form-control'}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'tiempo_entrega': forms.NumberInput(attrs={'class': 'form-control'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'proveedor': forms.TextInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class ProductoTerminadoForm(forms.ModelForm):
    class Meta:
        model = ProductoTerminado
        fields = '__all__' # Incluye 'descripcion', 'categoria', 'precio_unitario', 'stock', 'imagen'
        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}), # CAMBIO: Ahora es Select
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}), # Si añadiste imagen al modelo
        }