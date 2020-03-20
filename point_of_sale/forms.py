from django import forms

from .models import SalesInvoice, SalesInvoiceItem

from project_settings.forms import BaseForm


class SalesInvoiceForm(BaseForm, forms.ModelForm):
    date = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = SalesInvoice
        fields = ['date', 'order_type', 'title', 'costumer', 'payment_method', 'extra_value',
                'description']