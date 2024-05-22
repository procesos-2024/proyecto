from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.forms import inlineformset_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView, TemplateView, CreateView, DetailView

from .forms import UserRegisterForm, VentaForm, VentaDetalleForm, ProveedorForm, OrdenForm, ArticuloUnidadesForm, \
    CorteFechaForm
from .models import Venta, Proveedor, Orden, ArticuloUnidades, VentaDetalle


@login_required
def index(request):
    return render(request, 'index.html')


class CalcularCorteView(LoginRequiredMixin, FormView):
    template_name = 'calcular_corte.html'
    form_class = CorteFechaForm
    success_url = reverse_lazy('corte_calculado')

    def form_valid(self, form):
        fecha = form.cleaned_data['fecha']
        ventas = Venta.objects.filter(fecha__date=fecha, pagado=True)
        total_ventas = ventas.aggregate(total=Sum('total'))['total'] or 0.00

        context = self.get_context_data(form=form)
        context['ventas'] = ventas
        context['total_ventas'] = total_ventas
        return self.render_to_response(context)


class OrdenCreadaView(LoginRequiredMixin, TemplateView):
    template_name = 'orden_creada.html'


class CrearOrdenView(LoginRequiredMixin, FormView):
    template_name = 'crear_orden.html'
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


class ProveedorListView(LoginRequiredMixin, ListView):
    model = Proveedor
    template_name = 'lista_proveedores.html'
    context_object_name = 'proveedores'


class RegisterProveedor(LoginRequiredMixin, FormView):
    template_name = 'register_proveedor.html'
    success_url = reverse_lazy('index')
    form_class = ProveedorForm

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class RegisterView(LoginRequiredMixin, FormView):
    template_name = 'register.html'
    form_class = UserRegisterForm

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class CrearVentaView(LoginRequiredMixin, CreateView):
    model = Venta
    form_class = VentaForm
    template_name = 'crear_venta.html'

    def form_valid(self, form):
        form.instance.vendedor = self.request.user
        self.object = form.save()
        return redirect('agregar_articulo_a_venta', venta_id=self.object.id)


class AgregarArticuloAVentaView(LoginRequiredMixin, CreateView):
    model = VentaDetalle
    form_class = VentaDetalleForm
    template_name = 'agregar_articulo_a_venta.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['venta'] = get_object_or_404(Venta, id=self.kwargs['venta_id'])
        return context

    def form_valid(self, form):
        venta = get_object_or_404(Venta, id=self.kwargs['venta_id'])
        form.instance.venta = venta
        self.object = form.save()
        return redirect('ver_venta', venta_id=venta.id)


class VerVentaView(LoginRequiredMixin, DetailView):
    model = Venta
    template_name = 'ver_venta.html'
    context_object_name = 'venta'

    def get_object(self):
        return get_object_or_404(Venta, id=self.kwargs['venta_id'])
