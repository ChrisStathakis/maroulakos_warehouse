from django.shortcuts import render, reverse, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, TemplateView
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Sum, Count
from operator import attrgetter
from itertools import chain

from .models import PaymentInvoice, MyCard, Costumer, CostumerPayment
from point_of_sale.models import SalesInvoice, SalesInvoiceItem
from .tables import PaymentInvoiceTable, CostumerTable
from .forms import PaymentInvoiceForm, CostumerDetailsForm, CreateInvoiceItemForm, PaymentInvoiceEditForm, CostumerForm, CostumerPaymentForm
from project_settings.constants import CURRENCY
from .mixins import MyFormMixin
from reportlab.pdfgen import canvas
import io
from django.http import FileResponse


@method_decorator(staff_member_required, name='dispatch')
class CostumerHomepageView(TemplateView):
    template_name = 'costumers/homepage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['last_10_payments'] = CostumerPayment.objects.all()[:10]
        context['costumers'] = Costumer.objects.all().order_by('balance')[:10]
        return context


@method_decorator(staff_member_required, name='dispatch')
class CostumerListView(ListView):
    template_name = 'list_view.html'
    paginate_by = 50
    model = Costumer

    def get_queryset(self):
        qs = Costumer.objects.all()
        qs = Costumer.filters_data(self.request, qs)
        return qs

    def get_context_data(self, **kwargs):
        context = super(CostumerListView, self).get_context_data(**kwargs)
        page_title = 'Πελατες'
        queryset_table = CostumerTable(self.object_list)
        table_title, create_url = 'Λίστα', reverse('costumers:costumers_create')
        balance_filter, search_filter = [True]*2
        extra_buttons = True
        context.update(locals())
        return context


@method_decorator(staff_member_required, name='dispatch')
class CostumerCreateView(CreateView):
    template_name = 'form_view.html'
    model = Costumer
    form_class = CostumerForm
    success_url = reverse_lazy('costumers:costumer_list')

    def get_success_url(self):
        add_button = self.request.POST.get('add_button', None)
        if add_button:
            return self.new_instance.get_order_url()
        return self.success_url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form_title, back_url = 'Δημιουργία Πελάτη', self.success_url
        context.update(locals())
        return context

    def form_valid(self, form):
        self.new_instance = form.save()
        return super(CostumerCreateView, self).form_valid(form)


@method_decorator(staff_member_required, name='dispatch')
class CostumerDetailView(UpdateView):
    template_name = 'DetailView.html'
    model = Costumer
    form_class = CostumerForm

    def get_success_url(self):
        return self.object.get_edit_url()

    def get_context_data(self, **kwargs):
        context = super(CostumerDetailView, self).get_context_data(**kwargs)
        context['back_url'] = reverse('costumers:costumer_list')
        # data
        payments = CostumerPayment.filters_data(self.request, self.object.payments.all())
        invoices = SalesInvoice.filters_data(self.request, self.object.sale_invoices.all())
        total_payments = payments.aggregate(Sum('value'))['value__sum'] if payments.exists() else 0
        total_invoices = invoices.aggregate(Sum('final_value'))['final_value__sum'] if invoices.exists() else 0
        diff, currency = total_invoices - total_payments, CURRENCY
        context['data_qs'] = sorted(chain(payments, invoices), key=attrgetter('date'), reverse=True)
        context['date_filter'] = True
        get_params = self.request.get_full_path().split('?', 1)[1] if '?' in self.request.get_full_path() else ''
        print_url = reverse('costumers:pdf_costumer_analysis', kwargs={'pk': self.object.id}) + '?' + get_params
        context.update(locals())
        return context

    def form_valid(self, form):
        form.save()
        return super(CostumerDetailView, self).form_valid(form)


@staff_member_required
def delete_costumer_view(request, pk):
    costumer = get_object_or_404(Costumer, id=pk)
    costumer.delete()
    return redirect(reverse('costumer_list'))


@method_decorator(staff_member_required, name='dispatch')
class CreatePaymentFromCostumerDetailView(MyFormMixin, CreateView):
    model = CostumerPayment
    form_class = CostumerPaymentForm

    def get_success_url(self):
        return self.costumer.get_edit_url()

    def get_initial(self):
        initial = super().get_initial()
        self.costumer = get_object_or_404(Costumer, id=self.kwargs['pk'])
        # initial['date'] = datetime.now()
        initial['customer'] = self.costumer
        initial['value'] = self.costumer.balance
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form_title = f'Δημιουργία Πληρωμής -> {self.costumer}'
        back_url = self.costumer.get_edit_url()
        context.update(locals())
        return context


