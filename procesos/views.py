from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import FormView

from .forms import UserRegisterForm, VentaForm, VentaDetalleForm
from .models import Venta


class RegisterView(FormView):
    template_name = 'register.html'
    form_class = UserRegisterForm

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

@login_required
def crear_venta(request):
    if request.method == 'POST':
        form = VentaForm(request.POST)
        if form.is_valid():
            venta = form.save(commit=False)
            venta.vendedor = request.user
            venta.save()
            return redirect('agregar_articulo_a_venta', venta_id=venta.id)
    else:
        form = VentaForm()
    return render(request, 'crear_venta.html', {'form': form})

@login_required
def agregar_articulo_a_venta(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    if request.method == 'POST':
        form = VentaDetalleForm(request.POST)
        if form.is_valid():
            detalle = form.save(commit=False)
            detalle.venta = venta
            detalle.save()
            return redirect('ver_venta', venta_id=venta.id)
    else:
        form = VentaDetalleForm()
    return render(request, 'agregar_articulo_a_venta.html', {'venta': venta, 'form': form})

@login_required
def ver_venta(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    return render(request, 'ver_venta.html', {'venta': venta})