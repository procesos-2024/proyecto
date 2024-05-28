# Generated by Django 5.0.6 on 2024-05-27 00:31

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Articulo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("codigo", models.CharField(max_length=50, verbose_name="Codigo")),
                ("nombre", models.CharField(max_length=100)),
                ("unidades", models.IntegerField(default=0)),
                (
                    "precio_unitario",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                ("minimo", models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name="Proveedor",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nombre", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=254)),
                ("activo", models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name="ArticuloUnidades",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("unidades", models.IntegerField(default=0)),
                (
                    "articulo",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="procesos.articulo",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Orden",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("emision", models.DateTimeField(auto_now_add=True)),
                ("descripcion", models.TextField(max_length=250)),
                ("recibido", models.BooleanField(default=False)),
                (
                    "articulos",
                    models.ManyToManyField(
                        related_name="articulos_solicitados",
                        through="procesos.ArticuloUnidades",
                        to="procesos.articulo",
                    ),
                ),
                (
                    "emisor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "proveedor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="procesos.proveedor",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="articulounidades",
            name="orden",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="procesos.orden"
            ),
        ),
        migrations.AddField(
            model_name="articulo",
            name="proveedor",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="procesos.proveedor",
            ),
        ),
        migrations.CreateModel(
            name="Venta",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("fecha", models.DateTimeField(auto_now_add=True)),
                (
                    "total",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
                ),
                ("pagado", models.BooleanField(default=False)),
                (
                    "vendedor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="VentaDetalle",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("cantidad", models.IntegerField(default=0)),
                (
                    "subtotal",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
                ),
                (
                    "articulo",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="procesos.articulo",
                    ),
                ),
                (
                    "venta",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="detalles",
                        to="procesos.venta",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="venta",
            name="articulos",
            field=models.ManyToManyField(
                related_name="ventas",
                through="procesos.VentaDetalle",
                to="procesos.articulo",
            ),
        ),
    ]