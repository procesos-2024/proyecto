from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string

from Proyecto import settings
from .models import *


@receiver(post_save, sender=Orden)
def update_stock_on_checkout(sender, instance, **kwargs):

    if instance.recibido:
        for item in instance.articulounidades_set.all():
            product = item.articulo
            product.unidades += item.unidades
            product.save()

            """
            if product.units_in_stock < product.minimum_stock:
                send_mail(
                    subject="Test Email",
                    from_email=settings.EMAIL_HOST_USER,
                    fail_silently=False,
                    message=f'El producto {product.name} tiene un stock de {product.units_in_stock} unidades, por debajo del mínimo de {product.minimum_stock}.',
                    recipient_list=[
                        object.autorizador.email
                    ]
                )"""

