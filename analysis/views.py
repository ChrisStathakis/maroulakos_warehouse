from django.db.models import Sum, FloatField, F
from django.db.models.functions import TruncMonth
from django.shortcuts import render, reverse, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, CreateView, TemplateView, DetailView
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django_tables2 import RequestConfig

from operator import attrgetter
from itertools import chain

from costumers.models import CostumerPayment
from point_of_sale.models import SalesInvoice
from catalogue.models import Product, ProductStorage
from payroll.models import Bill, Payroll
from warehouse.models import Payment, Invoice, Vendor

from .tools import sort_months
from project_settings.constants import CURRENCY


@method_decorator(staff_member_required, name='dispatch')
class AnalysisHomepage(TemplateView):
    template_name = 'analysis/homepage.html'


@method_decorator(staff_member_required, name='dispatch')
class AnalysisSaleIncomeView(ListView):
    model = SalesInvoice
    template_name = 'analysis/analysis_incomes.html'
    paginate_by = 100

    def get_queryset(self):
        return self.model.filters_data(self.request, self.model.objects.all())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        date_filter, currency = True, settings.CURRENCY
        back_url = reverse('analysis:homepage')
        currency = CURRENCY
        total = self.object_list.aggregate(Sum('final_value'))['final_value__sum'] if self.object_list.exists() else 0
        total_taxes = self.object_list.aggregate(Sum('total_taxes'))['total_taxes__sum'] if self.object_list.exists() else 0
        diff = total - total_taxes
        analysis_per_month = self.object_list.annotate(month=TruncMonth('date')).values('month').annotate(
            total=Sum('final_value')).values('month', 'total').order_by('month')
        analysis_per_costumer = self.object_list.values('costumer__eponimia').annotate(
            total=Sum('final_value')).values('costumer__eponimia', 'total').order_by('total')
        analysis_per_payment = self.object_list.values('payment_method__title').annotate(total=Sum('final_value'))\
            .order_by('total')
        context.update(locals())
        return context


@staff_member_required
def warehouse_movements_view(request):
    # collect the data
    invoices = Invoice.filters_data(request, Invoice.objects.all())
    sales = SalesInvoice.filters_data(request, SalesInvoice.objects.all())

    movements = sorted(
            chain(invoices, sales),
            key=attrgetter('date'))
    return render(request, 'analysis/analysis_movements.html', context=locals())


@method_decorator(staff_member_required, name='dispatch')
class AnalysisOutcomeView(TemplateView):
    template_name = 'analysis/analysis_outcome.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        currency = settings.CURRENCY
        back_url = reverse('analysis:homepage')
        date_filter = True

        # collect the data from database
        bills = Bill.filters_data(self.request, Bill.objects.all())
        payrolls = Payroll.filters_data(self.request, Payroll.objects.all())
        invoices = Invoice.filters_data(self.request, Invoice.objects.filter(order_type__in=['a']))

        # analyse bills
        total_bills = bills.aggregate(Sum('final_value'))['final_value__sum'] if bills else 0
        analysis_bills = bills.values('category__title').annotate(total=Sum('final_value')).order_by('-total')
        analysis_bills_per_month = bills.annotate(month=TruncMonth('date_expired')).values('month').annotate(
            total=Sum('final_value')).values('month', 'total').order_by('month')

        # analyse invoice payments
        total_invoices = invoices.aggregate(Sum('final_value'))['final_value__sum'] if invoices else 0
        analysis_invoices = invoices.values('vendor__title').annotate(total=Sum('final_value')).order_by('-total')
        analysis_invoices_per_month = invoices.annotate(month=TruncMonth('date')).values('month').annotate(
            total=Sum('final_value')).values('month', 'total').order_by('month')

        # analyse payrolls
        total_payroll = payrolls.aggregate(Sum('final_value'))['final_value__sum'] if payrolls else 0
        payroll_analysis = payrolls.values('person__title').annotate(total=Sum('final_value')).order_by('-total')
        payroll_analysis_per_month = payrolls.annotate(month=TruncMonth('date_expired')).values('month'). \
            annotate(total=Sum('final_value')).values('month', 'total').order_by('month')

        total_expenses = total_bills + total_payroll + total_invoices

        # create unique months
        months = sort_months([analysis_invoices_per_month, analysis_bills_per_month, payroll_analysis_per_month])
        result_per_months = []
        for month in months:
            data = {
                'month': month,
                'total': 0
            }
            for ele in analysis_invoices_per_month:
                if ele['month'] == month:
                    data['invoice'] = ele['total']
                    data['total'] = data['total'] + ele['total']
            for ele in analysis_bills_per_month:
                if ele['month'] == month:
                    data['bills'] = ele['total']
                    data['total'] = data['total'] + ele['total']
            for ele in payroll_analysis_per_month:
                if ele['month'] == month:
                    data['payroll'] = ele['total']
                    data['total'] = data['total'] + ele['total']
            # put the data together
            data['invoice'] = data['invoice'] if 'invoice' in data.keys() else 0
            data['bills'] = data['bills'] if 'bills' in data.keys() else 0
            data['payroll'] = data['payroll'] if 'payroll' in data.keys() else 0
            result_per_months.append(data)
        context.update(locals())
        return context


