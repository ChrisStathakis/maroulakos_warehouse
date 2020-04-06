from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import ProductStorage, ProductIngredient


@receiver(post_save, sender=ProductStorage)
def update_priority(sender, instance, **kwargs):
    if instance.priority:
        ProductStorage.objects.filter(product=instance.product).exclude(id=instance.id).update(priority=False)


@receiver(post_save, sender=ProductIngredient)
def update_price_on_creation(sender, instance, created, **kwargs):
    if created:
        if instance.cost == 0:
            instance.cost = instance.ingredient.price_buy/instance.qty if instance.qty > 0 else 0
            instance.save()
