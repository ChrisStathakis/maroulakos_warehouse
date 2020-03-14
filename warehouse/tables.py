import django_tables2 as tables

from catalogue.models import Product
from .models import Vendor, Invoice


class ProductTransTable(tables.Table):
    title = tables.TemplateColumn("<a href='{{ record.get_prepare_url }}'> {{ record }} </a>")

    class Meta:
        model = Product
        template_name = 'django_tables2/bootstrap.html'
        fields = ['title', ]


class VendorTable(tables.Table):
    title = tables.TemplateColumn("<a href='{{ record.get_edit_url}}'>{{ record }}</a>",
            orderable=False, verbose_name='-')

    class Meta:
        model = Vendor
        template_name = 'django_tables2/bootstrap.html'
        fields = ['title', 'afm', 'phone',  'email', 'balance']


class InvoiceTable(tables.Table):
    title = tables.TemplateColumn("<a href='{{ record.get_edit_url}}'>{{ record }}</a>",
            orderable=False, verbose_name='-')


    class Meta:
        model = Invoice
        template_name = 'django_tables2/bootstrap.html'
        fields = ['date', 'title', 'vendor',  'order_type', 'final_value']