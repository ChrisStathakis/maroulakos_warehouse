from django.db import models
from django.db.models import Sum, Q
from django.conf import settings
from django.shortcuts import reverse
from django.db.models.signals import post_delete
from django.dispatch import receiver

from tinymce.models import HTMLField
from decimal import Decimal

from project_settings.models import PaymentMethod
from project_settings.tools import initial_date
from project_settings.constants import INVOICE_TYPES, CURRENCY, POSITIVE_INVOICES
from catalogue.models import Product, ProductStorage


TAXES_CHOICES = (
    ('a', 0),
    ('b', 13),
    ('c', 24)
)


class Vendor(models.Model):
    active = models.BooleanField(default=True, verbose_name='Ενεργό')
    title = models.CharField(max_length=200, unique=True, verbose_name='Εταιρία')
    owner = models.CharField(max_length=200, blank=True, verbose_name='Ιδιοκτήτης')
    afm = models.CharField(max_length=150, blank=True, verbose_name='ΑΦΜ')
    doy = models.CharField(max_length=150, blank=True, verbose_name='ΔΟΥ')
    phone = models.CharField(max_length=200, blank=True, verbose_name='Σταθερο Τηλεφωνο')
    cellphone = models.CharField(max_length=200, blank=True, verbose_name='Κινητό')
    email = models.EmailField(blank=True)
    site = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True, verbose_name='Λεπτομεριες')
    address = models.CharField(max_length=240, blank=True, null=True, verbose_name='Διευθυνση')
    city = models.CharField(max_length=240, blank=True, null=True, verbose_name='Πολη')
    balance = models.DecimalField(decimal_places=2, max_digits=50, default=0.00, verbose_name='Υπόλοιπο')
    paid_value = models.DecimalField(decimal_places=2, max_digits=50, default=0.00)
    value = models.DecimalField(decimal_places=2, max_digits=50, default=0.00)
    taxes_modifier = models.CharField(max_length=1, choices=TAXES_CHOICES, default='c')

    class Meta:
        ordering = ['title']

    def __str__(self):
        return f'{self.title}'

    def save(self, *args, **kwargs):
        self.balance = Decimal(self.value) - Decimal(self.paid_value)
        self.title = self.title.upper()
        super().save(*args, **kwargs)

    def get_edit_url(self):
        return reverse('warehouse:vendor_update', kwargs={'pk': self.id})

    def get_card_url(self):
        return reverse('warehouse:vendor_card', kwargs={'pk': self.id})

    def get_note_url(self):
        return reverse('warehouse:notes', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('warehouse:vendor_delete', kwargs={'pk': self.id})

    def update_paid_value(self):
        qs = self.payments.filter(is_paid=True)
        value = qs.aggregate(Sum('value'))['value__sum'] if qs.exists() else 0
        self.paid_value = Decimal(value)
        self.save()

    def update_value(self):
        qs = self.invoices.filter(order_type='a')
        value = qs.aggregate(Sum('final_value'))['final_value__sum'] if qs.exists() else 0
        self.value = Decimal(value)
        self.save()

    def tag_balance(self):
        return f'{self.balance} {CURRENCY}'

    tag_balance.short_description = 'Υπολοίπο'

    @staticmethod
    def filters_data(request, qs):
        search_name = request.GET.get('q', None)
        search_name_ = request.GET.get('search_name', None)
        vendor_name = request.GET.getlist('vendor_name', None)
        balance_name = request.GET.getlist('balance_name', [])

        if search_name_:
            qs = qs.filter(Q(title__icontains=search_name_) |
                           Q(afm__icontains=search_name_) |
                           Q(cellphone__icontains=search_name_) |
                           Q(phone__icontains=search_name_) |
                           Q(owner__icontains=search_name_)
                           ).distinct()

        qs = qs.filter(title__icontains=search_name.upper()) if search_name else qs
        qs = qs.filter(balance__gt=0) if 'have_' in balance_name else qs.filter(balance_name__lte=0) \
            if 'not' in balance_name else qs
        qs = qs.filter(id__in=vendor_name) if vendor_name else qs
        return qs


class Employer(models.Model):
    active = models.BooleanField(default=True)
    title = models.CharField(max_length=200, verbose_name='Ονομασια')
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='persons', verbose_name='Προμηθευτης')
    phone = models.CharField(max_length=10, blank=True, verbose_name='Τηλεφωνο')
    cellphone = models.CharField(max_length=10, blank=True, verbose_name='Κινητο')
    email = models.EmailField(blank=True)

    class Meta:
        ordering = ['title', ]

    def __str__(self):
        return self.title


