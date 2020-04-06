from django.db import models
from django.shortcuts import reverse
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save

from catalogue.models import Product, ProductStorage, ProductIngredient
from costumers.models import Costumer
from project_settings.constants import CURRENCY
from project_settings.models import PaymentMethod
from decimal import Decimal


class InvoiceTransformation(models.Model):
    locked = models.BooleanField(default=False, verbose_name="Μετασχηματισμενο")
    date = models.DateField(verbose_name="Ημερομηνια")
    title = models.CharField(max_length=200, verbose_name='Παρτιδα Εμφαλωσης')
    costumer = models.ForeignKey(Costumer, on_delete=models.CASCADE, verbose_name='Πελατης', blank=True, null=True)
    value = models.DecimalField(decimal_places=2, max_digits=17, default=0, verbose_name='Αξια')
    cost = models.DecimalField(decimal_places=2, max_digits=17, default=0, verbose_name='Κοστολογηση')
    payment_method = models.ForeignKey(PaymentMethod, null=True, on_delete=models.SET_NULL, verbose_name='Τροπος Πληρωμής')

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
                                related_name='trans_items', verbose_name='Αποθηκη'
                                )
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    qty = models.DecimalField(decimal_places=2, max_digits=17, default=0, verbose_name='Ποσοτητα')
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

    def tag_value(self):
        return f'{self.value} {CURRENCY}'

    def tag_total_value(self):
        return f'{self.total_value} {CURRENCY}'

    def tag_total_cost(self):
        return f'{self.total_cost} {CURRENCY}'

    def get_delete_url(self):
        return reverse('warehouse:delete_transformation_item', kwargs={'pk': self.id})

    def get_edit_url(self):
        return reverse('warehouse:invoice_item_trans_update', kwargs={'pk': self.id})

    @property
    def date(self):
        return self.invoice.date

    def transcation_type(self):
        return 'Δημιουργημενο Προϊον'

    @property
    def transaction_type_method(self):
        return 'add'

    def transcation_person(self):
        return 'Προσθηκη στην Αποθηκη'

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
    qty_ratio = models.DecimalField(decimal_places=3, max_digits=17, default=0)
    cost = models.DecimalField(decimal_places=2, max_digits=17, default=0)
    total_cost = models.DecimalField(decimal_places=2, max_digits=17, default=0)

    def save(self, *args, **kwargs):
        self.total_cost = Decimal(self.qty) * Decimal(self.cost)
        super().save(*args, **kwargs)
        self.invoice_item.save()
        if self.storage:
            self.storage.save()

    @property
    def date(self):
        return self.invoice_item.date

    def transcation_type(self):
        return 'Μετασχηματιζομενο Προϊον'

    def transcation_person(self):
        return 'Αφαιρεση Απο Αποθηκη'

    @property
    def transaction_type_method(self):
        return 'remove'

    def value(self):
        # for analysis normalization
        return self.cost

    def total_value(self):
        return self.total_cost

    @staticmethod
    def create_from_view(id_list, storages_ids, item, qty):
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


@receiver(post_delete, sender=InvoiceTransformationItem)
def update_trans_invoice_on_delete(sender, instance, **kwargs):
    instance.invoice.save()
    if instance.storage:
        instance.storage.save()
    else:
        instance.product.save()


@receiver(post_delete,sender=InvoiceTransformationIngredient)
def update_warehouse_on_delete(sender, instance, **kwargs):
    if instance.storage:
        instance.storage.save()
    else:
        instance.product.save()