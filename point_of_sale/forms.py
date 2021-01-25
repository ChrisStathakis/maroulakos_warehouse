from django import forms

from .models import SalesInvoice, SalesInvoiceItem, Costumer, ProductStorage
from catalogue.models import Product
from project_settings.forms import BaseForm

from dal import autocomplete


class SalesInvoiceForm(BaseForm, forms.ModelForm):
    date = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}), label='Ημερομηνια')
    costumer = forms.ModelChoiceField(queryset=Costumer.objects.all(),
                                      widget=autocomplete.ModelSelect2(url='point_of_sale:autocomplete_costumer'),
                                      label='Πελατης'
                                      )

    class Meta:
        model = SalesInvoice
        fields = ['date', 'lot', 'order_type', 'title', 'costumer', 'payment_method', 'extra_value',
                'description']


class SaleInvoiceItemForm(BaseForm, forms.ModelForm):
    product = forms.ModelChoiceField(queryset=Product.objects.all(), widget=forms.HiddenInput())
    invoice = forms.ModelChoiceField(queryset=SalesInvoice.objects.all(), widget=forms.HiddenInput())
    costumer = forms.ModelChoiceField(queryset=Costumer.objects.all(), widget=forms.HiddenInput())
    storage = forms.ModelChoiceField(queryset=ProductStorage.objects.all(), widget=forms.HiddenInput(), required=False)

    class Meta:
        model = SalesInvoiceItem
        fields = ['product', 'invoice', 'order_code', 'unit', 'qty',
                  'value', 'taxes_modifier', 'costumer', 'storage'
                  ]



