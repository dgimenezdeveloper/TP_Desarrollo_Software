# App_LUMINOVA/forms.py
from django import forms
from .models import Insumo, ProductoTerminado, CategoriaInsumo # ¡Importa CategoriaInsumo aquí!


class InsumoForm(forms.ModelForm):
    class Meta:
        model = Insumo
        fields = '__all__'
        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}), # <-- ¡CORRECCIÓN CLAVE AQUÍ!
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
        fields = '__all__'
        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.TextInput(attrs={'class': 'form-control'}), # Se mantiene como CharField en ProductoTerminado
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
        }