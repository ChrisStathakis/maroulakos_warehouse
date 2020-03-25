from django import forms

from .models import SalesInvoice, SalesInvoiceItem, Costumer
from catalogue.models import Product
from project_settings.forms import BaseForm


class SalesInvoiceForm(BaseForm, forms.ModelForm):
    date = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = SalesInvoice
        fields = ['date', 'order_type', 'title', 'costumer', 'payment_method', 'extra_value',
                'description']


class SaleInvoiceItemForm(BaseForm, forms.ModelForm):
    product = forms.ModelChoiceField(queryset=Product.objects.all(), widget=forms.HiddenInput())
    invoice = forms.ModelChoiceField(queryset=SalesInvoice.objects.all(), widget=forms.HiddenInput())
    costumer = forms.ModelChoiceField(queryset=Costumer.objects.all(), widget=forms.HiddenInput())

    class Meta:
        model = SalesInvoiceItem
        fields = ['product', 'invoice', 'order_code', 'unit', 'qty',
                  'value', 'discount', 'taxes_modifier', 'storage', 'costumer'
                  ]



