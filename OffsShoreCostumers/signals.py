from django.dispatch import receiver
from django.db.models.signals import post_delete

from .models import OffshoreOrder, OffshorePayment, OffsShoreCompanyCostumer, OffsShoreCostumer


@receiver(post_delete, sender=OffshoreOrder)
def update_customer_order_delete(sender, instance, **kwargs):
    print('here')
    instance.customer.save()


@receiver(post_delete, sender=OffshorePayment)
def update_customer_payment_delete(sender, instance, **kwargs):
    instance.customer.save()


@receiver(post_delete, sender=OffsShoreCompanyCostumer)
def update_company_on_delete(sender, instance, **kwargs):
    instance.company.save()


@receiver(post_delete, sender=OffsShoreCostumer)
def update_company_again(sender, instance, **kwargs):
    customers = instance.offsshorecompanycostumer_set.all()
    for cust in customers:
        cust.delete()