@method_decorator(staff_member_required, name='dispatch')
class CashRowView(TemplateView):
    template_name = 'analysis/cash_row.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        currency, date_filter = settings.CURRENCY, True
        back_url = reverse('analysis:homepage')

        # get the incomes
        incomes = CostumerPayment.filters_data(self.request, CostumerPayment.objects.all()).order_by('date')
        total = incomes.aggregate(Sum('value'))['value__sum'] if incomes.exists() else 0

        # vendor_paymets
        vendor_payments = Payment.filters_data(self.request, Payment.objects.all())
        vendor_payments_total = vendor_payments.aggregate(Sum('value'))['value__sum'] if vendor_payments.exists() else 0

        payrolls = Payroll.filters_data(self.request, Payroll.objects.filter(is_paid=True))
        payrolls_total = payrolls.aggregate(Sum('final_value'))['final_value__sum'] if payrolls.exists() else 0

        bills = Bill.filters_data(self.request, Bill.objects.filter(is_paid=True))
        bills_total = bills.aggregate(Sum('final_value'))['final_value__sum'] if bills.exists() else 0

        total_expenses = vendor_payments_total + bills_total + payrolls_total
        expenses_query = sorted(
            chain(bills, vendor_payments, payrolls),
            key=attrgetter('date'))
        diff = round(total - total_expenses, 2)
        context.update(locals())
        return context


