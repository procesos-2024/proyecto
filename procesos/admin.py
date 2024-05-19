from django.contrib import admin

from .models import *


# Register your models here.

class SinProveedor(admin.SimpleListFilter):
    title = 'Proveedor'
    parameter_name = 'proveedor'

    def lookups(self, request, model_admin):
        return [('sin_proveedor', 'sin proveedor')] + [(nombre.id, nombre) for nombre in Proveedor.objects.all()]

    def queryset(self, request, queryset):
        if self.value() == 'sin_proveedor':
            return queryset.filter(proveedor__isnull=True)

        if self.value() is not None:
            return queryset.filter(proveedor=self.value())

        # si no se selecciona ninguna opcion
        return queryset


class LowStockFilter(admin.SimpleListFilter):
    title = 'stock'
    parameter_name = 'minimo'

    def lookups(self, request, model_admin):
        return (
            ('below_minimum', 'Stock Bajo'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'below_minimum':
            return queryset.filter(unidades__lt=models.F('minimo'))
        return queryset


@admin.register(Articulo)
class ArticuloAdmin(admin.ModelAdmin):
    search_fields = ['nombre', 'codigo', ]
    list_display = ('codigo', 'nombre', 'proveedor', 'unidades', 'minimo')
    list_filter = (LowStockFilter, SinProveedor,)


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email',)
    search_fields = ['nombre', ]


class CartItemInline(admin.TabularInline):
    autocomplete_fields = ('articulo',)
    model = ArticuloUnidades
    extra = 1


@admin.register(Orden)
class CartAdmin(admin.ModelAdmin):
    list_display = ('proveedor', 'emision', 'descripcion',)
    inlines = [CartItemInline]

# class OrdenAdmin(admin.ModelAdmin):
# filter_horizontal = ('articulos',)
