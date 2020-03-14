import django_tables2 as tables

from .models import Storage, PaymentMethod


class StorageTable(tables.Table):
    title = tables.TemplateColumn('<a href="{{ record.get_edit_url }}"> {{ record }}</a>')

    class Meta:
        model = Storage
        template_name = 'django_tables2/bootstrap.html'
        fields = ['title', 'capacity', 'active']


class PaymentMethodTable(tables.Table):
    title = tables.TemplateColumn('<a href="{{ record.get_edit_url }}"> {{ record }}</a>')

    class Meta:
        model = PaymentMethod
        template_name = 'django_tables2/bootstrap.html'
        fields = ['title', ]
