from django.db import models
from django.db.models import Sum, Q
from django.urls import reverse
from django.utils import timezone
from django.conf import settings

import datetime
from decimal import Decimal

CURRENCY = settings.CURRENCY


class OffsShoreCompany(models.Model):
    title = models.CharField(unique=True, max_length=200)
    afm = models.CharField(unique=True, max_length=200)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('offshore:company_update', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('offshore:company_delete', kwargs={'pk': self.id})


class OffsShoreCostumer(models.Model):
    title = models.CharField(null=True, max_length=240, verbose_name='Επωνυμια')

    address = models.CharField(blank=True, null=True, max_length=240, verbose_name='Διευθυνση')
    job_description = models.CharField(blank=True, null=True, max_length=240, verbose_name='Επαγγελμα')
    loading_place = models.CharField(blank=True, null=True, max_length=240, default='Εδρα μας',
                                     verbose_name='Τοπος Φορτωσης')
    destination = models.CharField(blank=True, null=True, max_length=240, default='Εδρα του,',
                                   verbose_name='Προορισμος')
    afm = models.CharField(blank=True, null=True, max_length=10, verbose_name='ΑΦΜ')
    doy = models.CharField(blank=True, null=True, max_length=240, default='Σπαρτη', verbose_name='ΔΟΥ')
    destination_city = models.CharField(blank=True, null=True, max_length=240, verbose_name='Πολη')
    transport = models.CharField(blank=True, null=True, max_length=10, verbose_name='Μεταφορικο Μεσο')

    first_name = models.CharField(max_length=200, verbose_name='Ονομα', blank=True)
    last_name = models.CharField(max_length=200, verbose_name='Επιθετο', blank=True)
    notes = models.CharField(max_length=200, blank=True, verbose_name='Σημειώσεις')
    cellphone = models.CharField(max_length=20, blank=True, verbose_name='Κινητό')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Τηλέφωνο')
    active = models.BooleanField(default=True, verbose_name='Ενεργός')

    class Meta:
        ordering = ['title', 'afm']

    def save(self, *args, **kwargs):
        self.first_name = self.first_name.capitalize()
        self.last_name = self.last_name.capitalize()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_edit_url(self):
        return reverse('costumer_detail', kwargs={'pk': self.id})

    def get_order_url(self):
        return reverse('create_order_costumer_view', kwargs={'pk': self.id})

    def get_payment_url(self):
        return reverse('create_payment_costumer_view', kwargs={'pk': self.id})

    def get_quick_view_url(self):
        return reverse('costumer_quick_view', kwargs={'pk': self.id})

    @staticmethod
    def filters_data(request, queryset):
        q = request.GET.get('q', None)
        balance_name = request.GET.get('balance_name', None)
        status_name = request.GET.get('active_name', None)
        queryset = queryset.filter(active=True) if status_name else queryset
        queryset = queryset.filter(balance__gt=Decimal('0.00')) if balance_name else queryset
        queryset = queryset.filter(Q(first_name__startswith=q.capitalize()) |
                                   Q(last_name__startswith=q.capitalize()) |
                                   Q(eponimia__icontains=q) |
                                   Q(amka__icontains=q) |
                                   Q(afm__icontains=q) |
                                   Q(cellphone__icontains=q) |
                                   Q(phone__icontains=q)
                                   ).distinct() if q else queryset
        return queryset


class OffsShoreCompanyCostumer(models.Model):
    company = models.ForeignKey(OffsShoreCompany, on_delete=models.CASCADE)
    costumer = models.ForeignKey(OffsShoreCostumer, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=30, decimal_places=2, default=0, verbose_name='Υπόλοιπο')
    
    def save(self, *args, **kwargs):
        orders, payments = self.orders.all(), self.payments.all()
        add = orders.aggregate(Sum('value'))['value__sum'] if orders.exists() else 0
        minus = payments.aggregate(Sum('value'))['value__sum'] if payments.exists() else 0 
        self.balance = add - minus
        super(OffsShoreCompanyCostumer, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.costumer} | {self.company}'

    def get_absolute_url(self):
        return reverse('offshore:costumer_company_card', kwargs={'pk': self.id})

    def get_edit_url(self):
        return self.get_absolute_url()

    def get_order_url(self):
        return reverse('offshore:create_order', kwargs={'pk': self.id})

    def get_payment_url(self):
        return reverse('offshore:create_payment_costumer_view', kwargs={'pk': self.id})

    def get_quick_view_url(self):
        return reverse('offshore:costumer_quick_view', kwargs={'pk': self.id})

    def tag_balance(self):
        return f'{self.balance} {CURRENCY}'


class OffshoreOrder(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(OffsShoreCompanyCostumer, on_delete=models.CASCADE, related_name='orders', verbose_name='Πελάτης')
    date = models.DateField(verbose_name='Ημερομηνία')
    title = models.CharField(max_length=200, blank=True, verbose_name='Τίτλος')
    description = models.TextField(blank=True, verbose_name='Περιγραφή')
    value = models.DecimalField(decimal_places=2, max_digits=20, default=0.00, verbose_name='Ποσό')

    class Meta:
        ordering = ['-date']
        
    def __str__(self):
        return f'{self.customer} - {self.title}'

    def save(self, *args, **kwargs):
        if self.id:
            self.title = f'Παραστατικο {self.id}' if len(self.title) == 0 else self.title
        super().save(*args, **kwargs)
        self.customer.save()

    def tag_value(self):
        return f'{self.value} {CURRENCY}'

    def get_absolute_url(self):
        return reverse('offshore:update_payment', kwargs={'pk': self.id})

    def get_edit_url(self):
        return self.get_absolute_url()

    def get_delete_url(self):
        return reverse('offshore:delete_order', kwargs={'pk': self.id})

    def tag_movement(self):
        return 'Τιμολόγιο'

    def tag_print_value(self):
        return self.tag_value()

    @staticmethod
    def filters_data(request, qs):
        q = request.GET.get('q', None)
        if q:
            qs = qs.filter(Q(customer__first_name__icontains=q) |
                           Q(customer__last_name__icontains=q) |
                           Q(customer__amka__icontains=q) |
                           Q(customer__cellphone__icontains=q) |
                           Q(customer__phone__icontains=q)
                           ).distinct()
        date_range = request.GET.get('daterange', None)
        if date_range:
            date_range = date_range.split('-')
            date_range[0] = date_range[0].replace(' ', '')
            date_range[1] = date_range[1].replace(' ', '')
            try:
                date_start = datetime.datetime.strptime(date_range[0], '%m/%d/%Y')
                date_end = datetime.datetime.strptime(date_range[1], '%m/%d/%Y')
            except:
                date_start = datetime.datetime.now()
                date_end = datetime.datetime.now()

            qs = qs.filter(date__range=[date_start, date_end])
        return qs


class OffshorePayment(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(OffsShoreCompanyCostumer, on_delete=models.CASCADE, related_name='payments', verbose_name='Πελάτης')
    date = models.DateField(verbose_name='Ημερομηνία')
    title = models.CharField(max_length=200, blank=True, verbose_name='Τίτλος')
    description = models.TextField(blank=True, verbose_name='Περιγραφή')
    value = models.DecimalField(decimal_places=2, max_digits=20, default=0.00, verbose_name='Ποσό')

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.id:
            self.title = f'Πληρωμή {self.id}' if len(self.title) == 0 else self.title
        super().save(*args, **kwargs)
        self.customer.save()

    def tag_value(self):
        return f'{self.value} {CURRENCY}'

    def get_absolute_url(self):
        return reverse('offshore:update_payment', kwargs={'pk': self.id})

    def get_edit_url(self):
        return self.get_absolute_url()

    def get_delete_url(self):
        return reverse('offshore:delete_payment', kwargs={'pk': self.id})

    @staticmethod
    def filters_data(request, qs):
        q = request.GET.get('q', None)
        if q:
            qs = qs.filter(Q(customer__first_name__icontains=q) |
                           Q(customer__last_name__icontains=q) |
                           Q(customer__amka__icontains=q) |
                           Q(customer__cellphone__icontains=q) |
                           Q(customer__phone__icontains=q)
                           ).distinct()
        date_range = request.GET.get('daterange', None)
        if date_range:
            date_range = date_range.split('-')
            date_range[0] = date_range[0].replace(' ', '')
            date_range[1] = date_range[1].replace(' ', '')
            try:
                date_start = datetime.datetime.strptime(date_range[0], '%m/%d/%Y')
                date_end = datetime.datetime.strptime(date_range[1], '%m/%d/%Y')
            except:
                date_start = datetime.datetime.now()
                date_end = datetime.datetime.now()

            qs = qs.filter(date__range=[date_start, date_end])
        return qs

    def tag_movement(self):
        return 'Πληρωμή'

    def tag_print_value(self):
        return f'-{self.value} {CURRENCY}'