@method_decorator(staff_member_required, name='dispatch')
class EditPaymentFromCostumerView(UpdateView):
    model = CostumerPayment
    template_name = 'costumers/form_view.html'
    form_class = CostumerPaymentForm

    def get_success_url(self):
        return self.object.customer.get_edit_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form_title, back_url = f'Επεξεργασία {self.object}', self.get_success_url()
        delete_url = self.object.get_delete_url()
        context.update(locals())
        return context

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Η Πληρωμη επξεργαστηκε')
        return super().form_valid(form)


@staff_member_required
def delete_payment_from_costumer(request, pk):
    payment = get_object_or_404(CostumerPayment, id=pk)
    payment.delete()
    return redirect(payment.customer.get_edit_url())


@method_decorator(staff_member_required, name='dispatch')
class PrintListView(ListView):
    template_name = 'pdf_templates/list.html'

    model = Costumer

    def get_queryset(self):
        qs = Costumer.objects.filter(balance__gt=0)
        qs = Costumer.filters_data(self.request, qs)
        return qs

    def get_context_data(self, **kwargs):
        context = super(PrintListView, self).get_context_data(**kwargs)
        costumers = Costumer.filters_data(self.request, Costumer.objects.all())
        title = 'Λιστα Πελατών'
        context.update(locals())
        return context


# paymentsInvoice

@method_decorator(staff_member_required, name='dispatch')
class PaymentInvoiceListView(ListView):
    template_name = 'list_view.html'
    model = PaymentInvoice

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['queryset_table'] = PaymentInvoiceTable(self.object_list)
        context['create_url'] = reverse('costumers:payment_invoice_create')
        context['back_url'] = reverse('costumer_homepage')
        return context


