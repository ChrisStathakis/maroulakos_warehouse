import django_tables2 as tables

from .models import PaymentInvoice

from costumers.models import Costumer


class CostumerTable(tables.Table):
    action = tables.TemplateColumn(
        "<a href='{{ record.get_edit_url }}' class='btn btn-primary btn-round'><i class='fa fa-edit'></i></a>",
        orderable=False, verbose_name='Καρτέλα'
    )
    tag_balance = tables.Column(orderable=False, verbose_name='Υπολοιπο')

    class Meta:
        model = Costumer
        template_name = 'django_tables2/bootstrap.html'
        fields = ['eponimia', 'amka', 'afm', 'tag_balance',  'action']


class PaymentInvoiceTable(tables.Table):
    button = tables.TemplateColumn("<a href='{{ record.get_edit_url }}' "
                                   "class='btn btn-info'><i class='fa fa-edit'></i></a>",
                                   orderable=False, verbose_name='Επιλογες'
                                   )

    tag_total_value = tables.Column(orderable=False, verbose_name='Τελικη Αξια')

    class Meta:
        model = PaymentInvoice
        template_name = 'django_tables2/bootstrap.html'
        fields = ['date', '__str__', 'order_type', 'costumer', 'tag_total_value']