@method_decorator(staff_member_required, name='dispatch')
class BalanceSheetView(TemplateView):
    template_name = 'analysis/balance_sheet.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        date_filter, currency = True, settings.CURRENCY

        # incomes
        incomes = SalesInvoice.filters_data(self.request, SalesInvoice.objects.all())
        incomes_per_month = incomes.annotate(month=TruncMonth('date')).values('month').annotate(
            total=Sum('final_value')).values('month', 'total').order_by('month')
        incomes_total = incomes.aggregate(Sum('value'))['value__sum'] if incomes.exists() else 0

        # vendors data

        invoices = Invoice.filters_data(self.request, Invoice.objects.all())
        invoices_per_month = invoices.annotate(month=TruncMonth('date')).values('month').annotate(
            total=Sum('final_value')).values('month', 'total').order_by('month')
        invoices_total = invoices.aggregate(Sum('final_value'))['final_value__sum'] if invoices.exists() else 0
        vendors = invoices.values('vendor__title', 'vendor__balance').annotate(total=Sum('final_value')).order_by(
            '-total')[:15]

        # payments
        payments = Payment.filters_data(self.request, Payment.objects.all())
        payments_total = payments.aggregate(Sum('value'))['value__sum'] if payments.exists() else 0
        vendors_remaining = invoices_total - payments_total

        # bills
        bills = Bill.filters_data(self.request, Bill.objects.all())
        bills_per_month = bills.annotate(month=TruncMonth('date_expired')).values('month').annotate(
            total=Sum('final_value')).values('month', 'total').order_by('month')
        bills_total = bills.aggregate(Sum('final_value'))['final_value__sum'] if bills.exists() else 0
        bills_paid_total = bills.filter(is_paid=True).aggregate(Sum('final_value'))['final_value__sum'] if bills.filter(
            is_paid=True).exists() else 0
        bills_per_bill = bills.values('category__title').annotate(total_pay=Sum('final_value'),
                                                                  paid_value=Sum('paid_value')) \
            .order_by('category__title')

        # payrolls
        payrolls = Payroll.filters_data(self.request, Payroll.objects.all())
        payroll_per_month = payrolls.annotate(month=TruncMonth('date_expired')).values('month').annotate(
            total=Sum('final_value')).values('month', 'total').order_by('month')
        payrolls_total = payrolls.aggregate(Sum('final_value'))['final_value__sum'] if payrolls.exists() else 0
        payrolls_paid_total = payrolls.filter(is_paid=True).aggregate(Sum('final_value'))[
            'final_value__sum'] if payrolls.filter(is_paid=True).exists() else 0
        payroll_per_person = payrolls.values('person__title').annotate(total_pay=Sum('final_value'),
                                                                       paid_value=Sum('paid_value')) \
            .order_by('person__title')




        # diffs
        totals = bills_total + payrolls_total + invoices_total
        paid_totals = bills_paid_total + payrolls_paid_total + payments_total

        diff_paid = incomes_total - paid_totals
        diff_obligations = incomes_total - totals

        # chart analysis
        months = sort_months(
            [incomes_per_month, invoices_per_month, payroll_per_month, bills_per_month])

        result_per_months = []
        for month in months:
            data = {
                'month': month,
                'total': 0
            }
            for ele in incomes_per_month:
                if ele['month'] == month:
                    data['income'] = ele['total']
                    data['total'] = data['total'] + ele['total']
            for ele in invoices_per_month:
                if ele['month'] == month:
                    data['invoice'] = ele['total']
                    data['total'] = data['total'] + ele['total']
            for ele in bills_per_month:
                if ele['month'] == month:
                    data['bills'] = ele['total']
                    data['total'] = data['total'] + ele['total']
            for ele in payroll_per_month:
                if ele['month'] == month:
                    data['payroll'] = ele['total']
                    data['total'] = data['total'] + ele['total']
            data['invoice'] = data['invoice'] if 'invoice' in data.keys() else 0
            data['bills'] = data['bills'] if 'bills' in data.keys() else 0
            data['payroll'] = data['payroll'] if 'payroll' in data.keys() else 0
            data['generic'] = data['generic'] if 'generic' in data.keys() else 0
            result_per_months.append(data)

        context.update(locals())
        return context


@method_decorator(staff_member_required, name='dispatch')
class LogisticRowView(TemplateView):
    template_name = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[""] = ''
        return context


@method_decorator(staff_member_required, name='dispatch')
class StoreInventoryView(TemplateView):
    model = Product
    template_name = 'analysis/store_inventory.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.objects.all()
        vendor_products = ProductStorage.objects.all()
        products_total = products.aggregate(total=Sum(F('price_buy') * F('qty'), output_field=FloatField())) \
            if products.exists() else 0
        vendor_products = vendor_products.values('taxes_modifier').annotate(
            total=Sum(F('product__qty') * F('product__price_buy'), output_field=FloatField())).values('taxes_modifier',
                                                                                                      'total').order_by(
            'taxes_modifier')
        context.update(locals())
        return context