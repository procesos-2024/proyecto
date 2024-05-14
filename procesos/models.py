from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class Articulo(models.Model):
    codigo = models.CharField('Codigo', max_length=50, primary_key=True)
    nombre = models.CharField(blank=False, null=False, max_length=100)
    unidades = models.IntegerField(blank=False, null=False, default=0)
    minimo = models.IntegerField(blank=False, null=False, default=0)

    def __str__(self):
        return self.nombre


class Proveedor(models.Model):
    nombre = models.CharField(blank=False, null=False, max_length=100)
    email = models.EmailField(max_length=254)
    articulos = models.ManyToManyField(Articulo)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Orden(models.Model):
    emisor = models.ForeignKey(User, on_delete=models.CASCADE)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    emision = models.DateTimeField(auto_now_add=True)
    descripcion = models.TextField(max_length=250)
    total = models.IntegerField(default=0)

    def __str__(self):
        return self.descripcion


class ArticuloUnidades(models.Model):
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE)
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE)
    unidades = models.IntegerField(blank=False, null=False, default=0)

    def __str__(self):
        return f"#{self.orden.id} - ({self.unidades}) {self.articulo}"


class ResepcionOrden(models.Model):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    receptor = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.receptor)
