from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path

from .views import AgregarArticuloAVentaView
from .views import CalcularCorteView
from .views import EliminarArticuloDeVentaView
from .views import FinalizarVentaView
from .views import ProveedorListView
from .views import RegisterProveedor
from .views import RegisterView
from .views import index

urlpatterns = [
    path('', index, name='index'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('agregar-articulo/', AgregarArticuloAVentaView.as_view(), name='agregar_articulo_a_venta'),
    path('finalizar-venta/', FinalizarVentaView.as_view(), name='finalizar_venta'),
    path('agregar_articulo_a_venta/<int:venta_id>/', AgregarArticuloAVentaView.as_view(),
         name='agregar_articulo_a_venta'),
    path('register_provedor', RegisterProveedor.as_view(), name='crear_provedor'),
    path('proveedores/', ProveedorListView.as_view(), name='listar_proveedores'),
    path('calcular_corte/', CalcularCorteView.as_view(), name='calcular_corte'),
    path('eliminar-articulo/<int:pk>/', EliminarArticuloDeVentaView.as_view(), name='eliminar_articulo_de_venta')
]
