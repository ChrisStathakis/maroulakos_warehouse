from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.db.models import Sum, Q

from mptt.models import MPTTModel, TreeForeignKey
# Create your models here.
from project_settings.models import Storage
from project_settings.constants import POSITIVE_INVOICES, NEGATIVE_INVOICES

UNIT = (
        ('a', 'Τεμάχιο'),
        ('b', 'Κιβώτιο'),
        ('c', 'Κιλό'),
    )


class Category(MPTTModel):
    name = models.CharField(max_length=240, unique=True, verbose_name='Τίτλος')
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', verbose_name='Γονεας')

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' -> '.join(full_path[::-1])

    def get_edit_url(self):
        return reverse('catalogue:category_update', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('catalogue:category_delete', kwargs={'pk': self.id})

    def get_card_url(self):
        return reverse('vendors:category_card', kwargs={'pk': self.id})

    @staticmethod
    def filters_data(request, qs):
        search_name = request.GET.get('search_name', None)
        q = request.GET.get('q', None)
        qs = qs.filter(name__icontains=q) if q else qs
        qs = qs.filter(name__contains=search_name) if search_name else qs
        return qs


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
    active = models.BooleanField(default=True, verbose_name='Κατασταση')
    product_class = models.ForeignKey(ProductClass, on_delete=models.PROTECT, null=True, verbose_name='Ειδος')
    is_offer = models.BooleanField(default=True)
    title = models.CharField(max_length=120, verbose_name="'Ονομα προιόντος")
    # color = models.ForeignKey(Color, blank=True, null=True, verbose_name='Χρώμα', on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, blank=True, null=True, verbose_name='Κατηγοριες')
    # brand = models.ForeignKey(Brand, blank=True, null=True, verbose_name='Brand Name', on_delete=models.SET_NULL)

    sku = models.CharField(max_length=150, blank=True, null=True, verbose_name='MPN')
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
    unit = models.CharField(max_length=1, default='1', choices=UNIT, blank=True, null=True, verbose_name='ΜΜ')
    safe_stock = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name='Ασφαλη Αποθεμα')
    safe_warning = models.BooleanField(default=False)
    order_sku = models.CharField(blank=True, null=True, max_length=50, verbose_name='Κωδικος Τιμολογιου')
    price_buy = models.DecimalField(decimal_places=2, max_digits=6, default=0,
                                    verbose_name="Τιμή Αγοράς")  # the price which you buy the product
    order_discount = models.IntegerField(default=0, verbose_name="'Εκπτωση Τιμολογίου σε %")
    qty_kilo = models.DecimalField(max_digits=5, decimal_places=3, default=1,
                                   verbose_name='Βάρος/Τεμάχια ανά Συσκευασία ')
    taxes_modifier = models.IntegerField(default=24, verbose_name='ΦΠΑ')
    objects = models.Manager()
    # my_query = ProductManager()

    def save(self, *args, **kwargs):
        self.safe_warning = False if self.safe_stock == 0 else False if self.qty > self.safe_stock else True
        if self.product_class.have_storage:
            qs = self.storages.all()
            self.qty = qs.aggregate(Sum('qty'))['qty__sum'] if qs.exists() else 0
        if self.product_class.have_ingredient:
            qs = self.ingredients.all()
            self.price_buy = qs.aggregate(Sum('cost'))['cost__sum'] if qs.exists() else 0
        self.final_price = self.price_discount if self.price_discount > 0 else self.price
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_edit_url(self):
        return reverse('catalogue:product_update', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('catalogue:product_delete', kwargs={'pk': self.id})

    def get_prepare_url(self):
        return reverse('warehouse:transform_prepare', kwargs={'pk': self.id})

    def favorite_storage(self):
        print('here!')
        return self.storages.filter(priority=True).first() if self.storages.filter(priority=True).exists() else None

    def update_product_from_invoice(self, item):
        self.price_buy = item.value
        self.order_discount = item.discount
        self.taxes_modifier = item.taxes_modifier
        self.save()

    def update_product_from_sale(self, item):
        self.price = item.value
        self.taxes_modifier = item.taxes_modifier
        self.save()

    @staticmethod
    def filters_data(request, qs):
        q = request.GET.get('q', None)
        search_name = request.GET.get('search_name', None)
        product_class_name = request.GET.get('product_class_name', None)
        if product_class_name:
            qs = qs.filter(product_class__have_ingredient=True)

        if q:
            qs = qs.filter(Q(title__icontains=q) |
                           Q(order_sku__icontains=q) |
                           Q(sku__icontains=q)
                           ).distinct()
        if search_name:
            qs = qs.filter(Q(title__icontains=search_name) |
                           Q(order_sku__icontains=search_name) |
                           Q(sku__icontains=search_name)
                           ).distinct()
        return qs


class ProductStorage(models.Model):
    priority = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='storages')
    storage = models.ForeignKey(Storage, on_delete=models.PROTECT, verbose_name='Αποθηκη')
    qty = models.DecimalField(decimal_places=2, max_digits=17, default=0)

    def save(self, *args, **kwargs):
        invoices = self.storage_invoices.all()
        add_invoices, remove_invoices = invoices.filter(invoice__order_type__in=POSITIVE_INVOICES), \
                                        invoices.filter(invoice__order_type__in=NEGATIVE_INVOICES)
        add_qty = add_invoices.aggregate(Sum('qty'))['qty__sum'] if add_invoices.exists() else 0
        remove_qty = remove_invoices.aggregate(Sum('qty'))['qty__sum'] if remove_invoices.exists() else 0

        trans_items = self.trans_items.all()
        add_qty_2 = trans_items.aggregate(Sum('qty'))['qty__sum'] if trans_items.exists() else 0

        ingre_items = self.storage_ingre.all()
        remove_qty_2 = ingre_items.aggregate(Sum('qty'))['qty__sum'] if ingre_items.exists() else 0

        self.qty = add_qty + add_qty_2 - remove_qty - remove_qty_2
        super().save(*args, **kwargs)
        self.product.save()

    def update_product(self, value, discount):
        self.product.price_buy = value
        self.product.order_discount = discount
        self.product.save()

    class Meta:
        unique_together = ['product', 'storage']
        ordering = ['priority']
    
    def __str__(self):
        return self.storage.title

    def get_edit_url(self):
        return reverse('catalogue:product_storage_update', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('catalogue:delete_product_storage', kwargs={'pk': self.id})


class ProductIngredient(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ingredients')
    ingredient = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ingredient_value', verbose_name='Συστατικο')
    qty = models.DecimalField(decimal_places=2, max_digits=17, verbose_name='Αναλογια')
    cost = models.DecimalField(decimal_places=2, max_digits=17, verbose_name='Κοστος')

    def save(self, *args, **kwargs):
        if self.cost == 0:
            self.cost = self.ingredient.price_buy * (100-self.ingredient.order_discount)/100
        super().save(*args, **kwargs)
        self.product.save()

    class Meta:
        unique_together = ['product', 'ingredient']

    def __str__(self):
        return self.ingredient.title

    def get_edit_url(self):
        return reverse('catalogue:update_ingredient', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('catalogue:delete_ingredient', kwargs={'pk': self.id})






