from django.views.generic import ListView, TemplateView, DetailView, CreateView, UpdateView
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import reverse, get_object_or_404, redirect
from django.utils import timezone
from .models import Vendor, Note, VendorBankingAccount, Invoice, Payment
from .warehouse_models import InvoiceTransformation, InvoiceTransformationItem, InvoiceTransformationIngredient

from .forms import PaymentForm, PaymentCreateForm
from .models import Payment
from .tables import PaymentTable
from point_of_sale.models import SalesInvoiceItem, SalesInvoice
from .mixins import ListViewMixin

from django_tables2 import RequestConfig

from decimal import Decimal
from operator import attrgetter
from itertools import chain


@method_decorator(staff_member_required, name='dispatch')
class PaymentListView(ListView):
    model = Payment
    template_name = 'warehouse/list_view.html'

    def get_queryset(self):
        return self.model.filters_data(self.request, self.model.objects.all())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse('warehouse:payment_create')
        context['page_title'] = 'Πληρωμες Προμηθευτών'
        context['search_filter'], context['vendor_filter'], context['date_filter'] = [True] *3
        context['back_url'] = reverse('warehouse:homepage')
        qs_table = PaymentTable(self.object_list)

        context['queryset_table'] = qs_table
        return context


@method_decorator(staff_member_required, name='dispatch')
class PaymentCreateView(CreateView):
    model = Payment
    template_name = 'warehouse/form_view.html'
    form_class = PaymentCreateForm
    success_url = reverse_lazy('warehouse:payment_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Δημιουργια Πληρωμης'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Η πληρωμη Δημιουργηθηκε')
        return super().form_valid(form)


@method_decorator(staff_member_required, name='dispatch')
class PaymentUpdateView(UpdateView):
    model = Payment
    template_name = 'warehouse/form_view.html'
    form_class = PaymentForm
    success_url = reverse_lazy('warehouse:payment_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = f'Επεξεργασια {self.object}'
        context['back_url'] = self.success_url
        context['delete_url'] = self.object.get_delete_url()
        return context

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Η Πληρωμη επεξεργαστηκε')
        return super().form_valid(form)


@staff_member_required
def payment_delete_view(request, pk):
    instance = get_object_or_404(Payment, id=pk)
    instance.delete()
    messages.warning(request, 'Η πληρωμη διαγραφηκε')
    return redirect('warehouse:payment_list')