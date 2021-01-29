from django.views.generic import ListView, TemplateView, DetailView, CreateView, UpdateView
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import reverse, get_object_or_404, redirect
from django.utils import timezone
from .models import Vendor, Note, VendorBankingAccount, Invoice, Payment
from .warehouse_models import InvoiceTransformation, InvoiceTransformationItem, InvoiceTransformationIngredient

from .forms import (VendorForm, PaymentForm, InvoiceForm, NoteForm, InvoiceVendorDetailForm,
                    InvoiceProductForm, InvoiceTransformationForm, InvoiceTransformationItemForm, EmployerForm
                    )
from catalogue.models import Product, ProductStorage, Category
from .tables import ProductTransTable, VendorTable, InvoiceTable, InvoiceTransformationTable, VendorProductTable
from point_of_sale.models import SalesInvoiceItem, SalesInvoice
from .mixins import ListViewMixin

from django_tables2 import RequestConfig

from decimal import Decimal
from operator import attrgetter
from itertools import chain


@method_decorator(staff_member_required, name='dispatch')
class HomepageView(TemplateView):
    template_name = 'warehouse/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vendors'] = Vendor.objects.filter(balance__gt=0)[:10]
        context['payments'] = Payment.objects.filter(is_paid=False).order_by('date')[:10]
        context['invoices'] = Invoice.objects.all()[:10]
        context['trans'] = InvoiceTransformation.objects.all()[:10]

        return context


@method_decorator(staff_member_required, name='dispatch')
class VendorListView(ListView):
    model = Vendor
    template_name = 'warehouse/list_view.html'
    paginate_by = 25

    def get_queryset(self):
        qs = Vendor.objects.all()
        qs = Vendor.filters_data(self.request, qs)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs_table = VendorTable(self.object_list)
        RequestConfig(self.request, paginate={'per_page': self.paginate_by}).configure(qs_table)
        queryset_table = qs_table
        create_url = reverse('warehouse:vendor_create')
        page_title, back_url = 'Προμηθευτές', reverse('warehouse:homepage')
        # report_button, report_url = True, reverse('vendors:ajax_vendors_balance')
        balance_filter, search_filter = [True] * 2
        context.update(locals())
        return context


@method_decorator(staff_member_required, name='dispatch')
class CreateVendorView(CreateView):
    template_name = 'warehouse/form_view.html'
    model = Vendor
    form_class = VendorForm

    def get_initial(self):
        initial = super().get_initial()
        # initial['site'] = 'http://'
        return initial

    def get_success_url(self):
        return self.new_object.get_edit_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"], context['back_url'], = 'Δημιουργια Προμηθευτη', reverse('warehouse:vendor_list')

        return context

    def form_valid(self, form):
        self.new_object = form.save()
        new_vendor = form.cleaned_data['title']
        messages.success(self.request, f'Ο Προμηθευτής {new_vendor} δημιουργήθηκε.')
        return super().form_valid(form)


@method_decorator(staff_member_required, name='dispatch')
class UpdateVendorView(UpdateView):
    model = Vendor
    template_name = 'warehouse/update_vendor.html'
    form_class = VendorForm

    def get_success_url(self):
        return self.object.get_edit_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['invoice_form'] = InvoiceVendorDetailForm(initial={'vendor': self.object})
        context['payment_form'] = PaymentForm(initial={'vendor': self.object})
        context['employer_form'] = EmployerForm(initial={'vendor': self.object})
        context['page_title'] = f'{self.object.title}'
        context['notes'] = Note.objects.filter(vendor_related=self.object, status=True)
        invoices = Invoice.filters_data(self.request, self.object.invoices.all())
        payments = Payment.filters_data(self.request, self.object.payments.all())
        qs_together = sorted(chain(
            invoices, payments
        ), key=attrgetter('date'))
        context['qs_together'] = qs_together
        # context['action_url'] = reverse('vendors:list')
        return context


@staff_member_required
def delete_vendor_view(request, pk):
    instance = get_object_or_404(Vendor, id=pk)
    instance.delete()
    return redirect(reverse('warehouse:vendor_list'))


@method_decorator(staff_member_required, name='dispatch')
class VendorNotesView(ListView):
    template_name = 'warehouse/NoteContainer.html'
    model = Note

    def get_queryset(self):
        self.vendor = get_object_or_404(Vendor, id=self.kwargs['pk'])
        return self.vendor.notes.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Σημειώσεις {self.vendor}'
        context['back_url'] = self.vendor.get_edit_url()
        context['form'] = NoteForm(initial={'vendor_related': self.vendor})
        context['vendor'] = self.vendor
        return context


