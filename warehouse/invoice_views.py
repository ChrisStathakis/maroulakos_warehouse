from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, HttpResponseRedirect


from .models import Vendor, InvoiceItem
from .tables import InvoiceItemTable

from django_tables2 import RequestConfig




@method_decorator(staff_member_required, name='dispatch')
class InvoiceItemListView(ListView):
    template_name = 'warehouse/list_view.html'
    model = InvoiceItem
    paginate_by = 100

    def get_queryset(self):
        return self.model.filters_data(self.request, self.model.objects.all())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        date_filter, vendor_filter = [True] * 2
        vendors = Vendor.filters_data(self.request, Vendor.objects.filter(id__in=self.object_list.values_list('vendor__id')))
        queryset_table = InvoiceItemTable(self.object_list)
        RequestConfig(self.request, paginate={'per_page': self.paginate_by}).configure(queryset_table)
        context.update(locals())
        return context


@staff_member_required
def order_item_locked_view(request, pk):
    instance = get_object_or_404(InvoiceItem, id=pk)
    instance.locked = True if not instance.locked else False
    instance.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
