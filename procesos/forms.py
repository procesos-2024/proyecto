from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Venta, VentaDetalle, Proveedor, ArticuloUnidades
from django import forms
from .models import Proveedor, ArticuloUnidades, Orden

from django import forms


class CorteFechaForm(forms.Form):
    fecha = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))


class OrdenForm(forms.ModelForm):
    class Meta:
        model = Orden
        fields = ['proveedor']
        widgets = {
            'proveedor': forms.Select(attrs={'class': 'form-control'}),
        }


class ArticuloUnidadesForm(forms.ModelForm):
    class Meta:
        model = ArticuloUnidades
        fields = ['articulo', 'unidades']
        widgets = {
            'articulo': forms.Select(attrs={'class': 'form-control'}),
            'unidades': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }


class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = [
            'nombre',
            'email',
            'activo'
        ]


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password1',
            'password2'
        ]


class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['pagado']


class VentaDetalleForm(forms.ModelForm):
    class Meta:
        model = VentaDetalle
        fields = ['articulo', 'cantidad']
