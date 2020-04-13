import django_tables2 as tables

from catalogue.models import Product
from .models import Vendor, Invoice, Payment
from .warehouse_models import InvoiceTransformation, WarehouseMovementsInvoice


class ProductTransTable(tables.Table):
    title = tables.TemplateColumn("<a href='{{ record.get_prepare_url }}'> {{ record }} </a>")

    class Meta:
        model = Product
        template_name = 'django_tables2/bootstrap.html'
        fields = ['title', ]


class VendorProductTable(tables.Table):

    class Meta:
        model = Product
        fields = ['order_sku', 'title', 'price_buy', 'order_discount', 'taxes_modifier', 'qty']


class VendorTable(tables.Table):
    title = tables.TemplateColumn("<a href='{{ record.get_edit_url}}'>{{ record }}</a>",
            orderable=False, verbose_name='-')

    class Meta:
        model = Vendor
        template_name = 'django_tables2/bootstrap.html'
        fields = ['title', 'afm', 'phone',  'email', 'balance']


class InvoiceTable(tables.Table):
    title = tables.TemplateColumn("<a href='{{ record.get_edit_url}}'>{{ record }}</a>",
             verbose_name='Κωδικος Τιμ.')
    order_type = tables.Column(verbose_name='Ειδος')
    date = tables.TemplateColumn("<p>{{ record.date|date:'d/M/Y'}} </p>")

    class Meta:
        model = Invoice
        template_name = 'django_tables2/bootstrap.html'
        fields = ['date', 'title', 'vendor',  'order_type', 'value','final_value']


class InvoiceTransformationTable(tables.Table):
    title = tables.TemplateColumn("<a href='{{ record.get_edit_url}}'>{{ record }}</a>",
                                  orderable=False, verbose_name='Επεξηγηση')
    date = tables.TemplateColumn("<p>{{ record.date|date:'d/M/Y'}} </p>")


    class Meta:
        model = InvoiceTransformation
        template_name = 'django_tables2/bootstrap.html'
        fields = ['date', 'title', 'costumer', 'value', 'locked']


class PaymentTable(tables.Table):
    title = tables.TemplateColumn("<a href='{{ record.get_edit_url}}'>{{ record }}</a>",
                                  orderable=False, verbose_name='Επεξηγηση')
    date = tables.TemplateColumn("<p>{{ record.date|date:'d/M/Y'}} </p>")

    class Meta:
        model = Payment
        template_name = 'django_tables2/bootstrap.html'
        fields = ['date', 'title', 'vendor', 'value', 'is_paid']


class WarehouseMovementsInvoiceTable(tables.Table):
    date = tables.TemplateColumn("<p>{{ record.date|date:'d/M/Y'}} </p>", verbose_name='Ημερομηνια')
    button = tables.TemplateColumn("<a class='btn btn-primary' href='{{ record.get_edit_url}}'><i class='fa fa-edit'></i>", verbose_name='-')

    class Meta:
        model = InvoiceTransformation
        template_name = 'django_tables2/bootstrap.html'
        fields = ['date', 'title', 'order_type','button']