import django_tables2 as tables

from .models import Storage


class StorageTable(tables.Table):
    title = tables.TemplateColumn('<a href="{{ record.get_edit_url }}"> {{ record }}</a>')

    class Meta:
        model = Storage
        fields = ['title', 'capacity']
