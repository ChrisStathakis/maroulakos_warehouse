from django.dispatch import receiver
from django.db.models.signals import post_delete

from .models import OffshoreOrder, OffshorePayment


@receiver(post_delete, sender=OffshoreOrder)
def update_customer_order_delete(sender, instance, **kwargs):
    print('here')
    instance.customer.save()


@receiver(post_delete, sender=OffshorePayment)
def update_customer_payment_delete(sender, instance, **kwargs):
    instance.customer.save()