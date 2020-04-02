from django.views.generic import ListView, TemplateView, DetailView, CreateView, UpdateView
from django.utils.decorators import method_decorator
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import reverse, get_object_or_404, redirect

from .models import Vendor, InvoiceItem, Invoice, Payment
from project_settings.constants import POSITIVE_INVOICES
from analysis.tools import create_data_for_chart

@method_decorator(staff_member_required, name='dispatch')
class ReportHomepageView(TemplateView):
    template_name = 'warehouse/analysis/homepage.html'


@method_decorator(staff_member_required, name='dispatch')
class InvoiceListAnalysisView(ListView):
    template_name = 'warehouse/analysis/invcoice_list_analysis.html'
    model = Invoice

    def get_queryset(self):
        self.payment_qs = Payment.filters_data(self.request,  Payment.objects.all())
        return self.model.filters_data(self.request, self.model.objects.filter(order_type='a'))

    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        context['date_filter'], context['vendor_filter'] = [True] * 2

        vendor_ids = self.object_list.values_list('vendor__id')
        context['vendors'] = Vendor.objects.filter(id__in=vendor_ids)

        # invoice analysis
        context['vendors_analysis'] = self.object_list.values('vendor__title').annotate(total=Sum('final_value'),
                                                                                        count=Count('id')
                                                                                        ).order_by('vendor__title')
        month_analysis = self.object_list.annotate(month=TruncMonth('date')).values('month').\
            annotate(total=Sum('final_value')).values('month', 'total').order_by('month')

        # totals
        totals_invoice = self.object_list.aggregate(Sum('final_value'))['final_value__sum'] if self.object_list.exists() else 0
        totals_payments = self.payment_qs.aggregate(Sum('value'))['value__sum'] if self.payment_qs.exists() else 0
        diff = totals_invoice - totals_payments
        # payments
        context['month_payments'] = month_payments = self.payment_qs.annotate(month=TruncMonth('date')).values('month').annotate(total=Sum('value')).values('month', 'total').order_by('month')
        payment_analysis = self.payment_qs.values('vendor__title').annotate(total=Sum('value'),
                                                                            count=Count('id')
                                                                           ).order_by('vendor__title')

        context['payment_qs'] = self.payment_qs
        context['chart_analysis'] = create_data_for_chart(month_payments, month_analysis)
        context['month_analysis'] = month_analysis
        context['payment_analysis'] = payment_analysis
        context['total_invoice'], context['total_payments'], context['diff'] = totals_invoice, totals_payments, diff
        return context


@method_decorator(staff_member_required, name='dispatch')
class InvoiceItemListAnalysisView(ListView):
    template_name = 'warehouse/analysis/invoice_item_analysis.html'
    model = InvoiceItem

    def get_queryset(self):
        return InvoiceItem.filters_data(self.request, InvoiceItem.objects.all())

    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        incomes_invoices = self.object_list.filter(invoice__order_type__in=POSITIVE_INVOICES)
        vendors_ids = self.object_list.values_list('vendor')
        context['vendors'] = Vendor.objects.filter(id__in=vendors_ids)
        context['date_filter'], context['vendor_filter'] = [True] * 2
        context['product_analysis'] = incomes_invoices.values('product__title').annotate(total=Sum('total_value'),
                                                                                         count=Sum('qty')
                                                                                         ).order_by('product__title')
        vendor_ids = self.object_list.values_list('vendor__id')
        context['vendors'] = Vendor.objects.filter(id__in=vendor_ids)
        context['vendors__analysis'] = incomes_invoices.values('vendor__title').annotate(total=Sum('total_value'),
                                                                                         qty=Sum('qty')
                                                                                         ).order_by('vendor__title')
        return context





