from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.db.models import Sum

# Create your models here.
from project_settings.models import Storage
from project_settings.constants import POSITIVE_INVOICES, NEGATIVE_INVOICES

UNIT = (
        ('a', 'Τεμάχιο'),
        ('b', 'Κιβώτιο'),
        ('c', 'Κιλό'),
    )


class ProductClass(models.Model):
    title = models.CharField(unique=True, max_length=200, verbose_name='Ονομασια')
    have_storage = models.BooleanField(default=False, verbose_name='εχει Αποθηκη')
    wholesale_active = models.BooleanField(default=False, verbose_name="Active for WholeSale")
    is_service = models.BooleanField(default=False, verbose_name='Service')
    have_ingredient = models.BooleanField(default=False, verbose_name='Παρασκευη Απο Εμας')

    def __str__(self):
        return self.title

    @staticmethod
    def filters_data(request, qs):
        return qs


class Product(models.Model):
    active = models.BooleanField(default=True, verbose_name='Active')
    product_class = models.ForeignKey(ProductClass, on_delete=models.PROTECT, null=True)
    is_offer = models.BooleanField(default=True)
    title = models.CharField(max_length=120, verbose_name="'Ονομα προιόντος")
    # color = models.ForeignKey(Color, blank=True, null=True, verbose_name='Χρώμα', on_delete=models.CASCADE)
    # category = models.ManyToManyField(Category, blank=True, null=True)
    # brand = models.ForeignKey(Brand, blank=True, null=True, verbose_name='Brand Name', on_delete=models.SET_NULL)

    sku = models.CharField(max_length=150, blank=True, null=True)
    # site_text = HTMLField(blank=True, null=True)
    meta_description = models.CharField(max_length=300, null=True, blank=True)
    slug = models.SlugField(blank=True, null=True, allow_unicode=True)

    # price sell and discount sells
    price = models.DecimalField(decimal_places=2, max_digits=6, default=0,
                                verbose_name="Τιμή λιανικής")  # the price product have in the store
    margin = models.IntegerField(default=30, verbose_name='Margin', blank=True, null=True)
    markup = models.IntegerField(default=30, verbose_name='Markup', blank=True, null=True)
    price_internet = models.DecimalField(decimal_places=2, max_digits=6, default=0,
                                         verbose_name="Τιμή Internet(No use)")
    price_b2b = models.DecimalField(decimal_places=2, max_digits=6, default=0,
                                    verbose_name="Τιμή Χονδρικής")  # the price product have in the website, if its 0 then website gets the price from store
    price_discount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Εκπτωτική Τιμή.')
    final_price = models.DecimalField(default=0, decimal_places=2, max_digits=10, blank=True)
    # size and color

    related_products = models.ManyToManyField('self', blank=True)
    different_color = models.ManyToManyField('self', blank=True)

    timestamp = models.DateField(default=timezone.now, verbose_name='Ημερομηνία Δημιουργίας')
    notes = models.TextField(null=True, blank=True, verbose_name='Περιγραφή')

    # warehouse_data
    vendor = models.ForeignKey('warehouse.Vendor', verbose_name="Προμηθευτής", blank=True, null=True, on_delete=models.SET_NULL)
    qty = models.DecimalField(default=0, verbose_name="Απόθεμα", max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=1, default='1', choices=UNIT, blank=True, null=True)
    safe_stock = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    order_sku = models.CharField(blank=True, null=True, max_length=50)
    price_buy = models.DecimalField(decimal_places=2, max_digits=6, default=0,
                                    verbose_name="Τιμή Αγοράς")  # the price which you buy the product
    order_discount = models.IntegerField(default=0, verbose_name="'Εκπτωση Τιμολογίου σε %")
    qty_kilo = models.DecimalField(max_digits=5, decimal_places=3, default=1,
                                   verbose_name='Βάρος/Τεμάχια ανά Συσκευασία ')
    taxes_modifier = models.IntegerField(default=24, verbose_name='ΦΠΑ')
    objects = models.Manager()
    # my_query = ProductManager()

    def save(self, *args, **kwargs):
        if self.product_class.have_storage:
            qs = self.storages.all()
            self.qty = qs.aggregate(Sum('qty'))['qty__sum'] if qs.exists() else 0
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_edit_url(self):
        return reverse('catalogue:product_update', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('catalogue:product_delete', kwargs={'pk': self.id})

    def get_prepare_url(self):
        return reverse('warehouse:transform_prepare', kwargs={'pk': self.id})

    def update_product_from_invoice(self, item):
        self.price_buy = item.value
        self.order_discount = item.discount
        self.taxes_modifier = item.taxes_modifier
        self.save()

    @staticmethod
    def filters_data(request, qs):
        return qs
    
    def estimate_qty(self):
        product_class = self.product_class
        if product_class.have_storage:
            return 0
        elif product_class.support_transcations:
            invoices = self.product_items.all()
            return 0
        else:
            return 0


class ProductStorage(models.Model):
    priority = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='storages')
    storage = models.ForeignKey(Storage, on_delete=models.PROTECT)
    qty = models.DecimalField(decimal_places=2, max_digits=17, default=0)

    def save(self, *args, **kwargs):
        invoices = self.storage_invoices.all()
        add_invoices, remove_invoices = invoices.filter(invoice__order_type__in=POSITIVE_INVOICES), \
                                        invoices.filter(invoice__order_type__in=NEGATIVE_INVOICES)
        add_qty = add_invoices.aggregate(Sum('qty'))['qty__sum'] if add_invoices.exists() else 0
        remove_qty = remove_invoices.aggregate(Sum('qty'))['qty__sum'] if remove_invoices.exists() else 0
        self.qty = add_qty - remove_qty
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ['product', 'storage']
        ordering = ['priority']
    
    def __str__(self):
        return self.storage.title


class ProductIngredient(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ingredients')
    ingredient = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ingredient_value')
    qty = models.DecimalField(decimal_places=2, max_digits=17)
    cost = models.DecimalField(decimal_places=2, max_digits=17)

    class Meta:
        unique_together = ['product', 'ingredient']

    def __str__(self):
        return self.ingredient.title