class VendorBankingAccount(models.Model):
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE, related_name='banking_accounts',
                                       null=True, verbose_name='Τροπος Πληρωμής')
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, verbose_name='Προμηθευτής', related_name='bankings')
    name = models.CharField(max_length=150, blank=True, verbose_name='Ονομα Δικαιούχου')
    iban = models.CharField(max_length=150, blank=True, )
    code = models.CharField(max_length=200, blank=True, verbose_name='Αριθμός Λογαριασμού')

    def __str__(self):
        return f'{self.vendor.title} {self.payment_method.title}'

    def get_edit_url(self):
        return reverse('warehouse:ajax_edit_banking_account', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('warehouse:delete_banking_account_view', kwargs={'pk': self.id})


class Invoice(models.Model):
    date = models.DateField(verbose_name='Ημερομηνια')
    order_type = models.CharField(max_length=1, choices=INVOICE_TYPES, default='a')
    title = models.CharField(max_length=150, verbose_name='Αριθμος Τιμολογιου')
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.PROTECT, null=True,
                                       verbose_name='Τροπος Πληρωμης')
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='invoices', verbose_name='Προμηθευτης')
    value = models.DecimalField(decimal_places=2, max_digits=20, verbose_name='Καθαρή Αξια', default=0.00)
    taxes_value = models.DecimalField(decimal_places=2, max_digits=20, verbose_name='Φορος', default=0)
    extra_value = models.DecimalField(decimal_places=2, max_digits=20, verbose_name='Επιπλέον Αξία', default=0.00)
    final_value = models.DecimalField(decimal_places=2, max_digits=20, verbose_name='Αξία', default=0.00)
    description = models.TextField(blank=True, verbose_name='Λεπτομεριες')

    class Meta:
        ordering = ['-date']

    def save(self, *args, **kwargs):
        qs = self.order_items.all()
        self.value = qs.aggregate(Sum('total_clean_value'))['total_clean_value__sum'] if qs.exists() else 0.00
        self.taxes_value = qs.aggregate(Sum('taxes_value'))['taxes_value__sum'] if qs.exists() else 0.00
        self.final_value = round(Decimal(self.value) + Decimal(self.extra_value) + Decimal(self.taxes_value), 2)
        super(Invoice, self).save(*args, **kwargs)
        if self.vendor:
            self.vendor.update_value()

    def __str__(self):
        return f'{self.title}'

    def get_edit_url(self):
        return reverse('warehouse:invoice_update', kwargs={'pk': self.id})

    def tag_value(self):
        return f'{self.value} {CURRENCY}'

    def tag_final_value(self):
        return f'{self.final_value} {CURRENCY}'

    def tag_order_type(self):
        return self.get_order_type_display()

    def tag_person(self):
        return self.vendor

    

    @staticmethod
    def filters_data(request, qs):
        date_start, date_end, date_range = initial_date(request, 6)
        search_name = request.GET.get('search_name', None)
        vendor_name = request.GET.getlist('vendor_name', None)
        qs = qs.filter(title__icontains=search_name) if search_name else qs
        qs = qs.filter(vendor__id__in=vendor_name) if vendor_name else qs
        if date_start and date_end:
            qs = qs.filter(date__range=[date_start, date_end])
        return qs


