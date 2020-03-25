from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import SalesInvoice, SalesInvoiceItem


@receiver(post_delete, sender=SalesInvoice)
def update_costumer_on_delete(sender, instance, **kwargs):
    instance.costumer.save()


@receiver(post_save, sender=SalesInvoiceItem)
def update_warehouse_and_invoice(sender, instance, **kwargs):
    instance.invoice.save()
    if instance.storage:
        instance.storage.save()
    else:
        instance.product.save()


@receiver(post_delete, sender=SalesInvoiceItem)
def update_on_delete_warehouse_and_invoice(sender, instance, **kwargs):
    instance.invoice.save()
    if instance.storage:
        instance.storage.save()
    else:
        instance.product.save()
    instance.storage.save() if instance.storage else instance.product.save()



