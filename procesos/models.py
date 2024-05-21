from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Venta(models.Model):
    vendedor = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    pagado = models.BooleanField(default=False)
    articulos = models.ManyToManyField('Articulo', through='VentaDetalle', related_name='ventas')

    def __str__(self):
        return f"Venta #{self.id} - {self.fecha}"


class VentaDetalle(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='detalles')
    articulo = models.ForeignKey('Articulo', on_delete=models.CASCADE)
    cantidad = models.IntegerField(blank=False, null=False, default=0)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        self.subtotal = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)
        self.venta.total += self.subtotal
        self.venta.save()

    def __str__(self):
        return f"{self.cantidad} x {self.articulo.nombre} @ {self.precio_unitario}"


class Articulo(models.Model):
    codigo = models.CharField('Codigo', max_length=50)
    nombre = models.CharField(blank=False, null=False, max_length=100)
    unidades = models.IntegerField(blank=False, null=False, default=0)
    minimo = models.IntegerField(blank=False, null=False, default=0)
    proveedor = models.ForeignKey('Proveedor', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.nombre


class Proveedor(models.Model):
    nombre = models.CharField(blank=False, null=False, max_length=100)
    email = models.EmailField(max_length=254)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class ArticuloUnidades(models.Model):
    orden = models.ForeignKey('Orden', on_delete=models.CASCADE)
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE)
    unidades = models.IntegerField(blank=False, null=False, default=0)

    def __str__(self):
        return f"#{self.orden.id} - ({self.unidades}) {self.articulo}"


class Orden(models.Model):
    emisor = models.ForeignKey(User, on_delete=models.CASCADE)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    emision = models.DateTimeField(auto_now_add=True)
    descripcion = models.TextField(max_length=250)
    articulos = models.ManyToManyField(Articulo, through='ArticuloUnidades', related_name='articulos_solicitados')
    recibido = models.BooleanField(default=False)

    def add_articulos(self, articulo, unidades):
        articulo_orden, created = ArticuloUnidades.objects.get_or_create(orden=self, articulo=articulo)

        if not created:
            articulo_orden.unidades += unidades
        else:
            articulo_orden.unidades = unidades

        articulo_orden.save()

    def __str__(self):
        return self.descripcion
