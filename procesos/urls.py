from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

from .views import RegisterView, index

urlpatterns = [
    path('', index, name='index'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('venta/nueva/', views.crear_venta, name='crear_venta'),
    path('venta/<int:venta_id>/agregar/', views.agregar_articulo_a_venta, name='agregar_articulo_a_venta'),
    path('venta/<int:venta_id>/', views.ver_venta, name='ver_venta'),
]