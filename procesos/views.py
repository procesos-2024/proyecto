from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, F
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.timezone import now
from django.views import View
from django.views.generic import FormView, CreateView

from .forms import UserRegisterForm, VentaDetalleForm, ProveedorForm, CorteFechaForm
from .models import Venta, VentaDetalle


@login_required
def index(request):
    return render(request, 'menu/index.html')


class EliminarArticuloDeVentaView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        venta_detalle_id = kwargs['pk']
        venta_detalle = get_object_or_404(VentaDetalle, id=venta_detalle_id)
        venta = venta_detalle.venta
        venta.total -= venta_detalle.subtotal
        venta.save()
        venta_detalle.delete()
        return redirect('agregar_articulo_a_venta')


class CalcularCorteView(LoginRequiredMixin, FormView):
    template_name = 'calcular_corte.html'
    form_class = CorteFechaForm
    success_url = reverse_lazy('corte_calculado')

    def get_initial(self):
        initial = super().get_initial()
        fecha_param = self.request.GET.get('fecha')
        if fecha_param:
            initial['fecha'] = fecha_param
        else:
            initial['fecha'] = now().date()  # Establece la fecha actual como predeterminada
        return initial

    def form_valid(self, form):
        fecha = form.cleaned_data['fecha']
        ventas = Venta.objects.filter(fecha__date=fecha, pagado=True)
        total_ventas = ventas.aggregate(total=Sum('total'))['total'] or 0.00

        context = self.get_context_data(form=form)
        context['ventas'] = ventas
        context['total_ventas'] = total_ventas
        return self.render_to_response(context)


from django.views.generic import ListView
from .models import Proveedor, Articulo


class ProveedorListView(LoginRequiredMixin, ListView):
    model = Proveedor
    template_name = 'lista_proveedores.html'
    context_object_name = 'proveedores'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        proveedores = context['proveedores']
        proveedores_info = []

        for proveedor in proveedores:
            bajo_stock = Articulo.objects.filter(proveedor=proveedor, unidades__lte=F('minimo')).exists()
            proveedores_info.append({
                'proveedor': proveedor,
                'bajo_stock': bajo_stock
            })

        context['proveedores_info'] = proveedores_info
        return context


class RegisterProveedor(LoginRequiredMixin, FormView):
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


class AgregarArticuloAVentaView(LoginRequiredMixin, CreateView):
    model = VentaDetalle
    form_class = VentaDetalleForm
    template_name = 'agregar_articulo_a_venta.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Verifica si hay una venta en la sesión actual
        venta_id = self.request.session.get('venta_id')
        if venta_id:
            venta = get_object_or_404(Venta, id=venta_id)
        else:
            # Crea una nueva venta si no existe
            venta = Venta.objects.create(vendedor=self.request.user)
            self.request.session['venta_id'] = venta.id

        context['venta'] = venta
        return context

    def form_valid(self, form):
        venta_id = self.request.session.get('venta_id')
        venta = get_object_or_404(Venta, id=venta_id)
        form.instance.venta = venta
        self.object = form.save()
        return redirect('agregar_articulo_a_venta', venta_id=venta.id)


class FinalizarVentaView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        venta_id = request.session.get('venta_id')

        if venta_id:
            venta = get_object_or_404(Venta, id=venta_id)
            # Aquí puedes marcar la venta como pagada o realizar cualquier otra lógica de finalización
            venta.pagado = True
            venta.save()
            # Elimina la venta de la sesión
            del request.session['venta_id']

        # Redirige a la vista de calcular corte con la fecha actual
        fecha_hoy = now().date()
        return redirect(reverse('calcular_corte') + f'?fecha={fecha_hoy}')
