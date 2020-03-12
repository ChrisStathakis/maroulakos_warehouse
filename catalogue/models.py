from django.db import models

# Create your models here.


class ProductClass(models.Model):
    title = models.CharField(unique=True, max_length=200)
    wholesale_active = models.BooleanField(default=False, verbose_name="Active for WholeSale")
    is_service = models.BooleanField(default=False, verbose_name='Service')
    have_ingredient = models.BooleanField(default=False, verbose_name='Μεγεθολόγιο')


class Product(models.Model):
    active = models.BooleanField(default=True, verbose_name='Active')
    is_offer = models.BooleanField(default=True)
    title = models.CharField(max_length=120, verbose_name="'Ονομα προιόντος")
    color = models.ForeignKey(Color, blank=True, null=True, verbose_name='Χρώμα', on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, blank=True, null=True)
    brand = models.ForeignKey(Brand, blank=True, null=True, verbose_name='Brand Name', on_delete=models.SET_NULL)

    sku = models.CharField(max_length=150, blank=True, null=True)
    site_text = HTMLField(blank=True, null=True)
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
    vendor = models.ForeignKey(Vendor, verbose_name="Προμηθευτής", blank=True, null=True, on_delete=models.SET_NULL)
    qty = models.DecimalField(default=0, verbose_name="Απόθεμα", max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=1, default='1', choices=UNIT, blank=True, null=True)
    safe_stock = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    order_sku = models.CharField(blank=True, null=True)
    price_buy = models.DecimalField(decimal_places=2, max_digits=6, default=0,
                                    verbose_name="Τιμή Αγοράς")  # the price which you buy the product
    order_discount = models.IntegerField(default=0, verbose_name="'Εκπτωση Τιμολογίου σε %")
    qty_kilo = models.DecimalField(max_digits=5, decimal_places=3, default=1,
                                   verbose_name='Βάρος/Τεμάχια ανά Συσκευασία ')
    objects = models.Manager()
    my_query = ProductManager()

    # site attritubes




