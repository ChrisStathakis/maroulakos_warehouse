from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import ProductStorage


@receiver(post_save, sender=ProductStorage)
def update_priority(sender, instance, **kwargs):
    if instance.priority:
        ProductStorage.objects.filter(product=instance.product).exclude(id=instance.id).update(priority=False)


