from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path

from .views import RegisterView, index, RegisterProveedor, ProveedorListView, CrearOrdenView, OrdenCreadaView, \
    CalcularCorteView, AgregarArticuloAVentaView, VerVentaView, FinalizarVentaView

urlpatterns = [
    path('', index, name='index'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),

    path('agregar-articulo/', AgregarArticuloAVentaView.as_view(), name='agregar_articulo_a_venta'),
    path('finalizar-venta/', FinalizarVentaView.as_view(), name='finalizar_venta'),

    #path('crear_venta/', CrearVentaView.as_view(), name='crear_venta'),
    path('agregar_articulo_a_venta/<int:venta_id>/', AgregarArticuloAVentaView.as_view(), name='agregar_articulo_a_venta'),
    path('ver_venta/<int:venta_id>/', VerVentaView.as_view(), name='ver_venta'),

    path('register_provedor', RegisterProveedor.as_view(), name='crear_provedor'),
    path('proveedores/', ProveedorListView.as_view(), name='listar_proveedores'),
    path('ordenar_articulos/', CrearOrdenView.as_view(), name='ordenar_articulos'),
    path('orden_creada/', OrdenCreadaView.as_view(), name='orden_creada'),
    path('calcular_corte/', CalcularCorteView.as_view(), name='calcular_corte'),
]
