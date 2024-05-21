import csv

from import_export import resources
from django.contrib import admin, messages
from django.http import HttpResponse
from import_export.admin import ImportExportModelAdmin

from .models import *


# Register your models here.

class ExportCsvMixin:
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"


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
class ArticuloAdmin(ImportExportModelAdmin):
    search_fields = ['nombre', 'codigo', ]
    list_display = ('codigo', 'nombre', 'proveedor', 'unidades', 'minimo')
    list_filter = (LowStockFilter, SinProveedor,)

    actions = ["generar_orden", "export_as_csv"]

    @admin.action(description='Crear ordenes')
    def generar_orden(self, request, queryset):

        if queryset.filter(proveedor__isnull=True).exists():
            messages.warning(request, "Se omitieron artículos sin proveedor!")

        for proveedor in Proveedor.objects.all():
            articulos = queryset.filter(proveedor=proveedor)

            if articulos.exists():
                orden = Orden(
                    emisor=request.user,
                    proveedor=proveedor,
                    descripcion="")

                orden.save()

                for articulo in articulos:
                    orden.add_articulos(articulo, articulo.minimo)


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

class VentaDetalleItemInline(admin.TabularInline):
    autocomplete_fields = ('articulo',)
    model = VentaDetalle
    extra = 1


@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    inlines = [VentaDetalleItemInline]
