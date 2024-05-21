from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Venta, VentaDetalle


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password1',
            'password2',
            'is_staff'
        ]


class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['pagado']


class VentaDetalleForm(forms.ModelForm):
    class Meta:
        model = VentaDetalle
        fields = ['articulo', 'cantidad', 'precio_unitario']
