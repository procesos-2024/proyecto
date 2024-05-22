from django.contrib.auth.decorators import login_required
from django.forms import formset_factory, inlineformset_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView

from .forms import UserRegisterForm, VentaForm, VentaDetalleForm, ProveedorForm, OrdenForm, ArticuloUnidadesForm
from .models import Venta, Proveedor, Orden, ArticuloUnidades


def index(request):
    return render(request, 'index.html')


class CrearOrdenView(FormView):
    template_name = 'ordenes/crear_orden.html'
    form_class = OrdenForm
    success_url = reverse_lazy('orden_creada')  # Puedes definir una vista o URL para mostrar una confirmación

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['articulos_formset'] = ArticuloUnidadesFormSet(self.request.POST)
        else:
            data['articulos_formset'] = ArticuloUnidadesFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        articulos_formset = context['articulos_formset']
        if articulos_formset.is_valid():
            orden = form.save(commit=False)
            orden.emisor = self.request.user
            orden.descripcion = 'Nueva orden generada automáticamente'
            orden.save()

            articulos_formset.instance = orden
            articulos_formset.save()

            return super().form_valid(form)
        else:
            return self.form_invalid(form)

ArticuloUnidadesFormSet = inlineformset_factory(Orden, ArticuloUnidades, form=ArticuloUnidadesForm, extra=1)


class ProveedorListView(ListView):
    model = Proveedor
    template_name = 'lista_proveedores.html'
    context_object_name = 'proveedores'


class RegisterProveedor(FormView):
    template_name = 'register_proveedor.html'
    success_url = reverse_lazy('index')
    form_class = ProveedorForm

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


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

    return render(
        request,
        'agregar_articulo_a_venta.html',
        {'venta': venta, 'form': form}
    )


@login_required
def ver_venta(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    return render(
        request,
        'ver_venta.html',
        {'venta': venta}
    )
