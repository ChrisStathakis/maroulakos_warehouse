from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum

from payroll.models import Bill, Payroll
from warehouse.models import Payment, Vendor
from catalogue.models import Product
from project_settings.constants import CURRENCY
from point_of_sale.models import SalesInvoice, Costumer
from datetime import date


@method_decorator(staff_member_required, name='dispatch')
class DashboardHomepageView(TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        date_start, date_end,  = date(date.today().year, 1, 1), date(date.today().year, 12, 31)
        incomes_qs = SalesInvoice.objects.filter(date__range=[date_start, date_end])
        context['total_incomes'] = incomes_qs.aggregate(Sum('final_value'))['final_value__sum'] if incomes_qs.exists() else 0.00
        context['total_vendors'] = Vendor.objects.all().aggregate(Sum('balance'))['balance__sum'] if Vendor.objects.exists() else 0.00
        context['total_costumers'] = Costumer.objects.all().aggregate(Sum('balance'))['balance__sum'] if Costumer.objects.exists() else 0.00
        context['total_bills'] = Bill.objects.filter(is_paid=False).aggregate(Sum('value'))['value__sum'] if Bill.objects.filter(is_paid=False) else 0.00
        context['bills'] = Bill.objects.filter(is_paid=False)[:8]
        context['payroll'] = Payroll.objects.filter(is_paid=False)[:8]
        context['vendor_payments'] = Payment.objects.all()[:8]
        context['warning_products'] = Product.objects.filter(safe_warning=True)[:10]
        context['page_title'], context['currency'] = 'Αρχικη Σελιδα', CURRENCY
        return context
