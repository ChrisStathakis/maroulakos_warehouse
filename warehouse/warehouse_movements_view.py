from django.views.generic import ListView, TemplateView, DetailView, CreateView, UpdateView
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import reverse, get_object_or_404, redirect
from django.utils import timezone
from .warehouse_models import WarehouseMovementsInvoice, WarehouseMovementInvoiceItem


from .forms import (WarehouseMovementInvoiceForm, WarehouseMovementInvoiceItemForm)
from catalogue.models import Product, ProductStorage, Category
from .tables import WarehouseMovementsInvoiceTable
from point_of_sale.models import SalesInvoiceItem, SalesInvoice
from .mixins import ListViewMixin

from django_tables2 import RequestConfig

from decimal import Decimal

@method_decorator(staff_member_required, name='dispatch')
class WarehouseMovementsInvoiceListView(ListView):
    model = WarehouseMovementsInvoice
    template_name = 'warehouse/list_view.html'
    paginate_by = 25

    def get_queryset(self):
        return self.model.filters_data(self.request, self.model.objects.all())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs_table = WarehouseMovementsInvoiceTable(self.object_list)
        RequestConfig(self.request, paginate={'per_page': self.paginate_by}).configure(qs_table)
        queryset_table = qs_table
        create_url = reverse('warehouse:ware_move_create')
        page_title, back_url = 'Κινησεις Αποθηκης', reverse('warehouse:ware_move_list')
        date_filter, search_filter = [True] * 2
        context.update(locals())
        return context


@method_decorator(staff_member_required, name='dispatch')
class CreateWarehouseMovementsInvoiceView(CreateView):
    template_name = 'warehouse/form_view.html'
    model = WarehouseMovementsInvoice
    form_class = WarehouseMovementInvoiceForm

    def get_success_url(self):
        return self.new_object.get_edit_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"], context['back_url'], = 'Δημιουργια Κινησης', reverse('warehouse:ware_move_list')
        return context

    def form_valid(self, form):
        self.new_object = form.save()
        new_vendor = form.cleaned_data['title']
        messages.success(self.request, f'Ο Προμηθευτής {new_vendor} δημιουργήθηκε.')
        return super().form_valid(form)


@method_decorator(staff_member_required, name='dispatch')
class WarehouseMovementsInvoiceUpdateView(UpdateView):
    model = WarehouseMovementsInvoice
    template_name = 'warehouse/include/warehouse_movement_update.html'
    form_class = WarehouseMovementInvoiceForm

    def get_success_url(self):
        return self.object.get_edit_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all().filter(product_class__is_service=False)[:15]
        return context


@staff_member_required
def delete_warehouse_movements_invoice_view(request, pk):
    instance = get_object_or_404(WarehouseMovementsInvoice, id=pk)
    instance.delete()
    return redirect(reverse('warehouse:vendor_list'))


@staff_member_required
def validate_add_products_view(request, pk):
    instance = get_object_or_404(WarehouseMovementsInvoice, id=pk)
    for ele in request.POST:
        if 'add_id' in ele:
            id = ele.split('id_')[1]
            product = get_object_or_404(Product, id=id)
            qty = request.POST.get(f'qty_{id}',0)
            qty = Decimal(qty)
            if product.product_class.have_storage:
                storage = product.favorite_storage()
                if storage:
                    new_item = WarehouseMovementInvoiceItem.objects.create(
                        product=product,
                        invoice=instance,
                        qty=qty,
                        storage=storage
                    )
                else:
                    messages.warning(request, f'Το Προϊον {product} δε εχει αγαπημενη αποθηκη.')
            else:
                new_item = WarehouseMovementInvoiceItem.objects.create(
                    product=product,
                    invoice=instance,
                    qty=qty,
                )
    return redirect(instance.get_edit_url())


@staff_member_required
def delete_ware_move_item(request, pk):
    instance = get_object_or_404(WarehouseMovementInvoiceItem, id=pk)
    instance.delete()
    return redirect(instance.invoice.get_edit_url())