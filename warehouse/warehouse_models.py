from django.db import models
from django.shortcuts import reverse
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from catalogue.models import Product, ProductStorage, ProductIngredient
from costumers.models import Costumer

from decimal import Decimal


class InvoiceTransformation(models.Model):
    locked = models.BooleanField(default=False)
    date = models.DateField()
    title = models.CharField(max_length=200)
    costumer = models.ForeignKey(Costumer, on_delete=models.CASCADE)
    value = models.DecimalField(decimal_places=2, max_digits=17, default=0)
    cost = models.DecimalField(decimal_places=2, max_digits=17, default=0)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        qs = self.invoicetransformationitem_set.all()
        self.cost = qs.aggregate(Sum('total_cost'))['total_cost__sum'] if qs.exists() else 0
        self.value = qs.aggregate(Sum('total_value'))['total_value__sum'] if qs.exists() else 0
        super().save(*args, **kwargs)

    def get_edit_url(self):
        return reverse('warehouse:invoice_trans_detail', kwargs={'pk': self.id})


class InvoiceTransformationItem(models.Model):
    invoice = models.ForeignKey(InvoiceTransformation, on_delete=models.CASCADE)
    storage = models.ForeignKey(ProductStorage, on_delete=models.PROTECT, blank=True, null=True,
                                related_name='trans_items'
                                )
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    qty = models.DecimalField(decimal_places=2, max_digits=17, default=0, verbose_name='Ποσοτητσ')
    value = models.DecimalField(decimal_places=2, max_digits=17, default=0, verbose_name='Αξια')

    total_value = models.DecimalField(decimal_places=2, max_digits=17, default=0)
    total_cost = models.DecimalField(decimal_places=2, max_digits=17, default=0)

    def save(self, *args, **kwargs):
        qs = self.transf_ingre.all()
        self.total_cost = qs.aggregate(Sum('total_cost'))['total_cost__sum'] if qs.exists() else 0
        self.total_value = Decimal(self.qty) * Decimal(self.value)
        super().save(*args, **kwargs)
        if self.storage:
            self.storage.save()
        else:
            self.product.save()
        self.invoice.save()

    def __str__(self):
        return self.product.title

    @staticmethod
    def create_from_view(invoice, product, qty):
        new = InvoiceTransformationItem.objects.create(
            product=product,
            invoice=invoice,
            qty=qty,
            value=product.final_price,

        )
        return new


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
        self.total_cost = Decimal(self.qty) * Decimal(self.cost)
        super().save(*args, **kwargs)
        self.invoice_item.save()
        if self.storage:
            self.storage.save()

    @staticmethod
    def create_from_view(id_list, storages_ids, item, qty):
        print('cost', id_list[1])
        storage = None
        for ele in storages_ids:
            if ele[0] == id_list[0]:
                storage = get_object_or_404(ProductStorage, id=ele[1])
        product_indi = get_object_or_404(ProductIngredient, id=id_list[0])
        correct_qty = round(qty/product_indi.qty, 2)
        product = product_indi.product

        instance = InvoiceTransformationIngredient.objects.create(
            invoice_item=item,
            product=product,
            qty=correct_qty,
            cost=id_list[1],
        )
        if storage:
            instance.storage = storage
            instance.save()


