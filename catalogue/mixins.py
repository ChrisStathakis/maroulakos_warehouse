from django.views.generic.list import MultipleObjectMixin
from django_tables2 import RequestConfig


class ListViewMixin(MultipleObjectMixin):
    paginate_by = 50
    template_name = 'catalogue/list_view.html'

    def get_queryset(self):
        qs = self.model.objects.all()
        qs = self.model.filters_data(self.request, qs)
        return qs

