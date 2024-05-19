from django.contrib import admin

from .models import *


# Register your models here.

@admin.register(Articulo)
class ArticuloAdmin(admin.ModelAdmin):
    search_fields=['nombre', 'codigo',]
    list_display = ('nombre', 'codigo',)


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email',)
    search_fields=['nombre',]
    filter_horizontal = ('articulos',)


@admin.register(ResepcionOrden)
class ResepcionOrdenAdmin(admin.ModelAdmin):
    list_display = ('proveedor', 'receptor',)


class CartItemInline(admin.TabularInline):
    autocomplete_fields = ('articulo', )
    model = ArticuloUnidades
    extra = 1

@admin.register(Orden)
class CartAdmin(admin.ModelAdmin):
    list_display = ('proveedor', 'emision', 'descripcion',)
    inlines = [CartItemInline]


# class OrdenAdmin(admin.ModelAdmin):
    # filter_horizontal = ('articulos',)
