from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import reverse, get_object_or_404, redirect
from django.utils import timezone
from .models import Vendor, Note, VendorBankingAccount, Invoice, Payment
from .warehouse_models import InvoiceTransformation, InvoiceTransformationItem, InvoiceTransformationIngredient

from .forms import PaymentForm, PaymentCreateForm
from .models import Vendor, InvoiceItem
from .tables import InvoiceItemTable
from point_of_sale.models import SalesInvoiceItem, SalesInvoice
from .mixins import ListViewMixin

from django_tables2 import RequestConfig

from decimal import Decimal
from operator import attrgetter
from itertools import chain


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
        
        queryset_table = InvoiceItemTable(self.object_list)
        context.update(locals())
        return context