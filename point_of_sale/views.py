from django.shortcuts import render
from django.db.models import Sum
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import reverse, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, CreateView, UpdateView
from django import forms
from .forms import SalesInvoiceForm
from .models import SalesInvoice, SalesInvoiceItem
from .tables import SalesInvoiceItemTable, SalesInvoiceTable, SalesInvoiceListTable
from costumers.models import Costumer
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

    def get_queryset(self):
        qs = SalesInvoice.objects.all()
        qs = SalesInvoice.filters_data(self.request, qs)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['costumers'] = Costumer.objects.filter(active=True)
        context['page_title'] = 'Πωλησεις'
        context['create_url'] = reverse('point_of_sale:sales_create')
        context['back_url'] = reverse('point_of_sale:homepage')
        context['date_filter'], context['search_filter'], context['costumer_filter'], context['payment_filter'] = [True] * 4
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
        context['popup'] = True

        return context

    def form_valid(self, form):
        self.invoice = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return self.invoice.get_edit_url()


@staff_member_required
def update_sale_invoice_view(request, pk):
    instance = get_object_or_404(SalesInvoice, id=pk)
    form = SalesInvoiceForm(request.POST or None, instance=instance)
    form.fields['costumer'].widget = forms.HiddenInput()
    if form.is_valid():
        form.save()
        return redirect(instance.get_edit_url())

    back_url = instance.get_edit_url()
    products = Product.filters_data(request, Product.objects.filter(active=True))[:10]
    return render(request, 'point_of_sale/update_view.html', context={'form': form,
                                                                      'object': instance,
                                                                      'products': products,
                                                                      'back_url': back_url
                                                                    })


@staff_member_required
def delete_sales_invoice_view(request, pk):
    instance = get_object_or_404(SalesInvoice, id=pk)
    instance.delete()
    messages.success(request, 'Το Παραστατικο Διαγραφηκε!.')
    return redirect(reverse('point_of_sale:sales_list'))


@staff_member_required
def order_items_analysis_view(request):
    date_filter = True
    order_items = SalesInvoiceItem.filter_data(request, SalesInvoiceItem.objects.all())
    costumers_id = order_items.values_list('costumer')
    costumers = Costumer.objects.filter(id__in=costumers_id)
    sells_per_costumer = order_items.values('costumer__eponimia').annotate(total_value=Sum('total_value'), total_qty=Sum('qty')).order_by('qty')
    sells_per_product = order_items.values('product__title').annotate(total_value=Sum('total_value'),
                                                                        total_qty=Sum('qty')).order_by('qty')
    context = locals()
    return render(request, 'point_of_sale/order_item_analysis.html', context)