class InvoiceItem(models.Model):
    UNITS = (
        ('a', 'Τεμάχιο'),
        ('b', 'Κιβώτιο'),
        ('c', 'Κιλό'),

    )
    order_code = models.CharField(max_length=50, blank=True, verbose_name='Κωδικος Τιμολογιου')
    vendor = models.ForeignKey(Vendor, on_delete=models.PROTECT, verbose_name='Προμηθευτης')
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='invoice_items', verbose_name='Προϊον')

    unit = models.CharField(max_length=1, choices=UNITS, default='a', verbose_name='ΜΜ')
    qty = models.DecimalField(max_digits=17, decimal_places=2, default=1, verbose_name='Ποσότητα')
    value = models.DecimalField(max_digits=17, decimal_places=2, verbose_name='Τιμή')

    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Εκπτωση')
    discount_value = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Ποσο Εκπτωσης')

    clean_value = models.DecimalField(max_digits=17, decimal_places=2, verbose_name='Αξια')
    total_clean_value = models.DecimalField(max_digits=17, decimal_places=2, verbose_name='Καθαρη Αξια')
    taxes_modifier = models.IntegerField(default=24, verbose_name='ΦΠΑ')
    taxes_value = models.DecimalField(max_digits=17, decimal_places=2, verbose_name='Αξια ΦΠΑ')
    total_value = models.DecimalField(max_digits=17, decimal_places=2, verbose_name='Τελικη Αξία')
    storage = models.ForeignKey(ProductStorage, blank=True, null=True, on_delete=models.PROTECT, related_name='storage_invoices', verbose_name='Αποθηκη')
    used_qty = models.DecimalField(max_digits=17, decimal_places=2, verbose_name='Χρησιμοποιημενη Ποσοτητα', default=0)
    locked = models.BooleanField(default=False, verbose_name='Κλειδωμενο')

    def save(self, *args, **kwargs):
        print(self.value,100-self.discount/100, self.discount)
        self.clean_value = self.value * ((100-self.discount)/100)
        self.discount_value = (Decimal(self.value) * Decimal(self.discount / 100)) * (self.qty)
        self.total_clean_value = self.clean_value * self.qty

        self.taxes_value = Decimal(self.total_clean_value) * Decimal(self.taxes_modifier / 100)
        self.total_value = Decimal(self.total_clean_value) + Decimal(self.taxes_value)
        self.used_qty = self.warehouse_items.aggregate(Sum('qty'))['qty__sum'] if self.warehouse_items.exists() else 0
        if self.used_qty >= self.qty:
            self.locked = True
        super().save(*args, **kwargs)
        if self.storage:
            self.storage.update_product(self.value, self.discount, )
            self.storage.save()
        else:
            self.product.save()
        self.invoice.save()

    def get_delete_url(self):
        return reverse('warehouse:delete_invoice_item', kwargs={'pk': self.id})

    def get_locked_url(self):
        return reverse('warehouse:invoice_item_locked', kwargs={'pk': self.id})

    def tag_value(self):
        str_value = str(self.value).replace('.', ',')
        return str_value

    def not_used_qty(self):
        return self.qty - self.used_qty

    def tag_clean_value(self):
        return str(self.clean_value).replace('.', ',')

    def final_value(self):
        return round(self.value * ((100 - self.discount)/100), 2)

    def tag_total_value(self):
        return str(self.total_clean_value).replace('.', ',')

    def tag_discount(self):
        return str(self.discount).replace('.', ',')

    def tag_date(self):
        return self.invoice.date

    

    @property
    def transaction_type_method(self):
        return 'add' if self.invoice.order_type in POSITIVE_INVOICES else 'remove'

    @property
    def date(self):
        return self.invoice.date

    def transcation_type(self):
        return self.invoice.get_order_type_display()

    def transcation_person(self):
        return self.invoice.vendor

    @staticmethod
    def filters_data(request, qs):
        print('workd')
        date_start, date_end, date_range = initial_date(request, 6)
        vendor_name = request.GET.getlist('vendor_name', None)

        qs = qs.filter(vendor__id__in=vendor_name) if vendor_name else qs

        if date_start and date_end:
            qs = qs.filter(invoice__date__range=[date_start, date_end])
        return qs


class Payment(models.Model):
    is_paid = models.BooleanField(default=True, verbose_name='Πληρωμενο;')
    date = models.DateField(verbose_name='Ημερομηνία')
    title = models.CharField(max_length=150, verbose_name='Τίτλος')
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.PROTECT, null=True,
                                       verbose_name='Τροπος Πληρωμής')
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='payments', verbose_name='Προμηθευτής')
    value = models.DecimalField(decimal_places=2, max_digits=20, verbose_name='Αξία')
    description = models.TextField(blank=True, verbose_name='Περιγραφή')


    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f'{self.title}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.vendor:
            self.vendor.update_paid_value()

    def tag_value(self):
        return f'{self.value} {CURRENCY}'

    def tag_is_paid(self):
        return 'Πληρωμενο' if self.is_paid else 'Μη Πληρωμενο'

    def filters_data(request, qs):
        date_start, date_end, date_range = initial_date(request, 6)
        paid_name = request.GET.getlist('paid_name', None)
        qs = qs.filter(is_paid=True) if 'have_' in paid_name else qs.filter(
            is_paid=False) if 'not_' in paid_name else qs
        if date_start and date_end:
            qs = qs.filter(date__range=[date_start, date_end])
        return qs

    # for reports

    @property
    def report_date(self):
        return self.date

    def get_edit_url(self):
        return reverse('warehouse:payment_update', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('warehouse:payment_delete', kwargs={'pk': self.id})

    def report_expense_type(self):
        return f'Πληρωμη-{self.vendor}'

    def report_value(self):
        return self.value

    def tag_order_type(self):
        return 'Πληρωμη'

    def tag_final_value(self):
        return f'{self.value} {CURRENCY}'

    def taxes_value(self):
        return '-'


class Note(models.Model):
    status = models.BooleanField(default=True, verbose_name='Κατάσταση')
    vendor_related = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='notes')
    date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200, blank=True, null=True)
    text = HTMLField(blank=True)

    def __str__(self):
        return f'{self.title}' if self.title else 'Σημειωση'


@receiver(post_delete, sender=Payment)
def update_vendor_on_delete(sender, instance, **kwargs):
    instance.vendor.update_paid_value()


@receiver(post_delete, sender=Invoice)
def update_vendor_invoice_on_delete(sender, instance, **kwargs):
    instance.vendor.update_value()


@receiver(post_delete, sender=InvoiceItem)
def update_anything_on_order_item_delete(sender, instance, **kwargs):
    instance.invoice.save()
    if instance.storage:
        instance.storage.save()
    else:
        instance.product.save()