@method_decorator(staff_member_required, name='dispatch')
class NoteUpdateView(UpdateView):
    model = Note
    form_class = NoteForm
    template_name = 'warehouse/note_update.html'

    def get_initial(self):
        initial = super().get_initial()
        initial['vendor_related'] = self.object.vendor_related
        return initial

    def get_success_url(self):
        vendor = self.object.vendor_related
        return reverse('warehouse:notes', kwargs={'pk': vendor.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["vendor"] = self.object.vendor_related
        context['back_url'] = self.get_success_url()
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


@staff_member_required
def delete_note_view(request, pk):
    note = get_object_or_404(Note, id=pk)
    note.delete()
    return redirect(reverse('warehouse:notes', kwargs={'pk': note.vendor_related.id}))


@method_decorator(staff_member_required, name='dispatch')
class VendorCardView(ListView):
    model = Product
    template_name = 'warehouse/vendor_card.html'
    paginate_by = 500

    def get_queryset(self):
        self.vendor = vendor = get_object_or_404(Vendor, id=self.kwargs['pk'])
        qs = Product.objects.filter(vendor=vendor)
        qs = Product.filters_data(self.request, qs)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["vendor"] = self.vendor
        context['create_form'] = InvoiceProductForm(initial={'taxes_modifier': self.vendor.taxes_modifier})
        context['search_filter'], context['category_filter'] = [True] * 2

        return context


@method_decorator(staff_member_required, name='dispatch')
class ProductTransformationListView(ListView):
    template_name = 'warehouse/list_view.html'
    model = Product

    def get_queryset(self):
        qs = Product.objects.filter(product_class__have_ingredient=True)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs_table = ProductTransTable(self.object_list)
        context['queryset_table'] = qs_table
        return context


@method_decorator(staff_member_required, name='dispatch')
class InvoiceTransformationListView(ListView):
    template_name = 'warehouse/list_view.html'
    model = InvoiceTransformation


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset_table = InvoiceTransformationTable(self.object_list)
        context['create_url'] = reverse('warehouse:invoice_trans_create')
        context['queryset_table'] = queryset_table
        return context


@method_decorator(staff_member_required, name='dispatch')
class InvoiceTransformationCreateView(CreateView):
    model = InvoiceTransformation
    form_class = InvoiceTransformationForm
    template_name = 'warehouse/form_view.html'

    def get_success_url(self):
        return self.new_product.get_edit_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = 'Δημιουργια Προϊόντος'
        context["back_url"] = reverse('warehouse:invoice_trans_list')
        return context

    def form_valid(self, form):
        self.new_product = form.save()
        return super().form_valid(form)


@method_decorator(staff_member_required, name='dispatch')
class InvoiceTransformationDetailView(UpdateView):
    template_name = 'warehouse/transfo_detail.html'
    model = InvoiceTransformation
    form_class = InvoiceTransformationForm

    def get_success_url(self):
        return self.object.get_edit_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.filter(product_class__have_ingredient=True)[:10]
        context["back_url"] = reverse('warehouse:invoice_trans_list')
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


@staff_member_required()
def delete_invoice_transformation_view(request, pk):
    obj = get_object_or_404(InvoiceTransformation, id=pk)
    # need heklp


@method_decorator(staff_member_required, name='dispatch')
class InvoiceItemTransformationUpdateView(UpdateView):
    model = InvoiceTransformationItem
    form_class = InvoiceTransformationItemForm
    template_name = 'warehouse/product_ingridient_form.html'

    def get_success_url(self):
        return self.object.invoice.get_edit_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = f'Παραστατικο ==> {self.object}'
        context['trans_info'] = True
        context['back_url'] = self.get_success_url()
        context['sale_invoices'] = self.object.sale_items.all()
        return context

    def form_valid(self, form):
        data = form.save()
        for item in self.object.transf_ingre.all():
            item.qty = data.qty*item.qty_ratio
            item.save()
        messages.success(self.request, 'Επιτυχής επεξεργασία')
        return super().form_valid(form)


@method_decorator(staff_member_required, name='dispatch')
class ProductTransformationPrepareView(DetailView):
    model = Product
    template_name = 'warehouse/prepare_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        max_per_ind = []
        for ele in self.object.ingredients.all():
            max_per_ind.append(ele.ingredient.qty/ele.qty if ele.qty != 0 else 0)
        context['max_items'] = min(max_per_ind)
        context['create_form'] = InvoiceTransformationForm()
        context['invoices'] = InvoiceTransformation.objects.filter(locked=False)
        return context

    def post(self, request, *args, **kwargs):
        form = InvoiceTransformationForm(request.POST or None)
        my_product = get_object_or_404(Product, id=self.kwargs['pk'])
        qty = Decimal(request.POST.get('qty', 0))
        if form.is_valid():
            new_invoice = form.save()
        else:
            new_invoice = get_object_or_404(InvoiceTransformation, id=request.POST.get('edit_form', None))
        new_item = InvoiceTransformationItem.create_from_view(new_invoice, my_product, qty)
        ids, storages_ids = [], []
        for ele in request.POST:
            if str(ele).startswith('product_'):
                product, id = ele.split('_')
                ids.append([id, request.POST.get(ele)])
            if str(ele).startswith('storage_'):
                storage, id = ele.split('_')
                storages_ids.append([id, request.POST.get(ele)])
        for id_list in ids:
            InvoiceTransformationIngredient.create_from_view(id_list, storages_ids, new_item, qty)

        return self.render_to_response(context={'object': my_product})
    

@method_decorator(staff_member_required, name='dispatch')
class InvoiceListView(ListView):
    model = Invoice
    template_name = 'warehouse/list_view.html'
    paginate_by = 25

    def get_queryset(self):
        qs = Invoice.objects.all()
        qs = Invoice.filters_data(self.request, qs)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs_table = InvoiceTable(self.object_list)
        RequestConfig(self.request, paginate={'per_page': self.paginate_by}).configure(qs_table)
        queryset_table = qs_table
        create_url = reverse('warehouse:invoice_create')
        page_title, back_url = 'Προμηθευτές', reverse('warehouse:homepage')
        # report_button, report_url = True, reverse('vendors:ajax_vendors_balance')
        vendors = Vendor.objects.filter(active=True)
        vendor_filter, search_filter, date_filter = [True] * 3
        context.update(locals())
        return context


@method_decorator(staff_member_required, name='dispatch')
class CreateInvoiceView(CreateView):
    template_name = 'warehouse/form_view.html'
    model = Invoice
    form_class = InvoiceForm

    def get_initial(self):
        initial = super().get_initial()
        # initial['site'] = 'http://'
        return initial

    def get_success_url(self):
        return self.new_object.get_edit_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"], context['back_url'], = 'Δημιουργια Προμηθευτη', reverse('warehouse:invoice_list')
        context['popup'] = True
        return context

    def form_valid(self, form):
        self.new_object = form.save()
        new_vendor = form.cleaned_data['title']
        messages.success(self.request, f'Το Παραστατικο {new_vendor} δημιουργήθηκε.')
        return super().form_valid(form)


@method_decorator(staff_member_required, name='dispatch')
class InvoiceDetailView(UpdateView):
    model = Invoice
    template_name = 'warehouse/invoice_detail.html'
    form_class = InvoiceForm

    def get_success_url(self):
        return self.object.get_edit_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.filter(vendor=self.object.vendor)
        context['product_form'] = InvoiceProductForm(initial={'vendor': self.object.vendor})
        context['order_items'] = self.object.order_items.all()
        products = Product.objects.filter(vendor=self.object.vendor)
        q = self.request.GET.get('q', None)
        if q:
            products = Product.filters_data(self.request, products)
        context['products'] = products
        context['page_title'] = f'{self.object.get_order_type_display()} - {self.object.title}'
        return context


@staff_member_required
def delete_invoice_view(request, pk):
    instance = get_object_or_404(Invoice, id=pk)
    instance.delete()
    return redirect(reverse('warehouse:invoice_list'))


@staff_member_required()
def create_sale_invoice_transformation_view(request, pk):
    instance = get_object_or_404(InvoiceTransformation, id=pk)
    instance.locked = True
    instance.save()
    '''
    sale_invoice = SalesInvoice.objects.create(
        costumer=instance.costumer,
        order_type='a',
        payment_method=instance.payment_method,
        date=timezone.now(),
        title=instance.title
    )
    for item in instance.invoicetransformationitem_set.all():
        SalesInvoiceItem.objects.create(
            invoice=sale_invoice,
            product=item.product,
            qty=item.qty,
            value=item.value,
            storage=item.storage,
            costumer=instance.costumer
        )
    '''
    return redirect(instance.get_edit_url())
