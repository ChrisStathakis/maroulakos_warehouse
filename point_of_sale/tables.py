import django_tables2 as tables


from .models import SalesInvoice, SalesInvoiceItem


class SalesInvoiceTable(tables.Table):

    class Meta:
        model = SalesInvoice
        template_name = 'django_tables2/bootstrap.html'
        fields = ['date', 'title', 'order_type', 'costumer']


class SalesInvoiceItemTable(tables.Table):
    class Meta:
        model = SalesInvoice
        template_name = 'django_tables2/bootstrap.html'
        fields = ['date', 'product', 'invoice', 'costumer']


class SalesInvoiceListTable(tables.Table):
    title = tables.TemplateColumn("<a href={{ record.get_edit_url }}'>{{ record.title }}</a>")


    class Meta:
        model = SalesInvoice
        template_name = 'django_tables2/bootstrap.html'
        fields = ['date', 'order_title', 'order_type', 'costumer', 'final_value']

