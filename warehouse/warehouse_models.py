from django.db import models
from django.db.models import Sum
from catalogue.models import Product, ProductStorage
from costumers.models import Costumer


class InvoiceTransformation(models.Model):
    locked = models.BooleanField(default=False)
    date = models.DateField()
    title = models.CharField(max_length=200)
    costumer = models.ForeignKey(Costumer, on_delete=models.CASCADE)
    value = models.DecimalField(decimal_places=2, max_digits=17, default=0)
    cost = models.DecimalField(decimal_places=2, max_digits=17, default=0)


class InvoiceTransformationItem(models.Model):
    invoice = models.ForeignKey(InvoiceTransformation, on_delete=models.CASCADE)
    storage = models.ForeignKey(ProductStorage, on_delete=models.PROTECT, blank=True, null=True,
                                related_name='trans_items'
                                )
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    qty = models.DecimalField(decimal_places=2, max_digits=17, default=0)
    value = models.DecimalField(decimal_places=2, max_digits=17, default=0)

    total_value = models.DecimalField(decimal_places=2, max_digits=17, default=0)
    total_cost = models.DecimalField(decimal_places=2, max_digits=17, default=0)

    def save(self, *args, **kwargs):
        qs = self.transf_ingre.all()
        self.total_cost = qs.aggregate(Sum('total_cost'))['total_cost_sum'] if qs.exists() else 0
        self.total_value = self.qty * self.value
        super().save(*args, **kwargs)
        if self.product.product_class.have_storage:
            self.storage.save()
        else:
            self.product.save()


class InvoiceTransformationIngredient(models.Model):
    invoice_item = models.ForeignKey(InvoiceTransformationItem, on_delete=models.CASCADE, related_name='transf_ingre')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    storage = models.ForeignKey(ProductStorage, on_delete=models.PROTECT,
                                blank=True, null=True, related_name='storage_ingre'
                                )
    qty = models.DecimalField(decimal_places=2, max_digits=17, default=0)
    cost = models.DecimalField(decimal_places=2, max_digits=17, default=0)
    total_cost = models.DecimalField(decimal_places=2, max_digits=17, default=0)

    def save(self, *args, **kwargs):
        self.total_cost = self.qty * self.cost
        super().save(*args, **kwargs)
        self.invoice_item.save()

