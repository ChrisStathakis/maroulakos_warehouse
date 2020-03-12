from django.views.generic.list import MultipleObjectMixin
from django_tables2 import RequestConfig


class ListViewMixin(MultipleObjectMixin):
    paginate_by = 50
    template_name = 'catalogue/list_view.html'

    def get_queryset(self):
        qs = self.model.my_query.active_for_site()
        qs = self.model.filters_data(self.request, qs)
        return qs

    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        qs_table = self.queryset_table(self.object_list)
        RequestConfig.request(self.request, {'per_page': self.paginate_by}).configure(qs_table)
        context['queryset_table'] = qs_table

        return context
