from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import reverse, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, CreateView, UpdateView

from .forms import SalesInvoiceForm
from .models import SalesInvoice, SalesInvoiceItem
from .tables import SalesInvoiceItemTable, SalesInvoiceTable, SalesInvoiceListTable
from catalogue.models import Product
from django_tables2 import RequestConfig


@method_decorator(staff_member_required, name='dispatch')
class PointOfSaleHomepageView(TemplateView):
    template_name = 'point_of_sale/homepage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['invoices'] = SalesInvoiceTable(SalesInvoice.objects.all()[:10])
        context['order_items'] = SalesInvoiceItemTable(SalesInvoiceItem.objects.all()[:10])
        return context


@method_decorator(staff_member_required, name='dispatch')
class SalesListView(ListView):
    template_name = 'point_of_sale/list_view.html'
    model = SalesInvoice
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Πωλησεις'
        context['create_url'] = reverse('point_of_sale:sales_create')
        context['back_url'] = reverse('point_of_sale:homepage')
        qs_table = SalesInvoiceListTable(self.object_list)
        RequestConfig(self.request).configure(qs_table)
        context['queryset_table'] = qs_table
        return context


@method_decorator(staff_member_required, name='dispatch')
class SalesCreateView(CreateView):
    template_name = 'point_of_sale/form_view.html'
    model = SalesInvoice
    form_class = SalesInvoiceForm
    success_url = reverse_lazy('point_of_sale:sales_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Νεα Πωληση'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        self.invoice = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return self.invoice.get_edit_url()


@method_decorator(staff_member_required, name='dispatch')
class SalesUpdateView(UpdateView):
    model = SalesInvoice
    form_class = SalesInvoiceForm
    template_name = 'point_of_sale/update_view.html'
    success_url = reverse_lazy('point_of_sale:sales_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = ''
        context['back_url'] = self.success_url
        context['products'] = Product.objects.filter(active=True)
        return context

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Το Παραστατικο Πωλήσης Επεξεργαστηκε!')
        return super().form_valid(form)


@staff_member_required
def delete_sales_invoice_view(request, pk):
    instance = get_object_or_404(SalesInvoice, id=pk)
    instance.delete()
    return redirect(reverse(''))
