from django.contrib import admin

from .models import *

# Register your models here.

@admin.register(Articulo)
class ArticuloAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'codigo',)


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email',)
    filter_horizontal = ('articulos',)


@admin.register(ResepcionOrden)
class ResepcionOrdenAdmin(admin.ModelAdmin):
    list_display = ('proveedor', 'receptor',)


@admin.register(Orden)
class OrdenAdmin(admin.ModelAdmin):
    list_display = ('proveedor', 'emision', 'descripcion', 'total',)


admin.site.register(ArticuloUnidades)