@method_decorator(staff_member_required, name='dispatch')
class PaymentInvoiceCreateView(CreateView):
    template_name = 'form_view.html'
    model = PaymentInvoice
    form_class = PaymentInvoiceForm

    def get_initial(self):
        initial = super().get_initial()
        fav_card = MyCard.objects.filter(favorite=True)
        if fav_card.exists():
            initial['card_info'] = fav_card.first()
        return initial

    def get_success_url(self):
        return self.new_instance.get_edit_url()

    def form_valid(self, form):
        self.new_instance = form.save()
        return super(PaymentInvoiceCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Δημιουργια Παραστατικου'
        context['back_url'] = reverse('costumers:home')

        return context


@method_decorator(staff_member_required, name='dispatch')
class PaymentInvoiceCreateFromOrderView(CreateView):
    template_name = 'form_view.html'
    model = PaymentInvoice
    form_class = PaymentInvoiceForm

    def get_initial(self):
        costumer = get_object_or_404(Costumer, id=self.kwargs['pk'])
        initial = super().get_initial()
        fav_card = MyCard.objects.filter(favorite=True)
        if fav_card.exists():
            initial['card_info'] = fav_card.first()
        initial['costumer'] = costumer
        return initial

    def get_success_url(self):
        return self.new_instance.get_edit_url()

    def form_valid(self, form):
        self.new_instance = form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Δημιουργια Παραστατικου'
        context['back_url'] = reverse('costumers:home')

        return context


@method_decorator(staff_member_required, name='dispatch')
class PaymentInvoiceUpdateView(UpdateView):
    template_name = 'costumers/update_invoice.html'
    model = PaymentInvoice
    form_class = PaymentInvoiceEditForm

    def get_success_url(self):
        return self.object.get_edit_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['costumer_form'] = CostumerDetailsForm(self.request.POST or None, instance=self.object.profile)
        context['item_form'] = CreateInvoiceItemForm(self.request.POST or None, initial={'invoice': self.object})
        return context

    def form_valid(self, form):
        form.save()
        return super(PaymentInvoiceUpdateView, self).form_valid(form)


@staff_member_required()
def print_invoice_view(request, pk):
    instance = get_object_or_404(PaymentInvoice, id=pk)
    costumer = instance.profile
    card = instance.card_info
    return render(request, 'costumers/print/index.html', {'instance': instance,
                                                          'costumer': costumer,
                                                          'card_info': card
                                                          })


@staff_member_required
def pdf_costumer_movements_view(request, pk):
    instance = get_object_or_404(Costumer, id=pk)
    date = request.GET.get('date_range', 'None')
    payments = CostumerPayment.filters_data(request,instance.payments.all())
    invoices = SalesInvoice.filters_data(request,instance.sale_invoices.all())
    data_qs = sorted(chain(payments, invoices), key=attrgetter('date'))
    return render(request, 'costumers/print/costumer_amalysis.html', context=locals())


@staff_member_required
def costumer_analysis_view(request, pk):
    costumer = get_object_or_404(Costumer, id=pk)
    order_items = costumer.salesinvoiceitem_set.all()
    order_items = SalesInvoiceItem.filter_data(request, order_items)
    date_filter = [True]
    total_incomes = round(order_items.aggregate(Sum('total_value'))['total_value__sum'] if order_items.exists() else 0, 2)
    total_qty = order_items.aggregate(Sum('qty'))['qty__sum'] if order_items.exists() else 0
    avg = total_incomes/total_qty if total_qty !=0 else 0.00
    product_analysis = order_items.values('product__title').annotate(total_qty=Sum('qty'),
                                                                     total_value=Sum('total_value')
                                                                     ).order_by('product__title')
    return render(request, 'costumers/costumer_analysis.html', context=locals())


def test_pdf(request):
    buffer = io.BytesIO()
    # Creating Canvas
    c = canvas.Canvas(buffer, pagesize=(200, 250), bottomup=0)
    # Logo Section
    # Setting th origin to (10,40)
    c.translate(10, 40)
    # Inverting the scale for getting mirror Image of logo
    c.scale(1, -1)
    # Inserting Logo into the Canvas at required position
    c.drawImage("logo.jpg", 0, 0, width=50, height=30)
    # Title Section
    # Again Inverting Scale For strings insertion
    c.scale(1, -1)
    # Again Setting the origin back to (0,0) of top-left
    c.translate(-10, -40)
    # Setting the font for Name title of company
    c.setFont("Helvetica-Bold", 10)
    # Inserting the name of the company
    c.drawCentredString(125, 20, "XYZ PRIVATE LIMITED")
    # For under lining the title
    c.line(70, 22, 180, 22)
    # Changing the font size for Specifying Address
    c.setFont("Helvetica-Bold", 5)
    c.drawCentredString(125, 30, "Block No. 101, Triveni Apartments, Pitam Pura,")
    c.drawCentredString(125, 35, "New Delhi - 110034, India")
    # Changing the font size for Specifying GST Number of firm
    c.setFont("Helvetica-Bold", 6)
    c.drawCentredString(125, 42, "GSTIN : 07AABCS1429B1Z")
    # Line Seprating the page header from the body
    c.line(5, 45, 195, 45)
    # Document Information
    # Changing the font for Document title
    c.setFont("Courier-Bold", 8)
    c.drawCentredString(100, 55, "TAX-INVOICE")
    # This Block Consist of Costumer Details
    c.roundRect(15, 63, 170, 40, 10, stroke=1, fill=0)
    c.setFont("Times-Bold", 5)
    c.drawRightString(70, 70, "INVOICE No. :")
    c.drawRightString(70, 80, "DATE :")
    c.drawRightString(70, 90, "CUSTOMER NAME :")
    c.drawRightString(70, 100, "PHONE No. :")
    # This Block Consist of Item Description
    c.roundRect(15, 108, 170, 130, 10, stroke=1, fill=0)
    c.line(15, 120, 185, 120)
    c.drawCentredString(25, 118, "SR No.")
    c.drawCentredString(75, 118, "GOODS DESCRIPTION")
    c.drawCentredString(125, 118, "RATE")
    c.drawCentredString(148, 118, "QTY")
    c.drawCentredString(173, 118, "TOTAL")
    # Drawing table for Item Description
    c.line(15, 210, 185, 210)
    c.line(35, 108, 35, 220)
    c.line(115, 108, 115, 220)
    c.line(135, 108, 135, 220)
    c.line(160, 108, 160, 220)
    # Declaration and Signature
    c.line(15, 220, 185, 220)
    c.line(100, 220, 100, 238)
    c.drawString(20, 225, "We declare that above mentioned")
    c.drawString(20, 230, "information is true.")
    c.drawString(20, 235, "(This is system generated invoive)")
    c.drawRightString(180, 235, "Authorised Signatory")
    # End the Page and Start with new
    c.showPage()
    # Saving the PDF
    c.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='hello.pdf')


